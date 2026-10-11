#!/usr/bin/env python3
"""Check the exact bounded review, diagnostics and corruption sensitivity."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time


def need(ok, msg):
    if not ok:
        raise ValueError(msg)


def digest(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def verify(path, b):
    need(digest(path) == {k: b[k] for k in ("bytes", "sha256")}, "hash mismatch: " + str(path))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--study-root", type=Path)
    p.add_argument("--author", type=Path)
    a = p.parse_args()
    start = time.monotonic()
    root = Path(__file__).resolve().parent
    need(not a.out.exists() and not a.out.is_symlink(), "fresh output required")
    out = a.out.resolve()
    out.mkdir(parents=True)
    count = None
    if (root / "manifest.json").exists():
        rows = json.loads((root / "manifest.json").read_text())["exports"]
        for name, b in rows.items():
            target = root / name
            need(not target.is_symlink() and target.resolve().is_relative_to(root), "unsafe export")
            verify(target, b)
        count = len(rows)
    bindings = json.loads((root / "bindings.json").read_text())
    for name, b in bindings.items():
        if "snapshot" in b:
            verify(root / b["snapshot"], b)
            if a.author:
                verify(a.author / name, b)
        elif a.study_root:
            verify(a.study_root / b["private_path"], b)
    run = subprocess.run([sys.executable, "-B", "-O", str(root / "module_models.py"),
                          "--out", str(out / "models.json")], capture_output=True, text=True, timeout=180)
    need(run.returncode == 0, run.stderr)
    report = json.loads((out / "models.json").read_text())
    need(report == json.loads((root / "model_report.json").read_text()), "model result changed")
    src = (root / "module_models.py").read_text()
    mutations = [
        ("omit_sign_cocycle", "return (lam if sign(p) else 0) ^ a ^ act(a, p)", "return a ^ act(a, p)"),
        ("omit_coboundary", "return (lam if sign(p) else 0) ^ a ^ act(a, p)", "return lam if sign(p) else 0"),
        ("wrong_graph16_first_column", 'if family == "16" and j == 0:', 'if family == "16" and j != 0:'),
        ("omit_initial_coordinate", "k = 1", "k = 0"),
        ("allow_zero_seed", "z = red(1)", "z = 0"),
    ]
    controls = []
    for name, old, new in mutations:
        need(src.count(old) == 1, "mutation anchor")
        f = out / (name + ".py")
        f.write_text(src.replace(old, new))
        proc = subprocess.run([sys.executable, "-B", "-O", str(f)], capture_output=True, text=True, timeout=180)
        (out / (name + ".log")).write_text(proc.stdout + proc.stderr)
        need(proc.returncode != 0 and "ValueError:" in proc.stderr, "mutation accepted: " + name)
        controls.append({"name": name, "rejected": True})
    total_models = sum(len(x["nonzero_quotient_models"]) for x in report["module_quotients"])
    total_pairs = sum(x["IP_pairs"] for r in report["module_quotients"] for x in r["nonzero_quotient_models"])
    record = {"status": "PASS", "exports_verified": count, "nonzero_quotient_modules": total_models,
              "full_IP_pairs": total_pairs, "shear_ranks": list(range(2, 13)), "literal_diagram_models": 33,
              "cocycle_permutation_pairs": sum(x["permutation_pairs"] or 0 for x in report["shears"]),
              "controls": controls, "source_bindings_checked": a.study_root is not None,
              "current_author_bytes_checked": a.author is not None,
              "general_twisting_scope": "Complete written argument reviewed; no claim of machine proof of the general geometry theorem.",
              "new_source_credit": 0, "new_question_credit": 0, "new_formal_credit": 0,
              "elapsed_seconds": round(time.monotonic() - start, 6)}
    (out / "report.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(json.dumps(record))


if __name__ == "__main__":
    main()
