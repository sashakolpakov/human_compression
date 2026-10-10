#!/usr/bin/env python3
"""Independent native-field/cross-ratio replay and exact author-certificate comparison."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def require(ok, msg):
    if not ok:
        raise RuntimeError(msg)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--gap", default="gap")
    a = ap.parse_args()
    out = a.output_dir.absolute()
    require(not out.exists() and not out.is_symlink(), "Fresh review output required")
    out.mkdir(parents=True)
    root = Path(__file__).resolve().parent
    inputs = [root / "phase183_inversive_review.g", root / "phase182_inversive_geometry_check.py",
              root / "phase182_inversive_residues.md"]
    before = {p.name: sha(p) for p in inputs}
    start = time.monotonic()
    g = subprocess.run([a.gap, "-q", "-T", str(inputs[0])], capture_output=True, text=True, timeout=600)
    text = g.stdout + g.stderr
    (out / "native_gap.log").write_text(text)
    require(g.returncode == 0 and "L092_LITERAL_Q3_E2_INDEPENDENT_PASS" in text
            and not re.search(r"Error,|warning:|error:", text), "Independent GAP check failed")
    gap_seconds = time.monotonic() - start
    rows = {}
    for match in re.finditer(r"^([A-Z0-9_]+) (\[)", text, re.MULTILINE):
        rows[match.group(1)] = json.JSONDecoder().raw_decode(text[match.start(2):])[0]
    inv = {v: i for i, v in enumerate(rows["ROOT_TO_NATIVE_POINT_MAP"])}

    def points(s):
        return sorted(inv[v] for v in s)

    mapped = []
    for i, (t, v) in enumerate(zip(rows["NATIVE_TYPES"], rows["NATIVE_OBJECTS"])):
        if t in [1, 4]:
            obj, key = inv[v[0]], (t, inv[v[0]])
        elif t == 3:
            obj = points(v)
            key = (t, obj)
        else:
            b, pair = map(points, v)
            obj = [pair, sorted(set(b) - set(pair))]
            key = (t, b, pair)
        mapped.append((key, i, [t - 1, obj]))
    mapped.sort(key=lambda z: z[0])
    renumber = {old + 1: new for new, (_, old, _) in enumerate(mapped)}
    encoding = {"blocks": sorted(points(b) for b in rows["BLOCKS"]),
                "objects": [obj for _, _, obj in mapped],
                "neighbours": [sorted(renumber[v] for v in rows["NATIVE_NEIGHBOURS"][old])
                               for _, old, _ in mapped]}
    native_hash = hashlib.sha256(json.dumps(encoding, sort_keys=True).encode()).hexdigest()
    (out / "native_certificate.json").write_text(json.dumps(encoding, sort_keys=True) + "\n")
    start = time.monotonic()
    py = subprocess.run([sys.executable, "-B", "-O", str(inputs[1]), "--output", str(out / "author.json")],
                        capture_output=True, text=True, timeout=600)
    (out / "author.log").write_text(py.stdout + py.stderr)
    require(py.returncode == 0, "Author diagnostic failed on fresh execution")
    author = json.loads((out / "author.json").read_text())
    require(native_hash == author["certificate_sha256"], "Independent full incidence certificates disagree")
    require(rows["FLAG_COUNTS"] == author["all_flag_counts"], "Independent flag counts disagree")
    author_seconds = time.monotonic() - start
    controls = []
    original = inputs[0].read_text()
    for name, old, new in [
        ("allow_point_copy_diagonal", "return x<>y;", "return true;"),
        ("admit_marked_object_own_block", "return Intersection(x[1],y)=x[2];", "return IsSubset(y,x[2]);"),
    ]:
        require(original.count(old) == 1, "Nonunique mutation anchor")
        p = out / (name + ".g")
        p.write_text(original.replace(old, new))
        r = subprocess.run([a.gap, "-q", "-T", str(p)], capture_output=True, text=True, timeout=600)
        body = r.stdout + r.stderr
        (out / (name + ".log")).write_text(body)
        require("every typed flag extends" in body and "L092_LITERAL_Q3_E2_INDEPENDENT_PASS" not in body,
                "Changed literal incidence was not rejected: " + name)
        controls.append({"name": name, "rejected": True, "reason": "nonextendable typed flag",
                         "log_sha256": sha(out / (name + ".log"))})
    for p in inputs:
        require(sha(p) == before[p.name], "Reviewed input changed during execution")
    report = {"status": "PASS", "independently_authored_group_and_geometry_checker": True,
              "source_hashes": before, "native_algorithm": "GAP GF(9), harmonic determinant cross-ratios, typed Cartesian flag enumeration, union-of-components residue test",
              "exact_full_incidence_certificate_agrees_after_field_isomorphism": True,
              "certificate_sha256": native_hash, "all_flags": rows["FLAG_COUNTS"],
              "typed_flags": rows["TYPED_FLAG_COUNTS"], "residues": rows["RESIDUE_TABLE"],
              "panel_degrees": rows["PANEL_DEGREES"], "rank_two_IP2_checks": 1650,
              "full_design_automorphism_order": 1440, "full_geometry_automorphism_order": 1440,
              "full_group_order_scope": "Complete7! normalized design automorphism search, combined with sharp3-transitivity of PGL; geometry/design group equality uses the reviewed written reconstruction.",
              "chambers": 2160, "flag_transitive": False,
              "literal_Lemma5_refuted": True, "Theorem11_refuted": False,
              "uniform_residue_proof_reviewed": True, "uniform_theorem_Lean_verified": False,
              "new_whole_source_principal_credit": 0, "new_open_conjecture_solution": False,
              "runs": {"native_gap_seconds": gap_seconds, "author_python_seconds": author_seconds},
              "negative_controls": controls}
    (out / "review.json").write_text(json.dumps(report, indent=2) + "\n")
    print("PHASE183_INDEPENDENT_REVIEW_PASS", native_hash)


if __name__ == "__main__":
    main()
