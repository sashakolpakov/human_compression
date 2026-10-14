"""Replay the twelve saved certificates with explicitly bound named inputs."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time

if not __debug__:
    raise SystemExit("Run without Python optimization.")

BASE = Path(__file__).resolve().parent


def need(test, message):
    if not test:
        raise ValueError(message)


def check_pin(path, item):
    data = path.read_bytes()
    need(len(data) == item["bytes"], "Wrong length: " + str(path))
    need(hashlib.sha256(data).hexdigest() == item["sha256"],
         "Wrong digest: " + str(path))


def replay(out, public, gap, control):
    out.mkdir()
    driver = ("PacketDirectory:=" + json.dumps(str(BASE)) + ";;\n" +
              "WitnessDirectory:=" + json.dumps(str(public / "papers/topic-diagonal/v2/papers/sporadic/witnesses")) + ";;\n" +
              "Control:=" + json.dumps(control) + ";;\n" +
              "Read(" + json.dumps(str(BASE / "verify.g")) + ");;\n")
    (out / "driver.g").write_text(driver)
    start = time.monotonic()
    with (out / "stdout").open("wb") as so, (out / "stderr").open("wb") as se:
        result = subprocess.run([str(gap), "-q", "-b", str(out / "driver.g")],
                                stdout=so, stderr=se, timeout=180)
    stdout = (out / "stdout").read_text()
    stderr = (out / "stderr").read_text()
    if control == "none":
        need(result.returncode == 0 and not stderr, "Failed mathematical replay")
        lines = [line.strip() for line in stdout.splitlines() if line.strip()]
        need(lines[-1:] == ["TERMINAL_PASS 12 sporadic chirality certificates"],
             "Missing complete terminal receipt")
        expected = json.loads((BASE / "expected.json").read_text())
        need(lines[:-1] == expected["lines"], "Twelve-case receipt differs")
    else:
        reasons = {"identity": "M23: nonidentity involution",
                   "wrong_ambient": "M23: named group order",
                   "wrong_order": "M23: named group order",
                   "equal_word_orders": "M23: exact word orders"}
        need(result.returncode == 1 and not stderr and
             stdout.strip() == "REJECT " + reasons[control],
             "Control was not rejected at the intended mathematical condition")
    receipt = {"status": "PASS" if control == "none" else "EXPECTED_REJECTION",
               "returncode": result.returncode, "control": control,
               "elapsed_seconds": time.monotonic() - start}
    (out / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    return receipt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--public-root", type=Path, required=True)
    ap.add_argument("--gap", type=Path, default=Path(shutil.which("gap") or "/missing/gap"))
    ap.add_argument("--gap-root", type=Path)
    args = ap.parse_args()
    need(args.out.is_absolute() and not args.out.exists() and not args.out.is_symlink(),
         "Use a fresh absolute output path")
    public = args.public_root.resolve()
    gap = args.gap.resolve()
    gaproot = (args.gap_root or gap.parent.parent).resolve()
    manifest = json.loads((BASE / "manifest.json").read_text())
    for item in manifest["exports"]:
        check_pin(BASE / item["path"], item)
    deps = json.loads((BASE / "dependencies.json").read_text())
    for item in deps["files"]:
        root = public if item["namespace"] == "public" else gaproot
        check_pin(root / item["path"], item)
    args.out.mkdir()
    receipts = [replay(args.out / "positive", public, gap, "none")]
    for control in ["identity", "wrong_ambient", "wrong_order", "equal_word_orders"]:
        receipts.append(replay(args.out / control, public, gap, control))
    report = {"status": "PASS", "cases": 12, "negative_controls": 4,
              "bound_exports": len(manifest["exports"]), "bound_dependencies": len(deps["files"]),
              "receipts": receipts, "whole_original_credit": 0,
              "new_conjecture_credit": 0, "new_lean_credit": 0,
              "new_measurement_credit": 0}
    (args.out / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
