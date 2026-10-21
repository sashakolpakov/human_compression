"""Independent arithmetic reconstruction; no torus-search outputs are trusted.
The subgroup classification and polytope reconstruction steps are written proofs,
not assertions established by this arithmetic program.
"""
from pathlib import Path
import json,math,hashlib,argparse
args=argparse.ArgumentParser();args.add_argument('--out',type=Path,required=True);arg=args.parse_args();arg.out.mkdir(parents=True,exist_ok=False);W=arg.out
MOD=(1<<15)|(1<<1)|1

def mul(a,b):
    c=0
    while b:
        if b&1:c^=a
        a<<=1;b>>=1
        if a&(1<<15):a^=MOD
    return c

def power(a,n):
    if n<0:
        assert a
        n%=32767
    r=1
    while n:
        if n&1:r=mul(r,a)
        a=mul(a,a);n>>=1
    return r

def polyrem(a,b):
    while a and a.bit_length()>=b.bit_length():a^=b<<(a.bit_length()-b.bit_length())
    return a

def polygcd(a,b):
    while b:a,b=b,polyrem(a,b)
    return a

def mm(a,b):
    out=[[0]*4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):out[i][j]^=mul(a[i][k],b[k][j])
    return out
I=[[int(i==j)for j in range(4)]for i in range(4)]
J=[[int(i+j==3)for j in range(4)]for i in range(4)]
def mp(a,n):
    r=I
    while n:
        if n&1:r=mm(r,a)
        a=mm(a,a);n>>=1
    return r

def inv(a):
    b=[row[:]+I[i][:]for i,row in enumerate(a)]
    for j in range(4):
        k=next(k for k in range(j,4)if b[k][j]);b[j],b[k]=b[k],b[j]
        z=power(b[j][j],-1);b[j]=[mul(z,e)for e in b[j]]
        for i in range(4):
            if i!=j:
                z=b[i][j];b[i]=[e^mul(z,f)for e,f in zip(b[i],b[j])]
    assert [r[:4]for r in b]==I
    return [r[4:]for r in b]

def U(x,y):
    X=power(x,256)
    return [[1,0,0,0],[x,1,0,0],[mul(x,X)^y,X,1,0],
            [mul(mul(x,x),X)^mul(x,y)^power(y,256),y,x,1]]

def H(t):
    d=[power(t,e)for e in [257,1,-1,-257]]
    return [[d[i]if i==j else 0 for j in range(4)]for i in range(4)]

def invol(x,y):
    r=U(x,y)
    return mm(mm(mm(mm(inv(r),J),U(0,1)),J),r)

def transpose(a):return [list(row)for row in zip(*a)]
def phi(a):
    pp=[(0,1),(0,2),(1,3),(2,3)]
    return [[power(mul(a[i][k],a[j][l])^mul(a[i][l],a[j][k]),128)
             for k,l in pp]for i,j in pp]
def in32(a):return all(power(x,32)==x for row in a for x in row)
def trace(a):return a[0][0]^a[1][1]^a[2][2]^a[3][3]
def predicates(a):
    return {'upper_triangular':all(a[i][j]==0 for i in range(4)for j in range(i)),
            'lower_triangular':all(a[i][j]==0 for i in range(4)for j in range(i+1,4)),
            'antidiagonal':all(a[i][j]==0 for i in range(4)for j in range(4)if i+j!=3)}

