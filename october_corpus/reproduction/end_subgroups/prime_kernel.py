"""Retained supplied-only prime checks; classification is an attributed input."""

def checked_prime(fact, prime, marks, side, identity, arithmetic, work):
    arithmetic.need(prime in (19, 37) and type(prime) is int,
                    'one of the two explicitly classified primes')
    arithmetic.need(type(fact) is dict and set(fact) == {
        'side', 'word', 'cofactor', 'prime_value'}
        and type(fact['side']) is int and fact['side'] == side
        and type(fact['cofactor']) is int
        and fact['cofactor'] in (1, 7 if prime == 19 else 3),
        'whole supplied same-end word and explicit permitted power')
    value = arithmetic.word_value(fact['word'], marks, side, identity, work)
    value = arithmetic.power(value, fact['cofactor'], identity, work)
    arithmetic.need(value == arithmetic.field_matrix(fact['prime_value'])
                    and value != identity
                    and arithmetic.power(value, prime, identity, work) == identity,
                    'fresh full actual prime-order matrix, not a supplier verdict')
    return value


def check_record(record, marks, side, identity, arithmetic, work):
    found = []
    for prime, key in ((19, 'prime19'), (37, 'prime37')):
        if record[key] is not None:
            checked_prime(record[key], prime, marks, side, identity, arithmetic, work)
            found.append(prime)
    kind = ('TWO_PRIMES_FULL_END' if len(found) == 2 else
            'ONE_PRIME_PARTIAL' if found else 'FINITE_TRIAL_MISS')
    arithmetic.need(record['kind'] == kind,
                    'the exact conclusion follows only from supplied positive words')
    full = found == [19, 37]
    return dict(kind=kind, exact_same_end_primes_verified=found,
                end_conclusion='FULL_NATURAL_G2_11' if full else None,
                IP_failure_verified=full,
                borrowed_generation_theorem='f1b6c8a6:Theorem two and Corollary words',
                fixed_line_or_irreducibility_or_orbit_search_needed=False,
                finite_miss_is_not_absence=True,
                attempted_predicates_are_method_diagnostics_only=True)
