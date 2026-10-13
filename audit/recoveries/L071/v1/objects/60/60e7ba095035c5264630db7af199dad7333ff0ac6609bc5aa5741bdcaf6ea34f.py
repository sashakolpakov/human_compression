"""Exact elementary checks of the displayed V4 counterexample and regular action."""
from itertools import permutations
from pathlib import Path
import argparse,hashlib,json

def mul(a,b):return tuple(a[b[i]] for i in range(len(a)))
def inv(a):return tuple(a.index(i) for i in range(len(a)))
def conjugate(a,f):return mul(mul(f,a),inv(f))
def closure(gens,n):
 identity=tuple(range(n));group={identity};stack=[identity]
 while stack:
  x=stack.pop()
  for y in gens:
   z=mul(x,y)
   if z not in group:group.add(z);stack.append(z)
 return group

def automorphisms(group):
 el=sorted(group);ident=tuple(range(len(el[0])));non=[g for g in el if g!=ident]
 result=[]
 for perm in permutations(non):
  f={ident:ident,**dict(zip(non,perm))}
  if all(f[mul(x,y)]==mul(f[x],f[y]) for x in el for y in el):
   result.append(tuple(el.index(f[x]) for x in el))
 return result

def action(group):
 el=sorted(group);n=len(el[0]);normalizer=[];centralizer=[];images=set()
 for f in permutations(range(n)):
  conj=[conjugate(g,f) for g in el]
  if set(conj)==group:
   normalizer.append(f);images.add(tuple(el.index(x) for x in conj))
   if conj==el:centralizer.append(f)
 assert len(normalizer)==len(centralizer)*len(images)
 return {'normalizer_order':len(normalizer),'centralizer_order':len(centralizer),'automorphism_image_order':len(images)},images

def main(out):
 out.mkdir(parents=True,exist_ok=False)
 a=(1,0,2,3,4,5);b=(0,1,3,2,5,4)
 G=closure([a,b],6);assert len(G)==4
 assert mul(a,a)==mul(b,b)==tuple(range(6)) and mul(a,b)==mul(b,a)
 assert closure([a],6)&closure([b],6)=={tuple(range(6))}
 aut=automorphisms(G);assert len(aut)==6
 bad,images=action(G);assert len(images)==1
 edges=[sum(x!=i for i,x in enumerate(g))//2 for g in (a,b)]
 assert edges==[1,2] and edges!=list(reversed(edges))
 unrelated=closure([(1,0,2,3,4,5),(1,2,0,3,4,5)],6)
 assert len(unrelated)==6
 el=sorted(G);regular={tuple(el.index(mul(g,x)) for x in el) for g in el}
 good,images=action(regular);assert len(images)==6
 report={'status':'PASS','counterexample_group_order':len(G),'abstract_automorphism_order':len(aut),'unrelated_S3_embedding_order':len(unrelated),'colour_zero_edges':[edges[0],edges[1]],'counterexample_action':bad,'regular_action':good,'whole_original_credit':0,'formal_verification':False,'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);main(p.parse_args().out)
