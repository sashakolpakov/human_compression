#!/usr/bin/env python3
"""Independent finite separating images; these do not prove the infinite gluing theorem."""
from itertools import permutations
import json

IDENTITY = ((0, 1, 2), 0)
A = ((1, 0, 2), 0)
B = ((0, 2, 1), 0)
C = ((0, 1, 2), 1)


def need(ok, message):
    if not ok:
        raise ValueError('N005_FINITE_REJECT: ' + message)


def mul(x, y):
    return (tuple(x[0][y[0][i]] for i in range(3)), x[1] ^ y[1])


def generated(*gens):
    group = {IDENTITY}
    todo = [IDENTITY]
    while todo:
        x = todo.pop()
        for g in gens:
            z = mul(x, g)
            if z not in group:
                group.add(z)
                todo.append(z)
    return group


def validate(a, b, c, hnn_word=None):
    aa, bb, cc = generated(a, c), generated(b, c), generated(c)
    da, db, ea, eb = generated(a), generated(b), generated(mul(a, c)), generated(mul(b, c))
    need(len(aa) == len(bb) == 4 and aa & bb == cc and len(cc) == 2, 'embedded Klein four factors')
    need(all(h & cc == {IDENTITY} for h in [da, db, ea, eb]), 'four trivial associated intersections')
    need(da & ea == db & eb == {IDENTITY}, 'trivial local intersections')
    need(mul(a, c) == mul(c, a) and mul(b, c) == mul(c, b), 'central amalgamating involution')
    w = mul(a, b)
    need(w != IDENTITY and mul(w, w) != IDENTITY and mul(w, mul(w, w)) == IDENTITY,
         'nontrivial amalgam separating word of order three')
    need(w == mul(mul(a, c), mul(b, c)), 'literal second factorization')
    h = mul(mul(a, b), a) if hnn_word is None else hnn_word
    need(h == mul(mul(mul(a, c), b), mul(a, c)) and h not in generated(b),
         'literal HNN word outside stable-letter cyclic image')
    return dict(ambient_order=len(generated(a, b, c)), factor_orders=[len(aa), len(bb)],
                associated_order=len(cc), amalgam_word_order=3,
                finite_intersection_order=len(generated(a, b) & generated(mul(a, c), mul(b, c))),
                HNN_word_outside_stable_cyclic=True)


def run():
    separating = validate(A, B, C)
    # In the first Klein four factor these cosets form a flag with no
    # common representative. It explains why arbitrary subgroup data
    # cannot replace the geometric flag-transitivity hypothesis.
    h1, h2, h3 = generated(C), generated(A), generated(mul(A, C))
    cosets = [h1, h2, {mul(A, x) for x in h3}]
    need(all(cosets[i] & cosets[j] for i in range(3) for j in range(i)), 'pairwise local incidence')
    need(not set.intersection(*cosets), 'failure of local common-representative condition')
    # Empty P: A is the Q-parabolic in B, so A *_A B = B. Use an
    # ineffective C2 kernel to make the chamber stabilizer nontrivial.
    whole_b = generated(A, B, C)
    b0, b1 = generated(A, C), generated(B, C)
    borel = b0 & b1
    need(len(borel) == 2 and len(whole_b) == 12, 'nontrivial ineffective Borel')
    rows = []
    for J in [set(), {0}, {1}, {0, 1}]:
        db = whole_b.copy()
        if 0 in J:
            db &= b0
        if 1 in J:
            db &= b1
        da = b1 if 0 not in J else borel
        need(da <= db, 'collapsed factor is contained in remaining parabolic')
        rows.append(dict(J=sorted(J), A_factor=len(da), B_factor=len(db), collapsed_order=len(db)))
    need(len(b0) // len(borel) == len(b1) // len(borel) == 2, 'thin panels with nontrivial Borel')
    controls = []
    for name, call in [
        ('collapse associated involution', lambda: validate(A, B, IDENTITY)),
        ('identify distinct factor reflections', lambda: validate(A, A, C)),
        ('substitute stable letter for separating HNN word', lambda: validate(A, B, C, B)),
        ('make amalgamating involution noncentral', lambda: validate(A, B, A))
    ]:
        try:
            call()
        except ValueError:
            controls.append(name)
        else:
            raise ValueError('accepted invalid diagnostic ' + name)
    return dict(status='PASS', separating_images=separating,
                pairwise_local_cosets_without_common_representative=True,
                empty_private_type_cases=rows, nontrivial_Borel_order=2,
                rejected_controls=controls, infinite_group_equality_certified=False,
                uniform_tree_gluing_verified_by_finite_tests=False)


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
