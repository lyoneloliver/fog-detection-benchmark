from __future__ import annotations

import numpy as np
import torch
from torch.utils.data import Dataset

from models.tcn import InitialTCN, TCNYang2024, _WindowDataset


class _RotationBalancedDataset(Dataset):
    def __init__(
        self,
        base: _WindowDataset,
        labels: list[np.ndarray],
        seed: int,
    ):
        self.base = base
        self.rng = np.random.default_rng(seed)
        all_labels = np.concatenate(labels)
        class_counts = np.bincount(all_labels, minlength=2)
        if class_counts[1] == 0 or class_counts[1] >= class_counts[0]:
            self.synthetic_indices = np.empty(0, dtype=np.int64)
        else:
            fog_indices = np.flatnonzero(all_labels == 1)
            deficit = int(class_counts[0] - class_counts[1])
            self.synthetic_indices = self.rng.choice(
                fog_indices,
                size=deficit,
                replace=True,
            )
        self.synthetic_rotations = self._make_rotations(len(self.synthetic_indices))

    def __len__(self) -> int:
        return len(self.base) + len(self.synthetic_indices)

    def _make_rotations(self, count: int) -> np.ndarray:
        if count == 0:
            return np.empty((0, 3, 3), dtype=np.float32)
        matrices = self.rng.normal(size=(count, 3, 3))
        q, r = np.linalg.qr(matrices)
        diagonal_signs = np.sign(np.diagonal(r, axis1=1, axis2=2))
        diagonal_signs[diagonal_signs == 0] = 1.0
        q *= diagonal_signs[:, None, :]
        reflection = np.linalg.det(q) < 0
        q[reflection, :, 0] *= -1
        return q.astype(np.float32, copy=False)

    def _rotate(self, window: np.ndarray, rotation: np.ndarray) -> np.ndarray:
        rotated = window.copy()
        rotated[:, :3] = window[:, :3] @ rotation
        return rotated

    def __getitem__(self, index: int) -> tuple[torch.Tensor, torch.Tensor]:
        if index < len(self.base):
            return self.base[index]
        source_index = int(self.synthetic_indices[index - len(self.base)])
        window, label = self.base[source_index]
        rotation = self.synthetic_rotations[index - len(self.base)]
        rotated = self._rotate(window.numpy(), rotation)
        return torch.from_numpy(rotated), label


class TCNYang2024RotationAugmentation(TCNYang2024):
    name = "tcn-rotation-augmentation"

    @property
    def training_window_samples(self) -> int:
        return max(self.window_samples, InitialTCN.receptive_field)

    def _fit_initial(
        self,
        signals: list[np.ndarray],
        labels: list[np.ndarray],
        class_weights: np.ndarray,
    ) -> None:
        self._fit_initial_windows(signals, labels, class_weights)

    def _training_class_counts(self, labels: list[np.ndarray]) -> np.ndarray:
        counts = super()._training_class_counts(labels)
        if 0 < counts[1] < counts[0]:
            counts[1] += counts[0] - counts[1]
        return counts

    def _build_training_dataset(
        self,
        signals: list[np.ndarray],
        labels: list[np.ndarray],
    ) -> Dataset:
        base_dataset = _WindowDataset(
            signals,
            labels,
            self.training_window_samples,
        )
        return _RotationBalancedDataset(base_dataset, labels, self.seed)

    def card(self) -> dict:
        result = super().card()
        result["nama"] = self.name
        result["hiperparameter"]["augmentasi"] = (
            "Rotasi arbitrer 3D pada sampel FoG tambahan hingga jumlah kelas "
            "seimbang"
        )
        result["deviasi"] = [
            "Li et al. (2020) mengusulkan augmentasi rotasi arbitrer untuk menyeimbangkan sampel FoG, tetapi arsitektur paper adalah SEC-ALSTM, bukan TCN; model ini memakai initial-prediction dan refinement MS-TCN Yang et al. (2024).",
            "Paper Li memakai Daphnet dengan sembilan kanal akselerometer; Figshare menyediakan satu IMU dengan enam kanal; rotasi diterapkan pada triad akselerometer Figshare, bukan kanal giroskop.",
            "Pembentukan sampel mengikuti antarmuka prediksi per-sampel TCN benchmark, bukan segmentasi 256-frame dengan langkah 4 yang dipakai pada eksperimen Li.",
            "Augmentasi rotasi diterapkan pada training initial TCN; refinement tetap dilatih pada recording asli agar target temporal dan kontinuitas sinyal tidak berubah.",
            "Evaluasi mengikuti LOSO Figshare dan protokol threshold benchmark, bukan evaluasi Daphnet Li."

        ]
        return result


def factory(seed: int = 0) -> TCNYang2024RotationAugmentation:
    return TCNYang2024RotationAugmentation(seed=seed)