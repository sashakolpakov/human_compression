#!/usr/bin/env python3
"""Render the exact frozen Compress_A v1 body and measure representation sensitivity.

Requires pandoc 3.10, the bound XeLaTeX release, and pypdf 6.13.0 by default.
Use --output-dir with a NEW private scratch directory. No source text or source
PDF is copied. Only the authored replacement is rendered there. This is not a
mathematical coverage checker or an approved compression-factor calculation.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import unicodedata


HERE = Path(__file__).resolve().parent
PROTOCOL_NAME = "phase37_rendered_measurement_protocol.json"
PROTOCOL_SHA256 = "2c3bf7bf8332c0ae1279546b7571e44ca76580e4ada8ed1eac0f96415f57d8ad"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_bound(path: Path, expected: str) -> bytes:
    data = path.read_bytes()
    if sha(data) != expected:
        raise ValueError(f"Hash mismatch: {path}")
    return data


def load_helper(path: Path):
    spec = importlib.util.spec_from_file_location("frozen_body_measurement", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load the bound measurement helper")
    module = importlib.util.module_from_spec(spec)
    old = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    try:
        spec.loader.exec_module(module)
    finally:
        sys.dont_write_bytecode = old
    return module


def json_write(path: Path, obj: dict) -> None:
    with path.open("x", encoding="utf-8") as stream:
        json.dump(obj, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def program_info(name: str) -> dict:
    located = shutil.which(name)
    if located is None:
        raise RuntimeError(f"Required executable is unavailable: {name}")
    # Preserve the invocation name: xelatex may be a symlink to xetex, whose
    # format selection depends on argv[0]. Hash the resolved binary separately.
    path = Path(located).absolute()
    binary = path.resolve()
    result = subprocess.run([str(path), "--version"], capture_output=True,
                            text=True, check=True)
    return {"path": str(path), "binary_realpath": str(binary),
            "sha256": sha(binary.read_bytes()),
            "version_output": result.stdout.strip(),
            "first_line": result.stdout.splitlines()[0]}


def ast_counts(node) -> dict:
    counts = {"inline_math": 0, "display_math": 0, "qed_str_occurrences": 0}

    def visit(value) -> None:
        if isinstance(value, dict):
            if value.get("t") == "Math":
                kind = value["c"][0]["t"]
                if kind not in ("InlineMath", "DisplayMath"):
                    raise ValueError(f"Unexpected Pandoc math node: {kind}")
                counts["inline_math" if kind == "InlineMath" else "display_math"] += 1
            if value.get("t") == "Str":
                counts["qed_str_occurrences"] += value["c"].count("∎")
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(node)
    return counts


def font_names(reader) -> list[str]:
    names = set()
    for page in reader.pages:
        resources = page.get("/Resources")
        if resources is None:
            continue
        fonts = resources.get_object().get("/Font")
        if fonts is None:
            continue
        for reference in fonts.get_object().values():
            font = reference.get_object()
            if "/BaseFont" in font:
                names.add(str(font["/BaseFont"]))
    return sorted(names)


def report_markdown(report: dict) -> str:
    lines = [
        "# Frozen two-paper replacement: rendering sensitivity",
        "",
        "This fresh run renders the fixed Compress_A v1 body, then applies the "
        "frozen counting rules to its PDF extraction. Source bodies and exclusions "
        "remain unchanged. All quotients below describe these representations; "
        "none is an approved compression factor.",
        "",
        f"Status: `{report['status']}`. Output directory: `{report['output_directory']}`.",
        "",
        "| Normalization | Count unit | Source sum | Raw replacement | Rendered replacement | Source/raw | Source/rendered |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for form in report["normalization_forms"]:
        for key in report["metric_keys"]:
            src = report["source_body_sums"][form][key]
            raw = report["replacement"]["raw"][form][key]
            rendered = report["replacement"]["rendered"][form][key]
            lines.append(f"| {form} | {key} | {src} | {raw} | {rendered} | "
                         f"{src / raw:.6f} | {src / rendered:.6f} |")
    lines.extend([
        "",
        f"The PDF has {report['rendering']['pages']} pages. Pandoc parses "
        f"{report['rendering']['ast']['inline_math']} inline and "
        f"{report['rendering']['ast']['display_math']} display math expressions. "
        f"All {report['rendering']['ast']['qed_str_occurrences']} proof-end marks "
        f"appear as {report['rendering']['extracted_qed_black_squares']} extracted black squares.",
        "",
        f"Pandoc/rendering stderr is empty: `{report['rendering']['stderr_empty']}`. "
        f"Missing-glyph diagnostics: `{report['rendering']['missing_glyph_diagnostics']}`. "
        f"The bound exploratory AST and extraction replay exactly: "
        f"`{report['baseline_replay']['all_expected_checks_pass']}`.",
        "",
        "N001 remains a damaged browser transcription with control characters and "
        "formula/diagram loss, and its original PDF is still unavailable. Rendering "
        "the replacement does not make the source representations uniform. Text "
        "extraction is sensitive to formula layout, ligatures, font encodings and "
        "line boundaries. The run makes no mathematical equivalence claim and "
        "does not measure or admit the three-paper manuscript.",
        "",
        "The root agent previously inspected pages 2 and 3 of the bound exploratory "
        "render. That is a limited visual observation, not a complete visual audit. "
        "This runner checks syntax counts, proof-end marks, diagnostics and exact "
        "extraction replay; it does not visually inspect pages.",
        "",
        "Reproduction requires the private hash-bound primary transcriptions, "
        "the frozen body protocol/helper and v1 manuscript. The runner refuses "
        "an existing output directory and never writes source bodies or source "
        "PDFs. The authored replacement PDF and its extraction stay in the chosen "
        "private scratch directory. `report.json` records all input/output hashes, "
        "versions, commands, font names, exact counts and normalization hashes.",
        "",
        "Run with Python and the bound pypdf/Pandoc/XeLaTeX versions; replace the "
        "paths below with the private input directory and a new output directory:",
        "",
        "```sh",
        "python3 phase37_rendered_measurement.py \\",
        "  --input-root /path/to/private/research/leemans \\",
        "  --output-dir /private/tmp/compress-A-v1-render-NEW",
        "```",
        "",
        "A toolchain mismatch is refused by default. `--allow-toolchain-drift` "
        "permits an explicitly labeled sensitivity run, while preserving all "
        "input hashes, body boundaries and counting rules.",
        "",
        "PDF bytes can differ through metadata even when the extracted content "
        "and AST replay exactly; byte-identical PDF reproducibility is not claimed.",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-root", type=Path, default=HERE,
                        help="Directory containing the unchanged bound private inputs")
    parser.add_argument("--protocol", type=Path, default=HERE / PROTOCOL_NAME)
    parser.add_argument("--output-dir", type=Path, required=True,
                        help="NEW private scratch directory; any existing path is refused")
    parser.add_argument("--allow-toolchain-drift", action="store_true",
                        help="Permit other renderer versions, recording drift without treating it as the bound replay")
    args = parser.parse_args()
    out = args.output_dir.expanduser().absolute()
    if os.path.lexists(out):
        raise FileExistsError(f"Refusing existing output directory: {out}")
    protocol = json.loads(read_bound(args.protocol, PROTOCOL_SHA256))
    root = args.input_root.resolve()
    helper_spec = protocol["measurement_helper"]
    helper_path = root / helper_spec["path"]
    read_bound(helper_path, helper_spec["sha256"])
    measure = load_helper(helper_path)
    body_spec = protocol["body_protocol"]
    body_protocol = json.loads(read_bound(root / body_spec["path"], body_spec["sha256"]))
    if body_protocol["documents"][protocol["replacement_key"]]["body"] != protocol["replacement_body"]:
        raise ValueError("Replacement body boundaries differ from the rendering contract")
    docs, bodies = {}, {}
    keys = protocol["source_keys"] + [protocol["replacement_key"]]
    for key in keys:
        spec = body_protocol["documents"][key]
        path = root / spec["path"]
        text = measure.checked_text(path, spec["file_sha256"])
        body, exclusions = measure.body_text(text, spec)
        bodies[key] = body
        docs[key] = {"path": str(path), "file_sha256": spec["file_sha256"],
                     "selected_body": spec["body"], "exclusions": exclusions,
                     "body_after_exclusions_sha256": sha(body.encode()),
                     "metrics": {form: measure.metrics(body, form) for form in protocol["forms"]},
                     "nonwhitespace_control_codepoints": sorted({ord(c) for c in body if ord(c) < 32 and not c.isspace()}),
                     "ligature_codepoint_count": sum(0xFB00 <= ord(c) <= 0xFB06 for c in body)}
    try:
        import pypdf
    except ImportError as exc:
        raise RuntimeError("This runner requires pypdf; the bound release is 6.13.0") from exc
    tools = {name: program_info(name) for name in ("pandoc", "xelatex")}
    expected = protocol["expected_toolchain"]
    drift = {}
    for name in ("pandoc", "xelatex"):
        if tools[name]["first_line"] != expected[name + "_first_line"]:
            drift[name] = {"expected": expected[name + "_first_line"], "actual": tools[name]["first_line"]}
    if pypdf.__version__ != expected["pypdf"]:
        drift["pypdf"] = {"expected": expected["pypdf"], "actual": pypdf.__version__}
    if drift and not args.allow_toolchain_drift:
        raise RuntimeError("Toolchain differs from the bound run; explicit --allow-toolchain-drift is required: " + json.dumps(drift))
    out.mkdir(parents=False, exist_ok=False)
    authored_body = bodies[protocol["replacement_key"]]
    (out / "replacement.md").write_text(authored_body, encoding="utf-8")
    header = protocol["render"]["header"]
    if sha(header.encode()) != protocol["render"]["header_sha256"]:
        raise ValueError("QED header binding failed")
    (out / "qed.tex").write_text(header, encoding="utf-8")
    commands = []

    def run(label: str, command: list[str]) -> subprocess.CompletedProcess:
        result = subprocess.run(command, cwd=out, capture_output=True, text=True)
        (out / f"{label}.stdout.txt").write_text(result.stdout, encoding="utf-8")
        (out / f"{label}.stderr.txt").write_text(result.stderr, encoding="utf-8")
        commands.append({"label": label, "argv": command, "cwd": str(out), "returncode": result.returncode})
        if result.returncode:
            raise RuntimeError(f"{label} failed with exit code {result.returncode}; logs retained in {out}")
        return result

    pandoc = tools["pandoc"]["path"]
    reader_option = "--from=" + protocol["render"]["reader"]
    run("ast", [pandoc, "replacement.md", reader_option, "--to=json", "--output=ast.json"])
    ast_data = (out / "ast.json").read_bytes()
    parsed_counts = ast_counts(json.loads(ast_data))
    for key, count in parsed_counts.items():
        if count != protocol["expected_ast"][key]:
            raise ValueError(f"Parsed syntax count changed: {key}; outputs retained in {out}")
    if authored_body.count("∎") != parsed_counts["qed_str_occurrences"]:
        raise ValueError("A proof-end mark did not survive the Markdown AST")
    options = [reader_option, "--pdf-engine=" + tools["xelatex"]["path"]]
    for variable in protocol["render"]["variables"]:
        options.extend(["--variable", variable])
    options.append("--include-in-header=qed.tex")
    # Save the template and expanded LaTeX as provenance, using the same options.
    template = run("template", [pandoc, "--print-default-template=latex"])
    (out / "default-template.tex").write_text(template.stdout, encoding="utf-8")
    run("latex", [pandoc, "replacement.md", *options, "--standalone", "--to=latex", "--output=replacement.tex"])
    render = run("render", [pandoc, "replacement.md", *options, "--output=replacement.pdf"])
    reader = pypdf.PdfReader(out / "replacement.pdf")
    extracted = protocol["render"]["page_join"].join(page.extract_text() or "" for page in reader.pages)
    (out / "replacement_extraction.txt").write_text(extracted, encoding="utf-8")
    rendered_metrics = {form: measure.metrics(extracted, form) for form in protocol["forms"]}
    stderr = "\n".join((out / f"{item['label']}.stderr.txt").read_text() for item in commands)
    missing = [line for line in stderr.splitlines()
               if re.search(r"missing character|missing glyph|does not contain.*glyph|glyph.*not found", line, re.I)]
    if missing:
        raise RuntimeError(f"Missing-glyph diagnostics; outputs retained in {out}")
    baseline = protocol["expected_rendered"]
    checks = {"ast_hash": sha(ast_data) == protocol["expected_ast"]["sha256"],
              "page_count": len(reader.pages) == baseline["pages"],
              "all_qed_black_squares": extracted.count("■") == baseline["qed_black_squares"],
              "extraction_hash": sha(extracted.encode()) == baseline["extraction_sha256"]}
    for form in protocol["forms"]:
        checks[form + "_metrics"] = all(rendered_metrics[form][key] == value for key, value in baseline[form].items())
    sums, quotients = {}, {}
    for form in protocol["forms"]:
        sums[form] = {metric: sum(docs[key]["metrics"][form][metric] for key in protocol["source_keys"])
                      for metric in protocol["metric_keys"]}
        quotients[form] = {}
        for representation, data in (("raw", docs[protocol["replacement_key"]]["metrics"]), ("rendered", rendered_metrics)):
            quotients[form][representation] = {
                metric: {"source_sum": sums[form][metric], "replacement": data[form][metric],
                         "quotient": sums[form][metric] / data[form][metric]}
                for metric in protocol["metric_keys"]}
    artifact_hashes = {path.name: sha(path.read_bytes()) for path in sorted(out.iterdir()) if path.is_file()}
    report = {
        "schema": "compress_A_v1_rendering_sensitivity_report_v1",
        "status": "rendering_sensitivity_only_bound_replay_pass" if all(checks.values()) and not drift else "rendering_sensitivity_only_replay_drift",
        "output_directory": str(out), "protocol_sha256": PROTOCOL_SHA256,
        "runner_sha256": sha(Path(__file__).read_bytes()),
        "measurement_helper": helper_spec, "body_protocol": body_spec,
        "normalization_forms": protocol["forms"], "metric_keys": protocol["metric_keys"],
        "environment": {"python": sys.version, "python_executable": sys.executable,
                        "platform": platform.platform(), "unicode_database": unicodedata.unidata_version,
                        "pypdf_version": pypdf.__version__, "pypdf_module_sha256": sha(Path(pypdf.__file__).read_bytes()),
                        "programs": tools, "toolchain_drift": drift,
                        "SOURCE_DATE_EPOCH": os.environ.get("SOURCE_DATE_EPOCH"),
                        "FORCE_SOURCE_DATE": os.environ.get("FORCE_SOURCE_DATE")},
        "documents": docs, "source_body_sums": sums,
        "replacement": {"raw": docs[protocol["replacement_key"]]["metrics"], "rendered": rendered_metrics},
        "descriptive_source_sum_divided_by_replacement": quotients,
        "rendering": {"commands": commands, "ast": parsed_counts, "pages": len(reader.pages),
                      "extracted_qed_black_squares": extracted.count("■"), "pdf_font_names": font_names(reader),
                      "stderr_empty": not stderr.strip(), "missing_glyph_diagnostics": missing,
                      "text_repairs_applied": False, "page_join": protocol["render"]["page_join"]},
        "baseline_replay": {"checks": checks, "all_expected_checks_pass": all(checks.values()),
                            "exploratory_provenance": protocol["baseline_provenance"]},
        "artifact_hashes": artifact_hashes,
        "source_text_exported": False, "source_pdf_exported": False,
        "three_paper_measurement": False, "third_paper_numerator_admitted": False,
        "final_compression_factor": None, "whole_document_equivalence_claim": False,
        "interpretation": protocol["interpretation"],
    }
    json_write(out / "report.json", report)
    with (out / "report.md").open("x", encoding="utf-8") as stream:
        stream.write(report_markdown(report))
    json_write(out / "manifest.json", {"files": {path.name: sha(path.read_bytes()) for path in sorted(out.iterdir()) if path.is_file()},
                                       "source_bodies_included": False, "authored_render_only": True})
    print(json.dumps({"status": report["status"], "output_directory": str(out),
                      "report_sha256": sha((out / "report.json").read_bytes()),
                      "rendered_NFC": rendered_metrics["NFC"],
                      "rendered_NFKC": rendered_metrics["NFKC"],
                      "baseline_checks": checks, "final_compression_factor": None}, indent=2))
    if not all(checks.values()) and not args.allow_toolchain_drift:
        raise SystemExit("The render differs from the bound exploratory content; inspect the retained report before using it.")


if __name__ == "__main__":
    main()
