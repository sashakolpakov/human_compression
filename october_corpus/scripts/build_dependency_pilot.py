"""Draw the recorded L032 proof dependencies; this does not verify proofs."""
import argparse
from hashlib import sha256
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Patch, Rectangle

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "research/case_study"
DATA = STUDY / "phase202_dependency_pilot.json"
COLORS = {
    "retained": "#E5E7EB", "proved": "#DBEAFE", "computation": "#FEF3C7",
    "application": "#E9D5FF", "target": "#D1FAE5",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.output_dir.exists():
        raise ValueError("Use a fresh output directory.")
    data = json.loads(DATA.read_text())
    for binding in data["replacement_bindings"]:
        if sha256((STUDY / binding["path"]).read_bytes()).hexdigest() != binding["sha256"]:
            raise ValueError("Changed replacement edition: " + binding["path"])
    for graph in data["graphs"]:
        nodes = {node["id"]: node for node in graph["nodes"]}
        if len(nodes) != len(graph["nodes"]):
            raise ValueError("Duplicate node.")
        pending = set(nodes)
        edges = {(edge["from"], edge["to"]) for edge in graph["edges"]}
        if len(edges) != len(graph["edges"]) or not all(a in nodes and b in nodes for a,b in edges):
            raise ValueError("Invalid edge list.")
        while pending:
            ready = {v for v in pending if not any(b == v and a in pending for a,b in edges)}
            if not ready:
                raise ValueError("Dependency cycle.")
            pending -= ready
    plt.rcParams.update({"font.family": "DejaVu Sans", "svg.fonttype": "none"})
    fig, axes = plt.subplots(2, 1, figsize=(19, 12))
    drawings = []
    for ax, graph in zip(axes, data["graphs"]):
        nodes = {node["id"]: node for node in graph["nodes"]}
        labels_by_id = {}
        for node in nodes.values():
            labels_by_id[node["id"]] = ax.text(*node["xy"], node["label"], ha="center", va="center", fontsize=9.5,
                bbox=dict(boxstyle="round,pad=0.5", fc=COLORS[node["kind"]],
                          ec="#475569", lw=0.8), zorder=2)
        ax.set_title(graph["title"], loc="left", fontsize=14, pad=17)
        ax.set_xlim(-1.4, max(n["xy"][0] for n in nodes.values())+1.6)
        ax.set_ylim(-0.8, 6.3)
        ax.axis("off")
        drawings.append((ax, graph, nodes, labels_by_id))
    labels = {"retained":"Retained mathematics", "proved":"Written argument",
              "computation":"Reported computation", "application":"Application argument",
              "target":"Matched conclusion"}
    fig.legend(handles=[Patch(facecolor=COLORS[k], edgecolor="#475569", label=v)
                        for k,v in labels.items()], loc="lower center", ncol=5,
               bbox_to_anchor=(0.5, 0.035), frameon=False)
    fig.suptitle("One result, two proof structures", fontsize=19, x=0.06, ha="left", y=0.99)
    fig.text(0.06, 0.952, "Pilot: selected dependencies only. Node size is not proof length; no compression ratio is inferred.", fontsize=11)
    fig.text(0.06, 0.017, "Arrows run from a prerequisite to its use. External theorem interiors and the stronger hypertope branch are not expanded.", fontsize=10)
    fig.subplots_adjust(left=0.06, right=0.98, top=0.90, bottom=0.10, hspace=0.28)
    fig.canvas.draw()
    for ax, graph, nodes, labels_by_id in drawings:
        # Keep the clipping boxes in data coordinates so export DPI cannot
        # move arrowheads underneath the text boxes.
        boxes = {}
        for key, label in labels_by_id.items():
            bounds = label.get_bbox_patch().get_window_extent().transformed(ax.transData.inverted())
            boxes[key] = Rectangle((bounds.x0, bounds.y0), bounds.width, bounds.height,
                                   transform=ax.transData)
        for edge in graph["edges"]:
            a, b = edge["from"], edge["to"]
            ax.add_patch(FancyArrowPatch(nodes[a]["xy"], nodes[b]["xy"],
                patchA=boxes[a], patchB=boxes[b], arrowstyle="-|>",
                mutation_scale=13, shrinkA=3, shrinkB=3, color="#64748B", lw=1.25,
                zorder=1))
    args.output_dir.mkdir(parents=True)
    fig.savefig(args.output_dir / "dependency_pilot.svg", metadata={"Date": None})
    fig.savefig(args.output_dir / "dependency_pilot.png", dpi=140)
    report = {"data_sha256":sha256(DATA.read_bytes()).hexdigest(),
              "scope":"Topology and frozen replacement bytes checked; no mathematical or numerical compression admission.",
              "graphs":[{"id":g["id"], "nodes":len(g["nodes"]), "edges":len(g["edges"])} for g in data["graphs"]]}
    (args.output_dir / "report.json").write_text(json.dumps(report, indent=2)+"\n")
    print("PASS: two acyclic recorded graphs rendered; no length ratio claimed.")


if __name__ == "__main__":
    main()
