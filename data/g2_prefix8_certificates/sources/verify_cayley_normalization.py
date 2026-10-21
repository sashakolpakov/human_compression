"""Pure GF11 Cayley normalization certificate; Root admission is external.

Input is the existing F004_GF11_INVARIANT_TENSOR_CANDIDATES_V1 JSON schema.
No generator invariance, named-group/order, candidate or census claim is made.
Preparation must never invoke this verifier on actual data.
"""
import argparse
import fcntl
import hashlib
from itertools import combinations, combinations_with_replacement, permutations
import json
import os
from pathlib import Path
import resource
import stat
import sys
import time

P, D = 11, 7
TRIPLES = tuple(combinations(range(D), 3))
PAIRS = tuple(combinations_with_replacement(range(D), 2))
INPUT_CAP = OUTPUT_CAP = 65536


def need(ok, message):
    if not ok:
        raise ValueError(message)


def vector(value, length, name):
    need(type(value) is list and len(value) == length
         and all(type(x) is int and 0 <= x < P for x in value), name)
    return tuple(value)


def matrix(value, name):
    need(type(value) is list and len(value) == D, name)
    return tuple(vector(row, D, name) for row in value)


def inverse(matrix_value):
    work = [list(row) + [int(i == j) for j in range(D)]
            for i, row in enumerate(matrix_value)]
    for column in range(D):
        pivot = next((i for i in range(column, D) if work[i][column]), None)
        need(pivot is not None, 'nonsingular beta')
        work[column], work[pivot] = work[pivot], work[column]
        scale = pow(work[column][column], -1, P)
        work[column] = [x * scale % P for x in work[column]]
        for i in range(D):
            if i != column:
                scale = work[i][column]
                work[i] = [(x - scale * y) % P for x, y in zip(work[i], work[column])]
    return [row[D:] for row in work]


def certify(data, *, checkpoint):
    """Return all coefficients only after the complete196-relation check."""
    need(type(data) is dict
         and data.get('schema') == 'F004_GF11_INVARIANT_TENSOR_CANDIDATES_V1'
         and data.get('status') == 'PRODUCED_INVARIANT_TENSOR_CANDIDATES'
         and data.get('field') == P and data.get('dimension') == D
         and data.get('ordered_generators') == 2, 'exact existing q11 candidate schema')
    for name, expected in [('alternating_coefficient_order', TRIPLES),
                           ('symmetric_coefficient_order', PAIRS)]:
        order = data.get(name)
        need(type(order) is list and len(order) == len(expected)
             and all(type(row) is list and len(row) == len(wanted)
                     and all(type(x) is int for x in row) and row == list(wanted)
                     for row, wanted in zip(order, expected)),
             'original canonical increasing coefficient orders')
    beta = matrix(data.get('beta'), 'canonical beta7-by-7')
    tau = vector(data.get('tau'), 35, 'canonical35 alternating coefficients')
    need(all(beta[i][j] == beta[j][i] for i in range(D) for j in range(D)), 'symmetric beta')
    need(any(tau), 'nonzero tau')
    inv = inverse(beta)
    tensor = [[[0] * D for _ in range(D)] for _ in range(D)]
    for triple, value in zip(TRIPLES, tau):
        for order in permutations(range(3)):
            sign = -1 if sum(order[i] > order[j] for i in range(3)
                             for j in range(i + 1, 3)) % 2 else 1
            i, j, k = (triple[t] for t in order)
            tensor[i][j][k] = sign * value % P
    cross = [[[sum(tensor[i][j][k] * inv[k][r] for k in range(D)) % P
               for r in range(D)] for j in range(D)] for i in range(D)]

    def pair(x, y):
        return sum(x[i] * beta[i][j] * y[j] for i in range(D) for j in range(D)) % P

    def product(x, y):
        return tuple(sum(x[i] * y[j] * cross[i][j][r]
                         for i in range(D) for j in range(D)) % P for r in range(D))

    units = [tuple(int(i == j) for j in range(D)) for i in range(D)]
    xs = [(units[i], [i]) for i in range(D)]
    xs += [(tuple(int(r in (i, j)) for r in range(D)), [i, j])
           for i, j in combinations(range(D), 2)]
    relations, witness = [], None
    for x, support in xs:
        for j, y in enumerate(units):
            checkpoint()
            left = product(x, product(x, y))
            xy, xx = pair(x, y), pair(x, x)
            right = tuple((xy * x[r] - xx * y[r]) % P for r in range(D))
            relations.append((left, right))
            if witness is None:
                for r in range(D):
                    if right[r]:
                        witness = dict(x_support=support, y_index=j, output_coordinate=r,
                                       left=left[r], right=right[r])
                        break
    need(len(relations) == 196 and witness is not None, 'complete196 relations and nonzero coefficient')
    kappa = witness['left'] * pow(witness['right'], -1, P) % P
    need(kappa != 0, 'nonzero kappa')
    for number, (left, right) in enumerate(relations):
        checkpoint()
        need(all(left[r] == kappa * right[r] % P for r in range(D)),
             'double-cross identity at relation' + str(number))
    pure = [[kappa * beta[i][j] % P for j in range(D)] for i in range(D)]
    quadratic = [[0] * 8 for _ in range(8)]
    quadratic[0][0] = 1
    multiplication = [[[0] * 8 for _ in range(8)] for _ in range(8)]
    for i in range(8):
        multiplication[0][i][i] = multiplication[i][0][i] = 1
    for i in range(D):
        for j in range(D):
            quadratic[i + 1][j + 1] = pure[i][j]
            multiplication[i + 1][j + 1][0] = -pure[i][j] % P
            multiplication[i + 1][j + 1][1:] = cross[i][j]
    checkpoint()
    return dict(status='CERTIFIED_GF11_SPLIT_CAYLEY_COMPOSITION', certificate_verified=True,
        kappa=kappa, kappa_coefficient_witness=witness, vector_identities_checked=196,
        scalar_identities_checked=1372, pure_quadratic_form_matrix=pure,
        quadratic_form_matrix=quadratic,
        full_polar_form_matrix=[[2 * x % P for x in row] for row in quadratic],
        normalized_alternating_coefficients=[kappa * x % P for x in tau],
        multiplication_tensor=multiplication,
        coordinates='[scalar,v0,v1,v2,v3,v4,v5,v6]; right row coordinates',
        multiplication_tensor_convention='tensor[i][j][r] is coefficient of e_r in e_i*e_j',
        quadratic_matrix_convention='N(x)=x*Q*transpose(x); full polar matrix=2*Q')


