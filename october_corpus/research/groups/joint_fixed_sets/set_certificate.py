"""Pure fixed-set certificate relation. STATIC; no main or IO.

Author /root/f009_consumer_lineage. The unchanged profile6f87 supplies
whole bijection validation and u32 vector digests; decoder3beab supplies
the literal permutation reader. Caller owns one shared20s/10M Budget.
Lookup rows are separately authenticated original ambient edges, not an
ambient permutation search or a retagged earlier endpoint fixed set.
"""


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


def decode_third(raw, degree, decoder, budget):
    budget.bytes(len(raw), 8)
    cursor = decoder['Cursor'](raw)
    cursor.token('thirdMark')
    cursor.token(':=')
    b = decoder['permutation'](cursor, degree, budget)
    cursor.token(';')
    cursor.token(';')
    cursor.space()
    need(cursor.at == len(cursor.text), 'whole thirdMark grammar and EOF')
    budget.charge(0)
    return b


def scan(a, e, b, degree, profile, budget):
    """All actual A/E/B relations; AB commutation is deliberately absent."""
    for vector in (a, e, b):
        profile['permutation_checks'](vector, degree, budget)
    ae, ab, triple = [], [], []
    counts = [0, 0, 0]
    for i in range(degree):
        budget.charge(20)
        point = i + 1
        av, ev, bv = a[i], e[i], b[i]
        need(a[av - 1] == point and e[ev - 1] == point and b[bv - 1] == point,
             'all three complete original involutions')
        need(a[ev - 1] == e[av - 1] and b[ev - 1] == e[bv - 1],
             'whole AE and BE original prefix commutation')
        fa, fe, fb = av == point, ev == point, bv == point
        counts[0] += fa
        counts[1] += fe
        counts[2] += fb
        if fa and fe:
            ae.append(point)
        if fa and fb:
            ab.append(point)
        if fa and fe and fb:
            triple.append(point)
    digests = [profile['vector_digest'](v, budget) for v in (a, e, b)]
    budget.charge(0)
    return dict(degree=degree, ordered_mark_roles=['A', 'E', 'B'],
                all_three_bijections=True, all_three_involutions=True,
                AE_commute=True, BE_commute=True, AB_commutation_not_required=True,
                vector_hashes=digests, fixed_A=counts[0], fixed_E=counts[1],
                fixed_B=counts[2], AE_points=ae, AB_points=ab, triple_points=triple,
                AE_count=len(ae), AB_count=len(ab), triple_count=len(triple))


def valid_escape(witness, base, acquired_lookups, budget):
    need(type(acquired_lookups) is list and 1 <= len(acquired_lookups) <= 64,
         'finite complete authenticated lookup vector')
    need(type(witness) is dict and set(witness) == {'original_generator_index', 'point', 'image'},
         'whole exact original ambient lookup witness')
    k, point, image = (witness[n] for n in ('original_generator_index', 'point', 'image'))
    need(type(k) is type(point) is type(image) is int and k >= 1
         and 1 <= point <= base['degree'] and 1 <= image <= base['degree'],
         'original one-based generator and point labels')
    budget.charge(len(acquired_lookups) + len(base['AE_points']) * 2 + 1)
    need(any(typed_equal(witness, row) for row in acquired_lookups),
         'same separately authenticated actual original-generator lookup')
    need(bool(base['AE_points']) and base['AE_points'] == base['AB_points']
         and point in base['AE_points'] and image not in base['AE_points'],
         'complete equal joint fixed sets and actual escape from THIS set')


def proposed(base, acquired_lookups, proposed_witness, budget):
    """Try one explicitly supplied attested edge; never enumerate a group."""
    budget.charge(len(base['AE_points']) + len(base['AB_points']) + 1)
    if base['AE_points'] and base['AE_points'] == base['AB_points']:
        try:
            valid_escape(proposed_witness, base, acquired_lookups, budget)
        except ValueError:
            # The shared Budget's failures are RuntimeError subclasses and
            # escape this branch. A failed candidate is not nonexistence.
            pass
        else:
            return dict(**base, status='EQUAL_JOINT_FIXED_SETS_WITH_ORIGINAL_ESCAPE',
                        escape=dict(proposed_witness))
    return dict(**base, status='VALID_PREFIX_WITHOUT_APPLICATION', escape=None)


def verified(supplied, base, acquired_lookups, budget):
    """ANY supplied valid attested edge; no producer or supplier call."""
    need(type(supplied) is dict and set(supplied) == set(base) | {'status', 'escape'},
         'whole supplied fixed-set record grammar')
    budget.charge(len(base['AE_points']) + len(base['AB_points']) + len(base['triple_points']) + 1)
    need(all(typed_equal(supplied[k], value) for k, value in base.items()),
         'all recomputed complete lists, vector digests and original relations')
    if supplied['status'] == 'EQUAL_JOINT_FIXED_SETS_WITH_ORIGINAL_ESCAPE':
        valid_escape(supplied['escape'], base, acquired_lookups, budget)
    elif supplied['status'] == 'VALID_PREFIX_WITHOUT_APPLICATION':
        need(supplied['escape'] is None, 'unpaid prefix asserts no absence or generation')
    else:
        raise ValueError('unknown fixed-set certificate status')
    budget.charge(0)
    return dict(**base, status=supplied['status'], escape=supplied['escape'])
