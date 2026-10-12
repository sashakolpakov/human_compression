#!/usr/bin/env python3
"""Optional exact word/affine diagnostics; no universal-group census premise."""
def need(value, message):
    if not value:
        raise ValueError(message)


def normal_form(word):
    """(V4 * C2) semidirect C2, with t swapping a,c and fixing b."""
    blocks = []
    parity = 0
    for letter in word:
        if letter == 't':
            parity ^= 1
            continue
        value = {'a': 1, 'c': 2, 'b': 4}[letter]
        if parity and value != 4:
            value = ((value & 1) << 1) | ((value & 2) >> 1)
        if blocks and ((blocks[-1] == 4) == (value == 4)):
            value ^= blocks.pop()
        if value:
            blocks.append(value)
    return tuple(blocks), parity


def mul(a, b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(3))
                       for j in range(3)) for i in range(3))


def run():
    identities = [
        ('abcb', 't'+'tab'*2+'t'),
        ('abc'*2, 'abat'*2),
        ('t'+'abcb'+'t', 'b'+'bcba'+'b'),
        ('t'+'abc'+'t', 'cba'),
        ('cbt', 'tab'),
        ('cbab', 'cbt'*2),
        ('ta'*4, ''),
    ]
    for left, right in identities:
        need(normal_form(left) == normal_form(right), ('word identity', left, right))
    for label, left, bad in [
        ('omit square in axial conversion', 'abcb', 't'+'tab'+'t'),
        ('halve diagonal exponent incorrectly', 'abc'*2, 'abat'),
        ('fix a instead of exchanging a,c', 'tat', 'a'),
    ]:
        need(normal_form(left) != normal_form(bad), label)
    matrices = {
        'a': ((-1,0,0),(0,1,0),(0,0,1)),
        'c': ((1,0,0),(0,-1,0),(0,0,1)),
        'b': ((0,-1,1),(-1,0,1),(0,0,1)),
        't': ((0,1,0),(1,0,0),(0,0,1)),
    }
    identity = ((1,0,0),(0,1,0),(0,0,1))
    def matrix(word):
        result = identity
        for letter in word:
            result = mul(result, matrices[letter])
        return result
    for word, vector in [('abcb',(-2,0)), ('abc'*2,(-2,2)), ('taba',(1,-1))]:
        need(matrix(word) == ((1,0,vector[0]),(0,1,vector[1]),(0,0,1)), word)
    return {'word_identities': len(identities), 'wrong_word_controls': 3,
            'exact_local_translation_checks': 3,
            'role': 'optional diagnostics; full presentation and geometry proofs are written',
            'census_or_sample_based_uniform_claim': False}


if __name__ == '__main__':
    import json
    print(json.dumps(run(), indent=2))
