#!/usr/bin/env python3
"""Bind the literal Lean tables/words to the reviewed source certificate."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import re


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", type=Path, required=True)
    ap.add_argument("--lean", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        raise SystemExit("Refusing to overwrite evidence")
    data = json.loads(args.data.read_text())
    source = args.lean.read_text()

    def vector(name):
        match = re.search(r"^def " + name + r"[^\n]* := (!\[.*?\])\n\n", source, re.M | re.S)
        assert match, name
        value = match.group(1).replace("!", "")
        if name == "relations":
            value = re.sub(r"\b([xyzXY])\b", r"'\1'", value)
        return ast.literal_eval(value)

    forward = [[j - 1 for j in row] for row in data["permutations"]]
    backward = []
    for p in forward:
        b = [0] * len(p)
        for i, j in enumerate(p):
            b[j] = i
        backward.append(b)
    assert vector("forward") == forward
    assert vector("backward") == backward
    assert vector("voltage") == data["weights"]
    expected = [list("x" * 6), list("y" * 3), list("zz"),
                list("zx" * 3), list("zy" * 6), list("Xy" * 2),
                list("YXX" * 3), list("zxxx" * 2),
                list("Xz" + "Yz" * 2 + "zx" + "zy" * 2),
                list(("y" + "zy" * 2) * 6)]
    assert vector("relations") == expected
    assert re.search(r"^def witness[^\n]* := \[x,y,x,z,x,y,x,z\]$", source, re.M)
    report = {"status": "PASS", "checker_sha256": digest(Path(__file__)),
              "data_sha256": digest(args.data), "lean_sha256": digest(args.lean),
              "tables": 3, "entries_per_table": 648, "source_relator_words": 10,
              "witness": "(x*y*x*z)^2",
              "scope": "Exact literal transcription check. The Lean kernel separately proves the defining relations and infinitude."}
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print("FORMAL_DATA_ALIGNMENT_PASS")


if __name__ == "__main__":
    main()
