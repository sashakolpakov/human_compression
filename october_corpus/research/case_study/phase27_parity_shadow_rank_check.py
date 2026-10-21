#!/usr/bin/env python3
"""Independent bitset audit of the firm rank-four parity-shadow example.

No imports from the author's checker. Reconstructs Construction 3.6 from
computed even-walk classes, then enumerates every typed flag recursively.
"""
from collections import Counter, deque
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json


def indices(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def graph_components(mask, adjacency):
    parts = []
    while mask:
        seed = mask & -mask
        part = seed
        todo = seed
        mask ^= seed
        while todo:
            i = next(indices(todo))
            todo ^= 1 << i
            new = adjacency[i] & mask
            part |= new
            todo |= new
            mask ^= new
        parts.append(part)
    return parts


def even_classes(vertex_mask, graph):
    """Connected components in the graph of length-two walks."""
    even = [0] * len(graph)
    for v in indices(vertex_mask):
        for middle in indices(graph[v] & vertex_mask):
            even[v] |= graph[middle] & vertex_mask
    return graph_components(vertex_mask, even)


def analyze(objects, incidence):
    n = len(objects)
    types = [o[0] for o in objects]
    adjacency = [sum(1 << j for j in range(n)
                     if types[i] != types[j] and incidence(objects[i], objects[j]))
                 for i in range(n)]
    flags = []

    def extend(flag, candidates):
        flags.append(flag)
        while candidates:
            low = candidates & -candidates
            candidates ^= low
            i = low.bit_length() - 1
            extend(flag | low, candidates & adjacency[i])

    extend(0, (1 << n) - 1)
    chambers = [f for f in flags if f.bit_count() == 4]
    failures = []
    panel_sizes = Counter()
    rank_two = {}
    for flag in flags:
        assert any(flag & chamber == flag for chamber in chambers)
        residue = (1 << n) - 1
        selected_types = set()
        for i in indices(flag):
            residue &= adjacency[i]
            selected_types.add(types[i])
        missing = sorted(set(range(4)) - selected_types)
        if len(missing) == 1:
            panel_sizes[residue.bit_count()] += 1
        if len(missing) >= 2:
            components = graph_components(residue, adjacency)
            if len(components) != 1:
                failures.append({"flag_object_indices": list(indices(flag)),
                                 "flag_types": sorted(selected_types),
                                 "component_sizes": sorted(p.bit_count() for p in components)})
        if len(missing) == 2:
            key = ",".join(map(str, missing))
            row = rank_two.setdefault(key, {"residues": 0, "all_complete_bipartite": True})
            row["residues"] += 1
            for i in indices(residue):
                expected = sum(1 << j for j in indices(residue) if types[i] != types[j])
                row["all_complete_bipartite"] &= adjacency[i] & residue == expected
    return {"object_counts": [types.count(i) for i in range(4)],
            "flags": len(flags), "chambers": len(chambers),
            "geometry": True, "panel_counts": dict(sorted(panel_sizes.items())),
            "rank_two_residues": rank_two, "RC_failures": failures}, adjacency


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_suffix(".json"))
    args = parser.parse_args()
    # Vertices 0,1 | 2,3 | 4,5 | 6,7; higher objects omit one whole part.
    graph = [sum(1 << w for w in range(8) if v // 2 != w // 2) for v in range(8)]
    all_vertices = 255
    edge_masks = [(1 << v) | (1 << w) for v, w in combinations(range(8), 2)
                  if graph[v] & (1 << w)]
    shadows = [all_vertices ^ (3 << (2 * p)) for p in range(4)]
    objects = [(0, 1 << v) for v in range(8)] + [(1, e) for e in edge_masks]
    objects += [(i, s) for i in (2, 3) for s in shadows]

    def old_incident(x, y):
        if x[0] > y[0]: x, y = y, x
        if x[0] == y[0]: return x == y
        if x[0] == 0 or x[0] == 1: return x[1] & y[1] == x[1]
        return True

    assert len(edge_masks) == len(set(edge_masks)) == 24
    assert len(even_classes(all_vertices, graph)) == 1
    b2_instances = 0
    for edge in [(1, e) for e in edge_masks]:
        for higher in [(i, s) for i in (2, 3) for s in shadows]:
            assert old_incident(edge, higher) == all(
                old_incident((0, 1 << v), higher) for v in indices(edge[1]))
            b2_instances += 1

    # New higher record is (type, old shadow, selected parity class, opposite class).
    new_objects = [(i, 1 << v, 0, 0) for i in (0, 1) for v in range(8)]
    higher_classes = []
    for i in (2, 3):
        for shadow in shadows:
            classes = even_classes(shadow, graph)
            higher_classes.append(len(classes))
            for parity in classes:
                opposite = parity if len(classes) == 1 else shadow ^ parity
                new_objects.append((i, shadow, parity, opposite))

    def new_incident(x, y):
        if x[0] > y[0]: x, y = y, x
        if x[0] == y[0]: return x == y
        if y[0] == 1:
            v = next(indices(x[1]))
            return bool(graph[v] & y[1])
        if x[0] == 0: return bool(x[1] & y[2])
        if x[0] == 1: return bool(x[1] & y[3])
        return bool(x[2] & y[2])

    old, _ = analyze(objects, old_incident)
    new, _ = analyze(new_objects, new_incident)
    assert old["flags"] == 801 and old["chambers"] == 192
    assert not old["RC_failures"] and old["panel_counts"] == {2: 336, 4: 24}
    assert all(old["rank_two_residues"][key]["all_complete_bipartite"]
               for key in ("0,2", "0,3", "2,3"))
    assert higher_classes == [1] * 8
    assert len(new["RC_failures"]) == 12
    assert all(f["flag_types"] == [2, 3] and f["component_sizes"] == [4, 4]
               for f in new["RC_failures"])
    # The same graph computed directly on intersected old shadows has TWO classes.
    intersections = []
    for left in range(4):
        for right in range(4):
            if left != right:
                mask = shadows[left] & shadows[right]
                cls = even_classes(mask, graph)
                assert len(cls) == 2 and sorted(c.bit_count() for c in cls) == [2, 2]
                intersections.append({"omitted_parts": [left, right],
                                      "intersection_vertices": list(indices(mask)),
                                      "even_walk_classes": [list(indices(c)) for c in cls]})
    report = {"status": "PASS", "checker_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "method": "Independent bitset flag recursion and computed even-walk parity classes",
              "source_relation": "Literal Construction3.6 of arXiv2405.19050v1",
              "B1": True, "B2_instances": b2_instances,
              "single_higher_parity_class_counts": higher_classes,
              "original": old, "partitioned": new,
              "distinct_higher_intersections": intersections,
              "boundary": "Firm but nonthin starting geometry; no regular-hypertope counterexample claimed"}
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("PASS: 801 original flags, 192 chambers, all original residues connected; 12 new disconnected residues")


if __name__ == "__main__":
    main()
