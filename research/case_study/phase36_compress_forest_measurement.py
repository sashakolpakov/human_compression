#!/usr/bin/env python3
"""Measure exact manuscript-body snapshots without exporting source text.

This is a length/integrity tool, not a proof or coverage checker.  Its ratios
describe the bound textual representations only.  The two private primary
transcriptions are required; the primary N003 PDF is optional corroboration.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import re
import unicodedata


HERE = Path(__file__).resolve().parent


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def checked_text(path: Path, expected: str) -> str:
    data = path.read_bytes()
    actual = digest(data)
    if actual != expected:
        raise ValueError(f"Snapshot hash mismatch for {path}: {actual} != {expected}")
    return data.decode("utf-8")


def checked_span(text: str, span: dict) -> tuple[int, int]:
    start, end = span["start_codepoint"], span["end_codepoint_exclusive"]
    if not 0 <= start <= end <= len(text):
        raise ValueError("Invalid codepoint interval")
    if digest(text[start:end].encode()) != span["sha256_utf8"]:
        raise ValueError(f"Span hash mismatch at {start}:{end}")
    return start, end


def body_text(text: str, spec: dict) -> tuple[str, list[dict]]:
    start, end = checked_span(text, spec["body"])
    exclusions = []
    for span in spec["exclusions"]:
        a, b = checked_span(text, span)
        if not start <= a < b <= end:
            raise ValueError("An exclusion escapes its selected body")
        exclusions.append((a, b, span["kind"]))
    exclusions.sort()
    if any(a[1] > b[0] for a, b in zip(exclusions, exclusions[1:])):
        raise ValueError("Overlapping exclusions")
    chunks, cursor, log = [], start, []
    for a, b, kind in exclusions:
        chunks.extend((text[cursor:a], " "))
        log.append({"kind": kind, "codepoints": b - a,
                    "start_codepoint": a, "end_codepoint_exclusive": b})
        cursor = b
    chunks.append(text[cursor:end])
    return "".join(chunks), log


def metrics(text: str, form: str = "NFC") -> dict:
    normalized = unicodedata.normalize(form, text)
    collapsed = " ".join(normalized.split())
    # Alphanumeric runs are a representation-sensitive word proxy, not prose
    # words: they include formula identifiers, numbers and TeX command names.
    return {
        "unicode_normalization": form,
        "whitespace_tokens": len(collapsed.split()),
        "alphanumeric_units": len(re.findall(r"[^\W_]+", normalized)),
        "characters_without_whitespace": sum(not c.isspace() for c in normalized),
        "characters_with_collapsed_whitespace": len(collapsed),
        "utf8_bytes_with_collapsed_whitespace": len(collapsed.encode()),
        "collapsed_text_sha256": digest(collapsed.encode()),
    }


def light_markdown(text: str) -> str:
    # Presentation-only sensitivity.  No math delimiters, commands, equations,
    # links, words, proof headings or source-result labels are removed.
    text = re.sub(r"(?m)^#{1,6}[ \t]+", "", text)
    return text.replace("**", "").replace("`", "")


def ratio(numerator: int, denominator: int) -> dict:
    return {"numerator": numerator, "denominator": denominator,
            "decimal": numerator / denominator}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path,
                        default=HERE / "phase36_compress_forest_measurement_protocol.json")
    parser.add_argument("--input-root", type=Path, default=HERE)
    parser.add_argument("--n001-text", type=Path)
    parser.add_argument("--n003-text", type=Path)
    parser.add_argument("--replacement", type=Path)
    parser.add_argument("--source-pdf", type=Path)
    parser.add_argument("--verify-pdf-extraction", action="store_true")
    parser.add_argument("--output", type=Path,
                        default=HERE / "phase36_compress_forest_measurement.json")
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(f"Refusing to overwrite existing output: {args.output}")
    protocol_bytes = args.protocol.read_bytes()
    protocol = json.loads(protocol_bytes)
    overrides = {"N001": args.n001_text, "N003": args.n003_text,
                 "Compress_A": args.replacement}
    results, texts = {}, {}
    for key, spec in protocol["documents"].items():
        path = overrides[key] or args.input_root / spec["path"]
        text = checked_text(path, spec["file_sha256"])
        texts[key] = text
        body, log = body_text(text, spec)
        sensitive = light_markdown(body) if spec["format"] == "markdown_tex" else body
        chars = sorted({ord(c) for c in body if ord(c) < 32 and not c.isspace()})
        results[key] = {
            "input_file_sha256": spec["file_sha256"],
            "selected_raw_body_codepoints": spec["body"]["end_codepoint_exclusive"] - spec["body"]["start_codepoint"],
            "selected_raw_body_sha256": spec["body"]["sha256_utf8"],
            "exclusions": log,
            "main_body": metrics(body),
            "nfkc_sensitivity": metrics(body, "NFKC"),
            "light_markdown_sensitivity": metrics(sensitive),
            "extraction_diagnostics": {
                "nonwhitespace_control_codepoints_retained": chars,
                "literal_backslash_command_occurrences": len(re.findall(r"\\[A-Za-z]+", body)),
                "ascii_hyphen_space_between_letters_occurrences": len(re.findall(r"(?<=[A-Za-z])-\s+(?=[A-Za-z])", body)),
                "ligature_codepoints": sum(0xFB00 <= ord(c) <= 0xFB06 for c in body),
            },
        }
    metric_keys = ("whitespace_tokens", "alphanumeric_units",
                   "characters_without_whitespace", "characters_with_collapsed_whitespace",
                   "utf8_bytes_with_collapsed_whitespace")
    totals, ratios = {}, {}
    for convention in ("main_body", "nfkc_sensitivity", "light_markdown_sensitivity"):
        totals[convention] = {
            metric: sum(results[k][convention][metric] for k in ("N001", "N003"))
            for metric in metric_keys}
        ratios[convention] = {
            metric: ratio(totals[convention][metric], results["Compress_A"][convention][metric])
            for metric in metric_keys}
    diagnostics = []
    for span in protocol["scope_diagnostic_spans"]:
        text = texts[span["document"]]
        start, end = checked_span(text, span)
        diagnostics.append({"document": span["document"], "role": span["role"],
                            "start_codepoint": start, "end_codepoint_exclusive": end,
                            "sha256_utf8": span["sha256_utf8"],
                            "raw_metrics": metrics(text[start:end]),
                            "excluded_from_main_body_measurement": False})
    pdf = dict(protocol["optional_pdf"])
    pdf["supplied_and_hash_verified"] = False
    pdf["extraction_replayed"] = False
    if args.source_pdf:
        data = args.source_pdf.read_bytes()
        if digest(data) != pdf["sha256"]:
            raise ValueError("Optional primary PDF hash mismatch")
        pdf["supplied_and_hash_verified"] = True
    if args.verify_pdf_extraction:
        if not args.source_pdf:
            raise ValueError("--verify-pdf-extraction requires --source-pdf")
        import pypdf
        reader = pypdf.PdfReader(args.source_pdf)
        extracted = "".join(f"\n--- PDF PAGE {i+1} ---\n" +
                            (page.extract_text() or "") + "\n"
                            for i, page in enumerate(reader.pages))
        if extracted != texts["N003"]:
            raise ValueError("Fresh PDF extraction differs from the bound transcription")
        pdf.update(extraction_replayed=True, pypdf_version=pypdf.__version__,
                   page_count=len(reader.pages), extraction_byte_identical=True)
    report = {
        "schema": "compress_A_full_body_descriptive_measurement_v1",
        "date": protocol["date"], "status": "provisional_descriptive_only",
        "protocol_sha256": digest(protocol_bytes),
        "runner_sha256": digest(Path(__file__).read_bytes()),
        "python_version": platform.python_version(),
        "unicode_database_version": unicodedata.unidata_version,
        "documents": results, "source_body_sums": totals,
        "descriptive_source_sum_divided_by_replacement": ratios,
        "optional_primary_pdf": pdf,
        "scope_diagnostic_spans": diagnostics,
        "final_principal_result_compression_ratio": None,
        "whole_document_equivalence_claim": False,
        "source_text_exported_by_runner": False,
        "interpretation": protocol["interpretation"],
    }
    with args.output.open("x", encoding="utf-8") as out:
        out.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "status": report["status"],
                      "main_body_source_sums": totals["main_body"],
                      "replacement": results["Compress_A"]["main_body"],
                      "final_compression_ratio": None}, indent=2))


if __name__ == "__main__":
    main()
