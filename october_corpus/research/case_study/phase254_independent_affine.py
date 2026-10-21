#!/usr/bin/env python3
"""Independent exact quotient enumeration and Schreier-orientation control."""
import argparse,itertools,json,pathlib,time

def need(ok,s):
 if not ok:raise RuntimeError('PHASE254_REJECT '+s)
def mm(A,B):return tuple(tuple(sum(a*b for a,b in zip(row,col)) for col in zip(*B)) for row in A)
def mv(A,x):return tuple(sum(a*b for a,b in zip(row,x)) for row in A)
def add(x,y):return tuple(a+b for a,b in zip(x,y))
def neg(x):return tuple(-a for a in x)
def ident(n):return tuple(tuple(int(i==j) for j in range(n)) for i in range(n))
def affmul(a,b):return mm(a[0],b[0]),add(a[1],mv(a[0],b[1]))
def affinv(a):
 T=tuple(zip(*a[0]));return T,neg(mv(T,a[1]))
def det(A):
 if len(A)==1:return A[0][0]
 return sum((-1)**j*A[0][j]*det(tuple(tuple(row[k] for k in range(len(A)) if k!=j) for row in A[1:])) for j in range(len(A)))
def adj(A):
 n=len(A)
 return tuple(tuple((-1)**(i+j)*det(tuple(tuple(A[r][c] for c in range(n) if c!=i) for r in range(n) if r!=j)) for j in range(n)) for i in range(n))

def orientation_control():
 I=ident(2);minus=((-1,0),(0,-1));swap=((0,1),(1,0));zero=(0,0)
 s=(minus,(1,0));t=(minus,zero);u=(swap,zero);gens=[s,t,u]
 Q=[I,minus,swap,mm(minus,swap)];lifts={q:(q,zero) for q in Q}
 need(all(affmul(g,g)==(I,zero) for g in gens),'counterexample involutions')
 raw=[];normalized=[]
 for q in Q:
  for g in gens:
   y=affmul(g,lifts[q]);target=lifts[y[0]]
   raw.append(affmul(y,affinv(target))[1])
   normalized.append(affmul(affinv(target),y)[1])
 trans=affmul(s,t);other=affmul(affmul(u,trans),u)
 need(set(raw)=={zero,(1,0)} and trans==(I,(1,0)) and other==(I,(0,1)),'raw-transition counterexample')
 need(any(x[0] and not x[1] for x in normalized) and any(x[1] and not x[0] for x in normalized),'correct normalization finds both directions')
 return dict(raw_vectors=sorted(set(raw)),normalized_vectors=sorted(set(normalized)),actual_translations=[trans[1],other[1]],conclusion='Raw left-prefix differences require Q-saturation; normalized Schreier transitions generate the full lattice.')

def enumerate_family(kind,m,vectors,expect_ip=True):
 I=ident(3);zero=(0,0,0)
 a=(((0,1,0),(1,0,0),(0,0,1)),zero)
 b=(((-1,0,0),(0,0,1),(0,1,0)),(1,0,0))
 c=(((1,0,0),(0,1,0),(0,0,-1)),zero) if kind=='64' else (((0,-1,0),(-1,0,0),(0,0,1)),zero)
 gens=[a,b,c];Q=[I];qi={I:0}
 for q in Q:
  for M,t in gens:
   h=mm(M,q)
   if h not in qi:qi[h]=len(Q);Q.append(h)
 need(len(Q)==48,'point group')
 B=tuple(tuple(m*vectors[j][i] for j in range(3)) for i in range(3));D=det(B);ad=adj(B)
 need(D!=0 and mm(ad,B)==tuple(tuple(D*int(i==j) for j in range(3)) for i in range(3)),'exact adjugate identity')
 Dabs=abs(D)
 actions=[]
 for M in Q:
  numerator=mm(mm(ad,M),B)
  need(all(x%D==0 for row in numerator for x in row),'whole point group preserves period lattice')
  actions.append(tuple(tuple(x//D for x in row) for row in numerator))
 genq=[qi[x[0]] for x in gens];gent=[tuple(x%Dabs for x in mv(ad,g[1])) for g in gens]
 qt=[[qi[mm(g[0],q)] for q in Q] for g in gens]
 one=(0,zero)
 def step(i,g):
  q,v=g;return qt[i][q],tuple(x%Dabs for x in add(gent[i],mv(actions[genq[i]],v)))
 def subgroup(ids):
  out=[one];seen={one}
  for g in out:
   for i in ids:
    h=step(i,g)
    if h not in seen:need(len(out)<30000,'bounded enumeration');seen.add(h);out.append(h)
  return seen
 sets=[tuple(i for i in range(3) if (mask>>i)&1) for mask in range(8)]
 subs={I:subgroup(I) for I in sets}
 failures=[]
 for J in sets:
  for K in sets:
   both=tuple(sorted(set(J)&set(K)))
   if subs[J]&subs[K]!=subs[both]:failures.append([J,K])
 need((not failures)==expect_ip,'actual full intersection verdict')
 for i in range(3):need(step(i,step(i,one))==one and step(i,one)!=one,'marked involutions')
 need(step(0,step(2,one))==step(2,step(0,one)),'commuting endpoints')
 orders=[]
 for i,j in [(0,1),(1,2)]:
  g=one
  for k in range(1,25):
   g=step(i,step(j,g))
   if g==one:orders.append(k);break
 need(orders==([6,4] if kind=='64' else [6,6]),'actual product orders')
 return dict(kind=kind,m=m,group_order=len(subs[(0,1,2)]),lattice_determinant=Dabs,adjacent_orders=orders,intersection_tests=64,intersection_failures=failures)

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=pathlib.Path,required=True);a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh output')
 start=time.monotonic();report=dict(orientation_control=orientation_control(),models=[])
 bases64=[[(2,0,0),(0,-2,0),(0,0,-2)],[(2,0,2),(2,-2,0),(-2,-2,0)],[(2,-2,2),(2,-2,-2),(-2,-2,-2)]]
 bases66=[[(4,0,0),(0,-4,0),(0,0,-4)],[(4,-4,0),(4,0,-4),(-4,-4,0)],[(4,-4,4),(4,-4,-4),(-4,-4,4)]]
 for kind,bases,constants in [('64',bases64,[96,192,384]),('66',bases66,[192,384,768])]:
  for i,(base,k) in enumerate(zip(bases,constants)):
   for m in [1,2,3]:
    result=enumerate_family(kind,m,base)
    need(result['group_order']==k*m**3,'independent group order')
    result['source_family']=i+1;report['models'].append(result)
 bad=enumerate_family('66',1,[(2,2,0),(2,0,2),(0,2,2)],False)
 need(bad['group_order']==48,'invalid period kills translations')
 report.update(status='PASS',bad_period=bad,seconds=round(time.monotonic()-start,3),scope='Independent finite quotient enumerations and orientation counterexample; uniform presentation theorem remains written plus exact author presentation certificates.')
 a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status='PASS',models=len(report['models']),seconds=report['seconds'],bad_period_IP='rejected',old_Schreier_formula='refuted')))
if __name__=='__main__':main()
