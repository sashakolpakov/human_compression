#!/usr/bin/env python3
"""Check literal L092 Construction 3 on the deleted-line affine geometries.

This checks every flag and every rank-at-least-two residue, and constructs
explicit incidence-preserving permutations. It does not compute the full
automorphism group or supply a Lean proof of the uniform classification.
"""
import argparse
from collections import Counter, deque
import hashlib
from itertools import combinations
import json
from pathlib import Path


def require(test, message):
    if not test:
        raise RuntimeError(message)


class Field:
    def __init__(self, q):
        require(q in (4, 8), "only the two stated fields are implemented")
        self.q = q
        self.modulus = {4: 0b111, 8: 0b1011}[q]

    def mul(self, a, b):
        result = 0
        while b:
            if b & 1:
                result ^= a
            b >>= 1
            a <<= 1
            if a & self.q:
                a ^= self.modulus
        return result

    def validate(self):
        Q = range(self.q)
        for a in Q:
            require(self.mul(a, 1) == a, "identity")
            if a:
                require(sum(self.mul(a, b) == 1 for b in Q) == 1, "inverse")
            for b in Q:
                require(self.mul(a, b) == self.mul(b, a), "commutativity")
                for c in Q:
                    require(self.mul(a, b ^ c) == self.mul(a, b) ^ self.mul(a, c),
                            "distributivity")
                    require(self.mul(self.mul(a, b), c) == self.mul(a, self.mul(b, c)),
                            "associativity")


def components(vertices, neighbours):
    remaining = set(vertices)
    result = []
    while remaining:
        root = min(remaining)
        seen, queue = {root}, deque([root])
        remaining.remove(root)
        while queue:
            current = queue.popleft()
            new = neighbours[current] & remaining
            seen.update(new)
            remaining.difference_update(new)
            queue.extend(sorted(new))
        result.append(sorted(seen))
    return result


