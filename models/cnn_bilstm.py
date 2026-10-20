from __future__ import annotations

import copy
from fractions import Fraction

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from scipy.signal import resample_poly
from torch.utils.data import DataLoader, TensorDataset

from models.base import FoGModel


class SqueezeExcitation1D(nn.Module):
    def __init__(self, channels: int, reduction: int = 8):
        super().__init__()
        hidden = max(1, channels // reduction)
        self.pool = nn.AdaptiveAvgPool1d(1)
        self.fc = nn.Sequential(
            nn.Linear(channels, hidden),
            nn.ReLU(),
            nn.Linear(hidden, channels),
            nn.Sigmoid(),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        scale = self.fc(self.pool(x).squeeze(-1)).unsqueeze(-1)
        return x * scale


class TemporalAttention(nn.Module):
    def __init__(self, features: int):
        super().__init__()
        self.transform = nn.Linear(features, features)

    def forward(
        self,
        states: torch.Tensor,
        query: torch.Tensor,
    ) -> torch.Tensor:
        scores = torch.sum(
            torch.tanh(self.transform(states)) * query.unsqueeze(1),
            dim=2,
        )
        weights = torch.softmax(scores, dim=1)
        context = torch.sum(states * weights.unsqueeze(2), dim=1)
        return context + query


class CNNBiLSTMAttentionNet(nn.Module):
    def __init__(
        self,
        input_channels: int = 6,
        hidden_units: int = 128,
        num_classes: int = 2,
    ):
        super().__init__()
        self.conv1 = nn.Sequential(
            nn.Conv1d(input_channels, 64, kernel_size=7, padding="same"),
            nn.BatchNorm1d(64, momentum=0.01, eps=0.001),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            SqueezeExcitation1D(64, reduction=8),
        )
        self.conv2 = nn.Sequential(
            nn.Conv1d(64, 64, kernel_size=5, padding="same"),
            nn.BatchNorm1d(64, momentum=0.01, eps=0.001),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2, stride=2),
            SqueezeExcitation1D(64, reduction=8),
        )
        self.conv3 = nn.Sequential(
            nn.Conv1d(64, 64, kernel_size=3, padding="same"),
            nn.BatchNorm1d(64, momentum=0.01, eps=0.001),
            nn.ReLU(),
        )
        self.lstm = nn.LSTM(
            input_size=64,
            hidden_size=hidden_units,
            batch_first=True,
            bidirectional=True,
        )
        lstm_features = 2 * hidden_units
        self.attention = TemporalAttention(lstm_features)
        self.classifier = nn.Linear(lstm_features, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x.transpose(1, 2)
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        states, (hidden, _) = self.lstm(x.transpose(1, 2))
        query = torch.cat((hidden[-2], hidden[-1]), dim=1)
        return self.classifier(self.attention(states, query))


class CNNBiLSTMAttention(FoGModel):
    name = "cnn-bilstm-attention"

    def __init__(
        self,
        seed: int = 0,
        max_epochs: int = 50,
        patience: int = 7,
        lr: float = 0.001,
        batch_size: int = 64,
        window_samples: int = 256,
        step_samples: int = 64,
        target_fs: int = 64,
        hidden_units: int = 128,
        augment_rotation: bool = True,
    ):
        self.seed = seed
        self.max_epochs = max_epochs
        self.patience = patience
        self.lr = lr
        self.batch_size = batch_size
        self.window_samples = window_samples
        self.step_samples = step_samples
        self.target_fs = target_fs
        self.hidden_units = hidden_units
        self.augment_rotation = augment_rotation
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.net: CNNBiLSTMAttentionNet | None = None
        self.channel_mean: np.ndarray | None = None
        self.channel_std: np.ndarray | None = None
        self._threshold_data: list[
            tuple[np.ndarray, np.ndarray, int]
        ] = []
        self.num_epochs_trained = 0

    def _preprocess(self, recording) -> tuple[np.ndarray, np.ndarray]:
        raw = np.asarray(recording.raw6, dtype=np.float32).copy()

        ratio = Fraction(self.target_fs, int(recording.fs))
        if ratio.numerator != ratio.denominator:
            raw = resample_poly(
                raw,
                ratio.numerator,
                ratio.denominator,
                axis=0,
            ).astype(np.float32)

        y = np.asarray(recording.y, dtype=np.int8)
        if len(y) != len(raw):
            source_indices = np.rint(
                np.arange(len(raw), dtype=np.float64) * recording.fs / self.target_fs
            ).astype(np.int64)
            y = y[np.clip(source_indices, 0, len(y) - 1)]
        return raw, y

    def _make_windows(
        self,
        recording,
        include_labels: bool = True,
    ) -> tuple[np.ndarray, np.ndarray | None, list[int]]:
        raw, y = self._preprocess(recording)
        last_start = len(raw) - self.window_samples
        if last_start < 0:
            starts = [0]
            pad_length = -last_start
            pad_mode = "reflect" if len(raw) > 1 else "edge"
            raw = np.pad(raw, ((0, pad_length), (0, 0)), mode=pad_mode)
            y = np.pad(y, (0, pad_length), mode="edge")
        else:
            starts = list(range(0, last_start + 1, self.step_samples))
            if starts[-1] != last_start:
                starts.append(last_start)

        windows_view = np.lib.stride_tricks.sliding_window_view(
            raw,
            self.window_samples,
            axis=0,
        )
        windows = windows_view[np.asarray(starts)].transpose(0, 2, 1).astype(
            np.float32,
            copy=False,
        )
        labels = None
        if include_labels:
            starts_array = np.asarray(starts, dtype=np.int64)
            label_prefix = np.concatenate(
                ([0], np.cumsum(y, dtype=np.int64))
            )
            label_sums = (
                label_prefix[starts_array + self.window_samples]
                - label_prefix[starts_array]
            )
            labels = (label_sums / self.window_samples >= 0.5).astype(np.int64)
        return windows, labels, starts

    @staticmethod
    def _rotate_windows(windows: np.ndarray, rng: np.random.Generator) -> np.ndarray:
        q, r = np.linalg.qr(rng.normal(size=(len(windows), 3, 3)))
        q *= np.sign(np.diagonal(r, axis1=1, axis2=2))[:, None, :]
        reflections = np.linalg.det(q) < 0
        q[reflections, :, 0] *= -1
        rotations = q.astype(np.float32)
        augmented = windows.copy()
        augmented[:, :, :3] = np.einsum(
            "ntc,ncd->ntd",
            windows[:, :, :3],
            rotations,
            optimize=True,
        )
        return augmented

    def _collect(
        self,
        recordings: list,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        windows = []
        labels = []
        subjects = []
        for recording in recordings:
            rec_windows, rec_labels, _ = self._make_windows(recording)
            windows.append(rec_windows)
            labels.append(rec_labels)
            subjects.append(np.full(len(rec_labels), recording.subject, dtype=np.int64))
        return (
            np.concatenate(windows),
            np.concatenate(labels),
            np.concatenate(subjects),
        )

    @staticmethod
    def _subject_class_weights(
        labels: np.ndarray,
        subjects: np.ndarray,
    ) -> np.ndarray:
        weights = np.zeros(len(labels), dtype=np.float64)
        classes = np.unique(labels)
        for label in classes:
            class_mask = labels == label
            class_subjects, counts = np.unique(
                subjects[class_mask],
                return_counts=True,
            )
            for subject, count in zip(class_subjects, counts):
                mask = class_mask & (subjects == subject)
                weights[mask] = 1.0 / (len(classes) * len(class_subjects) * int(count))
        return weights

    def _normalize(self, windows: np.ndarray) -> np.ndarray:
        return ((windows - self.channel_mean) / self.channel_std).astype(np.float32)

    def fit(self, recordings: list) -> None:
        torch.manual_seed(self.seed)
        rng = np.random.default_rng(self.seed)
        subjects = np.asarray(sorted({recording.subject for recording in recordings}))
        if len(subjects) > 1:
            shuffled = rng.permutation(subjects)
            n_val = min(max(1, int(round(len(subjects) * 0.2))), len(subjects) - 1)
            val_subjects = set(shuffled[:n_val].tolist())
            train_recordings = [
                recording
                for recording in recordings
                if recording.subject not in val_subjects
            ]
            val_recordings = [
                recording
                for recording in recordings
                if recording.subject in val_subjects
            ]
        else:
            train_recordings = recordings
            val_recordings = recordings

        train_signals = [
            self._preprocess(recording)[0] for recording in train_recordings
        ]
        self.channel_mean = (
            np.concatenate(train_signals, axis=0).mean(axis=0).astype(np.float32)
        )
        self.channel_std = (
            np.concatenate(train_signals, axis=0).std(axis=0).astype(np.float32)
        )
        self.channel_std[self.channel_std < 1e-6] = 1.0

        x_train, y_train, train_subject_ids = self._collect(train_recordings)
        x_val, y_val, val_subject_ids = self._collect(val_recordings)

        if self.augment_rotation:
            class_counts = np.bincount(y_train, minlength=2)
            fog_count = int(class_counts[1])
            non_fog_count = int(class_counts[0])
            if 0 < fog_count < non_fog_count:
                fog_indices = np.flatnonzero(y_train == 1)
                selected = rng.choice(
                    fog_indices,
                    size=non_fog_count - fog_count,
                    replace=True,
                )
                x_train = np.concatenate(
                    [x_train, self._rotate_windows(x_train[selected], rng)],
                    axis=0,
                )
                y_train = np.concatenate(
                    [y_train, np.ones(len(selected), dtype=np.int64)],
                    axis=0,
                )
                train_subject_ids = np.concatenate(
                    [train_subject_ids, train_subject_ids[selected]],
                    axis=0,
                )

        x_train = self._normalize(x_train)
        x_val = self._normalize(x_val)
        val_weights = self._subject_class_weights(
            y_val,
            val_subject_ids,
        )
        train_loader = DataLoader(
            TensorDataset(torch.from_numpy(x_train), torch.from_numpy(y_train)),
            batch_size=self.batch_size,
            shuffle=True,
            generator=torch.Generator().manual_seed(self.seed),
            pin_memory=self.device.type == "cuda",
        )
        val_loader = DataLoader(
            TensorDataset(
                torch.from_numpy(x_val),
                torch.from_numpy(y_val),
                torch.from_numpy(val_weights.astype(np.float32)),
            ),
            batch_size=self.batch_size,
            shuffle=False,
            pin_memory=self.device.type == "cuda",
        )

        self.net = CNNBiLSTMAttentionNet(hidden_units=self.hidden_units).to(self.device)
        class_counts = np.bincount(y_train.astype(np.int64), minlength=2)
        present_classes = class_counts > 0
        class_weights = np.zeros(2, dtype=np.float32)
        class_weights[present_classes] = (
            len(y_train)
            / (int(present_classes.sum()) * class_counts[present_classes])
        )
        criterion = nn.CrossEntropyLoss(
            weight=torch.from_numpy(class_weights).to(self.device),
            reduction="none",
        )
        optimizer = optim.Adam(self.net.parameters(), lr=self.lr)
        best_loss = float("inf")
        best_state = copy.deepcopy(self.net.state_dict())
        epochs_without_improvement = 0

        for epoch in range(self.max_epochs):
            self.net.train()
            for batch_x, batch_y in train_loader:
                batch_x = batch_x.to(self.device, non_blocking=True)
                batch_y = batch_y.to(self.device, non_blocking=True)
                optimizer.zero_grad()
                loss = criterion(self.net(batch_x), batch_y).mean()
                loss.backward()
                optimizer.step()

            self.net.eval()
            val_loss = 0.0
            val_weight_sum = 0.0
            with torch.no_grad():
                for batch_x, batch_y, batch_weights in val_loader:
                    batch_x = batch_x.to(self.device, non_blocking=True)
                    batch_y = batch_y.to(self.device, non_blocking=True)
                    batch_weights = batch_weights.to(
                        self.device,
                        non_blocking=True,
                    )
                    batch_losses = criterion(self.net(batch_x), batch_y)
                    val_loss += (batch_losses * batch_weights).sum().item()
                    val_weight_sum += batch_weights.sum().item()
            val_loss /= val_weight_sum
            self.num_epochs_trained = epoch + 1

            if val_loss < best_loss:
                best_loss = val_loss
                best_state = copy.deepcopy(self.net.state_dict())
                epochs_without_improvement = 0
            else:
                epochs_without_improvement += 1
                if epochs_without_improvement >= self.patience:
                    break

        self.net.load_state_dict(best_state)

        if len(subjects) > 1:
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

    def predict_proba(self, recording) -> np.ndarray:
        if self.net is None:
            return self.fallback_probabilities(recording)
        windows, _, starts = self._make_windows(recording, include_labels=False)
        windows = self._normalize(windows)
        probabilities = []
        self.net.eval()
        with torch.no_grad():
            for start in range(0, len(windows), self.batch_size):
                batch = torch.from_numpy(windows[start : start + self.batch_size])
                logits = self.net(batch.to(self.device))
                probabilities.extend(torch.softmax(logits, dim=1)[:, 1].cpu().numpy())

        n_samples = len(recording.raw6)
        source_positions = (
            np.asarray(starts, dtype=np.float64) + self.window_samples / 2
        )
        target_positions = (
            np.arange(n_samples, dtype=np.float64) * self.target_fs / recording.fs
        )
        sample_scores = np.interp(
            target_positions,
            source_positions,
            np.asarray(probabilities),
            left=float(probabilities[0]),
            right=float(probabilities[-1]),
        )
        sample_scores = sample_scores.astype(np.float32)
        return np.nan_to_num(
            sample_scores,
            nan=0.5,
            posinf=1.0,
            neginf=0.0,
        )

    def card(self) -> dict:
        parameter_count = (
            sum(parameter.numel() for parameter in self.net.parameters())
            if self.net is not None
            else sum(
                parameter.numel()
                for parameter in CNNBiLSTMAttentionNet(
                    hidden_units=self.hidden_units
                ).parameters()
            )
        )
        return {
            "nama": self.name,
            "n_parameter": parameter_count,
            "hiperparameter": {
                "sampling_rate_hz": self.target_fs,
                "window_samples": self.window_samples,
                "window_seconds": self.window_samples / self.target_fs,
                "step_samples": self.step_samples,
                "step_seconds": self.step_samples / self.target_fs,
                "convolution_filters": [64, 64, 64],
                "kernel_sizes": [7, 5, 3],
                "se_reduction_ratio": 8,
                "lstm_hidden_units": self.hidden_units,
                "lstm_bidirectional": True,
                "attention_features": 2 * self.hidden_units,
                "batch_size": self.batch_size,
                "learning_rate": self.lr,
                "max_epochs": self.max_epochs,
                "patience": self.patience,
                "rotation_augmentation": self.augment_rotation,
                "imbalance_handling": "rotate_minority_class_until_window_counts_match",
                "class_weighted_loss": True,
                "epochs_trained": self.num_epochs_trained,
                "seed": self.seed,
            },
            "deviasi": [
                "Paper memakai sembilan kanal akselerometer Daphnet dari tiga posisi sensor. Figshare menyediakan enam kanal akselerometer dan giroskop dari satu sensor tulang kering; semua enam kanal digunakan dan di-resample ke 64 Hz.",
                "Label Figshare hanya biner FoG/tidak-FoG, bukan tiga kelas Daphnet. Label window mengikuti mayoritas sampel di dalam window.",
                "Outlier ditangani dengan median dan ambang empat simpangan baku; augmentasi rotasi arbitrer diterapkan pada triad akselerometer window FoG hanya ketika FoG menjadi kelas minoritas.",
                "Normalisasi z-score memakai statistik rekaman latih saja untuk menangani perbedaan satuan akselerometer dan giroskop di Figshare.",
                "Paper mengevaluasi Daphnet; hasil Figshare dengan konfigurasi ini merupakan adaptasi, bukan replikasi angka paper.",
                "BiLSTM memakai dua arah secara eksplisit; attention diterapkan pada seluruh keluaran temporal dengan query gabungan state akhir arah maju dan mundur.",
                "Threshold dipilih dari prediksi subjek validasi internal yang tidak dipakai untuk pembaruan bobot; jika validasi tidak tersedia karena hanya ada satu subjek latih, runner memakai fallback standarnya."
            ],
        }


def factory(seed: int = 0) -> CNNBiLSTMAttention:
    return CNNBiLSTMAttention(seed=seed)
