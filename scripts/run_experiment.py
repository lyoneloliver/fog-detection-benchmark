
"""Jalankan satu model pada satu dataset dengan protokol resmi.

Contoh LOSO standar:
    python scripts/run_experiment.py --model models.random_forest --dataset figshare

Contoh dengan 5 pasien latih:
    python scripts/run_experiment.py --model models.random_forest --dataset figshare --train-patients 5
"""
import argparse
import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fogbench import data as D
from fogbench.evaluate import protocol, run_loso


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

    run_loso(
        mod.factory,
        recs,
        out,
        name,
        a.dataset,
        seeds=seeds,
        train_patients=a.train_patients,
    )

    print(f"\nSelesai. Hasil tersimpan di: {out}")
    print(
        "Validasi hasil: "
        f"python scripts/validate_results.py {out}"
    )


if __name__ == "__main__":
    main()
