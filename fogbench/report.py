"""Ubah berkas hasil per fold menjadi tabel dan uji statistik."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.stats import wilcoxon

from fogbench.metrics import bootstrap_ci, pooled_and_per_subject


def load_run(folder: Path) -> list[dict]:
    return [json.loads(f.read_text(encoding="utf-8"))
            for f in sorted(Path(folder).glob("fold_*.json"))]


def summarize(folder: Path) -> dict:
    folds = load_run(folder)
    if not folds:
        raise FileNotFoundError(f"tidak ada hasil di {folder}")
    s = pooled_and_per_subject(folds)
    auroc = [m["auroc"] for m in s["per_subject"]]
    lo, hi = bootstrap_ci(auroc)
    s["per_subject_ringkas"]["auroc_ci95"] = [lo, hi]
    s["model"] = folds[0]["model"]
    s["dataset"] = folds[0]["dataset"]
    s["n_fold"] = len(folds)
    s["train_time_s_total"] = float(sum(f["train_time_s"] for f in folds))
    s["infer_time_ms_median"] = float(np.median([f["infer_time_ms"] for f in folds]))
    s["model_card"] = folds[0]["model_card"]
    return s



def table(folders: list[Path]) -> str:
    """Tabel perbandingan dalam format Markdown."""
    head = (
        "| Model | Pasien Latih | AUROC | AUPRC | Sensitivitas | Spesifisitas | "
        "F1 | F1 episode | AUROC per pasien | Waktu Latih (s) | "
        "Waktu Inferensi (ms) | Parameter |\n"
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|\n"
    )

    rows = ""
    for f in folders:
        s = summarize(Path(f))
        p, q = s["pooled"], s["per_subject_ringkas"]

        nama_folder = Path(f).name
        pasien_latih = nama_folder.rsplit("_train", 1)[-1]

        rows += (
            f"| {s['model']} "
            f"| {pasien_latih} "
            f"| {p['auroc']:.3f} "
            f"| {p['auprc']:.3f} "
            f"| {p['sensitivitas']:.3f} "
            f"| {p['spesifisitas']:.3f} "
            f"| {p['f1']:.3f} "
            f"| {p['episode_f1']:.3f} "
            f"| {q['auroc_mean']:.3f} ± {q['auroc_sd']:.3f} "
            f"| {s['train_time_s_total']:.2f} "
            f"| {s['infer_time_ms_median']:.2f} "
            f"| {s['model_card'].get('n_parameter', '-')} |\n"
        )

    return head + rows




def paired_tests(ref_folder: Path, other_folders: list[Path]) -> str:
    """Uji Wilcoxon berpasangan pada AUROC per pasien, dengan koreksi Holm."""
    def by_subject(folder):
        return {m["test_subject"]: m["auroc"] for m in summarize(Path(folder))["per_subject"]}

    ref = by_subject(ref_folder)
    hasil = []
    for f in other_folders:
        oth = by_subject(f)
        common = sorted(set(ref) & set(oth))
        a = np.array([ref[s] for s in common]); b = np.array([oth[s] for s in common])
        try:
            stat, p = wilcoxon(a, b)
        except ValueError:
            stat, p = float("nan"), 1.0
        lo, hi = bootstrap_ci(a - b)
        hasil.append({"model": summarize(Path(f))["model"], "n": len(common),
                      "selisih": float((a - b).mean()), "ci": (lo, hi),
                      "menang": int((a > b).sum()), "W": stat, "p": float(p)})
    # koreksi Holm
    order = sorted(range(len(hasil)), key=lambda i: hasil[i]["p"])
    m = len(hasil); prev = 0.0
    for rank, i in enumerate(order):
        adj = min(1.0, max(prev, (m - rank) * hasil[i]["p"]))
        hasil[i]["p_holm"] = adj; prev = adj

    out = ("| Pembanding | n | Selisih AUROC per pasien [IK 95%] | Menang | W | p | p Holm |\n"
           + "|---" * 7 + "|\n")
    for h in hasil:
        out += (f"| {h['model']} | {h['n']} | {h['selisih']:+.3f} "
                f"[{h['ci'][0]:+.3f}, {h['ci'][1]:+.3f}] | {h['menang']}/{h['n']} | "
                f"{h['W']:.0f} | {h['p']:.4f} | {h['p_holm']:.4f} |\n")
    return out
