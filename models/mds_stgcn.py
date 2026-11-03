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


class MDSGCN(nn.Module):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        adjacency: np.ndarray,
        rel_channels: int = 8,
    ):
        super().__init__()
        self.num_subsets = adjacency.shape[0]
        self.out_channels = out_channels
        self.rel_channels = rel_channels
        adjacency_tensor = torch.from_numpy(adjacency.astype(np.float32))
        self.register_buffer("static_adjacency", adjacency_tensor)
        self.learned_adjacency = nn.Parameter(adjacency_tensor.clone())
        self.alpha = nn.Parameter(torch.zeros(1))
        self.beta = nn.Parameter(torch.zeros(1))
        self.relation = nn.Conv2d(
            in_channels,
            self.num_subsets * 2 * rel_channels,
            kernel_size=1,
        )
        self.value = nn.Conv2d(
            in_channels,
            self.num_subsets * out_channels,
            kernel_size=1,
        )
        self.topology = nn.Conv2d(
            self.num_subsets * rel_channels,
            self.num_subsets * out_channels,
            kernel_size=1,
            groups=self.num_subsets,
        )
        if in_channels == out_channels:
            self.down = nn.Identity()
        else:
            self.down = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1),
                nn.BatchNorm2d(out_channels),
            )
        self.bn = nn.BatchNorm2d(out_channels)
        self.relu = nn.ReLU()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch, _, steps, nodes = x.shape
        relation = self.relation(x).mean(dim=2).reshape(
            batch,
            self.num_subsets,
            2,
            self.rel_channels,
            nodes,
        )
        f_i, f_j = relation[:, :, 0], relation[:, :, 1]
        values = self.value(x).reshape(
            batch,
            self.num_subsets,
            self.out_channels,
            steps,
            nodes,
        )
        trainable_topology = self.topology(
            torch.tanh(f_i.unsqueeze(-1) - f_j.unsqueeze(-2)).reshape(
                batch,
                self.num_subsets * self.rel_channels,
                nodes,
                nodes,
            )
        ).reshape(batch, self.num_subsets, self.out_channels, nodes, nodes)
        similarity_topology = torch.softmax(
            torch.einsum("nkcu,nkcv->nkuv", f_i, f_j),
            dim=-1,
        ).unsqueeze(2)
        combined = (
            (self.static_adjacency + self.learned_adjacency)[None, :, None]
            + self.alpha * trainable_topology
            + self.beta * similarity_topology
        )
        output = torch.einsum("nkcuv,nkctv->nctu", combined, values)
        return self.relu(self.bn(output) + self.down(x))


class MultiScaleTemporalConv(nn.Module):
    dilations = (1, 2, 3, 4)

    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        stride: int = 1,
        kernel_size: int = 3,
    ):
        super().__init__()
        n_branches = len(self.dilations) + 1
        branch_channels = [out_channels // n_branches] * n_branches
        branch_channels[0] += out_channels - sum(branch_channels)
        self.branch_channels = branch_channels

        self.reduce = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=1),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(),
        )
        self.branches = nn.ModuleList()
        for channels, dilation in zip(branch_channels, self.dilations):
            padding = (kernel_size - 1) * dilation // 2
            self.branches.append(
                nn.Sequential(
                    nn.Conv2d(
                        channels,
                        channels,
                        kernel_size=(kernel_size, 1),
                        stride=(stride, 1),
                        padding=(padding, 0),
                        dilation=(dilation, 1),
                    ),
                    nn.BatchNorm2d(channels),
                )
            )
        self.branches.append(
            nn.Sequential(
                nn.MaxPool2d(
                    kernel_size=(kernel_size, 1),
                    stride=(stride, 1),
                    padding=(kernel_size // 2, 0),
                ),
                nn.BatchNorm2d(branch_channels[-1]),
            )
        )

        if in_channels == out_channels and stride == 1:
            self.residual = nn.Identity()
        else:
            self.residual = nn.Sequential(
                nn.Conv2d(
                    in_channels,
                    out_channels,
                    kernel_size=1,
                    stride=(stride, 1),
                ),
                nn.BatchNorm2d(out_channels),
            )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        reduced = torch.split(self.reduce(x), self.branch_channels, dim=1)
        output = torch.cat(
            [branch(part) for branch, part in zip(self.branches, reduced)],
            dim=1,
        )
        return output + self.residual(x)


class MDSSTGCNBlock(nn.Module):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        adjacency: np.ndarray,
        stride: int = 1,
        residual: bool = True,
        rel_channels: int = 8,
    ):
        super().__init__()
        self.gcn = MDSGCN(in_channels, out_channels, adjacency, rel_channels)
        self.tcn = MultiScaleTemporalConv(out_channels, out_channels, stride=stride)
        self.relu = nn.ReLU()
        self.use_residual = residual
        if not residual or (in_channels == out_channels and stride == 1):
            self.residual = nn.Identity()
        else:
            self.residual = nn.Sequential(
                nn.Conv2d(
                    in_channels,
                    out_channels,
                    kernel_size=1,
                    stride=(stride, 1),
                ),
                nn.BatchNorm2d(out_channels),
            )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        output = self.tcn(self.gcn(x))
        if self.use_residual:
            output = output + self.residual(x)
        return self.relu(output)


