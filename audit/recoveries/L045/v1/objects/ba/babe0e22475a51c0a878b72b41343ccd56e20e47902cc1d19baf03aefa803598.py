"""Check the component's bound files and reproduce its finite algebra controls."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

if not __debug__:
    raise SystemExit("Run without Python optimization.")

BASE = Path(__file__).resolve().parent


def need(condition, message):
    if not condition:
        raise ValueError(message)


def run():
    manifest = json.loads((BASE / "manifest.json").read_text())
    for item in manifest["exports"]:
        p = BASE / item["path"]
        data = p.read_bytes()
        need(len(data) == item["bytes"], "Wrong length: " + item["path"])
        need(hashlib.sha256(data).hexdigest() == item["sha256"],
             "Wrong digest: " + item["path"])
    result = subprocess.run([sys.executable, str(BASE / "finite.py")],
                            capture_output=True, text=True, timeout=30, check=True)
    need(not result.stderr, "Unexpected finite-check diagnostics")
    report = json.loads(result.stdout)
    need(report == json.loads((BASE / "finite_report.json").read_text()),
         "Finite replay differs")
    lines = (BASE / "generation.stdout").read_text().splitlines()
    import math
    need(lines == [f"PASS {n} {math.factorial(n)//2}" for n in range(8, 31)] +
         ["TERMINAL_PASS 23 finite generation checks"], "GAP receipt differs")
    need(not (BASE / "generation.stderr").read_bytes(), "GAP diagnostics present")
    need(json.loads((BASE / "scope.json").read_text())["whole_original_credit"] == 0,
         "This component does not complete L045")
    return {"status": "PASS", "bound_exports": len(manifest["exports"]),
            "finite_algebra_cases": report["cases"], "retained_gap_cases": 23,
            "all_degree_proof": "alternating.tex", "whole_original_credit": 0,
            "new_conjecture_credit": 0, "new_lean_credit": 0,
            "new_measurement_credit": 0}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
