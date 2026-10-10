#!/usr/bin/env python3
"""Render the paper map from frozen records without rewriting their metadata.

The earlier generator and detailed reader are preserved in archive/. The current
reader applies the recorded assessments in memory and checks their hash chain and
counts. Rendering does not rerun mathematical proofs or refresh the literature.
"""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "research/case_study"
OVERLAYS = (
    "phase181_registry_overlay.json",
    "phase185_L092_overlay.json",
    "phase189_L068_overlay.json",
    "phase193_F010_overlay.json",
    "phase208_L092_overlay.json",
    "phase233_F014_overlay.json",
)


def load(name):
    return json.loads((STUDY / name).read_text())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def view_counts(rows):
    return {
        "indexed": len(rows),
        "retrieved_full_text": sum(r["access_coverage"]["retrieved_full_text"] for r in rows),
        "encoded": sum(r["encoded"] for r in rows),
        "rederived": sum(r["rederived"] for r in rows),
        "full_principal_results": sum(r["full_principal_results"] for r in rows),
        "reading_categories": dict(Counter(r["access_coverage"]["reading_category"] for r in rows)),
    }


def registry_view():
    """Apply only the published additions; no saved record is mutated."""
    registry = load("paper_registry.json")
    rows = {r["id"]: r for r in registry["entries"]}
    require(len(rows) == len(registry["entries"]), "Duplicate source identifiers")
    previous = "paper_registry.json"
    for name in OVERLAYS:
        overlay = load(name)
        predecessor = overlay.get("baseline", overlay.get("previous_assessment"))
        require(predecessor["path"] == previous, f"Unexpected predecessor for {name}")
        require(sha256((STUDY / previous).read_bytes()).hexdigest() == predecessor["sha256"],
                f"Recorded predecessor hash differs for {name}")
        updates = overlay.get("updates", [overlay])
        for update in updates:
            row = rows[update["id"]]
            for field in ("status", "encoded", "rederived", "full_principal_results"):
                # Single-paper additions use 'status' for the review itself,
                # rather than for the registry's mathematical progress category.
                if field in update and (field != "status" or "updates" in overlay):
                    row[field] = update[field]
            if "reading_category" in update:
                row["access_coverage"]["reading_category"] = update["reading_category"]
            if update.get("new_known_result_rederivation_credits", 0):
                require(not row["rederived"], f"Repeated addition for {row['id']}")
                row["encoded"] = row["rederived"] = True
                row["status"] = ("principal_results_rederived" if row["full_principal_results"]
                                 else "component_rederived")
            row["current_record"] = name
        actual = view_counts(registry["entries"])
        require(actual == overlay["counts_after_overlay"], f"Counts disagree with {name}: {actual}")
        previous = name
    registry["current_counts"] = view_counts(registry["entries"])
    return registry


