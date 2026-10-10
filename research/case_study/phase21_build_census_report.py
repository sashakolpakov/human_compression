#!/usr/bin/env python3
"""Validate and package one completed phase21_kernel_census.g execution.

This does not rerun GAP or independently prove the census. It validates
the terminal log, checkpoint cardinalities, witness metadata and source
binding, and writes deterministic compressed mathematical checkpoints.
"""

from __future__ import annotations

import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import re


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--rank", type=int, choices=(3, 4, 5), required=True)
    ap.add_argument("--log", type=Path, required=True)
    ap.add_argument("--checkpoint-prefix", type=Path, required=True)
    ap.add_argument("--script", type=Path, default=Path(__file__).with_name("phase21_kernel_census.g"))
    ap.add_argument("--executed-sha256", required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()
    assert digest(args.script) == args.executed_sha256, "Executed source hash mismatch"
    raw = args.log.read_bytes().lstrip(b"\r\n")
    text = raw.decode("utf-8")
    assert "PASS: exact bounded normal-index-eight" in text
    assert "Error," not in text and "Syntax warning:" not in text
    version = re.search(r"VERSION GAP=(\S+) NQ=(\S+)", text)
    universal = re.search(r"UNIVERSAL rank=(\d+) order=(\d+) gamma3=(\d+)", text)
    result = re.search(
        r"RESULT rank=(\d+) candidates=(\d+) ordered=(\d+) selfdual=(\d+) "
        r"up_to_reversal=(\d+) actual_meets=(\d+) elapsed_ms=(\d+)", text
    )
    profile = re.search(
        r"KERNEL_PROFILE_CHECKS comparisons=(\d+) rejected=(\d+) directly_verified=(\d+)", text
    )
    assert version and universal and result and profile
    rank, candidates, ordered, fixed, dual, full_meets, elapsed_ms = map(int, result.groups())
    assert rank == args.rank == int(universal[1])
    universal_order, kernel_order = int(universal[2]), int(universal[3])
    assert universal_order // kernel_order == 2 ** (2 * rank - 1)
    assert full_meets == ordered * 4**rank
    assert int(profile[2]) + ordered == candidates
    assert int(profile[3]) == ordered and 2 * dual == ordered + fixed
    log_levels = re.findall(
        r"LEVEL index=(\d+) parents=(\d+) hyperplane_edges=(\d+) unique=(\d+) "
        r"max_coinvariant_dimension=(\d+) elapsed_ms=(\d+)", text
    )
    assert len(log_levels) == 3
    args.output_dir.mkdir(parents=True, exist_ok=True)
    stem = f"phase21_rank{rank}_census"
    log_path = args.output_dir / f"{stem}.log"
    log_path.write_bytes(raw)
    checkpoints = []
    last_keys = set()
    for depth, entry in enumerate(log_levels, start=1):
        index, parents, edges, count, dimension, milliseconds = map(int, entry)
        assert index == 2**depth
        source = Path(f"{args.checkpoint_prefix}.level{depth}.json")
        values = json.loads(source.read_text())
        keys = {tuple(v) for v in values}
        assert len(keys) == len(values) == count
        assert all(all(isinstance(x, int) and 0 < x < universal_order for x in v) for v in values)
        assert all(len(v) == kernel_order.bit_length() - 1 - depth for v in values)
        data = (json.dumps(values, separators=(",", ":")) + "\n").encode()
        target = args.output_dir / f"{stem}.level{depth}.json.gz"
        target.write_bytes(gzip.compress(data, mtime=0))
        checkpoints.append({
            "depth": depth, "index": index, "parents": parents,
            "hyperplane_edges": edges, "distinct_kernels": count,
            "max_coinvariant_dimension": dimension, "elapsed_ms": milliseconds,
            "path": target.name, "sha256": digest(target),
            "uncompressed_sha256": hashlib.sha256(data).hexdigest(),
        })
        last_keys = keys
    assert len(last_keys) == candidates
    accepted = json.loads(Path(f"{args.checkpoint_prefix}.accepted.json").read_text())
    assert len(accepted) == ordered
    accepted_keys = {tuple(row[0]) for row in accepted}
    assert len(accepted_keys) == ordered and accepted_keys <= last_keys
    type_count: Counter[tuple[int, ...]] = Counter()
    fixed_count: Counter[tuple[int, ...]] = Counter()
    class_kernel: Counter[tuple[int, tuple[int, ...]]] = Counter()
    for key, marking_type, cls, kernel_type, self_dual, facets in accepted:
        assert len(marking_type) == rank - 1
        assert all(x >= 4 and x & (x - 1) == 0 for x in marking_type)
        assert 3 <= cls <= 5 and isinstance(self_dual, bool)
        assert kernel_type in ([2, 2, 2], [2, 4], [8])
        assert len(facets) == 2 and all(1 < x < 2 ** (2 * rank + 2) for x in facets)
        typ = min(tuple(marking_type), tuple(reversed(marking_type)))
        type_count[typ] += 1
        fixed_count[typ] += self_dual
        class_kernel[cls, tuple(kernel_type)] += 1
    assert sum(fixed_count.values()) == fixed
    type_rows = []
    for typ in sorted(type_count):
        assert (type_count[typ] + fixed_count[typ]) % 2 == 0
        type_rows.append({"type": typ, "ordered": type_count[typ],
                          "selfdual": fixed_count[typ],
                          "up_to_reversal": (type_count[typ] + fixed_count[typ]) // 2})
    accepted_path = args.output_dir / f"{stem}.accepted.json"
    accepted_path.write_text(json.dumps(accepted, separators=(",", ":")) + "\n")
    report = {
        "status": "PASS", "rank": rank, "excess": 3,
        "group_order": 2 ** (2 * rank + 2),
        "universal_class_bound": 5, "universal_order": universal_order,
        "universal_gamma3_order": kernel_order,
        "versions": {"GAP": version[1], "NQ": version[2]},
        "executed_script": {"path": args.script.name, "sha256": digest(args.script)},
        "report_builder": {"path": Path(__file__).name, "sha256": digest(Path(__file__))},
        "log": {"path": log_path.name, "sha256": digest(log_path),
                "normalization": "Only initial carriage-return/newline removed"},
        "ladder": checkpoints, "candidate_kernels": candidates,
        "ordered_markings": ordered, "selfdual_markings": fixed,
        "classes_up_to_reversal": dual, "direct_actual_IP_meets": full_meets,
        "small_kernel_meets": int(profile[1]), "small_kernel_rejections": int(profile[2]),
        "elapsed_ms": elapsed_ms, "types": type_rows,
        "class_kernel_histogram": [
            {"class": c, "gamma3_invariants": k, "count": n}
            for (c, k), n in sorted(class_kernel.items())
        ],
        "accepted_witnesses": {"path": accepted_path.name, "sha256": digest(accepted_path),
            "row_schema": ["ambient canonical-pcgs binary keys", "ordered type", "class",
                           "gamma3 abelian invariants", "selfdual", "oriented facet orders"]},
        "trust_boundary": [
            "Universal nilpotent quotient computation retains GAP/NQ exact algorithms",
            "Every relative pc order is explicitly asserted to be two before key encoding",
            "Normal-kernel exhaustion uses the proved invariant index-two ladder",
            "Rejected candidates use the proved small-kernel IP criterion",
            "Every accepted quotient is independently checked with all actual parabolic meets",
            "No source census count, SmallGroups catalogue or proposed parameter pattern filters candidates",
            "This finite report alone does not prove an all-rank formula",
        ],
    }
    target = args.output_dir / f"{stem}.json"
    target.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"report": target.name, "sha256": digest(target),
                      "ordered": ordered, "up_to_reversal": dual}))


if __name__ == "__main__":
    main()
