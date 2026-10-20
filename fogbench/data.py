"""Pemuat data. Mengembalikan sinyal enam kanal MENTAH dan label per sampel.

Aturan penting: modul ini berhenti di sinyal mentah. Tidak ada penyelarasan
gravitasi, tidak ada perputaran sumbu, tidak ada ekstraksi fitur. Semua itu
adalah bagian dari metode, dan metode adalah pekerjaan Anda.
"""
from __future__ import annotations

import glob
import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

CFG_DIR = Path(__file__).resolve().parent.parent / "config"


@dataclass
class Recording:
    """Satu rekaman dari satu pasien."""
    subject: int                 # nomor pasien
    session: int                 # nomor rekaman dalam pasien tersebut
    dataset: str
    fs: int                      # laju cuplik asli, Hz
    raw6: np.ndarray             # (T, 6) float32: accX, accY, accZ, gyrX, gyrY, gyrZ
    y: np.ndarray                # (T,) int8: 1 = FoG, 0 = bukan FoG
    meta: dict = field(default_factory=dict)

    def __post_init__(self):
        assert self.raw6.ndim == 2 and self.raw6.shape[1] == 6, "raw6 harus (T, 6)"
        assert len(self.y) == len(self.raw6), "panjang label harus sama dengan panjang sinyal"

    @property
    def n_samples(self) -> int:
        return len(self.y)

    @property
    def duration_s(self) -> float:
        return self.n_samples / self.fs

    @property
    def fog_ratio(self) -> float:
        return float(self.y.mean())


# --------------------------------------------------------------------- konfigurasi
def load_config() -> tuple[dict, dict]:
    """Baca datasets.yaml (sama untuk semua) dan paths.local.yaml (milik Anda)."""
    datasets = yaml.safe_load((CFG_DIR / "datasets.yaml").read_text(encoding="utf-8"))
    local = CFG_DIR / "paths.local.yaml"
    if not local.is_file():
        raise FileNotFoundError(
            "config/paths.local.yaml belum ada.\n"
            "Salin config/paths.example.yaml menjadi config/paths.local.yaml, "
            "lalu isi jalur data di komputer Anda."
        )
    paths = yaml.safe_load(local.read_text(encoding="utf-8"))
    return datasets, paths


def sha256(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while blk := f.read(chunk):
            h.update(blk)
    return h.hexdigest()


# --------------------------------------------------------------------- pemuat
def load(dataset: str) -> list[Recording]:
    """Muat seluruh rekaman satu dataset."""
    datasets, paths = load_config()
    if dataset not in datasets:
        raise KeyError(f"dataset '{dataset}' tidak ada di config/datasets.yaml")
    if dataset not in paths:
        raise KeyError(f"jalur untuk '{dataset}' belum diisi di config/paths.local.yaml")
    reader = _READERS.get(dataset)
    if reader is None:
        raise NotImplementedError(
            f"pemuat untuk '{dataset}' belum ditulis. Tambahkan fungsinya di fogbench/data.py "
            f"dan daftarkan di _READERS. Pastikan keluarannya tetap enam kanal mentah."
        )
    recs = reader(Path(paths[dataset]), datasets[dataset])
    n_exp = datasets[dataset].get("n_pasien_diharapkan")
    n_got = len({r.subject for r in recs})
    if n_exp and n_got != n_exp:
        raise RuntimeError(
            f"dataset '{dataset}': ditemukan {n_got} pasien, seharusnya {n_exp}. "
            f"Periksa jalur data dan kelengkapan berkas sebelum melanjutkan."
        )
    return recs


def _read_figshare(root: Path, spec: dict) -> list[Recording]:
    imu = root / "IMU" / "IMU"
    if not imu.is_dir():
        imu = root / "IMU"
    if not imu.is_dir():
        raise FileNotFoundError(f"folder IMU tidak ditemukan di {root}")
    ac, gc, lc = spec["kolom"]["akselerasi"], spec["kolom"]["giroskop"], spec["kolom"]["label_fog"]
    subs = sorted({int(m.group(1)) for f in glob.glob(str(imu / "*_*.txt"))
                   if (m := re.match(r"SUB(\d+)_", Path(f).name))})
    recs: list[Recording] = []
    for sub in subs:
        files = sorted(glob.glob(str(imu / f"SUB{sub:02d}_[0-9].txt")))
        for si, path in enumerate(files):
            d = pd.read_csv(path, sep="\t")
            acc = d.iloc[:, ac].values.astype(np.float32)
            gyr = d.iloc[:, gc].values.astype(np.float32)
            y = (d.iloc[:, lc].values if d.shape[1] > lc else np.zeros(len(d)))
            recs.append(Recording(
                subject=sub, session=si, dataset="figshare", fs=int(spec["fs_hz"]),
                raw6=np.concatenate([acc, gyr], axis=1).astype(np.float32),
                y=(np.asarray(y) > 0).astype(np.int8),
                meta={"berkas": Path(path).name}))
    return recs


_READERS = {"figshare": _read_figshare}


# --------------------------------------------------------------------- laju evaluasi
def to_eval_rate(sig: np.ndarray, fs_src: int, fs_eval: int, is_label: bool = False) -> np.ndarray:
    """Ubah deret per sampel ke laju evaluasi bersama.

    Semua metode dinilai pada laju yang sama, apa pun laju internal modelnya.
    Probabilitas dirata-ratakan per blok, label diambil mayoritasnya.
    """
    sig = np.asarray(sig).ravel()
    if fs_src == fs_eval:
        return sig
    if fs_src % fs_eval != 0:
        idx = (np.arange(int(len(sig) * fs_eval / fs_src)) * fs_src / fs_eval).astype(int)
        return sig[np.clip(idx, 0, len(sig) - 1)]
    k = fs_src // fs_eval
    n = (len(sig) // k) * k
    blocks = sig[:n].reshape(-1, k)
    out = blocks.mean(axis=1)
    return (out >= 0.5).astype(np.int8) if is_label else out
