#!/usr/bin/env python3
"""Check supplied F11 matrix certificates; no group or witness search.

Portable adaptation by /root/registration_reuse_review. Arithmetic and witness
predicates are adapted from the independent shared-batch, resume and extended
end-word checkers credited, with exact source hashes, in README.rst and data.
Original model, domains, membership and classification remain imported premises.
"""
import time
ENTERED = time.monotonic()
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import stat
import sys

HERE = Path(__file__).resolve().parent
SECONDS = 125
RSS_LIMIT = 128 * 2**20
READ_LIMIT = 32 * 2**20
PRODUCT_LIMIT = 400000
DATA_BYTES = 1017819
DATA_SHA = '3bda2afe3d12cb7ab669a8e4de66fbcec7602a1797d4805d1baa9a5953e534b6'
CACHE_BYTES = 723387
CACHE_SHA = 'a7733219294aa0a14661c7ffe280c51ee78e72b7c736a7339b9e19f19fc40fbd'
JOB_COUNTS = {12: 685, 15: 3801, 16: 3779, 17: 7455, 19: 694}
BATCH_COUNTS = [('seed', 5661), ('resume1', 9940), ('resume2', 696), ('extended', 55)]
TAG_COUNTS = {'line': 1451, 'commutant': 438, 'pair': 8486, 'prime_end': 5977}
I = tuple(int(i == j) for i in range(7) for j in range(7))
PRODUCTS = 0
READ_BYTES = 0
PEAK_RSS = 0


def require(ok, message):
    if not ok:
        raise ValueError(message)


def resources():
    global PEAK_RSS
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform != 'darwin':
        rss *= 1024
    PEAK_RSS = max(PEAK_RSS, rss)
    require(rss <= RSS_LIMIT and time.monotonic() - ENTERED < SECONDS,
            '125 seconds / 128 MiB sampled resource limit')


def alarm(*unused):
    raise ValueError('125 second wall limit')


def signature(s):
    return (s.st_dev, s.st_ino, s.st_mode, s.st_size, s.st_mtime_ns, s.st_ctime_ns)


def read_file(name, size, digest):
    global READ_BYTES
    resources()
    require(name in ('portabledata.json', 'cache.u8'), 'Only two local data files')
    path = HERE / name
    before = path.lstat()
    require(stat.S_ISREG(before.st_mode) and path.resolve(strict=True) == path
            and before.st_size == size, 'Exact ordinary local file and byte count')
    require(READ_BYTES + size + 1 <= READ_LIMIT, '32 MiB physical read limit')
    with path.open('rb') as stream:
        opened = os.fstat(stream.fileno())
        raw = stream.read(size + 1)
        finished = os.fstat(stream.fileno())
    READ_BYTES += len(raw)
    require(signature(before) == signature(opened) == signature(finished)
            == signature(path.lstat()) and len(raw) == size
            and hashlib.sha256(raw).hexdigest() == digest,
            'Whole stable file with exact SHA256')
    resources()
    return raw


def parse(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'Unique JSON keys')
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=pairs,
                      parse_float=lambda x: (_ for _ in ()).throw(ValueError(x)),
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


def integer(x, low, high):
    return type(x) is int and low <= x <= high


def vector(raw, length):
    require(type(raw) is list and len(raw) == length
            and all(integer(x, 0, 10) for x in raw), 'Canonical F11 vector')
    return tuple(raw)


def matrix(raw):
    require(type(raw) is list and len(raw) == 7
            and all(type(row) is list and len(row) == 7 for row in raw),
            'Complete 7 by 7 matrix')
    return vector([x for row in raw for x in row], 49)


def multiply(x, y):
    """Ordinary row by column multiplication over F11."""
    global PRODUCTS
    PRODUCTS += 1
    require(PRODUCTS <= PRODUCT_LIMIT, '400000 matrix product limit')
    if PRODUCTS % 128 == 0:
        resources()
    columns = tuple(y[j::7] for j in range(7))
    out = []
    for i in range(0, 49, 7):
        row = x[i:i+7]
        for col in columns:
            out.append((row[0]*col[0] + row[1]*col[1] + row[2]*col[2]
                        + row[3]*col[3] + row[4]*col[4] + row[5]*col[5]
                        + row[6]*col[6]) % 11)
    return tuple(out)


def power(x, exponent):
    require(integer(exponent, 0, 128), 'Bounded nonnegative exponent')
    out = I
    while exponent:
        if exponent & 1:
            out = multiply(out, x)
        exponent //= 2
        if exponent:
            x = multiply(x, x)
    return out


def row_image(v, g):
    return tuple(sum(v[k] * g[7*k+j] for k in range(7)) % 11 for j in range(7))


def invertible(g):
    """Seven columns of modular Gaussian elimination; no group enumeration."""
    rows = [list(g[i:i+7]) for i in range(0, 49, 7)]
    rank = 0
    for column in range(7):
        pivot = next((i for i in range(rank, 7) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][column], -1, 11)
        rows[rank] = [x*inv % 11 for x in rows[rank]]
        for i in range(rank+1, 7):
            t = rows[i][column]
            rows[i] = [(x-t*y) % 11 for x, y in zip(rows[i], rows[rank])]
        rank += 1
    return rank == 7


