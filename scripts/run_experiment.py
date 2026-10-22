
"""Jalankan satu model pada satu dataset dengan protokol resmi.

Contoh LOSO standar:
    python scripts/run_experiment.py --model models.random_forest --dataset figshare

Contoh dengan 5 pasien latih:
    python scripts/run_experiment.py --model models.random_forest --dataset figshare --train-patients 5

Contoh Eksperimen 3 (modul dengan CONFIGS, semua kombinasi sekaligus):
    python scripts/run_experiment.py --model "models.experiment 3.freeze_index" --dataset figshare --out results/experiment3
"""
import argparse
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fogbench import data as D
from fogbench import schema
from fogbench.evaluate import protocol, run_loso
from fogbench.report import table
from summarize_results import make_markdown


def main():
    ap = argparse.ArgumentParser()

    ap.add_argument(
        "--model",
        required=True,
        help="Modul model, misalnya models.random_forest"
    )
    ap.add_argument(
        "--dataset",
        required=True,
        help="Nama dataset, misalnya figshare"
    )
    ap.add_argument(
        "--seeds",
        default=None,
        help="Daftar seed dipisahkan koma, misalnya 0,1,2"
    )
    ap.add_argument(
        "--out",
        default=None,
        help="Direktori keluaran"
    )
    ap.add_argument(
        "--train-patients",
        type=int,
        default=None,
        help="Jumlah pasien latih; tanpa argumen ini menggunakan LOSO standar"
    )

    ap.add_argument(
        "--resume",
        action="store_true",
        help="Lewati fold yang hasilnya sudah ada"
    )

    a = ap.parse_args()

    if a.train_patients is not None and a.train_patients < 1:
        ap.error("--train-patients harus minimal 1")

    mod = importlib.import_module(a.model)

    if not hasattr(mod, "factory"):
        sys.exit(
            f"{a.model} harus menyediakan fungsi "
            "factory(seed) yang mengembalikan model"
        )

    seeds = (
        [int(s.strip()) for s in a.seeds.split(",") if s.strip()]
        if a.seeds
        else protocol()["seeds"]
    )

    if not seeds:
        ap.error("--seeds tidak boleh kosong")

    name = getattr(
        mod.factory(seed=seeds[0]),
        "name",
        a.model.split(".")[-1]
    )

    out = Path(
        a.out
        or f"results/{name}_{a.dataset}"
    )

    print(f"Model          : {name}")
    print(f"Dataset        : {a.dataset}")
    print(f"Seed           : {seeds}")
    print(f"Pasien latih   : {a.train_patients or 'LOSO standar'}")
    print(f"Keluaran       : {out}")
    print()

    recs = D.load(a.dataset)

    configs = getattr(mod, "CONFIGS", None)

    if not configs:
        run_loso(
            mod.factory,
            recs,
            out,
            name,
            a.dataset,
            seeds=seeds,
            train_patients=a.train_patients,
            resume=a.resume,
        )

        print(f"\nSelesai. Hasil tersimpan di: {out}")
        print(
            "Validasi hasil: "
            f"python scripts/validate_results.py {out}"
        )
        return

    n_subjects = len({r.subject for r in recs})
    folders = []

    for i, (config_name, config) in enumerate(configs.items(), start=1):
        config_out = out / config_name
        print("=" * 60)
        print(f"Konfigurasi {i}/{len(configs)}: {config_name}")
        print("=" * 60)

        run_loso(
            mod.factory,
            recs,
            config_out,
            name,
            a.dataset,
            seeds=seeds,
            model_kwargs=config.get("model_kwargs"),
            experiment_config=config.get("experiment_config"),
            train_patients=a.train_patients,
            resume=a.resume,
        )

        valid, messages = schema.validate_dir(config_out, n_fold_wajib=n_subjects)
        if not valid:
            for message in messages:
                print(f"  - {message}")
            sys.exit(f"Hasil {config_name} belum valid.")

        (config_out / "report.md").write_text(
            make_markdown(config_out), encoding="utf-8"
        )
        folders.append(config_out)

    (out / "report_all.md").write_text(table(folders), encoding="utf-8")

    print(f"\nSelesai. {len(folders)} konfigurasi tersimpan di: {out}")
    print(f"Ringkasan semua konfigurasi: {out / 'report_all.md'}")


if __name__ == "__main__":
    main()
