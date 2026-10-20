"""Normalisasi yang dipasang HANYA pada pasien latih.

Ini penyebab kebocoran data yang paling sering dan paling sulit terlihat.
Karena itu pemasangan dan penerapan dipisah menjadi dua fungsi, dan fungsi
pemasangan menolak menerima rekaman pasien uji.
"""
from __future__ import annotations

import numpy as np


class Normalizer:
    """Standardisasi per kanal. Rerata dan simpangan baku dari pasien latih saja."""

    def __init__(self):
        self.mean_: np.ndarray | None = None
        self.std_: np.ndarray | None = None
        self.fitted_subjects_: tuple[int, ...] = ()

    def fit(self, train_recordings, forbidden_subjects=()) -> "Normalizer":
        subs = {r.subject for r in train_recordings}
        bad = subs & set(forbidden_subjects)
        if bad:
            raise ValueError(f"kebocoran: pasien uji {sorted(bad)} ikut dipakai untuk normalisasi")
        if not train_recordings:
            raise ValueError("tidak ada rekaman latih")
        stacked = np.concatenate([r.raw6 for r in train_recordings], axis=0)
        self.mean_ = stacked.mean(axis=0)
        self.std_ = stacked.std(axis=0)
        self.std_[self.std_ < 1e-8] = 1.0
        self.fitted_subjects_ = tuple(sorted(subs))
        return self

    def transform(self, recording_or_array) -> np.ndarray:
        if self.mean_ is None:
            raise RuntimeError("Normalizer belum dipasang. Panggil fit() pada pasien latih dulu.")
        x = getattr(recording_or_array, "raw6", recording_or_array)
        return ((np.asarray(x, dtype=np.float32) - self.mean_) / self.std_).astype(np.float32)

    def params(self) -> dict:
        return {"mean": None if self.mean_ is None else self.mean_.tolist(),
                "std": None if self.std_ is None else self.std_.tolist()}