def witness(raw, marks, ambient):
    require(type(raw) is list and raw and type(raw[0]) is str,
            'Tagged supplied witness')
    a, b, c, e = marks
    tag = raw[0]
    if tag == 'line':
        require(len(raw) == 5, 'Line witness fields')
        _, raw_v, signs, t, minor = raw
        v = vector(raw_v, 7)
        require(any(v) and type(signs) is list and len(signs) == 4
                and all(type(x) is int and x in (1, 10) for x in signs),
                'Nonzero line and four involution eigenvalues')
        require(integer(t, 0, 1) and type(minor) is list and len(minor) == 2
                and all(integer(x, 0, 6) for x in minor) and minor[0] < minor[1],
                'Ambient matrix and two-coordinate minor')
        for g, sign in zip(marks, signs):
            require(row_image(v, g) == tuple(sign*x % 11 for x in v),
                    'Every mark preserves the supplied line')
        moved = row_image(v, ambient[t])
        i, j = minor
        require((v[i]*moved[j] - v[j]*moved[i]) % 11 != 0,
                'Supplied minor proves an ambient matrix moves the line')
    elif tag == 'commutant':
        require(len(raw) == 4, 'Commutant witness fields')
        _, raw_x, t, at = raw
        x = vector(raw_x, 49)
        require(integer(t, 0, 1) and integer(at, 0, 48), 'Ambient commutator entry')
        for g in marks:
            require(multiply(x, g) == multiply(g, x), 'Every mark commutes with X')
        left, right = multiply(x, ambient[t]), multiply(ambient[t], x)
        require(left[at] != right[at], 'An ambient matrix does not commute with X')
    elif tag == 'pair':
        require(len(raw) == 6, 'Pair witness fields')
        _, case, k, epsilon, j, eta = raw
        require(integer(case, 0, 2) and integer(k, 0, 127)
                and integer(j, 0, 127) and integer(epsilon, 0, 1)
                and integer(eta, 0, 1), 'Bounded dihedral word descriptors')
        choices = (((a, b), (b, c), (I, b)),
                   ((b, c), (c, e), (I, c)),
                   ((a, b), (c, e), (I,)))
        (s, t), (u, v), forbidden = choices[case]
        left = power(multiply(s, t), k)
        right = power(multiply(u, v), j)
        if epsilon:
            left = multiply(left, s)
        if eta:
            right = multiply(right, u)
        require(left == right and left not in forbidden,
                'Equal supplied words violate the required pair intersection')
    elif tag == 'prime_end':
        require(len(raw) == 4 and integer(raw[1], 0, 1), 'Single three-mark end')
        allowed = (0, 1, 2) if raw[1] == 0 else (1, 2, 3)
        for item, prime, cofactor in zip(raw[2:], (19, 37), (14, 6)):
            require(type(item) is list and len(item) == 2
                    and type(item[0]) is list and 1 <= len(item[0]) <= 18
                    and all(type(x) is int and x in allowed for x in item[0])
                    and type(item[1]) is int and item[1] == cofactor,
                    'Literal word of length at most18 wholly in the same end')
            value = I
            for letter in item[0]:
                value = multiply(value, marks[letter])
            y = power(value, cofactor)
            require(y != I and power(y, prime) == I,
                    'Supplied power has exact prime order19 or37')
    else:
        raise ValueError('Unknown positive tag')
    return tag


