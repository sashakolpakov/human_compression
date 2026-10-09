"""Repeat the lexical open-problem audit over identified full texts only.

This is a retrieval aid, not a claim that no other open problem occurs in a paper.
It deliberately records false-positive bibliography and already-resolved hits.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
PATTERN = r"conjectur|open problem|open question|remains? (?:open|unknown|to)|not (?:yet )?known|unknown|future work|problem\s+\d|question\s+\d|\?|we do not know|we did not (?:find|investigate)|most likely"


def main():
    inventory = json.loads((ROOT / "literature_inventory.json").read_text())
    regex = re.compile(PATTERN, re.I)
    records = []
    for entry in inventory["entries"]:
        if not entry["fulltext_available"]:
            continue
        asset = entry["assets"][0]
        source = ROOT / asset["filename"]
        text_file = source.with_suffix(".txt")
        if source.suffix == ".html":
            text = BeautifulSoup(source.read_text(), "html.parser").get_text("\n", strip=True)
        else:
            text = text_file.read_text(errors="replace")
        lines = text.splitlines()
        hits = []
        for index, line in enumerate(lines):
            if regex.search(line):
                hits.append({"line": index + 1, "text": line.strip(),
                             "context": " ".join(lines[max(0, index - 1):index + 3]).strip()})
        records.append({"id": entry["id"], "title": entry["title"],
                        "fulltext_sha256": asset["sha256"],
                        "text_filename": str(text_file.relative_to(ROOT)) if text_file.exists() else asset["filename"],
                        "text_sha256": hashlib.sha256(text.encode()).hexdigest(), "hits": hits,
                        "caveat": "Lexical search can miss unstated questions, unusual phrasing, formulas and OCR errors. Hits may be bibliography entries or resolved problems. This is not a proof-by-proof reading."})
    output = {"as_of": inventory["as_of"], "pattern": PATTERN, "records": records}
    (ROOT / "fulltext_open_problem_hits.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    print(f"Searched {len(records)} identified full texts; {sum(len(x['hits']) for x in records)} candidate contexts.")


if __name__ == "__main__":
    main()
