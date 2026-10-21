"""Acquire finite wing inputs from already reviewed census outputs."""
import ast
import hashlib
import json
from pathlib import Path
import re
import sys

if sys.flags.optimize:
    raise SystemExit("optimized Python is unsupported")

def need(p, message):
    if not p:
        raise ValueError(message)

w = Path(__file__).resolve().parent
s = w.parents[2]
small_path = s / "topic_B_L047_candidate_v2/finite_results.json"
records = s / "reboot_20261013/L071_A11_full_IP01/records.g"
stdout = w / "extract_a11.stdout"
small = json.loads(small_path.read_text())
rows = []
for kind in ("small_transitive", "primitive_markings"):
    for j, row in enumerate(small[kind]["literal_solutions"]):
        if 2 * len(row["permutations"]) > row["n"]:
            rows.append({"kind": kind, "source_index": j,
                         "n": row["n"], "id": row["id"],
                         "permutations": row["permutations"]})
need(len(rows) == 15, "wrong small census count")
matches = re.findall(r"MARKS (\d+) (\[.*?\])\s*ANCHORS", stdout.read_text(), re.S)
need(len(matches) == 4, "wrong A11 extraction count")
ids = ast.literal_eval(re.search(r"recordedMarks\[6\]:=(\[.*?\]);;", records.read_text(), re.S)[1])
large = [{"source_index": int(j) - 1, "ids": ids[int(j) - 1],
          "permutations": ast.literal_eval(text)} for j, text in matches]
payload = {"small_exceptions": rows, "a11_rank_six": large}
(w / "wing_inputs.json").write_text(json.dumps(payload, indent=2) + "\n")
pins = [{"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
         "bytes": p.stat().st_size} for p in (small_path, records, stdout)]
(w / "extraction.json").write_text(json.dumps({"inputs": pins,
    "method": "Literal one-based permutations; A11 indices and GAP extraction are retained.",
    "counts": {"small": len(rows), "a11": len(large)}}, indent=2) + "\n")
print("EXTRACTED 15 small exceptions and 4 complete A11 rank-six representatives")
