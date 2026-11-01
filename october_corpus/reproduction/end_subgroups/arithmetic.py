"""Literal same-end word/field/power primitives with a charged byte adapter."""
ENDS=((0,1,2),(1,2,3))
I7=tuple(tuple(int(i==j)for j in range(7))for i in range(7))

def need(ok, why):
    if not ok:
        raise ValueError(why)

def field_matrix(value):
    need(type(value) is list and len(value) == 7
         and all(type(row) is list and len(row) == 7 for row in value)
         and all(type(x) is int and 0 <= x < 11 for row in value for x in row),
         'whole supplied canonical seven-by-seven matrix')
    return tuple(tuple(row) for row in value)

def word_value(word, marks, side, identity, work):
    need(type(side) is int and side in (0, 1)
         and type(word) is list and 1 <= len(word) <= 32
         and all(type(j) is int and j in ENDS[side] for j in word),
         'bounded word in the stated original three-mark end')
    value = identity
    for j in word:
        value = work.multiply(value, marks[j])
    return value

def power(value, exponent, identity, work):
    need(type(exponent) is int and exponent >= 0, 'fixed nonnegative exponent')
    result = identity
    while exponent:
        if exponent & 1:
            result = work.multiply(result, value)
        exponent //= 2
        if exponent:
            value = work.multiply(value, value)
    return result

def internal(g):
    return tuple(tuple(tuple(mat[7*i+j]for j in range(7))for i in range(7))for mat in g)

class Adapter:
    def __init__(self,b):self.b=b
    def multiply(self,A,B):
        raw=self.b.multiply(bytes(x for r in A for x in r),bytes(x for r in B for x in r))
        return tuple(tuple(raw[7*i+j]for j in range(7))for i in range(7))
