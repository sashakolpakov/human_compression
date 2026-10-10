#!/usr/bin/env python3
"""Untrusted generator of direct Lean deductions for the frozen 1024-name certificate."""
from pathlib import Path
from collections import deque
import argparse,gzip,hashlib,json
BASE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
if args.out.exists() or args.out.is_symlink():raise RuntimeError('Fresh output directory required')
OUT=args.out.resolve();OUT.mkdir(parents=True)
meta=json.loads((BASE/'phase214_tables.json').read_text())['tables'][0]
packed=(BASE/meta['path']).read_bytes()
if hashlib.sha256(packed).hexdigest()!=meta['gzip_sha256']:raise RuntimeError('packed binding')
raw=gzip.decompress(packed)
if hashlib.sha256(raw).hexdigest()!=meta['raw_sha256']:raise RuntimeError('raw binding')
ints=list(map(int,raw.split()));N,d=ints[:2]
if (N,d)!=(1024,3):raise RuntimeError('header')
table=[[v-1 for v in ints[2+i*d:2+(i+1)*d]] for i in range(N)]
rels=[]
for i in range(d):
 for j in range(i+1,d):rels.append([i,j]*(11 if j==i+1 else 2))
for i in range(d-2):
 for k in range(1,11):rels.append(([i+1,i+2]*k+[i,i+1]*k)*2)
known={};reps={0:[]};steps=[]
def install(u,s,v,reason):
 if table[u][s]!=v or table[v][s]!=u:raise RuntimeError('oracle mismatch')
 if (u,s) in known:
  if steps[known[u,s]]['edge']!=[u,s,v]:raise RuntimeError('conflict')
  return
 j=len(steps);known[u,s]=j;steps.append(dict(edge=[u,s,v],**reason))
 if (v,s) not in known:
  known[v,s]=len(steps);steps.append(dict(edge=[v,s,u],kind='reverse',previous=j))
for s in range(d-1):install(0,s,0,dict(kind='rootLoop'))
pending=deque([0])
while pending:
 u=pending.popleft()
 for s,v in enumerate(table[u]):
  if v not in reps:
   reps[v]=reps[u]+[s];pending.append(v);install(u,s,v,dict(kind='tree'))
while len(known)<N*d:
 before=len(known)
 for u in range(N):
  for r,w in enumerate(rels):
   a=b=u;l=0;t=len(w);p=[];q=[]
   while l<t and (a,w[l]) in known:
    j=known[a,w[l]];p.append(j);a=steps[j]['edge'][2];l+=1
   while l<t and (b,w[t-1]) in known:
    j=known[b,w[t-1]];q.append(j);b=steps[j]['edge'][2];t-=1
   if l==t and a!=b:raise RuntimeError('unproved coincidence')
   if l+1==t:install(a,w[l],b,dict(kind='gap',start=u,relation=r,forward=p,backward=q,left=w[:l],right=w[t:]))
 if len(known)==before:raise RuntimeError('incomplete')
ls=lambda xs:'['+', '.join(map(str,xs))+']'
rows=['import CosetUpperCertificate','namespace HumanCompression.CosetUpperCertificate.RankThree',
 'set_option maxRecDepth 20000','set_option maxHeartbeats 0',
 'def relators : List (List (Fin 3)) := '+ls([ls(w) for w in rels]),
 'REPRESENTATIVES_PLACEHOLDER',
 'def representatives (u : Fin 1024) : List (Fin 3) := representativesData[u.val]!',
 'abbrev D := Derives (listSet relators) (listSet ([0, 1] : List (Fin 3))) (0 : Fin 1024) representatives']
for i,w in enumerate(rels):rows.append(f'private theorem relator{i} : ({ls(w)} : List (Fin 3)) ∈ listSet relators := by change _ ∈ relators; decide')
def path(indices,start):
 if not indices:return f'(Derives.refl {start})'
 e=steps[indices[-1]]['edge'];out=f'(Derives.refl {e[2]})'
 for i in reversed(indices):out=f'(Derives.append edge{i} {out})'
 return out
