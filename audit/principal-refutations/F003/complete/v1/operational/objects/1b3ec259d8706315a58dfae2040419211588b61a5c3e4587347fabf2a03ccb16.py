#!/usr/bin/env python3
"""Independent bounded proof-binding and characteristic-two identity check."""
import argparse,hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
AUTHOR_SHA='a68047923f19a808995230a97060f8542179157e3c71cca006a5a994d42d9e30'
def require(v,m):
 if not v:raise ValueError(m)
def pin(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def check_scope(s):
 require(s['whole_original_accepted'] is False,'whole source still pending')
 for k in ['new_original_credit','new_question_credit','new_Lean_declarations']:require(s[k]==0,k)
 require(s['compression_factor'] is None,'no factor')
 require(s['required_programs']==[] and s['diagnostic_programs_are_proof_premises'] is False,'written proof route')
 require(len(s['proved'])==4 and len(s['pending'])==2,'bounded four statements/two unpaid routes')
# Exact Laurent polynomials over F2; variables s,t,S,T,d,e, where S=s^theta,T=t^theta.
ZERO=frozenset();ONE=frozenset({(0,)*6})
def mon(i,n=1):
 a=[0]*6;a[i]=n;return frozenset({tuple(a)})
def add(*ps):
 a=set()
 for p in ps:a.symmetric_difference_update(p)
 return frozenset(a)
def mul(p,q):
 a=set()
 for x in p:
  for y in q:
   z=tuple(i+j for i,j in zip(x,y))
   if z in a:a.remove(z)
   else:a.add(z)
 return frozenset(a)
def mm(a,b):return [[add(*(mul(a[i][k],b[k][j])for k in range(4)))for j in range(4)]for i in range(4)]
def ident():return [[ONE if i==j else ZERO for j in range(4)]for i in range(4)]
def matrix_check():
 s,t,S,T,d,e=[mon(i)for i in range(6)]
 z=ident();z[2][0]=s;z[3][0]=S;z[3][1]=s
 w=ident();w[2][0]=t;w[3][0]=T;w[3][1]=t
 j=[[ONE if i+k==3 else ZERO for k in range(4)]for i in range(4)]
 di=[d,e,mon(5,-1),mon(4,-1)];D=[[di[i]if i==k else ZERO for k in range(4)]for i in range(4)]
 M=mm(mm(mm(mm(z,D),j),w),j)
 require(mm(M,M)[0][1]==mul(mul(s,T),mul(d,e)),'square off diagonal')
 require(mm(z,z)==ident()and mm(w,w)==ident(),'root involutions in char2')
 require(mm(j,j)==ident(),'Weyl involution')
 return {'ring':'F2[s,t,S,T,d^+-1,e^+-1]','square_12':'s*T*d*e','root_squares':'identity','theta_relation_used':False}
def main():
 p=argparse.ArgumentParser();p.add_argument('--author',type=Path,default=HERE.parent/'corpus106_F003_proper_faces_v1');p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 require(pin(a.author/'manifest.json')['sha256']==AUTHOR_SHA,'author freeze')
 m=json.loads((a.author/'manifest.json').read_text())
 for x in m['exports']:require(pin(a.author/x['path'])=={k:x[k]for k in ['bytes','sha256']},x['path'])
 scope=json.loads((a.author/'scope.json').read_text());check_scope(scope)
 controls=[]
 for k,v in [('whole_original_accepted',True),('new_original_credit',1),('new_question_credit',1),('new_Lean_declarations',1),('compression_factor',2),('diagnostic_programs_are_proof_premises',True)]:
  bad=dict(scope);bad[k]=v
  try:check_scope(bad)
  except ValueError:controls.append(k)
  else:raise ValueError('accepted mutation '+k)
 report={'status':'PASS','author_manifest':AUTHOR_SHA,'author_exports':len(m['exports']),'independent_polynomial_identity':matrix_check(),'rejected_scope_mutations':controls,'scope':'Bounded written four-result review; no diagnostic rerun or classification reproving.'}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
