#!/usr/bin/env python3
"""Independent exhaustive parameter accounting and polynomial controls."""
import argparse,json,math,pathlib

def need(ok,s):
    if not ok:raise RuntimeError('PHASE267_REJECT '+s)
def primes(n):
    table=bytearray(b'\x01')*(n+1);table[:2]=b'\x00\x00'
    for p in range(2,math.isqrt(n)+1):
        if table[p]:table[p*p:n+1:p]=bytes(len(range(p*p,n+1,p)))
    return [p for p in range(2,n+1) if table[p]]
def factor(n,ps):
    answer=[];left=n
    for p in ps:
        if p*p>left:break
        e=0
        while left%p==0:left//=p;e+=1
        if e:answer.append([p,e])
    if left>1:answer.append([left,1])
    need(math.prod(p**e for p,e in answer)==n,'exact factorization reconstruction')
    return answer
def quartic(p,s,x):return ((s-4)*(x*x+1)**2-4*s*x*x)%p
def deriv(p,s,x):return (4*x*((s-4)*x*x-s-4))%p
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=pathlib.Path,required=True);a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'fresh report')
    # Generate primes and odd powers, rather than test consecutive bases as the old code does.
    cap=(21*19)**4; ps=primes(math.isqrt(cap)+1);small=[p for p in ps if p%2 and p**5<=cap]
    nonnested=[]
    for p in small:
        for b in range(5,23,2):
            g=1
            while p**(g*b)<=(21*(b-2))**4:
                for aa in range(3,b,2):
                    if math.gcd(aa,b)!=1:continue
                    Q=p**(g*b);fs=factor(Q-1,ps);W=1<<len(fs)
                    nonnested.append(dict(p=p,g=g,base=p**g,a=aa,b=b,Q=Q,factors=fs,W=W,passed=(Q-1)**2>16*aa*aa*W*W*Q))
                g+=2
    nonnested.sort(key=lambda r:(r['b'],r['base'],r['a']))
    fail=[(r['base'],r['a'],r['b']) for r in nonnested if not r['passed']]
    need(len(nonnested)==66 and fail==[(3,3,5),(5,3,5),(3,3,7),(3,5,7),(3,5,9),(3,7,9)],'complete nonnested scope')
    need(sorted({r['base'] for r in nonnested if r['g']>1})==[27],'only odd-exponent composite base')
    nested=[];exceptions=[]
    for p in ps:
        if p==2:continue
        if p**3>21**4:break
        e=3
        while p**e<=21**4:
            Q=p**e;fs=factor(Q-1,ps);W=1<<len(fs);v=Q-1-4*W
            okay=v>0 and v*v>16*W*W*Q
            divisors=[d for d in range(3,e+1,2) if e%d==0]
            nested.append(dict(p=p,e=e,Q=Q,factors=fs,W=W,allowed_first_exponents=divisors,passed=okay))
            if not okay:exceptions.extend((p,d,e) for d in divisors)
            e+=2
    need(len(nested)==23 and exceptions==[(3,3,3),(3,5,5),(5,3,3),(7,3,3),(11,3,3)],'complete nested scope including divisors')
    need(64**4<5**4*math.prod([2,3,5,7,11,13]),'strict W constant')
    need(3**23>(21*21)**4 and 9*21**4>23**4,'induction base and multiplier')
    # Point tests validate the algebraic identities; they do not replace algebraic-closure proofs.
    fields=[p for p in ps if 3<=p<=31];tested=0;roots=0
    for p in fields:
        for s in range(p):
            for x in range(p):
                f=quartic(p,s,x);B=((s-4)*x*x-s-4)%p
                need(((s-4)*f-(B*B-16*s))%p==0,'Bezout identity')
                if x:
                    u=x+pow(x,-1,p)
                    need((quartic(p,s,x)-x*x*(s*u*u-4*(s+u*u)))%p==0,'trace identity')
                if s not in [0,4%p] and not f:need(deriv(p,s,x)!=0,'simple root')
                if not f:
                    roots+=1
                    need(all(quartic(p,t,x)!=0 for t in range(p) if t!=s),'disjoint parameter roots')
                tested+=1
    controls={
        'char2_disjointness_fails':quartic(2,0,1)==quartic(2,1,1)==0,
        's0_multiple_root':quartic(5,0,2)==deriv(5,0,2)==0,
        's4_multiple_root':quartic(5,4,0)==deriv(5,4,0)==0,
        'degree_one_counterexample':((1*1-4*(1+1))%3)==2,
    }
    need(all(controls.values()),'explicit false-weakenings')
    report=dict(status='PASS',nonnested_count=len(nonnested),nested_count=len(nested),nonnested=nonnested,nested=nested,
                algebra_point_pairs=tested,roots_tested=roots,prime_fields=fields,controls=controls,
                limits=['Integer parameter enumeration is complete only after the proved analytic thresholds.','Point enumeration supplements but does not prove uniform polynomial or Weil statements.'])
    a.out.write_text(json.dumps(report,indent=2)+'\n');print('PHASE267_ARITHMETIC_PASS',len(nonnested),len(nested),tested)
if __name__=='__main__':main()