for i,t in enumerate(steps):
 u,s,v=t['edge'];start=f'private theorem edge{i} : D {u} [{s}] {v} := '
 if t['kind']=='rootLoop':proof=f'.rootLoop {s} (by change _ ∈ ([0, 1] : List (Fin 3)); decide)'
 elif t['kind']=='tree':proof=f'.tree {u} {s} {v} (by rfl)'
 elif t['kind']=='reverse':proof=f'.reverse edge{t["previous"]}'
 else:
  proof=f'.gap (u := {t["start"]}) (p := {ls(t["left"])}) (q := {ls(t["right"])}) relator{t["relation"]} '+path(t['forward'],t['start'])+' '+path(t['backward'],t['start'])
 rows.append(start+proof)

defs=['private def representative0 : List (Fin 3) := []']
for t in steps:
 if t['kind']=='tree':
  u,k,v=t['edge'];defs.append(f'private def representative{v} : List (Fin 3) := representative{u} ++ [{k}]')
if len(defs)!=N:raise RuntimeError('tree closure')
defs.append('def representativesData : Array (List (Fin 3)) := #['+', '.join(f'representative{u}' for u in range(N))+']')
pos=rows.index('REPRESENTATIVES_PLACEHOLDER');rows[pos:pos+1]=defs
rows += ['def pairWord (a b : Fin 3) (n : Nat) : List (Fin 3) := (List.replicate n [a, b]).flatten',
 'def tripleWord (k : Nat) : List (Fin 3) := let w := pairWord 1 2 k ++ pairWord 0 1 k; w ++ w',
 'theorem relators_literal : relators = [pairWord 0 1 11, pairWord 0 2 2, pairWord 1 2 11] ++ (List.range 10).map (fun k => tripleWord (k + 1)) := by decide',
 'structure VerifiedRow where','  name : Fin 1024','  evidence : ∀ s : Fin 3, ∃ v, D name [s] v',
 'def proofRows : Array VerifiedRow := #[']
for u in range(N):
 vals=[f'⟨{table[u][k]}, edge{known[u,k]}⟩' for k in range(d)]
 rows.append(f'  ⟨{u}, Fin.cases {vals[0]} (Fin.cases {vals[1]} (Fin.cases {vals[2]} (fun i => Fin.elim0 i)))⟩'+(',' if u<N-1 else ''))
rows += [']','private theorem proofRows_size : proofRows.size = 1024 := by decide',
 "def proofRow (u : Fin 1024) : VerifiedRow := proofRows[u.val]'(by simpa only [proofRows_size] using u.isLt)",
 'theorem proofRow_name : ∀ u : Fin 1024, (proofRow u).name = u := by decide',
 'theorem complete : Complete (listSet relators) (listSet ([0, 1] : List (Fin 3))) (0 : Fin 1024) representatives := by',
 '  intro u s','  have h := (proofRow u).evidence s','  rw [proofRow_name] at h','  exact h',
 'theorem index_bound : (facet (listSet relators) (listSet ([0, 1] : List (Fin 3)))).index ≤ 1024 := by',
 '  have h := universal_index_bound (listSet relators) (listSet ([0, 1] : List (Fin 3))) (0 : Fin 1024) representatives (by rfl) complete',
 '  simpa using h.2',
 '#print axioms relators_literal','#print axioms complete','#print axioms index_bound',
 'end HumanCompression.CosetUpperCertificate.RankThree','']
(OUT/'LabelElevenRankThree.lean').write_text('\n'.join(rows))
(OUT/'rank3_trace.json').write_text(json.dumps(dict(source_sha256=meta['raw_sha256'],nodes=N,generators=d,relators=rels,representatives=[reps[u] for u in range(N)],steps=steps),separators=(',',':'))+'\n')
print(json.dumps(dict(nodes=N,edges=len(steps),source_bytes=(OUT/'LabelElevenRankThree.lean').stat().st_size)))
