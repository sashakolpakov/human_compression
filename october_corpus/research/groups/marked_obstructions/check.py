"""Check the bundled F_11 marked-matrix obstruction certificates.

Portable packaging: /root/registration_reuse_review. Column-dot arithmetic
and bounded input checks adapt the independently reviewed word checkers;
see README.rst for attribution, source pins and imported group premises.
No project module, private path, group enumeration or search is used.
"""
import time

STARTED = time.monotonic()
import argparse
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import stat
import sys

HERE = Path(__file__).resolve().parent
DATA = HERE / "certificates.json"
DATA_BYTES = 137867
DATA_SHA256 = "2ea8e82737c92f6c5a101ca0d5852a0b875aadd8fb6229f512b8894325dbb835"
FIXTURE_BYTES = 100429
FIXTURE_SHA256 = "b2a2d44f31a4a2ae66e3bd7af29e1e22dc00a4a1649c8fbab7e386978395ad14"
P, N, ORBITS = 11, 7, 694
WALL_SECONDS, RSS_BYTES, READ_BYTES = 60, 128 * 2**20, 2**20
PAIR_CASES = ((0, 1, 1, 2), (1, 2, 2, 3), (0, 1, 2, 3))
SHARED = (1, 2, None)


def need(condition, message):
    if not condition:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")


def decode(raw):
    def pairs(items):
        value = {}
        for key, item in items:
            need(key not in value, "duplicate JSON key")
            value[key] = item
        return value

    def nonfinite(value):
        raise ValueError("nonfinite JSON: " + value)

    return json.loads(raw, object_pairs_hook=pairs, parse_constant=nonfinite)


def matrix(value):
    need(type(value) is list and len(value) == N
         and all(type(row) is list and len(row) == N
                 and all(type(x) is int and 0 <= x < P for x in row)
                 for row in value), "canonical 7x7 matrix over F_11")
    return tuple(tuple(row) for row in value)


