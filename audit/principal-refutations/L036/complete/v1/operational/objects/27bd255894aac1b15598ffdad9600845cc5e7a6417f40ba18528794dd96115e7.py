"""Verify the supplied 48-element matrix bijection, without searching for it."""
import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
from itertools import product
import json
H=Path(__file__).resolve().parent
SOURCE=H.parents[2]/'algebra/subgroup_atlas/structural_labels_pilot_v1/discovery01/m11_13.json'
def need(b,m):
 if not b:raise ValueError(m)
def mul(a,b):return ((a[0]*b[0]+a[1]*b[2])%3,(a[0]*b[1]+a[1]*b[3])%3,(a[2]*b[0]+a[3]*b[2])%3,(a[2]*b[1]+a[3]*b[3])%3)
def pmul(a,b):return tuple(b[x] for x in a)
def verify(cert):
 source=json.loads(SOURCE.read_text());elts=[tuple(p) for p in source['elements']]
 need(cert['actual_elements']==source['elements'] and cert['actual_generators']==source['permutation_generators'],'literal acquired group')
 images=[tuple(m) for m in cert['matrix_images']]
 matrices={m for m in product(range(3),repeat=4) if (m[0]*m[3]-m[1]*m[2])%3}
 need(len(images)==len(elts)==48 and len(set(images))==48 and set(images)==matrices,'full matrix bijection')
 image=dict(zip(elts,images));need(image[tuple(range(11))]==(1,0,0,1),'identity')
 for x in elts:
  for y in elts:need(image[pmul(x,y)]==mul(image[x],image[y]),'matrix multiplication table')
 N=[elts[i] for i in source['certificate']['normal']['elements']]
 C=[elts[i] for i in source['certificate']['complement']['elements']]
 kernel=[x for x in C if all(pmul(x,n)==pmul(n,x) for n in N)]
 need(kernel==[tuple(range(11))],'faithful complement action')
 need(cert['matrix_generator_images']==[list(image[tuple(g)]) for g in source['permutation_generators']],'named generator images')
 return dict(status='PASS_LITERAL_GL2_3_BIJECTION',elements=48,products=2304,faithful_S3_action=True,search_performed=False)
if __name__=='__main__':print(json.dumps(verify(json.loads((H/'gl23.stdout').read_text()))))
