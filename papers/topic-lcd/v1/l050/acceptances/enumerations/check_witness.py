#!/usr/bin/env python3
"""Independent coordinate certificate: no author imports or large enumeration."""
from pathlib import Path
import argparse,copy,hashlib,itertools,json
ROOT=Path(__file__).resolve().parent

def need(x,m):
 if not x:raise ValueError(m)
def reduced(rows):
 a=[list(r)for r in rows];d=0;piv=[]
 for j in range(len(a[0])):
  i=next((i for i in range(d,len(a))if a[i][j]%3),None)
  if i is None:continue
  a[d],a[i]=a[i],a[d];v=pow(a[d][j],-1,3);a[d]=[v*x%3 for x in a[d]]
  for i in range(len(a)):
   if i!=d:
    c=a[i][j];a[i]=[(x-c*y)%3 for x,y in zip(a[i],a[d])]
  piv.append(j);d+=1
  if d==len(a):break
 return a[:d],piv

def graph():
 # Explicit multiplication table for F_2[t]/(t^2+t+1), independently of
 # the author's shift-and-reduce implementation.
 mul=((0,0,0,0),(0,1,2,3),(0,2,3,1),(0,3,1,2))
 def pairing(v,w):
  z=0
  for x,y in zip(v,w):z^=mul[x][y]
  return z
 points=[v for v in itertools.product(range(4),repeat=3)if v!=(0,0,0)and v[next(i for i,x in enumerate(v)if x)]==1]
 flags=[(x,l)for x in points for l in points if pairing(x,l)==0]
 need(len(points)==21 and len(flags)==105,'PG flags')
 rows=[]
 for i,(x,l)in enumerate(flags):
  row=[]
  for j,(y,m)in enumerate(flags):
   # Complement's adjacency: distinct noncommon point/line and at
   # least one cross incidence. Complement this to obtain degree72.
   edge=(x!=y and l!=m and (pairing(x,m)==0 or pairing(y,l)==0))
   row.append(int(i!=j and not edge))
  rows.append(row)
 need(all(sum(r)==72 for r in rows),'graph degree')
 for i in range(105):
  need(rows[i][i]==0,'diagonal')
  for j in range(i):
   need(rows[i][j]==rows[j][i],'symmetry')
   need(sum(x*y for x,y in zip(rows[i],rows[j]))==(51 if rows[i][j] else 45),'SRG parameters')
 return rows

def verify(certificate,basis,adjacency):
 need(certificate['n']==105 and certificate['k']==19,'parameters')
 need(len(basis)==19 and all(len(r)==105 and set(r)<=set(range(3))for r in basis),'basis format')
 differences=[[(x-y)%3 for x,y in zip(r,adjacency[0])]for r in adjacency[1:]]
 actual,piv=reduced(differences)
 need(actual==basis,'exact independently reconstructed difference basis')
 need(len(actual)==19 and len(reduced(adjacency)[0])==20,'independent ranks')
 words=certificate['witnesses'];need(len(words)==19,'witness count')
 coeffs=[];actualwords=[]
 for row in words:
  c=row['coefficients'];w=row['word'];need(len(c)==19 and set(c)<=set(range(3)),'coefficient vector')
  calculated=[sum(c[i]*basis[i][j]for i in range(19))%3 for j in range(105)]
  need(calculated==w,'word coordinates');need(sum(x!=0 for x in w)==36,'weight36')
  coeffs.append(c);actualwords.append(w)
 need(len(reduced(coeffs)[0])==19,'coefficient independence')
 need(len(reduced(actualwords)[0])==19,'word independence')
 return {'rank_adjacency':20,'rank_differences':19,'coefficient_rank':19,'word_rank':19,'weights':[36]*19,'basis_pivots':piv,'graph_parameters':[105,72,51,45]}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();need(not args.out.exists(),'fresh output');args.out.mkdir(parents=True)
 f=ROOT/'evidence/105_differences.txt';ls=f.read_text().splitlines();need(ls[0]=='105 19','basis header');basis=[list(map(int,s))for s in ls[1:]]
 cert=json.loads((ROOT/'weight36_witness.json').read_text());need(hashlib.sha256(f.read_bytes()).hexdigest()==cert['basis_sha256'],'basis pin');a=graph();result=verify(cert,basis,a)
 full=json.loads((ROOT/'evidence/105_adjacency.json').read_text());diff=json.loads((ROOT/'evidence/105_differences.json').read_text())
 need(full['weight_counts'][36]==diff['weight_counts'][36]==3360,'equal numbers of weight36 words')
 need(sum(full['weight_counts'])==3**20 and sum(diff['weight_counts'])==3**19,'complete cardinalities')
 controls=[]
 def reject(label,c,b):
  try:verify(c,b,a)
  except ValueError:controls.append(label)
  else:raise ValueError('mutation accepted: '+label)
 bad=copy.deepcopy(cert);bad['witnesses'][0]['coefficients'][0]=(bad['witnesses'][0]['coefficients'][0]+1)%3;reject('coefficient change',bad,basis)
 bad=copy.deepcopy(cert);bad['witnesses'][0]['word'][0]=(bad['witnesses'][0]['word'][0]+1)%3;reject('word change',bad,basis)
 bad=copy.deepcopy(cert);bad['witnesses'][1]=copy.deepcopy(bad['witnesses'][0]);reject('dependent collection',bad,basis)
 badbasis=copy.deepcopy(basis);badbasis[0][0]=(badbasis[0][0]+1)%3;reject('wrong basis',cert,badbasis)
 result.update(status='PASS_INDEPENDENT_COORDINATE_WITNESS',controls=controls,source_weight36_code_equals_difference_code=True,
 equality_reason='D is contained in the adjacency code. The completed enumerators give 3360 weight36 words in each, so those sets coincide. Nineteen independent weight36 words span D.',
 retained_input='Uniqueness of the (105,32,4,12) strongly regular graph identifies this explicit complement with the named graph; not proved here.',large_enumeration_restarted=False)
 (args.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
