#!/usr/bin/env python3
"""Independent rightmost-rewrite check of the printed label-eight presentation.

No author collector, nilpotent quotient, or group library is imported.
The all-rank implication remains the separate termination/locality proof.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import time


def require(value, message):
    if not value:
        raise RuntimeError(message)


def presentation(rank):
    letters = [(kind, i) for kind, length in (("r", 1), ("x", 2),
               ("y", 3), ("z", 4), ("w", 2))
               for i in range(rank - length + 1)]
    index = {letter: i for i, letter in enumerate(letters)}
    correction = {}

    def record(b, a, *tail):
        if b not in index or a not in index:
            return
        require(all(x in index for x in tail), "Nonexistent output letter")
        require(index[b] > index[a], "Wrong orientation in printed table")
        pair = (index[b], index[a])
        require(pair not in correction, "Duplicated nontrivial rule")
        correction[pair] = tuple(index[x] for x in tail)

    for i in range(rank):
        record(("r", i+1), ("r", i), ("x", i), ("w", i))
        record(("x", i), ("r", i), ("w", i))
        record(("x", i), ("r", i+1), ("w", i))
        record(("x", i), ("r", i+2), ("y", i))
        record(("x", i), ("r", i-1), ("y", i-1), ("w", i-1), ("w", i))
        record(("x", i+1), ("x", i), ("w", i), ("w", i+1))
        record(("x", i+2), ("x", i), ("z", i))
        record(("y", i), ("r", i-1), ("z", i-1))
        record(("y", i), ("r", i+1), ("w", i), ("w", i+1))
        record(("y", i), ("r", i+3), ("z", i))
    rules = {(j, i): (i, j) + correction.get((j, i), ())
             for j in range(len(letters)) for i in range(j)}
    for j, (kind, i) in enumerate(letters):
        rules[j, j] = (index["w", i],) if kind == "x" else ()
    lengths = {"r": 1, "x": 2, "y": 3, "z": 4, "w": 2}
    supports = [set(range(i, i + lengths[kind])) for kind, i in letters]
    for (j, i), rhs in rules.items():
        tail = rhs if j == i else rhs[2:]
        require(all(k > j for k in tail), "Nontriangular correction")
        require(all(supports[k] <= supports[i] | supports[j] for k in rhs),
                "Support union not preserved")
    return letters, index, rules


def reduce_rightmost(word, rules):
    word = tuple(word)
    while True:
        for k in range(len(word)-2, -1, -1):
            if word[k] >= word[k+1]:
                word = word[:k] + rules[word[k], word[k+1]] + word[k+2:]
                break
        else:
            return word


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    require(not args.report.exists() and not args.report.is_symlink(), "Fresh report required")
    start = time.monotonic()
    letters, index, rules = presentation(14)
    digest = hashlib.sha256()
    count = 0
    for c, b, a in itertools.combinations_with_replacement(range(len(letters)), 3):
        left = reduce_rightmost(rules[a, b] + (c,), rules)
        right = reduce_rightmost((a,) + rules[b, c], rules)
        require(left == right, "Nonjoinable critical pair")
        digest.update(json.dumps([a, b, c, left], separators=(",", ":")).encode() + b"\n")
        count += 1
    require((len(letters), len(rules), count) == (63, 2016, 43680), "Incomplete finite check")
    local, ix, local_rules = presentation(3)
    A = (ix["r", 0], ix["r", 1])
    B = (ix["r", 1], ix["r", 2])
    expected = [[], [("r",0),("r",2),("x",0),("x",1),("y",0),("w",1)],
                [("x",0),("x",1),("w",0),("w",1)],
                [("r",0),("r",2),("w",0),("w",1)], [("w",0),("w",1)],
                [("r",0),("r",2),("x",0),("x",1),("y",0),("w",0)],
                [("x",0),("x",1)], [("r",0),("r",2)]]
    source_rows = []
    for k in range(8):
        value = reduce_rightmost(B*k + A*k, local_rules)
        require([local[j] for j in value] == expected[k], "Printed normal-form table differs")
        require(reduce_rightmost(value*2, local_rules) == (), "Source power word fails")
        source_rows.append({"k": k, "normal_form": [local[j] for j in value], "square": []})
    for i in range(2):
        edge = (ix["r",i], ix["r",i+1])
        require(reduce_rightmost(edge*2, local_rules) == (ix["x",i],), "Edge square")
        require(reduce_rightmost(edge*4, local_rules) == (ix["w",i],), "Edge fourth power")
        require(reduce_rightmost(edge*8, local_rules) == (), "Edge eighth power")
    report = {"status": "PASS", "rank": 14, "letters": len(letters), "rules": len(rules),
              "overlapping_critical_pairs": count, "critical_normal_forms_sha256": digest.hexdigest(),
              "source_rows": source_rows, "exact_adjacent_order_eight": True,
              "normalization_strategy": "rightmost reducible pair; no author imports",
              "scope": "Finite critical-pair and local-word check; uniform transfer is a separate written proof",
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "seconds": time.monotonic()-start}
    with args.report.open("x") as output:
        json.dump(report, output, indent=2)
        output.write("\n")
    print(json.dumps({key: value for key, value in report.items() if key != "source_rows"}, indent=2))


if __name__ == "__main__":
    main()
