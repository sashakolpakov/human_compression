#!/usr/bin/env python3
"""Independent rational arithmetic and literal-graph checks; imports no author code."""
import argparse, ast, copy, hashlib, itertools, json, math, subprocess
from fractions import Fraction as F
from pathlib import Path
import numpy as np


def need(x,s):
    if not x: raise ValueError(s)

def trim(a):
    a=list(map(F,a))
    while len(a)>1 and a[-1]==0:a.pop()
    return a

def add(a,b):
    return trim([(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))])

def scale(a,x):return trim([v*x for v in a])
def mul(a,b):
    c=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return trim(c)

def parse(s):
    def rec(t):
        if isinstance(t,ast.Constant) and isinstance(t.value,int):return [F(t.value)]
        if isinstance(t,ast.Name) and t.id=='n':return [F(0),F(1)]
        if isinstance(t,ast.UnaryOp) and isinstance(t.op,ast.USub):return scale(rec(t.operand),-1)
        if isinstance(t,ast.BinOp):
            a,b=rec(t.left),rec(t.right)
            if isinstance(t.op,ast.Add):return add(a,b)
            if isinstance(t.op,ast.Sub):return add(a,scale(b,-1))
            if isinstance(t.op,ast.Mult):return mul(a,b)
            if isinstance(t.op,ast.Div):
                need(len(b)==1 and b[0]!=0,'constant denominator');return scale(a,1/b[0])
            if isinstance(t.op,ast.Pow):
                need(len(b)==1 and b[0].denominator==1 and b[0]>=0,'nonnegative power')
                c=[F(1)]
                for _ in range(int(b[0])):c=mul(c,a)
                return c
        raise ValueError('unexpected polynomial grammar')
    return rec(ast.parse(s,mode='eval').body)

def value(a,n):
    r=F(0)
    for x in reversed(a):r=r*n+x
    return r

def interpolate(points):
    ans=[F(0)]
    for x,y in points:
        term=[F(y)]
        for z,_ in points:
            if z!=x:term=scale(mul(term,[-z,1]),F(1,x-z))
        ans=add(ans,term)
    return ans

def direct_counts(n,k,r):
    X=set(range(k));Y=[set(range(j))|set(range(k,2*k-j)) for j in range(k+1)]
    out=[0]*(k+1)
    for z in itertools.combinations(range(n),k):
        Z=set(z)
        if len(X&Z)==r:
            for j,T in enumerate(Y):out[j]+=len(T&Z)==r
    return out

def prime_factors(n):
    out=[];p=2
    while p*p<=n:
        if n%p==0:
            out.append(p)
            while n%p==0:n//=p
        p+=1
    if n>1:out.append(n)
    return out

def expected(k,r,p,n,mode):
    if (k,r)==(2,0):return p==2 and n%4==(3 if mode=='RLCD' else 1)
    if (k,r)==(3,0):return ((p==2 and n%4==1) or (p==3 and n%9 in ([5] if mode=='RLCD' else [2,8])) or (p>=5 and n%p==5%p))
    if (k,r)==(4,0):return p==2 and n%8==(7 if mode=='RLCD' else 3)
    if (k,r)==(3,1):return p==2 and n%4 in ([0] if mode=='RLCD' else [0,1])
    if (k,r)==(4,1):return (p==2 and n%(4 if mode=='RLCD' else 8)==1) or (p==3 and n%9==6)
    if r==k-1:return p==2 and n%2==1 and (mode=='RLCD' or math.comb(n,k)%2==0)
    raise ValueError('unlisted family')

