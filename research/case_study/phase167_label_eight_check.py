#!/usr/bin/env python3
"""Rebuild the literal label-eight finite rewrite certificate with the Lean kernel."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import shutil
import subprocess
import sys
import time

DEPENDENCY_SHA = "4c716f4ff0ea4940311014c9853c0b8e5aaab8250f8cefdf9f8003845cfb02e3"
NAMESPACE = "MathCompression.LabelEightCriticalPairs"
MODULES = [
    ("LabelEightCriticalPairs.lean",
     "22dce0b70cba3f4a9c9e3608bda7ee829e7d3d7352ec96d887e2a2b3a07a092d",
     {"next_sound", "collect_reachable", "criticalCheck_sound"}),
    ("LabelEightFiniteCertificate.lean",
     "7e8955c729a052f24075197e24371abdbcf77efd0f45f972b85320cfa4cffec4",
     {"allCritical_sound", "allCritical14_verified", "rank14_critical_pairs_join",
      "allSourceWords_verified", "rank3_source_word_reduces"}),
    ("LabelEightAlphabet.lean",
     "31a97fdde7ed8c518c8251a90a82498e4041cc58dce2d94a29bd7e6d75f7a24b",
     {"rank14_rules_closed", "rank3_rules_closed", "step_preserves_alphabet",
      "reachable_restrict", "rank14_critical_pairs_join_in_alphabet",
      "sourceWord_bounded", "rank3_source_word_reduces_in_alphabet"}),
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--packages", type=Path, required=True)
    ap.add_argument("--lean", default="lean")
    ap.add_argument("--source-dir", type=Path,
                    default=Path(__file__).resolve().parent / "formal")
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    output = args.output_dir.absolute()
    require(not output.exists() and not output.is_symlink(), "Fresh output directory required")
    source_dir = args.source_dir.resolve()
    dependency_file = source_dir / "dependency_manifest.json"
    require(sha(dependency_file) == DEPENDENCY_SHA, "Frozen dependency manifest changed")
    for name, expected, _ in MODULES:
        source = source_dir / name
        require(sha(source) == expected, "Frozen source changed: " + name)
        require(not re.search(r"\b(sorry|admit|axiom|native_decide)\b", source.read_text()),
                "Unproved or native-evaluated source declaration: " + name)
    dependencies = json.loads(dependency_file.read_text())
    lean = shutil.which(args.lean)
    require(lean is not None, "Lean executable not found")
    env = dict(os.environ)
    env["ELAN_TOOLCHAIN"] = dependencies["lean"]
    version = subprocess.check_output([lean, "--version"], env=env, text=True).strip()
    expected_version = dependencies["lean"].split(":")[-1].removeprefix("v")
    require(re.search(r"\bversion " + re.escape(expected_version) + r"(?:,|\s|\))", version),
            "Unexpected Lean version")
    checked, libraries = [], []
    for item in dependencies["packages"]:
        checkout = args.packages.resolve() / item["name"]
        rev = subprocess.check_output(
            ["git", "-C", str(checkout), "rev-parse", "HEAD"], text=True).strip()
        require(rev == item["rev"], "Wrong dependency revision: " + item["name"])
        clean = subprocess.run(["git", "-C", str(checkout), "diff", "--quiet", "HEAD", "--"])
        require(clean.returncode == 0, "Tracked dependency changed: " + item["name"])
        library = checkout / ".lake/build/lib/lean"
        if library.is_dir():
            libraries.append(library)
        checked.append({"name": item["name"], "revision": rev, "tracked_files_clean": True,
                        "compiled_library_present": library.is_dir()})
    output.mkdir(parents=True, exist_ok=False)
    env["LEAN_PATH"] = os.pathsep.join(map(str, [output] + libraries))
    builds = []
    for name, expected_sha, declarations in MODULES:
        source = source_dir / name
        require(sha(source) == expected_sha, "Frozen source changed during execution: " + name)
        obj = output / name.replace(".lean", ".olean")
        before = resource.getrusage(resource.RUSAGE_CHILDREN)
        started = time.monotonic()
        run = subprocess.run([lean, "-o", str(obj), str(source)], cwd=source_dir, env=env,
                             capture_output=True, text=True, timeout=900)
        elapsed = time.monotonic() - started
        after = resource.getrusage(resource.RUSAGE_CHILDREN)
        log = output / name.replace(".lean", ".log")
        log.write_text(run.stdout + run.stderr)
        require(run.returncode == 0 and not run.stderr.strip(), run.stdout + run.stderr)
        require(not re.search(r"sorryAx|native_decide|warning:|error:", run.stdout),
                "Unexpected diagnostic or trust assumption: " + name)
        prefix = "'" + re.escape(NAMESPACE) + r"\.([A-Za-z0-9_]+)' "
        matches = re.findall(prefix + r"depends on axioms: \[([^]]*)\]", run.stdout)
        matches += [(n, "") for n in re.findall(prefix + r"does not depend on any axioms", run.stdout)]
        require(len(matches) == len(declarations) and {n for n, _ in matches} == declarations,
                "Missing or duplicate axiom report: " + name)
        reports = {}
        for declaration, text in matches:
            axioms = {a.strip() for a in text.split(",") if a.strip()}
            require(axioms <= {"propext", "Classical.choice", "Quot.sound"},
                    "Unexpected axiom: " + declaration)
            reports[NAMESPACE + "." + declaration] = sorted(axioms)
        require(obj.is_file() and not obj.is_symlink(), "Fresh compiler object missing: " + name)
        builds.append({"source": name, "source_sha256": expected_sha,
                       "seconds": elapsed, "exit_code": run.returncode,
                       "child_user_seconds": after.ru_utime - before.ru_utime,
                       "child_system_seconds": after.ru_stime - before.ru_stime,
                       "cumulative_child_peak_rss_raw": after.ru_maxrss,
                       "peak_rss_units": "bytes" if sys.platform == "darwin" else "KiB",
                       "log_sha256": sha(log), "object_sha256": sha(obj),
                       "axiom_reports": reports, "stdout": run.stdout, "stderr": run.stderr})
    require(sha(dependency_file) == DEPENDENCY_SHA, "Frozen dependency manifest changed during execution")
    for name, expected, _ in MODULES:
        require(sha(source_dir / name) == expected, "Frozen source changed during execution: " + name)
    report = {
        "status": "PASS", "date": "2026-10-10", "lean": version,
        "runner_sha256": sha(Path(__file__)),
        "dependency_manifest_sha256": DEPENDENCY_SHA, "dependencies": checked, "builds": builds,
        "printed_declarations": 15, "additional_kernel_checked_row_helpers": 63,
        "rank": 14, "alphabet_size": 63, "descending_triples": 43680,
        "critical_branch_fuel": 32, "rank_three_source_words": 8, "source_word_fuel": 256,
        "scope": "Literal presentation-rewrite reachability; actual joinability of every descending rank-14 triple; reduction to the empty word for the eight rank-three source words; closed finite alphabets and preservation along every intermediate rewrite.",
        "confluence_assumed": False, "sufficient_fuel_assumed": False,
        "target_joinability_assumed": False, "unproved_placeholders": False,
        "native_evaluation_axioms": False,
        "trust_boundary": "All three local sources are freshly compiled. Pinned package revisions and tracked cleanliness are checked; cached package dependency objects and the installed Lean compiler remain trusted. Local proof evaluation uses ordinary kernel reduction. The inherited LEAN_PATH is replaced.",
        "exclusions": ["uniform termination", "support-compression transfer to arbitrary rank",
                       "all-rank confluence", "presented-group normal forms or order",
                       "intersection property", "all-integer source relators",
                       "all-rank polytope existence", "all-label universal-group conjecture",
                       "historical priority", "source compression ratio"]
    }
    (output / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "printed_declarations": 15, "row_helpers": 63,
                      "local_modules_compiled": 3,
                      "seconds": sum(b["seconds"] for b in builds), "output": str(output)}, indent=2))


if __name__ == "__main__":
    main()
