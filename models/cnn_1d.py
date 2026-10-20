from __future__ import annotations

import numpy as np
import torch
import torch.nn as nn
from scipy.signal import resample
from scipy.spatial.transform import Rotation as R
from torch.utils.data import DataLoader, TensorDataset

from models.base import FoGModel


class ODayCNN1DModule(nn.Module):
    def __init__(self, in_channels: int = 6, window_length: int = 128):
        super().__init__()

        self.conv_block = nn.Sequential(
            nn.Conv1d(in_channels, 16, kernel_size=17, padding="same"),
            nn.Dropout(0.5),
            nn.MaxPool1d(kernel_size=2),
            nn.Conv1d(16, 16, kernel_size=17, padding="same"),
            nn.Dropout(0.5),
            nn.MaxPool1d(kernel_size=2),
        )

        with torch.no_grad():
            sample = torch.zeros(1, in_channels, max(1, window_length))
            flatten_dim = int(self.conv_block(sample).numel())

        self.fc = nn.Sequential(nn.Linear(flatten_dim, 10), nn.ReLU(), nn.Linear(10, 1))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.conv_block(x)
        x = torch.flatten(x, start_dim=1)
        x = self.fc(x)
        return x


class CNN1DOday2022(FoGModel):
    name = "cnn1d-oday2022"

    def __init__(
        self,
        seed: int = 0,
        max_epochs: int = 50,
        patience: int = 7,
        lr: float = 0.001,
        batch_size: int = 512,
        win_sec: float = 2.0,
        stride_sec: float = 0.5,
    ):
        self.seed = seed
        self.max_epochs = max_epochs
        self.patience = patience
        self.lr = lr
        self.batch_size = batch_size
        self.win_sec = win_sec
        self.stride_sec = stride_sec
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.net: ODayCNN1DModule | None = None
        self.channel_mean: np.ndarray | None = None
        self.channel_std: np.ndarray | None = None
        self._threshold_data: list[tuple[np.ndarray, np.ndarray, int]] = []
        torch.manual_seed(seed)
        np.random.seed(seed)

    @staticmethod
    def _augment_rotations(windows: np.ndarray) -> np.ndarray:
        n_windows, _, n_channels = windows.shape
        augmented = np.zeros_like(windows)
        n_sensor_axes = n_channels - n_channels % 3
        if n_sensor_axes == 0:
            return augmented
        rotations = R.random(n_windows).as_matrix()
        grouped = windows[:, :, :n_sensor_axes].reshape(
            n_windows,
            windows.shape[1],
            n_sensor_axes // 3,
            3,
        )
        augmented[:, :, :n_sensor_axes] = np.einsum(
            "ntgc,ndc->ntgd",
            grouped,
            rotations,
            optimize=True,
        ).reshape(n_windows, windows.shape[1], n_sensor_axes)
        return augmented

    @staticmethod
    def _resample(
        raw6: np.ndarray,
        fs: int,
        target_fs: int = 64,
        y: np.ndarray | None = None,
    ) -> tuple[np.ndarray, np.ndarray | None]:
        if fs == target_fs:
            return raw6.astype(np.float32), y

        n_samples = int(len(raw6) * (target_fs / fs))
        resampled_raw6 = resample(raw6, num=n_samples, axis=0).astype(np.float32)
        resampled_y = None

        if y is not None:
            oldx = np.linspace(0.0, 1.0, num=len(y))
            newx = np.linspace(0.0, 1.0, num=n_samples)
            idx = np.round(np.interp(newx, oldx, np.arange(len(y)))).astype(int)
            idx = np.clip(idx, 0, len(y) - 1)
            resampled_y = y[idx]

        return resampled_raw6, resampled_y

    @classmethod
    def _prepare_windows(
        cls,
        raw6: np.ndarray,
        fs: int,
        win_sec: float = 2.0,
        stride_sec: float = 0.5,
        augment: bool = False,
    ) -> np.ndarray:
        windows, _ = cls._prepare_windows_with_starts(
            raw6,
            fs,
            win_sec=win_sec,
            stride_sec=stride_sec,
            augment=augment,
        )
        return windows

    @classmethod
    def _prepare_windows_with_starts(
        cls,
        raw6: np.ndarray,
        fs: int,
        win_sec: float = 2.0,
        stride_sec: float = 0.5,
        augment: bool = False,
        channel_mean: np.ndarray | None = None,
        channel_std: np.ndarray | None = None,
    ) -> tuple[np.ndarray, list[int]]:
        target_fs = 64
        win_len = int(win_sec * target_fs)
        stride_len = max(1, int(stride_sec * target_fs))

        data, _ = cls._resample(raw6, fs, target_fs=target_fs)
        if len(data) <= win_len:
            starts = [0]
            if len(data) < win_len:
                pad_mode = "reflect" if len(data) > 1 else "edge"
                data = np.pad(
                    data,
                    ((0, win_len - len(data)), (0, 0)),
                    mode=pad_mode,
                )
        else:
            last_start = len(data) - win_len
            starts = list(range(0, last_start + 1, stride_len))
            if starts[-1] != last_start:
                starts.append(last_start)

        windows_view = np.lib.stride_tricks.sliding_window_view(
            data,
            win_len,
            axis=0,
        )
        windows_arr = windows_view[np.asarray(starts)].transpose(0, 2, 1).astype(
            np.float32,
            copy=False,
        )
        if augment:
            windows_arr = cls._augment_rotations(windows_arr).astype(np.float32)
        if channel_mean is not None and channel_std is not None:
            windows_arr = (
                (windows_arr - channel_mean[None, None, :])
                / channel_std[None, None, :]
            ).astype(np.float32)
        return windows_arr, starts

    def _extract(self, recs, is_train: bool = False):
        x_list, y_list, w_list = [], [], []
        subj_recs_map = {}

        for r in recs:
            s_id = r.subject
            subj_recs_map.setdefault(s_id, []).append(r)
        n_subjs = len(subj_recs_map)

        for s_id, s_recs in subj_recs_map.items():
            s_x_list, s_y_list = [], []

            for r in s_recs:
                raw_data = r.raw6
                windows, starts = self._prepare_windows_with_starts(
                    raw_data,
                    r.fs,
                    win_sec=self.win_sec,
                    stride_sec=self.stride_sec,
                    augment=is_train,
                    channel_mean=self.channel_mean,
                    channel_std=self.channel_std,
                )

                y = np.asarray(r.y).ravel()
                target_fs = 64
                win_len = int(self.win_sec * target_fs)
                _, y_resampled = self._resample(
                    raw_data,
                    r.fs,
                    target_fs=target_fs,
                    y=y,
                )

                starts_array = np.asarray(starts, dtype=np.int64)
                ends_array = np.minimum(
                    starts_array + win_len,
                    len(y_resampled),
                )
                label_prefix = np.concatenate(
                    ([0], np.cumsum(y_resampled, dtype=np.int64))
                )
                positive_counts = (
                    label_prefix[ends_array] - label_prefix[starts_array]
                )
                rec_y = (
                    positive_counts / (ends_array - starts_array) >= 0.5
                ).astype(np.float32)

                s_x_list.append(windows)
                s_y_list.append(rec_y)

            s_x = np.concatenate(s_x_list, axis=0)
            s_y = np.concatenate(s_y_list, axis=0)

            s_n_total = len(s_y)
            s_n_pos = int(np.sum(s_y == 1.0))
            s_n_neg = s_n_total - s_n_pos
            s_w = np.zeros(s_n_total, dtype=np.float32)

            if s_n_pos > 0 and s_n_neg > 0:
                s_w[s_y == 1.0] = 0.5 / (s_n_pos * n_subjs)
                s_w[s_y == 0.0] = 0.5 / (s_n_neg * n_subjs)
            elif s_n_pos > 0:
                s_w[s_y == 1.0] = 1.0 / (s_n_pos * n_subjs)
            elif s_n_neg > 0:
                s_w[s_y == 0.0] = 1.0 / (s_n_neg * n_subjs)

            x_list.append(s_x)
            y_list.append(s_y)
            w_list.append(s_w)

        x = np.concatenate(x_list, axis=0)
        y = np.concatenate(y_list, axis=0)
        w = np.concatenate(w_list, axis=0)
        weight_sum = float(w.sum())
        if weight_sum <= 0:
            w.fill(1.0)
        else:
            w *= len(w) / weight_sum
        x = np.transpose(x, (0, 2, 1))

        return x, y, w

    def _train_epochs(self, train_loader, optimizer, epochs: int) -> None:
        if self.net is None:
            return

        self.net.train()
        for _ in range(epochs):
            for batch_x, batch_y, batch_w in train_loader:
                batch_x = batch_x.to(self.device)
                batch_y = batch_y.to(self.device).unsqueeze(1)
                batch_w = batch_w.to(self.device).unsqueeze(1)

                optimizer.zero_grad()
                out = self.net(batch_x)
                loss = nn.functional.binary_cross_entropy_with_logits(
                    out,
                    batch_y,
                    weight=batch_w,
                )
                loss.backward()
                optimizer.step()

    def fit(self, recordings) -> None:
        if not recordings:
            return

        self._threshold_data = []
        subj_map = {}

        for r in recordings:
            s_id = r.subject
            subj_map.setdefault(s_id, []).append(r)

        unique_subjs = list(subj_map.keys())
        np.random.shuffle(unique_subjs)

        val_subj_count = max(1, int(len(unique_subjs) * 0.2))
        val_subjs = set(unique_subjs[:val_subj_count])

        train_recs = [
            r
            for r in recordings
            if r.subject not in val_subjs
        ]

        val_recs = [
            r
            for r in recordings
            if r.subject in val_subjs
        ]

        if not train_recs:
            train_recs, val_recs = recordings, recordings
        has_independent_validation = bool(val_recs) and len(train_recs) < len(recordings)

        train_arrays = [
            self._resample(
                np.asarray(r.raw6),
                r.fs,
                target_fs=64,
            )[0]
            for r in train_recs
        ]
        self.channel_mean = np.concatenate(train_arrays, axis=0).mean(axis=0)
        self.channel_std = np.concatenate(train_arrays, axis=0).std(axis=0)
        self.channel_std = np.maximum(self.channel_std, 1e-6).astype(np.float32)
        self.channel_mean = self.channel_mean.astype(np.float32)

        x_train, y_train, w_train = self._extract(train_recs, is_train=True)
        x_val, y_val, w_val = self._extract(val_recs, is_train=False)

        in_channels = x_train.shape[1]

        window_length = int(self.win_sec * 64)
        self.net = ODayCNN1DModule(
            in_channels=in_channels,
            window_length=window_length,
        ).to(self.device)
        train_dataset = TensorDataset(
            torch.tensor(x_train, dtype=torch.float32),
            torch.tensor(y_train, dtype=torch.float32),
            torch.tensor(w_train, dtype=torch.float32),
        )
        train_loader = DataLoader(
            train_dataset,
            batch_size=self.batch_size,
            shuffle=True,
        )
        val_dataset = TensorDataset(
            torch.tensor(x_val, dtype=torch.float32),
            torch.tensor(y_val, dtype=torch.float32),
            torch.tensor(w_val, dtype=torch.float32),
        )
        val_loader = DataLoader(
            val_dataset,
            batch_size=self.batch_size,
            shuffle=False,
        )

        optimizer = torch.optim.Adam(self.net.parameters(), lr=self.lr)
        best_val_loss = float("inf")
        best_model_weights = None
        best_epoch = 0
        patience_counter = 0

        for epoch in range(self.max_epochs):
            self._train_epochs(train_loader, optimizer, 1)

            self.net.eval()
            val_loss = 0.0

            with torch.no_grad():
                for batch_x, batch_y, batch_w in val_loader:
                    batch_x = batch_x.to(self.device)
                    batch_y = batch_y.to(self.device).unsqueeze(1)
                    batch_w = batch_w.to(self.device).unsqueeze(1)

                    out = self.net(batch_x)

                    loss = nn.functional.binary_cross_entropy_with_logits(
                        out,
                        batch_y,
                        weight=batch_w,
                    )

                    val_loss += loss.item() * len(batch_x)

            val_loss /= len(val_dataset)

            if val_loss < best_val_loss:
                best_val_loss = val_loss
                best_epoch = epoch + 1
                best_model_weights = {
                    k: v.cpu().clone() for k, v in self.net.state_dict().items()
                }
                patience_counter = 0
            else:
                patience_counter += 1
                if patience_counter >= self.patience:
                    break

        if best_model_weights is None:
            return
        self.net.load_state_dict(best_model_weights)

        if has_independent_validation:
            self._threshold_data = [
                (
                    np.asarray(recording.y).ravel().copy(),
                    self.predict_proba(recording),
                    int(recording.fs),
                )
                for recording in val_recs
            ]

            x_full, y_full, w_full = self._extract(recordings, is_train=True)
            full_dataset = TensorDataset(
                torch.tensor(x_full, dtype=torch.float32),
                torch.tensor(y_full, dtype=torch.float32),
                torch.tensor(w_full, dtype=torch.float32),
            )
            full_loader = DataLoader(
                full_dataset,
                batch_size=self.batch_size,
                shuffle=True,
            )
            torch.manual_seed(self.seed)
            self.net = ODayCNN1DModule(
                in_channels=x_full.shape[1],
                window_length=window_length,
            ).to(self.device)
            optimizer = torch.optim.Adam(self.net.parameters(), lr=self.lr)
            self._train_epochs(full_loader, optimizer, best_epoch)

    def threshold_predictions(
        self,
    ) -> list[tuple[np.ndarray, np.ndarray, int]]:
        return [
            (labels.copy(), probabilities.copy(), fs)
            for labels, probabilities, fs in self._threshold_data
        ]

    def predict_proba(self, recording) -> np.ndarray:
        raw_data = recording.raw6
        if self.net is None:
            return self.fallback_probabilities(recording)

        windows, starts = self._prepare_windows_with_starts(
            raw_data,
            recording.fs,
            win_sec=self.win_sec,
            stride_sec=self.stride_sec,
            augment=False,
            channel_mean=self.channel_mean,
            channel_std=self.channel_std,
        )

        x = np.transpose(windows, (0, 2, 1))
        self.net.eval()

        with torch.no_grad():
            tensor_x = torch.tensor(x, dtype=torch.float32).to(self.device)
            logits = self.net(tensor_x)
            probabilities = torch.sigmoid(logits).cpu().numpy().ravel()
        probabilities = np.nan_to_num(
            probabilities,
            nan=0.5,
            posinf=1.0,
            neginf=0.0,
        )
        target_length = int(len(self._resample(raw_data, recording.fs, target_fs=64)[0]))
        probability_sum = np.zeros(target_length, dtype=np.float64)
        coverage = np.zeros(target_length, dtype=np.int32)
        window_length = int(round(self.win_sec * 64))
        for start, probability in zip(starts, probabilities):
            end = min(start + window_length, target_length)
            probability_sum[start:end] += probability
            coverage[start:end] += 1
        probabilities_per_sample = np.divide(
            probability_sum,
            coverage,
            out=np.zeros_like(probability_sum),
            where=coverage > 0,
        )
        original_positions = (
            np.arange(len(raw_data), dtype=np.float64) * 64.0 / recording.fs
        )
        return np.interp(
            original_positions,
            np.arange(target_length, dtype=np.float64),
            probabilities_per_sample,
            left=float(probabilities_per_sample[0]),
            right=float(probabilities_per_sample[-1]),
        ).astype(np.float32)

    def card(self) -> dict:
        return {
            "nama": self.name,
            "n_parameter": (
                sum(p.numel() for p in self.net.parameters()) if self.net else 0
            ),
            "hiperparameter": {
                "window_detik": self.win_sec,
                "stride_detik": self.stride_sec,
                "sampling_rate": 64,
                "kernel_size": 17,
                "filters": 16,
                "dropout": 0.5,
                "batch_size": self.batch_size,
                "lr": self.lr,
                "max_epochs": self.max_epochs,
                "patience": self.patience,
                "seed": self.seed,
                "final_refit": "all outer-training subjects for selected epoch count",
                "threshold_calibration": "held-out inner-training subjects",
            },
            "deviasi": [
                "Dataset Figshare menggunakan satu lokasi sensor tibia, sedangkan paper O'Day et al. mengevaluasi berbagai kombinasi lokasi IMU (hingga 11 sensor)",
                "Arsitektur CNN 1D mempertahankan dua blok konvolusi-pooling (16 filter, kernel 17), dropout 0.5, dan fully connected layer sesuai paper.",
                "Sinyal di-resample ke 64 Hz untuk kebutuhan benchmark (data asli paper dikoleksi pada 128 Hz).",
                "Penambahan pembobotan sampel kelas (class weighting) untuk menangani ketimpangan kelas pada dataset Figshare[.",
                "Validasi internal dan early stopping diterapkan pada subjek latih terpisah untuk mencegah kebocoran data pada pasien uji LOSO."
            ],
        }


def factory(seed: int = 0) -> CNN1DOday2022:
    return CNN1DOday2022(seed=seed)
