#!/usr/bin/env python3
"""Independent replay and primary-data audit of the frozen N009 label adapter.

Run against the private source directory to audit HTML provenance as well.
No downloaded code is executed. All GAP reruns use a disposable directory.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class PreBlocks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.blocks = []
        self.current = []

    def handle_starttag(self, tag, attrs):
        if tag == "pre":
            assert self.depth == 0
            self.depth = 1
            self.current = []

    def handle_endtag(self, tag):
        if tag == "pre":
            assert self.depth == 1
            self.blocks.append("".join(self.current))
            self.depth = 0

    def handle_data(self, data):
        if self.depth:
            self.current.append(data)


def source_check(root):
    counts = dict(markings=0, generators=0, cycles=0, relators=0,
                  overlapping_generator_cycles=0)
    sources = []
    for stem, rank, variable in [("atlas", 3, "atlas22"),
                                 ("atlas4", 4, "atlas4_22")]:
        name = f"phase22_N009_{stem}_library"
        library = json.loads((root / (name + ".json")).read_text())
        glines = (root / (name + ".g")).read_text().splitlines()[2:]
        assert len(glines) == len(library)
        for entry, gline in zip(library, glines):
            # Independently read the numerical GAP literal, without eval.
            pat = (r"Add\(" + variable +
                   r",rec\(label:=(\".*\"),order:=(\d+),typ:=(\[.*\]),"
                   r"gens:=List\((\[.*\]),PermList\),words:=(\[.*\])\)\);;")
            m = re.fullmatch(pat, gline)
            assert m
            assert [json.loads(m[1]), int(m[2]), json.loads(m[3]),
                    json.loads(m[4]), json.loads(m[5])] == [
                entry[k] for k in ["label", "order", "type", "permutations",
                                   "relator_words"]]
            source = root / "sources" / entry["primary_snapshot"]
            assert sha(source) == entry["primary_sha256"]
            raw_html = source.read_text()
            canonical = re.findall(r'<span class="apa-canonical">([^<]*)</span>', raw_html)
            assert canonical == [entry["label"]]
            parser = PreBlocks()
            parser.feed(raw_html)
            permutation_blocks = [b for b in parser.blocks
                                  if re.search(r"s0\s*:=\s*\(", b)
                                  and "Sym(" not in b]
            assert len(permutation_blocks) == 1
            b = permutation_blocks[0]
            for i, expected in enumerate(entry["permutations"]):
                expr = re.search(rf"s{i}\s*:=\s*(.*?);;", b, re.S)[1]
                assert re.fullmatch(r"[\s\d,()]+", expr)
                cycles = [[int(t) for t in c.split(",")]
                          for c in re.findall(r"\(([^()]*)\)", expr)]
                degree = max([v for c in cycles for v in c], default=0)
                seen = set()
                perm = list(range(1, degree + 1))
                for c in cycles:
                    assert len(c) == len(set(c))
                    if seen.intersection(c):
                        counts["overlapping_generator_cycles"] += 1
                    seen.update(c)
                    cycle_map = dict(zip(c, c[1:] + c[:1]))
                    # Genuine permutation composition, rather than assigning
                    # images under an unverified disjoint-cycle assumption.
                    perm = [cycle_map.get(v, v) for v in perm]
                assert perm == expected
                counts["generators"] += 1
                counts["cycles"] += len(cycles)
            fp = [b for b in parser.blocks if "FreeGroup(" in b]
            assert len(fp) == 1
            rel = re.search(r"rels\s*:=\s*\[(.*?)\]", fp[0], re.S)[1]
            words = []
            for word in rel.split(","):
                tokens = word.strip().split("*")
                assert all(re.fullmatch(r"s[0-9]+", t.strip()) for t in tokens)
                parsed = [int(t.strip()[1:]) + 1 for t in tokens]
                assert all(1 <= x <= rank for x in parsed)
                words.append(parsed)
            assert words == entry["relator_words"]
            counts["markings"] += 1
            counts["relators"] += len(words)
            sources.append(dict(label=entry["label"], url=entry["url"],
                                sha256=sha(source)))
    assert counts["overlapping_generator_cycles"] == 0
    return dict(status="PASS", counts=counts, primary_sources=sources,
                scope="Independent HTML parser, composed permutations, literal relator words, and JSON-to-GAP data identity.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--directory", type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument("--gap", default=os.environ.get("GAP") or shutil.which("gap"))
    ap.add_argument("--primary-sources", action="store_true")
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    assert args.gap
    root = args.directory.resolve()
    manifest_path = root / "phase22_N009_table_labels_manifest.json"
    manifest = json.loads(manifest_path.read_text())
    for row in manifest["original_files"] + manifest["retained_dependencies"]:
        assert sha(root / row["path"]) == row["sha256"], row
    provenance = source_check(root) if args.primary_sources else None
    # Bind the transported prior census and all input presentation row lists.
    accepted = json.loads((root / "phase21_rank4_census.accepted.json").read_text())
    literal = (root / "phase22_N009_facet_input.g").read_text().strip()
    assert json.loads(literal[len("accepted22:="):-2]) == accepted
    rows = json.loads((root / "phase22_N009_table6_rows.json").read_text())
    for rank, name, variable in [(4, "universal_input", "rows22"),
                                 (5, "universal5_input", "rows5_22")]:
        literal = (root / f"phase22_N009_{name}.g").read_text().strip()
        expected = [[r["labels"], int(r["universal_order"])] for r in rows
                    if len(r["type"]) == rank - 1 and r["universal_order"] != "∞"]
        assert json.loads(literal[len(variable) + 2:-2]) == expected
    scripts = ["facet_check", "rank5_labels_check", "universal_check", "universal5_check"]
    generated = ["facet_matches", "atlas_duals", "rank5_facet_matches",
                 "rank4_atlas_duals", "universal_orders", "atlas_presentation_orders",
                 "universal5_orders", "atlas4_presentation_orders"]
    with tempfile.TemporaryDirectory(prefix="N009_independent_") as tmp:
        scratch = Path(tmp)
        for row in manifest["original_files"]:
            path = root / row["path"]
            if path.suffix == ".g" or path.name in ["phase22_N009_table6_rows.json",
                                                     "phase22_N009_table_compare.py"]:
                shutil.copy2(path, scratch / path.name)

        def run(stem):
            filename = f"phase22_N009_{stem}.g"
            cp = subprocess.run([args.gap, "-q", "-T", filename], cwd=scratch,
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                check=True)
            output = cp.stdout.decode()
            assert "PASS" in output and "Error," not in output, output[-3000:]
            print(stem + ": " + output.splitlines()[-1], flush=True)
            return dict(script=filename, script_sha256=sha(root / filename),
                        stdout_sha256=hashlib.sha256(cp.stdout).hexdigest(),
                        stdout=output)

        with ThreadPoolExecutor(max_workers=4) as pool:
            runs = list(pool.map(run, scripts))
        outputs = []
        for stem in generated:
            name = f"phase22_N009_{stem}.json"
            assert json.loads((scratch / name).read_text()) == json.loads((root / name).read_text())
            outputs.append(dict(path=name, fresh_sha256=sha(scratch / name),
                                authored_sha256=sha(root / name),
                                decoded_equal=True,
                                byte_identical=sha(scratch / name) == sha(root / name)))
        cmd = ["python3", "phase22_N009_table_compare.py", "--directory", str(scratch),
               "--output", str(scratch / "comparison.json")]
        if args.primary_sources:
            cmd.extend(["--source-text", str(root / "sources" / "phase17_gomi_loyola2018.txt")])
        cp = subprocess.run(cmd, cwd=scratch, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, check=True)
        comparison = json.loads((scratch / "comparison.json").read_text())
        assert comparison["rank4"]["classes"] == 105
        assert comparison["rank5"]["classes"] == 8
        report = dict(schema_version=1, status="PASS", checker_sha256=sha(Path(__file__)),
                      author_manifest_sha256=sha(manifest_path),
                      manifest_original_hashes_verified=len(manifest["original_files"]),
                      retained_dependency_hashes_verified=len(manifest["retained_dependencies"]),
                      provenance=provenance, fresh_gap_runs=runs, generated_outputs=outputs,
                      fresh_source_table_comparison=comparison,
                      scope="Fresh execution of the four unchanged author GAP checkers, independent primary-data parsing when requested, and exact row comparison. This is not an independent rank-four exhaustive census, and does not reprove the retained infinite decomposition.")
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(dict(status="PASS", output=args.output.name,
                          sha256=sha(args.output), all_generated_bytes_identical=all(x["byte_identical"] for x in outputs))))


if __name__ == "__main__":
    main()
