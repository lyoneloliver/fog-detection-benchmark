from __future__ import annotations

import copy
from fractions import Fraction

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from scipy.signal import butter, resample_poly, sosfiltfilt
from torch.utils.data import DataLoader, TensorDataset

from models.base import FoGModel


class SpectralCNN(nn.Module):
    def __init__(self, in_channels: int = 3):
        super().__init__()
        self.conv1 = nn.Sequential(
            nn.Conv1d(in_channels, 128, kernel_size=4, padding="valid"),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2),
        )
        self.conv2 = nn.Sequential(
            nn.Conv1d(128, 64, kernel_size=4, padding="valid"),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=2),
        )
        self.conv3 = nn.Sequential(
            nn.Conv1d(64, 32, kernel_size=4, padding="valid"),
            nn.ReLU(),
        )
        self.pool = nn.AdaptiveAvgPool1d(1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.conv3(x)
        return self.pool(x).squeeze(-1)


class MultiHeadSelfAttention(nn.Module):
    def __init__(
        self,
        embed_dim: int = 32,
        num_heads: int = 3,
        head_dim: int = 32,
        dropout: float = 0.25,
    ):
        super().__init__()
        self.num_heads = num_heads
        self.head_dim = head_dim
        inner_dim = num_heads * head_dim
        self.query = nn.Linear(embed_dim, inner_dim)
        self.key = nn.Linear(embed_dim, inner_dim)
        self.value = nn.Linear(embed_dim, inner_dim)
        self.output = nn.Linear(inner_dim, embed_dim)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch, steps, _ = x.shape

        def split_heads(layer: nn.Linear) -> torch.Tensor:
            return (
                layer(x)
                .reshape(batch, steps, self.num_heads, self.head_dim)
                .transpose(1, 2)
            )

        query = split_heads(self.query)
        key = split_heads(self.key)
        value = split_heads(self.value)
        scores = torch.matmul(query, key.transpose(-2, -1))
        scores = scores / (self.head_dim**0.5)
        weights = self.dropout(torch.softmax(scores, dim=-1))
        attended = torch.matmul(weights, value)
        attended = attended.transpose(1, 2).reshape(
            batch, steps, self.num_heads * self.head_dim
        )
        return self.output(attended)


class TransformerEncoderBlock(nn.Module):
    def __init__(
        self,
        embed_dim: int = 32,
        num_heads: int = 3,
        head_dim: int = 32,
        dropout: float = 0.25,
    ):
        super().__init__()
        self.attention = MultiHeadSelfAttention(
            embed_dim=embed_dim,
            num_heads=num_heads,
            head_dim=head_dim,
            dropout=dropout,
        )
        self.attention_dropout = nn.Dropout(dropout)
        self.attention_norm = nn.LayerNorm(embed_dim, eps=1e-3)
        self.feed_forward = nn.Sequential(
            nn.Conv1d(embed_dim, 16, kernel_size=1),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Conv1d(16, embed_dim, kernel_size=1),
        )
        self.feed_forward_dropout = nn.Dropout(dropout)
        self.feed_forward_norm = nn.LayerNorm(embed_dim, eps=1e-3)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.attention_norm(x + self.attention_dropout(self.attention(x)))
        feed_forward = self.feed_forward(x.transpose(1, 2)).transpose(1, 2)
        return self.feed_forward_norm(x + self.feed_forward_dropout(feed_forward))


class FOGTransformerNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.spectral_cnn = SpectralCNN(in_channels=3)
        self.encoder = nn.Sequential(
            *[
                TransformerEncoderBlock(
                    embed_dim=32,
                    num_heads=3,
                    head_dim=32,
                    dropout=0.25,
                )
                for _ in range(3)
            ]
        )
        self.classifier = nn.Sequential(
            nn.Linear(32, 80),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(80, 40),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(40, 1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch, steps, bins, channels = x.shape
        x = x.reshape(batch * steps, bins, channels).transpose(1, 2)
        x = self.spectral_cnn(x).reshape(batch, steps, 32)
        x = self.encoder(x)
        x = x.mean(dim=1)
        return self.classifier(x).squeeze(-1)


class SpectralTransformer(FoGModel):
    name = "transformer"

    def __init__(
        self,
        seed: int = 0,
        max_epochs: int = 150,
        patience: int = 7,
        lr: float = 6e-4,
        batch_size: int = 512,
        target_fs: int = 40,
        window_samples: int = 128,
        overlap: float = 0.75,
    ):
        self.seed = seed
        self.max_epochs = max_epochs
        self.patience = patience
        self.lr = lr
        self.batch_size = batch_size
        self.target_fs = target_fs
        self.window_samples = window_samples
        self.overlap = overlap
        self.step_samples = int(round(window_samples * (1.0 - overlap)))
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.net: FOGTransformerNet | None = None
        self.channel_min: np.ndarray | None = None
        self.channel_max: np.ndarray | None = None
        self.train_class_counts: tuple[int, int] | None = None
        self.positive_class_weight: float | None = None
        self._threshold_data: list[
            tuple[np.ndarray, np.ndarray, int]
        ] = []
        self.num_epochs_trained = 0

    def _preprocess(self, recording) -> tuple[np.ndarray, np.ndarray]:
        raw6 = np.asarray(recording.raw6, dtype=np.float32)
        raw = raw6[:, :3].copy()
        ratio = Fraction(self.target_fs, int(recording.fs)).limit_denominator()
        if ratio.numerator != ratio.denominator:
            raw = resample_poly(
                raw,
                ratio.numerator,
                ratio.denominator,
                axis=0,
            ).astype(np.float32)

        if len(raw) > 1:
            lowpass = butter(2, 15.0, btype="lowpass", fs=self.target_fs, output="sos")
            highpass = butter(3, 0.2, btype="highpass", fs=self.target_fs, output="sos")
            for sos in (lowpass, highpass):
                padlen = min(3 * (2 * len(sos) + 1), len(raw) - 1)
                raw = sosfiltfilt(sos, raw, axis=0, padlen=padlen).astype(np.float32)

        y_source = np.asarray(recording.y).reshape(-1)
        source_indices = np.rint(
            np.arange(len(raw), dtype=np.float64) * recording.fs / self.target_fs
        ).astype(np.int64)
        y = (y_source[np.clip(source_indices, 0, len(y_source) - 1)] > 0).astype(
            np.int8
        )
        return raw, y

    def _fit_normalizer(self, recordings: list) -> None:
        minima = []
        maxima = []
        for recording in recordings:
            raw, _ = self._preprocess(recording)
            minima.append(raw.min(axis=0))
            maxima.append(raw.max(axis=0))
        self.channel_min = np.min(np.stack(minima), axis=0).astype(np.float32)
        self.channel_max = np.max(np.stack(maxima), axis=0).astype(np.float32)
        constant_channels = self.channel_max == self.channel_min
        self.channel_max[constant_channels] = self.channel_min[constant_channels] + 1.0

    def _normalize(self, raw: np.ndarray) -> np.ndarray:
        if self.channel_min is None or self.channel_max is None:
            return raw.astype(np.float32)
        normalized = 2.0 * (raw - self.channel_min) / (
            self.channel_max - self.channel_min
        ) - 1.0
        return np.clip(normalized, -1.0, 1.0).astype(np.float32)

    def _window_starts(self, n_samples: int) -> list[int]:
        if n_samples <= self.window_samples:
            return [0]
        last_start = n_samples - self.window_samples
        starts = list(range(0, last_start + 1, self.step_samples))
        if starts[-1] != last_start:
            starts.append(last_start)
        return starts

    def _spectral_frames(
        self,
        normalized: np.ndarray,
        labels: np.ndarray | None,
    ) -> tuple[np.ndarray, np.ndarray | None, list[int], list[int]]:
        starts = self._window_starts(len(normalized))
        padded = normalized
        if len(padded) < self.window_samples:
            pad_mode = "reflect" if len(padded) > 1 else "edge"
            padded = np.pad(
                padded,
                ((0, self.window_samples - len(padded)), (0, 0)),
                mode=pad_mode,
            )
        windows = np.lib.stride_tricks.sliding_window_view(
            padded,
            self.window_samples,
            axis=0,
        )
        windows = windows[np.asarray(starts)].transpose(0, 2, 1)
        spectrum = np.abs(
            np.fft.fft(windows, axis=1)[:, : self.window_samples // 2]
        )
        frame_array = (spectrum / self.window_samples).astype(np.float32)
        if labels is None:
            return frame_array, None, starts, []

        starts_array = np.asarray(starts, dtype=np.int64)
        ends_array = np.minimum(
            starts_array + self.window_samples,
            len(labels),
        )
        label_prefix = np.concatenate(
            ([0], np.cumsum(labels, dtype=np.int64))
        )
        positive_counts = label_prefix[ends_array] - label_prefix[starts_array]
        lengths = ends_array - starts_array
        positive = positive_counts / lengths > 0.5
        negative = positive_counts == 0
        label_array = np.full(len(starts), -1.0, dtype=np.float32)
        label_array[positive] = 1.0
        label_array[negative] = 0.0
        valid_indices = np.flatnonzero(positive | negative).tolist()
        return frame_array, label_array, starts, valid_indices

    @staticmethod
    def _make_sequences(frames: np.ndarray) -> np.ndarray:
        padded = np.concatenate(
            [np.repeat(frames[:1], 3, axis=0), frames],
            axis=0,
        )
        return np.lib.stride_tricks.sliding_window_view(
            padded,
            4,
            axis=0,
        ).transpose(0, 3, 1, 2).astype(np.float32, copy=True)

    def _recording_examples(
        self,
        recording,
        with_labels: bool,
    ) -> tuple[np.ndarray, np.ndarray | None, list[int], int]:
        raw, sample_labels = self._preprocess(recording)
        normalized = self._normalize(raw)
        frames, frame_labels, starts, valid_indices = self._spectral_frames(
            normalized,
            sample_labels if with_labels else None,
        )
        sequences = self._make_sequences(frames)
        if with_labels:
            valid = np.asarray(valid_indices, dtype=np.int64)
            if len(valid) == 0:
                return (
                    np.empty((0, 4, 64, 3), dtype=np.float32),
                    np.empty((0,), dtype=np.float32),
                    starts,
                    len(raw),
                )
            return sequences[valid], frame_labels[valid], starts, len(raw)
        return sequences, None, starts, len(raw)

    def _collect_examples(
        self,
        recordings: list,
    ) -> tuple[np.ndarray, np.ndarray]:
        x_parts = []
        y_parts = []
        for recording in recordings:
            x, y, _, _ = self._recording_examples(recording, with_labels=True)
            if len(x):
                x_parts.append(x)
                y_parts.append(y)
        return np.concatenate(x_parts), np.concatenate(y_parts)

    def fit(self, recordings: list) -> None:
        torch.manual_seed(self.seed)
        rng = np.random.default_rng(self.seed)
        subjects = np.asarray(sorted({recording.subject for recording in recordings}))
        if len(subjects) > 1:
            shuffled = rng.permutation(subjects)
            n_val = min(max(1, int(round(len(subjects) * 0.2))), len(subjects) - 1)
            val_subjects = set(shuffled[:n_val].tolist())
            train_recordings = [
                r for r in recordings if r.subject not in val_subjects
            ]
            val_recordings = [r for r in recordings if r.subject in val_subjects]
        else:
            train_recordings = recordings
            val_recordings = recordings

        self._fit_normalizer(train_recordings)
        x_train, y_train = self._collect_examples(train_recordings)
        x_val, y_val = self._collect_examples(val_recordings)
        train_dataset = TensorDataset(
            torch.from_numpy(x_train),
            torch.from_numpy(y_train),
        )
        val_dataset = TensorDataset(
            torch.from_numpy(x_val),
            torch.from_numpy(y_val),
        )
        generator = torch.Generator().manual_seed(self.seed)
        train_loader = DataLoader(
            train_dataset,
            batch_size=self.batch_size,
            shuffle=True,
            generator=generator,
            pin_memory=self.device.type == "cuda",
        )
        val_loader = DataLoader(
            val_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            pin_memory=self.device.type == "cuda",
        )

        class_counts = np.bincount(y_train.astype(np.int64), minlength=2)
        negative_count, positive_count = (int(class_counts[0]), int(class_counts[1]))
        if negative_count == 0 or positive_count == 0:
            positive_class_weight = 1.0
        else:
            positive_class_weight = negative_count / positive_count
        self.train_class_counts = (negative_count, positive_count)
        self.positive_class_weight = float(positive_class_weight)

        self.net = FOGTransformerNet().to(self.device)
        criterion = nn.BCEWithLogitsLoss(
            pos_weight=torch.tensor(
                [positive_class_weight],
                dtype=torch.float32,
                device=self.device,
            )
        )
        optimizer = optim.Adam(self.net.parameters(), lr=self.lr)
        best_loss = float("inf")
        best_state = copy.deepcopy(self.net.state_dict())
        epochs_without_improvement = 0
        self.num_epochs_trained = 0

        for epoch in range(self.max_epochs):
            self.net.train()
            for batch_x, batch_y in train_loader:
                batch_x = batch_x.to(self.device, non_blocking=True)
                batch_y = batch_y.to(self.device, non_blocking=True)
                optimizer.zero_grad(set_to_none=True)
                loss = criterion(self.net(batch_x), batch_y)
                loss.backward()
                optimizer.step()

            self.net.eval()
            val_loss = 0.0
            with torch.no_grad():
                for batch_x, batch_y in val_loader:
                    batch_x = batch_x.to(self.device, non_blocking=True)
                    batch_y = batch_y.to(self.device, non_blocking=True)
                    val_loss += criterion(self.net(batch_x), batch_y).item() * len(
                        batch_y
                    )
            val_loss /= len(val_loader.dataset)
            if not np.isfinite(val_loss):
                break
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
        sequences, _, starts, n_resampled = self._recording_examples(
            recording,
            with_labels=False,
        )
        self.net.eval()
        probabilities = []
        with torch.no_grad():
            for start in range(0, len(sequences), self.batch_size):
                batch = torch.from_numpy(
                    sequences[start : start + self.batch_size]
                ).to(self.device)
                probabilities.append(torch.sigmoid(self.net(batch)).cpu().numpy())
        window_probs = np.concatenate(probabilities).astype(np.float32)

        probability_sum = np.zeros(n_resampled, dtype=np.float64)
        coverage = np.zeros(n_resampled, dtype=np.float64)
        for start, probability in zip(starts, window_probs):
            end = min(start + self.window_samples, n_resampled)
            probability_sum[start:end] += probability
            coverage[start:end] += 1.0
        uncovered = coverage == 0
        if np.any(uncovered):
            covered = np.flatnonzero(~uncovered)
            if len(covered):
                probability_sum[uncovered] = np.interp(
                    np.flatnonzero(uncovered),
                    covered,
                    probability_sum[covered] / coverage[covered],
                )
            else:
                probability_sum[uncovered] = 0.5
            coverage[uncovered] = 1.0
        resampled_probs = (probability_sum / coverage).astype(np.float32)
        source_indices = np.rint(
            np.arange(recording.n_samples, dtype=np.float64)
            * self.target_fs
            / recording.fs
        ).astype(np.int64)
        return resampled_probs[
            np.clip(source_indices, 0, n_resampled - 1)
        ].astype(np.float32)

    def card(self) -> dict:
        n_params = (
            sum(parameter.numel() for parameter in self.net.parameters())
            if self.net is not None
            else sum(
                parameter.numel()
                for parameter in FOGTransformerNet().parameters()
            )
        )
        return {
            "nama": self.name,
            "n_parameter": int(n_params),
            "hiperparameter": {
                "target_fs_hz": self.target_fs,
                "lowpass_order": 2,
                "lowpass_cutoff_hz": 15.0,
                "highpass_order": 3,
                "highpass_cutoff_hz": 0.2,
                "normalisasi": "min-max per sumbu ke [-1, 1], dihitung dari pasien training",
                "window_samples": self.window_samples,
                "window_seconds": self.window_samples / self.target_fs,
                "overlap": self.overlap,
                "fft_bins": self.window_samples // 2,
                "spectral_context_windows": 4,
                "cnn_filters": [128, 64, 32],
                "cnn_kernel_size": 4,
                "cnn_padding": "valid",
                "transformer_blocks": 3,
                "attention_heads": 3,
                "attention_head_size": 32,
                "layer_norm_epsilon": 1e-3,
                "mlp_units": [80, 40, 1],
                "lr": self.lr,
                "batch_size": self.batch_size,
                "max_epochs": self.max_epochs,
                "patience": self.patience,
                "epochs_trained": self.num_epochs_trained,
                "validation_split": "20% pasien pada data training untuk early stopping",
                "loss": "BCEWithLogitsLoss dengan pos_weight=jumlah_negatif/jumlah_positif",
                "jumlah_window_train_non_fog": (
                    self.train_class_counts[0]
                    if self.train_class_counts is not None
                    else None
                ),
                "jumlah_window_train_fog": (
                    self.train_class_counts[1]
                    if self.train_class_counts is not None
                    else None
                ),
                "pos_weight_fog": self.positive_class_weight,
            },
            "deviasi": [
                "Paper memakai akselerometer pinggang 200 Hz; Figshare memakai sensor tulang kering 128 Hz yang di-resample ke 40 Hz.",
                "Hanya 3 kanal akselerometer yang dipakai; kanal giroskop diabaikan sesuai domain spektral paper.",
                "Label Figshare biner (FoG/non-FoG), sedangkan paper mencakup kelas tambahan (berjalan dan berdiri).",
                "Window dilabeli positif jika FoG >50%, negatif jika 0%, dan window campuran dibuang.",
                "Normalisasi min-max ke rentang [-1, 1] dihitung murni dari data training untuk mencegah kebocoran data.",
                "Loss training menggunakan pos_weight berdasarkan rasio kelas untuk mengatasi ketidakseimbangan data.",
                "Early stopping dan pemilihan threshold divalidasi pada subjek internal agar set uji LOSO tidak tercemar.",
                "Runner benchmark memakai rentang threshold 0.01-0.99 (paper 0.2-0.8) demi kompatibilitas sistem.",
                "Implementasi memakai padding valid sesuai default Conv1D Keras yang dirujuk paper.",
                "Probabilitas level-window diproyeksikan dan dirata-ratakan pada area overlap untuk memenuhi antarmuka sampel benchmark."
            ],
        }


def factory(seed: int = 0) -> SpectralTransformer:
    return SpectralTransformer(seed=seed)