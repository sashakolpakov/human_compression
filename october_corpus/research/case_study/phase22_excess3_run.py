#!/usr/bin/env python3
"""Run the third-excess transition calculation from frozen original checkpoints."""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output-prefix", type=Path, required=True)
    parser.add_argument("--gap", default=os.environ.get("GAP") or shutil.which("gap"))
    args = parser.parse_args()
    if not args.gap:
        parser.error("GAP is required on PATH or via --gap/GAP")
    inputs = args.inputs.resolve()
    prefix = args.output_prefix.resolve()
    prefix.parent.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).with_name("phase22_excess3_transfer.g").resolve()
    report_path = inputs / "phase21_rank5_census.json"
    report = json.loads(report_path.read_text())
    if (report["status"], report["rank"], report["ordered_markings"]) != ("PASS", 5, 584):
        raise ValueError("Expected complete frozen rank-five census")
    kernels = []
    bindings = [{"path": report_path.name, "sha256": sha(report_path)}]
    for level in report["ladder"][:2]:
        path = inputs / level["path"]
        if sha(path) != level["sha256"]:
            raise ValueError(f"Checkpoint hash mismatch: {path.name}")
        raw = gzip.decompress(path.read_bytes())
        if hashlib.sha256(raw).hexdigest() != level["uncompressed_sha256"]:
            raise ValueError("Uncompressed checkpoint hash mismatch")
        rows = json.loads(raw)
        if len(rows) != level["distinct_kernels"]:
            raise ValueError("Checkpoint count mismatch")
        kernels.append(rows)
        bindings.append({"path": path.name, "sha256": sha(path)})
    witness_path = inputs / report["accepted_witnesses"]["path"]
    if sha(witness_path) != report["accepted_witnesses"]["sha256"]:
        raise ValueError("Accepted witness hash mismatch")
    rows = json.loads(witness_path.read_text())
    if len(rows) != 584:
        raise ValueError("Accepted witness count mismatch")
    kernels.append([row[0] for row in rows])
    bindings.append({"path": witness_path.name, "sha256": sha(witness_path)})
    if any(type(n) is not int or n < 0 for layer in kernels for row in layer for n in row):
        raise ValueError("Kernel data must contain nonnegative integers only")
    run = {
        "status": "RUNNING", "source": {"path": source.name, "sha256": sha(source)},
        "runner": {"path": Path(__file__).name, "sha256": sha(Path(__file__))},
        "retained_inputs": bindings,
    }
    run_path = Path(str(prefix) + ".run.json")
    run_path.write_text(json.dumps(run, indent=2) + "\n")
    with tempfile.TemporaryDirectory(prefix="phase22_excess3_") as temp:
        data = Path(temp) / "kernels.g"
        data.write_text("data22:=" + json.dumps(kernels, separators=(",", ":")) + ";;\n")
        code = ("DATA_FILE22:=" + json.dumps(str(data)) + ";;OUTPUT_PREFIX22:="
                + json.dumps(str(prefix)) + ";;Read(" + json.dumps(str(source)) + ");")
        with Path(str(prefix) + ".log").open("wb") as log:
            completed = subprocess.run([args.gap, "-q", "-T", "-c", code], stdout=log,
                                       stderr=subprocess.STDOUT, check=False)
    log_path = Path(str(prefix) + ".log")
    text = log_path.read_text()
    passed = completed.returncode == 0 and "PASS exact budget-three" in text and "Error" not in text
    run["status"] = "PASS" if passed else "FAIL"
    run["returncode"] = completed.returncode
    run["outputs"] = []
    for suffix in (".log", ".graph.json", ".windows.json", ".gluings.json"):
        path = Path(str(prefix) + suffix)
        if path.exists():
            run["outputs"].append({"path": path.name, "sha256": sha(path)})
    run_path.write_text(json.dumps(run, indent=2) + "\n")
    print(json.dumps({"status": run["status"], "report": str(run_path)}))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
