"""Periksa data sebelum mulai bekerja.

Pemakaian:
    python scripts/check_data.py --dataset figshare
"""
import argparse, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np
from fogbench import data as D


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True)
    a = ap.parse_args()

    print(f"Memuat {a.dataset} ...")
    recs = D.load(a.dataset)
    subs = sorted({r.subject for r in recs})
    dur = sum(r.duration_s for r in recs) / 60
    pos = sum(int(r.y.sum()) for r in recs)
    tot = sum(r.n_samples for r in recs)
    tanpa = [s for s in subs if not any(r.y.sum() for r in recs if r.subject == s)]

    print(f"  pasien            : {len(subs)}")
    print(f"  rekaman           : {len(recs)}")
    print(f"  durasi total      : {dur:.1f} menit")
    print(f"  laju cuplik       : {recs[0].fs} Hz")
    print(f"  kanal             : {recs[0].raw6.shape[1]} (enam kanal mentah)")
    print(f"  proporsi label FoG: {pos / tot:.3%}")
    print(f"  pasien tanpa FoG  : {len(tanpa)} -> {tanpa}")
    amp = np.concatenate([np.linalg.norm(r.raw6[:, :3], axis=1) for r in recs])
    print(f"  norma akselerasi  : median {np.median(amp):.3f} "
          f"(dekat 1 berarti satuan g, dekat 9,8 berarti m/s2)")
    print("\nData siap dipakai.")


if __name__ == "__main__":
    main()
