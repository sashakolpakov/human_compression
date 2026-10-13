from pathlib import Path
import json
W=Path(__file__).resolve().parent;n=14;I=tuple(range(n))
def mul(*ps):
 v=I
 for p in ps:v=tuple(p[x] for x in v)
 return v
def powr(p,k):return mul(*([p]*k))
def tr(a,b):
 p=list(I);p[a],p[b]=p[b],p[a];return tuple(p)
def diag(a,b):return mul(tr(2*a,2*b),tr(2*a+1,2*b+1))
def sw(cycle):
 p=list(range(n//2))
 for a,b in zip(cycle,cycle[1:]+cycle[:1]):p[a]=b
 inv=[p.index(i) for i in range(n//2)]
 return tuple(2*(p[x//2] if x%2==0 else inv[x//2])+(1-x%2) for x in range(n))
l=sw([]);r=sw([0,1,2]);s=mul(tr(2,6),tr(5,7));spr=mul(l,s,l);z=mul(diag(1,2),l);records=[]
for e in [(3,4),(4,5)]:
 g=mul(diag(*e),diag(0,1),l);t=mul(l,g)
 if e==(3,4):w=mul(powr(mul(t,spr),2),powr(mul(s,t),2),s,powr(mul(spr,t),2),s,spr,s)
 else:w=powr(mul(l,powr(mul(s,g),2),s),2)
 if w!=mul(r,l):raise RuntimeError('word fails')
 records.append({'selected_edge':e,'word_images':list(w),'equals_r_l_on_14_points':True,'generic_outside_pair_fixed':w[12:]==(12,13)})
for s1 in [s,sw([1,3,2])]:
 for t in [r,l,s1]:
  if mul(z,t)!=mul(t,z):raise RuntimeError('z not central')
S=sw([1,3,2]);walk=[0,3,4,1,2,5,6,7]
for e in [(3,4),(4,5)]:
 g=mul(diag(*e),diag(0,1),l)
 for a,b,p in zip(walk,walk[1:],[r,S,r,g,r,S,r]):
  if p[a]!=b:raise RuntimeError('walk fails')
report={'status':'PASS_UNIFORM_PERMUTATION_IDENTITIES','right_action':True,'points':14,'records':records,'central_pair_both_forms':True,'both_eight_point_walks':True,'scope':'Independent arithmetic check of displayed universal identities, not a classification premise.'};(W/'word_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
