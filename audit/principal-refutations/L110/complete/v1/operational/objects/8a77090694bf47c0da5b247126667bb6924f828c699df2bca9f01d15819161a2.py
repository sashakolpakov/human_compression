"""Two exact finite controls, including a prime shared with the base torus.

These check the displayed arithmetic, not the general theorem or any group.
"""
import itertools, json, math
from pathlib import Path

def run():
    rows=[]
    for e, aa, ll in [(3,[3,5],[73,31]),(3,[3,7],[73,7])]:
        t=2**e; A=math.prod(aa); M=(t-1)*math.prod(ll)
        assert all(all(l%d for d in range(2,math.isqrt(l)+1)) for l in ll)
        assert all(((t**a-1)//(t-1))%l==0 for a,l in zip(aa,ll))
        for mask in itertools.product([False,True],repeat=len(aa)):
            D=math.prod(a for a,removed in zip(aa,mask) if not removed)
            L=(t-1)*math.prod(l for l,removed in zip(ll,mask) if not removed)
            actual=math.gcd(M,t**D-1)
            assert actual==L
            degrees=[f for f in range(1,e*D+1) if e*D%f==0 and (2**f-1)%L==0]
            assert degrees==[e*D]
            rows.append(dict(e=e,relative_primes=aa,cyclic_primes=ll,
                removed=mask,gcd=actual,scalar_order=L,containing_field_degrees=degrees))
    return dict(status='PASS_EIGHT_EXACT_ARITHMETIC_CONTROLS',rows=rows,
                group_enumerations=0,general_proof_by_computation=False)

if __name__=='__main__':
    out=Path(__file__).with_name('arithmetic_controls.json')
    if out.exists():raise ValueError('preserve existing control result')
    out.write_text(json.dumps(run(),indent=2)+'\n')
    print('PASS: eight finite arithmetic controls; no group computation.')
