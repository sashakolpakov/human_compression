"""Collect hashes and bounded verification results for the phase-three notes."""
from pathlib import Path
import hashlib
import json
import re


root = Path(__file__).resolve().parent
proof = root / "phase3_psl4.md"
symbolic = json.loads((root / "phase3_psl4_symbolic.json").read_text())
assert symbolic["status"] == "passed"
assert symbolic["proof_sha256"] == hashlib.sha256(proof.read_bytes()).hexdigest()
log = (root / "phase3_psl4_reducible_probe.log").read_text()
required = [
    "FIELD 25 projective_degree 16276 torder 3",
    "INVOLUTION_ORDERS [ 2, 2, 2, 2, 2 ]",
    "PSL_MEMBERSHIP_DETERMINANT_TEST [ true, true, true, true, true ]",
    "ADJACENT_PRODUCTS [ 4, 6, 6, 3 ]",
    "DISTANT_COMMUTATIONS [ true, true, true, true, true, true ]",
    "LEFT_TRIPLE_IP true", "MIDDLE_TRIPLE_IP true", "RIGHT_TRIPLE_IP true",
    "LEFT_RANK4_IP_INTERSECTION 36 EXPECTED 12",
    "RIGHT_RANK4_IP_INTERSECTION 12 EXPECTED 12",
    "EXPLICIT_FORM_MULTIPLIERS [ Z(5)^2, Z(5)^0, Z(5)^0, Z(5)^0, Z(5)^0 ]",
    "PSL4_EXPECTED_ORDER 232442642250000000000",
]
assert all(item in log for item in required)
assert "Error," not in log
assert re.search(r"SUBGROUP \[ 1, 2, 3, 4, 5 \] ORDER 28800 ", log)

names = [
    "phase3_psl4.md", "phase3_psl4_symbolic.py", "phase3_psl4_symbolic.json",
    "phase3_psl4_reducible_probe.g", "phase3_psl4_reducible_probe.log",
    "phase3_psl4_build_certificate.py", "psl4_theory.md",
]
report = {
    "date": "2026-10-09",
    "status": "bounded_checks_passed",
    "mathematical_scope": [
        "Uniform rank-five common-form obstruction when the joint endpoint module is completely reducible, with arbitrary cross-commutator signs.",
        "Uniform all-rank common-form obstruction if every generator is a projective reflection.",
        "Uniform rank bound seven for connected string C-groups in odd-characteristic PGL4; rank eight is excluded using the intersection property.",
    ],
    "independent_review": "Root agent independently audited sections 1, 3, 4, 5, 6 and the rank-eight proof in section 7. This is internal review, not external peer review.",
    "machine_checks": {
        "symbolic_scalar_identities": sum(symbolic["checks"].values()),
        "symbolic_domain": "Exact polynomial identities over Z with explicitly supplied constraint combinations; no division.",
        "finite_probe": {
            "field_order": 25, "projective_degree": 16276,
            "group_order": 28800, "adjacent_product_orders": [4, 6, 6, 3],
            "consecutive_rank3_IP": [True, True, True],
            "left_rank4_IP": False, "intersection_order": 36,
            "required_intersection_order": 12,
            "common_form": "diag(2X,X), X=[[0,1],[1,0]]",
            "multipliers": [-1, 1, 1, 1, 1],
        },
    },
    "limitations": [
        "The conjectured maximum rank four for PSL(4,q) is not proved.",
        "Nonsemisimple rank-five endpoint modules and possible ranks six and seven remain unresolved.",
        "Symbolic checks cover matrix identities; the representation-theoretic classification and rank-eight exclusion are paper proofs, not Lean certificates.",
        "No publication-priority claim is made.",
    ],
    "artifacts": [
        {"path": name, "sha256": hashlib.sha256((root/name).read_bytes()).hexdigest(),
         "bytes": (root/name).stat().st_size} for name in names
    ],
}
(root / "phase3_psl4_certificate.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"status": report["status"], "artifacts": len(names),
                  "symbolic_identities": report["machine_checks"]["symbolic_scalar_identities"]}))