def main():
    require(len(sys.argv) == 1, 'No arguments; stdout receipt only')
    signal.signal(signal.SIGALRM, alarm)
    signal.setitimer(signal.ITIMER_REAL, max(.001, SECONDS-(time.monotonic()-ENTERED)))
    raw = read_file('portabledata.json', DATA_BYTES, DATA_SHA)
    data = parse(raw)
    del raw
    resources()
    require(data['schema'] == 'PORTABLE_F11_SHARED_OBSTRUCTIONS_V1'
            and data['field'] == 11 and data['dimension'] == 7
            and data['catalogue_count'] == 14763, 'Exact shared F11 data schema')
    require(data['fixed_prefix_order'] == ['a', 'e', 'b']
            and data['mark_order'] == ['a', 'b', 'candidate_final', 'e'],
            'Original fixed and marked orders')
    require(data['cache']['file'] == 'cache.u8'
            and data['cache']['bytes'] == CACHE_BYTES
            and data['cache']['sha256'] == CACHE_SHA, 'Exact raw cache pin')
    buf = read_file('cache.u8', CACHE_BYTES, CACHE_SHA)
    require(len(buf) == 14763*49 and all(x < 11 for x in buf),
            '14763 canonical row-major uint8 F11 matrices')
    catalogue = [tuple(buf[i:i+49]) for i in range(0, len(buf), 49)]
    del buf
    for g in catalogue:
        require(g != I and multiply(g, g) == I, 'Every cached matrix is a nonidentity involution')
    require(type(data['ambient_generators']) is list
            and len(data['ambient_generators']) == 2, 'Two supplied ambient matrices')
    ambient = tuple(matrix(g) for g in data['ambient_generators'])
    require(all(invertible(g) for g in ambient), 'Ambient matrices are invertible')
    require(type(data['jobs']) is list and len(data['jobs']) == 5, 'Five original jobs')
    jobs = {}
    eligible = set()
    for job in data['jobs']:
        identifier = job['job']
        require(type(identifier) is list and len(identifier) == 2
                and type(identifier[0]) is int and identifier[0] in JOB_COUNTS
                and type(identifier[1]) is int and identifier[1] == 4
                and identifier[0] not in jobs, 'Unique original job and rank4')
        prefix = identifier[0]
        require(type(job['fixed_prefix']) is list and len(job['fixed_prefix']) == 3,
                'Original three fixed matrices')
        a, e, b = tuple(matrix(g) for g in job['fixed_prefix'])
        for g in (a, e, b):
            require(g != I and multiply(g, g) == I, 'Fixed nonidentity involutions')
        require(multiply(a, e) == multiply(e, a)
                and multiply(b, e) == multiply(e, b), 'Fixed distant commutations')
        orbits = job['orbits']
        require(type(orbits) is list and len(orbits) == JOB_COUNTS[prefix],
                'Exact original indexed row count')
        reps = set()
        for index, row in enumerate(orbits, 1):
            require(type(row) is list and len(row) == 3
                    and integer(row[0], 1, 14763)
                    and all(type(x) is int and x > 0 for x in row[1:])
                    and row[0] not in reps, 'Original representative, orbit size and stabilizer order')
            reps.add(row[0])
            c = catalogue[row[0]-1]
            require(multiply(a, c) == multiply(c, a), 'Every original row has distant a,c commutation')
            eligible.add((prefix, index))
        jobs[prefix] = (a, b, e, orbits)
    require(set(jobs) == set(JOB_COUNTS) and len(eligible) == 16414,
            'All original indexed positions represented exactly once')
    batches = data['positive_batches']
    require(type(batches) is list and len(batches) == len(BATCH_COUNTS), 'Four supplied positive batches')
    tags = dict.fromkeys(TAG_COUNTS, 0)
    per_job = dict.fromkeys(JOB_COUNTS, 0)
    for batch, (name, count) in zip(batches, BATCH_COUNTS):
        require(batch['name'] == name and batch['count'] == count
                and type(batch['records']) is list and len(batch['records']) == count,
                'Exact positive batch and count')
        batch_tags = {}
        for row in batch['records']:
            require(type(row) is list and len(row) == 4
                    and all(type(x) is int for x in row[:3]), 'Original positive position')
            prefix, index, rep, cert = row
            key = (prefix, index)
            require(key in eligible and prefix in jobs, 'Unique remaining original positive index')
            a, b, e, orbits = jobs[prefix]
            require(orbits[index-1][0] == rep, 'Exact original representative join')
            tag = witness(cert, (a, b, catalogue[rep-1], e), ambient)
            tags[tag] += 1
            batch_tags[tag] = batch_tags.get(tag, 0) + 1
            per_job[prefix] += 1
            eligible.remove(key)
        require(batch_tags == batch['tags'], 'Every advertised tag count recomputed')
        resources()
    missing = data['unresolved']
    require(type(missing) is list and len(missing) == 62, 'All62 unresolved rows explicit')
    remaining = []
    for row in missing:
        require(type(row) is list and len(row) == 3
                and all(type(x) is int for x in row), 'Original unresolved position')
        prefix, index, rep = row
        require((prefix, index) in eligible and jobs[prefix][3][index-1][0] == rep,
                'Exact unresolved original index and representative')
        remaining.append((prefix, index))
    require(remaining == sorted(set(remaining)) and set(remaining) == eligible,
            'Disjoint positives plus unresolved exactly partition all16414 rows')
    require(tags == TAG_COUNTS and sum(per_job.values()) == 16352,
            'All16352 supplied arithmetic certificates checked')
    read_file('portabledata.json', DATA_BYTES, DATA_SHA)
    read_file('cache.u8', CACHE_BYTES, CACHE_SHA)
    resources()
    receipt = dict(status='PASS_SUPPLIED_F11_MATRIX_ARITHMETIC', original_indexed_rows=16414,
                   checked_positive_rows=16352, unresolved_rows=62, tags=tags,
                   jobs=[dict(job=[p, 4], rows=JOB_COUNTS[p], positives=per_job[p],
                              unresolved=JOB_COUNTS[p]-per_job[p]) for p in sorted(jobs)],
                   matrix_products=PRODUCTS, product_limit=PRODUCT_LIMIT,
                   physical_input_bytes_read=READ_BYTES, read_limit_bytes=READ_LIMIT,
                   seconds=time.monotonic()-ENTERED, wall_limit_seconds=SECONDS,
                   sampled_peak_rss_bytes=PEAK_RSS, sampled_rss_limit_bytes=RSS_LIMIT,
                   original_model_and_domain_reacquired=False, classification_reproved=False,
                   original_manuscript_or_conjecture_claim=False,
                   Lean_claim=False, compression_measurement_claim=False)
    signal.setitimer(signal.ITIMER_REAL, 0)
    print(json.dumps(receipt, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
