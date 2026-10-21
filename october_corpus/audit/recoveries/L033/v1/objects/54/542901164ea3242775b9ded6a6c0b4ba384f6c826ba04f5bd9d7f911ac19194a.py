"""Exact finite arithmetic accompanying the written affine quotient argument."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Normal Python is required')
import itertools
import json
from pathlib import Path

I = (1,0,0,0,1,0,0,0,1)
S = [(0,-1,1,-1,0,1,0,0,1),
     (-1,1,0,0,1,0,0,0,1),
     (1,0,0,1,-1,0,0,0,1)]

def mul(a,b):
    return tuple(sum(a[3*i+k]*b[3*k+j] for k in range(3))
                 for i in range(3) for j in range(3))

def power(a,n):
    b=I
    for _ in range(n): b=mul(b,a)
    return b

def linear(a):
    return (a[0],a[1],0,a[3],a[4],0,0,0,1)

def closure(gens,cap=100):
    seen={I};queue=[I]
    for x in queue:
        for g in gens:
            y=mul(x,g)
            if y not in seen:
                seen.add(y);queue.append(y)
                if len(seen)>cap: raise ValueError('Finite closure bound exceeded')
    return seen

def translation(a,b): return (1,0,a,0,1,b,0,0,1)

def main():
    assert all(power(s,2)==I and s!=I for s in S)
    W=closure([S[1],S[2]])
    assert len(W)==6 and {linear(w) for w in W}==W
    parabolics=[]
    for i,j in itertools.combinations(range(3),2):
        assert power(mul(S[i],S[j]),3)==I and mul(S[i],S[j])!=I
        P=closure([S[i],S[j]])
        assert len(P)==6 and {linear(x) for x in P}==W
        parabolics.append(dict(generators=[i,j],elements=[list(x) for x in sorted(P)],
                               order=6,distinct_linear_parts=6))
    theta=mul(mul(S[1],S[2]),S[1])
    assert mul(S[0],theta)==translation(1,1)
    assert mul(mul(S[1],translation(1,1)),S[1])==translation(0,1)
    assert mul(translation(1,1),translation(0,-1))==translation(1,0)
    # The three chamber vertices are stored after multiplication by three.
    vertices={(0,0),(1,2),(2,1)}
    def act(m,v):
        return (m[0]*v[0]+m[1]*v[1]+3*m[2],
                m[3]*v[0]+m[4]*v[1]+3*m[5])
    assert [w for w in W if {act(w,v) for v in vertices}==vertices]==[I]
    for s in S:
        for v in vertices:
            image=act(s,v)
            assert all((image[k]-v[k])%3==0 for k in [0,1])
    # A literal witness to the failed intersection in the linear quotient:
    # all maximal marked parabolics are W, but their prescribed pairwise
    # intersections have order two.
    quotient_parabolics=[closure([linear(S[j]) for j in range(3) if j!=i])
                          for i in range(3)]
    assert all(H==W for H in quotient_parabolics)
    assert linear(S[0]) not in closure([linear(S[2])])
    # The repaired kernel-product condition fails explicitly for U_0 U_1.
    # theta lies in U_0, s0 in U_1, and their product is a nonzero translation.
    bad=mul(theta,S[0])
    assert bad==translation(-1,-1) and bad!=I
    report=dict(status='PASS_LITERAL_AFFINE_QUOTIENT',linear_group_order=6,
                maximal_parabolics=parabolics,
                translation_generators=[[1,1],[0,1],[1,0]],
                kernel_product_witness=list(bad),
                quotient_faces_per_type=[1,1,1],quotient_chambers=1,
                quotient_panels_size=1,quotient_thin=False,
                infinite_group_claims_require_written_proof=True,
                whole_original_credit=0,new_question_credit=0,new_Lean_declarations=0)
    out=Path(sys.argv[1])
    if out.exists(): raise RuntimeError('Refuse to overwrite a certificate')
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='maximal_parabolics'}))

if __name__=='__main__': main()
