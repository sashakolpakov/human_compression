#!/usr/bin/env python3
"""Run the two complete J1 certificates for Module C in a fresh directory.

No predecessor manuscript or source geometry list is read. GAP/TomLib and their
complete subgroup data remain trusted inputs. This is an explicit, potentially
several-minute replay, not a prerequisite for each editorial revision.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time

ROOT = Path(__file__).resolve().parent
PROGRAMS = {
    "phase40_compress_operations_check.g":
        "f1d49b61e210e0026468a2bcb2621399e5fda10778893fd1c20d364019f54810",
    "phase40_compress_operations_exhaustive.g":
        "bfe4190665e751a3c65d00fd692ae0a6059d25f6345fd11f0efdc5a5a938c952",
}
CLASS_SHA = "787cd6d5563dc475bb2cadc0f57759eadf180fc3a19c3deede21738b4822f4b1"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--gap", default=shutil.which("gap"))
    args = parser.parse_args()
    require(not os.path.lexists(args.output_dir), "Refusing existing output path")
    for name, digest in PROGRAMS.items():
        require(sha(args.inputs / name) == digest, "Changed required program: " + name)
    require(bool(args.gap), "GAP is required for an explicit census replay")
    query = (
        'LoadPackage("tomlib");;Print(GAPInfo.Version,"\\n",'
        'PackageInfo("tomlib")[1].Version,"\\n",'
        'Filename(DirectoriesPackageLibrary("tomlib","data"),'
        '"tmjank.tom.gz"),"\\n");QUIT;'
    )
    process = subprocess.run([args.gap, "-q", "-T", "-c", query],
                             capture_output=True, text=True, timeout=30, check=True)
    versions = process.stdout.strip().splitlines()
    require(len(versions) == 3 and not process.stderr, "Unexpected GAP version query")
    software = {"GAP": versions[0], "TomLib": versions[1],
                "J1_data_name": "tomlib/data/tmjank.tom.gz",
                "J1_data_sha256": sha(Path(versions[2]))}
    args.output_dir.mkdir(parents=True)
    logs = []
    runs = []
    with tempfile.TemporaryDirectory(prefix="module-C-J1-") as temporary:
        scratch = Path(temporary)
        for name in PROGRAMS:
            shutil.copyfile(args.inputs / name, scratch / name)
        for name, marker in zip(PROGRAMS, ["COMPRESS_C_J1_PASS", "COMPRESS_C_EXHAUSTIVE_PASS"]):
            log_path = args.output_dir / Path(name).with_suffix(".log").name
            started = time.monotonic()
            with log_path.open("x") as stream:
                process = subprocess.run([args.gap, "-q", "-T", name], cwd=scratch,
                                         stdout=stream, stderr=subprocess.STDOUT, timeout=900)
            elapsed = time.monotonic() - started
            log = log_path.read_text()
            require(process.returncode == 0 and "Error," not in log, "Certificate failed: " + name)
            require(log.rstrip().endswith(marker), "Certificate did not finish: " + name)
            require(sha(scratch / name) == PROGRAMS[name], "Certificate program changed")
            logs.append(log)
            runs.append({"program": name, "sha256": PROGRAMS[name], "seconds": elapsed,
                         "log": log_path.name, "log_sha256": sha(log_path)})
        class_name = "phase40_compress_operations_exhaustive_classes.json"
        require(sha(scratch / class_name) == CLASS_SHA, "Different exact class certificate")
        classes = json.loads((scratch / class_name).read_text())
        require(len(classes[0]) == 6 and classes[1] == [] and len(classes[2]) == 6,
                "Incorrect census shape")
        require(len({tuple(row) for row in classes[2]}) == 6, "Classes lack distinct invariants")
        shutil.copyfile(scratch / class_name, args.output_dir / class_name)
    positive = re.findall(r"^GEOMETRY (\d) .* IP_MEETS 256 HELLY_ROWS 16 PASS$", logs[0], re.M)
    negative = re.findall(r"^NEGATIVE (\d) IP_FAILURES 8 PANELS .* PASS$", logs[0], re.M)
    require(positive == list("123456") and negative == list("12"), "Incomplete construction checks")
    local = [[int(v) for v in row] for row in re.findall(
        r"^LOCAL (\d) MAXIMAL (\d+) ORDER (\d+) ORBITS (\d+) REGULAR (\d+)$", logs[1], re.M)]
    require(len(local) == 14, "Incomplete maximal-subgroup coverage")
    for k, count, regular in [(3, 245, 95), (4, 1476, 15)]:
        require(sum(row[3] for row in local if row[0] == k) == count, "Wrong local orbit total")
        require(sum(row[4] for row in local if row[0] == k) == regular, "Wrong local regular total")
    stages = [[int(v) for v in row] for row in re.findall(
        r"^STAGE_TOTAL (\d) TESTED (\d+) ACCEPTED (\d+)$", logs[1], re.M)]
    require(stages == [[4, 100016, 40], [5, 21352, 0]], "Wrong exhaustive extension totals")
    for name, digest in PROGRAMS.items():
        require(sha(args.inputs / name) == digest, "Input program changed during execution")
    result = {
        "status": "PASS", "runner_sha256": sha(Path(__file__)), "programs": PROGRAMS,
        "software": software, "runs": runs, "class_sha256": CLASS_SHA,
        "construction": {"geometries": 6, "marked_meets": 1536, "typed_Helly_rows": 96,
                         "negative_controls": 2, "presentation_index": 1463, "group_order": 175560},
        "census": {"local_rows": local, "stages": stages, "rank4_classes": 6,
                   "rank5_classes_in_all_subgroups": 0},
        "classification_scope": "Thin regular residually connected geometries; not non-Helly C-group markings",
        "source_geometry_list_read": False,
        "retained_inputs": ["Complete TomLib J1 subgroup catalogue and model", "Exact GAP group/coset algorithms"],
        "uniform_operation_proofs_checked_by_this_run": False,
    }
    with (args.output_dir / "phase150_module_C_j1_replay.json").open("x") as stream:
        json.dump(result, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print("MODULE_C_J1_COMPLETE_REPLAY_PASS")


if __name__ == "__main__":
    main()
