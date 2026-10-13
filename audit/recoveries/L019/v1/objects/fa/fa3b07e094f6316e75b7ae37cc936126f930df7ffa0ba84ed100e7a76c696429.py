import hashlib
import json
from pathlib import Path
import shutil
import sys

if sys.flags.optimize:
    raise SystemExit("optimized Python is unsupported")

def need(p, message):
    if not p:
        raise ValueError(message)

def pin(path, role=None):
    item = {"path": str(path), "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    if role:
        item["role"] = role
    return item

w = Path(__file__).resolve().parent; s = w.parents[2]
packets = [
 ("topic_B_L047_candidate_v2", "complete transitive half-degree theorem; actual pre-cocycle base marks and complete finite exception list"),
 ("topic_B_L047_independent_review", "distinct review of complete L047 recovery"),
 ("topic_B_L047_root_adoption", "root adoption of complete L047 recovery"),
 ("corpus106_L044_principal_v1", "complete natural alternating rank theorem, with exact small exceptions"),
 ("corpus106_L044_principal_independent_review", "distinct complete principal review"),
 ("corpus106_L044_principal_root_adoption", "root complete principal adoption"),
 ("corpus106_L071_alternating_v1", "complete A11 rank-six census and exhaustive marked enumeration proof"),
 ("corpus106_L071_alternating_independent_review", "distinct review of alternating census"),
 ("corpus106_L071_alternating_root_adoption", "root adoption of alternating census"),
 ("topic_B_L019_central_intersections_v1", "central extension difference map and odd-index obstruction"),
 ("topic_B_L019_central_intersections_root_review", "distinct acceptance of central intersection theorem"),
]
deps = {}; acquired = []
for name, interface in packets:
    root = s / name; path = root / "manifest.json"; p = pin(path, interface)
    deps[str(path)] = p; acquired.append({**p, "interface": interface})
    manifest = json.loads(path.read_text())
    for e in manifest["exports"]:
        f = root / e["path"]; q = pin(f, "complete export of " + name)
        need(q["sha256"] == e["sha256"] and q["bytes"] == e["bytes"], "export mismatch: " + str(f))
        deps[str(f)] = q
for p, role in [
 (s / "sources/stability2024.pdf", "exact L019 primary source"),
 (w.parent / "SnJanuary2023.tex", "exact L019 primary TeX"),
 (s / "reboot_20261013/L071_A11_full_IP01/records.g", "literal complete A11 record; exact extraction input"),
]:
    deps[str(p)] = pin(p, role)
(w / "dependencies.json").write_text(json.dumps(list(deps.values()), indent=2) + "\n")
(w / "acquired_packets.json").write_text(json.dumps(acquired, indent=2) + "\n")
scope = {"original": "L019", "status": "BOUNDED_COMPONENT_ONLY",
 "proved": ["Every nonsymmetric actual wing of the stated perfect split has rank at most half its degree.",
 "At rank 2r>n+2 at least one actual wing is full symmetric."],
 "finite_additions": "Thirty empty small-exception anchor sets; all four A11 representatives in both orientations; four trivial anchored suffix centralizers and four index-six obstructions.",
 "not_claimed": ["Existence of a perfect split", "Stability extension/contraction bijection", "Complete L019 principal recovery", "New census or open-conjecture solution"],
 "whole_original_credit": 0, "new_question_credit": 0, "new_Lean": 0, "measurement": None}
(w / "scope.json").write_text(json.dumps(scope, indent=2) + "\n")
attribution = {"author": "/root/l044_resume",
 "new_argument": "Actual endpoint anchors plus the complete rank exceptions and central-intersection obstruction.",
 "inherited": "Historical L047/L044 classifications and L071 complete census, with all acquired proof and finite premises; the reviewed central-intersection lemma.",
 "parent_contribution": "Requested explicit audit of every rank-bound exception, endpoint-anchor hypothesis, and actual-action rather than quotient-IP interface; no new mathematical argument supplied for this packet.",
 "distinct_review": "pending"}
(w / "attribution.json").write_text(json.dumps(attribution, indent=2) + "\n")
(w / "visual_review.json").write_text(json.dumps({"pages": 3, "all_pages_directly_viewed": True,
 "result": "Readable; no clipping, unresolved references or mathematical notation defect in final three pages.",
 "images": [pin(w / ("native-%02d.png" % i)) for i in range(1,4)]}, indent=2) + "\n")
(w / "development_record.json").write_text(json.dumps({"retained_first_failure": "first_build.log",
 "description": "Initial split environment used multiple alignment pairs and failed. Replaced it by aligned; two final builds passed. The mathematical content was unchanged.",
 "old_extraction_scope": "extract_a11.g obtains all four literal tuples and tests their first orientations. The complete both-orientation independent replay is gap_wings.g; direct_report.json tests the same complete scope."}, indent=2) + "\n")
(w / "README.rst").write_text("Symmetric wings at a perfect split\n=================================\n\nA bounded L019 proof component. Read actual_wings.pdf and scope.json.\nThe exact acquired classification and review roots are in acquired_packets.json;\ntheir complete exports and the literal census record are hashed in dependencies.json.\nNo whole-original credit.\n\nRun check_wings.py --output fresh_report.json for the independent literal checks.\nRun gap -q -b gap_wings.g for the distinct group-library check.\nThe original extraction requires the pinned private census record; runtime checks\nuse only wing_inputs.json or the literal permutations embedded in gap_wings.g.\n")
excluded = {"actual_wings.aux", "actual_wings.out", "actual_wings.log"}
dest = s / "topic_B_L019_actual_wings_v1"
need(not dest.exists(), "immutable destination already exists")
dest.mkdir()
for f in sorted(w.iterdir()):
    if f.is_file() and f.name not in excluded and not f.name.startswith("native-"):
        shutil.copy2(f, dest / f.name)
exports = []
for f in sorted(dest.iterdir()):
    q = pin(f); q["path"] = f.name; exports.append(q)
(dest / "manifest.json").write_text(json.dumps({"status": "AUTHOR_FROZEN_BOUNDED_L019_ACTUAL_WINGS",
 "exports": exports, "whole_original_credit": 0, "new_question_credit": 0}, indent=2) + "\n")
print(json.dumps({"manifest": pin(dest / "manifest.json"), "exports": len(exports), "dependencies": len(deps)}))
