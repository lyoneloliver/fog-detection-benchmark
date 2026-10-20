
"""Eksperimen 3: sensitivitas Freeze Index terhadap window dan overlap.

Contoh:
    python scripts/run_experiment3.py
    python scripts/run_experiment3.py --out results/experiment3_uji
    python scripts/run_experiment3.py --out results/experiment3_uji --resume
"""


from __future__ import annotations

import argparse
import csv
import importlib
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fogbench import data as D
from fogbench import schema
from fogbench.evaluate import protocol, run_loso
from fogbench.report import summarize


WINDOWS = [1.0, 2.0, 4.0]
OVERLAPS = [0.0, 0.5, 0.75]


def nama_konfigurasi(window: float, overlap: float) -> str:
    overlap_pct = int(round(overlap * 100))
    return f"window_{window:g}s_overlap_{overlap_pct}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="models.freeze_index3")
    ap.add_argument("--dataset", default="figshare")
    ap.add_argument("--seeds", default=None, help="Contoh: 0,1,2")
    ap.add_argument("--out", default=None)
    ap.add_argument("--resume", action="store_true")
    a = ap.parse_args()

    p = protocol()
    seeds = (
        [int(s) for s in a.seeds.split(",")]
        if a.seeds
        else list(p["seeds"])
    )

    module = importlib.import_module(a.model)

    if not hasattr(module, "factory"):
        sys.exit(f"{a.model} harus menyediakan fungsi factory(seed, ...)")

    if a.out:
        root = Path(a.out)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        root = Path("results") / f"experiment3_{timestamp}"

    root.mkdir(parents=True, exist_ok=True)

    print(f"Model       : {a.model}")
    print(f"Dataset     : {a.dataset}")
    print(f"Seed        : {seeds}")
    print(f"Output root : {root}")
    print("Threshold   : otomatis, F1 maksimum dari data latih")
    print()

    recordings = D.load(a.dataset)
    subjects = sorted({r.subject for r in recordings})
    n_subjects = len(subjects)

    if n_subjects != 35:
        raise RuntimeError(
            f"Ditemukan {n_subjects} pasien, bukan 35. "
            "Periksa dataset sebelum menjalankan eksperimen."
        )

    rows = []

    for window in WINDOWS:
        for overlap in OVERLAPS:
            step = window * (1.0 - overlap)
            config_name = nama_konfigurasi(window, overlap)
            out_dir = root / config_name

            model_kwargs = {
                "window_sec": window,
                "step_sec": step,
            }

            experiment_config = {
                "window_sec": window,
                "overlap": overlap,
                "step_sec": step,
                "threshold_method": "f1_maksimum_pada_pasien_latih",
            }

            print("=" * 60)
            print(f"Konfigurasi : {config_name}")
            print(f"Window      : {window:g} detik")
            print(f"Overlap     : {overlap:.0%}")
            print(f"Step        : {step:g} detik")
            print(f"Output      : {out_dir}")
            print("=" * 60)

            model = module.factory(
                seed=seeds[0],
                **model_kwargs,
            )
            model_name = getattr(
                model, "name", a.model.split(".")[-1]
            )

            run_loso(
                model_factory=module.factory,
                recordings=recordings,
                out_dir=out_dir,
                model_name=model_name,
                dataset=a.dataset,
                seeds=seeds,
                model_kwargs=model_kwargs,
                experiment_config=experiment_config,
                resume=a.resume,
            )

            valid, messages = schema.validate_dir(
                out_dir,
                n_fold_wajib=n_subjects,
            )

            if not valid:
                print(f"VALIDASI GAGAL: {config_name}")
                for message in messages:
                    print(f"  - {message}")
                raise RuntimeError(
                    f"Hasil {config_name} belum valid; "
                    "ringkasan tidak dibuat."
                )

            s = summarize(out_dir)
            pooled = s["pooled"]
            per_subject = s["per_subject_ringkas"]
            
            fold_results = [
                json.loads(f.read_text(encoding="utf-8"))
                for f in sorted(out_dir.glob("fold_*.json"))
            ]

            threshold_mean = sum(
                f["threshold"] for f in fold_results
            ) / len(fold_results)

            rows.append({
                "konfigurasi": config_name,
                "window_sec": window,
                "overlap": overlap,
                "step_sec": step,
                "n_fold": s["n_fold"],
                "threshold_mean": threshold_mean,
                "auroc": pooled["auroc"],
                "auprc": pooled["auprc"],
                "sensitivitas": pooled["sensitivitas"],
                "spesifisitas": pooled["spesifisitas"],
                "f1": pooled["f1"],
                "episode_f1": pooled["episode_f1"],
                "auroc_per_pasien_mean": per_subject["auroc_mean"],
                "auroc_per_pasien_sd": per_subject["auroc_sd"],
                "folder_hasil": str(out_dir),
            })

            print(
                f"Valid: {n_subjects} fold | "
                f"AUROC={pooled['auroc']:.4f} | "
                f"F1={pooled['f1']:.4f}"
            )
            print()

    summary_path = root / "summary.csv"
    fieldnames = list(rows[0].keys())

    with summary_path.open(
        "w", newline="", encoding="utf-8-sig"
    ) as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("=" * 60)
    print("Eksperimen 3 selesai.")
    print(f"Jumlah konfigurasi : {len(rows)}")
    print(f"Fold per konfigurasi: {n_subjects}")
    print(f"Total evaluasi fold : {len(rows) * n_subjects}")
    print(f"Ringkasan           : {summary_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()