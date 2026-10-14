"""Validate the exact finite roster and the theorem's numerical interfaces."""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')


def need(value, message):
    if not value:
        raise ValueError(message)


def sp_order(n, q):
    value = q ** ((n // 2) ** 2)
    for i in range(1, n // 2 + 1):
        value *= q ** (2 * i) - 1
    return value


def validate(report):
    need(report['status'] == 'PASS', 'completed matrix certificate')
    fibres = [(2, m) for m in range(1, 6)] + [(4, m) for m in range(1, 5)] + [(8, m) for m in range(1, 4)]
    need([(r['q'], r['m']) for r in report['fibres']] == fibres, 'complete fibre roster')
    total = 0
    for row in report['fibres']:
        q, m = row['q'], row['m']
        need(row['matrices'] == q ** (m * (m + 1) // 2), 'symmetric inventory')
        need(row['image'] == q ** m // 2, 'trace hyperplane')
        need(row['omega_kernel'] == q ** (m * (m - 1) // 2), 'omega kernel')
        total += row['matrices']
    need(report['symmetric_matrices'] == total == 1349270, 'total matrix inventory')
    frames = [(2, m) for m in range(1, 7)] + [(4, m) for m in range(2, 5)] + [(8, m) for m in range(2, 4)]
    need([(r['q'], r['m']) for r in report['frames']] == frames, 'frame roster')
    for row in report['frames']:
        q, m = row['q'], row['m']
        want = sp_order(m - 1, q) if m % 2 else q ** (m - 1) * sp_order(m - 2, q)
        need(row['J_order'] == want, 'exact orthonormal frame order')
    centralizers = [(q, m, arf) for q, m in [(2, 2), (2, 3), (2, 4), (4, 2), (4, 3), (8, 2)] for arf in (0, 1)]
    need([(r['q'], r['m'], r['arf_parameter']) for r in report['centralizers']] == centralizers, 'both-form centralizer roster')
    actual_nu = {(2, 2): 4, (2, 3): 20, (2, 4): 368, (4, 2): 16, (4, 3): 304, (8, 2): 64}
    total = 0
    for row in report['centralizers']:
        q, m = row['q'], row['m']
        exponent = (m * m - m) // 2 if m % 2 else (m * m + m - 2) // 2
        n = m - 1 if m % 2 else m - 2
        kernel = q ** exponent
        order = kernel * sp_order(n, q)
        bound = kernel * (q * q if n else 1)
        need(row['O_centralizer'] == 2 * order and row['Omega_centralizer'] == order, 'finite component and fibre orders')
        need(row['nu2'] == actual_nu[q, m] <= bound == row['bound'], 'literal involution count and upper bound')
        total += row['O_centralizer']
    need(report['literal_centralizer_matrices'] == total == 28176, 'literal centralizer total')
    return dict(fibre_rows=len(fibres), frame_rows=len(frames), centralizer_rows=len(centralizers),
                symmetric_matrices=1349270, literal_centralizer_matrices=28176)
