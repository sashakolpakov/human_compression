#!/usr/bin/env python3
"""Independent phase144 representation audit; no author helper imports.

Public mode recounts the denominator and arithmetic from bound source counts.
--primary independently re-extracts and counts the six exact private PDFs.
"""
import argparse
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import unicodedata

MANIFEST_SHA = "0ecc2b506828b1ddfe7ba55ea4460b9a0cdc891b8b9030665ccfc7c31feb6333"


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def counts(text, form):
    # State transitions, rather than the author's regex/split-length counter.
    text = unicodedata.normalize(form, text)
    tokens = runs = chars = 0
    previous_space, previous_alnum = True, False
    for char in text:
        space, alnum = char.isspace(), char.isalnum()
        tokens += int(previous_space and not space)
        runs += int(alnum and not previous_alnum)
        chars += int(not space)
        previous_space, previous_alnum = space, alnum
    collapsed = " ".join(text.split())
    require(len(collapsed) == chars + max(0, tokens - 1), "Collapse arithmetic")
    return {"unicode_normalization": form, "whitespace_tokens": tokens,
            "alphanumeric_units": runs, "characters_without_whitespace": chars,
            "characters_with_collapsed_whitespace": len(collapsed),
            "utf8_bytes_with_collapsed_whitespace": len(collapsed.encode()),
            "collapsed_text_sha256": digest(collapsed.encode())}


