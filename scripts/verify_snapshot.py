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

# Exact project-authored renderings only. Primary publication PDFs and source
# raster/text captures remain excluded from the distributed snapshot.
OWN_RENDERED_PDFS = {
    "research/case_study/phase179_livingstone.pdf":
        "e5ff46b8b96e00402470eff20b5ba6815bb647d577a58de0ec08f0726316b836",
    "research/case_study/phase164_enumeration.pdf":
        "fa29377f2139bfbf7bb338227c9efd6b33e8e2f4f3c03365d0853bbd79d8bbf2",
    "research/case_study/phase150_module_C_render/application.pdf":
        "9ab28c9313517f94f927b8b1e99c1a43f9702bdb505045d9d59e1108072c7202",
    "research/case_study/phase144_render/replacement.pdf":
        "5708e7b1c0507547645ecacfb9d19c917dd37d3288a4dd939520a4b3e47cbb81",
    "research/case_study/phase138_render_A_v2/application.pdf":
        "10ddd1c09774e6c3cea960025b9bb1081111b85b49684d22e7491ea13d81272b",
    "research/case_study/phase138_render_U/application.pdf":
        "c541bcb2d5f4662f2771b00b22dbf699fbce10b4c7a6181c843294373e5dc2cd",
    "research/case_study/phase132_module_B_render/application.pdf":
        "d1f285d15fa3f1aeca04d9bf86c52ab79eef557f1c88d32b44598de41caa5bbd",
    "research/case_study/phase117_two_group_application_render/application.pdf":
        "4183f4dfecf7bc01d87af73dde3607e68ca76844d97d8d729a98e2cdd5c71491",
    "research/case_study/phase51_compress_C_measurement_replacement.pdf":
        "e7b7a19ea3dc979ef12e57885bd0ba8d8e87c087ef4d09979167a6e2870b59f8",
    "research/case_study/phase57_ten_source_measurement_replacement.pdf":
        "5a21613dd5310db8daac0700cea5994e50fb0a8c404c6896f832735d15c3119b",
    "research/case_study/phase84_eleven_measurement_replacement.pdf":
        "9af1d1dda508d061d12993d93f2b63d630a08bf3fdc95c01b9594302f698239b",
    "research/case_study/phase98_twelve_measurement_render/replacement.pdf":
        "a9736e98b5eaa49386a0a7c40afb337872e033cb3826db1ae4a49d090b52662c",
}

# This immutable rendering input is a byte-for-byte snapshot of the root
# ATTRIBUTION.md, whose links keep their original base. It is not the reader's
# navigation page; ATTRIBUTION_11.md links to the live root legend instead.
FROZEN_LINK_BASES = {
    "research/case_study/phase79_eleven_attribution_legend.md":
        ("27a576a7d958ee620a4afe736a28f49a0043e19df17a4b70d29aaf418610ae85", ROOT),
}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def frozen_question_exports():
    """Preserve admitted proof packages when refreshing the public snapshot."""
    manifests = {
        "phase217_export.json": "af256c4766c31865608b5c333cef200533b3f8280351e59295cbf3db292aaeb8",
        "phase221_export.json": "7325a1698d540caf372ac8b4e0bf0f392e706c26ef59279dde7f027d6e797ab7",
    }
    checked = 0
    for name, expected in manifests.items():
        manifest = STUDY / name
        assert digest(manifest) == expected, (name, "changed admission manifest")
        for rel, record in json.loads(manifest.read_text())["files"].items():
            path = ROOT / rel
            assert path.stat().st_size == record["bytes"] and digest(path) == record["sha256"], (
                rel, "changed frozen admission artifact; publish follow-up work separately")
            checked += 1
    return checked


def own_rendered_pages():
    """Admit exactly the independently reviewed authored replacement rasters.

    The fixed manifest hash authenticates the 83 individual raster hashes.
    Primary-publication page images and other PNG paths remain excluded.
    """
    manifest = STUDY / "phase98_twelve_measurement_manifest.json"
    assert digest(manifest) == "7477a91be128f4c0fb953e4a7f4b9d422bd70a371367de1fcee2db0cd59b229d"
    bound = json.loads(manifest.read_text())["files"]
    names = {f"phase98_twelve_measurement_render/page-{n:02d}.png" for n in range(1, 84)}
    assert {p for p in bound if p.endswith(".png")} == names
    assert all((STUDY / name).is_file() for name in names)
    return {"research/case_study/" + name: bound[name]["sha256"] for name in names}


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
        native = re.findall(r"\b\w+\._native\.native_decide\.ax_\d+_\d+", report.get("stdout", ""))
        expected_native = ([f"{name}._native.native_decide.ax_1_1" for name in (
            "third_difference", "terminal_basis_fixed", "fourth_difference", "newton_coefficients"
        )] if source.stem == "Phase23TransferAnnihilator" else [])
        assert native == expected_native, (source.name, "native-evaluation trust boundary changed")
        result.append(source.name)
    assert len(result) == 77, result
    return result


def check_links():
    missing = []
    for path, rel in files():
        if path.suffix != ".md":
            continue
        link_base = path.parent
        if rel in FROZEN_LINK_BASES:
            expected_hash, link_base = FROZEN_LINK_BASES[rel]
            assert digest(path) == expected_hash, (rel, "changed frozen link context")
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if target.startswith(("http:", "https:", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0].strip("<>")
            if target and not (link_base / target).exists():
                missing.append((str(path.relative_to(ROOT)), target))
    assert not missing, missing


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-manifest", action="store_true",
                        help="Record reviewed publication bytes; does not certify new mathematics.")
    args = parser.parse_args()
    frozen = frozen_question_exports()
    checked = lean_reports()
    check_links()
    rendered_pages = own_rendered_pages()
    rows = []
    for path, rel in files():
        if path.is_symlink():
            assert path.resolve().is_relative_to(ROOT), rel
            rows.append({"file": rel, "symlink": str(path.readlink())})
        else:
            if path.suffix == ".pdf":
                assert rel in OWN_RENDERED_PDFS and digest(path) == OWN_RENDERED_PDFS[rel], rel
            elif path.suffix == ".png":
                assert rel in rendered_pages and digest(path) == rendered_pages[rel], rel
            else:
                assert path.suffix not in {".png", ".html", ".pid"}, rel
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
    print(f"PASS: {frozen} frozen question-proof publication artifacts retain their admitted bytes.")
    print("Trust scope: 76 reports without native-evaluation axioms; 1 transfer report with four explicitly recorded native-evaluation axioms.")
    print("PASS: local documentation links resolve in their recorded context; the frozen root-legend input retains its original base.")
    print("External publications are referenced, not bundled.")
    print("This is an integrity check. Run scripts/smoke_check.py to rerun selected computations.")


if __name__ == "__main__":
    main()
