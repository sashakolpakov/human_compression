"""Replay all fourteen counting cases from the pinned classification inputs."""
import sys
if not __debug__:
    raise SystemExit("Run without Python optimization.")
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import time
from counting_verify import verify, controls, need

BASE = Path(__file__).resolve().parent


def pincheck(path, item):
    data = path.read_bytes()
    need(len(data) == item["bytes"] and hashlib.sha256(data).hexdigest() == item["sha256"],
         "Changed bound input: " + str(path))


def run(command, directory, seconds):
    directory.mkdir()
    start = time.monotonic()
    with (directory / "stdout").open("wb") as so, (directory / "stderr").open("wb") as se:
        try:
            result = subprocess.run([str(x) for x in command], stdout=so,
                                    stderr=se, timeout=seconds)
        except subprocess.TimeoutExpired:
            receipt = dict(status="TIMEOUT_NOT_A_PROOF", elapsed_seconds=time.monotonic() - start)
            (directory / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
            raise
    receipt = dict(returncode=result.returncode, elapsed_seconds=time.monotonic() - start)
    (directory / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    need(result.returncode == 0 and not (directory / "stderr").read_text().strip(),
         "Failed execution: " + str(directory))
    return receipt


def native(out):
    out.mkdir()
    shutil.copy2(BASE / "counting.tex", out / "counting.tex")
    for i in range(2):
        run(["pdflatex", "-halt-on-error", "-interaction=nonstopmode",
             "-output-directory=" + str(out), out / "counting.tex"], out / ("pass" + str(i)), 60)
    log = (out / "counting.log").read_text()
    need("Overfull" not in log and "LaTeX Warning" not in log, "Native layout or references")
    from pypdf import PdfReader
    text = "\n".join(page.extract_text() or "" for page in PdfReader(out / "counting.pdf").pages)
    (out / "text.txt").write_text(text)
    expected = (BASE / "native/text.txt").read_text()
    need(text == expected, "Native text matches frozen manuscript")
    run(["gs", "-q", "-dNOPAUSE", "-dBATCH", "-sDEVICE=png16m", "-r110",
         "-sOutputFile=" + str(out / "page-%02d.png"), out / "counting.pdf"], out / "render", 60)
    return dict(pages=len(PdfReader(out / "counting.pdf").pages), text_matches=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--study", type=Path, required=True)
    ap.add_argument("--gap", type=Path, default=Path(shutil.which("gap") or "/missing/gap"))
    ap.add_argument("--gap-root", type=Path)
    ap.add_argument("--render", action="store_true")
    args = ap.parse_args()
    need(args.out.is_absolute() and not args.out.exists() and not args.out.is_symlink(),
         "Use a fresh absolute output path")
    gap = args.gap.resolve()
    roots = dict(study=args.study.resolve(), gap=(args.gap_root or gap.parent.parent).resolve())
    manifest = json.loads((BASE / "manifest.json").read_text())
    for item in manifest["exports"]:
        pincheck(BASE / item["path"], item)
    deps = json.loads((BASE / "dependencies.json").read_text())["files"]
    for item in deps:
        pincheck(roots[item["namespace"]] / item["path"], item)
    args.out.mkdir()
    data_path = args.out / "data.json"
    driver = args.out / "driver.g"
    driver.write_text("OutputPath:=" + json.dumps(str(data_path)) + ";;\nRead(" +
                      json.dumps(str(BASE / "counting_export.g")) + ");;\n")
    receipt = run([gap, "-q", "-b", driver], args.out / "gap", 180)
    lines = [s.strip() for s in (args.out / "gap/stdout").read_text().splitlines() if s.strip()]
    need(len(lines) == 15 and lines[-1] == "TERMINAL_PASS 14 sporadic counting cases",
         "Complete fourteen-case GAP terminal receipt")
    data = json.loads(data_path.read_text())
    need(data == json.loads((BASE / "data.json").read_text()), "Exact bound table data reproduced")
    report = verify(data)
    report["negative_controls"] = controls(data)
    need(report == json.loads((BASE / "expected.json").read_text()),
         "Exact independent arithmetic and controls reproduced")
    guard_dir = args.out / "optimization_controls"
    guard_dir.mkdir()
    for script in ["check.py", "counting_verify.py"]:
        r = subprocess.run([sys.executable, "-O", str(BASE / script)], capture_output=True, timeout=15)
        (guard_dir / (script + ".stdout")).write_bytes(r.stdout)
        (guard_dir / (script + ".stderr")).write_bytes(r.stderr)
        need(r.returncode != 0 and r.stderr.decode().strip() == "Run without Python optimization.",
             "Pre-output optimization guard")
    summary = dict(status="PASS_FOURTEEN_SPORADIC_COUNTING_CASES", cases=14,
                   bound_tables=report["bound_tables"], bound_exports=len(manifest["exports"]),
                   bound_dependencies=len(deps), negative_controls=6, optimization_guards=2,
                   gap_execution=receipt, native=native(args.out / "native") if args.render else None,
                   whole_original_credit=0, new_conjecture_credit=0,
                   new_lean_credit=0, new_measurement_credit=0)
    (args.out / "arithmetic.json").write_text(json.dumps(report, indent=2) + "\n")
    (args.out / "report.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
