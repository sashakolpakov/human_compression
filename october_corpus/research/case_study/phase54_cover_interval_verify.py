#!/usr/bin/env python3
"""Replay the reviewed finite cover interval using stock GAP and a new directory.

The complete program is the exact hash-bound assembly reviewed in phase50.
Primary source captures and the older private manifest tree are not required.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time

SCRIPT_SHA = "f1858df347d64f2ed773de4c496915888205aac584caf46f22361ba54c87f4d9"
LOG_SHA = "84a79b2e22c59632fcaee542712efce1fcdf29a77ff366c5571032f708bc139d"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gap", default="gap")
    parser.add_argument("--input-root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    source = (args.input_root / "phase54_cover_interval_check.g").resolve()
    if sha(source.read_bytes()) != SCRIPT_SHA:
        raise RuntimeError("Certificate differs from the reviewed complete program")
    executable = shutil.which(args.gap)
    if executable is None:
        raise RuntimeError("GAP executable unavailable")
    output = args.output_dir.absolute()
    output.mkdir()  # Existing directories are rejected before any execution.
    command = [executable, "-q", str(source)]
    started = time.monotonic()
    run = subprocess.run(command, cwd=output, capture_output=True, timeout=300)
    elapsed = time.monotonic() - started
    (output / "stdout.log").write_bytes(run.stdout)
    (output / "stderr.log").write_bytes(run.stderr)
    # Match the original text-mode replay while preserving the raw output too.
    canonical = run.stdout.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    (output / "canonical_stdout.log").write_text(canonical)
    passed = (run.returncode == 0 and not run.stderr
              and sha(canonical.encode()) == LOG_SHA
              and sha(source.read_bytes()) == SCRIPT_SHA)
    report = {
        "date": "2026-10-10", "status": "PASS" if passed else "FAIL",
        "command": command, "exit_code": run.returncode,
        "elapsed_seconds": elapsed, "script_sha256": SCRIPT_SHA,
        "runner_sha256": sha(Path(__file__).read_bytes()),
        "stdout_sha256": sha(run.stdout), "stderr_sha256": sha(run.stderr),
        "canonical_stdout_sha256": sha(canonical.encode()),
        "canonicalization": "UTF-8 decode; CRLF and bare CR replaced by LF, matching original universal-newline text mode; no other changes.",
        "expected_version_in_exact_log": "GAP 4.15.1",
        "scope": "Exact source reconstruction, all six kernel subspaces, four invariant quotients, three admissible and two maximal kernels; scoped tetrahedral example. Stock GAP is trusted.",
        "not_claimed": ["general cover conjecture", "all infinite families", "all minimal covers outside this interval", "written-theorem formalization", "new source compression"],
    }
    (output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
