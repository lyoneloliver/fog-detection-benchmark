"""Contoh model, SENGAJA DIBUAT LEMAH.

Tujuannya hanya menunjukkan bentuk antarmuka dan bentuk berkas hasil. Model ini
bukan metode dari makalah mana pun dan tidak layak dilaporkan sebagai pembanding.
"""
from __future__ import annotations

import numpy as np
from sklearn.linear_model import LogisticRegression

from models.base import FoGModel


def _fitur(raw6: np.ndarray, fs: int, win: int = 2) -> np.ndarray:
    """Tiga fitur kasar per sampel: norma akselerasi, simpangan bakunya, norma giroskop."""
    k = max(1, int(win * fs))
    acc = np.linalg.norm(raw6[:, :3], axis=1)
    gyr = np.linalg.norm(raw6[:, 3:], axis=1)
    pad = np.pad(acc, (k // 2, k - k // 2 - 1), mode="edge")
    roll = np.lib.stride_tricks.sliding_window_view(pad, k)
    return np.stack([acc, roll.std(axis=1)[:len(acc)], gyr], axis=1).astype(np.float32)


class ExampleLogReg(FoGModel):
    name = "contoh-logreg"

    def __init__(self, seed: int = 0):
        self.seed = seed
        self.clf = LogisticRegression(max_iter=200, class_weight="balanced", random_state=seed)

    def fit(self, recordings) -> None:
        X = np.concatenate([_fitur(r.raw6, r.fs) for r in recordings])
        y = np.concatenate([np.asarray(r.y).ravel() for r in recordings])
        step = max(1, len(y) // 200_000)
        self.clf.fit(X[::step], y[::step])

    def predict_proba(self, recording) -> np.ndarray:
        return self.clf.predict_proba(_fitur(recording.raw6, recording.fs))[:, 1]

    def card(self) -> dict:
        return {"nama": self.name, "n_parameter": 4,
                "hiperparameter": {"window_detik": 2, "seed": self.seed},
                "deviasi": ["bukan metode dari makalah mana pun, hanya contoh antarmuka"]}


def factory(seed: int = 0) -> ExampleLogReg:
    return ExampleLogReg(seed=seed)
