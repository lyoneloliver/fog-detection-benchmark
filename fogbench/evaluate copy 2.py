"""Penjalan eksperimen: satu model, satu dataset, protokol resmi."""
from __future__ import annotations

import time
from pathlib import Path

import numpy as np
import yaml

from fogbench import data as D
from fogbench import splits, schema
from fogbench.threshold import pick_threshold

CFG = Path(__file__).resolve().parent.parent / "config" / "protocol.yaml"


def protocol() -> dict:
    return yaml.safe_load(CFG.read_text(encoding="utf-8"))


def run_loso(model_factory, recordings, out_dir: Path, model_name: str,
             dataset: str, seeds=None, fs_eval=None, verbose=True) -> Path:
    """Jalankan LOSO penuh dan tulis satu berkas hasil per fold."""
    p = protocol()
    seeds = list(seeds or p["seeds"])
    fs_eval = int(fs_eval or p["fs_evaluasi_hz"])
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    folds = splits.loso_folds({r.subject for r in recordings})

    for fold in folds:
        train, test = splits.split_recordings(recordings, fold)
        p_seeds, t_train = [], 0.0
        for sd in seeds:
            model = model_factory(seed=sd)
            t0 = time.perf_counter()
            model.fit(train)                     # HANYA pasien latih
            t_train += time.perf_counter() - t0
            p_seeds.append(np.concatenate(
                [D.to_eval_rate(model.predict_proba(r), r.fs, fs_eval) for r in test]))
        p_mean = np.mean(p_seeds, axis=0)
        y_eval = np.concatenate([D.to_eval_rate(r.y, r.fs, fs_eval, is_label=True) for r in test])
        n = min(len(p_mean), len(y_eval))
        p_mean, y_eval = p_mean[:n], y_eval[:n]
        p_seeds = [q[:n] for q in p_seeds]

        # ambang dari pasien latih saja
        model_t = model_factory(seed=seeds[0]); model_t.fit(train)
        y_tr = np.concatenate([D.to_eval_rate(r.y, r.fs, fs_eval, is_label=True) for r in train])
        p_tr = np.concatenate([D.to_eval_rate(model_t.predict_proba(r), r.fs, fs_eval)
                               for r in train])
        m = min(len(y_tr), len(p_tr))
        thr = pick_threshold(y_tr[:m], p_tr[:m])

        t0 = time.perf_counter()
        _ = model_t.predict_proba(test[0])
        infer_ms = (time.perf_counter() - t0) * 1000

        schema.write_fold(
            out_dir / f"fold_{fold.index:02d}.json",
            model=model_name, dataset=dataset, fold=fold.index,
            test_subject=fold.test_subject, train_subjects=list(fold.train_subjects),
            fs_eval=fs_eval, threshold=thr, y_true=y_eval, p_mean=p_mean,
            p_per_seed=p_seeds, seeds=seeds, train_time_s=t_train,
            infer_time_ms=infer_ms, model_card=model_t.card())
        if verbose:
            print(f"  fold {fold.index:02d}/{len(folds)} pasien {fold.test_subject} selesai")
    return out_dir
