#!/usr/bin/env python3
"""Replay the frozen L009 author packet and independent phase271 diagnostics."""
import argparse, hashlib, json, pathlib, re, subprocess, sys, time

ROOT = pathlib.Path(__file__).resolve().parent
AUTHOR_SHA = "18cd719df0625cbb3d7795bf64072e93bcfaf57e6aec3d1557355be897d1280c"

def need(value, message):
    if not value:
        raise RuntimeError("PHASE271_REJECT " + message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify(row):
    rel = pathlib.PurePosixPath(row["path"])
    need(not rel.is_absolute() and ".." not in rel.parts, "relative binding")
    path = ROOT / rel
    need(path.is_file() and path.stat().st_size == row["bytes"] and sha(path) == row["sha256"], "binding " + str(rel))

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    for name in ["out", "gap", "lean", "packages"]:
        ap.add_argument("--" + name, type=pathlib.Path, required=True)
    ap.add_argument("--verify-primary", action="store_true")
    args = ap.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(), "fresh raw output directory")
    out = args.out.resolve()
    need(not out.exists(), "fresh resolved output directory")
    out.mkdir(parents=True)
    start = time.monotonic()
    manifest_path = ROOT / "phase265_manifest.json"
    need(sha(manifest_path) == AUTHOR_SHA, "frozen author manifest")
    author = json.loads(manifest_path.read_bytes())
    bindings = author["exports"] + [row for row in author["retained_bindings"]
                                   if args.verify_primary or not row["path"].startswith("sources/")]
    for row in bindings:
        verify(row)
    own_manifest = ROOT / "phase271_manifest.json"
    if own_manifest.exists():
        for row in json.loads(own_manifest.read_bytes())["exports"]:
            verify(row)
    executions = []

    def run(label, command):
        then = time.monotonic()
        result = subprocess.run([str(x) for x in command], cwd=out, text=True,
                                capture_output=True, timeout=240)
        stdout, stderr = out / (label + ".stdout"), out / (label + ".stderr")
        stdout.write_text(result.stdout)
        stderr.write_text(result.stderr)
        executions.append(dict(label=label, returncode=result.returncode,
                               seconds=round(time.monotonic()-then, 4),
                               stdout_sha256=sha(stdout), stderr_sha256=sha(stderr)))
        return result

    command = [sys.executable, "-B", "-O", ROOT / "phase265_check.py", "--out", out / "author",
               "--gap", args.gap, "--lean", args.lean, "--packages", args.packages]
    if args.verify_primary:
        command.append("--verify-primary")
    result = run("author", command)
    need(result.returncode == 0, "author replay")
    author_report = json.loads((out / "author/report.json").read_bytes())
    need(author_report["status"] == "PASS" and author_report["source_rows"] == 44
         and author_report["proof_spans"] == 13 and len(author_report["axiom_reports"]) == 4,
         "exact author scope")

    result = run("geometry", [sys.executable, "-B", "-O", ROOT / "phase271_independent_geometry.py",
                              "--out", out / "geometry.json"])
    need(result.returncode == 0 and "PHASE271_INDEPENDENT_PASS" in result.stdout, "independent geometry")
    geometry = json.loads((out / "geometry.json").read_bytes())
    need(geometry["status"] == "PASS" and len(geometry["circle_models"]) == 4
         and sum(x["signature_pairs"] for x in geometry["hermitian_models"]) == 540910,
         "complete independent diagnostics")
    result = run("a7", [args.gap, "-q", "-T", ROOT / "phase271_independent_a7.g"])
    need(result.returncode == 0 and "PHASE271_A7_PASS" in result.stdout
         and not re.search(r"Error|warning", result.stdout + result.stderr, re.I), "independent A7 reconstruction")

    source = (ROOT / "phase271_independent_geometry.py").read_text()
    controls = [
        ("positive_incidence", "if p in blocks[m] and q not in blocks[l]:",
         "if p in blocks[m] and q in blocks[l]:", "literal panel completion"),
        ("remove_semilinear_half", "H=[(a,e) for a in matrices for e in [0,1]",
         "H=[(a,e) for a in matrices for e in [0]", "frame orders"),
        ("wrong_trace", "==F.neg(1)", "==0", "sampled exact unital criterion")
    ]
    for label, old, new, expected in controls:
        need(source.count(old) == 1, label + " unique mutation")
        mutant = out / (label + ".py")
        mutant.write_text(source.replace(old, new))
        target = out / (label + ".json")
        result = run(label, [sys.executable, "-B", "-O", mutant, "--out", target])
        need(result.returncode != 0 and "PHASE271_REJECT " + expected in result.stdout + result.stderr
             and not target.exists(), label + " rejected at mathematical assertion")
    for row in bindings:
        verify(row)
    need(sha(manifest_path) == AUTHOR_SHA, "author unchanged")
    report = dict(status="PASS", author_manifest_sha256=AUTHOR_SHA,
                  seconds=round(time.monotonic()-start, 4), primary_checked=args.verify_primary,
                  author_exports_checked=len(author["exports"]), author_rows=44, author_proof_spans=13,
                  actual_lean_declarations=4, independent_signature_pairs=540910,
                  independent_circle_models=4, independent_controls=[x[0] for x in controls],
                  executions=executions,
                  scope="Fresh execution supports, but does not replace, the full written independent review.",
                  limits=["Retained BDL classification and classical full automorphism inputs remain explicit.",
                          "Phase210 written transport interface reviewed for this use; no independent review of this reviewer's earlier phase210 Lean is claimed.",
                          "No complete classification has been formalized; no ratio, priority, question or global-count claim follows from replay."])
    (out / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(dict(status="PASS", seconds=report["seconds"], report=str(out / "report.json"))))

if __name__ == "__main__":
    main()
