"""Reproduce the complete exact short-root F4 model used in the first run."""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json
P=Path(__file__).resolve().parent
roots=[]
for i in range(4):
    for sg in [-1,1]:roots.append(tuple(2*sg if j==i else 0 for j in range(4)))
roots+=list(product([-1,1],repeat=4));roots=sorted(roots)
simple=[(0,1,-1,0),(0,0,1,-1),(0,0,0,1),(1,-1,-1,-1)]
perms=[]
for a in simple:
    aa=sum(x*x for x in a);im=[]
    for v in roots:
        av=sum(x*y for x,y in zip(a,v))
        w=tuple(Q(x)-Q(2*av*y,aa)for x,y in zip(v,a));im.append(roots.index(w)+1)
    perms.append(im)
(P/'F4_model.json').write_text(json.dumps({'short_roots_scaled_by_two':roots,'simple_root_directions':simple,'reflection_permutations':perms},indent=2)+'\n')
(P/'F4_model.g').write_text('modelName:="F4";;\nexpectedOrder:=1152;;\nmodelPerms:='+str(perms)+';;\nG:=Group(List(modelPerms,PermList));;\n')
