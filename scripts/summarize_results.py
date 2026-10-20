"""Buat ringkasan Markdown dari hasil eksperimen yang sudah tersimpan.

Contoh:
    python scripts/summarize_results.py results/freeze-index_figshare
    python scripts/summarize_results.py results/freeze-index_figshare --out results/freeze-index_figshare/report.md
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fogbench import report
from fogbench.metrics import sample_metrics


def _format_metric(value: float) -> str:
    """Format angka metrik, termasuk nilai tak terdefinisi."""
    return f"{value:.4f}"


def make_markdown(folder: Path) -> str:
    summary = report.summarize(folder)
    pooled = summary["pooled"]
    per_subject = summary["per_subject_ringkas"]
    card = summary["model_card"]
    valid_subject_count = per_subject["n"]

    lines = [
        f"# Ringkasan hasil: {summary['model']}",
        "",
        f"- **Dataset:** {summary['dataset']}",
        f"- **Fold tersedia:** {summary['n_fold']}",
        f"- **Jumlah parameter:** {card.get('n_parameter', '-')}",
        f"- **Total waktu latih:** {summary['train_time_s_total']:.2f} detik",
        f"- **Median waktu inferensi:** {summary['infer_time_ms_median']:.2f} ms",
        "",
        "## Metrik gabungan",
        "",
        "| AUROC pooled | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode |",
        "|---:|---:|---:|---:|---:|---:|",
        (
            f"| {_format_metric(pooled['auroc'])} | {_format_metric(pooled['auprc'])} "
            f"| {_format_metric(pooled['sensitivitas'])} "
            f"| {_format_metric(pooled['spesifisitas'])} "
            f"| {_format_metric(pooled['f1'])} "
            f"| {_format_metric(pooled['episode_f1'])} |"
        ),
        "",
        "## AUROC per pasien", 
        "",
        (
            f"- **Rerata ± SD:** {_format_metric(per_subject['auroc_mean'])} ± "
            f"{_format_metric(per_subject['auroc_sd'])} "
            f"(n = {valid_subject_count})"
        ),
        (
            f"- **IK bootstrap 95%:** "
            f"[{_format_metric(per_subject['auroc_ci95'][0])}, "
            f"{_format_metric(per_subject['auroc_ci95'][1])}]"
        ),
        "",
        "| Pasien uji | AUROC | AUPRC | Sensitivitas | Spesifisitas | F1 | F1 episode | Waktu Latih (s) | Waktu Inferensi (ms) |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for fold in report.load_run(folder):
        metrics = sample_metrics(
            fold["y_true"],
            fold["p_mean"],
            fold["threshold"],
        )
        lines.append(
            f"| {fold['test_subject']} | {_format_metric(metrics['auroc'])} "
            f"| {_format_metric(metrics['auprc'])} "
            f"| {_format_metric(metrics['sensitivitas'])} "
            f"| {_format_metric(metrics['spesifisitas'])} "
            f"| {_format_metric(metrics['f1'])} "
            f"| {_format_metric(metrics['episode_f1'])} "
            f"| {_format_metric(fold.get('train_time_s', 0.0))} "
            f"| {_format_metric(fold.get('infer_time_ms', 0.0))} |"
        )

    lines.extend(["", "## Kartu metode", "", "### Hiperparameter", ""])

    hiperparameter = card.get("hiperparameter", {})

    if isinstance(hiperparameter, dict):
        for nama, nilai in hiperparameter.items():
            if isinstance(nilai, list):
                nilai = ", ".join(map(str, nilai))
            lines.append(f"- **{nama.replace('_', ' ').capitalize()}:** {nilai}")
    else:
        lines.append(f"- {hiperparameter}")
    
    deviations = card.get("deviasi", [])
    if isinstance(deviations, str):
        deviations = [deviations]
    if deviations:
        lines.append("- **Deviasi dari metode acuan:**")
        lines.extend(f"  - {deviation}" for deviation in deviations)
    else:
        lines.append("- **Deviasi dari metode acuan:** tidak dicatat.")
    lines.extend([
        "",
        "> IK bootstrap dan statistik AUROC per pasien hanya bermakna jika tersedia "
        "lebih dari satu pasien dengan kedua kelas label. Pasien tanpa kedua kelas "
        "tidak memiliki AUROC/AUPRC dan tidak masuk ringkasan per pasien.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Ringkas metrik dan waktu dari folder hasil benchmark."
    )
    parser.add_argument("folder", type=Path, help="folder berisi fold_*.json")
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
        help="simpan laporan Markdown ke path ini; jika tidak diisi, cetak ke terminal",
    )
    args = parser.parse_args()

    try:
        markdown = make_markdown(args.folder)
    except (FileNotFoundError, KeyError, ValueError) as exc:
        parser.error(str(exc))

    if args.out is None:
        print(markdown)
    else:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(markdown, encoding="utf-8")
        print(f"Laporan disimpan: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
