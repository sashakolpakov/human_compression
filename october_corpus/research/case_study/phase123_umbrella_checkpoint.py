#!/usr/bin/env python3
"""Bind exact U statements/proofs and draft costs; no source-ratio inference."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import re
import unicodedata

BASE = Path(__file__).resolve().parent
MANUSCRIPT = BASE / "phase123_umbrella_manuscript.md"
PROVENANCE = BASE / "phase123_umbrella_provenance.md"
DEPS = {
    "U.K0": [], "U.K": ["U.K0"], "U.Q": [], "U.Coset": [],
    "U.D": [], "U.SK": ["U.K"], "U.SK.Local": ["U.SK"],
    "U.SK.Delete": ["U.SK", "U.D"], "U.SK.Central": ["U.SK"],
    "U.SK.Separator": ["U.SK"], "U.Fiber": [],
    "U.Nilpotent": ["U.D", "U.K"], "U.Ladder": [], "U.Order": [],
    "U.Helly": [], "U.Compare": ["U.Helly"],
    "U.Compare.Matrix": ["U.Compare"], "U.Geometry": [],
    "U.Action": ["U.Geometry"], "U.Orbits": [], "U.ExtensionOrbits": [],
    "U.RelativeBound": [], "U.Relative": [], "U.Maximal": [],
    "U.FrattiniTransport": [], "U.FrattiniLadder": ["U.Maximal"],
    "U.Phi": [], "U.Amalgam": [],
}
RETAINED = {
    "U.Nilpotent": ["lower-central graded commutator calculus",
                    "nilpotence of finite p-groups",
                    "epimorphic images of the lower central series"],
    "U.SK.Central": ["epimorphic images of the lower central series"],
    "U.Ladder": ["Burnside basis theorem", "orbit-stabilizer theorem"],
    "U.Phi": ["Burnside basis theorem"],
    "U.Maximal": ["Zorn's lemma"],
    "U.Amalgam": ["free-product universal property",
                   "amalgamated free-product normal-form theorem"],
}
ORIGIN = {
    "U.K0": ("reused_proof", "phase78 K(0)"),
    "U.K": ("reused_proof", "phase78 K(a)"),
    "U.Q": ("reused_proof", "phase78 K(d)"),
    "U.Coset": ("reused_proof", "phase78 K(b)"),
    "U.D": ("reused_proof", "phase78 Section 8"),
    "U.SK": ("new_integration_step", "phase117 and phase122 support induction"),
    "U.SK.Local": ("reorganized_proof", "phase117/phase122 antichain recognition"),
    "U.SK.Delete": ("new_integration_step", "phase122 derived local deletions"),
    "U.SK.Central": ("reorganized_proof", "phase117/phase122 lower central argument"),
    "U.SK.Separator": ("reused_proof", "phase117/phase122 supported separator"),
    "U.Fiber": ("reused_proof", "phase78 Section 8"),
    "U.Nilpotent": ("reorganized_proof", "phase78 Q5.5, exact-Q generalization"),
    "U.Ladder": ("reused_proof", "phase78 Q5.6"),
    "U.Order": ("reused_proof", "phase78 Section 8"),
    "U.Helly": ("reused_proof", "phase36 Section 4"),
    "U.Compare": ("reused_proof", "phase36 Sections 1-4"),
    "U.Compare.Matrix": ("reused_proof", "phase36 Section 6"),
    "U.Geometry": ("reused_proof", "phase78 O0/O1"),
    "U.Action": ("reused_proof", "phase78 K(c)"),
    "U.Orbits": ("reused_proof", "phase110 K(e)"),
    "U.ExtensionOrbits": ("reused_proof", "phase78 Section 21.1"),
    "U.RelativeBound": ("reused_proof", "phase78 R(a); CC02 source context"),
    "U.Relative": ("reused_proof", "phase78 R(b); CC02 source context"),
    "U.Maximal": ("reused_proof", "phase78 E1"),
    "U.FrattiniTransport": ("reused_proof", "phase78 E4; ACK05 source context"),
    "U.FrattiniLadder": ("reused_proof", "phase78 E2; ACK05 source context"),
    "U.Phi": ("reused_proof", "phase78 S; ACK05 source context"),
    "U.Amalgam": ("reorganized_proof", "phase78 Q9.1, arbitrary prime p"),
}
CONSUMERS = {
    "U.K": ["A Section 2 finite search", "A Section 7 complete census"],
    "U.Q": ["A Sections 6-7 central descent"],
    "U.D": ["A Sections 2-4 exact deletions"],
    "U.SK": ["A Section 4 edge inflation", "A Section 4 square sections"],
    "U.SK.Local": ["A Section 4 exact local recognition"],
    "U.SK.Delete": ["A Section 4 FAP deletion premise"],
    "U.SK.Central": ["A Section 4 global gamma_3 kernel"],
    "U.SK.Separator": ["A Section 4 path separator"],
    "U.Fiber": ["A Section 4 fork compatible product"],
    "U.Nilpotent": ["A Section 2 universal finite search", "A Section 7 census"],
    "U.Ladder": ["A Section 2 universal finite search", "A Section 7 census"],
    "U.Order": ["A Section 4 universal presentation recognition"],
    "U.Phi": ["A Section 2 forest quotient", "A Sections 5-7 Frattini coordinates"],
    "U.Amalgam": ["A Section 8 three free extensions"],
}
FORMAL = {
    "U.K0": {
        "status": "exact_reverse_implication_existing_declaration",
        "file": "formal/LiftCertificate.lean",
        "declarations": ["LeemansLift.intersection_of_image_and_kernel"],
        "gap": "The trivial forward implication and this new U interface are not newly compiled."
    },
    "U.K": {
        "status": "algebraic_component_only",
        "file": "formal/LiftCertificate.lean",
        "declarations": ["LeemansLift.intersection_of_image_and_kernel"],
        "gap": "Quantified actual-marking equivalence not bound by a new wrapper."
    },
    "U.Q": {
        "status": "complete_exact_existing_declarations",
        "file": "formal/QuotientIntersectionCriterion.lean",
        "declarations": [
            "MathCompression.QuotientIntersectionCriterion.image_inf_iff_kernel_product",
            "MathCompression.QuotientIntersectionCriterion.quotient_inf_iff_kernel_product"],
        "gap": "Application hypotheses and new U bindings still need formal connection."
    },
    "U.D": {
        "status": "range_meet_component_only",
        "file": "formal/BooleanRetractions.lean",
        "declarations": ["MathCompression.BooleanRetractions.range_intersection"],
        "gap": "Actual deletion construction, marked images, kernel normal closure and split product."
    },
    "U.SK": {
        "status": "final_transport_after_assumed_profile_only",
        "file": "formal/CoordinateKernels.lean",
        "declarations": ["LeemansCoordinates.coordinate_kernel_meet",
                         "LeemansCoordinates.intersection_transport_with_coordinates"],
        "gap": "Full fiber generation, support induction, kernel-product identification and hcoords proof."
    },
    "U.Compare": {
        "status": "complete_exact_existing_declaration_at_stronger_rank_scope",
        "file": "formal/ParabolicMarkedComparison.lean",
        "declarations": ["MathCompression.ParabolicMarkedComparison.quotient_marking_comparison"],
        "gap": "Arithmetic and geometric applications; no new compile performed in phase123."
    },
}
INPUTS = [
    "phase78_n009_integration_manuscript.md",
    "phase36_parabolic_comparison.md",
    "phase110_commuting_pairs_integration_core.md",
    "phase117_reusable_proof_legs_supported_kernels.md",
    "phase122_supported_kernel_early_review.md",
    "phase117_two_group_application.md",
    "phase121_gkm_method_inputs.json",
    "formal/LiftCertificate.lean", "formal/CoordinateKernels.lean",
    "formal/BooleanRetractions.lean", "formal/QuotientIntersectionCriterion.lean",
    "formal/ParabolicMarkedComparison.lean", "formal/ParabolicProductComparison.lean",
    "formal/OneExceptionalParabolic.lean", "formal/ParabolicQuotientTransport.lean",
]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def measure(text: str) -> dict:
    return {"sha256_utf8": sha(text.encode()), "utf8_bytes": len(text.encode()),
            "codepoints": len(text),
            "plain_NFC_whitespace_tokens": len(unicodedata.normalize("NFC", text).split())}


def bound(path: Path) -> dict:
    data = path.read_bytes()
    return {"path": path.name if path.parent == BASE else str(path.relative_to(BASE)),
            "sha256": sha(data), "utf8_bytes": len(data)}


def write_new(path: Path, value: dict) -> None:
    with path.open("x", encoding="utf-8") as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-prefix", required=True,
                        help="New absolute or current-directory prefix; never overwrites.")
    parser.add_argument("--previous-checkpoint", type=Path,
                        help="Optional earlier checkpoint for signed and whole-unit change accounting.")
    args = parser.parse_args()
    prefix = Path(args.output_prefix).resolve()
    outputs = {k: Path(str(prefix) + "_" + k + ".json")
               for k in ("contracts", "checkpoint", "manifest")}
    if any(p.exists() for p in outputs.values()):
        raise FileExistsError("All three output paths must be new.")
    if not prefix.parent.is_dir():
        raise FileNotFoundError(prefix.parent)

    text = MANUSCRIPT.read_text()
    matches = list(re.finditer(
        r"^\*\*(?:Lemma|Theorem|Proposition|Corollary) (U\.[A-Za-z0-9.]+) \(",
        text, re.M))
    ids = [m.group(1) for m in matches]
    if len(ids) != len(set(ids)) or set(ids) != set(DEPS):
        raise ValueError("The theorem inventory must match exactly, without duplicates.")
    for name, deps in DEPS.items():
        if not set(deps) <= set(ids):
            raise ValueError("Unknown dependency: " + name)
    visiting, visited = set(), set()
    def visit(name: str) -> None:
        if name in visiting:
            raise ValueError("Dependency cycle: " + name)
        if name in visited:
            return
        visiting.add(name)
        for dep in DEPS[name]:
            visit(dep)
        visiting.remove(name)
        visited.add(name)
    for name in ids:
        visit(name)

    units = []
    contracts = []
    cursor = 0
    for index, match in enumerate(matches):
        start, name = match.start(), match.group(1)
        if start > cursor:
            content = text[cursor:start]
            units.append({"id": "context:" + name,
                          "start_codepoint": cursor,
                          "end_codepoint_exclusive": start, **measure(content)})
        proof_start = text.index("*Proof.*", start)
        next_start = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        if proof_start >= next_start:
            raise ValueError("Missing full proof: " + name)
        proof_end = text.index(r"\(\square\)", proof_start) + len(r"\(\square\)")
        if proof_end > next_start:
            raise ValueError("Unclosed proof: " + name)
        statement = text[start:proof_start]
        proof = text[proof_start:proof_end]
        statement_unit = {"id": "statement:" + name, "start_codepoint": start,
                          "end_codepoint_exclusive": proof_start, **measure(statement)}
        proof_unit = {"id": "proof:" + name, "start_codepoint": proof_start,
                      "end_codepoint_exclusive": proof_end, **measure(proof)}
        units.extend([statement_unit, proof_unit])
        origin_kind, origin = ORIGIN[name]
        contracts.append({
            "id": name, "statement_exact_markdown": statement,
            "statement_binding": statement_unit, "complete_proof_binding": proof_unit,
            "dependencies": DEPS[name], "retained_inputs": RETAINED.get(name, []),
            "provenance_kind": origin_kind, "proof_bank_origin": origin,
            "historical_novelty_claim": False, "open_conjecture_claim": False,
            "intended_application_A_consumers": CONSUMERS.get(name, []),
            "consumer_status": "proposed_bindings; complete A review pending",
            "formal_coverage": FORMAL.get(name, {
                "status": "no_complete_exact_formal_bridge_established",
                "gap": "Written proof; no whole-theorem certificate asserted."})
        })
        cursor = proof_end
    if cursor < len(text):
        units.append({"id": "context:tail", "start_codepoint": cursor,
                      "end_codepoint_exclusive": len(text), **measure(text[cursor:])})
    if "".join(text[u["start_codepoint"]:u["end_codepoint_exclusive"]]
               for u in units) != text:
        raise ValueError("Units do not partition the complete manuscript.")
    if sum(u["utf8_bytes"] for u in units) != len(text.encode()):
        raise ValueError("UTF-8 units do not sum to the whole manuscript.")
    all_inputs = [bound(BASE / p) for p in INPUTS]
    data = {
        "schema": "phase123_exact_theorem_contracts_v1",
        "status": "PRIVATE_AUTHOR_DRAFT_PENDING_COMPLETE_INDEPENDENT_REVIEW",
        "manuscript": bound(MANUSCRIPT),
        "shared_notation_and_retained_input_context": "U Section 1; all context units charged",
        "theorem_count": len(contracts), "contracts": contracts,
        "input_bindings": all_inputs,
        "provenance_ledger": bound(PROVENANCE),
        "formal_sources_inspected": True, "fresh_lean_compilation_in_this_phase": False,
        "complete_formalization_claim": False,
    }
    write_new(outputs["contracts"], data)

    current = measure(text)
    # Whole-unit charging is intentionally explicit. A changed unit counts in
    # full on both sides; these are not lexical diff or semantic-novelty costs.
    previous = None
    prev_units = {}
    if args.previous_checkpoint:
        previous = json.loads(args.previous_checkpoint.read_text())
        prev_units = {u["id"]: u for u in previous["partition_units"]}
    cur_units = {u["id"]: u for u in units}
    unchanged = sorted(name for name in cur_units.keys() & prev_units.keys()
                       if cur_units[name]["sha256_utf8"] == prev_units[name]["sha256_utf8"])
    added = [u for name, u in cur_units.items() if name not in unchanged]
    removed = [u for name, u in prev_units.items() if name not in unchanged]
    gross_added = sum(u["plain_NFC_whitespace_tokens"] for u in added)
    gross_removed = sum(u["plain_NFC_whitespace_tokens"] for u in removed)
    prev_total = previous["whole_text"]["plain_NFC_whitespace_tokens"] if previous else 0
    checkpoint = {
        "schema": "phase123_U_draft_checkpoint_v1",
        "status": "AUTHOR_DRAFT_ACQUISITION_NOT_A_COMPRESSION_MEASUREMENT",
        "manuscript": bound(MANUSCRIPT), "whole_text": current,
        "partition_units": units, "theorem_count": len(contracts),
        "previous_checkpoint": (bound(args.previous_checkpoint)
                                if args.previous_checkpoint and args.previous_checkpoint.parent == BASE
                                else str(args.previous_checkpoint) if args.previous_checkpoint else None),
        "cost_convention": "NFC whitespace tokens; changed disjoint statement/proof/context units charged in full",
        "signed_whole_text_token_growth": current["plain_NFC_whitespace_tokens"] - prev_total,
        "gross_added_or_replaced_unit_tokens": gross_added,
        "gross_removed_or_replaced_unit_tokens": gross_removed,
        "unchanged_unit_ids": unchanged,
        "gross_costs_are_not_lexical_diff": True,
        "first_checkpoint_is_acquisition": previous is None,
        "consumer_bindings": {name: CONSUMERS.get(name, []) for name in ids},
        "consumer_validation": "application author bindings; independent complete review pending",
        "original_paper_baseline": "not measured in this checkpoint",
        "compression_ratio": None, "rendered_page_ratio": None,
        "new_conjecture_solutions": 0,
        "methodology_attribution": "GKM; phase123 provenance note and phase121 exact method-input bindings",
    }
    write_new(outputs["checkpoint"], checkpoint)
    manifest = {
        "schema": "phase123_umbrella_author_package_v1",
        "status": "FROZEN_AUTHOR_CHECKPOINT_PENDING_COMPLETE_REVIEW",
        "exports": [bound(MANUSCRIPT), bound(PROVENANCE), bound(Path(__file__).resolve()),
                    bound(outputs["contracts"]), bound(outputs["checkpoint"])],
        "source_assets_exported": False, "public_tree_modified": False,
        "author_checks": ["exact inventory", "complete proof-end bindings",
                          "disjoint whole-text partition", "acyclic declared dependencies"],
        "mathematical_review_note": "phase122 early mutable sections 1-3 feedback only; full root review pending",
        "does_not_claim": ["new source admission", "measured compression ratio",
                           "full Lean verification", "historical priority",
                           "resolved open conjecture"],
    }
    write_new(outputs["manifest"], manifest)
    print(json.dumps({"outputs": [str(p) for p in outputs.values()],
                      "theorems": len(contracts), **current,
                      "manifest_sha256": sha(outputs["manifest"].read_bytes())}, indent=2))


if __name__ == "__main__":
    main()
