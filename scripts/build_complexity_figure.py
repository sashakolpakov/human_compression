#!/usr/bin/env python3
"""Plot admitted cost checkpoints and length ratios; no new proof measurement.

Requires matplotlib. Reads only the two hash-bound public measurement records.
The output directory must be new. A PNG preview is optional and not published.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "research/case_study"
PINS = {
    "phase138_cost_checkpoint.json":
        "712544463edd4bbe15ced5dbbd8ff0782e14eaac34c3a25c97ba2ff6d88dc293",
    "phase144_author_primary_recount.json":
        "e085070162f866f7ba5277a57bdc0db916aea92744cd023fbce04546ed69a3a6",
}


def require(test, message):
    if not test:
        raise ValueError(message)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--preview", action="store_true")
    args = ap.parse_args()
    require(not args.output_dir.exists() and not args.output_dir.is_symlink(),
            "A fresh output directory is required")
    bound = {}
    for name, digest in PINS.items():
        data = (STUDY / name).read_bytes()
        require(sha256(data).hexdigest() == digest, "Changed measurement: " + name)
        bound[name] = json.loads(data)
    costs = bound["phase138_cost_checkpoint.json"]
    measured = bound["phase144_author_primary_recount.json"]
    require(measured["status"] == "PASS", "Unaccepted measurement")
    baselines = costs["baselines"]
    checkpoints = [
        {"label": "Corrected five-source baseline", "principal_sources": 5,
         "raw_utf8_bytes": baselines["five_source_with_N009_correction"]["whole_package_bytes"]},
        {"label": "Six-source additive package", "principal_sources": 6,
         "raw_utf8_bytes": baselines["six_source_additive_with_both_corrections"]["whole_package_bytes"]},
        {"label": "Six-source integrated U+A", "principal_sources": 6,
         "raw_utf8_bytes": costs["whole_U_A_four_artifact_bytes"]},
    ]
    lengths = [p["raw_utf8_bytes"] for p in checkpoints]
    require(lengths == [196962, 214717, 208861], "Changed admitted checkpoints")
    delta = lengths[2] - lengths[1]
    require(delta == baselines["six_source_additive_with_both_corrections"]["diff"]["signed_net_bytes"],
            "Checkpoint delta disagrees with recorded diff")
    names = [
        ("whitespace_tokens", "Whitespace tokens"),
        ("alphanumeric_units", "Alphanumeric units"),
        ("characters_without_whitespace", "Nonwhitespace characters"),
        ("characters_with_collapsed_whitespace", "Collapsed-whitespace characters"),
        ("utf8_bytes_with_collapsed_whitespace", "Collapsed-whitespace UTF-8 bytes"),
    ]
    ratios = []
    for key, label in names:
        n = measured["source_body_sums"]["NFC"][key]
        d = measured["denominator"]["NFC"][key]
        require(n / d == measured["comparisons"]["NFC"][key]["factor"],
                "Ratio disagrees with recorded lengths")
        ratios.append({"metric": key, "label": label, "numerator": n,
                       "denominator": d, "source_over_replacement": n / d})
    report = {
        "status": "PLOT_OF_PREVIOUSLY_ADMITTED_MEASUREMENTS",
        "bound_inputs": PINS,
        "checkpoints": checkpoints,
        "checkpoint_scope": "Comparable corrected packages, not equally spaced observation dates.",
        "source_addition_bytes": lengths[1] - lengths[0],
        "fixed_six_source_change_bytes": delta,
        "fixed_six_source_reduction_percent": -100 * delta / lengths[1],
        "ratios": ratios,
        "ratio_scope": "Six specified source bodies divided by full U+A and all four required programs; NFC PDF-text metrics.",
        "raw_inventory_and_PDF_metrics_are_distinct": True,
        "repeating_sawtooth_established": False,
        "aggregate_A_to_D_ratio_measured": False,
        "new_source_measurement_or_proof_execution": False,
    }
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                         "svg.fonttype": "none", "svg.hashsalt": "human-compression-cost-v1"})
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={"width_ratios": [1, 1.15]})
    fig.patch.set_facecolor("#ffffff")
    fig.suptitle("Human Compression: what the measurements establish", fontsize=17, x=0.06, ha="left", y=0.97)
    ax = axes[0]
    ax.set_title("U+A: comparable corrected packages", loc="left", pad=18, fontsize=12)
    ax.plot([0, 1], lengths[:2], color="#a35d22", linewidth=2, marker="o")
    ax.plot([1, 2], lengths[1:], color="#287663", linewidth=2, marker="o")
    for x, y in enumerate(lengths):
        ax.annotate(f"{y:,}", (x, y), xytext=(0, 10), textcoords="offset points", ha="center", fontsize=11)
    ax.set_xticks([0, 1, 2], ["5 sources\ncorrected baseline", "6 sources\nadditive", "6 sources\nintegrated"])
    ax.set_xlim(-0.35, 2.35)
    ax.set_ylim(0, 245000)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x / 1000)}k"))
    ax.set_ylabel("Required raw UTF-8 bytes (full U + A + programs)")
    ax.text(0.06, 0.60, "+17,755 bytes: one source added", transform=ax.transAxes, color="#a35d22")
    ax.text(0.06, 0.43, f"−5,856 bytes: same six-source coverage\n{report['fixed_six_source_reduction_percent']:.2f}% reduction", transform=ax.transAxes, color="#287663", linespacing=1.6)
    ax.text(0.06, 0.20, "One fixed-coverage decrease.\nA repeating sawtooth is not yet established.", transform=ax.transAxes, color="#444444", linespacing=1.6)
    ax.grid(axis="y", alpha=0.15)
    ax.set_axisbelow(True)
    ax = axes[1]
    ax.set_title("Six-source compression: sensitivity to length metric", loc="left", pad=18, fontsize=12)
    values = [r["source_over_replacement"] for r in ratios]
    ax.barh(range(5), values, color="#386a8b", height=0.48)
    ax.set_yticks(range(5), [r["label"] for r in ratios], fontsize=9)
    ax.invert_yaxis()
    ax.set_xlim(0, 1.90)
    ax.axvline(1, color="#777777", linestyle="--", linewidth=1)
    ax.set_xlabel("Source length / complete replacement length")
    for y, value in enumerate(values):
        ax.text(value + 0.035, y, f"{value:.3f}×", va="center", fontsize=10)
    ax.grid(axis="x", alpha=0.15)
    ax.set_axisbelow(True)
    for ax in axes:
        ax.spines[["top", "right"]].set_visible(False)
    fig.subplots_adjust(left=0.07, right=0.97, top=0.83, bottom=0.23, wspace=0.72)
    fig.text(0.07, 0.09, "Left: raw file inventory. Right: NFC-normalized PDF text; full U, A and four programs included.\nThese are different measurements. No aggregate A–D source-length ratio has been established.", color="#555555", fontsize=10, linespacing=1.6)
    args.output_dir.mkdir(parents=True)
    fig.savefig(args.output_dir / "complexity.svg", metadata={"Date": None, "Creator": "scripts/build_complexity_figure.py"})
    if args.preview:
        fig.savefig(args.output_dir / "preview.png", dpi=140)
    plt.close(fig)
    (args.output_dir / "measurements.json").write_text(json.dumps(report, indent=2) + "\n")
    print("PASS: plotted three corrected checkpoints and all five admitted NFC ratios.")


if __name__ == "__main__":
    main()