class MDSSTGCNNet(nn.Module):
    block_channels = (64, 64, 64, 64, 128, 128, 128, 256, 256, 256)
    block_strides = (1, 1, 1, 1, 2, 1, 1, 2, 1, 1)
    inward_edges = ((1, 0),)

    def __init__(
        self,
        num_nodes: int = 2,
        node_channels: int = 3,
        num_classes: int = 2,
        rel_channels: int = 8,
    ):
        super().__init__()
        self.num_nodes = num_nodes
        self.node_channels = node_channels
        adjacency = self._spatial_adjacency(num_nodes, self.inward_edges)
        self.data_bn = nn.BatchNorm1d(num_nodes * node_channels)

        blocks = []
        in_channels = node_channels
        for index, (out_channels, stride) in enumerate(
            zip(self.block_channels, self.block_strides)
        ):
            blocks.append(
                MDSSTGCNBlock(
                    in_channels,
                    out_channels,
                    adjacency,
                    stride=stride,
                    residual=index > 0,
                    rel_channels=rel_channels,
                )
            )
            in_channels = out_channels
        self.blocks = nn.Sequential(*blocks)
        self.classifier = nn.Linear(in_channels, num_classes)

    @staticmethod
    def _normalize_digraph(adjacency: np.ndarray) -> np.ndarray:
        degree = adjacency.sum(axis=0)
        inverse_degree = np.zeros_like(degree)
        inverse_degree[degree > 0] = 1.0 / degree[degree > 0]
        return adjacency * inverse_degree[None, :]

    @classmethod
    def _spatial_adjacency(
        cls,
        num_nodes: int,
        inward_edges: tuple[tuple[int, int], ...],
    ) -> np.ndarray:
        self_link = np.eye(num_nodes, dtype=np.float32)
        inward = np.zeros((num_nodes, num_nodes), dtype=np.float32)
        outward = np.zeros((num_nodes, num_nodes), dtype=np.float32)
        for source, target in inward_edges:
            inward[target, source] = 1.0
            outward[source, target] = 1.0
        return np.stack(
            [
                self_link,
                cls._normalize_digraph(inward),
                cls._normalize_digraph(outward),
            ]
        ).astype(np.float32)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch, steps, _ = x.shape
        x = x.reshape(batch, steps, self.num_nodes, self.node_channels)
        x = x.permute(0, 2, 3, 1).reshape(
            batch,
            self.num_nodes * self.node_channels,
            steps,
        )
        x = self.data_bn(x)
        x = x.reshape(batch, self.num_nodes, self.node_channels, steps)
        x = x.permute(0, 2, 3, 1)
        x = self.blocks(x)
        return self.classifier(x.mean(dim=(2, 3)))


