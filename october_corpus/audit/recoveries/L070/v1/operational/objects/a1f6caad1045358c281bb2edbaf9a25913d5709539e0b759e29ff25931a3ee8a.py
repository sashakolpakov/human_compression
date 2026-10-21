"""Literal two source-mentioned vertex figures; no group or atlas census."""
import sys
if sys.flags.optimize:
 raise RuntimeError('ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import json,hashlib,argparse
C=Path(__file__).resolve().parent.parent;P=C/'small_entries_v1'
def need(x,s):
 if not x:raise ValueError(s)
def pin(p):b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def traversal(edges,root):
 order=[root];labels={root:0};code=[]
 for v in order:
  for y in edges[v]:
   if y not in labels:labels[y]=len(order);order.append(y)
   code.append(labels[y])
 need(len(order)==len(edges),'connected');return tuple(code),order
def check_map(edges,target,mapping):
 need(set(mapping)==set(range(len(edges))) and set(mapping.values())==set(range(len(target))) and len(edges)==len(target),'complete bijection')
 need(all(mapping[edges[x][c]]==target[mapping[x]][c]for x in range(len(edges))for c in range(3)),'every literal colour edge')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');data=json.loads((P/'data01.json').read_text());classes=json.loads((P/'expected_classes.json').read_text());results=[];deps={str(P/'data01.json'):pin(P/'data01.json'),str(P/'expected_classes.json'):pin(P/'expected_classes.json')}
 for typ in[[3,6,18],[6,6,9]]:
  ids=[i for i,r in enumerate(data)if r['rank']==4 and r['type']==typ];need(len(ids)==1,'one Table1 marking');i=ids[0];path=P/'groups01'/('entry_%02d.json'%i);deps[str(path)]=pin(path);orig=[[x-1 for x in row]for row in json.loads(path.read_text())['edges']]
  component=[0];seen={0}
  for v in component:
   for c in[1,2,3]:
    y=orig[v][c]
    if y not in seen:seen.add(y);component.append(y)
  ix={x:j for j,x in enumerate(component)};edges=[[ix[orig[x][c]]for c in[1,2,3]]for x in component]
  code,order=min((traversal(edges,r)for r in range(len(edges))),key=lambda x:x[0]);matches=[z for z in classes if data[z['entry']]['rank']==3 and tuple(z['canonical_code'])==code];need(len(matches)==1,'one actual acquired rank3 graph');target=matches[0]['entry'];q=P/'groups01'/('entry_%02d.json'%target);deps[str(q)]=pin(q);te=[[x-1 for x in row]for row in json.loads(q.read_text())['edges']];tc,to=min((traversal(te,r)for r in range(len(te))),key=lambda x:x[0]);need(tc==code,'same complete rooted graph');mapping=dict(zip(order,to));need(len(set(mapping.values()))==len(te)==len(edges),'bijection');need(all(mapping[edges[x][c]]==te[mapping[x]][c]for x in range(len(edges))for c in range(3)),'every literal colour edge')
  check_map(edges,te,mapping)
  bad=dict(mapping);bad[0]=bad[1]
  swapped=dict(mapping);swapped[0],swapped[1]=swapped[1],swapped[0]
  for damaged in [bad,swapped]:
   try:check_map(edges,te,damaged)
   except ValueError:pass
   else:raise ValueError('damaged vertex-figure map accepted')
  need(data[target]['type']==typ[1:],'exact source vertex-figure type')
  results.append(dict(rank4_entry=i,type=typ,source_rank3_entry=target,vertex_figure_type=typ[1:],flags=len(edges),parent_component_vertices=component,complete_isomorphism=[mapping[j]for j in range(len(edges))],edges_checked=3*len(edges),source_url=data[target]['url']))
 a.out.parent.mkdir(exist_ok=True);a.out.write_text(json.dumps(dict(status='PASS_TWO_SOURCE_VERTEX_FIGURE_JOINS',results=results,inputs=list(deps.values()),map_damage_controls=4,new_group_calls=0,new_censuses=0),indent=2)+'\n');print(json.dumps([dict(parent=x['rank4_entry'],target=x['source_rank3_entry'],flags=x['flags'],type=x['vertex_figure_type'])for x in results]))
if __name__=='__main__':main()
