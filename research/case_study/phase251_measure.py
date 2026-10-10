"""Measure bound PDFs without exporting their text. Requires pypdf 6.13.0.

Run with --root pointing to the study directory containing the hash-bound
source PDFs in sources/. Those primary publications are not redistributed.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import unicodedata
import pypdf


def digest(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def metrics(text, form):
    normalized = unicodedata.normalize(form, text)
    collapsed = " ".join(normalized.split())
    return {
        "whitespace_tokens": len(collapsed.split()),
        "alphanumeric_units": len(re.findall(r"[^\W_]+", normalized)),
        "characters_without_whitespace": sum(not c.isspace() for c in normalized),
        "characters_with_collapsed_whitespace": len(collapsed),
        "utf8_bytes_with_collapsed_whitespace": len(collapsed.encode()),
        "collapsed_text_sha256": digest(collapsed.encode()),
    }


def selected(raw, binding):
    intervals = binding["included_spans"]
    furniture = binding["excluded_furniture"]
    for spans in (intervals, furniture):
        previous = -1
        for span in spans:
            a, b = span["start"], span["end"]
            require(0 <= a < b <= len(raw) and a >= previous, "invalid/overlapping interval")
            require(digest(raw[a:b].encode()) == span["sha256"], "span hash changed")
            previous = b
    for f in furniture:
        require(any(s["start"] <= f["start"] < f["end"] <= s["end"] for s in intervals),
                "excluded furniture outside selected intervals")
    pieces = []
    for span in intervals:
        at = span["start"]
        for f in furniture:
            if span["start"] <= f["start"] < f["end"] <= span["end"]:
                pieces.append(raw[at:f["start"]])
                at = f["end"]
        pieces.append(raw[at:span["end"]])
    return "\n".join(pieces)


def measure(root):
    config_path = root / "phase251_boundaries.json"
    config = json.loads(config_path.read_text())
    require(pypdf.__version__ == config["pypdf_version"], "pypdf version mismatch")
    require(digest((root / "phase251_protocol.md").read_bytes()) == config["protocol_sha256"],
            "protocol hash changed")
    costs = {}
    texts = {}
    for key, binding in (config["sources"] | config["ours"]).items():
        pdf = root / binding["path"]
        require(digest(pdf.read_bytes()) == binding["pdf_sha256"], key + " PDF changed")
        pages = [p.extract_text() or "" for p in pypdf.PdfReader(pdf).pages]
        require(len(pages) == binding["pages"], key + " page count changed")
        raw = "\n".join(pages)
        require(digest(raw.encode()) == binding["extraction_sha256"], key + " extraction changed")
        at = 0
        for i, (page, bound) in enumerate(zip(pages, binding["page_bindings"])):
            require(bound == {"page": i + 1, "start": at, "end": at + len(page),
                              "sha256": digest(page.encode())}, key + " page binding changed")
            at += len(page) + 1
        texts[key] = selected(raw, binding)
        costs[key] = {form: metrics(texts[key], form) for form in config["normalizations"]}
    render = config["render"]
    code = (root / render["code_path"]).read_bytes()
    require(digest(code) == render["code_sha256"], "required program changed")
    require(digest((root / render["config"]).read_bytes()) == render["config_sha256"],
            "render config changed")
    require(digest((root / "phase251_code_appendix.md").read_bytes()) == render["appendix_md_sha256"],
            "code appendix source changed")
    require(re.sub(r"\s+", "", code.decode()) in re.sub(r"\s+", "", texts["Code"]),
            "complete required code absent from counted appendix")
    comparisons = {}
    for form in config["normalizations"]:
        comparisons[form] = {}
        for metric in config["metrics"]:
            c = {k: v[form][metric] for k, v in costs.items()}
            human = c["L083"] + c["L079"]
            written = c["U_E"] + c["A1"] + c["A2"]
            complete = written + c["Code"]
            comparisons[form][metric] = {
                "source_written": human, "replacement_written": written,
                "replacement_with_required_code": complete,
                "written_ratio": human / written,
                "artifact_inclusive_factor_lower_bound": human / complete,
                "conditional_L083_over_A1": c["L083"] / c["A1"],
                "conditional_L079_over_A2": c["L079"] / c["A2"],
                "source_written_cumulative": [c["L083"], human],
                "replacement_written_cumulative": [c["U_E"] + c["A1"], written],
                "replacement_with_code_cumulative": [c["U_E"] + c["Code"] + c["A1"], complete],
            }
    return {
        "status": "PASS", "boundaries_sha256": digest(config_path.read_bytes()),
        "protocol_sha256": config["protocol_sha256"], "pypdf": pypdf.__version__,
        "primary": {"normalization": "NFC", "metric": config["primary_metric"]},
        "costs": costs, "comparisons": comparisons,
        "historical_required_program_cost": None,
        "classical_and_source_specific_external_input_cost": None,
        "code_complete_nonspace_check": True,
        "interpretation": "Conditional written lengths and a lower bound, not an exact full proof-cost factor.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    require(not args.out.exists(), "refusing to replace an existing report")
    result = measure(args.root)
    args.out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result["comparisons"]["NFC"]["characters_without_whitespace"], indent=2))
