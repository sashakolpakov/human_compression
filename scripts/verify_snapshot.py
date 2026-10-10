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
    "research/case_study/phase268_point_cloning.pdf":
        "bea25c468166e7743010a39c875c611e1bb6a31d6461c1870fc1f50b83882e48",
    "research/case_study/phase246_locally_faithful_covers.pdf":
        "c680e40ec35e49c9cbdc14ff951b2492aaa26bc0638066b66a55c8122ab162ec",
    "research/case_study/phase258_projective_maniplexes.pdf":
        "b9d3d0ef1a2e02faa992fab70e4dd7bed5638230e576cdd52f8cc78b8b9a746a",
    "research/case_study/phase257_four_families.pdf":
        "0409ad2048072752a9ce0f7cb70cd0229cc229fade475080e92d9e32dac25965",
    "research/case_study/phase250_affine_lattice_umbrella.pdf":
        "e44c7c97b7c0f61830ddd15299be0a3beff063358f18210222cb077aa82b103b",
    "research/case_study/phase250_mixed_prime_application.pdf":
        "b91fafc778f8cf5a189007d5fb45284d84a8cb1f6d37d212cbe9aa864b8d1e1a",
    "research/case_study/phase251_code_appendix.pdf":
        "8d160981cf9d96fb2c0ca849d8d0179161bcdfa0e18992da98e71b81f3036ad5",
    "research/case_study/phase236_odd_kernel_manuscript.pdf":
        "aafaf06208e37deadb354be5c24907a0d51a972672587cdaec7a32228d6de580",
    "research/case_study/phase238_topic_E_umbrella.pdf":
        "26f89586c13c75b278ad5cc701e8e71ed71b2dacc9cd4b121606c92a970471b4",
    "research/case_study/phase238_L083_application.pdf":
        "65a448586998eef8314bd215b51d9be90aa6da04dcec3019d64696df9f5aa2a6",
    "research/case_study/phase238_L079_application.pdf":
        "b4ae8804c17be65ffdf056ebfc900c498f880393e892a2c28b2a8915726acc0d",
    "research/case_study/phase230_rank_one_classification.pdf":
        "fc8364d6e4a04f522fc634f12fd106121e79bd21d1219deb0d2a67c8508eaa7a",
    "research/case_study/phase232_application.pdf":
        "5f5d32b0c1699e0253939c48042e14e072ad1684f02a7aee2a55068081520df5",
    "research/case_study/phase228_umbrella.pdf":
        "a847695734b9e9bb88f3b0a6b977197c480fa8b667998751268898e3eb500166",
    "research/case_study/phase228_application.pdf":
        "3bd794ddfc116ab28d83d8d99c43160db4311e28dd2c574678658bc49bcf590b",
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
    "research/case_study/phase221_infinite_minimal_covers_reader.md":
        ("a46769cc33cccf3100e0a017f1d79ea155e3010a4eb144987a3bbe48a823c575", ROOT),
}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def frozen_question_exports():
    """Preserve admitted proof packages when refreshing the public snapshot."""
    manifests = {
        "phase275_export.json": "424e086716452bf776c5ad7e56061b90a9023c62dda92f3ca4d2562d564bf73b",
        "phase270_export.json": "31a643201a8e4b85adcea74064391d74d23a74430f605e08d6c471883b4bfb17",
        "phase269_export.json": "957b996134bad5df0dfe8146a345d8f4d0f0c99629424c1318e8a7a6a08bd4aa",
        "phase260_export.json": "2b1f0ed5cd074950b9d0a20dfa69004b0de6c2a04dd646962ed2c3d7f291cb19",
        "phase264_export.json": "ead4da8042604b23cf367013c69d968ecf040b53539c78e3fee8ea31c2e74b07",
        "phase262_export.json": "45e64ab258da84fb87faf1cfb7245ee1adeae6e6bde9d426bda95d3cf3c9c951",
        "phase259_export.json": "1f99f26828e6d1f25cca7b7270e4395849daa86ad752d45c09e5c75f21d4541a",
        "phase253_export.json": "34ea2524bc18a08bbf676495a32facae5b433359fee4d773b4a557c4a7b12c07",
        "phase249_export.json": "6c6866615a17f9d2e2bd70f67d98bba462e1c704212a993082a867e57f8b1bbc",
        "phase247_export.json": "cc75729ebfa9457b610cf4596f913f2ea36edb2fd13697c9274b016bc6141f58",
        "phase244_export.json": "0c127e2b1ef4cdce3d150565e224c06a13af17a2fa26f8a59e23eb67421f4e43",
        "phase243_export.json": "a6eac730f11e8f8a7b81e67d826f1e9adfba08807436c27ae4111972252dd9cb",
        "phase235_export.json": "18882d876f74b42ee6c6a91c192b46a82d25ca90c659cf5f447f2eba81b21ed8",
        "phase217_export.json": "af256c4766c31865608b5c333cef200533b3f8280351e59295cbf3db292aaeb8",
        "phase221_export.json": "7325a1698d540caf372ac8b4e0bf0f392e706c26ef59279dde7f027d6e797ab7",
        "phase223_export.json": "89f51c64ef3f86c0b1f566223ce0afb8e92e366f11dc52f963e454b887ef65a7",
        "phase225_export.json": "2da3e1b6d6fea721b051bf4f575c615de80ff7c3a1b65465d23f844860c9e061",
        "phase231_export.json": "73b010822235ac33101c4cd30e29a159b1a6870affb5bf72aab986828cc9a298",
        "phase233_export.json": "8a402eae507217bd178210c89a71090ad5e7833f8cc974aea2f4b182b2f607cb",
    }
    # Current readers may be updated; their original publication bytes stay
    # bound at these explicit archive paths. No proof bytes are rewritten.
    archived = {
        ("phase221_export.json", "INFINITE_MINIMAL_COVERS.md"):
            "research/case_study/phase221_infinite_minimal_covers_reader.md",
    }
    checked = 0
    for name, expected in manifests.items():
        manifest = STUDY / name
        assert digest(manifest) == expected, (name, "changed admission manifest")
        for rel, record in json.loads(manifest.read_text())["files"].items():
            path = ROOT / archived.get((name, rel), rel)
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
    assert len(result) == 93, result
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
    print("Trust scope: 92 reports without native-evaluation axioms; 1 transfer report with four explicitly recorded native-evaluation axioms.")
    print("PASS: local documentation links resolve in their recorded context; the frozen root-legend input retains its original base.")
    print("External publications are referenced, not bundled.")
    print("This is an integrity check. Run scripts/smoke_check.py to rerun selected computations.")


if __name__ == "__main__":
    main()
