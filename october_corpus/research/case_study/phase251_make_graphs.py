"""Render the two-paper measurement and explicit theorem dependency graphs.

No primary publication text is read or exported by this script.
"""
from pathlib import Path
import argparse
import json
import os


def graph_data():
    sources = {
        "D": ("Dickson and projective subgroup theory", "retained external input", "L083 Theorem2; L079 Propositions1–2"),
        "P": ("C-groups, polytopes and local maps", "retained external input", "both sources §2; L083 §5"),
        "R": ("Earlier PSL2 rank bound", "retained external input", "L083 p2, reference[14]"),
        "S083": ("String setup and proper parabolics", "L083", "§2 and start of §4"),
        "L1": ("Odd characteristic", "L083", "Lemma1, p5"),
        "L2": ("Odd end labels", "L083", "Lemma2, p5"),
        "L3": ("Subfield intersection count", "L083", "Lemma3, p6; distinct conjugates in proof"),
        "L4": ("Exclude PSL2 facets", "L083", "Lemma4, p6"),
        "L5": ("Cyclic intersections and normalizers", "L083", "Lemma5, p7"),
        "L6": ("Exclude PGL2 facets", "L083", "Lemma6, pp7–8"),
        "T": ("Local maps and ten universal groups", "L083", "Table1, p9; computation or hand calculation"),
        "C083": ("PSL2 classification", "L083", "Theorems1 and3, pp2,9"),
        "G083": ("Geometric properties and even subgroup", "L083", "Theorem4 and §5, pp10–11"),
        "S079": ("String setup and subgroup alternatives", "L079", "§2 and start of §4"),
        "R079": ("PGL2 rank bound", "L079", "Lemma3, p4"),
        "O079": ("Odd end labels", "L079", "Lemma4, p5"),
        "I079": ("Subfield containment and intersections", "L079", "Lemmas5–6, pp5–6; repeats earlier counting argument"),
        "A079": ("Exclude affine facets", "L079", "Lemma7, p6"),
        "F079": ("Exclude PSL2 and PGL2 facets", "L079", "Lemmas8–9, pp6–7"),
        "C079": ("PGL2 classification", "L079", "Theorem10, p7"),
    }
    old_edges = [
        ("P","S083","definitions and intersection property"),
        ("D","L1","possible subgroup C2 times a dihedral group"),
        ("S083","L1","independent nonadjacent generators"),
        ("D","L2","forbidden four-group times a dihedral group"),
        ("L1","L2","odd characteristic"),
        ("D","L3","multiplicity and normalizer counts"),
        ("L3","L4","facet and its conjugate"),
        ("S083","L4","properness and intersection property"),
        ("L3","L5","cyclic normalizer argument"),
        ("L3","L6","dihedral intersection exclusion"),
        ("L5","L6","normalizer containment"),
        ("L2","L6","odd endpoint order"),
        ("D","C083","remaining exceptional subgroup types and group orders"),
        ("R","C083","rank at most four is cited, not reproved"),
        ("L1","C083","characteristic restriction"),
        ("L4","C083","PSL2 facets excluded"),
        ("L6","C083","PGL2 facets excluded"),
        ("P","T","classical six local maps"),
        ("T","C083","universal group table and quotient orders"),
        ("C083","G083","the two surviving groups"),
        ("P","G083","local maps, cosets and universal covers"),
        ("T","G083","marked universal presentations"),
        ("D","G083","simplicity for the even subgroup"),
        ("P","S079","definitions and intersection property"),
        ("D","S079","Propositions1–2 subgroup alternatives"),
        ("C083","S079","earlier PSL2 result excludes characteristic two, p4"),
        ("D","R079","involution centralizers and dihedral alternatives"),
        ("S079","R079","rank and independence constraints"),
        ("D","O079","centralizer bound; earlier PSL2 facts invoked"),
        ("S079","O079","nonadjacent parabolic"),
        ("D","I079","multiplicities and normalizers"),
        ("L3","I079","earlier proof repeated in a stronger form, pp5–6"),
        ("D","A079","unipotent normalizer and absence of D4p"),
        ("S079","A079","independent commuting involution"),
        ("I079","F079","intersection exclusion and normalizers"),
        ("O079","F079","odd order and index two"),
        ("S079","F079","proper facet conjugates"),
        ("R079","C079","rank reduction"),
        ("A079","C079","affine alternative excluded"),
        ("F079","C079","subfield alternatives excluded"),
        ("T","C079","L083 Table1 explicitly reused, not reprinted"),
        ("D","C079","group orders and simplicity"),
    ]
    ours = {
        "D": ("Dickson types, embeddings and group facts", "retained external input", "U_E InputD"),
        "P": ("C-groups, polytopes and local maps", "retained external input", "U_E InputP and applications"),
        "S": ("Indecomposability and string consequences", "U_E", "§2"),
        "N": ("Odd-order normalizer lemma", "U_E", "Lemma2"),
        "C2": ("Characteristic-two centralizer", "U_E", "Lemma3"),
        "V": ("Four-group centralizer", "U_E", "Lemma4"),
        "C": ("Dihedral centralizer descent", "U_E", "Theorem5"),
        "O": ("Odd end labels", "U_E", "Corollary6"),
        "R": ("Uniform rank restriction", "U_E", "Proposition7"),
        "L": ("Elementary facet exclusions", "U_E", "Lemma8"),
        "F": ("Exceptional facets only", "U_E", "Theorem9"),
        "Code": ("Complete exact finite program", "required program", "phase230_finite_check.g"),
        "Loc": ("Six local classes", "U_E", "Lemma10"),
        "Tab": ("Ten universal presentations", "U_E", "Lemma11"),
        "U": ("Uniform reduction", "U_E", "Theorem1, proof §6"),
        "A1": ("PSL2 classification and geometry", "A1", "complete phase238_L083_application.md"),
        "A2": ("PGL2 classification and simplex", "A2", "complete phase238_L079_application.md"),
    }
    new_edges = [
        ("D","S","simplicity and direct indecomposability"),
        ("C","O","unique nontrivial dihedral centralizer"),
        ("C2","R","excludes characteristic two"),
        ("V","R","excludes independent commuting triple"),
        ("S","R","consecutive labels at least three"),
        ("D","F","proper subgroup types with natural embeddings"),
        ("L","F","elementary and affine alternatives excluded"),
        ("S","F","properness and irreducibility"),
        ("R","F","odd characteristic"),
        ("C","F","centralizer stays in the smaller projective group"),
        ("N","F","normalizer plus odd endpoint order"),
        ("O","F","odd endpoint order"),
        ("Code","Loc","exhaustive local markings and presentation orders"),
        ("Loc","Tab","fourteen compatible ordered pairs"),
        ("Code","Tab","exact universal orders and all markings"),
        ("P","Tab","coset indices and incidences interpreted as polytope face counts and K11"),
        ("R","U","rank and characteristic"),
        ("F","U","exceptional end groups"),
        ("Loc","U","six local markings"),
        ("Tab","U","surjection from one of ten presentations"),
        ("U","A1","common reduction"),
        ("Tab","A1","quotient elimination and marked uniqueness"),
        ("D","A1","orders and simplicity"),
        ("P","A1","cosets, duality, local maps and covering theorem"),
        ("U","A2","common reduction"),
        ("Tab","A2","quotient elimination and explicit simplex marking"),
        ("D","A2","orders and index-two subgroup structure"),
        ("P","A2","polytope interpretation"),
    ]
    def assemble(nodes, edges):
        ids = set(nodes)
        outgoing = {k: [] for k in ids}
        for a,b,_ in edges:
            if a not in ids or b not in ids:
                raise ValueError("unknown graph vertex")
            outgoing[a].append(b)
        visited, active = set(), set()
        def visit(k):
            if k in active:
                raise ValueError("dependency cycle")
            if k in visited:
                return
            active.add(k)
            for child in outgoing[k]:
                visit(child)
            active.remove(k)
            visited.add(k)
        for k in ids:
            visit(k)
        return {"nodes": [{"id": k, "label": v[0], "document": v[1], "locator": v[2]} for k,v in nodes.items()],
                "edges": [{"from": a, "to": b, "reason": c} for a,b,c in edges]}
    return {
        "scope": "Proof dependencies of the matched principal contracts, grouped at named lemmas or closely connected blocks.",
        "not_a_minimal_dag": True,
        "cost_assignment": "Costs are measured at full selected document level. Nodes have no separate numerical weights; node counts are not complexity ratios.",
        "source_auxiliary_lemmas": "Historical proof steps are represented, not claimed individually recovered or newly verified by the replacement.",
        "source": assemble(sources, old_edges), "replacement": assemble(ours, new_edges),
        "cross_topic_discount": False,
        "formal_verification": "Optional Lean verification is separate from mathematical-premise edges; scope remains partial.",
    }