def check(q):
    field = Field(q)
    field.validate()
    mul = field.mul
    points = [(x, y) for x in range(q) for y in range(1, q)]
    lines = [(a, b) for a in range(q) for b in range(q)]
    line_sets = [frozenset(i for i, (x, y) in enumerate(points) if x == mul(a, y) ^ b)
                 for a, b in lines]
    require(all(len(M) == q-1 for M in line_sets), "wrong source line size")
    require(all(sum(p in M for M in line_sets) == q for p in range(len(points))),
            "wrong source point degree")
    require(all(len(M & N) <= 1 for M, N in combinations(line_sets, 2)),
            "source is not a partial linear space")
    source_flags = [(p, m) for p in range(len(points)) for m, M in enumerate(line_sets)
                    if p in M]
    objects = ([(0, p) for p in range(len(points))]
               + [(1, m) for m in range(len(lines))]
               + [(2, flag) for flag in source_flags])
    bytype = [set(i for i, (t, _) in enumerate(objects) if t == j) for j in range(3)]
    index = {obj: i for i, obj in enumerate(objects)}
    neighbours = [set() for obj in objects]

    def incident(i, j):
        ti, x = objects[i]
        tj, y = objects[j]
        if ti > tj:
            return incident(j, i)
        if ti == tj:
            return False
        if (ti, tj) == (0, 1):
            return x not in line_sets[y]
        if (ti, tj) == (0, 2):
            p, m = y
            return x != p and x in line_sets[m]
        if (ti, tj) == (1, 2):
            p, m = y
            return line_sets[x] & line_sets[m] == {p}
        raise RuntimeError("missing incidence rule")

    for i, j in combinations(range(len(objects)), 2):
        if incident(i, j):
            neighbours[i].add(j)
            neighbours[j].add(i)

    allflags = [[] for _ in range(4)]

    def enumerate_flags(prefix, choices):
        allflags[len(prefix)].append(tuple(prefix))
        for i in sorted(choices):
            enumerate_flags(prefix+[i], {j for j in choices & neighbours[i] if j > i})

    enumerate_flags([], set(range(len(objects))))
    chambers = set(allflags[3])
    extended = set()
    for C in chambers:
        for k in range(4):
            extended.update(combinations(C, k))
    require(all(F in extended for layer in allflags for F in layer),
            "literal construction has a nonextendable flag")
    panel_counts = Counter(len(neighbours[i] & neighbours[j]) for i, j in allflags[2])
    require(min(panel_counts) >= 2, "literal construction is not firm")
    require(len(chambers) == q*q*(q-1)**2*(q-2), "wrong chamber count")
    whole_components = components(range(len(objects)), neighbours)
    require(len(whole_components) == 1, "whole incidence graph disconnected")
    residue_patterns = [Counter() for _ in range(3)]
    disconnected_examples = []
    for i, (t, obj) in enumerate(objects):
        pieces = components(neighbours[i], neighbours)
        signature = tuple(sorted(len(C) for C in pieces))
        residue_patterns[t][signature] += 1
        if len(pieces) > 1 and not disconnected_examples:
            disconnected_examples.append({'object':objects[i],
                'components':[[objects[j] for j in C] for C in pieces],
                'vertex_degrees':sorted(len(neighbours[j] & neighbours[i])
                                        for j in neighbours[i])})

    # Lines (a,b) of the original structure are points of the dual net.
    # Its lines are the sets ay+b=x with y nonzero. This identification
    # allows an independently specified group action on the same incidence.
    dual_lines = [frozenset(m for m, M in enumerate(line_sets) if p in M)
                  for p in range(len(points))]
    dual_line_index = {M:p for p, M in enumerate(dual_lines)}
    line_index = {L:i for i, L in enumerate(lines)}
    basis = [1 << k for k in range(q.bit_length()-1)]
    dual_generators = []
    for e in basis:
        dual_generators.append((f'translate_first_{e}', [(a ^ e, b) for a, b in lines]))
        dual_generators.append((f'translate_second_{e}', [(a, b ^ e) for a, b in lines]))
    dual_generators += [
        ('scale_first', [(mul(2, a), b) for a, b in lines]),
        ('scale_second', [(a, mul(2, b)) for a, b in lines]),
        ('swap', [(b, a) for a, b in lines]),
        ('frobenius', [(mul(a, a), mul(b, b)) for a, b in lines])]
    object_generators = []
    for name, images in dual_generators:
        lm = [line_index[L] for L in images]
        pm = [dual_line_index[frozenset(lm[m] for m in M)] for M in dual_lines]
        perm = []
        for t, obj in objects:
            image = pm[obj] if t == 0 else lm[obj] if t == 1 else (pm[obj[0]], lm[obj[1]])
            perm.append(index[t, image])
        require(len(set(perm)) == len(objects), "nonbijective action: " + name)
        for i in range(len(objects)):
            require({perm[j] for j in neighbours[i]} == neighbours[perm[i]],
                    "action does not preserve incidence: " + name)
        object_generators.append(perm)
    remaining = set(chambers)
    chamber_orbits = []
    while remaining:
        root = min(remaining)
        orbit, queue = {root}, deque([root])
        remaining.remove(root)
        while queue:
            C = queue.popleft()
            for perm in object_generators:
                D = tuple(perm[i] for i in C)
                require(D in chambers, "nonchamber image")
                if D not in orbit:
                    require(D in remaining, "overlapping orbits")
                    remaining.remove(D)
                    orbit.add(D)
                    queue.append(D)
        chamber_orbits.append(len(orbit))
    require(len(chamber_orbits) == 1, "displayed subgroup is not chamber transitive")
    is_rc = all(len(pattern) == 1 for counts in residue_patterns for pattern in counts)
    require(is_rc == (q == 8), "unexpected residual-connectedness outcome")
    if q == 4:
        require(residue_patterns[1] == {(6, 6, 6):16}, "q4 line residues must be 3C6")
    encoding = {'points':points, 'lines':lines, 'source_line_sets':[sorted(M) for M in line_sets],
                'objects':objects, 'neighbours':[sorted(N) for N in neighbours],
                'object_generators':object_generators}
    return {'q':q, 'polynomial_bits':field.modulus, 'field_axioms_checked':True,
            'objects_by_type':[len(T) for T in bytype],
            'all_flag_counts':[len(F) for F in allflags],
            'all_flags_extend':True, 'firm':True,
            'panel_completion_distribution':dict(sorted(panel_counts.items())),
            'whole_incidence_graph_connected':True,
            'rank_two_residue_component_patterns':[
                [{'component_sizes':list(P),'number_of_residues':n} for P,n in sorted(C.items())]
                for C in residue_patterns],
            'residually_connected':is_rc, 'disconnected_examples':disconnected_examples,
            'verified_subgroup_generators':[name for name,_ in dual_generators],
            'chamber_orbits_under_verified_subgroup':chamber_orbits,
            'flag_transitive':True,
            'full_automorphism_group_computed':False,
            'certificate_sha256':hashlib.sha256(json.dumps(encoding,sort_keys=True).encode()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    require(not args.output.exists(), 'refusing existing output')
    report = {'status':'PASS', 'source':'L092 Construction 3 and Theorem 6',
              'source_type_order':'original point, original line, original flag',
              'cases':[check(q) for q in (4,8)],
              'uniform_parameter_classification_checked':False, 'Lean_certificate':False,
              'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    with args.output.open('x') as f:
        json.dump(report, f, indent=2)
        f.write('\n')
    for case in report['cases']:
        print(json.dumps({key:case[key] for key in ('q','objects_by_type','all_flag_counts',
              'firm','residually_connected','chamber_orbits_under_verified_subgroup')}))


if __name__ == '__main__':
    main()
