import itertools,json,sys
from pathlib import Path
if sys.flags.optimize: raise ValueError('optimization forbidden')
def need(v,s):
    if not v: raise ValueError(s)
def mul(a,b): return tuple(b[a[i]] for i in range(len(a)))
def power(a,k):
    if k<0:
        a=tuple(a.index(i) for i in range(len(a)));k=-k
    z=tuple(range(len(a)))
    for _ in range(k): z=mul(z,a)
    return z
def product(seq,n):
    z=tuple(range(n))
    for a in seq:z=mul(z,a)
    return z
def order(a):
    e=tuple(range(len(a)));z=e
    for k in range(1,1000):
        z=mul(z,a)
        if z==e:return k
    raise ValueError('order cap')
e=tuple(range(4)); inv=[x for x in itertools.permutations(range(4)) if mul(x,x)==e]
cases=0
for a,b,c in itertools.product(inv,repeat=3):
    if mul(a,c)!=mul(c,a):continue
    s=mul(a,b);t=mul(b,c)
    for j in range(1,7):
        h=product([a,b]+[c,b]*(j-1),4);z=product([a]+[b,c]*j,4)
        need(h==mul(s,power(t,1-j)),'hole identity')
        comm=product([s,power(t,-j),power(s,-1),power(t,j)],4)
        need(mul(z,z)==comm,'zigzag square')
        need(product([a,power(t,j),a],4)==product([s,power(t,-j),power(s,-1)],4),'conjugation')
        need(order(comm)==order(product([power(t,j),s,power(t,-j),power(s,-1)],4)),'conjugate period')
        cases+=1
# Signed coordinate permutations generate the flags of a cube and its dual.
def perm(cycles):
    a=list(range(6))
    for cyc in cycles:
        for i,j in zip(cyc,cyc[1:]+cyc[:1]):a[i]=j
    return tuple(a)
r=[perm([[0,1]]),perm([[0,2],[1,3]]),perm([[2,4],[3,5]])]
models=[]
for marks in [r,list(reversed(r))]:
    E=tuple(range(6)); flags={E:0}; todo=[E]
    for g in todo:
        for a in marks:
            h=mul(g,a)
            if h not in flags:flags[h]=(flags[g]+1)%2;todo.append(h)
            else:need(flags[h]!=(flags[g]),'flag bipartition')
    need(len(flags)==48,'48 flags')
    q=order(mul(marks[1],marks[2]));s=mul(marks[0],marks[1]);t=mul(marks[1],marks[2]);periods=[]
    for j in range(1,q//2+1):
        hw=[marks[0],marks[1]]+[marks[2],marks[1]]*(j-1);zw=[marks[0]]+[marks[1],marks[2]]*j
        h=product(hw,6);z=product(zw,6)
        comm=product([s,power(t,-j),power(s,-1),power(t,j)],6)
        need(order(h)==order(mul(s,power(t,1-j))),'even word period')
        need(order(z)==2*order(comm),'odd return factor')
        for flag in flags:
            reached=flag
            for _ in range(order(z)):reached=mul(reached,z)
            need(reached==flag,'actual full flag return')
        periods.append([j,order(h),order(z)])
    models.append({'q':q,'periods':periods})
out={'status':'PASS_DISTINCT_FLAG_WORD_CONTROLS','word_identity_cases':cases,'flag_models':models,'general_proof':False,'genuinely_chiral_model_claim':False}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
