#!/usr/bin/env python3
"""Finite full-ambient diagnostics; the all-rank IP theorem remains a cited input."""
import argparse,hashlib,json,time
from pathlib import Path

def require(ok,msg):
 if not ok:raise ValueError(msg)

class Field:
 def __init__(self,e,poly):
  self.q=1<<e;self.poly=poly
  def mult(a,b):
   out=0
   while b:
    if b&1:out^=a
    a<<=1
    if a&self.q:a^=poly
    b>>=1
   return out
  self.tab=[[mult(a,b) for b in range(self.q)] for a in range(self.q)]
  for a in range(1,self.q):require(len(set(self.tab[a]))==self.q,'not a field')
 def mul(self,a,b):return self.tab[a][b]

def addv(a,b):return tuple(x^y for x,y in zip(a,b))
def eye(d):return tuple(int(i==j) for i in range(d) for j in range(d))
def mm(a,b,d,F):
 out=[0]*(d*d);tab=F.tab
 for i in range(d):
  for k in range(d):
   x=a[i*d+k]
   if x:
    row=tab[x]
    for j in range(d):out[i*d+j]^=row[b[k*d+j]]
 return tuple(out)
def mv(a,v,d,F):
 out=[]
 for i in range(d):
  x=0
  for j in range(d):x^=F.mul(a[i*d+j],v[j])
  out.append(x)
 return tuple(out)
def powr(a,n,d,F):
 out=eye(d)
 while n:
  if n&1:out=mm(out,a,d,F)
  a=mm(a,a,d,F);n>>=1
 return out

def model(d,F,alpha):
 def basis(i):return tuple(int(j==i) for j in range(d))
 def Q(v):
  x=0
  for vj in v:x^=F.mul(vj,vj)
  for i in range(d-1):x^=F.mul(alpha,F.mul(v[i],v[i+1]))
  return x
 def B(u,v):return Q(addv(u,v))^Q(u)^Q(v)
 def lin(action):
  columns=[action(basis(j)) for j in range(d)]
  return tuple(columns[j][i] for i in range(d) for j in range(d))
 def sym(u):
  require(Q(u)==1,'symmetry norm')
  return lin(lambda x:addv(x,tuple(F.mul(B(x,u),ui) for ui in u)))
 def T(z,u):
  require(Q(z)==0 and B(z,u)==0,'T hypotheses')
  def image(x):
   b=B(x,z);c=B(x,u)^F.mul(Q(u),b)
   return tuple(xi^F.mul(b,ui)^F.mul(c,zi) for xi,ui,zi in zip(x,u,z))
  return lin(image)
 return basis,Q,B,sym,T

def choose(F,n):
 for a in range(1,F.q):
  H=(1,a,a,1^F.mul(a,a))
  if powr(H,n,2,F)==eye(2) and all(powr(H,k,2,F)!=eye(2) for k in range(1,n)):return a
 raise ValueError('missing exact-order coefficient')

def relations(d,F,n,a):
 basis,Q,B,sym,T=model(d,F,a);one=eye(d);marks=[sym(basis(i)) for i in range(d)]
 def checkQ(M):
  for i in range(d):
   require(Q(mv(M,basis(i),d,F))==1,'Q diagonal')
   for j in range(i):require(B(mv(M,basis(i),d,F),mv(M,basis(j),d,F))==B(basis(i),basis(j)),'Q polar')
 for r in marks:require(mm(r,r,d,F)==one and r!=one,'involution');checkQ(r)
 for i in range(d):
  for j in range(i+1,d):
   p=mm(marks[i],marks[j],d,F);o=n if j==i+1 else 2
   require(powr(p,o,d,F)==one and all(powr(p,k,d,F)!=one for k in range(1,o)),'exact pair order')
 count=0
 for i in range(d-2):
  A=mm(marks[i],marks[i+1],d,F);C=mm(marks[i+1],marks[i+2],d,F)
  for k in range(1,n):
   word=mm(powr(C,k,d,F),powr(A,k,d,F),d,F)
   require(mm(word,word,d,F)==one,'full ambient power relation');count+=1
 return marks,{'q':F.q,'n':n,'rank':d,'alpha':a,'power_relators':count,'whole_ambient_matrix':True}

def translations(F,n):
 d=5;a=choose(F,n);basis,Q,B,sym,T=model(d,F,a);z=addv(basis(1),basis(3));one=eye(d)
 vecs=[tuple(x if i==1 else y if i==2 else 0 for i in range(d)) for x in range(F.q) for y in range(F.q)]
 trans={u:T(z,u) for u in vecs}
 for u in vecs:
  require(mm(trans[u],trans[u],d,F)==one,'T square')
  for v in vecs:require(mm(trans[u],trans[v],d,F)==trans[addv(u,v)],'T sum')
 e=basis(1);require(mm(sym(e),sym(addv(e,z)),d,F)==T(z,e),'symmetry product T')
 A=mm(sym(e),sym(basis(2)),d,F);Ai=powr(A,n-1,d,F)
 for u in vecs:require(mm(mm(A,T(z,u),d,F),Ai,d,F)==T(z,mv(A,u,d,F)),'ambient conjugation')
 return {'q':F.q,'n':n,'rank':5,'all_parameter_pairs_mod_radical':len(vecs)**2,'outer_ambient_coordinates_present':True,'all_conjugation_tests':len(vecs)}

def subgroup(gens,one,d,F):
 out={one};queue=[one]
 for x in queue:
  for g in gens:
   y=mm(x,g,d,F)
   if y not in out:out.add(y);queue.append(y)
 return out

def IP(d,F,n):
 a=choose(F,n);marks,_=relations(d,F,n,a);one=eye(d)
 subs=[subgroup([marks[i] for i in range(d) if m>>i&1],one,d,F) for m in range(1<<d)]
 for j in range(1<<d):
  for k in range(j,1<<d):require(subs[j]&subs[k]==subs[j&k],'intersection property')
 return {'q':F.q,'n':n,'rank':d,'order':len(subs[-1]),'parabolics':1<<d,'subset_pairs':(1<<d)*((1<<d)+1)//2}

def main():
 p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);a=p.parse_args()
 require(not a.report.exists(),'Refusing to overwrite report');start=time.monotonic()
 fields={e:Field(e,poly) for e,poly in [(2,0b111),(3,0b1011),(4,0b10011),(5,0b100101)]}
 rows=[]
 for e,F in fields.items():
  for n in ([F.q+1] if e==2 else [F.q-1,F.q+1]):
   alpha=choose(F,n)
   for d in range(3,9):rows.append(relations(d,F,n,alpha)[1])
 ts=[translations(fields[e],n) for e,n in [(2,5),(3,7),(3,9)]]
 ip=[IP(d,fields[e],n) for e,n,d in [(2,5,4),(3,7,3),(3,9,3)]]
 out={'status':'PASS','scope':'finite full-ambient identity diagnostics and three finite IP examples; no universal-presentation assertion or replacement of the retained all-rank theorem','matrix_relations':rows,'translation_identity_checks':ts,'finite_IP_examples':ip,'total_power_relators':sum(x['power_relators'] for x in rows),'seconds':time.monotonic()-start,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 with a.report.open('x') as f:json.dump(out,f,indent=2);f.write('\n')
 print(json.dumps({k:v for k,v in out.items() if k not in ['matrix_relations']},indent=2))
if __name__=='__main__':main()
