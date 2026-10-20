import argparse, importlib, sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from fogbench import data as D, schema, splits
from fogbench.evaluate import protocol
from fogbench.threshold import pick_threshold


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="modul model, misal models.example_logreg")
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--seeds", default=None, help="misal 0,1,2")
    ap.add_argument("--fold", type=int, default=1, help="indeks fold LOSO, dimulai dari 1")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    mod = importlib.import_module(a.model)
    if not hasattr(mod, "factory"):
        sys.exit(f"{a.model} harus menyediakan fungsi factory(seed) yang mengembalikan model")
    seeds = [int(s) for s in a.seeds.split(",")] if a.seeds else protocol()["seeds"]
    name = getattr(mod.factory(seed=seeds[0]), "name", a.model.split(".")[-1])
    
    out_name = f"{name}_{a.dataset}_fold{a.fold:02d}"
    out = Path(a.out or f"results/{out_name}")

    print(f"Model   : {name}\nDataset : {a.dataset}\nSeed    : {seeds}\nFold    : {a.fold}\nKeluaran: {out}\n")
    recs = D.load(a.dataset)
    folds = splits.loso_folds({r.subject for r in recs})
    if a.fold < 1 or a.fold > len(folds):
        ap.error(f"--fold harus antara 1 dan {len(folds)}")

    fold = folds[a.fold - 1]
    train, test = splits.split_recordings(recs, fold)
    fs_eval = int(protocol()["fs_evaluasi_hz"])
    p_seeds, train_time_s = [], 0.0
    threshold_model = None

    for seed in seeds:
        model = mod.factory(seed=seed)
        t0 = time.perf_counter()
        model.fit(train)
        train_time_s += time.perf_counter() - t0
        if threshold_model is None:
            threshold_model = model
        p_seeds.append(np.concatenate([
            D.to_eval_rate(model.predict_proba(r), r.fs, fs_eval)
            for r in test
        ]))

    p_mean = np.mean(p_seeds, axis=0)
    y_eval = np.concatenate([
        D.to_eval_rate(r.y, r.fs, fs_eval, is_label=True)
        for r in test
    ])
    n = min(len(p_mean), len(y_eval))
    p_mean, y_eval = p_mean[:n], y_eval[:n]
    p_seeds = [p[:n] for p in p_seeds]

    y_tr = np.concatenate([D.to_eval_rate(r.y, r.fs, fs_eval, is_label=True) for r in train])
    p_tr = np.concatenate([D.to_eval_rate(threshold_model.predict_proba(r), r.fs, fs_eval) for r in train])
    m = min(len(y_tr), len(p_tr))
    threshold = pick_threshold(y_tr[:m], p_tr[:m])

    t0 = time.perf_counter()
    threshold_model.predict_proba(test[0])
    infer_time_ms = (time.perf_counter() - t0) * 1000

    schema.write_fold(
        out / f"fold_{fold.index:02d}.json",
        model=name,
        dataset=a.dataset,
        fold=fold.index,
        test_subject=fold.test_subject,
        train_subjects=list(fold.train_subjects),
        fs_eval=fs_eval,
        threshold=threshold,
        y_true=y_eval,
        p_mean=p_mean,
        p_per_seed=p_seeds,
        seeds=seeds,
        train_time_s=train_time_s,
        infer_time_ms=infer_time_ms,
        model_card=threshold_model.card(),
    )
    print(f"\nSelesai. Validasi dengan: python scripts/validate_results.py {out} --n-fold 1")


if __name__ == "__main__":
    main()