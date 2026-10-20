from __future__ import annotations

import copy

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

from models.base import FoGModel


class DeepFoGNet(nn.Module):
    def __init__(self, num_classes: int = 2, window_length: int = 384):
        super().__init__()
        self.acc_branch = self._branch()
        self.gyr_branch = self._branch()
        self.dropout = nn.Dropout(0.5)
        window_length = max(6, window_length)
        self.fc = nn.Linear(80 * (window_length // 6), num_classes)

    @staticmethod
    def _branch() -> nn.Sequential:
        return nn.Sequential(
            nn.Conv1d(3, 100, kernel_size=10, padding="same"),
            nn.ReLU(),
            nn.MaxPool1d(kernel_size=3, stride=3),
            nn.Conv1d(100, 40, kernel_size=10, padding="same"),
            nn.ReLU(),
            nn.AvgPool1d(kernel_size=2, stride=2),
            nn.Flatten(start_dim=1),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        acc = self.acc_branch(x[:, :, :3].transpose(1, 2))
        gyr = self.gyr_branch(x[:, :, 3:].transpose(1, 2))
        return self.fc(self.dropout(torch.cat((acc, gyr), dim=1)))


class DeepFoG(FoGModel):
    name = "deepfog"

    def __init__(
        self,
        seed: int = 0,
        max_epochs: int = 50,
        patience: int = 7,
        lr: float = 0.001,
        batch_size: int = 32,
        win_sec: float = 3.0,
        stride_sec: float = 0.25,
        target_fs: float = 128.0,
    ):
        self.seed = seed
        self.max_epochs = max_epochs
        self.patience = patience
        self.lr = lr
        self.batch_size = batch_size
        self.win_sec = win_sec
        self.stride_sec = stride_sec
        self.target_fs = target_fs
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.net: DeepFoGNet | None = None
        self.channel_scale: np.ndarray | None = None
        self.num_epochs_trained = 0
        self._threshold_data: list[tuple[np.ndarray, np.ndarray, int]] = []

    def _window_starts(self, n_samples: int, win_len: int, step_len: int) -> list[int]:
        if n_samples <= win_len:
            return [0]
        starts = list(range(0, n_samples - win_len + 1, step_len))
        last_start = n_samples - win_len
        if starts[-1] != last_start:
            starts.append(last_start)
        return starts

    def _preprocess(
        self,
        recording,
        include_labels: bool,
    ) -> tuple[np.ndarray, np.ndarray | None]:
        raw = np.asarray(recording.raw6, dtype=np.float32)
        y = np.asarray(recording.y, dtype=np.int8) if include_labels else None
        if int(recording.fs) == int(self.target_fs):
            return raw, y

        n_samples = max(1, int(round(len(raw) * self.target_fs / recording.fs)))
        source_positions = np.arange(len(raw), dtype=np.float64)
        target_positions = np.linspace(
            0.0,
            max(0, len(raw) - 1),
            num=n_samples,
        )
        resampled = np.column_stack(
            [
                np.interp(target_positions, source_positions, raw[:, channel])
                for channel in range(raw.shape[1])
            ]
        ).astype(np.float32)
        if y is None:
            return resampled, None
        label_indices = np.rint(target_positions).astype(np.int64)
        return resampled, y[np.clip(label_indices, 0, len(y) - 1)]

    def _make_windows(
        self,
        recording,
        include_labels: bool,
    ) -> tuple[np.ndarray, np.ndarray | None, list[int]]:
        raw, y = self._preprocess(recording, include_labels)
        win_len = int(round(self.win_sec * self.target_fs))
        step_len = max(1, int(round(self.stride_sec * self.target_fs)))
        starts = self._window_starts(len(raw), win_len, step_len)
        windows = []
        labels = []
        events = []
        if y is not None:
            transitions = np.diff(np.pad(y.astype(np.int8), (1, 1)))
            events = np.column_stack(
                (
                    np.flatnonzero(transitions == 1),
                    np.flatnonzero(transitions == -1),
                )
            )

        for start in starts:
            end = min(start + win_len, len(raw))
            window = raw[start:end]
            if len(window) < win_len:
                pad_width = win_len - len(window)
                mode = "reflect" if len(window) > 1 else "edge"
                window = np.pad(window, ((0, pad_width), (0, 0)), mode=mode)
            windows.append(window)

        if y is not None:
            event_starts = events[:, 0]
            event_ends = events[:, 1]
            starts_array = np.asarray(starts, dtype=np.int64)
            ends_array = np.minimum(starts_array + win_len, len(raw))
            for offset in range(0, len(starts), 256):
                stop = min(offset + 256, len(starts))
                window_starts = starts_array[offset:stop, None]
                window_ends = ends_array[offset:stop, None]
                overlap = np.maximum(
                    0,
                    np.minimum(window_ends, event_ends[None, :])
                    - np.maximum(window_starts, event_starts[None, :]),
                )
                contained = (
                    (window_starts <= event_starts[None, :])
                    & (event_ends[None, :] <= window_ends)
                )
                labels.extend(
                    np.any(
                        contained | (overlap >= win_len / 2),
                        axis=1,
                    ).astype(np.int64)
                )

        label_array = np.asarray(labels, dtype=np.int64) if y is not None else None
        return np.asarray(windows, dtype=np.float32), label_array, starts

    def _normalize(self, windows: np.ndarray) -> np.ndarray:
        return (windows / self.channel_scale).astype(np.float32)

    def _dataset(self, recordings: list) -> tuple[np.ndarray, np.ndarray]:
        windows = []
        labels = []
        for recording in recordings:
            rec_windows, rec_labels, _ = self._make_windows(recording, include_labels=True)
            windows.append(self._normalize(rec_windows))
            labels.append(rec_labels)
        return np.concatenate(windows), np.concatenate(labels)

    def fit(self, recordings: list) -> None:
        if not recordings:
            return

        torch.manual_seed(self.seed)
        np.random.seed(self.seed)
        self._threshold_data = []
        subjects = np.asarray(sorted({recording.subject for recording in recordings}))
        rng = np.random.default_rng(self.seed)
        if len(subjects) > 1:
            shuffled_subjects = rng.permutation(subjects)
            n_val_subjects = min(
                max(1, int(round(len(subjects) * 0.2))),
                len(subjects) - 1,
            )
            val_subjects = set(shuffled_subjects[:n_val_subjects].tolist())
            train_recordings = [
                recording for recording in recordings if recording.subject not in val_subjects
            ]
            val_recordings = [
                recording for recording in recordings if recording.subject in val_subjects
            ]
        else:
            train_recordings = recordings
            val_recordings = recordings

        self.channel_scale = np.maximum.reduce(
            [np.max(np.abs(recording.raw6), axis=0) for recording in train_recordings]
        ).astype(np.float32)
        self.channel_scale[self.channel_scale == 0] = 1.0

        x_train, y_train = self._dataset(train_recordings)
        x_val, y_val = self._dataset(val_recordings)
        x_train_tensor = torch.from_numpy(x_train)
        y_train_tensor = torch.from_numpy(y_train)
        x_val_tensor = torch.from_numpy(x_val)
        y_val_tensor = torch.from_numpy(y_val)

        generator = torch.Generator().manual_seed(self.seed)
        train_loader = DataLoader(
            TensorDataset(x_train_tensor, y_train_tensor),
            batch_size=self.batch_size,
            shuffle=True,
            generator=generator,
        )
        val_loader = DataLoader(
            TensorDataset(x_val_tensor, y_val_tensor),
            batch_size=self.batch_size,
            shuffle=False,
        )

        class_counts = torch.bincount(y_train_tensor, minlength=2).float()
        class_weights = class_counts.sum() / (2.0 * class_counts.clamp_min(1.0))
        window_length = int(round(self.win_sec * self.target_fs))
        self.net = DeepFoGNet(window_length=window_length).to(self.device)
        criterion = nn.CrossEntropyLoss(weight=class_weights.to(self.device))
        optimizer = optim.Adam(self.net.parameters(), lr=self.lr)
        best_loss = float("inf")
        best_state = copy.deepcopy(self.net.state_dict())
        epochs_without_improvement = 0

        for epoch in range(self.max_epochs):
            self.net.train()
            for batch_x, batch_y in train_loader:
                batch_x = batch_x.to(self.device)
                batch_y = batch_y.to(self.device)
                optimizer.zero_grad()
                loss = criterion(self.net(batch_x), batch_y)
                loss.backward()
                optimizer.step()

            self.net.eval()
            val_loss = 0.0
            with torch.no_grad():
                for batch_x, batch_y in val_loader:
                    batch_x = batch_x.to(self.device)
                    batch_y = batch_y.to(self.device)
                    val_loss += criterion(self.net(batch_x), batch_y).item() * len(batch_y)
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
        windows, _, starts = self._make_windows(recording, include_labels=False)
        windows = self._normalize(windows)
        self.net.eval()
        probabilities = []
        with torch.no_grad():
            for start in range(0, len(windows), self.batch_size):
                batch = torch.from_numpy(windows[start : start + self.batch_size])
                logits = self.net(batch.to(self.device))
                probabilities.extend(torch.softmax(logits, dim=1)[:, 1].cpu().numpy())

        n_samples = len(recording.raw6)
        n_resampled = max(1, int(round(n_samples * self.target_fs / recording.fs)))
        differences = np.zeros(n_resampled + 1, dtype=np.float64)
        counts = np.zeros(n_resampled + 1, dtype=np.int32)
        win_len = int(round(self.win_sec * self.target_fs))
        for start, probability in zip(starts, probabilities):
            end = min(start + win_len, n_samples)
            differences[start] += probability
            differences[end] -= probability
            counts[start] += 1
            counts[end] -= 1
        total = np.cumsum(differences[:-1])
        coverage = np.cumsum(counts[:-1])
        probabilities = np.divide(
            total,
            coverage,
            out=np.zeros_like(total),
            where=coverage > 0,
        ).astype(np.float32)
        if len(probabilities) == n_samples:
            return probabilities
        source_times = np.arange(len(probabilities), dtype=np.float64) / self.target_fs
        target_times = np.arange(n_samples, dtype=np.float64) / float(recording.fs)
        return np.interp(
            target_times,
            source_times,
            probabilities,
            left=float(probabilities[0]),
            right=float(probabilities[-1]),
        ).astype(np.float32)

    def card(self) -> dict:
        parameter_count = (
            sum(parameter.numel() for parameter in self.net.parameters())
            if self.net is not None
            else sum(parameter.numel() for parameter in DeepFoGNet().parameters())
        )
        return {
            "nama": self.name,
            "n_parameter": parameter_count,
            "hiperparameter": {
                "arsitektur": "dua cabang Conv1D, ACC dan GYR diproses terpisah",
                "filters_per_cabang": [100, 40],
                "kernel_size": 10,
                "max_pool_size": 3,
                "average_pool_size": 2,
                "global_average_pooling": False,
                "temporal_features_flattened": True,
                "dropout": 0.5,
                "window_sec": self.win_sec,
                "step_sec": self.stride_sec,
                "target_fs": self.target_fs,
                "batch_size": self.batch_size,
                "learning_rate": self.lr,
                "max_epochs": self.max_epochs,
                "patience": self.patience,
                "epochs_trained": self.num_epochs_trained,
                "class_weighted_loss": True,
                "seed": self.seed,
            },
            "deviasi": [
                "Paper DeepFoG memakai satu CNN dengan enam kanal gabungan; adaptasi ini memakai dua cabang terpisah ACC dan GYR sesuai permintaan multi-cabang.",
                "Paper memprediksi tiga kelas FoG, Stop, dan Walking-with-Turns dari sensor pergelangan tangan. Figshare hanya memiliki label biner FoG/tidak-FoG dan sensor tulang kering, sehingga output diadaptasi menjadi dua kelas.",
                "Window 3 detik mengikuti paper. Paper menyebut overlap 0.25 detik, sedangkan benchmark memakai langkah 0.25 detik (overlap 2.75 detik) untuk mempertahankan resolusi temporal yang lebih rapat; pilihan ini bukan interpretasi literal paper. Label FoG memakai aturan episode utuh atau overlap minimal setengah panjang window.",
                "Normalisasi maksimum per kanal dihitung hanya dari rekaman latih untuk menghindari penggunaan statistik pasien validasi/uji.",
                "Class-weighted cross entropy ditambahkan untuk ketimpangan kelas; paper menggunakan categorical cross entropy dan tidak menyebut pembobotan kelas.",
                "Threshold dipilih dari prediksi pasien validasi internal yang tidak digunakan untuk memperbarui bobot model; pasien uji LOSO tetap tidak digunakan untuk pemilihan threshold.",
                "Global average pooling dihilangkan agar fitur urutan waktu dipertahankan sebelum fully connected layer, sesuai alur konvolusi-pooling-dense pada arsitektur paper."
            ],
        }


def factory(seed: int = 0) -> DeepFoG:
    return DeepFoG(seed=seed)
