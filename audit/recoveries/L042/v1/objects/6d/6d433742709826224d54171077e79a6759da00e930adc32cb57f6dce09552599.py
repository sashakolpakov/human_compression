from pathlib import Path
import importlib.util,json,sys
S=Path(__file__).resolve().parents[2]
p=S/'corpus106_L042_principal_v1'
spec=importlib.util.spec_from_file_location('literal_diagrams',p/'diagrams.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def need(c,s):
 if not c:raise ValueError(s)
checked=0;entries=0
for k,name,j in m.FAMILIES:
 for n in range(2*k+3,2*k+19):
  t,edges=m.graph(k,name,n);nt,newedges=m.graph(k,name,n+1)
  cut=[(u,v)for u,v,l in edges if l==j];need(len(cut)==1,'one cut edge');a,b=cut[0];need(b==a+1,'path position')
  q={v:v+(v>=b) for v in range(n)};q[n]=b
  generated=set()
  for u,v,l in edges:
   if l==j:generated|={(q[u],b,j),(b,q[v],j+1)}
   else:generated.add((q[u],q[v],l+(l>j)))
  need(generated==set(newedges),'explicit path-position map')
  # Omission components computed from edges, independently of pure_cut.
  adj=[set() for _ in range(n)]
  for u,v,l in edges:
   if l!=j:adj[u].add(v);adj[v].add(u)
  seen={a};todo=[a]
  for u in todo:
   for v in adj[u]-seen:seen.add(v);todo.append(v)
  right=set(range(n))-seen;need(b in right,'separated endpoints')
  todo=[b];other={b}
  for u in todo:
   for v in adj[u]-other:other.add(v);todo.append(v)
  need(other==right,'exactly two connected components')
  for u,v,l in edges:
   if l<j:need(u in seen and v in seen,'smaller left')
   if l>j:need(u in right and v in right,'larger right')
  checked+=1;entries+=len(generated)
# Check all retained base maps literally without author's conjugacy/BFS.
bases=json.loads((S/'topic_B_L019_balanced_pairs_v1/arrays_report.json').read_text())['boundary_literal_classes']
rows=json.loads((p/'diagram_report01.json').read_text())['families'];coverage={k:set()for k in range(1,5)}
for r in rows:
 k=r['k'];t,_=m.graph(k,r['family'],r['base_n']);b=r['base_match'];target=bases[str(k)][b['index']]['marks'];target=target[::-1]if b['reverse_target']else target;q=b['point_map']
 need(set(q)==set(range(len(t[0]))) and len(t)==len(target),'map dimensions')
 for i,g in enumerate(t):
  for v in range(len(g)):need(q[g[v]]==target[i][q[v]],'literal base image')
 coverage[k].add(b['index'])
need({k:len(v)for k,v in coverage.items()}=={1:1,2:1,3:7,4:9},'coverage')
r={'status':'PASS_INDEPENDENT_PATH_POSITION_GROWTH','finite_growth_controls':checked,'literal_edge_comparisons':entries,'literal_base_maps':18,'basis_coverage':{k:len(v)for k,v in coverage.items()},'all_degree_proof':'Written table formulas; finite controls are diagnostics only','whole_original_credit':0}
Path(__file__).with_name('independent_growth.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
