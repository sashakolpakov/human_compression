#!/usr/bin/env python3
"""Replay the Livingstone source audit, retained C certificate, and Lean component."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

PINS = {
    "phase179_livingstone_check.g": "2fd04abbd8610404fefa5dec7ff486489256d387e536ec2f73e368ebe2d76031",
    "phase40_compress_operations_check.g": "f1d49b61e210e0026468a2bcb2621399e5fda10778893fd1c20d364019f54810",
    "phase179_formal/EquivariantIncidence.lean": "386b25ace5827c91c3ae9518612b313a0d50d01399811f7042ff34b2001cf962",
    "formal/dependency_manifest.json": "4c716f4ff0ea4940311014c9853c0b8e5aaab8250f8cefdf9f8003845cfb02e3"
}
DECLARATIONS = {"reconstruction", "localOrbit_subset", "reconstruction_of_card"}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--inputs", type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument("--output-dir", type=Path, required=True)
    ap.add_argument("--packages", type=Path, required=True)
    ap.add_argument("--gap", default="gap")
    ap.add_argument("--lean", default="lean")
    a = ap.parse_args()
    out = a.output_dir.absolute()
    require(not out.exists() and not out.is_symlink(), "Fresh output directory required")
    require(len(PINS) == 4, "Unfrozen program pins")
    source = a.inputs.resolve()
    for name, digest in PINS.items():
        require(sha(source / name) == digest, "Changed pinned input: " + name)
    gap, lean = shutil.which(a.gap), shutil.which(a.lean)
    require(gap is not None and lean is not None, "GAP and Lean executables required")
    dependencies = json.loads((source / "formal/dependency_manifest.json").read_text())
    packages = a.packages.resolve()
    checked = []
    for item in dependencies["packages"]:
        p = packages / item["name"]
        revision = subprocess.check_output(["git", "-C", str(p), "rev-parse", "HEAD"], text=True).strip()
        require(revision == item["rev"], "Wrong dependency revision: " + item["name"])
        require(subprocess.run(["git", "-C", str(p), "diff", "--quiet", "HEAD", "--"]).returncode == 0,
                "Changed dependency source: " + item["name"])
        checked.append({"name": item["name"], "revision": revision})
    out.mkdir(parents=True, exist_ok=False)
    stage = out / "source"
    stage.mkdir()
    for name in PINS:
        target = stage / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / name, target)
    env = dict(os.environ)
    env.pop("PYTHONOPTIMIZE", None)
    env["ELAN_TOOLCHAIN"] = dependencies["lean"]
    overlay = out / "dependencies"
    overlay.mkdir()
    libs = []
    for item in dependencies["packages"]:
        library = packages / item["name"] / ".lake/build/lib/lean"
        if library.is_dir():
            alias = overlay / item["name"]
            alias.symlink_to(library, target_is_directory=True)
            libs.append(alias)
    env["LEAN_PATH"] = os.pathsep.join(map(str, libs))
    version = subprocess.check_output([lean, "--version"], env=env, text=True).strip()
    require(re.search(r"\bversion 4\.32\.2(?:,|\s|\))", version), "Wrong Lean compiler")
    query = ('LoadPackage("tomlib");;Print(GAPInfo.Version,"\\n",'
             'PackageInfo("tomlib")[1].Version,"\\n",'
             'Filename(DirectoriesPackageLibrary("tomlib","data"),"tmjank.tom.gz"),"\\n");QUIT;')
    q = subprocess.run([gap, "-q", "-T", "-c", query], env=env,
                       capture_output=True, text=True, timeout=30)
    lines = q.stdout.strip().splitlines()
    require(q.returncode == 0 and not q.stderr.strip() and len(lines) == 3, "Invalid GAP environment query")
    software = {"GAP": lines[0], "TomLib": lines[1], "J1_data_sha256": sha(Path(lines[2])),
                "Lean": version, "Lean_dependencies": checked}
    runs = []

    def run(label, command, marker):
        start = time.monotonic()
        r = subprocess.run(command, cwd=stage, env=env, capture_output=True, text=True, timeout=1200)
        body = r.stdout + r.stderr
        log = out / (label + ".log")
        log.write_text(body)
        require(r.returncode == 0 and marker in body and not re.search(r"Error,|error:|warning:", body),
                "Failed or incomplete " + label + ": " + body[-2500:])
        runs.append({"label": label, "seconds": round(time.monotonic() - start, 6),
                     "exit_code": r.returncode, "log": log.name, "log_sha256": sha(log)})
        print(label + " PASS", flush=True)
        return body

    run("retained_C", [gap, "-q", "-T", str(stage / "phase40_compress_operations_check.g")],
        "COMPRESS_C_J1_PASS")
    graph = run("livingstone", [gap, "-q", "-T", str(stage / "phase179_livingstone_check.g")],
                "L068_P_AND_REPAIRED_Q_BRIDGE_PASS")
    rows = re.findall(r"INCIDENCE mode (\d+) types \[ (\d+), (\d+) \] neighbours (\d+) stabilizer (\d+) PASS", graph)
    require(len(rows) == 12, "Missing source incidence relation")
    require("SOURCE_Q23_EXTRA_FLAG_TYPE1_EXTENSIONS 0" in graph and
            "SOURCE_Q23_WITNESS_MEMBERSHIP [ true, true, true ]" in graph and
            "literal neighbours 12 repaired 2 stabilizer_orbits [ 2, 10 ]" in graph,
            "Missing literal source counterexample")
    obj = out / "EquivariantIncidence.olean"
    leanlog = run("lean", [lean, "-o", str(obj), str(stage / "phase179_formal/EquivariantIncidence.lean")],
                  "HumanCompression.EquivariantIncidence.reconstruction_of_card")
    matches = re.findall(r"'HumanCompression\.EquivariantIncidence\.([^']+)' depends on axioms: \[([^]]*)\]", leanlog)
    require(len(matches) == 3 and {n for n, _ in matches} == DECLARATIONS, "Incomplete Lean declarations")
    axioms = {}
    for name, values in matches:
        used = {x.strip() for x in values.split(",") if x.strip()}
        require(used <= {"propext", "Classical.choice", "Quot.sound"}, "Unexpected Lean axiom")
        axioms[name] = sorted(used)
    require(obj.is_file() and not obj.is_symlink(), "Missing fresh Lean object")
    for name, digest in PINS.items():
        require(sha(source / name) == sha(stage / name) == digest, "Input changed during replay")
    report = {"status": "PASS", "author_replay": True, "independent_mathematical_review": False,
              "source_inputs": PINS, "driver_sha256": sha(Path(__file__)), "software": software,
              "runs": runs, "incidence_rows": [[int(v) for v in row] for row in rows],
              "Lean_axioms": axioms, "Lean_object_sha256": sha(obj),
              "literal_second_construction": "PASS", "literal_first_construction": "REFUTED_AS_PRINTED",
              "corrected_first_construction": "PASS", "unchanged_whole_source_credit": 0,
              "full_J1_theorem_Lean_verified": False, "new_open_conjecture_solved": False,
              "trust_boundary": "Written proofs, named J1 data and exact GAP algorithms are retained. Only the generic incidence reconstruction is freshly Lean-compiled; cached dependency objects are read through a private symlink overlay and remain trusted."}
    (out / "replay.json").write_text(json.dumps(report, indent=2) + "\n")
    print("L068_SOURCE_AUDIT_REPLAY_PASS", flush=True)


if __name__ == "__main__":
    main()
