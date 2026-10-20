from __future__ import annotations

from fractions import Fraction

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from scipy.signal import resample_poly
from torch.utils.data import DataLoader, Dataset

from models.base import FoGModel


class InitialTCN(nn.Module):
    dilations = (1, 3, 9, 27, 81)
    receptive_field = 1 + 2 * sum(dilations)

    def __init__(self, in_channels: int = 6, hidden_features: int = 32):
        super().__init__()
        layers: list[nn.Module] = []
        channels = in_channels
        for dilation in self.dilations:
            layers.extend(
                [
                    nn.Conv1d(
                        channels,
                        hidden_features,
                        kernel_size=3,
                        dilation=dilation,
                    ),
                    nn.ReLU(),
                ]
            )
            channels = hidden_features
        self.temporal = nn.Sequential(*layers)
        self.classifier = nn.Linear(hidden_features, 2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        features = self.temporal(x.transpose(1, 2)).transpose(1, 2)
        return self.classifier(features)


class _WindowDataset(Dataset):
    def __init__(
        self,
        signals: list[np.ndarray],
        labels: list[np.ndarray],
        window_samples: int,
    ):
        self.window_samples = window_samples
        self.center_offset = window_samples // 2
        self.signals: list[np.ndarray] = []
        self.labels = labels
        self.ends = np.cumsum([len(y) for y in labels], dtype=np.int64)
        for signal in signals:
            self.signals.append(
                np.pad(
                    signal,
                    ((self.center_offset, window_samples - self.center_offset), (0, 0)),
                    mode="constant",
                )
            )

    def __len__(self) -> int:
        return int(self.ends[-1])

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        recording_index = int(np.searchsorted(self.ends, index, side="right"))
        start = 0 if recording_index == 0 else int(self.ends[recording_index - 1])
        sample_index = index - start
        window = self.signals[recording_index][
            sample_index : sample_index + self.window_samples
        ]
        signal_tensor = torch.from_numpy(window.copy())
        label_tensor = torch.tensor(
            int(self.labels[recording_index][sample_index]),
            dtype=torch.long,
        )
        return signal_tensor, label_tensor


class _RefinementStage(nn.Module):
    dilations = (1, 2, 4, 8, 16, 32, 64, 128)

    def __init__(self, hidden_features: int = 32):
        super().__init__()
        self.input_projection = nn.Conv1d(2, hidden_features, kernel_size=1)
        self.layers = nn.ModuleList(
            nn.Conv1d(
                hidden_features,
                hidden_features,
                kernel_size=3,
                padding=dilation,
                dilation=dilation,
            )
            for dilation in self.dilations
        )
        self.output_projection = nn.Conv1d(
            hidden_features,
            2,
            kernel_size=1,
        )

    def forward(self, probabilities: torch.Tensor) -> torch.Tensor:
        features = self.input_projection(probabilities)
        for layer in self.layers:
            features = F.relu(features + layer(features))
        return self.output_projection(features)


class _MultiStageTCNRefiner(nn.Module):
    def __init__(self, stages: int = 4, hidden_features: int = 32):
        super().__init__()
        self.stages = nn.ModuleList(
            _RefinementStage(hidden_features) for _ in range(stages)
        )

    def forward(self, initial_probabilities: torch.Tensor) -> list[torch.Tensor]:
        stage_input = initial_probabilities
        outputs = []
        for stage in self.stages:
            logits = stage(stage_input)
            outputs.append(logits)
            stage_input = torch.softmax(logits, dim=1)
        return outputs


class TCNYang2024(FoGModel):
    name = "tcn-yang-2024"

    def __init__(
        self,
        seed: int = 0,
        max_epochs: int = 15,
        batch_size: int = 1024,
        lr: float = 0.0005,
        target_fs: int = 64,
        window_samples: int = 256,
    ):
        self.seed = seed
        self.max_epochs = max_epochs
        self.batch_size = batch_size
        self.lr = lr
        self.target_fs = target_fs
        self.window_samples = window_samples
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.net: InitialTCN | None = None
        self.refiner: _MultiStageTCNRefiner | None = None
        self._threshold_data: list[
            tuple[np.ndarray, np.ndarray, int]
        ] = []
        self.num_epochs_trained = 0
        self.refinement_epochs_trained = 0
        self.channel_mean: np.ndarray | None = None
        self.channel_std: np.ndarray | None = None

    @property
    def training_window_samples(self) -> int:
        return self.window_samples

    def _preprocess(self, recording) -> tuple[np.ndarray, np.ndarray]:
        raw = np.asarray(recording.raw6, dtype=np.float32)
        labels = np.asarray(recording.y, dtype=np.int64)
        ratio = Fraction(self.target_fs, int(round(recording.fs))).limit_denominator()
        if ratio.numerator != ratio.denominator:
            raw = resample_poly(
                raw,
                ratio.numerator,
                ratio.denominator,
                axis=0,
            ).astype(np.float32)
            source_indices = np.rint(
                np.arange(len(raw), dtype=np.float64)
                * float(recording.fs)
                / self.target_fs
            ).astype(np.int64)
            labels = labels[np.clip(source_indices, 0, len(labels) - 1)]
        return raw.astype(np.float32, copy=False), labels.astype(np.int64, copy=False)

    def _normalize(self, signal: np.ndarray) -> np.ndarray:
        if self.channel_mean is None or self.channel_std is None:
            return signal.astype(np.float32, copy=False)
        return (
            (signal - self.channel_mean[None, :])
            / self.channel_std[None, :]
        ).astype(np.float32)

    def fit(self, recordings: list) -> None:
        torch.manual_seed(self.seed)
        np.random.seed(self.seed)
        rng = np.random.default_rng(self.seed)
        subjects = np.asarray(sorted({r.subject for r in recordings}))
        if len(subjects) > 1:
            shuffled = rng.permutation(subjects)
            n_val = min(max(1, int(round(len(subjects) * 0.2))), len(subjects) - 1)
            val_subjects = set(shuffled[:n_val].tolist())
            train_recordings = [
                r for r in recordings if r.subject not in val_subjects
            ]
            val_recordings = [
                r for r in recordings if r.subject in val_subjects
            ]
        else:
            train_recordings = recordings
            val_recordings = []

        signals: list[np.ndarray] = []
        labels: list[np.ndarray] = []
        for recording in train_recordings:
            signal, target = self._preprocess(recording)
            signals.append(signal)
            labels.append(target)

        stacked_signals = np.concatenate(signals, axis=0)
        self.channel_mean = stacked_signals.mean(axis=0).astype(np.float32)
        self.channel_std = np.maximum(
            stacked_signals.std(axis=0),
            1e-6,
        ).astype(np.float32)
        signals = [self._normalize(signal) for signal in signals]

        class_counts = self._training_class_counts(labels).astype(np.float64)
        class_weights = self._class_weights(class_counts)
        refinement_counts = np.bincount(
            np.concatenate(labels),
            minlength=2,
        ).astype(np.float64)
        refinement_class_weights = self._class_weights(refinement_counts)

        self.net = InitialTCN().to(self.device)
        self._fit_initial(signals, labels, class_weights)
        self._fit_refiner(signals, labels, refinement_class_weights)
        if val_recordings:
            self._threshold_data = [
                (
                    np.asarray(recording.y).ravel().copy(),
                    self.predict_proba(recording),
                    int(recording.fs),
                )
                for recording in val_recordings
            ]

    def threshold_predictions(self) -> list[tuple[np.ndarray, np.ndarray, int]]:
        return [
            (labels.copy(), probabilities.copy(), fs)
            for labels, probabilities, fs in self._threshold_data
        ]

    def _fit_initial(
        self,
        signals: list[np.ndarray],
        labels: list[np.ndarray],
        class_weights: np.ndarray,
    ) -> None:
        batches: list[list[tuple[int, int, int]]] = []
        pending: list[tuple[int, int, int]] = []
        pending_size = 0
        for recording_index, signal in enumerate(signals):
            start = 0
            while start < len(signal):
                chunk_size = min(self.batch_size - pending_size, len(signal) - start)
                pending.append((recording_index, start, start + chunk_size))
                start += chunk_size
                pending_size += chunk_size
                if pending_size == self.batch_size:
                    batches.append(pending)
                    pending = []
                    pending_size = 0
        if pending:
            batches.append(pending)

        padded_signals = [
            np.pad(
                signal,
                (
                    (InitialTCN.receptive_field // 2,
                     InitialTCN.receptive_field // 2),
                    (0, 0),
                ),
                mode="constant",
            )
            for signal in signals
        ]
        targets = [torch.from_numpy(target) for target in labels]

        optimizer = optim.Adam(
            self.net.parameters(),
            lr=self.lr,
            betas=(0.9, 0.999),
            amsgrad=True,
        )
        scheduler = optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.95)
        rng = np.random.default_rng(self.seed)
        receptive_field = InitialTCN.receptive_field
        class_weights_tensor = torch.from_numpy(class_weights).to(self.device)

        for epoch in range(self.max_epochs):
            self.net.train()
            for batch_index in rng.permutation(len(batches)):
                weighted_loss = None
                weight_sum = torch.zeros((), device=self.device)
                for recording_index, start, stop in batches[int(batch_index)]:
                    chunk = np.ascontiguousarray(
                        padded_signals[recording_index][
                            start : stop + receptive_field - 1
                        ].T,
                        dtype=np.float32,
                    )
                    batch_x = torch.from_numpy(chunk).unsqueeze(0).to(self.device)
                    batch_y = targets[recording_index][start:stop].to(self.device)
                    logits = self.net(batch_x.transpose(1, 2))[0]
                    chunk_loss = F.cross_entropy(
                        logits,
                        batch_y,
                        weight=class_weights_tensor,
                        reduction="sum",
                    )
                    weighted_loss = (
                        chunk_loss
                        if weighted_loss is None
                        else weighted_loss + chunk_loss
                    )
                    weight_sum = weight_sum + class_weights_tensor[batch_y].sum()

                optimizer.zero_grad(set_to_none=True)
                loss = weighted_loss / weight_sum
                loss.backward()
                optimizer.step()
            scheduler.step()
            self.num_epochs_trained = epoch + 1

    def _fit_initial_windows(
        self,
        signals: list[np.ndarray],
        labels: list[np.ndarray],
        class_weights: np.ndarray,
    ) -> None:
        dataset = self._build_training_dataset(signals, labels)
        loader = DataLoader(
            dataset,
            batch_size=self.batch_size,
            shuffle=True,
            generator=torch.Generator().manual_seed(self.seed),
            pin_memory=self.device.type == "cuda",
        )
        criterion = nn.CrossEntropyLoss(
            weight=torch.from_numpy(class_weights).to(self.device)
        )
        optimizer = optim.Adam(
            self.net.parameters(),
            lr=self.lr,
            betas=(0.9, 0.999),
            amsgrad=True,
        )
        scheduler = optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.95)
        center_output_index = (
            self.training_window_samples // 2
            - InitialTCN.receptive_field // 2
        )

        for epoch in range(self.max_epochs):
            self.net.train()
            for batch_x, batch_y in loader:
                batch_x = batch_x.to(self.device, non_blocking=True)
                batch_y = batch_y.to(self.device, non_blocking=True)
                optimizer.zero_grad(set_to_none=True)
                logits = self.net(batch_x)[:, center_output_index, :]
                loss = criterion(logits, batch_y)
                loss.backward()
                optimizer.step()
            scheduler.step()
            self.num_epochs_trained = epoch + 1

    def _build_training_dataset(
        self,
        signals: list[np.ndarray],
        labels: list[np.ndarray],
    ) -> Dataset:
        return _WindowDataset(signals, labels, self.window_samples)

    def _training_class_counts(self, labels: list[np.ndarray]) -> np.ndarray:
        return np.bincount(np.concatenate(labels), minlength=2)

    @staticmethod
    def _class_weights(class_counts: np.ndarray) -> np.ndarray:
        present = class_counts > 0
        weights = np.zeros(2, dtype=np.float32)
        weights[present] = (
            class_counts.sum() / (int(present.sum()) * class_counts[present])
        ).astype(np.float32)
        return weights

    def _initial_probabilities(self, raw: np.ndarray) -> torch.Tensor:
        padding = InitialTCN.receptive_field // 2
        padded = np.pad(raw, ((padding, padding), (0, 0)), mode="constant")
        probabilities: list[np.ndarray] = []
        self.net.eval()
        inference_device = next(self.net.parameters()).device
        with torch.no_grad():
            for start in range(0, len(raw), max(self.batch_size, 1)):
                stop = min(start + max(self.batch_size, 1), len(raw))
                chunk = np.ascontiguousarray(
                    padded[start : stop + 2 * padding].T,
                    dtype=np.float32,
                )
                logits = self.net(
                    torch.from_numpy(chunk)
                    .unsqueeze(0)
                    .to(inference_device)
                    .transpose(1, 2)
                )[0]
                probabilities.append(
                    torch.softmax(logits, dim=1).cpu().numpy()
                )
        return torch.from_numpy(
            np.concatenate(probabilities, axis=0).T[None, :, :].astype(
                np.float32,
                copy=False,
            )
        )

    @staticmethod
    def _smoothing_loss(
        logits: torch.Tensor,
        tau: float = 4.0,
    ) -> torch.Tensor:
        if logits.shape[2] < 2:
            return logits.sum() * 0.0
        log_probabilities = torch.log_softmax(logits, dim=1)
        differences = log_probabilities[:, :, 1:] - log_probabilities[:, :, :-1]
        return differences.square().sum(dim=1).clamp(max=tau).mean()

    def _fit_refiner(
        self,
        signals: list[np.ndarray],
        labels: list[np.ndarray],
        class_weights: np.ndarray,
    ) -> None:
        self.refiner = _MultiStageTCNRefiner().to(self.device)
        optimizer = optim.Adam(
            self.refiner.parameters(),
            lr=self.lr,
            betas=(0.9, 0.999),
            amsgrad=True,
        )
        scheduler = optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.95)
        criterion = nn.CrossEntropyLoss(
            weight=torch.from_numpy(class_weights).to(self.device)
        )
        initial_predictions = [
            self._initial_probabilities(signal)
            for signal in signals
        ]
        targets = [
            torch.from_numpy(target.astype(np.int64, copy=False))
            .unsqueeze(0)
            for target in labels
        ]

        for epoch in range(self.max_epochs):
            self.refiner.train()
            for initial, target in zip(initial_predictions, targets):
                initial = initial.to(self.device)
                target = target.to(self.device)
                optimizer.zero_grad(set_to_none=True)
                stage_logits = self.refiner(initial)
                loss = sum(
                    criterion(logits, target)
                    + 0.15 * self._smoothing_loss(logits, tau=4.0)
                    for logits in stage_logits
                )
                loss.backward()
                optimizer.step()
            scheduler.step()
            self.refinement_epochs_trained = epoch + 1

    def predict_proba(self, recording) -> np.ndarray:
        if self.refiner is None:
            return self.fallback_probabilities(recording)
        raw, _ = self._preprocess(recording)
        raw = self._normalize(raw)
        initial = self._initial_probabilities(raw).to(self.device)
        self.refiner.eval()
        with torch.no_grad():
            logits = self.refiner(initial)[-1]
            probabilities = torch.softmax(logits, dim=1)[0, 1].cpu().numpy()
        probabilities = probabilities.astype(np.float32, copy=False)
        probabilities = np.nan_to_num(
            probabilities,
            nan=0.5,
            posinf=1.0,
            neginf=0.0,
        )
        if len(probabilities) == len(recording.y):
            return probabilities
        source_times = np.arange(len(probabilities), dtype=np.float64) / self.target_fs
        target_times = np.arange(len(recording.y), dtype=np.float64) / float(recording.fs)
        return np.interp(
            target_times,
            source_times,
            probabilities,
            left=float(probabilities[0]),
            right=float(probabilities[-1]),
        ).astype(np.float32)

    def card(self) -> dict:
        initial_net = self.net or InitialTCN()
        refinement_net = self.refiner or _MultiStageTCNRefiner()
        n_parameters = sum(
            parameter.numel()
            for model in (initial_net, refinement_net)
            for parameter in model.parameters()
        )
        return {
            "nama": self.name,
            "n_parameter": int(n_parameters),
            "hiperparameter": {
                "hidden_features": 32,
                "tcn_layers": 5,
                "kernel_size": 3,
                "dilation": list(InitialTCN.dilations),
                "window_samples": self.window_samples,
                "target_fs_hz": self.target_fs,
                "batch_size": self.batch_size,
                "epochs": self.max_epochs,
                "optimizer": "Amsgrad (beta=(0.9, 0.999))",
                "learning_rate": self.lr,
                "learning_rate_decay_per_epoch": 0.95,
                "loss": "class-weighted cross-entropy",
                "trained_epochs": self.num_epochs_trained,
                "refinement_stages": 4,
                "refinement_layers_per_stage": 8,
                "refinement_dilation": list(_RefinementStage.dilations),
                "refinement_batch_size": 1,
                "refinement_loss": "weighted cross-entropy + smoothing (tau=4, lambda=0.15)",
                "refinement_epochs_trained": self.refinement_epochs_trained,
                "threshold_calibration": (
                    "held-out training subjects"
                    if self._threshold_data
                    else "runner fallback when no validation subject exists"
                ),
            },
            "deviasi": [
                "Paper menggunakan lima IMU (30 kanal); adaptasi ini hanya memakai satu IMU tibia (6 kanal) sesuai ketersediaan kanal Figshare.",
                "Data Figshare di-resample ke 64 Hz agar 256 sampel tetap merepresentasikan jendela waktu 4 detik seperti pada paper.",
                "Model disesuaikan untuk mengembalikan probabilitas biner per sampel sesuai spesifikasi antarmuka benchmark.",
                "Jumlah epoch pelatihan diturunkan menjadi 15 untuk initial TCN dan 15 untuk refiner agar komputasi CPU lebih efisien.",
                "Evaluasi mengikuti kerangka LOSO benchmark, bukan partisi dan evaluasi spesifik dari paper.",
                "Threshold dikalibrasi dari subjek validasi internal data latih, terpisah dari subjek uji LOSO."
            ],
        }


def factory(seed: int = 0) -> TCNYang2024:
    return TCNYang2024(seed=seed)