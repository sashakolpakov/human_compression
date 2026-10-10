"""Check public snapshot integrity and the precise saved Lean-certificate scope.

This does not rerun the mathematical computations. Use smoke_check.py for that.
The manifest binds distributed bytes; historical report hashes remain historical.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "provenance/snapshot_manifest.json"
STUDY = ROOT / "research/case_study"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def files():
    for path in sorted(ROOT.rglob("*")):
        rel = path.relative_to(ROOT)
        if any(p in {".git", ".lake", ".verification", ".venv", "__pycache__", "scratch"} for p in rel.parts):
            continue
        if path == MANIFEST or path.suffix in {".pyc", ".olean", ".ilean"}:
            continue
        if path.is_file() or path.is_symlink():
            yield path, str(rel)


def lean_reports():
    result = []
    for source in sorted((STUDY / "formal").glob("*.lean")):
        if source.name == "lakefile.lean":
            continue
        report_path = source.with_suffix(".check.json")
        report = json.loads(report_path.read_text())
        assert report["exit_code"] == 0, source.name
        assert report["sha256"] == digest(source), (source.name, "stale source hash")
        assert "sorryAx" not in report.get("stdout", ""), source.name
        assert not re.search(r"\b(sorry|admit)\b", source.read_text()), source.name
        result.append(source.name)
    assert len(result) == 18, result
    return result


def check_links():
    missing = []
    for path, _ in files():
        if path.suffix != ".md":
            continue
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if target.startswith(("http:", "https:", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0].strip("<>")
            if target and not (path.parent / target).exists():
                missing.append((str(path.relative_to(ROOT)), target))
    assert not missing, missing


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifest", action="store_true",
                        help="Record reviewed publication bytes; does not certify new mathematics.")
    args = parser.parse_args()
    checked = lean_reports()
    check_links()
    rows = []
    for path, rel in files():
        if path.is_symlink():
            assert path.resolve().is_relative_to(ROOT), rel
            rows.append({"file": rel, "symlink": str(path.readlink())})
        else:
            assert path.suffix not in {".pdf", ".png", ".html", ".pid"}, rel
            rows.append({"file": rel, "sha256": digest(path), "bytes": path.stat().st_size})
    if args.write_manifest:
        MANIFEST.write_text(json.dumps({
            "date": "2026-10-10",
            "scope": "Public file integrity and saved Lean report/source agreement; not a new execution of all mathematical proofs or checks.",
            "lean_reports": checked,
            "external_sources": "Source full texts and GAP library inputs are intentionally excluded; see research/case_study/sources/source_assets.json.",
            "files": rows,
        }, indent=2) + "\n")
        print("Recorded public snapshot manifest.")
    manifest = json.loads(MANIFEST.read_text())
    assert manifest["files"] == rows, "Snapshot differs from its publication manifest."
    print(f"PASS: {len(rows)} published artifacts; {len(checked)} saved Lean reports match their sources.")
    print("PASS: local documentation links resolve; external publications are referenced, not bundled.")
    print("This is an integrity check. Run scripts/smoke_check.py to rerun selected computations.")


if __name__ == "__main__":
    main()
