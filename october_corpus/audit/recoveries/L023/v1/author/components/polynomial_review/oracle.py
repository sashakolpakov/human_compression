"""Independent polynomial-field enumeration; no author/GAP imports."""
from collections import deque
import argparse, json
from pathlib import Path

def need(ok, message):
    if not ok: raise ValueError(message)

def field(p, coefficients):
    n=len(coefficients); Q=p**n
    def digits(x):
        a=[]
        for _ in range(n): a.append(x%p); x//=p
        return a
    def encode(a): return sum(v*p**i for i,v in enumerate(a))
    ds=[digits(x) for x in range(Q)]
    add=[[encode([(a+b)%p for a,b in zip(x,y)]) for y in ds] for x in ds]
    mul=[]
    for x in ds:
        row=[]
        for y in ds:
            z=[0]*(2*n-1)
            for i,a in enumerate(x):
                for j,b in enumerate(y): z[i+j]=(z[i+j]+a*b)%p
            for i in range(2*n-2,n-1,-1):
                for j,c in enumerate(coefficients): z[i-n+j]=(z[i-n+j]-z[i]*c)%p
            row.append(encode(z[:n]))
        mul.append(row)
    def power(x,k):
        a=1
        while k:
            if k%2:a=mul[a][x]
            x=mul[x][x];k//=2
        return a
    # In the polynomial quotient, this independently verifies every nonzero
    # element has an inverse, hence that the chosen quotient really is a field.
    need(all(power(x,Q-1)==1 for x in range(1,Q)), 'every nonzero field inverse')
    neg=[encode([(-a)%p for a in x]) for x in ds]
    inv=[None]+[power(x,Q-2) for x in range(1,Q)]
    return Q,add,mul,power,neg,inv

def examine(q,p,modulus):
    Q,A,M,powf,N,inv=field(p,modulus);need(Q==q**3,'cubic extension')
    one=(1,0,0,1);zero=(0,0,0,0);J=(0,1,N[1],0)
    def mm(x,y):
        a,b,c,d=x;e,f,g,h=y
        return (A[M[a][e]][M[b][g]],A[M[a][f]][M[b][h]],
                A[M[c][e]][M[d][g]],A[M[c][f]][M[d][h]])
    def determinant(x):return A[M[x[0]][x[3]]][N[M[x[1]][x[2]]]]
    def mi(x):
        t=inv[determinant(x)];return tuple(M[t][y] for y in (x[3],N[x[1]],N[x[2]],x[0]))
    def frob(x):return tuple(powf(t,q) for t in x)
    def mpow(x,k):
        ans=one
        while k:
            if k%2:ans=mm(ans,x)
            x=mm(x,x);k//=2
        return ans
    def factors(k):
        fs=[];d=2
        while d*d<=k:
            if k%d==0:
                fs.append(d)
                while k%d==0:k//=d
            d+=1
        if k>1:fs.append(k)
        return fs
    def exact_order(x,k):return mpow(x,k)==one and all(mpow(x,k//r)!=one for r in factors(k))
    # Enumerate literal a,b,c, solving only the determinant where b != 0.
    # The b=0 branch is included in full, independently of the parameter proof.
    solutions=[]
    for a in range(Q):
        numerator=N[A[1][M[a][a]]]
        for b in range(Q):
            cs=range(Q) if b==0 and numerator==0 else [] if b==0 else [M[numerator][inv[b]]]
            for c in cs:
                R=(a,b,c,N[a])
                need(determinant(R)==1,'literal determinant')
                if frob(frob(R))==mm(R,frob(R)):solutions.append(R)
    scalar=[R for R in solutions if R[1]==R[2]==0 and R[0]==R[3]]
    nonscalar=[R for R in solutions if R not in scalar]
    expected=q*(q*q-1) if p%2 else (q+1)*(q*q-1)
    need(len(nonscalar)==expected,'independent complete total')
    need(scalar==([] if p%2 else [one]),'complete scalar boundary')
    minus=[R for R in nonscalar if exact_order(mm(R,J),Q-1)]
    plus=[R for R in nonscalar if exact_order(mm(R,J),Q+1)]
    bc=[sum(M[R[1]][R[2]]==0 for R in col) for col in [minus,plus]]
    base=[x for x in range(Q) if powf(x,q)==x];need(len(base)==q,'fixed base field')
    if p%2:
        matrices=[(a,b,0,1) for a in base if a for b in base]
        matrices += [(a,b,1,d) for a in base for b in base for d in base if M[a][d]!=b]
        R=nonscalar[0];orbit=[mm(mm(g,R),mi(g)) for g in matrices]
        need(len(orbit)==len(set(orbit)) and set(orbit)==set(nonscalar),'complete free PGL orbit')
    else:
        points=[one]+[(x,1,1,0) for x in base]
        params=[x for x in range(1,Q) if A[A[x][powf(x,q)]][powf(x,q*q)]==0]
        orbit=[mm(mm(g,(1,t,0,1)),mi(g)) for g in points for t in params]
        need(len(orbit)==len(set(orbit)) and set(orbit)==set(nonscalar),'complete trace/fixed-point parameters')
    sizes=[]
    if q in [2,3]:
        def projective(x):
            return min(x,tuple(N[t] for t in x)) if p%2 else x
        for col in [minus,plus]:
            if not col:sizes.append(None);continue
            R=col[0];gens=[R,J,frob(R)];todo=deque([one]);seen={projective(one)}
            while todo:
                x=todo.popleft()
                for g in gens:
                    y=projective(mm(x,g))
                    if y not in seen:seen.add(y);todo.append(y)
            target=Q*(Q*Q-1)//(2 if p%2 else 1)
            need(len(seen)==target,'literal projective generation')
            sizes.append(len(seen))
    return {'q':q,'p':p,'modulus_low_coefficients':modulus,'all_literal_solutions':len(solutions),
            'nonscalar_total':len(nonscalar),'scalar_count':len(scalar),
            'primitive_counts':[len(minus),len(plus)],'bc_zero_counts':bc,
            'parameterization_equals_full_literal_set':True,'sample_projective_group_orders':sizes}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);a=ap.parse_args()
    cases=[(2,2,[1,1,0]),(3,3,[1,2,0]),(4,2,[1,1,0,0,0,0]),(5,5,[1,1,0])]
    result={'role':'distinct reviewer independent coordinate arithmetic',
            'author_or_GAP_imports':False,'cases':[examine(*c) for c in cases]}
    a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
