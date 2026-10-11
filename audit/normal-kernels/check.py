#!/usr/bin/env python3
"""Compile both normal-kernel modules from source in a fresh directory."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def binding(path):
    data = path.read_bytes()
    return {"path": path.name, "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest()}


def containment_countermodel():
    """Containment is enough for detection, but not for a product onto ker(pi)."""
    group = {0, 1}
    mul = lambda x, y: x ^ y
    pi = rho = lambda x: x
    local = group
    need(all(mul(mul(x, y), z) == mul(x, mul(y, z))
             for x in group for y in group for z in group), "C2 associativity")
    need(all(mul(0, x) == x == mul(x, 0) and mul(x, x) == 0 for x in group),
         "C2 identity and inverses")
    need(all(pi(mul(x, y)) == mul(pi(x), pi(y)) and
             rho(mul(x, y)) == mul(rho(x), rho(y)) for x in group for y in group),
         "Actual homomorphisms")
    need(all(mul(mul(x, y), x) in local for x in group for y in local), "Normality")
    need(all(rho(x) != 0 or x == 0 for x in local), "Local faithfulness")
    kernel = {x for x in group if pi(x) == 0}
    need(kernel < local and len(kernel) != len(local), "Strict containment obstruction")
    return {"group": "C2", "base_map": "identity", "coordinate": "identity",
            "local_factors": "One factor, the entire group; off-diagonal hypotheses are vacuous.",
            "base_kernel_order": len(kernel), "product_order": len(local),
            "kernel_contained_in_join": True, "kernel_equals_join": False,
            "product_isomorphic_to_kernel": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--source-dir", type=Path, default=ROOT)
    parser.add_argument("--lean", type=Path, default=Path(
        "/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean"))
    parser.add_argument("--packages", type=Path, default=Path(
        "/Users/sasha/bogachev/formal/.lake/packages"))
    args = parser.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(), "Use a fresh output directory.")
    out = args.out.resolve()
    out.mkdir(parents=True)
    scope = json.loads((ROOT / "scope.json").read_text())
    pins = json.loads((ROOT / "dependency_manifest.json").read_text())
    dependencies = []
    for row in pins["packages"]:
        path = args.packages / row["name"]
        rev = subprocess.check_output(["git", "-C", path, "rev-parse", "HEAD"], text=True).strip()
        need(rev == row["rev"], "Wrong package revision: " + row["name"])
        need(subprocess.run(["git", "-C", path, "diff", "--quiet", "HEAD", "--"]).returncode == 0,
             "Changed tracked package sources: " + row["name"])
        dependencies.append({"name": row["name"], "rev": rev})
    version = subprocess.check_output([args.lean, "--version"], text=True).strip()
    need("version 4.32.2," in version, "Wrong Lean version.")
    env = dict(os.environ)
    env["LEAN_PATH"] = os.pathsep.join([str(out)] + [
        str(p / ".lake/build/lib/lean") for p in args.packages.iterdir()
        if (p / ".lake/build/lib/lean").is_dir()])
    modules = []
    for row in scope["modules"]:
        source = args.source_dir / row["source"]["path"]
        need(binding(source) == row["source"], "Changed proof source: " + source.name)
        text = source.read_text()
        need(not re.search(r"\b(sorry|admit|native_decide)\b|^\s*axiom\s", text, re.M),
             "Unapproved proof mechanism: " + source.name)
        copied = out / source.name
        copied.write_bytes(source.read_bytes())
        start = time.monotonic()
        proc = subprocess.run([args.lean, "-o", copied.with_suffix(".olean"), copied],
                              cwd=out, env=env, capture_output=True, text=True, timeout=180)
        for suffix, value in [("stdout", proc.stdout), ("stderr", proc.stderr)]:
            (out / (source.stem + "." + suffix)).write_text(value)
        need(proc.returncode == 0 and not re.search(
            r"warning(?:\([^)]*\))?:|error(?:\([^)]*\))?:|sorryAx", proc.stdout + proc.stderr),
            "Compilation failed: " + source.name)
        axioms = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", proc.stdout)
        need([name for name, _ in axioms] == row["declarations"], "Wrong declaration inventory.")
        reports = [{"name": name, "axioms": re.findall(r"[\w.]+", value)}
                   for name, value in axioms]
        need(all(set(r["axioms"]) <= {"propext", "Classical.choice", "Quot.sound"}
                 for r in reports), "Unapproved axiom dependency.")
        modules.append({"source": binding(source), "exit_code": proc.returncode,
                        "seconds": round(time.monotonic() - start, 3), "declarations": reports,
                        "stdout": binding(out / (source.stem + ".stdout")),
                        "stderr": binding(out / (source.stem + ".stderr"))})
    report = {"status": "PASS", "lean_version": version, "dependencies": dependencies,
              "modules": modules, "scope": scope["formal_scope"],
              "containment_countermodel": containment_countermodel(),
              "not_formalized": scope["not_formalized"],
              "dependency_trust": "Both local modules compiled from source. Existing compiled objects of pinned dependencies were used; mathlib was not rebuilt.",
              "source_credits": 0, "question_credits": 0, "compression_ratio": None}
    (out / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "modules": len(modules),
                      "declarations": sum(len(m["declarations"]) for m in modules),
                      "report": str(out / "report.json")}))


if __name__ == "__main__":
    main()
