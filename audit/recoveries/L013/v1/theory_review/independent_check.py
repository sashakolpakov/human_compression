"""Distinct literal field-graph checks; imports no author code or graph package."""
from pathlib import Path
from collections import deque
import argparse,hashlib,json

PIN='4ec2b452fd3696928039395aadee00a8f0aca25ff372c44dabc03f8dbb305ea3'
def need(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
class Arithmetic:
 def __init__(self,p,m=1,coefficients=()):
  self.p=p;self.m=m;self.q=p**m;self.coefficients=coefficients
  self.digits=[tuple((a//p**i)%p for i in range(m)) for a in range(self.q)]
  self.sum=[[self.encode(tuple((x+y)%p for x,y in zip(A,B))) for B in self.digits] for A in self.digits]
  self.product=[[self.multiply(A,B) for B in self.digits] for A in self.digits]
  for a in range(1,self.q):need(len(set(self.product[a]))==self.q,'actual field multiplication')
 def encode(self,A):return sum(a*self.p**i for i,a in enumerate(A))
 def multiply(self,A,B):
  c=[0]*(2*self.m-1)
  for i,a in enumerate(A):
   for j,b in enumerate(B):c[i+j]=(c[i+j]+a*b)%self.p
  for i in range(2*self.m-2,self.m-1,-1):
   for j,a in enumerate(self.coefficients):c[i-self.m+j]=(c[i-self.m+j]-c[i]*a)%self.p
  return self.encode(c[:self.m])
 def powers(self,a):
  x=1;seen=[]
  while x not in seen:seen.append(x);x=self.product[x][a]
  return seen
 def primitive(self):return next(a for a in range(1,self.q) if len(self.powers(a))==self.q-1)

def graph1(f,S=(),T=()):
 V=[(kind,x,y) for kind in [0,1] for x in range(f.q) for y in range(f.q)];index={v:i for i,v in enumerate(V)};A=[set() for _ in V]
 for i,(kind,x,y) in enumerate(V):
  if kind==0:
   for m in range(f.q):
    for b in range(f.q):
     if f.sum[f.product[m][x]][b]==y:
      j=index[(1,m,b)];A[i].add(j);A[j].add(i)
  for a in S if kind==0 else T:A[i].add(index[(kind,x,f.sum[y][a])])
 return V,A

def graph2(f,augment=True):
 W=[(x,y) for x in range(f.q) for y in range(f.q) if x or y];V=[(kind,v) for kind in [0,1] for v in W];index={v:i for i,v in enumerate(V)};A=[set() for _ in V]
 for i,(kind,v) in enumerate(V):
  if kind==0:
   for u in W:
    if f.sum[f.product[u[0]][v[0]]][f.product[u[1]][v[1]]]==1:
     j=index[(1,u)];A[i].add(j);A[j].add(i)
  if augment:
   primitive=f.primitive();a=primitive if kind==0 else f.product[primitive][primitive];w=tuple(f.product[a][x] for x in v);j=index[(kind,w)];A[i].add(j);A[j].add(i)
 return V,A

def metrics(A):
 need(all(u not in row and all(u in A[v] for v in row) for u,row in enumerate(A)),'simple undirected')
 diameter=0;girth=None;D=[]
 for s in range(len(A)):
  d=[-1]*len(A);d[s]=0;parent=[-1]*len(A);q=deque([s])
  while q:
   u=q.popleft()
   for v in A[u]:
    if d[v]<0:d[v]=d[u]+1;parent[v]=u;q.append(v)
    elif parent[u]!=v and parent[v]!=u:
     length=d[u]+d[v]+1;girth=length if girth is None else min(length,girth)
  need(-1 not in d,'connected');D.append(d);diameter=max(diameter,max(d))
 return dict(order=len(A),degrees=sorted({len(x) for x in A}),girth=girth,diameter=diameter),D

def shortset(f,S,T):
 two={f.sum[a][b] for a in S for b in S};three={f.sum[a][b] for a in two for b in S};return {0}|set(S)|two|three|set(T)

def run():
 cases=[];fibres=0
 def base(kind,q):
  f=Arithmetic(q);V,A=(graph1(f) if kind==1 else graph2(f,False));actual,D=metrics(A)
  expected=dict(order=2*q*q if kind==1 else 2*(q*q-1),degrees=[q],girth=8 if(kind,q)==(1,2) else 6,diameter=3 if(kind,q)==(2,2) else 4)
  need(actual==expected,'base exception or q3');cases.append(dict(name=f'base_type{kind}_q{q}',**actual))
 for q in [2,3]:
  for kind in [1,2]:base(kind,q)
 for f,S,T,diam in [(Arithmetic(2,2,(1,1)),[1],[2],4),(Arithmetic(2,3,(1,1,0)),[1],[2],4),(Arithmetic(5),[1,4],[2,3],2),(Arithmetic(7),[1,6],[2,5],3),(Arithmetic(11),[1,10],[2,9],4)]:
  V,A=graph1(f,S,T);actual,D=metrics(A);need(actual==dict(order=2*f.q*f.q,degrees=[f.q+len(S)],girth=5,diameter=diam),'additive metrics')
  for i,(kind,x,y) in enumerate(V):
   reachable=shortset(f,S,T) if kind==0 else shortset(f,T,S)
   for j,(other,x2,z) in enumerate(V):
    if kind==other and x==x2:
     expected=any(f.sum[y][delta]==z for delta in reachable);need((D[i][j]<=3)==expected,'exact entire fibre short-path equivalence');fibres+=1
  cases.append(dict(name=f'additive_q{f.q}',**actual))
 for f,diam in [(Arithmetic(2,3,(1,1,0)),3),(Arithmetic(11),4),(Arithmetic(2,4,(1,1,0,0)),4)]:
  V,A=graph2(f);actual,D=metrics(A);need(actual==dict(order=2*(f.q*f.q-1),degrees=[f.q+2],girth=5,diameter=diam),'multiplicative metrics')
  powers=f.powers(f.primitive());index={v:i for i,v in enumerate(V)}
  for i,(kind,v) in enumerate(V):
   # Complete point-ray short-path criterion; line rays have a different internal step.
   if kind==0:
    for exponent,t in enumerate(powers):
     j=index[(0,tuple(f.product[t][a] for a in v))];need((D[i][j]<=3)==(exponent in {n%len(powers) for n in range(-3,4)}),'multiplicative point-ray criterion');fibres+=1
  cases.append(dict(name=f'multiplicative_q{f.q}',**actual))
 # A nonprime odd-field diagnostic: additive shifts are trapped in F5, leaving 20 witnesses.
 f=Arithmetic(5,2,(2,0));short=shortset(f,[1,4],[2,3]);need(short==set(range(5)),'F25 prime subfield shortset')
 cases.append(dict(name='additive_q25_shortset_only',field=25,short_changes=sorted(short),uncovered=20,full_graph_enumerated=False))
 controls=[]
 def rejected(name,fn):
  try:fn()
  except ValueError as e:controls.append(dict(name=name,rejection=str(e)));return
  raise ValueError('control survived '+name)
 rejected('source small middle k2 cannot assert pentagon',lambda:need(next(x['girth'] for x in cases if x['name']=='base_type1_q2')==5,'actual C8 has girth8'))
 rejected('q7 cycle family cannot assert diameter4',lambda:need(next(x['diameter'] for x in cases if x['name']=='additive_q7')==4,'actual diameter3'))
 rejected('q8 multiplicative family cannot assert diameter4',lambda:need(next(x['diameter'] for x in cases if x['name']=='multiplicative_q8')==4,'actual diameter3'))
 # Removing disjointness actually creates a quadrangle, and a too-small line cycle does too.
 V,A=graph1(Arithmetic(5),[1,4],[1,4]);bad,_=metrics(A);rejected('overlapping shift sets',lambda:need(bad['girth']>=5,'actual quadrangle'))
 V,A=graph2(Arithmetic(3,2,(1,0)));bad2,_=metrics(A);rejected('type2 q9 line cycle4',lambda:need(bad2['girth']>=5,'actual quadrangle'))
 return dict(status='PASS_DISTINCT_OPTIONAL_DIAGNOSTICS',cases=cases,full_graph_cases=len(cases)-1,exact_fibre_pair_comparisons=fibres,controls=controls,uniform_proof_by_finite_checks=False,source_completeness_claim=False)

def main(a):
 need(sha(a.author/'manifest.json')==PIN,'frozen author manifest');m=json.loads((a.author/'manifest.json').read_text())
 for r in m['exports']:
  p=a.author/r['path'];need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'author binding '+r['path'])
 scope=json.loads((a.author/'scope.json').read_text());need(scope['complete_source_recovery'] is False and scope['new_Lean_declarations']==0 and scope['compression_factor'] is None,'bounded nonformal scope')
 if a.study_root:
  for r in json.loads((a.author/'dependencies.json').read_text())['source_bindings']:
   p=a.study_root/r['path'];need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'source dependency')
 result=run();result.update(author_manifest=PIN,exports=len(m['exports']));a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(status=result['status'],exports=result['exports'],full_graphs=result['full_graph_cases'],fibre_pairs=result['exact_fibre_pair_comparisons'],controls=len(result['controls']))))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--author',type=Path,required=True);p.add_argument('--study-root',type=Path);p.add_argument('--out',type=Path,required=True);main(p.parse_args())
