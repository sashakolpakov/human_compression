#!/usr/bin/env python3
"""Recount a saved exact transition graph and derive its proved eventual polynomial."""
import argparse
from collections import defaultdict
from fractions import Fraction
import hashlib
import heapq
import json
from pathlib import Path


def binding(path):
    return {"path": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def polynomial_from_forward_values(start, values):
    differences = [list(values)]
    while len(differences[-1]) > 1:
        row = differences[-1]
        differences.append([b-a for a, b in zip(row, row[1:])])
    coefficients = [Fraction(0) for _ in values]
    product = [Fraction(1)]
    factorial = 1
    for degree in range(len(values)):
        if degree:
            factorial *= degree
        for power, coefficient in enumerate(product):
            coefficients[power] += differences[degree][0]*coefficient/factorial
        next_product = [Fraction(0)]*(len(product)+1)
        for power, coefficient in enumerate(product):
            next_product[power] -= (start+degree)*coefficient
            next_product[power+1] += coefficient
        product = next_product
    return coefficients, differences


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prefix", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--prior-inputs", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    graph_path = Path(str(args.prefix)+".graph.json")
    windows_path = Path(str(args.prefix)+".windows.json")
    gluings_path = Path(str(args.prefix)+".gluings.json")
    initial, states, edges, saved_counts = json.loads(graph_path.read_text())
    windows = json.loads(windows_path.read_text())
    gluings = json.loads(gluings_path.read_text())
    assert len(windows) == 706
    assert [sum(w[1] == e for w in windows) for e in range(4)] == [1,15,106,584]
    assert len(set(tuple(w[0]) for w in windows)) == len(windows)
    assert len(states) == 708 and len(edges) == 1522
    assert len(set(map(tuple, edges))) == len(edges)
    assert len(set((s[0], tuple(s[1])) for s in states)) == len(states)
    assert all(1 <= s[0] <= len(windows) and windows[s[0]-1][1] <= s[2] <= 3
               and s[3] in (1,2,4,8) for s in states)
    assert len(initial) == len(windows)
    assert {states[i-1][0] for i,e in initial} == set(range(1,len(windows)+1))
    assert all(e == windows[states[i-1][0]-1][1] for i,e in initial)
    adjacency = defaultdict(list)
    for source, target, weight in edges:
        assert 1 <= source <= len(states) and 1 <= target <= len(states)
        assert 0 <= weight <= 3
        assert states[source-1][2]+weight <= 3
        adjacency[source].append((target,weight))
    # An independent heap implementation verifies every minimum-cost label.
    distance = [99]*(len(states)+1)
    queue = []
    for state, cost in initial:
        distance[state] = cost
        heapq.heappush(queue,(cost,state))
    while queue:
        cost, state = heapq.heappop(queue)
        if cost != distance[state]:
            continue
        for target, weight in adjacency[state]:
            new_cost = cost+weight
            if new_cost < distance[target]:
                distance[target] = new_cost
                heapq.heappush(queue,(new_cost,target))
    assert distance[1:] == [s[2] for s in states]
    extra_states = set(range(1,len(states)+1))-{s for s,e in initial}
    assert {row[1] for row in gluings} == extra_states
    assert len(gluings) == 2
    assert all(row[2] == 16384 and row[4] == 2 and row[5] == 4096 for row in gluings)
    # A sparse (state,total excess) recurrence differs from the GAP arrays.
    current = defaultdict(int)
    for state, excess in initial:
        current[(state,excess)] += 1
    counts = []
    for rank in range(5,25):
        totals = [sum(value for (s,e),value in current.items() if e == k) for k in range(4)]
        assert totals[:3] == [1,5*rank-10,(25*rank*rank-107*rank+122)//2]
        counts.append([rank]+totals)
        following = defaultdict(int)
        for (state,excess),value in current.items():
            for target,weight in adjacency[state]:
                if excess+weight <= 3:
                    following[(target,excess+weight)] += value
        current = following
    assert counts == saved_counts
    by_rank = {row[0]:row[-1] for row in counts}
    coefficients, differences = polynomial_from_forward_values(17,[by_rank[d] for d in range(17,21)])
    assert coefficients == [Fraction(-441),Fraction(1190,3),Fraction(-285,2),Fraction(125,6)]
    evaluate = lambda d: sum(c*d**i for i,c in enumerate(coefficients))
    rank3_path = args.prior_inputs/"phase21_rank3_census.json"
    rank4_path = args.prior_inputs/"phase21_rank4_census.json"
    rank3 = json.loads(rank3_path.read_text())
    rank4 = json.loads(rank4_path.read_text())
    assert rank3["status"] == rank4["status"] == "PASS"
    assert rank3["ordered_markings"] == 37 and rank4["ordered_markings"] == evaluate(4) == 199
    assert all(evaluate(d) == by_rank[d] for d in range(5,25))
    result = {
        "status":"PASS",
        "scope":"Independent sparse recount and shortest-cost verification of the saved exact graph; no independent GAP regeneration",
        "window_excess_counts":[1,15,106,584], "states":len(states),"transitions":len(edges),
        "extra_deletion_states":sorted(extra_states),"extra_state_gluings":gluings,
        "counts":counts,
        "interpolation":{"ranks":[17,18,19,20],"forward_differences":differences,
                         "coefficients_ascending":[str(c) for c in coefficients],
                         "formula":"(125*d^3-855*d^2+2380*d-2646)/6",
                         "polynomial_theorem_retained":"phase16_central_join.md: degree three for every d>=17 at excess three",
                         "finite_extension_checked":"d=4..16; gives formula for every d>=4",
                         "rank3_exception":37,
                         "not_inferred":"Eventual polynomiality is a retained proved theorem, not inferred from the finite values"},
        "inputs":[binding(path) for path in (graph_path,windows_path,gluings_path,rank3_path,rank4_path)],
        "checker":binding(Path(__file__)),
    }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":"PASS","formula":result["interpolation"]["formula"],"ranks":"d>=4; rank3=37"}))


if __name__ == "__main__":
    main()