def exact_json(path, digest):
    need(path.is_absolute(), 'absolute input path')
    a = path.lstat()
    need(stat.S_ISREG(a.st_mode) and a.st_nlink == 1 and a.st_size <= INPUT_CAP,
         'ordinary input at most64KiB')
    with path.open('rb') as stream:
        if sys.platform == 'darwin':
            fcntl.fcntl(stream.fileno(), 48, 1)
        b = os.fstat(stream.fileno())
        raw = stream.read(INPUT_CAP + 1)
        z = os.fstat(stream.fileno())
    sig = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_nlink, s.st_size,
                     s.st_mtime_ns, s.st_ctime_ns)
    need(sig(a) == sig(b) == sig(z) == sig(path.lstat()) and len(raw) == a.st_size
         and hashlib.sha256(raw).hexdigest() == digest, 'stable exact whole pinned input')
    def pairs(items):
        value = {}
        for key, item in items:
            need(key not in value, 'unique JSON key')
            value[key] = item
        return value
    def constant(text):
        raise ValueError('nonfinite JSON number:' + text)
    return dict(path=str(path), bytes=len(raw), sha256=digest), json.loads(
        raw, object_pairs_hook=pairs, parse_constant=constant)


def main():
    started = time.monotonic()
    ap = argparse.ArgumentParser(allow_abbrev=False, description=__doc__)
    ap.add_argument('--input', type=Path, required=True)
    ap.add_argument('--input-sha256', required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    need(sys.flags.ignore_environment and sys.dont_write_bytecode and not sys.flags.optimize,
         'isolated Python -E -B without optimization')
    need(len(args.input_sha256) == 64 and all(x in '0123456789abcdef' for x in args.input_sha256),
         'canonical input SHA256')
    need(args.output.is_absolute() and not os.path.lexists(args.output)
         and stat.S_ISDIR(args.output.parent.lstat().st_mode), 'fresh output in existing ordinary directory')
    def peak():
        value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        return value if sys.platform == 'darwin' else value * 1024
    def checkpoint():
        if time.monotonic() - started >= 100 or peak() > 128 * 2**20:
            raise RuntimeError('shared100s/observed128MiB bound')
    input_pin = None
    try:
        checkpoint()
        input_pin, data = exact_json(args.input, args.input_sha256)
        outcome = certify(data, checkpoint=checkpoint)
        again, _ = exact_json(args.input, args.input_sha256)
        need(again == input_pin, 'whole input unchanged after arithmetic')
        checkpoint()
    except (ValueError, RuntimeError, OSError) as exc:
        outcome = dict(status='REFUSED_GF11_CAYLEY_COMPOSITION_CERTIFICATE', certificate_verified=False,
                       error=type(exc).__name__ + ': ' + str(exc)[:2048])
    outcome.update(schema='F004_GF11_CAYLEY_NORMALIZATION_CERTIFICATE_V1', field=P,
        imaginary_dimension=D, algebra_dimension=8, input=input_pin,
        generator_invariance_rechecked=False, group_model_identification_certified=False,
        faithful_transport_certified=False, named_group_order_certified=False,
        eight_sign_frames_constructed=False, census_credit=0, candidate_credit=0,
        whole_original_credit=0, seconds=time.monotonic()-started, peak_self_bytes=peak(),
        qualification='Pure composition criterion only. Actual forms/frame/model/order/control/runtime authority '
                      'is external Root input. Refusal or interruption is not a census or nonexistence result.')
    raw = (json.dumps(outcome, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()
    need(len(raw) <= OUTPUT_CAP, 'complete output at most64KiB; no clipping')
    with args.output.open('xb') as stream:
        need(stream.write(raw) == len(raw), 'whole fresh output write')
    print(json.dumps(dict(status=outcome['status'], certificate_verified=outcome['certificate_verified'],
        output=dict(path=str(args.output), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()),
        census_credit=0), sort_keys=True))
    if not outcome['certificate_verified']:
        raise SystemExit(2)


if __name__ == '__main__':
    main()
