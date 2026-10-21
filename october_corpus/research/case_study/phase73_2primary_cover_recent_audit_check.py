#!/usr/bin/env python3
"""Check exact review/replay bindings and every finite count; no census rerun."""
import argparse
import hashlib
import itertools
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PREFIX = "phase73_2primary_cover_recent_audit"
MANIFEST_SHA = "a05194d0f85dab4955fdd85069947d883531b780d0e910734efb23fdb2585078"


def binding(path):
    raw = path.read_bytes()
    return {"sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    if args.report.exists() or args.report.is_symlink():
        raise FileExistsError("Existing report refused")
    name = "phase58_2primary_cover_manifest.json"
    assert binding(ROOT / name)["sha256"] == MANIFEST_SHA
    manifest = json.loads((ROOT / name).read_text())
    bindings = {name: binding(ROOT / name)}
    for name, expected in manifest["files"].items():
        assert binding(ROOT / name) == expected, name
        bindings[name] = expected
    for name, expected in manifest["source_bindings"].items():
        assert binding(ROOT / name)["sha256"] == expected, name
        bindings[name] = binding(ROOT / name)
    replay_name, log_name = PREFIX + "_replay.json", PREFIX + "_replay.log"
    replay = json.loads((ROOT / replay_name).read_text())
    log = (ROOT / log_name).read_text()
    assert replay["status"] == "PASS" and replay["runner_sha256"] == bindings["phase58_2primary_cover_check.py"]["sha256"]
    assert binding(ROOT / log_name) == bindings["phase58_2primary_cover_check.log"]
    assert replay["log_sha256"] == binding(ROOT / log_name)["sha256"]
    assert not re.search(r"FAIL|Error,|Syntax error|SKIP_", log)
    for name, expected in replay["sources_pre_post_sha256"].items():
        assert binding(ROOT / name)["sha256"] == expected, name
        bindings[name] = binding(ROOT / name)
    first, second = log.split("FILE phase58_2primary_cover_extension_check.g\n")
    first = re.sub(r"\s+", " ", first.replace("\\\n", ""))
    second = re.sub(r"\s+", " ", second.replace("\\\n", ""))
    chunks = re.split(r"(?=PARAM \[)", first)[1:]
    parameters = list(itertools.product([5, 6], [-1, 1], [-1, 1]))
    assert len(chunks) == len(parameters) == 8
    expected_normal = [(1, "1", True), (2, "C2", True), (2, "C2", True),
                       (2, "C2", False), (4, "C2 x C2", True), (8, "C4 x C2", False)]
    uniform = []
    for chunk, parameter in zip(chunks, parameters):
        match = re.search(r"PARAM \[ (\d+), (-?\d+), (-?\d+) \] orders P,R,T,Qraw,Q0,Q0d,H \[ ([\d, ]+) \]", chunk)
        assert tuple(map(int, match.groups()[:3])) == parameter
        q = 2**parameter[0]
        orders = [int(x) for x in match.group(4).split(",")]
        assert orders == [64*q, 128*q, 32*q, 512*q, 256*q, 256*q, 256*q]
        rows = re.findall(r'ROW \[ (\d+), (\d+), "([^"]+)", (true|false), \[ (\d+), (\d+) \], (true|false), (true|false) \]', chunk)
        interpreted = [(int(size), int(k), typ, central == "true", [int(a), int(b)], ip == "true", mirror == "true")
                       for size, k, typ, central, a, b, ip, mirror in rows]
        expected = [(128*q, 1, "1", True, [1,1], False, True),
                    (512*q, 4, "C4", False, [1,2], True, True),
                    (512*q, 4, "C4", False, [2,1], True, True)]
        expected += [(256*q, 2, "C2", True, [1,1], True, True)]*3
        assert interpreted == expected
        raw = re.search(r'RAW_H \[ (\d+), "C4 x C2", true \]', chunk)
        assert raw and int(raw.group(1)) == 1024*q
        normal = [(int(size), typ, flag == "true") for size, typ, flag in re.findall(r'RAW_NORMAL \[ (\d+), "([^"]+)", (true|false) \]', chunk)]
        assert normal == expected_normal
        assert 'RAW_MAXIMAL_GOOD [ 4 ]' in chunk
        assert 'W [ 16, "C4 x C4", 4, 4 ] Z2=Bhalf true' in chunk
        uniform.append({"parameters": parameter, "orders": orders, "raw_shared_order": 1024*q,
                        "all_six_IP_kernel_rows_checked": True, "all_six_invariant_quotient_rows_checked": True})
    assert 'FULL [ 8192, 5 ] invol [ 2, 2, 2, 2 ]' in second
    assert 'SMALL_PRESENTATION [ 8, 380, 8192, 8192 ]' in second
    assert 'CENTRAL_COVER [ 131072, 16, true, 2, true ]' in second
    assert 'CENTRAL_IP false' in second
    assert 'DOUBLE_COVERS [ 15, 1 ]' in second
    assert 'ALL_CENTRAL_QUOTIENTS [ 67, 4 ] max good kernel sizes [ 8 ] all good [ 2, 4, 4, 8 ]' in second
    c4rows = re.findall(r'C4_QUOTIENTS \[ ([\d, -]+) \] \[ (\d+), (\d+), (\d+) \]', second)
    v4rows = re.findall(r'V4_QUOTIENTS \[ ([\d, ]+) \] \[ (\d+), (\d+), (\d+) \]', second)
    c4 = [(tuple(int(x) for x in bits.split(",")), int(n), int(g), int(m)) for bits, n, g, m in c4rows]
    v4 = [(tuple(int(x) for x in bits.split(",")), int(n), int(g), int(m)) for bits, n, g, m in v4rows]
    assert [r[0] for r in c4] == list(itertools.product([-1,1], repeat=4))
    assert [r[0] for r in v4] == [r for r in itertools.product([0,1], repeat=4) if any(r)]
    assert [r[1:] for r in c4] == [(0,0,0),(24,0,0),(0,0,0),(8,2,0),(0,0,0),(8,2,0),(0,0,0),(8,4,0),(24,0,0),(8,0,0),(8,2,0),(0,0,0),(8,2,0),(0,0,0),(8,4,0),(0,0,0)]
    assert [r[1:] for r in v4] == [(35,0,0),(43,2,0),(35,0,0),(43,2,0),(35,0,0),(43,0,0),(35,0,0),(35,0,0),(43,3,0),(35,0,0),(43,2,0),(35,0,0),(43,2,0),(35,0,0),(43,0,0)]
    assert sum(r[2] for r in c4) == 16 and sum(r[2] for r in v4) == 11
    assert all(r[3] == 0 for r in c4 + v4)
    gap = Path(shutil.which("gap"))
    version = subprocess.run([str(gap), "-q", "-c", 'Print(GAPInfo.Version,"\\n"); QUIT_GAP(0);'],
                             capture_output=True, text=True, timeout=10)
    assert version.returncode == 0 and version.stdout.strip() == "4.15.1" and not version.stderr
    existing = {n: binding(ROOT / n) for n in (replay_name, log_name)}
    refusal = subprocess.run(["/Users/sasha/.venvs/global/bin/python", str(ROOT / "phase58_2primary_cover_check.py"),
                              "--report", str(ROOT / replay_name), "--log", str(ROOT / log_name)],
                             capture_output=True, text=True, timeout=10)
    assert refusal.returncode != 0 and "fresh output paths required" in refusal.stderr
    assert all(binding(ROOT / n) == v for n, v in existing.items())
    assert all(binding(ROOT / n) == v for n, v in bindings.items())
    result = {
        "schema": "phase73_independent_exact_evidence_check_v1", "status": "PASS",
        "checker": binding(Path(__file__)), "bound_inputs": bindings,
        "fresh_replay": existing, "fresh_replay_seconds": replay["seconds"],
        "exact_original_log_match": True, "uniform_rows": uniform,
        "cyclic_character_rows": c4, "noncentral_V4_character_rows": v4,
        "finite_sample": {"beta": 5, "signs": [1,1], "full_R_order": 8192, "p_class": 5,
                          "double_covers": 1, "quartic_cyclic": 16, "quartic_central_V4": 2,
                          "quartic_noncentral_V4": 11, "quartic_total": 29, "quartic_new_minimal": 0},
        "GAP": {"path": str(gap), "realpath": str(gap.resolve()), **binding(gap.resolve()), "version": version.stdout.strip()},
        "fresh_no_clobber_check": {"returncode": refusal.returncode, "stderr": refusal.stderr,
                                   "two_existing_outputs_unchanged": True},
        "all_bound_inputs_unchanged": True,
        "mathematical_completeness_review_is_separate_written_record": True,
    }
    with args.report.open("x") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    print(json.dumps({"status": "PASS", "report": str(args.report), **binding(args.report)}, indent=2))


if __name__ == "__main__":
    main()
