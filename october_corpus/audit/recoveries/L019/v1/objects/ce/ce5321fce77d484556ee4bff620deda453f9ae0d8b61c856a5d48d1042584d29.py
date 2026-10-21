from pathlib import Path
import json
if not __debug__:raise RuntimeError('normal Python required')
n=8;I=tuple(range(n))
def perm(*swaps):
 x=list(I)
 for a,b in swaps:x[a],x[b]=x[b],x[a]
 return tuple(x)
def mul(a,b):return tuple(b[a[i]]for i in I)
def power(a,e):
 x=I
 for _ in range(e):x=mul(x,a)
 return x
h0=perm((0,1),(2,3));h1=perm((1,2),(3,4),(5,6));h2=perm((4,5),(6,7));beta=perm((5,6));conj=mul(mul(h2,beta),h2);delta=mul(beta,conj)
if power(mul(h0,h1),5)!=beta or conj!=perm((4,7)) or delta in (I,h2):raise RuntimeError('IP words')
g=perm((3,4));three=mul(h0,mul(mul(g,h0),g))
if len([i for i in I if three[i]!=i])!=3 or power(three,3)!=I:raise RuntimeError('supported three cycle')
r={'status':'PASS_LITERAL_WORD_IDENTITIES','point_names':['b','x','u','v','z','p','q','w'],'fivefold_product':list(beta),'conjugate':list(conj),'intersection_element':list(delta),'tail_mark':list(h2),'three_cycle':list(three),'finite_proof_premise':False}
p=Path(__file__).with_name('word_report.json');p.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
