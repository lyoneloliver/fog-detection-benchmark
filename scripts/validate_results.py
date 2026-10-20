"""Periksa berkas hasil sebelum dibagikan atau dilaporkan.

Pemakaian:
    python scripts/validate_results.py results/contoh-logreg_figshare --n-fold 35
"""
import argparse, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from fogbench import schema


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--n-fold", type=int, default=None)
    a = ap.parse_args()

    ok, pesan = schema.validate_dir(Path(a.folder), a.n_fold)
    if ok:
        print(f"Hasil di {a.folder} SAH dan siap dilaporkan.")
        return 0
    print(f"Hasil di {a.folder} BELUM SAH. Perbaiki dulu:\n")
    for m in pesan:
        print("  -", m)
    return 1


if __name__ == "__main__":
    sys.exit(main())
