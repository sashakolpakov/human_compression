#!/usr/bin/env python3
"""Replay the bounded source-correction evidence; no full N006 admission."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time


def require(condition, message):
    if not condition:
        raise ValueError(message)


def binding(path):
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def bound(root, name, row):
    p = Path(name)
    require(not p.is_absolute() and p.parts and all(x not in (".", "..") for x in p.parts),
            "unsafe relative path")
    target = root / p
    require(not target.is_symlink() and target.resolve().is_relative_to(root.resolve()), "unsafe bound target")
    require(binding(target) == {k: row[k] for k in ("bytes", "sha256")}, "binding mismatch: " + name)


def command(argv, cwd, output):
    p = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, timeout=180)
    output.write_text(p.stdout + p.stderr)
    require(p.returncode == 0, "command failed: " + str(argv[0]))
    return p.stdout + p.stderr


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--study-root", type=Path)
    parser.add_argument("--render", action="store_true")
    parser.add_argument("--xelatex", default="xelatex")
    parser.add_argument("--gap")
    args = parser.parse_args()
    start = time.monotonic()
    root = Path(__file__).resolve().parent
    require(not args.out.exists() and not args.out.is_symlink(), "output must be fresh")
    out = args.out.resolve()
    out.mkdir(parents=True)
    manifest = root / "manifest.json"
    exports = None
    if manifest.exists():
        rows = json.loads(manifest.read_text())["exports"]
        for name, row in rows.items():
            bound(root, name, row)
        exports = len(rows)
    source = json.loads((root / "source_reading.json").read_text())
    primary = None
    if args.study_root:
        for key in ("pdf", "text"):
            row = source["primary"][key]
            bound(args.study_root, row["path"], row)
        from pypdf import PdfReader
        require(len(PdfReader(args.study_root / source["primary"]["pdf"]["path"]).pages) == 22,
                "primary extent")
        primary = source["primary"]["pdf"]["sha256"]
    model = out / "finite_models.py"
    shutil.copyfile(root / "finite_models.py", model)
    command([sys.executable, "-B", "-O", str(model), "--out", str(out / "models.json")],
            out, out / "models.stdout")
    computed = json.loads((out / "models.json").read_text())
    require(computed == json.loads((root / "model_report.json").read_text()), "finite evidence changed")
    src = model.read_text()
    changes = [
        ("literal_complement_factor", "P = frozenset(it.product(range(8), cyclic))", "P = BI"),
        ("identity_in_place_of_reversal", "rev = tuple(reversed(range(n)))", "rev = tuple(range(n))"),
        ("erase_ambient_generation_obstruction", "group = tuple(range(8))", "group = tuple(range(4))"),
        ("identify_all_automorphisms_as_inner", "inner = frozenset(it.product((1, 7), (0, 2, 4, 6)))",
         "inner = frozenset(autos)"),
        ("wrong_coordinate_parabolic", "parabolics = [supports[((1 << n) - 1) ^ (1 << i)] for i in range(n)]",
         "parabolics = [supports[(1 << n) - 1] for i in range(n)]"),
    ]
    controls = []
    for name, old, new in changes:
        require(src.count(old) == 1, "control anchor: " + name)
        test = out / (name + ".py")
        test.write_text(src.replace(old, new))
        p = subprocess.run([sys.executable, "-B", "-O", str(test)], cwd=out,
                           capture_output=True, text=True, timeout=180)
        (out / (name + ".log")).write_text(p.stdout + p.stderr)
        require(p.returncode != 0 and "ValueError:" in p.stderr, "control not rejected: " + name)
        controls.append({"name": name, "rejected": True,
                         "scope": "Model/interface corruption; not a substitute for the written proof."})
    render = None
    if args.render:
        target = out / "render"
        target.mkdir()
        shutil.copyfile(root / "coset_twisting_corrections.tex", target / "paper.tex")
        for i in (1, 2):
            command([args.xelatex, "-interaction=nonstopmode", "-halt-on-error", "paper.tex"],
                    target, target / ("pass%d.stdout" % i))
        log = (target / "paper.log").read_text()
        diagnostics = [line for line in log.splitlines() if any(s in line for s in
                      ("Overfull", "Underfull", "Missing character", "LaTeX Warning", "Package hyperref Warning"))]
        require(not diagnostics, "render diagnostics")
        from pypdf import PdfReader
        old = [p.extract_text() or "" for p in PdfReader(root / "coset_twisting_corrections.pdf").pages]
        new = [p.extract_text() or "" for p in PdfReader(target / "paper.pdf").pages]
        require(new == old and len(new) == 5, "rendered page text changed")
        require(not {c for t in new for c in t if (ord(c) < 32 and c not in "\n\r\t") or
                     ord(c) == 65533 or 0xe000 <= ord(c) <= 0xf8ff}, "unresolved extracted glyph")
        render = {"pages": 5, "per_page_text_equal": True, "diagnostics": [],
                  "text_sha256": [hashlib.sha256(t.encode()).hexdigest() for t in new]}
    gap = None
    if args.gap:
        shutil.copyfile(root / "observed_root_obstructions.g", out / "observed_root_obstructions.g")
        stdout = command([args.gap, "-q", "-x", "10000", str(out / "observed_root_obstructions.g")], out, out / "root_gap.stdout")
        tokens = ["N006_LITERAL_WREATH_THINNESS_COUNTEREXAMPLE order48 cosets2and8 panels8and2 PASS",
                  "N006_LITERAL_DUALITY_EMBEDDING_COUNTEREXAMPLE order16 AutA168 PASS",
                  "N006_BOOLEAN_RANK4_ALGEBRA order32 exponent4 PASS"]
        require(all(s in stdout for s in tokens) and "Error" not in stdout, "observed root GAP checks")
        gap = {"sentinels": tokens, "scope": "Replay of the exact observed root proposal, separate from independent models."}
    report = {"status": "PASS", "exports_verified": exports, "source_rows": len(source["rows"]),
              "primary_sha256": primary, "models": computed, "controls": controls, "render": render,
              "observed_root_gap": gap, "elapsed_seconds": round(time.monotonic() - start, 6),
              "whole_N006_admission": False, "new_source_credit": 0,
              "new_question_credit": 0, "new_formal_credit": 0}
    (out / "report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: report[k] for k in ("status", "exports_verified", "source_rows", "elapsed_seconds")}))


if __name__ == "__main__":
    main()
