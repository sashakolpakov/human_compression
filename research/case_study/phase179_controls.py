#!/usr/bin/env python3
"""Three mathematical negative controls for the source incidence bridge."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import time


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--gap", default="gap")
    args = ap.parse_args()
    out = args.output_dir.absolute()
    require(not out.exists() and not out.is_symlink(), "Fresh output directory required")
    out.mkdir(parents=True)
    source = Path(__file__).with_name("phase179_livingstone_check.g")
    original = source.read_text()
    mutations = [
        ("omit_induced_quadruple", "return Set([wimage,oimage])=Set([y[2],Difference(y[3],x[3])]);",
         "return true;", "printed Q rule versus repaired rule"),
        ("swap_P_facet_colour", "else return y in x[1]; fi;", "else return y in x[2]; fi;",
         "base pair incident"),
        ("change_Q_vertex_block_overlap", "return y[1] in p and Length(Intersection(y[3],p))=3;",
         "return y[1] in p and Length(Intersection(y[3],p))=2;", "base pair incident"),
    ]

    def check(mutation):
        name, old, new, rejection = mutation
        require(original.count(old) == 1, "Mutation anchor is not unique: " + name)
        script = out / (name + ".g")
        script.write_text(original.replace(old, new))
        start = time.monotonic()
        result = subprocess.run([args.gap, "-q", "-T", str(script)],
                                text=True, capture_output=True, timeout=1200)
        text = result.stdout + result.stderr
        (out / (name + ".log")).write_text(text)
        require("L068_P_AND_REPAIRED_Q_BRIDGE_PASS" not in text and rejection in text,
                "Mathematical mutation was not rejected as expected: " + name)
        return {"name": name, "rejected": True, "reason": rejection,
                "seconds": time.monotonic() - start, "exit_code": result.returncode,
                "log_sha256": hashlib.sha256(text.encode()).hexdigest()}

    with ThreadPoolExecutor(max_workers=3) as pool:
        records = list(pool.map(check, mutations))
    report = {"status": "PASS", "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "mathematical_controls": records,
              "scope": "Author-designed negative controls; not independent reimplementation."}
    (out / "controls.json").write_text(json.dumps(report, indent=2) + "\n")
    print("L068_MATHEMATICAL_CONTROLS_PASS")


if __name__ == "__main__":
    main()
