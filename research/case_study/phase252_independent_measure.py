#!/usr/bin/env python3
"""Independent arithmetic for the bound Topic E PDF comparison.

Uses pypdf directly, not the author's extraction/metric implementation.
Boundary semantics and dependency arrows require the accompanying written review.
"""
import argparse
import hashlib
import json
from pathlib import Path
import unicodedata

import pypdf


def need(condition, message):
    if not condition:
        raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def measure(text, form):
    text = unicodedata.normalize(form, text)
    collapsed = " ".join(text.split())
    runs = 0
    previous = False
    for char in text:
        current = char.isalnum()
        if current and not previous:
            runs += 1
        previous = current
    return {
        "whitespace_tokens": len(text.split()),
        "alphanumeric_units": runs,
        "characters_without_whitespace": sum(not char.isspace() for char in text),
        "characters_with_collapsed_whitespace": len(collapsed),
        "utf8_bytes_with_collapsed_whitespace": len(collapsed.encode("utf-8")),
        "collapsed_text_sha256": sha(collapsed.encode("utf-8")),
    }


def bound_text(root, document):
    path = root / document["path"]
    need(sha(path.read_bytes()) == document["pdf_sha256"], f"PDF bytes: {path}")
    reader = pypdf.PdfReader(path)
    pages = [page.extract_text() for page in reader.pages]
    need(len(pages) == document["pages"], f"page count: {path}")
    need(len(pages) == len(document["page_bindings"]), f"page bindings: {path}")
    text = "\n".join(pages)
    need(sha(text.encode()) == document["extraction_sha256"], f"extraction bytes: {path}")
    position = 0
    for index, (page, binding) in enumerate(zip(pages, document["page_bindings"]), 1):
        need(binding["page"] == index, "page order")
        need(binding["start"] == position and binding["end"] == position + len(page), "page interval")
        need(sha(page.encode()) == binding["sha256"], "individual page bytes")
        position += len(page) + 1
    included = document["included_spans"]
    removed = document["excluded_furniture"]
    for sequence in [included, removed]:
        end = 0
        for item in sequence:
            a, b = item["start"], item["end"]
            need(end <= a < b <= len(text), "unordered, overlapping or invalid interval")
            need(sha(text[a:b].encode()) == item["sha256"], "interval bytes")
            end = b
    for item in removed:
        need(any(s["start"] <= item["start"] < item["end"] <= s["end"] for s in included),
             "excluded furniture outside included material")
    pieces = []
    for item in included:
        a, b = item["start"], item["end"]
        # Character mask is independent of the author's interval-splicing code.
        pieces.append("".join(text[i] for i in range(a, b)
                              if not any(r["start"] <= i < r["end"] for r in removed)))
    return "\n".join(pieces)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--boundaries", default="phase251_boundaries.json")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    boundary_path = root / args.boundaries
    boundary = json.loads(boundary_path.read_text())
    need(pypdf.__version__ == boundary["pypdf_version"] == "6.13.0", "pinned pypdf version")
    need(sha((root / "phase251_protocol.md").read_bytes()) == boundary["protocol_sha256"], "protocol bytes")
    cleaned = {}
    for side in ["sources", "ours"]:
        for name, document in boundary[side].items():
            cleaned[name] = bound_text(root, document)
    code = (root / boundary["render"]["code_path"]).read_text()
    need(sha(code.encode()) == boundary["render"]["code_sha256"], "program bytes")
    title = "Complete finite program for the projective-line theory"
    need(cleaned["Code"].startswith(title), "program appendix title")
    actual_code = cleaned["Code"][len(title):]
    need("".join(actual_code.split()) == "".join(code.split()), "non-whitespace program content")
    metrics = {name: {form: measure(text, form) for form in ["NFC", "NFKC"]}
               for name, text in cleaned.items()}
    comparisons = {}
    for form in ["NFC", "NFKC"]:
        comparisons[form] = {}
        for metric in boundary["metrics"]:
            costs = {name: data[form][metric] for name, data in metrics.items()}
            old = costs["L083"] + costs["L079"]
            written = costs["U_E"] + costs["A1"] + costs["A2"]
            complete = written + costs["Code"]
            comparisons[form][metric] = {
                "costs": costs,
                "historical_written_total": old,
                "replacement_written_total": written,
                "replacement_with_required_program": complete,
                "written_ratio": old / written,
                "artifact_factor_lower_bound": old / complete,
                "conditional_local_factors": {
                    "L083_over_A1": costs["L083"] / costs["A1"],
                    "L079_over_A2": costs["L079"] / costs["A2"],
                },
            }
    report = {
        "status": "independent_arithmetic_pass_semantic_review_separate",
        "pypdf_version": pypdf.__version__,
        "boundary_sha256": sha(boundary_path.read_bytes()),
        "program_nonwhitespace_equal": True,
        "metrics": metrics,
        "comparisons": comparisons,
        "scope": "Same bound primary spans and complete replacement PDFs; no theorem admission by these counts.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "primary": comparisons["NFC"]["characters_without_whitespace"]}, indent=2))


if __name__ == "__main__":
    main()
