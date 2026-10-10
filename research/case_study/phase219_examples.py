#!/usr/bin/env python3
"""Emit small genuine proof traces; Lean must kernel-check their acceptance."""
from pathlib import Path
from collections import deque
import argparse,json
BASE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
if args.out.exists() or args.out.is_symlink():raise RuntimeError('Fresh output directory required')
OUT=args.out.resolve();OUT.mkdir(parents=True)

def certificate(n,facet):
 N=n if facet else 2*n
 def go(u,s):
  if facet:return (-u if s==0 else 1-u)%n
  k,e=divmod(u,2)
  return 2*((k+(0 if s==0 else (1 if e==0 else -1)))%n)+(1-e)
 table=[[go(u,s) for s in range(2)] for u in range(N)]
 known={};reps={0:[]};trace=[]
 def install(u,s,v,instruction):
  if (u,s) in known:
   if known[u,s]!=v:raise RuntimeError('conflict')
   return
  if table[u][s]!=v or table[v][s]!=u:raise RuntimeError('oracle')
  known[u,s]=v;trace.append(instruction)
  if (v,s) not in known:
   known[v,s]=u;trace.append(dict(kind='reverse',edge=[u,s,v]))
 if facet:install(0,0,0,dict(kind='rootLoop',s=0))
 pending=deque([0])
 while pending:
  u=pending.popleft()
  for s,v in enumerate(table[u]):
   if v not in reps:
    reps[v]=reps[u]+[s];pending.append(v)
    install(u,s,v,dict(kind='tree',u=u,s=s,v=v))
 rel=[0,1]*n
 changed=True
 while len(known)<2*N and changed:
  before=len(known)
  for u in range(N):
   a=b=u;l=0;r=len(rel);p=[];q=[]
   while l<r and (a,rel[l]) in known:
    v=known[a,rel[l]];p.append([a,rel[l],v]);a=v;l+=1
   while l<r and (b,rel[r-1]) in known:
    v=known[b,rel[r-1]];q.append([b,rel[r-1],v]);b=v;r-=1
   if l==r and a!=b:raise RuntimeError('coincidence')
   if l+1==r:install(a,rel[l],b,dict(kind='gap',u=u,p=p,s=rel[l],q=q))
  changed=len(known)>before
 if len(known)!=N*2:raise RuntimeError('incomplete')
 return dict(nodes=N,subgens=[0] if facet else [],reps=[reps[i] for i in range(N)],trace=trace,relation=rel)
def ls(xs):return '['+', '.join(map(str,xs))+']'
def edge(e):return '⟨'+', '.join(map(str,e))+'⟩'
def inst(i):
 k=i['kind']
 if k=='rootLoop':return f'.rootLoop {i["s"]}'
 if k=='tree':return f'.tree {i["u"]} {i["s"]} {i["v"]}'
 if k=='reverse':return f'.reverse {edge(i["edge"])}'
 return f'.gap {i["u"]} ['+', '.join(map(edge,i['p']))+f'] {i["s"]} ['+', '.join(map(edge,i['q']))+']'
rows=['import CosetUpperCertificate','', 'namespace HumanCompression.CosetUpperCertificate.Examples',
 'set_option maxRecDepth 10000','set_option maxHeartbeats 2000000','']
allcases={}
for name,facet in [('facet11',True),('group22',False)]:
 c=certificate(11,facet);allcases[name]=c;N=c['nodes']
 rows += [f'def {name}Reps : Fin {N} → List (Fin 2) := fun v =>',
   '  '+ls([ls(w) for w in c['reps']])+f'[v.val]!',
   f'def {name}Trace : List (Instruction (Fin 2) (Fin {N})) :=',
   '  [ '+',\n    '.join(inst(i) for i in c['trace'])+' ]',
   f'def {name}Rels : List (List (Fin 2)) := [{ls(c["relation"])}]',
   f'theorem {name}_accepted : accept {name}Rels {ls(c["subgens"])} 0 {name}Reps {name}Trace = true := by decide',
   f'theorem {name}_index_bound :',
   f'    (facet (listSet {name}Rels) (listSet ({ls(c["subgens"])} : List (Fin 2)))).index ≤ {N} := by',
   f'  have h := accepted_universal_index_bound {name}Rels {ls(c["subgens"])} 0 {name}Reps {name}Trace (by decide) {name}_accepted',
   '  simpa using h.2','']
rows += [
 'theorem group22_order_bound : Nat.card (Universal (listSet group22Rels)) ≤ 22 := by',
 '  simpa [facet, listSet] using group22_index_bound',
 '#print axioms group22_order_bound',
 'theorem root_alone_rejected : accept facet11Rels [0] (0 : Fin 1) (fun _ => []) [.rootLoop 0] = false := by decide',
 'theorem no_relators_rejected : accept ([] : List (List (Fin 2))) [] 0 group22Reps group22Trace = false := by decide',
 'theorem empty_trace_rejected : accept group22Rels [] 0 group22Reps [] = false := by decide',
 'theorem false_tree_rejected : step group22Rels [] 0 group22Reps [] (.tree 0 0 0) = none := by decide',
 '', '#print axioms facet11_accepted','#print axioms facet11_index_bound',
 '#print axioms group22_accepted','#print axioms group22_index_bound',
 '#print axioms root_alone_rejected','#print axioms no_relators_rejected',
 '#print axioms empty_trace_rejected','#print axioms false_tree_rejected',
 '', 'end HumanCompression.CosetUpperCertificate.Examples','']
(OUT/'CosetUpperExamples.lean').write_text('\n'.join(rows))
(OUT/'example_traces.json').write_text(json.dumps(allcases,indent=2)+'\n')
print(json.dumps({k:dict(nodes=v['nodes'],instructions=len(v['trace'])) for k,v in allcases.items()}))
