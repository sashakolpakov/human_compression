"""Reviewer controls; no author imports or finite-field implementation reused."""
import json
from pathlib import Path
import sys

if sys.flags.optimize:
    raise SystemExit('optimization is unsupported')

def need(ok, message):
    if not ok:
        raise ValueError(message)

# Polynomials in c, with integer coefficient tuples in ascending degree.
def trim(x):
    x = list(x)
    while len(x) > 1 and x[-1] == 0:
        x.pop()
    return tuple(x)

def add(a, b):
    return trim([(a[i] if i < len(a) else 0) +
                 (b[i] if i < len(b) else 0)
                 for i in range(max(len(a), len(b)))])

def mul(a, b):
    x = [0] * (len(a) + len(b) - 1)
    for i, v in enumerate(a):
        for j, w in enumerate(b):
            x[i+j] += v*w
    return trim(x)

def mm(a, b):
    return tuple(tuple(add(mul(a[i][0], b[0][j]), mul(a[i][1], b[1][j]))
                       for j in range(2)) for i in range(2))

one, zero, minus, c = (1,), (0,), (-1,), (0,1)
A = ((minus,one),(zero,one))
a1 = ((zero,one),(minus,one))
V = ((one,zero),(c,one))
U = ((one,one),(zero,one))
target = (((0,-1),one),((-1,-1),one))
need(mm(mm(mm(A,V),A),a1) == target, 'conjugation identity')
need(mm(U,((one,zero),((-1,-1),one))) == target, 'first coset identity')
need(mm(a1,((one,zero),((0,-1),one))) == target, 'second coset identity')

# Literal actions on x,y,z,d. Compose as matrices acting on columns.
identity = tuple(range(4))
def compose(a,b):
    return tuple(a[b[i]] for i in range(4))

def inv(a):
    return tuple(a.index(i) for i in range(4))

X, Y = (1,2,0,3), (0,2,3,1)
group = {identity}
todo = [identity]
while todo:
    g = todo.pop()
    for h in (X,Y):
        z = compose(g,h)
        if z not in group:
            group.add(z)
            todo.append(z)
need(len(group)==12, 'A4 action order')
rosters = [
    (0, [identity,X,compose(X,Y),compose(X,inv(Y))]),
    (3, [identity,Y,compose(Y,X),compose(Y,inv(X))]),
    (1, [identity,X,inv(X),Y]),
]
images=[]
for fixed, reps in rosters:
    values=[inv(g)[fixed] for g in reps]
    need(sorted(values)==list(range(4)), 'source Lemma9 transversal')
    images.append(values)
u=compose(compose(X,inv(Y)),X)
v=compose(X,Y)
need(u!=identity and v!=identity and u!=v, 'distinct translations')
need(compose(u,u)==identity and compose(v,v)==identity, 'translation squares')
need(compose(u,v)==compose(v,u), 'commuting translations')
need(len({identity,u,v,compose(u,v)})==4,'translation image')

report = {
    'status':'PASS_INDEPENDENT_L041_AUXILIARY_CONTROLS',
    'author_imports':False,
    'symbolic_integer_polynomial_matrix_identities':3,
    'literal_A4_order':len(group),
    'source_L9_transversal_rows':images,
    'source_L9_rows_apply_to_both_tetrahedra':True,
    'translation_image_order':4,
    'translation_words':[u,v],
    'scope':'Supplementary exact controls, not a substitute for the uniform proof.'
}
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
