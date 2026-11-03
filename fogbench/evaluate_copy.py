
"""Penjalan eksperimen: satu model, satu dataset, protokol resmi."""
from __future__ import annotations

import json
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


def run_loso(
    model_factory,
    recordings,
    out_dir: Path,
    model_name: str,
    dataset: str,
    seeds=None,
    fs_eval=None,
    verbose=True,
    model_kwargs=None,
    experiment_config=None,
    train_patients=None,
    resume=False,
) -> Path:
    """Jalankan LOSO dan tulis satu berkas hasil per fold."""
    p = protocol()
    seeds = list(seeds or p["seeds"])
    fs_eval = int(fs_eval or p["fs_evaluasi_hz"])
    model_kwargs = dict(model_kwargs or {})
    experiment_config = dict(experiment_config or {})

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    subjects = {r.subject for r in recordings}
    folds = splits.loso_folds(subjects)

    for fold in folds:
        out_file = out_dir / f"fold_{fold.index:02d}.json"

        if resume and out_file.is_file():
            try:
                saved = json.loads(out_file.read_text(encoding="utf-8"))
                valid = (
                    saved.get("model") == model_name
                    and saved.get("dataset") == dataset
                    and saved.get("fold") == fold.index
                    and saved.get("test_subject") == fold.test_subject
                    and saved.get("fs_eval") == fs_eval
                    and saved.get("seeds") == seeds
                    and saved.get("experiment_config", {}) == experiment_config
                    and len(saved.get("y_true", [])) > 0
                    and len(saved.get("p_mean", [])) > 0
                    and saved.get("train_subjects") is not None
                )

                if train_patients is not None:
                    valid = valid and (
                        len(saved.get("train_subjects", []))
                        == train_patients
                    )

                if valid:
                    if verbose:
                        print(
                            f"  fold {fold.index:02d}/{len(folds)} "
                            f"pasien {fold.test_subject}: hasil sudah ada, lewati"
                        )
                    continue
            except (OSError, ValueError, TypeError):
                pass

        train, test = splits.split_recordings(recordings, fold)

        if train_patients is not None:
            available = sorted({r.subject for r in train})

            if train_patients < 1 or train_patients > len(available):
                raise ValueError(
                    f"train_patients={train_patients} tidak valid; "
                    f"tersedia {len(available)} pasien latih"
                )

            rng = np.random.default_rng(10000 + int(fold.index))
            selected = set(
                rng.permutation(available)[:train_patients].tolist()
            )
            train = [r for r in train if r.subject in selected]

        actual_train_subjects = sorted({r.subject for r in train})

        p_seeds = []
        t_train = 0.0

        for sd in seeds:
            model = model_factory(seed=sd, **model_kwargs)

            t0 = time.perf_counter()
            model.fit(train)
            t_train += time.perf_counter() - t0

            pred = [
                D.to_eval_rate(
                    model.predict_proba(r), r.fs, fs_eval
                )
                for r in test
            ]
            p_seeds.append(np.concatenate(pred))

        p_mean = np.mean(p_seeds, axis=0)

        y_eval = np.concatenate([
            D.to_eval_rate(
                r.y, r.fs, fs_eval, is_label=True
            )
            for r in test
        ])

        n = min(len(p_mean), len(y_eval))
        p_mean = p_mean[:n]
        y_eval = y_eval[:n]
        p_seeds = [q[:n] for q in p_seeds]

        # Threshold tetap dipilih dari pasien latih saja.
        model_t = model_factory(seed=seeds[0], **model_kwargs)
        model_t.fit(train)

        y_tr = np.concatenate([
            D.to_eval_rate(
                r.y, r.fs, fs_eval, is_label=True
            )
            for r in train
        ])
        p_tr = np.concatenate([
            D.to_eval_rate(
                model_t.predict_proba(r), r.fs, fs_eval
            )
            for r in train
        ])

        m = min(len(y_tr), len(p_tr))
        thr = pick_threshold(y_tr[:m], p_tr[:m])

        t0 = time.perf_counter()
        _ = model_t.predict_proba(test[0])
        infer_ms = (time.perf_counter() - t0) * 1000

        schema.write_fold(
            out_file,
            model=model_name,
            dataset=dataset,
            fold=fold.index,
            test_subject=fold.test_subject,
            train_subjects=actual_train_subjects,
            fs_eval=fs_eval,
            threshold=thr,
            y_true=y_eval,
            p_mean=p_mean,
            p_per_seed=p_seeds,
            seeds=seeds,
            train_time_s=t_train,
            infer_time_ms=infer_ms,
            model_card=model_t.card(),
            experiment_config=experiment_config,
        )

        if verbose:
            print(
                f"  fold {fold.index:02d}/{len(folds)} "
                f"pasien {fold.test_subject} selesai"
            )

    return out_dir