class MDSSTGCNXia2025(FoGModel):
    name = "mds-stgcn-xia2025"

    def __init__(
        self,
        seed: int = 0,
        max_epochs: int = 50,
        patience: int = 7,
        lr: float = 0.001,
        batch_size: int = 128,
        window_samples: int = 128,
        step_samples: int = 64,
        target_fs: int = 128,
        rel_channels: int = 8,
        restart_epochs: int = 20,
        augment_noise: bool = True,
        noise_std: float = 0.05,
    ):
        self.seed = seed
        self.max_epochs = max_epochs
        self.patience = patience
        self.lr = lr
        self.batch_size = batch_size
        self.window_samples = window_samples
        self.step_samples = step_samples
        self.target_fs = target_fs
        self.rel_channels = rel_channels
        self.restart_epochs = restart_epochs
        self.augment_noise = augment_noise
        self.noise_std = noise_std
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.net: MDSSTGCNNet | None = None
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
    def _noisy_windows(
        windows: np.ndarray,
        rng: np.random.Generator,
        noise_std: float,
    ) -> np.ndarray:
        noise = rng.normal(0.0, noise_std, size=windows.shape)
        return (windows + noise).astype(np.float32)

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

        x_train, y_train, _ = self._collect(train_recordings)
        x_val, y_val, val_subject_ids = self._collect(val_recordings)
        x_train = self._normalize(x_train)
        x_val = self._normalize(x_val)

        if self.augment_noise:
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
                    [
                        x_train,
                        self._noisy_windows(x_train[selected], rng, self.noise_std),
                    ],
                    axis=0,
                )
                y_train = np.concatenate(
                    [y_train, np.ones(len(selected), dtype=np.int64)],
                    axis=0,
                )

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

        self.net = MDSSTGCNNet(rel_channels=self.rel_channels).to(self.device)
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
        scheduler = optim.lr_scheduler.CosineAnnealingWarmRestarts(
            optimizer,
            T_0=self.restart_epochs,
        )
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
            scheduler.step()

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
                for parameter in MDSSTGCNNet(
                    rel_channels=self.rel_channels
                ).parameters()
            )
        )
        return {
            "nama": self.name,
            "n_parameter": parameter_count,
            "hiperparameter": {
                "graph_nodes": ["accelerometer", "gyroscope"],
                "node_channels": ["x", "y", "z"],
                "center_node": "accelerometer",
                "spatial_partitions": 3,
                "adjacency": "MA + PA + alpha*TA + beta*SA (non-shared per channel)",
                "rel_channels": self.rel_channels,
                "block_channels": list(MDSSTGCNNet.block_channels),
                "block_strides": list(MDSSTGCNNet.block_strides),
                "ms_tcn_dilations": list(MultiScaleTemporalConv.dilations),
                "ms_tcn_maxpool_branch": True,
                "sampling_rate_hz": self.target_fs,
                "window_samples": self.window_samples,
                "window_seconds": self.window_samples / self.target_fs,
                "step_samples": self.step_samples,
                "step_seconds": self.step_samples / self.target_fs,
                "batch_size": self.batch_size,
                "learning_rate": self.lr,
                "optimizer": "Adam",
                "scheduler": "cosine annealing warm restarts",
                "restart_epochs": self.restart_epochs,
                "max_epochs": self.max_epochs,
                "patience": self.patience,
                "noise_augmentation": self.augment_noise,
                "noise_std": self.noise_std,
                "imbalance_handling": "gaussian_noise_minority_class_until_window_counts_match",
                "class_weighted_loss": True,
                "epochs_trained": self.num_epochs_trained,
                "seed": self.seed,
            },
            "deviasi": [
                "Paper menggabungkan skeleton 13 sendi dari video OpenPose dengan dua node IMU. Adaptasi ini hanya memakai modalitas IMU Figshare, sehingga graf hanya berisi node akselerometer dan giroskop dengan kanal x/y/z sebagai fitur node.",
                "Tanpa skeleton tidak ada node pusat pinggang tempat sensor dikaitkan; node akselerometer dijadikan pusat graf dan dihubungkan langsung ke node giroskop agar partisi spasial K=3 (diri sendiri, mendekati pusat, menjauhi pusat) tetap terbentuk.",
                "Paper tidak menyebut normalisasi sinyal; z-score per kanal dihitung dari rekaman latih saja karena satuan akselerometer (g) dan giroskop (deg/s) berbeda. Standar deviasi noise augmentasi tidak disebutkan paper dan ditetapkan 0.05 pada skala ternormalisasi.",
                "MS-TCN memakai empat cabang konvolusi 3x1 dengan dilasi 1-4, satu cabang MaxPool 3x1, dan satu cabang residual sesuai deskripsi paper; nilai dilasi tidak disebutkan paper. Kanal keluaran dibagi rata antarcabang dan sisanya diberikan ke cabang pertama.",
                "PA diinisialisasi dari MA, alpha dan beta diinisialisasi nol; TA dan SA memakai fitur f_i dan f_j yang sama dari 1x1 convolution setelah rata-rata temporal. Paper tidak merinci inisialisasi ini.",
                "Paper melatih 50 epoch penuh tanpa validasi. Di sini 20% pasien latih dipisahkan sebagai validasi internal dan early stopping memakai patience 7 untuk memilih checkpoint terbaik serta menyediakan prediksi pemilihan threshold; tujuh epoch memberi toleransi terhadap fluktuasi validation loss tanpa membiarkan training berlanjut terlalu lama. Nilai ini merupakan deviasi pragmatis karena paper tidak menetapkan early stopping. Pasien uji LOSO tidak dipakai.",
                "Batch size diubah menjadi 128 untuk mengurangi jumlah iterasi optimizer dan waktu training pada GPU; paper tidak menetapkan batch size yang sama secara eksplisit, sehingga nilai ini dicatat sebagai deviasi implementasi.",
                "Class-weighted cross entropy dipertahankan seperti model benchmark lain; setelah augmentasi noise jumlah kelas seimbang sehingga bobot kelas latih praktis bernilai satu.",
                "Paper mengeluarkan lima subjek karena kualitas video buruk; karena video tidak dipakai, seluruh 35 pasien Figshare dievaluasi dengan LOSO benchmark. Hasil ini adaptasi IMU-saja, bukan replikasi angka paper.",
                "Prediksi window 1 detik dikembalikan ke resolusi per sampel dengan interpolasi linear antar-titik tengah window agar sesuai antarmuka benchmark."
            ],
        }


def factory(seed: int = 0) -> MDSSTGCNXia2025:
    return MDSSTGCNXia2025(seed=seed)
