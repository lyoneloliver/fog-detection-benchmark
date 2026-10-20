"""Format berkas hasil dan pemvalidasinya.

Satu berkas JSON per fold. Format ini yang membuat hasil Anda dapat digabungkan
dengan hasil orang lain. Berkas yang tidak lolos pemeriksaan di sini tidak
diterima.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

WAJIB = ["model", "dataset", "fold", "test_subject", "train_subjects",
         "fs_eval", "threshold", "y_true", "p_mean", "p_per_seed",
         "seeds", "train_time_s", "infer_time_ms", "model_card"]


def write_fold(path: Path, **kwargs) -> Path:
    rec = {k: kwargs[k] for k in WAJIB}
    for k in ("y_true", "p_mean"):
        rec[k] = np.asarray(rec[k]).ravel().tolist()
    rec["p_per_seed"] = [np.asarray(p).ravel().tolist() for p in rec["p_per_seed"]]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rec), encoding="utf-8")
    return path


def validate_fold(rec: dict) -> list[str]:
    """Kembalikan daftar masalah. Daftar kosong berarti berkas sah."""
    err = []
    for k in WAJIB:
        if k not in rec:
            err.append(f"kunci wajib hilang: {k}")
    if err:
        return err
    y = np.asarray(rec["y_true"], dtype=float)
    p = np.asarray(rec["p_mean"], dtype=float)
    if len(y) != len(p):
        err.append(f"panjang y_true ({len(y)}) tidak sama dengan p_mean ({len(p)})")
    if np.isnan(p).any():
        err.append("p_mean mengandung nilai kosong")
    if len(p) and (p.min() < 0 or p.max() > 1):
        err.append(f"p_mean di luar rentang 0 sampai 1 (min {p.min():.3f}, maks {p.max():.3f})")
    if not set(np.unique(y)) <= {0.0, 1.0}:
        err.append("y_true harus hanya berisi 0 dan 1")
    if rec["test_subject"] in rec["train_subjects"]:
        err.append("KEBOCORAN: pasien uji ada di daftar pasien latih")
    if len(rec["p_per_seed"]) != len(rec["seeds"]):
        err.append("jumlah p_per_seed tidak sama dengan jumlah seed")
    for i, ps in enumerate(rec["p_per_seed"]):
        if len(ps) != len(y):
            err.append(f"p_per_seed[{i}] panjangnya tidak sama dengan y_true")
    if not (0 < float(rec["threshold"]) < 1):
        err.append("ambang harus berada di antara 0 dan 1")
    return err


def validate_dir(folder: Path, n_fold_wajib: int | None = None) -> tuple[bool, list[str]]:
    files = sorted(Path(folder).glob("fold_*.json"))
    msgs = []
    if not files:
        return False, [f"tidak ada berkas fold_*.json di {folder}"]
    subjects = []
    for f in files:
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            msgs.append(f"{f.name}: tidak dapat dibaca ({e})")
            continue
        for m in validate_fold(rec):
            msgs.append(f"{f.name}: {m}")
        subjects.append(rec.get("test_subject"))
    if len(set(subjects)) != len(subjects):
        msgs.append("ada pasien uji yang muncul di lebih dari satu fold")
    if n_fold_wajib and len(files) != n_fold_wajib:
        msgs.append(f"jumlah fold {len(files)}, seharusnya {n_fold_wajib}")
    return (len(msgs) == 0), msgs
