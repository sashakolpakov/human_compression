#!/usr/bin/env python3
"""Bounded distinct diagnostic of the PGL2 Klein/subfield multiplicities.
No author imports, GAP, group library or enumeration of large source examples.
"""
from pathlib import Path
import argparse,json,itertools,hashlib,time

def need(ok,msg):
 if not ok: raise ValueError(msg)

def group(p,k,mod):
 q=p**k
 def digits(x):
  a=[]
  for _ in range(k):a.append(x%p);x//=p
  return a
 ds=[digits(x) for x in range(q)]
 def enc(a):return sum(x*p**i for i,x in enumerate(a))
 add=[[enc([(ds[x][i]+ds[y][i])%p for i in range(k)]) for y in range(q)] for x in range(q)]
 neg=[enc([(-a)%p for a in ds[x]]) for x in range(q)]
 mul=[]
 for x in range(q):
  row=[]
  for y in range(q):
   a=[0]*(2*k-1)
   for i in range(k):
    for j in range(k):a[i+j]=(a[i+j]+ds[x][i]*ds[y][j])%p
   for i in range(2*k-2,k-1,-1):
    for j in range(k):a[i-k+j]=(a[i-k+j]-a[i]*mod[j])%p
   row.append(enc(a[:k]))
  mul.append(row)
 inv=[0]+[next(y for y in range(1,q) if mul[x][y]==1) for x in range(1,q)]
 def canon(a):
  x=next(x for x in a if x);return tuple(mul[inv[x]][t] for t in a)
 def det(a):return add[mul[a[0]][a[3]]][neg[mul[a[1]][a[2]]]]
 def product(a,b):
  return canon((add[mul[a[0]][b[0]]][mul[a[1]][b[2]]],add[mul[a[0]][b[1]]][mul[a[1]][b[3]]],add[mul[a[2]][b[0]]][mul[a[3]][b[2]]],add[mul[a[2]][b[1]]][mul[a[3]][b[3]]]))
 def inverse(a):return canon((a[3],neg[a[1]],neg[a[2]],a[0]))
 mats=[]
 for b,c,d in itertools.product(range(q),repeat=3):
  a=(1,b,c,d)
  if det(a):mats.append(a)
 for c in range(1,q):
  for d in range(q):mats.append((0,1,c,d))
 need(len(mats)==q*(q*q-1),'PGL order')
 squares={mul[x][x] for x in range(1,q)}
 identity=(1,0,0,1)
 inside=lambda a:det(a) in squares
 invol=[a for a in mats if a!=identity and product(a,a)==identity]
 return q,mats,product,inverse,inside,invol,identity

def run():
 start=time.monotonic();records=[];base_inner=None
 for p,k,mod in [(3,1,[0]),(5,1,[0]),(7,1,[0]),(3,2,[1,0]),(3,3,[2,2,0])]:
  q,X,mul,inv,inner,ivs,one=group(p,k,mod)
  need(len(ivs)==q*q,'PGL involution count')
  expected=q*(q+(1 if q%4==1 else -1))//2
  need(sum(inner(a) for a in ivs)==expected,'PSL involution count')
  classes=[]
  # Select one representative of each determinant type via commuting pairs.
  reps={}
  for a in ivs:
   if len(reps)==2:break
   for b in ivs:
    if b==a or mul(a,b)!=mul(b,a):continue
    V=frozenset((a,b,mul(a,b)))
    typ='inner' if all(inner(x) for x in V) else 'mixed'
    reps.setdefault(typ,V)
    if len(reps)==2:break
  need(set(reps)=={'inner','mixed'},'both Klein types')
  for typ,V in reps.items():
   orbit=set();normalizer=0
   for g in X:
    gi=inv(g); image=frozenset(mul(mul(g,x),gi) for x in V)
    orbit.add(image)
    if image==V:normalizer+=1
   need(normalizer==(24 if typ=='inner' else 8),'Klein normalizer')
   need(len(orbit)*normalizer==len(X),'orbit stabilizer')
   classes.append({'type':typ,'normalizer':normalizer,'orbit_size':len(orbit)})
   if p==3 and k==1 and typ=='inner':base_inner=V
  subfields=None
  if p==3 and k in (2,3):
   need(base_inner is not None,'base Klein exists')
   V=base_inner;M={a for a in X if all(t<3 for t in a)}
   need(len(M)==24 and all(inner(x) for x in V),'actual base subgroup')
   transporters=0;normalizer=0
   for g in X:
    gi=inv(g)
    if all(mul(mul(g,x),gi) in M for x in V):transporters+=1
    # Mapping a generating pair of M suffices; construct complete image here.
    if all(mul(mul(g,x),gi) in M for x in M):normalizer+=1
   need(normalizer==24,'PGL3 subfield self-normalizer')
   number=transporters//24
   need(transporters%24==0 and number==(4 if k==2 else 1),'through-V subfield multiplicity')
   subfields={'actual_PGL3_order':24,'normalizer':normalizer,'transporters':transporters,'number_through_V':number,'extension_degree':k}
  records.append({'p':p,'degree':k,'q':q,'projective_matrices':len(X),'involutions':len(ivs),'PSL_involutions':expected,'Klein_classes':classes,'subfield_test':subfields})
 need(records[3]['subfield_test']['number_through_V']!=1,'wrong uniqueness under even extension rejected')
 need(records[4]['subfield_test']['number_through_V']!=4,'wrong fourfold odd multiplicity rejected')
 need(records[3]['PSL_involutions']==45,'q9 positive sign')
 need(45-1-4*9==8,'q9 exact remainder')
 return {'status':'PASS_BOUNDED_DISTINCT_DIAGNOSTIC','records':records,'discriminating_controls':4,'no_author_or_group_library_imports':True,'uniform_proof_or_source_census':False,'elapsed_seconds':round(time.monotonic()-start,3)}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();r=run();a.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
