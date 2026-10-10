#!/usr/bin/env python3
"""Measure a frozen pair of matched proof descriptions without bundling source text.

Requires pypdf==6.13.0 and a user-supplied primary PDF with the protocol's
SHA-256. The JSON output contains counts, locators and hashes, never source
proof text. This measures description length, not mathematical difficulty.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import unicodedata
import pypdf


def sha(data):
    return hashlib.sha256(data).hexdigest()


def normalize(text):
    text = unicodedata.normalize("NFKC", text).replace("\u00ad", "")
    patterns = [
        r"^--- PDF PAGE \d+ ---[ \t]*$",
        r"^\d+ KIEFER AND LEEMANS[ \t]*$",
        r"^ON PAIRS OF COMMUTING INVOLUTIONS IN Sym\(n\) AND Alt\(n\) \d+[ \t]*$",
    ]
    for pattern in patterns:
        text = re.sub(pattern, "", text, flags=re.MULTILINE)
    return text


def metrics(raw):
    text = normalize(raw)
    return {
        "normalized_nonwhitespace_codepoints": sum(not c.isspace() for c in text),
        "unicode_alphanumeric_tokens": len(re.findall(r"[^\W_]+", text)),
        "raw_utf8_bytes": len(raw.encode()),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    here = Path(__file__).resolve().parent
    parser.add_argument("--source-pdf", required=True, type=Path)
    parser.add_argument("--protocol", type=Path, default=here / "phase9_L066_measurement_protocol.json")
    parser.add_argument("--output", type=Path, default=here / "phase9_L066_measurement.json")
    args = parser.parse_args()
    protocol = json.loads(args.protocol.read_text())
    source = protocol["source"]
    assert pypdf.__version__ == source["pypdf_version"], "extractor version differs"
    assert sha(args.source_pdf.read_bytes()) == source["pdf_sha256"], "primary PDF differs"
    reader = pypdf.PdfReader(args.source_pdf)
    assert len(reader.pages) == source["pdf_pages"]
    text = "".join("\n--- PDF PAGE " + str(i + 1) + " ---\n" + (page.extract_text() or "") + "\n"
                   for i, page in enumerate(reader.pages))
    assert sha(text.encode()) == source["extracted_text_sha256"], "extraction differs"
    replacement_file = args.protocol.parent / protocol["replacement"]["file"]
    replacement_text = replacement_file.read_text()
    assert sha(replacement_file.read_bytes()) == protocol["replacement"]["sha256"]

    selected = {}
    for side, full_text in [("source", text), ("replacement", replacement_text)]:
        spans = protocol[side]["spans"]
        ranges = sorted((r["start_codepoint"], r["end_codepoint_exclusive"]) for r in spans)
        assert all(a < b <= len(full_text) for a, b in ranges)
        assert all(ranges[i][1] <= ranges[i + 1][0] for i in range(len(ranges) - 1)), "overlapping spans"
        selected[side] = []
        for row in spans:
            raw = full_text[row["start_codepoint"]:row["end_codepoint_exclusive"]]
            assert sha(raw.encode()) == row["raw_span_sha256"], row["id"]
            selected[side].append({"id": row["id"], "role": row["role"], "targets": row["targets"],
                                   "included_in_primary": row.get("included_in_primary", True),
                                   "locator": row["locator"], "metrics": metrics(raw),
                                   "raw_span_sha256": row["raw_span_sha256"]})

    metric_names = list(selected["source"][0]["metrics"])

    def total(side, allowed_ids=None, include_optional=False):
        rows = [r for r in selected[side] if include_optional or r["included_in_primary"]]
        if allowed_ids is not None:
            rows = [r for r in rows if r["id"] in allowed_ids]
        return {m: sum(r["metrics"][m] for r in rows) for m in metric_names}

    def comparison(source_values, replacement_values):
        return {m: {"source": source_values[m], "replacement": replacement_values[m],
                    "ratio": source_values[m] / replacement_values[m]}
                for m in metric_names}

    totals = comparison(total("source"), total("replacement"))
    marginal = []
    seen = {"source": set(), "replacement": set()}
    for target in protocol["accounting"]["marginal_order"]:
        new = {}
        for side in seen:
            ids = {r["id"] for r in selected[side] if target in r["targets"] and r["included_in_primary"]}
            new[side] = ids - seen[side]
            seen[side].update(ids)
        marginal.append({"target_added": target, "new_span_ids": {k: sorted(v) for k, v in new.items()},
                         "increment": comparison(total("source", new["source"]), total("replacement", new["replacement"])),
                         "cumulative": comparison(total("source", seen["source"]), total("replacement", seen["replacement"]))})
    assert all(seen[side] == {r["id"] for r in selected[side] if r["included_in_primary"]} for side in seen)
    main_metric = totals["normalized_nonwhitespace_codepoints"]
    supporting_files = [Path(__file__), args.protocol]
    report = {
        "status": "PASS", "measured_at_utc": datetime.now(timezone.utc).isoformat(),
        "protocol_sha256": sha(args.protocol.read_bytes()),
        "script_sha256": sha(Path(__file__).read_bytes()), "pypdf_version": pypdf.__version__,
        "targets": protocol["targets"], "source_pdf_sha256": source["pdf_sha256"],
        "replacement_sha256": protocol["replacement"]["sha256"],
        "conditional_on_common_background": protocol["common_background_B"],
        "selected_spans": selected, "totals": totals, "marginal_in_order": marginal,
        "source_span_sensitivity": {
            "interpretation": "Including the source's optional Proposition4.1 exposition; its order formula is unnecessary for these targets",
            "including_optional_source_span": comparison(total("source", include_optional=True), total("replacement")),
        },
        "shared_background_sensitivity": {
            "interpretation": "Illustrative equal added background costs, not measured estimates of background proof length",
            "metric": "normalized_nonwhitespace_codepoints",
            "scenarios": [{"added_to_each_side": b, "ratio": (main_metric["source"] + b) / (main_metric["replacement"] + b)}
                          for b in [0, 1000, 10000, 100000]],
        },
        "separate_artifact_costs": {
            "replacement_full_file_utf8_bytes": len(replacement_file.read_bytes()),
            "replacement_unmeasured_exposition_utf8_bytes": len(replacement_file.read_bytes()) - total("replacement")["raw_utf8_bytes"],
            "measurement_infrastructure_utf8_bytes": {x.name: len(x.read_bytes()) for x in supporting_files},
            "mathematical_algorithm_or_certificate_bytes_required_for_this_proof": 0,
            "runtime_or_search_comparison": "Not measured; neither target proof relies on an exhaustive computation",
        },
        "limitations": protocol["limitations"],
    }
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({"status": "PASS", "totals": totals, "report": args.output.name}, indent=2))


if __name__ == "__main__":
    main()
