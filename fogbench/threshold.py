"""Pemilihan ambang keputusan dari pasien latih.

Fungsi di modul ini sengaja tidak pernah menerima label pasien uji. Memilih
ambang pada data uji adalah bentuk kebocoran yang membuat angka naik palsu.
"""
from __future__ import annotations

import numpy as np


def pick_threshold(y_train: np.ndarray, p_train: np.ndarray, n_grid: int = 101) -> float:
    """Ambang yang memaksimumkan F1 pada pasien latih."""
    y = np.asarray(y_train).ravel().astype(int)
    p = np.asarray(p_train).ravel().astype(float)
    if len(y) != len(p):
        raise ValueError("panjang label dan probabilitas harus sama")
    if y.max() == y.min():
        return 0.5
    best_t, best_f1 = 0.5, -1.0
    for t in np.linspace(0.01, 0.99, n_grid):
        pred = (p >= t).astype(int)
        tp = int((pred & y).sum())
        if tp == 0:
            continue
        prec = tp / max(int(pred.sum()), 1)
        rec = tp / max(int(y.sum()), 1)
        f1 = 2 * prec * rec / (prec + rec)
        if f1 > best_f1:
            best_t, best_f1 = float(t), f1
    return best_t
