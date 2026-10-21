#!/usr/bin/env python3
"""Small independent countermodels to false weakenings of the elementary lemmas.
These are not tests of the geometric theorem or evidence for its generality.
"""
import argparse
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def controls():
    swap = (1, 0)
    require(all(swap[swap[x]] == x for x in range(2)), 'swap is not involutory')
    require(any(swap[x] != x for x in range(2)), 'swap became trivial')
    # I=J={0}; coord(0,x)=x separates points, but supports overlap.
    # I=J=empty; constant coord fails separation and every permutation preserves it.
    def coordinate_hypotheses(coord, I, J):
        separates = all(x == y or any(row[x] != row[y] for row in coord)
                        for x in range(2) for y in range(2))
        preserves = lambda I: all(row[swap[x]] == row[x]
                                 for i, row in enumerate(coord) if i not in I
                                 for x in range(2))
        return {'separates': separates, 'disjoint': not I.intersection(J),
                'a_preserves_outside_I': preserves(I),
                'b_preserves_outside_J': preserves(J), 'a_times_b_identity': True}
    overlapping = coordinate_hypotheses([[0, 1]], {0}, {0})
    nonseparating = coordinate_hypotheses([[0, 0]], set(), set())
    require(overlapping == {'separates': True, 'disjoint': False,
            'a_preserves_outside_I': True, 'b_preserves_outside_J': True,
            'a_times_b_identity': True}, 'overlap hypotheses invalid')
    require(nonseparating == {'separates': False, 'disjoint': True,
            'a_preserves_outside_I': True, 'b_preserves_outside_J': True,
            'a_times_b_identity': True}, 'nonseparation hypotheses invalid')
    # W=C2^2, written additively with bitwise XOR. Its standard coordinate
    # parabolics P(I) are all vectors whose support lies in I.
    parabolic = {I: {x for x in range(4) if x & ~I == 0} for I in range(4)}
    K = {0, 3}
    candidates = ({0}, K)
    def ip(N):
        for I in range(4):
            for J in range(4):
                for a in parabolic[I]:
                    for b in parabolic[J]:
                        if a ^ b in N and not any(a ^ c in N for c in parabolic[I & J]):
                            return False, {'I': I, 'J': J, 'a': a, 'b': b}
        return True, None
    require(ip({0})[0], 'coordinate parabolics lost intersection property')
    require(not ip(K)[0], 'diagonal quotient unexpectedly has intersection property')
    admissible = [sorted(N) for N in candidates if ip(N)[0]]
    require(admissible == [[0]], 'unexpected admissible kernels')
    # R={3} normally generates K, but even powers 3^2 and3^4 are0.
    # Thus replacing consecutive powers m,m+1 by m,m+2 admits the bottom
    # kernel for both powers while the join of all admissible kernels is not K.
    power = lambda x, m: x if m % 2 else 0
    require(power(3, 2) == power(3, 4) == 0 and power(3, 1) == 3,
            'power witness error')
    return {
        'status': 'PASS',
        'scope': 'Four finite countermodels to false hypothesis weakenings only.',
        'overlapping_supports': {
            'F': [0, 1], 'coordinates': [[0, 1]], 'I': [0], 'J': [0],
            'a': list(swap), 'b': list(swap), 'checked_hypotheses': overlapping,
            'conclusion_a_eq_identity': False},
        'nonseparating_coordinates': {
            'F': [0, 1], 'coordinates': [[0, 0]], 'I': [], 'J': [],
            'a': list(swap), 'b': list(swap), 'checked_hypotheses': nonseparating,
            'conclusion_a_eq_identity': False},
        'nonconsecutive_powers': {
            'W': 'C2 x C2; operation XOR', 'K': sorted(K), 'R': [3],
            'parabolics': {str(i): sorted(v) for i, v in parabolic.items()},
            'm': 2, 'powers': [power(3, 2), power(3, 4)],
            'admissible_kernels': admissible, 'join': [0],
            'target_ip_failure': ip(K)[1], 'conclusion_join_eq_K': False},
        'missing_normal_generation': {
            'same_W_K_P': True, 'R': [], 'power_supply': 'vacuous',
            'normal_closure_R': [0], 'join': [0], 'conclusion_join_eq_K': False}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    require(not args.out.exists() and not args.out.is_symlink(), 'fresh output file required')
    args.out.parent.mkdir(parents=True, exist_ok=True)
    result = controls()
    args.out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'countermodels': 4}))


if __name__ == '__main__':
    main()
