"""Jalankan satu model pada satu dataset dengan protokol resmi.

Pemakaian:
    python scripts/run_experiment.py --model models.example_logreg --dataset figshare
"""
import argparse, importlib, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from fogbench import data as D
from fogbench.evaluate import protocol, run_loso


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True, help="modul model, misal models.example_logreg")
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--seeds", default=None, help="misal 0,1,2")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    mod = importlib.import_module(a.model)
    if not hasattr(mod, "factory"):
        sys.exit(f"{a.model} harus menyediakan fungsi factory(seed) yang mengembalikan model")
    seeds = [int(s) for s in a.seeds.split(",")] if a.seeds else protocol()["seeds"]
    name = getattr(mod.factory(seed=seeds[0]), "name", a.model.split(".")[-1])
    out = Path(a.out or f"results/{name}_{a.dataset}")

    print(f"Model   : {name}\nDataset : {a.dataset}\nSeed    : {seeds}\nKeluaran: {out}\n")
    recs = D.load(a.dataset)
    run_loso(mod.factory, recs, out, name, a.dataset, seeds=seeds)
    print(f"\nSelesai. Jalankan: python scripts/validate_results.py {out}")


if __name__ == "__main__":
    main()
