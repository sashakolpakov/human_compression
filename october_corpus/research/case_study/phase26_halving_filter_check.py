#!/usr/bin/env python3
"""Exact S6 endpoint-halving diagnostic using standard-library permutations.

No GAP, group database, source geometry list, or external mathematical package
is used. The output is written beside this new checker, never into old files.
"""
from collections import deque
from datetime import datetime, timezone
from hashlib import sha256
from itertools import permutations
import json
from pathlib import Path

N = 6
ONE = tuple(range(N))

def mul(p, q):
    """Right action: first p, then q, as for GAP permutations."""
    return tuple(q[p[i]] for i in range(N))

def cyc(*cycles):
    p = list(ONE)
    for cycle in cycles:
        for i, x in enumerate(cycle):
            p[x - 1] = cycle[(i + 1) % len(cycle)] - 1
    return tuple(p)

def closure(generators):
    seen = {ONE}
    todo = deque([ONE])
    while todo:
        p = todo.popleft()
        for g in generators:
            q = mul(p, g)
            if q not in seen:
                seen.add(q)
                todo.append(q)
    return frozenset(seen)

def shortest_word(generators, target):
    words = {ONE: ()}
    todo = deque([ONE])
    while todo:
        p = todo.popleft()
        if p == target:
            return words[p]
        for i, g in enumerate(generators):
            q = mul(p, g)
            if q not in words:
                words[q] = words[p] + (i,)
                todo.append(q)
    return None

def marked_subgroups(generators):
    return [closure([g for i, g in enumerate(generators) if m & (1 << i)])
            for m in range(16)]

def meets(groups):
    failures = []
    for i in range(16):
        for j in range(16):
            actual = groups[i] & groups[j]
            expected = groups[i & j]
            if actual != expected:
                failures.append({"masks": [i, j], "actual_order": len(actual),
                                 "expected_order": len(expected),
                                 "extra_elements": [list(p) for p in sorted(actual - expected)]})
    return failures

def conjugate_set(S, a):
    return frozenset(mul(mul(a, p), a) for p in S)

def set_image(p, S):
    return frozenset(p[i] for i in S)

a = cyc((1, 2))
b = cyc((1, 3), (2, 4), (5, 6))
c = cyc((4, 5))
d = cyc((4, 6))
e = mul(mul(a, b), a)
assert e == cyc((1, 4), (2, 3), (5, 6))
old = marked_subgroups([a, b, c, d])
new = marked_subgroups([e, b, c, d])
all_s6 = frozenset(permutations(range(N)))
assert all(mul(g, g) == ONE and g != ONE for g in [a, b, c, d, e])
assert mul(a, c) == mul(c, a) and mul(a, d) == mul(d, a)
assert old[15] == new[15] == all_s6
old_fail = meets(old)
new_fail = meets(new)
assert old_fail == []
assert [(f['masks'], f['actual_order'], f['expected_order']) for f in new_fail] == [([7, 11], 8, 4), ([11, 7], 8, 4)]

# Identify P, R and the two local rank-three groups by their actual actions.
P = old[14]
R = old[12]
block13 = frozenset([0, 2])
P_expected = frozenset(p for p in all_s6 if set_image(p, block13) == block13)
R_expected = frozenset(p for p in all_s6 if all(p[i] == i for i in range(3)))
assert P == P_expected and len(P) == 48
assert R == R_expected and len(R) == 6
assert P & conjugate_set(P, a) == R
local_identifications = []
for mask, blocks in [(7, [frozenset([0, 1, 5]), frozenset([2, 3, 4])]),
                     (11, [frozenset([0, 1, 4]), frozenset([2, 3, 5])])]:
    expected = frozenset(p for p in all_s6 if {set_image(p, B) for B in blocks} == set(blocks))
    assert old[mask] == new[mask] == expected
    assert len(expected) == 72
    local_identifications.append({'mask': mask, 'blocks_one_based': [sorted(i + 1 for i in B) for B in blocks], 'order': 72})
assert old[7] & old[11] == old[3]
assert len(old[3]) == 8 and len(new[3]) == 4 and a not in new[3]

# The filter uses subsets of {c,d}, encoded by bits 0 and 1.
filter_membership = []
recovery_words = []
for j in range(4):
    generators = [e, b] + ([c] if j & 1 else []) + ([d] if j & 2 else [])
    filter_membership.append(a in closure(generators))
    recovery_words.append(shortest_word(generators, a))
assert filter_membership == [False, True, True, True]
for g, word in [(c, recovery_words[1]), (d, recovery_words[2])]:
    value = ONE
    for i in word:
        value = mul(value, [e, b, g][i])
    assert value == a

def digest_group(group):
    raw = json.dumps([list(p) for p in sorted(group)], separators=(',', ':')).encode()
    return sha256(raw).hexdigest()

report = {
    'date_utc': datetime.now(timezone.utc).isoformat(),
    'status': 'PASS',
    'checker_sha256': sha256(Path(__file__).read_bytes()).hexdigest(),
    'arithmetic': 'Python standard library; explicit degree-six permutations and BFS subgroup closure',
    'permutation_convention': 'zero-based image arrays; multiplication means first left permutation then right permutation',
    'tuple_one_based_cycles': ['(1,2)', '(1,3)(2,4)(5,6)', '(4,5)', '(4,6)'],
    'old_generators': [list(g) for g in [a,b,c,d]],
    'new_generators': [list(g) for g in [e,b,c,d]],
    'old_group_order': len(old[15]), 'new_group_order': len(new[15]),
    'old_subset_orders_bitmask_order': list(map(len, old)),
    'new_subset_orders_bitmask_order': list(map(len, new)),
    'old_all_256_meet_failures': old_fail,
    'new_all_256_meet_failures': new_fail,
    'old_subset_element_set_sha256s': list(map(digest_group, old)),
    'new_subset_element_set_sha256s': list(map(digest_group, new)),
    'P_order': len(P), 'R_order': len(R), 'P_overlap_order': len(P & conjugate_set(P, a)),
    'local_wreath_product_identifications': local_identifications,
    'filter_membership_bitmask_order': filter_membership,
    'endpoint_recovery_words_zero_based': recovery_words,
    'scope': 'One exact finite negative example. No coset-Helly or classification claim.'
}
out = Path(__file__).with_suffix('.json')
out.write_text(json.dumps(report, indent=2) + '\n')
print('S6_FILTER_ISOLATION_PASS old_meets=256 new_meets=256 new_failures=2 overlap=6')
print('RECOVERY_WORDS', recovery_words)
