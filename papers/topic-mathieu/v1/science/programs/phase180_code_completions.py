#!/usr/bin/env python3
"""Enumerate all Golay-code completions of the literal primary MOG seeds.

This finite certificate retains the classical fact that Curtis's MOG comes
from a binary self-dual [24,12,8] Golay code. No QR labelling is assumed.
"""
import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


def require(test, message):
    if not test:
        raise ValueError(message)


def insert(vector, basis):
    while vector:
        pivot = vector.bit_length() - 1
        if pivot in basis:
            vector ^= basis[pivot]
        else:
            basis[pivot] = vector
            return


def span(vectors):
    result = [0]
    for vector in vectors:
        result += [old ^ vector for old in result]
    require(len(set(result)) == len(result), "dependent span generators")
    return result


def support(vector):
    return [i for i in range(24) if vector >> i & 1]


def binding(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": sha256(data).hexdigest()}


def complete(source):
    seeds = source["octad_seeds"]
    basis = {}
    for seed in seeds:
        points = seed["support"]
        require(len(points) == len(set(points)) == 8 and set(points) <= set(range(24)), "bad octad seed")
        insert(sum(1 << i for i in points), basis)
    require(len(basis) == 10, "primary seed code must have dimension10")
    require(all((a & b).bit_count() % 2 == 0 for a in basis.values() for b in basis.values()), "nonorthogonal primary seeds")
    lower = span(list(basis.values()))
    null_basis = []
    for free in sorted(set(range(24)) - set(basis)):
        vector = 1 << free
        for pivot in sorted(basis):
            if (vector & basis[pivot]).bit_count() % 2:
                vector ^= 1 << pivot
        require(all((vector & row).bit_count() % 2 == 0 for row in basis.values()), "nullspace equation")
        null_basis.append(vector)
    upper = span(null_basis)
    require(len(upper) == 2**14 and set(lower) <= set(upper), "orthogonal space dimensions")
    representatives, covered = [], set()
    for vector in upper:
        if vector not in covered:
            representatives.append(vector)
            covered.update(vector ^ word for word in lower)
    require(len(representatives) == 16, "quotient size")
    cosets = [{r ^ word for word in lower} for r in representatives]
    coset_of = {word: i for i, coset in enumerate(cosets) for word in coset}
    require(len(coset_of) == len(upper), "coset partition")
    allowed_weights = {0, 8, 12, 16, 24}
    allowed = {i for i, coset in enumerate(cosets) if all(word.bit_count() in allowed_weights for word in coset)}
    planes = set()
    for i, j in combinations(range(1, 16), 2):
        k = coset_of[representatives[i] ^ representatives[j]]
        planes.add(tuple(sorted([0, i, j, k])))
    require(len(planes) == 35 and all(len(set(p)) == 4 for p in planes), "all two-dimensional quotient subspaces")
    accepted = []
    for plane in sorted(planes):
        if not set(plane) <= allowed:
            continue
        words = set().union(*(cosets[i] for i in plane))
        require(len(words) == 4096, "full code size")
        require(Counter(w.bit_count() for w in words) == Counter({0: 1, 8: 759, 12: 2576, 16: 759, 24: 1}), "Golay weight distribution")
        blocks = sorted(support(w) for w in words if w.bit_count() == 8)
        pentads = Counter(p for block in blocks for p in combinations(block, 5))
        require(len(pentads) == 42504 and set(pentads.values()) == {1}, "Steiner axiom")
        accepted.append({"quotient_plane": list(plane), "blocks": blocks,
                         "codeword_sha256": sha256(json.dumps(sorted(words), separators=(",", ":")).encode()).hexdigest(),
                         "five_subset_count": len(pentads)})
    require(len(accepted) == 4, "unexpected compatible completion count")
    return {"seed_count": len(seeds), "seed_rank": 10, "orthogonal_rank": 14,
            "seed_basis_supports": [support(basis[k]) for k in sorted(basis)],
            "quotient_representative_supports": [support(r) for r in representatives],
            "quotient_subspaces_tested": len(planes), "allowed_cosets": sorted(allowed),
            "completions": accepted,
            "exhaustiveness": "Every binary self-dual dimension12 code containing the primary seed code lies in its orthogonal space and corresponds to one of the35 two-dimensional quotient subspaces. Minimum8 and double evenness leave exactly these four. Each is separately verified to give S(5,8,24)."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(__file__).with_name("phase180_source_notation.json"))
    parser.add_argument("--target-shadows", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    require(not args.output_dir.exists() and not args.output_dir.is_symlink(), "output directory occupied")
    source = json.loads(args.source.read_text())
    target = json.loads(args.target_shadows.read_text())
    report = complete(source)
    report.update(status="PASS", source=binding(args.source), target_shadows=binding(args.target_shadows),
                  retained_input=source["retained_mathematical_input"], QR_coordinate_identification_assumed=False)
    args.output_dir.mkdir()
    (args.output_dir / "code_completions.json").write_text(json.dumps(report, indent=2) + "\n")
    gap_data = {"sourceCodeBlocks": [[[p + 1 for p in block] for block in c["blocks"]] for c in report["completions"]],
                "targetBlocks": target["blocks"], "targetFixed": target["fixed"],
                "sourceTriples": [[[p + 1 for p in obj] for obj in case["objects"]] for case in source["colon_cases"]],
                "sourceLabels": [c["label"] for c in source["colon_cases"]],
                "sourcePairs": [[[p + 1 for p in obj] for obj in case["objects"]] for case in source["explicit_refined_pair_objects"]],
                "sourcePairLabels": [c["label"] for c in source["explicit_refined_pair_objects"]],
                "sourcePairTypes": [c["types"] for c in source["explicit_refined_pair_objects"]],
                "sourcePairOrders": [c["printed_pair_order"] for c in source["explicit_refined_pair_objects"]]}
    text = "\n".join(name + ":=" + json.dumps(value, separators=(",", ":")) + ";;" for name, value in gap_data.items()) + "\n"
    (args.output_dir / "code_inputs.g").write_text(text)
    print(json.dumps({"status": "PASS", "completions": 4, "seed_rank": 10, "quotient_subspaces_tested": 35}))


if __name__ == "__main__":
    main()