def vector(value):
    need(type(value) is list and len(value) == N
         and all(type(x) is int and 0 <= x < P for x in value),
         "canonical seven-coordinate row vector")
    return tuple(value)


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    parser.add_argument("--out", type=Path,
                        help="optional fresh result outside this package")
    args = parser.parse_args()

    def timeout(*unused):
        raise TimeoutError("whole 60-second check limit")

    signal.signal(signal.SIGALRM, timeout)
    signal.setitimer(signal.ITIMER_REAL,
                     max(.001, WALL_SECONDS - (time.monotonic() - STARTED)))
    peak, products, bytes_read = 0, 0, 0

    def tick():
        nonlocal peak
        need(time.monotonic() - STARTED < WALL_SECONDS, "whole 60-second limit")
        used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        used *= 1 if sys.platform == "darwin" else 1024
        peak = max(peak, used)
        need(used < RSS_BYTES, "sampled own RSS below 128 MiB")

    def read_data():
        nonlocal bytes_read
        tick()
        before = DATA.lstat()
        need(stat.S_ISREG(before.st_mode) and DATA.resolve(strict=True) == DATA
             and before.st_size == DATA_BYTES, "ordinary bounded local data")
        need(bytes_read + DATA_BYTES <= READ_BYTES, "whole 1 MiB file-read cap")
        signature = lambda s: (s.st_dev, s.st_ino, s.st_mode, s.st_size,
                               s.st_mtime_ns, s.st_ctime_ns)
        with DATA.open("rb") as handle:
            opened = os.fstat(handle.fileno())
            raw = handle.read(DATA_BYTES + 1)
            after = os.fstat(handle.fileno())
        need(signature(before) == signature(opened) == signature(after)
             == signature(DATA.lstat()) and len(raw) == DATA_BYTES
             and hashlib.sha256(raw).hexdigest() == DATA_SHA256,
             "stable complete bundled data and SHA256")
        bytes_read += len(raw)
        return raw

    def multiply(left, right):
        nonlocal products
        tick()
        need(products < 20000, "bounded supplied-certificate products")
        columns = tuple(zip(*right))
        result = tuple(tuple(sum(x*y for x, y in zip(row, column)) % P
                             for column in columns) for row in left)
        products += 1
        return result

    def action(row, mat):
        tick()
        return tuple(sum(row[k]*mat[k][j] for k in range(N)) % P
                     for j in range(N))

    def invertible(mat):
        # Ordinary elimination, used only for the two ambient matrices.
        rows = [list(row) for row in mat]
        for column in range(N):
            tick()
            pivot = next((i for i in range(column, N)
                          if rows[i][column] != 0), None)
            if pivot is None:
                return False
            rows[column], rows[pivot] = rows[pivot], rows[column]
            scale = pow(rows[column][column], P - 2, P)
            rows[column] = [x*scale % P for x in rows[column]]
            for i in range(column + 1, N):
                coefficient = rows[i][column]
                rows[i] = [(x - coefficient*y) % P
                           for x, y in zip(rows[i], rows[column])]
        return True

    raw = read_data()
    data = decode(raw)
    need(data["schema"] == "PORTABLE_F11_MARKED_OBSTRUCTIONS_V1",
         "this package's certificate schema")
    fixture = data["fixture"]
    original = canonical(fixture) + b"\n"
    need(len(original) == FIXTURE_BYTES
         and hashlib.sha256(original).hexdigest() == FIXTURE_SHA256,
         "whole original fixture reconstructed from ordinary JSON")
    need(fixture["original_job"] == [11, 4] and fixture["field"] == P
         and fixture["dimension"] == N and fixture["original_orbit_count"] == ORBITS
         and fixture["fixed_prefix_labels"] == ["a", "e", "b"]
         and fixture["reconstructed_mark_order"] == ["a", "b", "candidate_final", "e"],
         "specified fixture and mark convention")
    fixed = tuple(matrix(value) for value in fixture["fixed_prefix"])
    ambient = tuple(matrix(value) for value in fixture["ambient_generators"])
    need(len(fixed) == 3 and len(ambient) == 2
         and all(invertible(value) for value in ambient),
         "three fixed marks and two invertible ambient matrices")
    rows, representatives = {}, {}
    need(type(fixture["candidates"]) is list
         and len(fixture["candidates"]) == ORBITS, "all 694 included rows")
    for i, item in enumerate(fixture["candidates"], 1):
        need(type(item) is list and len(item) == 3 and type(item[0]) is int
             and item[0] == i and type(item[1]) is int and 1 <= item[1] <= 14763,
             "orbit index and catalogue representative are different fields")
        rows[i], representatives[i] = matrix(item[2]), item[1]
    need(len(set(representatives.values())) == ORBITS,
         "694 distinct included representative labels")
    identity = tuple(tuple(int(i == j) for j in range(N)) for i in range(N))
    for value in fixed + tuple(rows.values()):
        need(value != identity and multiply(value, value) == identity,
             "all included marks are nonidentity involutions")

    def marks(i):
        need(type(i) is int and i in rows, "included original row index")
        return fixed[0], fixed[2], rows[i], fixed[1]

    line_indices = []
    for record in data["line_certificates"]:
        i = record["orbit"]
        marked = marks(i)
        v = vector(record["line"])
        scalars, generator, minor = (record[k] for k in
                                     ("eigenvalues", "ambient_generator", "minor"))
        need(any(v) and type(scalars) is list and len(scalars) == 4
             and all(type(x) is int and x in (1, 10) for x in scalars)
             and type(generator) is int and generator in (0, 1),
             "nonzero supplied line and four nonzero eigenvalues")
        for mat, scalar in zip(marked, scalars):
            need(action(v, mat) == tuple(scalar*x % P for x in v),
                 "each full marked row-vector eigenidentity")
        image = action(v, ambient[generator])
        need(type(minor) is list and len(minor) == 3
             and all(type(x) is int for x in minor)
             and 0 <= minor[0] < minor[1] < N and 1 <= minor[2] < P,
             "advertised nonzero two-coordinate minor")
        j, k, value = minor
        need((v[j]*image[k] - v[k]*image[j]) % P == value,
             "ambient matrix moves the preserved line")
        line_indices.append(i)

    def pair_word(x, y, exponent, suffix):
        need(type(exponent) is int and 0 <= exponent < 128
             and type(suffix) is int and suffix in (0, 1),
             "bounded supplied alternating word")
        value, power = identity, multiply(x, y)
        while exponent:
            if exponent & 1:
                value = multiply(value, power)
            exponent >>= 1
            if exponent:
                power = multiply(power, power)
        return multiply(value, x) if suffix else value

    pair_indices = []
    for record in data["pair_word_certificates"]:
        need(type(record) is list and len(record) == 6
             and all(type(x) is int for x in record), "six integer pair-word fields")
        i, case, lk, le, rk, re = record
        need(0 <= case < len(PAIR_CASES), "one of three declared pair cases")
        marked = marks(i)
        a, b, c, d = PAIR_CASES[case]
        left = pair_word(marked[a], marked[b], lk, le)
        right = pair_word(marked[c], marked[d], rk, re)
        shared = SHARED[case]
        need(left == right and left != identity
             and (shared is None or left != marked[shared]),
             "common value outside the required shared subgroup")
        pair_indices.append(i)

    def digit_word(marked, text, allowed, bound):
        need(type(text) is str and 1 <= len(text) <= bound
             and all(x in allowed for x in text), "supplied word in its declared end")
        value = identity
        for digit in text:
            value = multiply(value, marked[ord(digit) - ord("0")])
        return value

    end_indices, endpoints, overlaps = [], 0, 0
    for record in data["parabolic_word_certificates"]:
        need(type(record) is list and len(record) in (4, 5)
             and type(record[1]) is int and record[1] in (0, 1),
             "endpoint or overlap certificate")
        i, kind = record[:2]
        marked = marks(i)
        if kind == 0:
            need(len(record) == 4 and type(record[2]) is int
                 and record[2] in (0, 3), "omitted endpoint")
            target, word = record[2:]
            value = digit_word(marked, word, "123" if target == 0 else "012", 20)
            need(value == marked[target] and value != identity,
                 "opposite-end word equals omitted nonidentity mark")
            endpoints += 1
        else:
            need(len(record) == 5 and type(record[4]) is int
                 and 1 <= record[4] <= 128, "supplied closing period")
            left, right, period = record[2:]
            value = digit_word(marked, left, "012", 10)
            need(value == digit_word(marked, right, "123", 10),
                 "the two end words agree as whole matrices")
            rotation = multiply(marked[1], marked[2])
            power = identity
            for unused in range(period):
                power = multiply(power, rotation)
            need(power == identity, "supplied period closes; no order search")
            power, equalities = identity, 0
            for unused in range(period):
                equalities += int(value == power)
                equalities += int(value == multiply(power, marked[1]))
                power = multiply(power, rotation)
            need(equalities == 0, "outside every one of the 2m literal normal forms")
            overlaps += 1
        end_indices.append(i)

    need(len(line_indices) == len(set(line_indices)) == 220
         and len(pair_indices) == len(set(pair_indices)) == 314
         and len(end_indices) == len(set(end_indices)) == 4
         and endpoints == 3 and overlaps == 1, "retained certificate counts")
    groups = list(map(set, (line_indices, pair_indices, end_indices)))
    union = set.union(*groups)
    need(len(union) == sum(map(len, groups)) == 538,
         "three obstruction lists have disjoint original indices")
    unresolved = set(range(1, ORBITS + 1)) - union
    need(len(unresolved) == 156, "156 rows have no supplied obstruction here")
    need(read_data() == raw, "bundled input unchanged after complete checking")
    tick()
    result = dict(status="PASS_BUNDLED_MATRIX_OBSTRUCTIONS", field=P, dimension=N,
                  included_rows=ORBITS, line_obstructions=220, pair_word_obstructions=314,
                  endpoint_obstructions=endpoints, overlap_obstructions=overlaps,
                  disjoint_obstructed_rows=538, unresolved_rows=156,
                  original_group_correspondence_reproved=False,
                  full_original_or_census_claim=False, Lean_claim=False,
                  compression_measurement_claim=False,
                  data_sha256=DATA_SHA256, matrix_products=products,
                  seconds=time.monotonic() - STARTED, sampled_peak_rss_bytes=peak,
                  wall_limit_seconds=WALL_SECONDS, sampled_rss_limit_bytes=RSS_BYTES)
    encoded = canonical(result) + b"\n"
    if args.out is not None:
        target = args.out.expanduser().absolute()
        need(target.parent.resolve(strict=True) == target.parent
             and not target.is_relative_to(HERE) and not os.path.lexists(target),
             "optional output must be a fresh file outside the package")
        with target.open("xb") as handle:
            need(handle.write(encoded) == len(encoded), "complete optional result")
    print(encoded.decode("ascii"), end="")
    signal.setitimer(signal.ITIMER_REAL, 0)


if __name__ == "__main__":
    main()
