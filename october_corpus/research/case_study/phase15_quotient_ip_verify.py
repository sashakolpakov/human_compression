#!/usr/bin/env python3
"""Verify one permutation witness by exhaustive exact operations, with no GAP."""
import argparse
import hashlib
import json
from collections import deque
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--witness", type=Path,
                        default=Path(__file__).with_name("phase15_quotient_ip_witness.json"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = json.loads(args.witness.read_text())
    degree = data["degree"]
    permutations = [tuple(i - 1 for i in p) for p in data["generators"]]
    identity = tuple(range(degree))
    assert all(sorted(p) == list(identity) for p in permutations)

    def compose(p, q):
        return tuple(p[q[i]] for i in range(degree))

    elements = [identity]
    index = {identity: 0}
    pending = deque([identity])
    while pending:
        p = pending.popleft()
        for r in permutations:
            product = compose(p, r)
            if product not in index:
                index[product] = len(elements)
                elements.append(product)
                pending.append(product)
    order = len(elements)
    assert order == 256
    product = [[index[compose(p, q)] for q in elements] for p in elements]
    inverse = [row.index(0) for row in product]
    marked = [index[p] for p in permutations]
    assert all(product[r][r] == 0 and r != 0 for r in marked)
    assert product[marked[0]][marked[2]] == product[marked[2]][marked[0]]

    def subgroup(generators):
        generators = set(generators) - {0}
        result, queue = {0}, deque([0])
        while queue:
            g = queue.popleft()
            for h in generators:
                gh = product[g][h]
                if gh not in result:
                    result.add(gh)
                    queue.append(gh)
        return result

    def commutator(g, h):
        return product[product[product[inverse[g]][inverse[h]]][g]][h]

    def element_order(g):
        h, count = 0, 0
        while True:
            h, count = product[h][g], count + 1
            if h == 0:
                return count

    parabolics = [subgroup(marked[i] for i in range(3) if mask >> i & 1)
                  for mask in range(8)]
    for i in range(8):
        for j in range(8):
            assert parabolics[i] & parabolics[j] == parabolics[i & j]
    lower = [set(range(order))]
    while len(lower[-1]) > 1:
        following = subgroup(commutator(g, h)
                             for g in lower[-1] for h in range(order))
        assert following < lower[-1]
        lower.append(following)
    assert list(map(len, lower)) == [256, 32, 8, 2, 1]
    c1, c2 = commutator(marked[0], marked[1]), commutator(marked[1], marked[2])
    z1, z2 = product[c1][c1], product[c2][c2]
    assert z1 != z2 and element_order(z1) == element_order(z2) == 2
    triple = commutator(c1, marked[2])
    assert product[triple][triple] == 0
    assert product[z1][z2] == commutator(c1, c2)
    last = lower[3]
    assert last == subgroup([product[z1][z2]])
    assert all(product[z][g] == product[g][z] for z in last for g in range(order))
    left, right = parabolics[3], parabolics[6]
    assert len(left) == len(right) == 16
    assert left & right == subgroup([marked[1]])
    assert left & last == right & last == {0}

    def quotient_meets(normal):
        preimages = [{product[g][n] for g in H for n in normal}
                     for H in parabolics]
        failures = [(i, j) for i in range(8) for j in range(8)
                    if preimages[i] & preimages[j] != preimages[i & j]]
        return preimages, failures

    preimages, failed = quotient_meets(last)
    middle_meet = preimages[3] & preimages[6]
    assert len(middle_meet) // len(last) == 4
    assert middle_meet == subgroup([marked[1], z1, *last])
    assert product[z1][inverse[z2]] in last and z1 not in last
    assert failed
    _, class_two_failures = quotient_meets(lower[2])
    assert not class_two_failures

    result = {
        "status": "PASS",
        "scope": "One exact generated permutation witness; no group catalogue, GAP or NQ used by this verifier.",
        "witness": args.witness.name,
        "witness_sha256": hashlib.sha256(args.witness.read_bytes()).hexdigest(),
        "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "permutation_degree": degree,
        "group_order": order,
        "type": [element_order(product[marked[i]][marked[i+1]]) for i in range(2)],
        "lower_central_orders": list(map(len, lower)),
        "displayed_presentation_relations_checked": 8,
        "original_IP_comparisons": 64,
        "parabolic_orders": [len(left), len(right)],
        "original_middle_meet_order": len(left & right),
        "last_central_order": len(last),
        "last_central_intersections_with_parabolics": [len(left & last), len(right & last)],
        "quotient_middle_meet_order": len(middle_meet) // len(last),
        "quotient_middle_meet_generators": ["image(r2)", "image([r1,r2]^2)=image([r2,r3]^2)"],
        "last_central_quotient_failed_IP_mask_pairs": failed,
        "class_two_quotient_order": order // len(lower[2]),
        "class_two_quotient_IP_comparisons": 64,
        "generalization": "No assertion that arbitrary last-central quotients preserve or fail IP."
    }
    rendered = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