def inspect_records(report):
    records=report['subset_family_certificates'];need(len(records)==14,'all fourteen lists')
    models={};out=[]
    for k,r in {(x['k'],x['r']) for x in records}:
        pts=[(n,direct_counts(n,k,r)) for n in range(2*k+1,3*k+2)]
        models[k,r]=[interpolate([(n,c[j]) for n,c in pts]) for j in range(k+1)]
    for row in records:
        k,r,mode=row['k'],row['r'],row['mode'];I=models[k,r]
        P=[add(a,[int(j==r)]) for j,a in enumerate(I)]
        fs=P if mode=='RLCD' else [add(I[-1],scale(a,-1)) for a in P]
        need(fs==[parse(a) for a in row['polynomials']],'literal subset reconstruction')
        bs=[parse(a) for a in row['bezout_coefficients']];g=parse(row['rational_gcd'])
        total=[F(0)]
        for a,b in zip(bs,fs):total=add(total,mul(a,b))
        need(total==g,'Bezout identity')
        qs=[parse(a) for a in row['common_divisor_quotients']]
        need(all(mul(g,q)==f for q,f in zip(qs,fs)),'divisor identities')
        need(g in [[F(1)],[-F(5),F(1)]],'exact monic integral gcd')
        bd=math.lcm(*(x.denominator for a in bs for x in a));fd=math.lcm(*(x.denominator for a in fs for x in a))
        need(bd==row['coefficient_denominator'] and fd==row['polynomial_denominator'],'denominator certificate')
        need(all(fd % x.denominator==0 for a in qs for x in a),'quotient denominators divide f denominator')
        primes=prime_factors(bd*fd);need(primes==row['exceptional_primes'],'exceptional primes')
        for case in row['finite_cases']:
            p=case['prime'];period=p
            while period<=k:period*=p
            need(period==case['period'],'period')
            residues=[];clcd=[]
            for residue in range(period):
                n=next(n for n in range(2*k+1,2*k+1+period) if n%period==residue)
                values=[value(f,n) for f in fs];need(all(x.denominator==1 for x in values),'integer-valued counts')
                if all(x.numerator%p==0 for x in values):
                    residues.append(residue)
                    if mode!='RLCD' and not (value(I[-1],n)%p==0 and (math.comb(n,k)-1)%p==0):clcd.append(residue)
            need(residues==case['residues'],'complete residue list')
            if mode!='RLCD':need(clcd==case['CLCD_residues'],'constant-line exclusion')
        for p in [2,3,5,7,11,17,23,29,31]:
            for n in range(2*k+1,151):
                result=all(value(f,n)%p==0 for f in fs)
                if mode!='RLCD':result=result and not(value(I[-1],n)%p==0 and (math.comb(n,k)-1)%p==0)
                need(result==expected(k,r,p,n,'RLCD' if mode=='RLCD' else 'CLCD'),'printed classification table')
        out.append({'k':k,'r':r,'mode':mode,'exceptional_primes':primes,'gcd':row['rational_gcd']})
    return out

def rank(a,p):
    a=np.array(a,dtype=np.int64)%p;m,n=a.shape;r=0
    for j in range(n):
        ids=np.flatnonzero(a[r:,j])
        if not len(ids):continue
        i=r+int(ids[0]);a[[r,i]]=a[[i,r]];a[r]=(a[r]*pow(int(a[r,j]),-1,p))%p
        if r+1<m:a[r+1:]=(a[r+1:]-a[r+1:,j,None]*a[r])%p
        r+=1
        if r==m:break
    return r

