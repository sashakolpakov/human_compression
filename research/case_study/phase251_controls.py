"""Check that the measurement rejects altered proof inputs under Python -O."""
from pathlib import Path
import argparse
import json
import subprocess
import sys
import tempfile


def main(root, output):
    if output.exists():
        raise ValueError("use a new report path")
    config = json.loads((root / "phase251_boundaries.json").read_text())
    paths = [v["path"] for v in (config["sources"] | config["ours"]).values()]
    paths += ["phase251_protocol.md", "phase230_finite_check.g", "phase238_render_config.json",
              "phase251_code_appendix.md"]
    reports = []
    for mode in ["changed_source_pdf", "shifted_proof_boundary", "changed_required_program"]:
        with tempfile.TemporaryDirectory(prefix="phase251-control-") as temp:
            directory = Path(temp)
            for name in paths:
                target = directory / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.symlink_to((root / name).resolve())
            bound = json.loads(json.dumps(config))
            if mode == "changed_source_pdf":
                target = directory / config["sources"]["L083"]["path"]
                original = target.read_bytes()
                target.unlink()
                target.write_bytes(original + b"\nchanged")
                expected = "L083 PDF changed"
            elif mode == "shifted_proof_boundary":
                bound["sources"]["L083"]["included_spans"][0]["start"] += 1
                expected = "span hash changed"
            else:
                target = directory / "phase230_finite_check.g"
                target.unlink()
                target.write_text("# removed required calculation\n")
                expected = "required program changed"
            (directory / "phase251_boundaries.json").write_text(json.dumps(bound))
            p = subprocess.run([sys.executable, "-B", "-O", str(root / "phase251_measure.py"),
                                "--root", str(directory), "--out", str(directory / "out.json")],
                               capture_output=True, text=True, timeout=90)
            if p.returncode == 0 or expected not in p.stderr or (directory / "out.json").exists():
                raise ValueError("control did not reject correctly: " + mode + p.stderr)
            reports.append({"control": mode, "exit_code": p.returncode,
                            "expected_rejection": expected, "report_written": False})
    result = {"status": "PASS", "python_optimization": 1, "controls": reports,
              "scope": "Input-integrity rejection controls, not mathematical theorem tests."}
    output.write_text(json.dumps(result, indent=2) + "\n")
    print("PASS: three altered-input controls rejected under -O")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    main(args.root, args.out)
