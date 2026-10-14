import ast,itertools,json,re,sys
from pathlib import Path
if sys.flags.optimize: raise RuntimeError('optimization is unsupported')
w=Path(__file__).resolve().parent
s=(w/'stdout.log').read_text(); results=[]
for name in ['4.4','4.5']:
 part=s.split('EXAMPLE '+name+'\n')[1].split('EXAMPLE ')[0]
 counts=ast.literal_eval(re.search(r'COS_COUNTS (\[[^\n]*\])',part)[1])
 edges=ast.literal_eval(part.split('EDGES ')[1].strip())
 vertices=[(i+1,j+1) for i,n in enumerate(counts)for j in range(n)]
 adj={v:set()for v in vertices}
 for i,h,j,k in edges:adj[(i,h)].add((j,k));adj[(j,k)].add((i,h))
 flags=[()]
 for v in vertices:flags += [f+(v,)for f in tuple(flags) if all(x[0]<v[0] and v in adj[x]for x in f)]
 chambers=[f for f in flags if len(f)==len(counts)]
 max_short=[]; panels={}; disconnected=[]
 for f in flags:
  available=[v for v in vertices if all(v in adj[x]for x in f)]
  if len(f)<len(counts) and not available:max_short.append(f)
  if len(f)==len(counts)-1:panels[len(available)]=panels.get(len(available),0)+1
  if len(f)<=len(counts)-2:
   left=set(available); comps=[]
   while left:
    stack=[left.pop()];comp=[]
    while stack:
     v=stack.pop();comp.append(v);new=left&adj[v];left-=new;stack.extend(new)
    comps.append(sorted(comp))
   if len(comps)>1:disconnected.append({'flag':f,'components':comps})
 result={'example':name,'type_counts':counts,'edge_count':len(edges),'flag_counts':{str(i):sum(len(f)==i for f in flags)for i in range(len(counts)+1)},'chambers':len(chambers),'short_maximal_flags':max_short,'panel_size_histogram':panels,'disconnected_residue_count':len(disconnected),'first_disconnected_residue':disconnected[:1]}
 results.append(result)
 print(json.dumps(result))
(w/'incidence_result.json').write_text(json.dumps(results,indent=2)+'\n')
