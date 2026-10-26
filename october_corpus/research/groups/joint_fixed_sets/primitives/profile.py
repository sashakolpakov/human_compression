"""Finite premises on complete original permutations; no group or field code.

All work uses the caller's one shared budget. Producer escape discovery and
Saved's direct certificate relation are deliberately separate functions.
"""
import hashlib


def need(ok, message):
    if not ok:
        raise ValueError(message)


def typed_equal(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return a.keys() == b.keys() and all(typed_equal(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(typed_equal(x, y) for x, y in zip(a, b))
    return a == b


def decode_pair(raw, degree, decoder, budget):
    """The borrowed Cursor/permutation bodies remain at their exact identity."""
    budget.bytes(len(raw), 8)
    cursor = decoder['Cursor'](raw)
    for token in ('fixedPair', ':=', '['):
        cursor.token(token)
    a = decoder['permutation'](cursor, degree, budget)
    cursor.token(',')
    e = decoder['permutation'](cursor, degree, budget)
    for token in (']', ';', ';'):
        cursor.token(token)
    cursor.space()
    need(cursor.at == len(cursor.text), 'whole fixedPair grammar and EOF')
    budget.charge(0)
    return a, e


def permutation_checks(vector, degree, budget):
    need(type(degree) is int and 1 <= degree <= 37449 and len(vector) == degree,
         'entire explicit permutation degree')
    budget.charge(degree)
    seen = bytearray(degree + 1)
    for value in vector:
        budget.charge(3)
        need(type(value) is int and 1 <= value <= degree and not seen[value],
             'all images typed, in range and unique')
        seen[value] = 1
    # The degree distinct values in the degree-sized domain prove surjectivity.
    budget.charge(0)


def vector_digest(vector, budget):
    budget.charge(4 * len(vector))
    h = hashlib.sha256()
    for value in vector:
        h.update(value.to_bytes(4, 'little', signed=False))
    budget.charge(0)
    return h.hexdigest()


def scan(a, e, degree, budget):
    permutation_checks(a, degree, budget)
    permutation_checks(e, degree, budget)
    budget.charge(2 * degree)
    fa, fe = bytearray(degree), bytearray(degree)
    counts = [0, 0, 0]
    for i in range(degree):
        budget.charge(20)
        x, y, p = a[i], e[i], i + 1
        need(a[x - 1] == p and e[y - 1] == p, 'whole endpoint involutions')
        need(a[y - 1] == e[x - 1], 'whole endpoint commutation')
        xa, xe = x == p, y == p
        fa[i], fe[i] = xa, xe
        counts[0] += xa
        counts[1] += xe
        counts[2] += xa and xe
    result = dict(degree=degree, endpoint_vector_hashes=[vector_digest(a, budget), vector_digest(e, budget)],
                  fixed_A=counts[0], fixed_E=counts[1], common_fixed=counts[2],
                  all_images_bijections=True, both_involutions=True, endpoints_commute=True)
    budget.charge(0)
    return result, fa, fe


def discover_escape(fa, fe, ambient, budget):
    """Untrusted supplier policy; no minimality or search-work claim is emitted."""
    for k, g in enumerate(ambient):
        for i in range(len(fa)):
            budget.charge(6)
            q = g[i]
            if fa[i] and fe[i] and not (fa[q - 1] and fe[q - 1]):
                return dict(original_generator_index=k + 1, point=i + 1, image=q)
    budget.charge(0)
    return None


def valid_escape(witness, fa, fe, ambient, budget):
    need(type(witness) is dict and set(witness) == {'original_generator_index', 'point', 'image'},
         'exact escape fields')
    k, p, q = (witness[x] for x in ('original_generator_index', 'point', 'image'))
    budget.charge(16)
    need(type(k) is type(p) is type(q) is int and 1 <= k <= len(ambient)
         and 1 <= p <= len(fa) and 1 <= q <= len(fa), 'typed original escape indices')
    need(ambient[k - 1][p - 1] == q and fa[p - 1] and fe[p - 1]
         and not (fa[q - 1] and fe[q - 1]), 'actual ambient projective-set escape')


def proposed(base, fa, fe, ambient, diagonal_clause, budget):
    counts = (base['fixed_A'], base['fixed_E'], base['common_fixed'])
    status, escape = 'VALID_PROFILE_WITHOUT_APPLICATION', None
    if base['degree'] == 37449 and counts == (73, 73, 9) and diagonal_clause is True:
        status = 'DISTINCT_MAXIMAL_PROFILE'
    elif base['degree'] == 37449 and counts == (73, 73, 73):
        escape = discover_escape(fa, fe, ambient, budget)
        if escape is not None:
            status = 'COMMON_MAXIMAL_PROFILE_WITH_ESCAPE'
    return dict(**base, status=status, escape=escape)


def verified(supplied, base, fa, fe, ambient, diagonal_clause, budget):
    """ANY valid supplied escape is accepted; the supplier is never called."""
    need(type(supplied) is dict and set(supplied) == set(base) | {'status', 'escape'}, 'entire profile record')
    need(all(typed_equal(supplied[k], value) for k, value in base.items()), 'all recomputed complete counts, digests and relations')
    counts = (base['fixed_A'], base['fixed_E'], base['common_fixed'])
    status, escape = supplied['status'], supplied['escape']
    if status == 'DISTINCT_MAXIMAL_PROFILE':
        need(base['degree'] == 37449 and counts == (73, 73, 9) and diagonal_clause is True and escape is None, 'exact distinct-maximal premises')
    elif status == 'COMMON_MAXIMAL_PROFILE_WITH_ESCAPE':
        need(base['degree'] == 37449 and counts == (73, 73, 73), 'exact common-maximal premises')
        valid_escape(escape, fa, fe, ambient, budget)
    elif status == 'VALID_PROFILE_WITHOUT_APPLICATION':
        need(escape is None, 'unpaid profile makes no absence-of-escape claim')
    else:
        raise ValueError('unknown profile status')
    budget.charge(0)
    return dict(**base, status=status, escape=escape)
