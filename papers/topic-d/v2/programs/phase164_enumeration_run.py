#!/usr/bin/env python3
"""Replay Module D certificates in a fresh directory, without source-tree writes.

The numerical M22 census is separate from the unresolved refined source table.
The full manuscript, classical group structure, catalogue completeness, and GAP
algorithms remain mathematical inputs; this driver does not certify them in Lean.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
PROGRAMS = {
    "phase110_commuting_pairs_integration_finite.g": "ec555ee0fc8c912bf23f325d87c1bc6167a7c31615ca6f98d85dfa3748f21368",
    "phase110_commuting_pairs_integration_formula.py": "002dc6c43ca6ea3ad30260c1b420e47912c61c00820b95cc31a3ea68dc45acc3",
    "phase110_commuting_pairs_integration_run.py": "2ad8478bda08c967d67f722cc304aa7c64fd97737feffa80ea4a84b45398a2be",
    "phase10_suzuki_marked_fields_check.py": "ae80feb2973aad327cc6f1327b2197cc54bcd81f40a198f4699a09c8df494f0b",
    "phase10_suzuki_marked_groups_check.g": "aa15b586b4d5df8ea17a74ca959615d0f6b12968b1f0c65da57aec799ca3438f",
    "phase5_j2_search.g": "e31ddbc7fb1fbe163dc20270375e7729e0ba9748a20b4cd2bb4047e19d5ddefb",
    "phase5_j2_fuse.g": "84773be26991c96d412be812b9dc40b9ad8ed9b10b6d4a31d8e10a99b24223d6",
    "phase5_j2_verify.g": "24b1f83a3fed6dfed6c086cc838cb0e6e76db7bd8c19e9d66593a711cd8c70b7",
    "phase4_geometry_checks.g": "b2159e974cf72e22eae1857772319c35c9d9b04f5f8abc60262df069fee7ca09",
    "phase164_m22_census.g": "292cf1c036f64e9fb2dde37358fac4105afcd830fe911755bb5993db4a35c7d6",
    "phase164_m22_validate.g": "51c602b84e43977309410bed3c8d73366f700df2d9f367b1719cb18b317ddf29",
    "phase164_m22_shadows.g": "f93f79389dfe8b1346ec9a5e5c178a98e5c759653d0bed0633bd2ccccd76e868",
    "phase164_m22_run.py": "959f8ee1eaa46a4a17555136909d8c4c1165f5a160525bd05590d3e0820ccf06",
}
PARTS = {
    "small": list(PROGRAMS)[:5],
    "j2": list(PROGRAMS)[5:9],
    "m22": list(PROGRAMS)[9:],
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--inputs", type=Path, default=ROOT)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--part", choices=["small", "j2", "m22", "all"], required=True)
    ap.add_argument("--gap", default=shutil.which("gap"))
    a = ap.parse_args()
    out = a.output_dir.resolve()
    require(not os.path.lexists(a.output_dir), "Refusing existing output path")
    require(bool(a.gap), "GAP is required")
    selected = list(PARTS) if a.part == "all" else [a.part]
    names = list(dict.fromkeys(n for part in selected for n in PARTS[part]))
    for name in names:
        require(sha(a.inputs / name) == PROGRAMS[name], "Changed program: " + name)
    out.mkdir(parents=True)
    stage = out / "work" / "research" / "leemans"
    stage.mkdir(parents=True)
    for name in names:
        shutil.copyfile(a.inputs / name, stage / name)
    env = dict(os.environ)
    env.pop("PYTHONOPTIMIZE", None)
    env["PATH"] = str(Path(a.gap).resolve().parent) + os.pathsep + env.get("PATH", "")
    records = []

    def run(label, argv, cwd, footer):
        start = time.monotonic()
        log = out / (label + ".log")
        with log.open("x") as stream:
            result = subprocess.run(argv, cwd=cwd, env=env, stdout=stream,
                                    stderr=subprocess.STDOUT, timeout=1200)
        body = log.read_text()
        require(result.returncode == 0 and footer in body and "Error," not in body,
                "Incomplete or failed computation: " + label)
        records.append(dict(label=label, seconds=round(time.monotonic()-start, 6),
                            exit_code=result.returncode, log=log.name,
                            log_sha256=sha(log), completion_marker=footer))
        print(label + " PASS", flush=True)
        return body

    query = ('LoadPackage("tomlib");;Print(GAPInfo.Version,"\\n",'
             'PackageInfo("tomlib")[1].Version,"\\n",'
             'Filename(DirectoriesPackageLibrary("tomlib","data"),'
             '"tmjank.tom.gz"),"\\n",'
             'Filename(DirectoriesPackageLibrary("tomlib","data"),'
             '"tmmath.tom.gz"),"\\n");QUIT;')
    version = subprocess.run([a.gap, "-q", "-T", "-c", query], env=env,
                             capture_output=True, text=True, timeout=30)
    lines = version.stdout.strip().splitlines()
    require(version.returncode == 0 and not version.stderr and len(lines) == 4,
            "Unexpected GAP/TomLib version query")
    software = dict(GAP=lines[0], TomLib=lines[1],
                    J2_data_sha256=sha(Path(lines[2])),
                    M22_data_sha256=sha(Path(lines[3])))
    if "small" in selected:
        run("degree_six", [sys.executable, "-B", str(stage / PARTS["small"][2]),
                           "--output-dir", str(out / "degree_six")], out, '"status": "PASS"')
        run("suzuki_fields", [sys.executable, "-B", str(stage / PARTS["small"][3]),
                              "--output", str(out / "suzuki_fields.json")], out, '"status": "PASS"')
        text = run("suzuki_matrices", [a.gap, "-q", "-T", str(stage / PARTS["small"][4])],
                   out, '"subgroup_intersections":2688')
        matrix = json.loads(text.strip())
        require(matrix["normalized_triples"] == 42 and matrix["duality_matrix_checks"] == 42,
                "Incomplete Suzuki matrix diagnostic")
    if "j2" in selected:
        (stage / "phase5_j2_checkpoints").mkdir()
        logs = {}
        for name, label, footer in [
            ("phase5_j2_search.g", "j2_search", "SEARCH_COMPLETE"),
            ("phase5_j2_fuse.g", "j2_fusion", "FULL_CENSUS_PASS"),
            ("phase5_j2_verify.g", "j2_validation", "ALL_WITNESSES_PASS count=30")]:
            logs[label] = run(label, [a.gap, "-q", "-T", "research/leemans/" + name],
                              out / "work", footer)
        completed = [int(x) for x in re.findall(r"^BOREL_COMPLETE id=(\d+) ", logs["j2_search"], re.M)]
        require(completed == list(range(1, 147)), "Incomplete Borel traversal")
        done = sorted((stage / "phase5_j2_checkpoints").glob("b*_done.g"))
        require(len(done) == 146, "Missing terminal checkpoints")
        for checkpoint in done:
            levels = re.search(r"levels:=(\[[^\]]*\])", checkpoint.read_text())
            require(levels is not None, "Missing terminal-level field")
            counts = json.loads(levels.group(1))
            require(not counts or counts[-1] == 0, "Nonempty terminal level")
        fusion = re.findall(r"^FUSION rank=(\d+) inner_classes=(\d+) aut_type_classes=(\d+)",
                            logs["j2_fusion"], re.M)
        require([[int(x) for x in row] for row in fusion[:3]] == [[2, 8, 8], [3, 24, 19], [4, 5, 3]],
                "Wrong J2 census")
        require(all(int(row[2]) == 0 for row in fusion[3:]) and len(fusion) == 13,
                "Incomplete higher-rank output")
        require(len(re.findall(r"^WITNESS id=", logs["j2_validation"], re.M)) == 30,
                "Missing J2 witness checks")
    if "m22" in selected:
        run("m22", [sys.executable, "-B", str(stage / "phase164_m22_run.py"),
                    "--output-dir", str(out / "m22"), "--gap", a.gap], out,
            "M22 census and shadow replay PASS")
    for name in names:
        require(sha(a.inputs / name) == PROGRAMS[name] == sha(stage / name),
                "Program changed during execution: " + name)
    record = dict(status="PASS", author_replay=True, independently_authored_checker=False,
                  selected=selected, programs={name: PROGRAMS[name] for name in names},
                  runner_sha256=sha(Path(__file__)), software=software, runs=records,
                  source_geometry_inputs=False, full_M22_refined_table_contract_complete=False,
                  uniform_written_proofs_checked_by_execution=False, Lean_certificate=False,
                  retained_inputs=["Complete named group catalogues", "Exact GAP algorithms",
                                   "Written recognition and completeness proofs"])
    (out / "replay.json").write_text(json.dumps(record, indent=2) + "\n")
    print("MODULE_D_REPLAY_PASS", flush=True)


if __name__ == "__main__":
    main()