def escaped(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def linked_title(row):
    title = escaped(row["title"])
    return f"[{title}]({row['primary_urls'][0]})" if row["primary_urls"] else title


def stage(row):
    return {
        "principal_results_rederived": "stated main results recovered",
        "component_rederived": "part of the results recovered",
        "finite_subfamily_reproduced": "a finite subfamily recovered",
        "conditional_component": "part recovered under stated assumptions",
        "proposed_new_result": "proposed answer or new result",
        "partial_progress": "partial progress",
        "generic_encoding": "explicit representation or test",
        "source_theorem_retained": "earlier theorem used as an input",
        "related_only": "related work only",
        "outside_current_core": "outside the present study",
        "unassessed": "not assessed",
    }[row["status"]]


def render(registry):
    rows, counts = registry["entries"], registry["current_counts"]
    older = [r for r in rows if r["year"] is not None and 1996 <= r["year"] <= 2006]
    principal = ", ".join(r["id"] for r in rows if r["full_principal_results"])
    origins = registry["counts"]
    out = [
        "# Paper registry: sources read and results recovered", "",
        f"**{len(rows)} mathematical works** are indexed: {origins['catalogue']} catalogue entries, "
        f"{origins['followup']} followups and {origins['network']} network additions. "
        f"**{len(older)} entries date from 1996–2006.**",
        "The registry includes books, proceedings papers and errata as well as journal articles.",
        "It records what was obtained, how much was read and which results have been assessed.",
        "It is neither a record of complete proof reading nor an exhaustive bibliography of",
        "every collaborator, student or postdoc. Coauthorship alone does not establish those relationships.", "",
        "The [current programme](MANUSCRIPT_PROGRAM.md) organizes the new papers by topic,",
        "with a full umbrella for each topic and complete applications to historical papers.",
        "Its A–D tables name the results already available for reworking. The counts below",
        "describe the source records; they do not count completed new application papers",
        "or measure compression.", "",
        "The [frozen registry](research/case_study/paper_registry.json) contains the detailed",
        "earlier records. The reviewed additions below update the displayed view without",
        "rewriting those records. The [previous paper map](archive/PAPER_MAP.previous.md)",
        "preserves the longer historical assessments, earlier compilation summaries and",
        "their measurements. See the [archive](archive/README.md) for those editions.", "",
        "## Reading and mathematical progress", "",
        "| Stage | Meaning |", "|---|---|",
        "| Retrieved | A primary full text was obtained and matched to the source. |",
        "| Read | The record distinguishes an abstract, a text search, selected sections and a complete reading. |",
        "| Encoded | A specified result has an explicit representation or test. |",
        "| Rederived | A named theorem, part of a theorem or finite subfamily has a replacement proof, with earlier results used by that proof stated. |",
        "| Main results recovered | The specified main results are recovered; this need not include every auxiliary assertion or imported classification. |",
        "| Proposed answer or new result | An internally checked argument is recorded; external review and verification of historical priority remain. |",
        "| Not assessed | No replacement proof has been assessed. This does not imply that the result is unknown or that any question remains open. |", "",
        "These categories describe different aspects of the work and overlap. Obtaining a",
        "paper does not establish a replacement proof. Progress on a question quoted in a",
        "survey does not imply that its original source has been read.", "",
        "| Access category | Works |", "|---|---:|",
    ]
    out += [f"| {key.replace('_', ' ')} | {value} |"
            for key, value in sorted(counts["reading_categories"].items())]
    out += [
        "", f"**{counts['retrieved_full_text']}** works have a retrieved full text; "
        f"**{counts['encoded']}** have an explicit representation or a specified conditional or partial derivation; "
        f"**{counts['rederived']}** have a recovered result, finite subfamily or stated main result.", "",
        f"The set with **stated main results recovered contains {counts['full_principal_results']} works: {principal}**.",
        "The exact targets and qualifications govern membership in this set. Proposed",
        "conjecture proofs do not add to it. The [question catalogue](CONJECTURE_RESULTS.md)",
        "keeps answers to questions separate from recovery of published results.", "",
        "## Reviewed additions to the frozen registry", "",
        "These additions supply the current counts and the revised entries below. Their",
        "files preserve the exact statements, earlier results used, evidence and remaining work.", "",
        "| Sources | Results and qualifications | Record |", "|---|---|---|",
        "| L073 and L104 | L073: 81 rank-two and 431 rank-three classes, witnesses and geometric shadows; refined correspondence with the printed table remains incomplete. L104: the fixed 8/19/3 census in ranks 2/3/4 and exclusion of higher ranks; further diagrams, full geometric automorphism and correlation groups, and the doubling assertion remain outside the recovered results. | [Reviewed census addition](research/case_study/phase181_registry_overlay.json) |",
        "| L092 | Corrected rank-three applications, complete higher-rank Steiner classification and rank-six M24 construction. The two quoted classifications remain external inputs; partial linearity in Theorem 1 and missing Pasini named-residue maps remain explicit. Lean verifies specified finite incidences and counterexamples. The existing Hermitian-unital answer is counted separately, once. | [Earlier corrections](research/case_study/phase185_L092_overlay.json); [main-result admission](research/case_study/phase208_L092_overlay.json); [proof reader](DESIGN_RESIDUES.md) |",
        "| L068 | Complete primary text read; construction P recovered as printed and Q recovered after an explicit repair. This adds a partial derivation, with the necessary group and graph inputs stated. | [Construction review](research/case_study/phase189_L068_overlay.json); [proof reader](GRAPH_INCIDENCE.md) |",
        "| F010 | The main constructive theorems are recovered in a complete written argument, with local corrections. Lean verifies the stated hexagon component, not the universal constructions. | [Reviewed addition](research/case_study/phase193_F010_overlay.json); [proof reader](FINITE_INCIDENCE_REPRESENTATIONS.md) |",
        "| F014 | All stated positive rank-three main results in arXiv v1: exact construction, matrices, universal presentation and both corollaries. Montero–Ivić Weiss supply the earlier polygon construction; the printed inverse-action convention is corrected. The higher-rank counterexample is a separate result. | [Reviewed addition](research/case_study/phase233_F014_overlay.json); [complete application](EQUAL_LABEL_POLYGONS.md) |", "",
        "Earlier mistaken PDF identifications for L097, L098, L101 and L123 remain",
        "explicitly rejected; those entries have only abstract-level access. L125's",
        "original J1 list must be read with the later correction reported by L105.", "",
        "## Complete registry", "",
        "All 161 records appear below, including papers for which no exact result has",
        "been assessed. Each result label is limited by its detailed statement and",
        "remaining-work record in the frozen JSON or the reviewed additions above.", "",
        "| ID | Year | Work | Reading | Mathematical progress |", "|---|---:|---|---|---|",
    ]
    for row in rows:
        year = row["year"] if row["year"] is not None else "unconfirmed"
        category = row["access_coverage"]["reading_category"].replace("_", " ")
        progress = stage(row)
        if "current_record" in row:
            progress = f"[{progress}](research/case_study/{row['current_record']})"
        out.append(f"| {row['id']} | {year} | {linked_title(row)} | {category} | {progress} |")
    out += [
        "", "## Rebuilding this reader", "",
        "The generator reads the frozen registry and its reviewed additions, verifies",
        "their hash chain and counts, and writes only this Markdown page. It does not",
        "change metadata, rerun proofs or refresh the literature search.", "",
        "```sh", "python3 scripts/build_paper_registry.py",
        "python3 scripts/build_paper_registry.py --check", "```", "",
        "A new mathematical assessment needs an exact statement, its proof and the",
        "earlier results it uses. It should be recorded and reviewed before an addition",
        "is included in this reader. Complete formalization, later-literature checks",
        "and measurements remain separate tasks. See [reproduction instructions](REPRODUCING.md).", "",
    ]
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check the reader without writing files")
    args = parser.parse_args()
    registry = registry_view()
    text = render(registry)
    target = ROOT / "PAPER_MAP.md"
    if args.check:
        require(target.read_text() == text, "PAPER_MAP.md differs from the recorded registry view")
        print(f"Paper map matches the frozen registry and all {len(OVERLAYS)} reviewed additions.")
    else:
        target.write_text(text)
        print("Wrote PAPER_MAP.md; frozen registry and reviewed additions unchanged.")
    print(json.dumps(registry["current_counts"], indent=2))


if __name__ == "__main__":
    main()
