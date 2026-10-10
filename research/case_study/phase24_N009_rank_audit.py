#!/usr/bin/env python3
"""Independent scratch replay of the N009 finite-example verification.

Optionally check the five private primary Atlas snapshots as literal data.
No author files are overwritten and no downloaded code is executed.
"""
import argparse
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


class Pre(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.active = False
        self.blocks = []
        self.buf = []

    def handle_starttag(self, tag, attrs):
        if tag == "pre":
            assert not self.active
            self.active = True
            self.buf = []

    def handle_endtag(self, tag):
        if tag == "pre":
            assert self.active
            self.blocks.append("".join(self.buf))
            self.active = False

    def handle_data(self, text):
        if self.active:
            self.buf.append(text)


def provenance(root, primary):
    library = json.loads((root / "phase24_N009_atlas_library.json").read_text())
    glines = (root / "phase24_N009_atlas_library.g").read_text().splitlines()[2:]
    assert len(library) == len(glines) == 5
    checks = []
    for row, line in zip(library, glines):
        m = re.fullmatch(r'Add\(atlas24,rec\(label:=(".*"),order:=(\d+),typ:=(\[.*\]),gens:=List\((\[.*\]),PermList\),words:=(\[.*\])\)\);;', line)
        assert m
        assert [json.loads(m[1]), int(m[2]), json.loads(m[3]), json.loads(m[4]), json.loads(m[5])] == [
            row[k] for k in ["label", "order", "type", "permutations", "relator_words"]]
        item = dict(label=row["label"], numerical_GAP_literal_verified=True)
        if primary:
            source = root / "sources" / row["primary_snapshot"]
            assert sha(source) == row["primary_sha256"]
            raw = source.read_text()
            assert re.findall(r'<span class="apa-canonical">([^<]*)</span>', raw) == [row["label"]]
            parser = Pre()
            parser.feed(raw)
            b = [b for b in parser.blocks if re.search(r"s0\s*:=\s*\(", b) and "Sym(" not in b]
            assert len(b) == 1
            for i, expected in enumerate(row["permutations"]):
                expr = re.search(rf"s{i}\s*:=\s*(.*?);;", b[0], re.S)[1]
                assert re.fullmatch(r"[\s\d,()]+", expr)
                cycles = [[int(x) for x in c.split(",")] for c in re.findall(r"\(([^()]*)\)", expr)]
                flat = [v for c in cycles for v in c]
                assert len(flat) == len(set(flat))
                perm = list(range(1, max(flat, default=0) + 1))
                for c in cycles:
                    cycle_map = dict(zip(c, c[1:] + c[:1]))
                    perm = [cycle_map.get(v, v) for v in perm]
                assert perm == expected
            fp = [b for b in parser.blocks if "FreeGroup(" in b]
            assert len(fp) == 1
            rel = re.search(r"rels\s*:=\s*\[(.*?)\]", fp[0], re.S)[1]
            words = []
            for expr in rel.split(","):
                tokens = [t.strip() for t in expr.strip().split("*")]
                assert all(re.fullmatch("s[012]", t) for t in tokens)
                words.append([int(t[1:]) + 1 for t in tokens])
            assert words == row["relator_words"]
            item.update(primary_sha256=sha(source), primary_url=row["url"],
                        canonical_name_verified=True, permutations_verified=3,
                        relators_verified=len(words))
        checks.append(item)
    return checks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--directory", type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument("--gap", default=os.environ.get("GAP") or shutil.which("gap"))
    ap.add_argument("--primary-sources", action="store_true")
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    assert args.gap
    root = args.directory.resolve()
    manifest_path = root / "phase24_N009_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    for row in manifest["original_files"] + manifest["retained_dependencies"]:
        assert sha(root / row["path"]) == row["sha256"]
    if args.primary_sources:
        for row in manifest["source_exclusions"]:
            assert sha(root / row["path"]) == row["sha256"]
    ledger = json.loads((root / "phase24_N009_coverage.json").read_text())
    expected = ["Definition 2.1", "Lemma 2.2", "Lemma 2.3", "Lemma 2.4",
                "Lemma 2.5", "Definition 2.6", "Theorem 2.7", "Lemma 2.8",
                "Lemma 3.1", "Lemma 3.2", "Corollary 3.3", "Lemma 3.4",
                "Lemma 3.5", "Theorem 3.6", "Corollary 3.7", "Theorem 3.8",
                "Example 3.9", "Definition 4.1", "Theorem 4.2", "Example 4.3",
                "Example 4.4", "Example 4.5", "Lemma 5.1", "Lemma 5.2",
                "Theorem 5.3", "Lemma 5.4", "Theorem 5.5"]
    assert [r["id"] for r in ledger["numbered_statements"]] == expected
    assert [r["id"] for r in ledger["tables"]] == [f"Table {i}" for i in range(1, 7)]
    for row in ledger["numbered_statements"] + ledger["tables"] + ledger["other_scope"]:
        for evidence in row.get("evidence", []):
            assert (root / evidence).is_file()
    inputs = ["phase24_N009_examples_check.g", "phase24_N009_atlas_library.g",
              "phase22_N009_atlas_library.g", "phase22_N009_rank3.accepted.json"]
    names = ["examples_results", "table3_matches", "table4_literal_matches",
             "example_facets", "census_matches"]
    data_checks = provenance(root, args.primary_sources)
    with tempfile.TemporaryDirectory(prefix="N009_phase24_independent_") as directory:
        scratch = Path(directory)
        for name in inputs:
            shutil.copy2(root / name, scratch / name)
        cp = subprocess.run([args.gap, "-q", "-T", inputs[0]], cwd=scratch,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            check=True, timeout=1200)
        log = cp.stdout.decode()
        terminal = "PASS raw_presentations=34 exact_IP_meets=3328; eight distinct Table3/Example3.9 target markings; all twelve Table3 assignments; Table4 literal e->c,f->a,h->c; three exhaustive Example4.5 central involutions."
        assert terminal in log
        assert not re.search(r"(^|\n)(Error,|Syntax error:|brk>)", log)
        outputs = []
        for stem in names:
            name = f"phase24_N009_{stem}.json"
            fresh = json.loads((scratch / name).read_text())
            authored = json.loads((root / name).read_text())
            assert fresh == authored
            outputs.append(dict(path=name, fresh_sha256=sha(scratch / name),
                                authored_sha256=sha(root / name), decoded_equal=True,
                                byte_identical=sha(scratch / name) == sha(root / name)))
        literal = json.loads((scratch / "phase24_N009_table4_literal_matches.json").read_text())
        assert literal == [[1, 1], [2, 2], [3, 3], [4, 4], [5, 3], [6, 1], [7, 7], [8, 3]]
        report = dict(schema_version=1, status="PASS", checker_sha256=sha(Path(__file__)),
                      author_manifest_sha256=sha(manifest_path),
                      original_hashes_verified=len(manifest["original_files"]),
                      retained_hashes_verified=len(manifest["retained_dependencies"]),
                      ledger_numbered_items_verified=27, ledger_tables_verified=6,
                      inputs=[dict(path=n, sha256=sha(root / n)) for n in inputs],
                      primary_sources_checked=args.primary_sources, data_checks=data_checks,
                      fresh_stdout=log, fresh_stdout_sha256=hashlib.sha256(cp.stdout).hexdigest(),
                      outputs=outputs, literal_table4_map=literal,
                      scope="Fresh unchanged author GAP execution and independent primary-data/literal transport checks. No independent census or proof-assistant claim.")
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(dict(status="PASS", raw_presentations=34, actual_IP_meets=3328,
                          all_outputs_byte_identical=all(x["byte_identical"] for x in outputs),
                          output_sha256=sha(args.output))))


if __name__ == "__main__":
    main()
