"""Metrik bersama.

Definisi F1 tingkat episode ditulis di sini satu kali. Kalau setiap pengguna
menulis versinya sendiri, angkanya tidak setara walaupun namanya sama.
"""
from __future__ import annotations

import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score


def _runs(mask: np.ndarray) -> list[tuple[int, int]]:
    """Daftar segmen bernilai 1 sebagai pasangan (awal, akhir_eksklusif)."""
    m = np.asarray(mask).astype(int).ravel()
    if m.size == 0:
        return []
    d = np.diff(np.concatenate([[0], m, [0]]))
    return list(zip(np.flatnonzero(d == 1).tolist(), np.flatnonzero(d == -1).tolist()))


def _overlap(a: tuple[int, int], b: tuple[int, int]) -> int:
    return max(0, min(a[1], b[1]) - max(a[0], b[0]))


def episode_f1(y_true: np.ndarray, y_pred: np.ndarray, min_overlap: float = 0.5) -> dict:
    """F1 pada tingkat episode.

    Episode sebenarnya dihitung terdeteksi bila minimal `min_overlap` bagian
    durasinya tertutup prediksi. Episode prediksi dihitung benar bila minimal
    `min_overlap` bagian durasinya berada di dalam episode sebenarnya.
    """
    true_ep, pred_ep = _runs(y_true), _runs(y_pred)
    if not true_ep and not pred_ep:
        return {"episode_f1": 1.0, "episode_recall": 1.0, "episode_precision": 1.0,
                "n_episode_true": 0, "n_episode_pred": 0}
    hit = sum(1 for t in true_ep
              if max((_overlap(t, p) for p in pred_ep), default=0) >= min_overlap * (t[1] - t[0]))
    ok = sum(1 for p in pred_ep
             if max((_overlap(p, t) for t in true_ep), default=0) >= min_overlap * (p[1] - p[0]))
    rec = hit / len(true_ep) if true_ep else 0.0
    prec = ok / len(pred_ep) if pred_ep else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) > 0 else 0.0
    return {"episode_f1": f1, "episode_recall": rec, "episode_precision": prec,
            "n_episode_true": len(true_ep), "n_episode_pred": len(pred_ep)}


def sample_metrics(y_true: np.ndarray, p: np.ndarray, threshold: float) -> dict:
    """Metrik pada tingkat sampel."""
    y = np.asarray(y_true).ravel().astype(int)
    p = np.asarray(p).ravel().astype(float)
    pred = (p >= threshold).astype(int)
    tp = int((pred & y).sum()); fp = int((pred & (1 - y)).sum())
    fn = int(((1 - pred) & y).sum()); tn = int(((1 - pred) & (1 - y)).sum())
    sens = tp / (tp + fn) if (tp + fn) else float("nan")
    spec = tn / (tn + fp) if (tn + fp) else float("nan")
    prec = tp / (tp + fp) if (tp + fp) else float("nan")
    f1 = 2 * prec * sens / (prec + sens) if (prec + sens) and not np.isnan(prec) else float("nan")
    dua_kelas = y.min() != y.max()
    out = {"auroc": roc_auc_score(y, p) if dua_kelas else float("nan"),
           "auprc": average_precision_score(y, p) if dua_kelas else float("nan"),
           "sensitivitas": sens, "spesifisitas": spec, "presisi": prec, "f1": f1,
           "n_sampel": int(len(y)), "prevalensi": float(y.mean()), "ambang": float(threshold)}
    out.update(episode_f1(y, pred))
    return out


def pooled_and_per_subject(per_fold: list[dict]) -> dict:
    """Gabungkan hasil per fold menjadi metrik gabungan dan metrik per pasien.

    Metrik gabungan memakai seluruh sampel yang disatukan. Metrik per pasien
    hanya dihitung pada pasien yang memiliki kedua kelas.
    """
    ys = np.concatenate([np.asarray(f["y_true"]).ravel() for f in per_fold])
    ps = np.concatenate([np.asarray(f["p_mean"]).ravel() for f in per_fold])
    thr = float(np.mean([f["threshold"] for f in per_fold]))
    pooled = sample_metrics(ys, ps, thr)
    per_sub = []
    for f in per_fold:
        y = np.asarray(f["y_true"]).ravel().astype(int)
        if y.min() == y.max():
            continue
        m = sample_metrics(y, np.asarray(f["p_mean"]).ravel(), f["threshold"])
        m["test_subject"] = f["test_subject"]
        per_sub.append(m)
    auroc = np.array([m["auroc"] for m in per_sub], dtype=float)
    return {"pooled": pooled, "per_subject": per_sub,
            "per_subject_ringkas": {
                "n": int(len(per_sub)),
                "auroc_mean": float(auroc.mean()) if len(auroc) else float("nan"),
                "auroc_sd": float(auroc.std(ddof=1)) if len(auroc) > 1 else float("nan"),
                "auroc_median": float(np.median(auroc)) if len(auroc) else float("nan")}}


def bootstrap_ci(values, n_boot: int = 2000, level: float = 0.95, seed: int = 0):
    """Selang kepercayaan bootstrap pada tingkat pasien."""
    v = np.asarray([x for x in values if not np.isnan(x)], dtype=float)
    if len(v) < 2:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    means = [rng.choice(v, size=len(v), replace=True).mean() for _ in range(n_boot)]
    lo, hi = (1 - level) / 2 * 100, (1 + level) / 2 * 100
    return float(np.percentile(means, lo)), float(np.percentile(means, hi))