def nodes(value, kind):
    result = []
    pending = [value]
    while pending:
        item = pending.pop()
        if isinstance(item, dict):
            if item.get("t") == kind:
                result.append(item["c"])
            pending.extend(reversed(list(item.values())))
        elif isinstance(item, list):
            pending.extend(reversed(item))
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument("--primary", action="store_true")
    ap.add_argument("--render-dir", type=Path,
                    help="Optional separate fresh renderer output; otherwise use bound exported PDF")
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    require(not os.path.lexists(args.output), "Fresh output required")
    root = args.root.resolve()
    manifest_bytes = (root / "phase144_manifest.json").read_bytes()
    require(digest(manifest_bytes) == MANIFEST_SHA, "Frozen author manifest changed")
    manifest = json.loads(manifest_bytes)
    bindings = manifest["files"] + manifest["required_shared_inputs"]
    for item in bindings:
        data = (root / item["path"]).read_bytes()
        require(len(data) == item["bytes"] and digest(data) == item["sha256"],
                "Bound input changed: " + item["path"])
    protocol = json.loads((root / "phase144_measurement_protocol.json").read_text())
    author = json.loads((root / "phase144_render/report.json").read_text())
    old = json.loads((root / "phase98_twelve_measurement_protocol.json").read_text())
    for key in protocol["inherited_source_keys"]:
        require(protocol["documents"][key] == old["documents"][key], "Inherited cut changed")
    import pypdf
    require(pypdf.__version__ == "6.13.0", "pypdf version differs")
    directory = args.render_dir.resolve() if args.render_dir else root / "phase144_render"
    pdf = pypdf.PdfReader(directory / "replacement.pdf")
    extracted = "\n".join(page.extract_text() or "" for page in pdf.pages)
    require(len(pdf.pages) == 65, "Replacement page count")
    require(digest(extracted.encode()) == protocol["expected"]["extraction_sha256"],
            "Replacement extraction differs")
    denominator = {form: counts(extracted, form) for form in protocol["forms"]}
    require(denominator == protocol["expected"]["metrics"], "Denominator differs")
    unwrapped = (directory / "replacement.md").read_text()
    manuscript_texts = [(root / item["path"]).read_text()
                        for item in protocol["replacement_manuscripts"]]
    require(unwrapped.startswith("\n\n".join(manuscript_texts) + "\n\n"),
            "Complete U and A prefix absent")
    require(all(unwrapped.count(text) == 1 for text in manuscript_texts),
            "Manuscript omitted or duplicated")
    old_ast = json.loads((directory / "replacement.json").read_text())
    new_ast = json.loads((directory / "render.json").read_text())
    ast_counts = {}
    for kind in ["Math", "Table"]:
        before, after = nodes(old_ast, kind), nodes(new_ast, kind)
        require(before == after, "Changed mathematical AST: " + kind)
        ast_counts[kind] = len(before)
    original, displayed = nodes(old_ast, "CodeBlock"), nodes(new_ast, "CodeBlock")
    wrap = json.loads((directory / "code_display_wrap.json").read_text())
    require(len(original) == len(displayed) == len(wrap) == 5, "Code block count")
    for before, after, instruction in zip(original, displayed, wrap):
        lines = after[1].split("\n")
        require(all(len(line) <= 64 for line in lines), "Excess display width")
        rebuilt, offset = [], 0
        for number in instruction["original_line_chunk_counts"]:
            require(number >= 1, "Invalid wrap count")
            rebuilt.append("".join(lines[offset:offset + number]))
            offset += number
        require(offset == len(lines) and "\n".join(rebuilt) == before[1]
                and before[0] == after[0], "Display is not reversible")
        require(digest(before[1].encode()) == instruction["original_sha256"]
                and digest(after[1].encode()) == instruction["wrapped_sha256"],
                "Code display-map hash")
    appendix = extracted.rsplit("Complete computational proof appendix", 1)
    require(len(appendix) == 2, "Printed appendix absent")
    appendix = appendix[1]
    programs = protocol["certificate_programs"]
    heads = ["\n" + item["path"] + "\n" for item in programs]
    positions = [appendix.index(head) for head in heads]
    require(positions == sorted(positions), "Printed program order")
    program_checks = []
    for i, item in enumerate(programs):
        raw = (root / item["path"]).read_text()
        require(original[i + 1][1] + "\n" == raw, "Incomplete executable AST")
        start = positions[i] + len(heads[i])
        end = positions[i + 1] if i + 1 < len(programs) else len(appendix)
        actual = "".join(c for c in appendix[start:end] if not c.isspace())
        expected = "".join(c for c in raw if not c.isspace())
        require(actual == expected, "Actual PDF loses code: " + item["path"])
        program_checks.append({"path": item["path"], "original_bytes": len(raw.encode()),
                               "printed_nonspace_characters": len(actual),
                               "printed_nonspace_sha256": digest(actual.encode())})
    sources, source_boundaries = {}, []
    for key in protocol["source_keys"]:
        spec = protocol["documents"][key]
        if not args.primary:
            sources[key] = author["source_documents"][key]["metrics"]
            continue
        primary = root / spec["pdf_path"]
        require(digest(primary.read_bytes()) == spec["pdf_sha256"]
                and primary.stat().st_size == spec["pdf_bytes"], "Primary changed: " + key)
        pages = [page.extract_text() or "" for page in pypdf.PdfReader(primary).pages]
        full = "\n".join(pages)
        require(len(pages) == spec["pages"]
                and digest(full.encode()) == spec["extraction_sha256"], "Primary extraction")
        for page, span in zip(pages, spec["page_spans"]):
            lo, hi = span["start_codepoint"], span["end_codepoint_exclusive"]
            require(full[lo:hi] == page and digest(page.encode()) == span["sha256_utf8"],
                    "Primary page span")
        body_spec = spec["body"]
        start, end = body_spec["start_codepoint"], body_spec["end_codepoint_exclusive"]
        require(0 <= start <= end <= len(full)
                and digest(full[start:end].encode()) == body_spec["sha256_utf8"], "Body span")
        masked = list(full[start:end])
        last = start
        for cut in sorted(spec["exclusions"], key=lambda x: x["start_codepoint"]):
            lo, hi = cut["start_codepoint"], cut["end_codepoint_exclusive"]
            require(last <= lo < hi <= end and lo >= start, "Invalid exclusion")
            require(digest(full[lo:hi].encode()) == cut["sha256_utf8"], "Exclusion hash")
            masked[lo - start] = " "
            for j in range(lo + 1 - start, hi - start):
                masked[j] = ""
            last = hi
        body = "".join(masked)
        sources[key] = {form: counts(body, form) for form in protocol["forms"]}
        require(sources[key] == author["source_documents"][key]["metrics"],
                "Independent primary count differs: " + key)
        source_boundaries.append({"source": key, "pdf_sha256": spec["pdf_sha256"],
                                  "pages": len(pages), "body_start": start, "body_end": end,
                                  "exclusions": len(spec["exclusions"]),
                                  "cleaned_body_sha256": digest(body.encode())})
    totals, ratios = {}, {}
    for form in protocol["forms"]:
        totals[form], ratios[form] = {}, {}
        for metric in protocol["metric_keys"]:
            num = sum(sources[key][form][metric] for key in protocol["source_keys"])
            den = denominator[form][metric]
            value = Fraction(num, den)
            totals[form][metric] = num
            ratios[form][metric] = {"numerator": num, "denominator": den,
                                   "reduced_fraction": str(value), "factor": float(value)}
    require(totals == author["source_body_sums"], "Source sum differs")
    raster_count = None
    if args.render_dir:
        fresh = json.loads((directory / "report.json").read_text())
        require(fresh["rendering"]["raster_sha256"] == author["rendering"]["raster_sha256"],
                "Fresh raster map differs")
        for name, value in fresh["rendering"]["raster_sha256"].items():
            require(digest((directory / name).read_bytes()) == value, "Fresh raster changed")
        raster_count = len(fresh["rendering"]["raster_sha256"])
        require(raster_count == 65, "Incomplete raster map")
    result = {"status": "PASS", "checker_sha256": digest(Path(__file__).read_bytes()),
              "author_manifest_sha256": MANIFEST_SHA, "checked_bindings": len(bindings),
              "author_helpers_imported": False, "primary_sources_freshly_counted": args.primary,
              "source_metrics": sources, "source_boundaries": source_boundaries,
              "source_sums": totals, "denominator": denominator, "ratios": ratios,
              "replacement_pdf_sha256": digest((directory / "replacement.pdf").read_bytes()),
              "replacement_extraction_sha256": digest(extracted.encode()),
              "replacement_pages": len(pdf.pages), "Math_Table_nodes_preserved": ast_counts,
              "five_code_blocks_reversible": True, "whole_U_A_prefix_checked": True,
              "complete_programs": program_checks, "fresh_rasters_checked": raster_count,
              "private_primary_text_or_images_exported": False,
              "new_mathematical_replay_or_ratio_from_page_counts": False}
    with args.output.open("x") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(json.dumps({"status": "PASS", "primary": args.primary,
                      "NFC": ratios["NFC"], "rasters": raster_count}))


if __name__ == "__main__":
    main()