# Rabin irreducibility and a primitive-root check for X^15+X+1.
assert power(2,1<<15)==2
assert polygcd(power(2,1<<5)^2,MOD)==1
assert polygcd(power(2,1<<3)^2,MOD)==1
assert all(power(2,32767//p)!=1 for p in [7,31,151])
eta=power(2,1057);lam=2267
assert eta==624 and power(eta,31)==1 and eta!=1
assert power(eta,5)^power(eta,3)^power(eta,2)^eta^1==0
assert power(lam,32)!=lam
u=invol(power(eta,2),power(eta,3))
vK=invol(power(eta,5),power(eta,30))
b=H(eta);h=H(lam);v=mm(mm(h,vK),inv(h))
a=mm(u,inv(b));c=mm(inv(b),v);w=mm(a,v)
for g in [u,vK,b,h,v,a,c,w]:
    assert mm(mm(transpose(g),J),g)==J
    assert phi(g)==g
assert in32(u)and in32(vK)and in32(b)and not in32(v)
assert a!=I and mp(a,31)==I and b!=I and mp(b,31)==I
assert mp(c,25)==I and mp(c,5)!=I
for t in [u,v,w]:assert t!=I and mm(t,t)==I
assert mm(a,b)==u and mm(b,c)==v and mm(mm(a,b),c)==w
assert all(not flag for g in [u,vK]for flag in predicates(g).values())
assert all(math.gcd(e,32767)==1 for e in [256,258,514])
assert all(n%31 for n in [100,164,20])
assert math.gcd(31,25)==1 and math.gcd(62,50)==2
lc=[lam,power(lam,32),power(lam,1024)]
coeff=[1]
for t in lc:
    nxt=[0]*(len(coeff)+1)
    for j,z in enumerate(coeff):nxt[j]^=mul(z,t);nxt[j+1]^=z
    coeff=nxt
assert all(power(z,32)==z for z in coeff)
assert coeff==[eta,power(eta,11),power(eta,12),1]
minpoly_at_lam=0
for z in reversed(coeff):minpoly_at_lam=mul(minpoly_at_lam,lam)^z
assert minpoly_at_lam==0
lookup={power(eta,k):k for k in range(31)}
def frozen(g):return tuple(e for row in g for e in row)
def cyclic(g,n):
    out=[];t=I
    for _ in range(n):out.append(t);t=mm(t,g)
    assert t==I and len({frozen(x)for x in out})==n
    return out
AA,BB,CC=cyclic(a,31),cyclic(b,31),cyclic(c,25)
SA,SB,SC=[{frozen(x)for x in seq}for seq in [AA,BB,CC]]
assert SA&SB=={frozen(I)} and SB&SC=={frozen(I)}
D1=AA+[mm(t,v)for t in AA];D2=CC+[mm(t,u)for t in CC]
assert len({frozen(x)for x in D1})==62 and len({frozen(x)for x in D2})==50
assert {frozen(x)for x in D1}&{frozen(x)for x in D2}=={frozen(I),frozen(w)}
def inE(g):return in32(mm(mm(inv(h),g),h))
assert {frozen(x)for x in D1 if in32(x)}==SA
assert {frozen(x)for x in D1 if inE(x)}=={frozen(I),frozen(v)}
assert {frozen(x)for x in D2 if in32(x)}=={frozen(I),frozen(u)}
assert {frozen(x)for x in D2 if inE(x)}==SC
bad=[row[:]for row in v];bad[0][0]^=1
assert mm(bad,bad)!=I and phi(bad)!=bad
# Direct comparison with the source's Wilson basis and normalization abc=J.
perm=[1,0,3,2]
Pmat=[[int(perm[i]==j)for j in range(4)]for i in range(4)]
def phi_wilson(g):
    pp=[(1,3),(0,1),(2,3),(0,2)]
    return [[power(mul(g[i][k],g[j][l])^mul(g[i][l],g[j][k]),128)
             for k,l in pp]for i,j in pp]
assert mm(mm(Pmat,J),Pmat)==J
for gg in [u,vK,b,h,v,a,c,w]:
    assert phi_wilson(mm(mm(Pmat,gg),Pmat))==mm(mm(Pmat,phi(gg)),Pmat)
assert w[0][3]
delta=power(w[0][3],pow(514,-1,32767));hd=H(delta)
wn=mm(mm(inv(hd),w),hd)
assert wn[0][3]==1
xx=wn[0][2]^1;yy=wn[0][1]^power(xx,256)
assert invol(xx,yy)==wn
normalizer=mm(mm(hd,inv(U(xx,yy))),U(1,1))
assert mm(mm(inv(normalizer),w),normalizer)==J
an=mm(mm(inv(normalizer),a),normalizer)
source_x=mm(mm(Pmat,inv(an)),Pmat)
assert transpose(source_x)==source_x and mm(mm(source_x,J),source_x)==J
assert phi_wilson(source_x)==source_x
sx=source_x
residuals={
'13':mul(sx[0][3],sx[1][3])^mul(sx[0][1],sx[3][3]),
'14':mul(sx[0][1],sx[0][3])^mul(sx[0][0],sx[1][3]),
'15':mul(sx[0][2],sx[3][3])^mul(sx[0][3],sx[2][3]),
'16':mul(sx[0][0],sx[2][3])^mul(sx[0][2],sx[0][3]),
'17':mul(sx[1][1],sx[2][3])^mul(sx[1][3],sx[1][2]),
'18':mul(sx[1][1],sx[0][2])^mul(sx[0][1],sx[1][2]),
'19':mul(sx[1][2],sx[2][3])^mul(sx[1][3],sx[2][2]),
'20':mul(sx[0][1],sx[2][2])^mul(sx[0][2],sx[1][2])}
assert any(residuals.values())
def bullet(vv,ww):
    return [power(mul(vv[i],ww[j])^mul(vv[j],ww[i]),128)
            for i,j in [(1,3),(0,1),(2,3),(0,2)]]
e1,e2,e3,e4=I
xe1=[row[0]for row in sx];xe4=[row[3]for row in sx]
bad_pair_bullet=bullet(xe1,xe4)
assert bullet(e1,e4)==[0]*4 and bad_pair_bullet!=[0]*4
for i,j in [(0,1),(0,2),(1,3),(2,3)]:
    left=bullet([row[i]for row in sx],[row[j]for row in sx]);base=bullet(I[i],I[j]);right=[0]*4
    for ri in range(4):
        for rj in range(4):right[ri]^=mul(sx[ri][rj],base[rj])
    assert left==right
source_diagnostic={'basis_permutation_one_based':[2,1,4,3],
                   'normalizer':normalizer,'normalized_source_x':source_x,
                   'source_x_symmetric':True,'source_x_J_x_equals_J':True,
                   'correct_Wilson_Suzuki_equations':True,
                   'inadmissible_source_equation_residuals':residuals,
                   'Wilson_xe1_bullet_xe4':bad_pair_bullet,
                   'source_defect':'Source p3 applies bullet invariance to pairs e1,e4 and e2,e3 whose symplectic pairing is 1, outside the stated orthogonality domain.'}
record={'status':'EXACT_ARITHMETIC_PASS_WRITTEN_GROUP_ARGUMENT_PENDING_REVIEW',
        'field_polynomial':'X^15+X+1','integer_encoding':'polynomial-basis bits, least significant bit constant',
        'eta':eta,'eta_definition':'X^1057','eta_minimal_polynomial':'T^5+T^3+T^2+T+1',
        'lambda':lam,'lambda_minimal_polynomial_coefficients_low_to_high':coeff,
        'lambda_coefficients_eta_exponents_low_to_high':[lookup.get(z)if z else None for z in coeff],
        'first_parameters':{'x_eta_exponent':2,'y_eta_exponent':3,'r':1},
        'second_parameters':{'x_eta_exponent':5,'y_eta_exponent':30,'r':1},
        'orders':{'a':31,'b':31,'c':25,'ab':2,'bc':2,'abc':2},
        'matrices':{'a':a,'b':b,'c':c,'u':u,'v':v,'vK':vK,'h':h,'abc':w},
        'source_principal_statement':'Spiga, arXiv:2010.04080v1, 8 Oct 2020, Theorem 1.1: every chiral polytope with Sz(q)<=G<=Aut(Sz(q)) has rank3.',
        'group_order_if_generation_proved':32768**2*(32768**2+1)*(32768-1),
        'required_written_steps':['Both faces Sz32 by maximal subgroup classification.','F intersection H(lambda)F H(lambda)^-1 is its split torus31 by Bruhat coordinates.','Sz32 is maximal in Sz32768 because 15/5=3.','Full IC+ using the four rank3 parabolics.','Chirality by odd outer automorphism group and odd centralizer of c.'],
        'finite_parabolic_checks':{'cyclic_orders':[31,31,25],'dihedral_orders':[62,50],'dihedral_intersection_order':2,'dihedral_face_intersection_orders':[31,2,2,25]},'negative_control':'corrupted v rejected by involution and Suzuki equations','source_diagnostic':source_diagnostic,'whole_original_credit':0}
(W/'report.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in record.items()if k!='matrices'},indent=2))
