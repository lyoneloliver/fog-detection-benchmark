"""Uji mandiri: jalankan seluruh rantai pada data sintetis, tanpa perlu data asli.

Jalankan ini lebih dulu untuk memastikan pemasangan Anda benar:
    python scripts/selftest.py
"""
import sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import numpy as np

from fogbench.data import Recording
from fogbench.evaluate import run_loso
from fogbench import report, schema
from models.example_logreg import factory


def data_sintetis(n_pasien=5, fs=64):
    rng = np.random.default_rng(0)
    recs = []
    for sub in range(1, n_pasien + 1):
        T = fs * 20
        raw6 = rng.normal(0, 1, (T, 6)).astype(np.float32)
        y = np.zeros(T, np.int8)
        for a in range(fs * 3, T - fs * 3, fs * 6):
            y[a:a + fs * 2] = 1
        raw6[y == 1] += 2.5
        recs.append(Recording(sub, 0, "sintetis", fs, raw6, y))
    return recs


def main():
    print("1. Membuat data sintetis")
    recs = data_sintetis()
    print(f"   {len(recs)} rekaman, {len({r.subject for r in recs})} pasien\n")

    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "contoh"
        print("2. Menjalankan LOSO")
        run_loso(factory, recs, out, "contoh-logreg", "sintetis", seeds=[0], verbose=False)
        print(f"   {len(list(out.glob('fold_*.json')))} berkas fold ditulis\n")

        print("3. Memvalidasi format hasil")
        ok, pesan = schema.validate_dir(out, n_fold_wajib=5)
        print("   SAH" if ok else "   BERMASALAH: " + "; ".join(pesan))
        if not ok:
            return 1
        print()

        print("4. Membuat tabel ringkasan")
        print(report.table([out]))
        s = report.summarize(out)
        print(f"   AUROC per pasien: {s['per_subject_ringkas']['auroc_mean']:.3f} "
              f"± {s['per_subject_ringkas']['auroc_sd']:.3f} "
              f"(n = {s['per_subject_ringkas']['n']})")

    print("\nSeluruh rantai berjalan. Pemasangan Anda sudah benar.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
