"""Independent tiny permutation/coset/incidence/palette audit, no GAP imports."""
import argparse,copy,itertools,json
from pathlib import Path
if not __debug__:raise SystemExit('normal Python required')
def need(v,s):
 if not v:raise ValueError(s)
def mul(a,b):return tuple(b[x-1]for x in a)
def check(d,full=True):
 E=list(map(tuple,d['group_elements']));gens=list(map(tuple,d['group_generators']));one=tuple(range(1,len(E[0])+1));seen={one};todo=[one]
 while todo:
  a=todo.pop()
  for b in gens:
   x=mul(a,b)
   if x not in seen:seen.add(x);todo.append(x)
 need(set(E)==seen and len(set(E))==len(E),'literal group closure')
 n=d['n'];r=d['rank'];types=d['types'];parts=[{E[i-1]for i in p}for p in d['coset_positions']];H=[{E[i-1]for i in p}for p in d['parabolics']]
 need(len(parts)==n and set(types)==set(range(1,r+1)),'typed objects')
 for t in range(1,r+1):
  ps=[parts[i]for i in range(n)if types[i]==t];need(set().union(*ps)==seen and sum(map(len,ps))==len(seen),'complete typed partition')
  for part in ps:
   x=next(iter(part));need(part=={mul(h,x)for h in H[t-1]},'literal right coset')
 adj=[{b+1 for b in range(n)if types[a]!=types[b]and parts[a]&parts[b]}for a in range(n)]
 need(adj==list(map(set,d['adjacency'])),'literal intersection incidence')
 for g,act in zip(gens,d['group_action']):
  need(sorted(act)==list(range(1,n+1)),'action permutation')
  for a in range(n):need({mul(x,g)for x in parts[a]}==parts[act[a]-1]and types[a]==types[act[a]-1],'literal right action')
 if full:
  blocks={frozenset(i+1 for i in range(n)if types[i]==t)for t in range(1,r+1)};cor=typed=0
  for p in itertools.permutations(range(1,n+1)):
   if {frozenset(p[i-1]for i in b)for b in blocks}!=blocks:continue
   if any({p[b-1]for b in adj[a]}!=adj[p[a]-1]for a in range(n)):continue
   cor+=1;typed+=all(types[a]==types[p[a]-1]for a in range(n))
  need(cor==d['correlation_order']and typed==d['typed_order'],'complete literal palette oracle')
 return n

def main():
 a=argparse.ArgumentParser();a.add_argument('--input',type=Path,required=True);a.add_argument('--out',type=Path,required=True);z=a.parse_args();need(not z.out.exists(),'fresh output');z.out.mkdir();models=json.loads(z.input.read_text());sizes=[check(d)for d in models];damages=[]
 for j,d in enumerate(models):
  for k in range(4):
   bad=copy.deepcopy(d)
   if k==0:bad['adjacency'][0]=[]
   elif k==1:bad['coset_positions'][0].pop()
   elif k==2:bad['group_action'][0][0]=bad['group_action'][0][1]
   else:bad['correlation_order']+=1
   try:check(bad)
   except ValueError:damages.append([j,k])
   else:raise ValueError('damaged model accepted')
 report=dict(status='PASS_INDEPENDENT_TINY_COSET_PALETTE_ORACLE',models=len(models),object_sizes=sizes,damage_controls=damages,target_runs=0);(z.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