def matrix_cube(d,k):return np.array([[int((x^y).bit_count()==k) for y in range(2**d)] for x in range(2**d)],dtype=np.int64)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
    report=json.loads(a.report.read_text());classification=inspect_records(report)
    graphs=[]
    vertices=list(map(set,itertools.combinations(range(5),2)))
    A=np.array([[int(not(x&y)) for y in vertices] for x in vertices]);B=1-np.eye(10,dtype=np.int64)-A
    need(not np.any((A@B)%2),'Petersen complement orthogonality');need(rank(A,2)==6 and rank(B,2)==4,'Petersen ranks')
    need(np.any((A@(A+np.eye(10,dtype=np.int64)))%2),'Petersen not reflexive')
    graphs.append({'graph':'Petersen','binary_ranks':[6,4],'CLCD':True,'RLCD':False})
    for d in [2,4,6,8]:
        A=matrix_cube(d,1);I=np.eye(2**d,dtype=np.int64);B=1-I-A
        need(not np.any((A@A)%2) and not np.any((B@B-I)%2),'even cube square identities')
        ra=rank(A,2);rb=rank(B,2);need(ra==2**(d-1) and rb==2**d,'even cube ranks')
        graphs.append({'cube':d,'rank':ra,'complement_rank':rb,'self_dual':True,'complement_dual':False})
    for d,expected_rank in [(6,42),(9,342)]:
        A=matrix_cube(d,2);I=np.eye(2**d,dtype=np.int64)
        need(not np.any((A@(A+I))%3),'ternary distance2 reflexive identity')
        direct=rank(A,3)
        eigen=[sum((-1)**i*math.comb(t,i)*math.comb(d-t,2-i) for i in range(3) if i<=t and 2-i<=d-t) for t in range(d+1)]
        spectral=sum(math.comb(d,t) for t,x in enumerate(eigen) if x%3)
        need(direct==spectral==expected_rank,'Hamming ranks')
        graphs.append({'distance2_dimension':d,'ternary_rank':direct,'integral_eigenvalues':eigen})
    hamming=[]
    for d,q in [(1,2),(2,2),(3,2),(2,3),(3,3),(2,4),(3,4)]:
        vertices=list(itertools.product(range(q),repeat=d))
        for k in range(1,d+1):
            A=np.array([[int(sum(u!=v for u,v in zip(x,y))==k) for y in vertices] for x in vertices],dtype=np.int64)
            gram=A@A
            for j in range(d+1):
                poly={(0,0):1}
                for coordinate in range(d):
                    factor={(0,0):1,(1,1):q-1} if coordinate>=j else {(1,0):1,(0,1):1,(1,1):q-2}
                    nxt={}
                    for (u,v),a0 in poly.items():
                        for (s0,t0),b0 in factor.items():nxt[u+s0,v+t0]=nxt.get((u+s0,v+t0),0)+a0*b0
                    poly=nxt
                count=poly.get((k,k),0)
                for y,v in enumerate(vertices):
                    if sum(z!=0 for z in v)==j:need(int(gram[0,y])==count,'Hamming generating polynomial count')
            if q%2:need(not np.any((A@(A+np.eye(len(A),dtype=np.int64)))%2),'odd-q binary reflexive identity')
            hamming.append({'d':d,'q':q,'k':k,'coefficient_counts_match':True})
    A=np.ones((4,4),dtype=np.int64)-np.eye(4,dtype=np.int64)
    need(not np.any((A@(A+np.eye(4,dtype=np.int64)))%3) and rank(A,3)==3,'excluded endpoint K4')
    graphs.append({'graph':'J(4,3)=K4','prime':3,'RLCD':True,'rank':3,'scope':'outside adopted n>=2k+1 domain; source all-n wording limitation'})
    controls=[]
    for name,edit,message in [
        ('changed Bezout coefficient',lambda x:x['subset_family_certificates'][0]['bezout_coefficients'].__setitem__(0,'0'),'Bezout identity'),
        ('missing exceptional prime',lambda x:x['subset_family_certificates'][0].__setitem__('exceptional_primes',[]),'exceptional primes'),
        ('admitted constant-line residue',lambda x:x['subset_family_certificates'][1]['finite_cases'][0].__setitem__('CLCD_residues',[1,3]),'constant-line exclusion'),
        ('dropped scalar list',lambda x:x['subset_family_certificates'].pop(),'all fourteen lists')]:
        changed=copy.deepcopy(report);edit(changed)
        try:inspect_records(changed)
        except ValueError as exc:
            need(message in str(exc),'mutation rejected incorrectly');controls.append({'name':name,'rejected_at':str(exc)})
        else:raise ValueError('mutation survived')
    result={'status':'PASS','author_imports':False,'classification_certificates':classification,'literal_graphs':graphs,'Hamming_generating_polynomial_checks':hamming,'negative_controls':controls,'scope':'Independent bounded scalar/classification/rank review. No complete F017 or finite-distance claim.','input_report_sha256':hashlib.sha256(a.report.read_bytes()).hexdigest()}
    (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','classification_lists':len(classification),'graph_checks':len(graphs),'controls':len(controls)}))
if __name__=='__main__':main()
