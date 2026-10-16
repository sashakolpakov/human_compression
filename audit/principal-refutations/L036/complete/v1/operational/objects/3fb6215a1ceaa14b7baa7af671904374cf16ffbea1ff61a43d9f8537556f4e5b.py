"""A small complete isomorphism to GL(2,3), with explicit quaternion/complement data."""
import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
from itertools import product
import json
H=Path(__file__).resolve().parent
SOURCE=H.parents[2]/'algebra/subgroup_atlas/structural_labels_pilot_v1/discovery01/m11_13.json'
I=(1,0,0,1);MINUS=(2,0,0,2)
def need(b,m):
 if not b:raise ValueError(m)
def pmul(p,q):return tuple(q[x] for x in p)
def mmul(a,b):return ((a[0]*b[0]+a[1]*b[2])%3,(a[0]*b[1]+a[1]*b[3])%3,(a[2]*b[0]+a[3]*b[2])%3,(a[2]*b[1]+a[3]*b[3])%3)
def pinv(p):
 q=[0]*len(p)
 for i,x in enumerate(p):q[x]=i
 return tuple(q)
def order(x,mul,identity):
 y=identity
 for i in range(1,49):
  y=mul(y,x)
  if y==identity:return i
 raise ValueError('element order bound')
def transport(gens,images):
 mapping={tuple(range(11)):I};queue=[tuple(range(11))]
 for p in queue:
  for g,a in zip(gens,images):
   q=pmul(p,g);b=mmul(mapping[p],a)
   if q in mapping:
    if mapping[q]!=b:return None
   else:mapping[q]=b;queue.append(q)
 return mapping

def calculate():
 data=json.loads(SOURCE.read_text());elts=[tuple(p) for p in data['elements']];idx={p:i for i,p in enumerate(elts)}
 need(len(elts)==48 and len(idx)==48,'actual 48-element group')
 c=data['certificate'];N=[elts[i] for i in c['normal']['elements']];C=[elts[i] for i in c['complement']['elements']]
 identity=tuple(range(11));need(len(N)==8 and len(C)==6 and set(N)&set(C)=={identity},'acquired normal complement')
 kernel=[x for x in C if all(pmul(pmul(pinv(x),n),x)==n for n in N)]
 need(kernel==[identity],'faithful S3 action on Q8')
 qi=elts[c['normal']['i']];qj=elts[c['normal']['j']]
 cr=next(x for x in C if order(x,pmul,identity)==3)
 cs=next(x for x in C if order(x,pmul,identity)==2)
 allmat=[a for a in product(range(3),repeat=4) if (a[0]*a[3]-a[1]*a[2])%3]
 qgens=[(0,1,2,0),(1,1,1,2)];cgens=[(1,1,0,1),(1,0,0,2)]
 def generated(gs):
  rows=[I];seen={I}
  for a in rows:
   for g in gs:
    b=mmul(a,g)
    if b not in seen:seen.add(b);rows.append(b)
  return rows
 Q=generated(qgens);D=generated(cgens)
 need(len(Q)==8 and len(D)==6 and set(Q)&set(D)=={I} and {mmul(q,d) for q in Q for d in D}==set(allmat),'explicit GL2(3)=Q8.S3')
 need(order(qgens[0],mmul,I)==order(qgens[1],mmul,I)==4 and mmul(qgens[0],qgens[0])==MINUS and mmul(qgens[1],qgens[1])==MINUS and mmul(qgens[0],qgens[1])!=mmul(qgens[1],qgens[0]),'matrix Q8')
 need(order(cgens[0],mmul,I)==3 and order(cgens[1],mmul,I)==2 and mmul(mmul(cgens[1],cgens[0]),cgens[1])==mmul(cgens[0],cgens[0]),'matrix S3')
 normalforms={pmul(n,c):(n,c) for n in N for c in C};need(set(normalforms)==set(elts),'unique actual normal forms')
 gens=[tuple(g) for g in data['permutation_generators']]
 candidate=None;tried=0
 for a,b in product(Q,repeat=2):
  qm=transport([qi,qj],[a,b])
  if qm is None or set(qm)!=set(N) or len(set(qm.values()))!=8:continue
  for r,s in product(D,repeat=2):
   cm=transport([cr,cs],[r,s])
   if cm is None or set(cm)!=set(C) or len(set(cm.values()))!=6:continue
   tried+=1;f={x:mmul(qm[n],cm[c]) for x,(n,c) in normalforms.items()}
   if len(set(f.values()))==48 and all(f[pmul(x,g)]==mmul(f[x],f[g]) for x in elts for g in gens):candidate=f;break
  if candidate is not None:break
 need(candidate is not None,'explicit bijective homomorphism found')
 need(set(candidate.values())==set(allmat) and all(candidate[pmul(x,y)]==mmul(candidate[x],candidate[y]) for x in elts for y in elts),'all2304 products')
 return dict(status='PASS_L036_LITERAL_GL2_3_ALIAS',actual_class=27,source_atlas_row=13,actual_generator_indices=[idx[g] for g in gens],actual_generators=gens,actual_quaternion_generators=[qi,qj],actual_complement_generators=[cr,cs],faithful_complement_kernel_indices=[idx[x] for x in kernel],matrix_quaternion_generators=qgens,matrix_complement_generators=cgens,actual_elements=elts,matrix_images=[candidate[x] for x in elts],matrix_generator_images=[candidate[g] for g in gens],all_invertible_matrices=allmat,full_product_checks=48*48,candidate_complement_transports=tried,GAP_launched=False,whole_source_accepted=False)
if __name__=='__main__':print(json.dumps(calculate(),separators=(',',':')))
