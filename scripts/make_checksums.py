"""Buat daftar checksum untuk satu dataset. Dijalankan sekali oleh pengelola salinan data.

    python scripts/make_checksums.py --dataset figshare
"""
import argparse, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from fogbench.data import load_config, sha256


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True)
    a = ap.parse_args()
    datasets, paths = load_config()
    root = Path(paths[a.dataset])
    pola = datasets[a.dataset].get("pola_berkas", "**/*")
    out = Path(__file__).resolve().parent.parent / datasets[a.dataset]["checksum"]
    out.parent.mkdir(parents=True, exist_ok=True)
    baris = []
    for f in sorted(root.glob(pola)):
        if f.is_file():
            baris.append(f"{sha256(f)}  {f.relative_to(root).as_posix()}")
    out.write_text("\n".join(baris) + "\n", encoding="utf-8")
    print(f"{len(baris)} berkas dicatat ke {out}")


if __name__ == "__main__":
    main()
