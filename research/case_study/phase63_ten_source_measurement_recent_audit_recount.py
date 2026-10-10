#!/usr/bin/env python3
"""Independent nine-source/full-ten PDF recount; no author helper imports.

Private source PDFs and a fresh phase57 rendering are required. Writes exactly
one new report. Existing reports are refused before reading the source PDFs.
The eight older boundary specifications are checked against their prior freezes;
the new N016 boundaries are explicit and were reviewed on all eight PDF pages.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import re
import subprocess
import sys
import unicodedata
import warnings
from pathlib import Path

import pypdf

ROOT = Path(__file__).resolve().parent
MANIFEST = "phase57_ten_source_measurement_manifest.json"
MANIFEST_SHA = "0637ee54fe1095ff28cdd47e7ee99023b61283856ae07e05a3e29a600299652f"
PROTOCOL = "phase57_ten_source_measurement_protocol.json"
PROTOCOL_SHA = "95971c144cc73ef4321d18ad1ab8bdd347796b39ce2e9dc2e81f4b028ea22063"
PRIOR = {
    "phase43_unified_lower_bound_protocol.json": "8c6459c1ed938f3bc8979579775b66f4b12af317029887e542e7338776dae4c0",
    "phase51_compress_C_measurement_protocol.json": "3109bd2b4e3d6857957b48a0d52ef43f3964a4c2c52d10814bcbfadac1437ad6",
}
KEYS = ["whitespace_tokens", "alphanumeric_units", "characters_without_whitespace",
        "characters_with_collapsed_whitespace", "utf8_bytes_with_collapsed_whitespace"]
N016_INTERVALS = [(360, 496), (1958, 1959), (4818, 4819), (6551, 6552),
                 (9427, 9428), (11306, 11307), (14003, 14004)]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def binding(path):
    data = path.read_bytes()
    return {"sha256": digest(data), "bytes": len(data)}


def require(condition, explanation):
    if not condition:
        raise ValueError(explanation)


def bound_read(path, expected):
    data = path.read_bytes()
    require(digest(data) == expected, "Hash mismatch: " + str(path))
    return data


def metrics(value, form):
    normalized = unicodedata.normalize(form, value)
    units = normalized.split()
    collapsed = " ".join(units)
    return {
        "unicode_normalization": form,
        "whitespace_tokens": len(units),
        "alphanumeric_units": len(re.findall(r"[^\W_]+", collapsed)),
        "characters_without_whitespace": sum(not c.isspace() for c in normalized),
        "characters_with_collapsed_whitespace": len(collapsed),
        "utf8_bytes_with_collapsed_whitespace": len(collapsed.encode("utf-8")),
        "collapsed_text_sha256": digest(collapsed.encode("utf-8")),
    }


def extract(path):
    logged = []

    class Capture(logging.Handler):
        def emit(self, record):
            logged.append(record.getMessage())

    logger = logging.getLogger("pypdf")
    handler = Capture()
    old_propagate = logger.propagate
    logger.addHandler(handler)
    logger.propagate = False
    try:
        with warnings.catch_warnings(record=True) as captured:
            warnings.simplefilter("always")
            reader = pypdf.PdfReader(path)
            pages = [page.extract_text() or "" for page in reader.pages]
        return pages, logged + [str(w.message) for w in captured]
    finally:
        logger.removeHandler(handler)
        logger.propagate = old_propagate


def typed_nodes(node, kind):
    found = []
    if isinstance(node, dict):
        if node.get("t") == kind:
            found.append(node["c"])
        for child in node.values():
            found.extend(typed_nodes(child, kind))
    elif isinstance(node, list):
        for child in node:
            found.extend(typed_nodes(child, kind))
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-root", type=Path, default=ROOT)
    parser.add_argument("--replay", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    root, replay, report_path = args.input_root.resolve(), args.replay.resolve(), args.report.absolute()
    if os.path.lexists(report_path):
        raise FileExistsError("Refusing existing report: " + str(report_path))
    require(pypdf.__version__ == "6.13.0", "Pinned pypdf 6.13.0 required")
    manifest = json.loads(bound_read(root / MANIFEST, MANIFEST_SHA))
    protocol = json.loads(bound_read(root / PROTOCOL, PROTOCOL_SHA))
    author_report = json.loads((root / "phase57_ten_source_measurement_report.json").read_text())
    replay_report = json.loads((replay / "report.json").read_text())
    inputs = {MANIFEST: binding(root / MANIFEST)}
    for name, expected in manifest["files"].items():
        require(binding(root / name) == expected, "Author manifest mismatch: " + name)
        inputs[name] = expected
    for item in (protocol["contract_bindings"] + protocol["external_costs"]
                 + [protocol["measurement_helper"], protocol["render_helper"]]):
        require(binding(root / item["path"]) == {k: item[k] for k in ("sha256", "bytes")},
                "Frozen input mismatch: " + item["path"])
        inputs[item["path"]] = binding(root / item["path"])

    inheritance = {}
    for name, expected_hash in PRIOR.items():
        older = json.loads(bound_read(root / name, expected_hash))
        inputs[name] = binding(root / name)
        for key in older["source_keys"]:
            old = older["documents"][key]
            new = protocol["documents"][key]
            require(all(new[k] == v for k, v in old.items()), "Inherited field changed: " + key)
            additions = set(new) - set(old)
            require(additions <= {"phase57_reading", "expected_extraction_warnings"}, "New source measurement field")
            if "expected_extraction_warnings" in additions:
                require(new["expected_extraction_warnings"] == [], "New warning suppression")
            inheritance[key] = {"prior_protocol": name, "all_prior_fields_identical": True,
                                "new_fields": sorted(additions)}
    require(len(inheritance) == 8, "Expected eight inherited source contracts")

    sources = {}
    for name in ("N003", "N008", "L032", "L035", "F013", "F016", "L088", "N013", "N016"):
        spec = protocol["documents"][name]
        path = root / spec["pdf_path"]
        require(binding(path) == {"sha256": spec["pdf_sha256"], "bytes": spec["pdf_bytes"]}, "Source PDF binding")
        inputs[spec["pdf_path"]] = binding(path)
        pages, extraction_warnings = extract(path)
        if name == "N003":
            text = "".join(f"\n--- PDF PAGE {i+1} ---\n" + page + "\n" for i, page in enumerate(pages))
        elif name == "N008":
            text = "\n\n".join(f"[[PDF PAGE {i+1}; PRINTED {169+i}]]\n" + page for i, page in enumerate(pages))
        else:
            text = "\n".join(pages)
        require(extraction_warnings == spec["expected_extraction_warnings"], "Source warnings changed: " + name)
        require(len(pages) == spec["pages"], "Source page count")
        require(digest(text.encode()) == spec["extraction_sha256"], "Source extraction changed: " + name)
        if "extraction_bytes" in spec:
            require(len(text.encode()) == spec["extraction_bytes"], "Source extraction byte count")
        require(len(spec["page_spans"]) == len(pages), "Page span count")
        for page, span in zip(pages, spec["page_spans"]):
            require(digest(page.encode()) == span["sha256_utf8"], "Source page extraction changed")
            if "start_codepoint" in span:
                require(text[span["start_codepoint"]:span["end_codepoint_exclusive"]] == page, "Source page interval")
        start, end = spec["body"]["start_codepoint"], spec["body"]["end_codepoint_exclusive"]
        intervals = [(e["start_codepoint"], e["end_codepoint_exclusive"]) for e in spec["exclusions"]]
        if name == "N016":
            require((start, end) == (185, 15398) and intervals == N016_INTERVALS, "New N016 explicit boundaries")
            require(text[start:].startswith("Abstract") and text[end:].startswith("\nReferences"), "N016 boundary anchors")
            require("July 25, 2023" in text[:start], "N016 author-edition date")
        if name == "L088":
            require(end == len(text), "L088 late mathematical diagrams must be retained")
        require(digest(text[start:end].encode()) == spec["body"]["sha256_utf8"], "Source body slice changed")
        pieces, cursor = [], start
        for (left, right), exclusion in zip(intervals, spec["exclusions"]):
            require(start <= cursor <= left < right <= end, "Invalid source exclusions")
            removed = text[left:right]
            require(digest(removed.encode()) == exclusion["sha256_utf8"], "Excluded text hash")
            if "exact_excluded_text" in exclusion:
                require(removed == exclusion["exact_excluded_text"], "Excluded text changed")
            pieces += [text[cursor:left], " "]
            cursor = right
        pieces.append(text[cursor:end])
        body = "".join(pieces)
        require("PDF PAGE" not in body, "Generated extraction wrapper charged as source body")
        computed = {form: metrics(body, form) for form in ("NFC", "NFKC")}
        for comparison in (author_report, replay_report):
            require(computed == comparison["source_documents"][name]["metrics"], "Independent source count disagrees: " + name)
            require(digest(body.encode()) == comparison["source_documents"][name]["cleaned_body_sha256"], "Cleaned source body differs")
        sources[name] = {
            "pdf": {"path": spec["pdf_path"], **binding(path)}, "pages": len(pages),
            "fresh_extraction_sha256": digest(text.encode()),
            "body_start": start, "body_end_exclusive": end, "excluded_intervals": intervals,
            "cleaned_body_sha256": digest(body.encode()), "metrics": computed,
            "extraction_warnings": extraction_warnings,
            "nonwhitespace_control_codepoints": sorted({ord(c) for c in body if ord(c) < 32 and not c.isspace()}),
        }

    replacement_pieces = []
    for key, start in (("Compress_10", 161), ("required_erratum", 0)):
        spec = protocol["documents"][key]
        path = root / spec["path"]
        value = bound_read(path, spec["sha256"]).decode()
        inputs[spec["path"]] = binding(path)
        require(len(value.encode()) == spec["bytes"], "Replacement source size")
        require((start, len(value)) == (spec["body"]["start_codepoint"], spec["body"]["end_codepoint_exclusive"]), "Complete denominator boundary")
        require(not spec["exclusions"], "Replacement exclusions forbidden")
        body = value[start:]
        require(digest(body.encode()) == spec["body"]["sha256_utf8"], "Replacement source body hash")
        if key == "Compress_10":
            require(body.startswith("The question addressed here"), "Replacement substantive start")
        replacement_pieces.append(body)
    assembled = "\n\n".join(replacement_pieces)
    require(assembled == (replay / "replacement.md").read_text(), "Full replacement plus full erratum assembly")
    require(digest(assembled.encode()) == protocol["expected_rendering"]["assembled_markdown_sha256"], "Replacement assembly hash")
    ast_run = subprocess.run(["/opt/homebrew/bin/pandoc", "--from", protocol["render"]["reader"], "--to", "json"],
                             input=assembled, text=True, capture_output=True, check=True)
    require(not ast_run.stderr, "Independent source AST diagnostic")
    source_ast = json.loads(ast_run.stdout)
    require(source_ast == json.loads((replay / "source-ast.json").read_text()), "Fresh original AST changed")
    final_ast = json.loads((replay / "ast.json").read_text())
    for kind in ("Math", "CodeBlock", "Table"):
        require(typed_nodes(source_ast, kind) == typed_nodes(final_ast, kind), "Changed mathematical/code/table AST: " + kind)
    math_nodes = typed_nodes(final_ast, "Math")
    codes = [node[1] for node in typed_nodes(final_ast, "CodeBlock")]
    programs = re.findall(r"```gap\n(.*?)\n```", assembled, re.S)
    require(len(programs) == 4 and programs == codes[-4:], "Complete four GAP appendices missing")
    for program, certificate in zip(programs, protocol["certificate_programs"]):
        require((program + "\n").encode() == bound_read(root / certificate["path"], certificate["sha256"]), "GAP program bytes changed")
    pages, extraction_warnings = extract(replay / "replacement.pdf")
    text = "\n".join(pages)
    require(not extraction_warnings, "Replacement extraction warnings")
    require(text == (replay / "replacement_extraction.txt").read_text(), "Fresh rendered extraction differs")
    require(digest(text.encode()) == protocol["expected_rendering"]["extraction_sha256"], "Replacement extraction baseline")
    require(len(pages) == 49, "Replacement page count")
    compact_pdf, cursor = "".join(text.split()), 0
    for code in codes:
        compact_code = "".join(code.split())
        position = compact_pdf.find(compact_code, cursor)
        require(position >= 0, "Entire code block is absent from rendered PDF")
        cursor = position + len(compact_code)
    require(len(codes) == 10 and len(typed_nodes(final_ast, "Table")) == 7, "Code/table inventory")
    display_count = sum(node[0]["t"] == "DisplayMath" for node in math_nodes)
    require(len(math_nodes) == 1523 and display_count == 99, "Math AST inventory")
    require(text.count("■") == 70, "Rendered QED count")
    for probe in protocol["expected_rendering"]["literal_probes"]:
        require("".join(probe.split()) in compact_pdf, "Lost notation literal")
    replacement_metrics = {form: metrics(text, form) for form in ("NFC", "NFKC")}
    for comparison in (author_report, replay_report):
        require(replacement_metrics == comparison["replacement"]["rendered_metrics"], "Independent denominator differs")
    ratios = {}
    for form in ("NFC", "NFKC"):
        ratios[form] = {}
        for key in KEYS:
            numerator = sum(sources[s]["metrics"][form][key] for s in sources)
            denominator = replacement_metrics[form][key]
            ratios[form][key] = {"numerator": numerator, "denominator": denominator,
                                "exact_fraction": f"{numerator}/{denominator}", "factor": numerator / denominator}
            for comparison in (author_report, replay_report):
                expected = comparison["conservative_lower_bounds_under_declared_convention"][form][key]
                require(all(ratios[form][key][k] == expected[k] for k in ("numerator", "denominator", "factor")), "Lower-bound disagreement")
    for name, expected in inputs.items():
        require(binding(root / name) == expected, "Input changed during independent recount: " + name)
    output = {
        "schema": "phase63_independent_nine_source_full_ten_recount_v1",
        "status": "PASS_CONSERVATIVE_LOWER_BOUND",
        "independent_implementation": "No author Python modules imported. Fresh pypdf extraction, independently implemented normalization/counts, pinned inheritance equality and explicit new N016 boundaries.",
        "environment": {"python": sys.version, "executable": sys.executable,
                        "pypdf": pypdf.__version__, "unicode_database": unicodedata.unidata_version},
        "recount_script": binding(Path(__file__)), "input_bindings": inputs,
        "replay_directory": str(replay), "replay_report": binding(replay / "report.json"),
        "inherited_source_protocols": inheritance, "sources": sources,
        "replacement": {"fresh_pdf": binding(replay / "replacement.pdf"), "pages": len(pages),
            "extraction_sha256": digest(text.encode()), "metrics": replacement_metrics,
            "assembled_markdown_sha256": digest(assembled.encode()), "complete_erratum_charged": True,
            "internal_lattice_proof_charged": True, "all_four_complete_GAP_programs_charged_once": True,
            "code_blocks": len(codes), "code_block_lines": [len(code.splitlines()) for code in codes],
            "GAP_program_bytes": sum(c["bytes"] for c in protocol["certificate_programs"]),
            "inline_math_nodes": len(math_nodes) - display_count, "display_math_nodes": display_count,
            "table_count": len(typed_nodes(final_ast, "Table")), "qed_in_pdf": text.count("■"),
            "extraction_warnings": extraction_warnings},
        "conservative_lower_bounds": ratios, "N001_credit": 0, "exact_ten_source_factor": None,
        "annotation_reader_measured": False, "annotation_reader_is_proof_dependency": False,
        "metadata_author_name_erratum_is_proof_dependency": False,
        "frozen_inputs_unchanged_pre_post": True,
        "visual_review_performed_by_this_script": False,
        "mathematical_or_priority_proof_performed_by_this_script": False,
    }
    with report_path.open("x", encoding="utf-8") as stream:
        json.dump(output, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(json.dumps({"status": output["status"], "report": str(report_path), **binding(report_path),
                      "NFC": ratios["NFC"]["whitespace_tokens"]}, indent=2))


if __name__ == "__main__":
    main()
