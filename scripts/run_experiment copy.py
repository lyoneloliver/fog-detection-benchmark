"""Jalankan satu model pada satu dataset dengan protokol resmi.

Pemakaian:
    python "scripts/run_experiment copy.py" --model models.example_logreg --dataset figshare
"""
import argparse, importlib, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from fogbench import data as D
from fogbench import schema
from fogbench.evaluate_copy_2 import protocol, run_loso
from summarize_results import make_markdown


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

    n_subjects = len({r.subject for r in recs})
    valid, messages = schema.validate_dir(out, n_fold_wajib=n_subjects)
    if not valid:
        for message in messages:
            print(f"  - {message}")
        sys.exit(f"Hasil di {out} belum valid, report tidak dibuat.")

    (out / "report.md").write_text(make_markdown(out), encoding="utf-8")
    print(f"\nSelesai. {n_subjects} fold tersimpan di: {out}")
    print(f"Report: {out / 'report.md'}")


if __name__ == "__main__":
    main()