def main(root, preview=None):
    data = graph_data()
    (root / "phase251_dependency_dags.json").write_text(json.dumps(data, indent=2) + "\n")
    parts = ["# Theorem dependencies for the projective-line comparison", "",
             data["scope"], "", data["cost_assignment"], "",
             "External inputs remain explicit. Arrows point from a premise to its use.", ""]
    for name in ["source", "replacement"]:
        parts += ["## " + name.capitalize(), "", "```mermaid", "flowchart TD"]
        for n in data[name]["nodes"]:
            parts.append('  ' + n["id"] + '["' + n["document"] + ': ' + n["label"] + '"]')
        for e in data[name]["edges"]:
            parts.append("  " + e["from"] + " --> " + e["to"])
        parts += ["```", ""]
    parts += ["The source graph retains three explicit forms of reuse from L083 in L079:",
              "the characteristic-two exclusion, the subfield counting argument, and Table1.",
              "The replacement graph has no dependency from A1 to A2; both use U_E.", ""]
    (root / "phase251_dependency_dags.md").write_text("\n".join(parts))
    report = json.loads((root / "phase251_measurement.json").read_text())
    c = {k: v["NFC"]["characters_without_whitespace"] for k,v in report["costs"].items()}
    os.environ.setdefault("MPLCONFIGDIR", "/private/tmp/phase251-matplotlib")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.4), layout="constrained")
    ax = axs[0]
    ax.bar([0,1,2], [c["U_E"],c["A1"],c["A2"]], .34, color="#20639b", label="Replacement writing")
    ax.bar([0], [c["Code"]], .34, bottom=[c["U_E"]], color="#73b3d8", label="Required code appendix")
    ax.bar([1.36,2.36], [c["L083"],c["L079"]], .34, color="#ad5934", label="Historical matched text")
    ax.set_xticks([0,1.18,2.18], ["Acquire U_E", "PSL2\nA1 / L083", "PGL2\nA2 / L079"])
    ax.set_ylabel("NFC characters without whitespace")
    ax.set_title("Acquisition and individual applications")
    ax.legend(fontsize=8)
    ax = axs[1]
    ax.plot([0,1,2], [0,c["L083"],c["L083"]+c["L079"]], "o-", color="#ad5934", label="Historical matched text")
    base = [c["U_E"],c["U_E"]+c["A1"],c["U_E"]+c["A1"]+c["A2"]]
    ax.plot([0,1,2], base, "o-", color="#20639b", label="Replacement writing")
    ax.plot([0,1,2], [x+c["Code"] for x in base], "o--", color="#287e9b", label="Replacement plus required code")
    ax.set_xticks([0,1,2], ["Acquisition", "PSL2", "+ PGL2"])
    ax.set_title("Cumulative cost; only two applications")
    ax.legend(fontsize=8)
    for ax in axs:
        ax.grid(axis="y", alpha=.2)
        ax.set_ylim(bottom=0)
    fig.suptitle("Topic E: local savings have not yet repaid the umbrella", fontsize=14)
    fig.savefig(root / "phase251_complexity.svg", metadata={"Date": None})
    if preview is not None:
        fig.savefig(preview, dpi=140)
    plt.close(fig)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--preview", type=Path)
    args = parser.parse_args()
    main(args.root, args.preview)
