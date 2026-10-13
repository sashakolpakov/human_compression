import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
from pathlib import Path
import argparse,json
from permutation_library import parse_marks,closure,need

def orbit(gs,a):
 out={a};todo=[a]
 while todo:
  u=todo.pop()
  for g in gs:
   v=g[u]
   if v not in out:out.add(v);todo.append(v)
 return out
def orbits(gs,n):
 left=set(range(n));out=[]
 while left:
  O=orbit(gs,min(left));out.append(sorted(O));left-=O
 return out
def even(p):
 # Every cycle length, not just the involution specialization.
 seen=set();cycles=0
 for u in range(len(p)):
  if u in seen:continue
  cycles+=1
  while u not in seen:seen.add(u);u=p[u]
 return (len(p)-cycles)%2==0
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,default=Path(__file__).with_name('eight_tuples.json'));ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 rows=json.loads(a.input.read_text());need(len(rows)==9,'all nine tuples');report=[]
 for i,row in enumerate(rows):
  t=parse_marks({'permutations':row},8,5);need(t[0][0]!=0 and all(g[0]==0 for g in t[1:]),'anchor1')
  need(len(closure(t))==40320,'natural S8')
  O=[orbits(t[:j]+t[j+1:],8)for j in range(5)];fractured=all(len(x)>1 for x in O)
  need(fractured==(i<8),'exact fracture list')
  entry={'index':i,'fractured':fractured,'omission_orbits':O,'first_pure':sum(t[0][x]!=x for x in range(8))==2}
  if i<6:need(entry['first_pure'],'six pure first marks')
  if i in [6,7]:
   j=3 if i==6 else 4;P=closure(t[:j-1]);Q=closure(t[:j]);X=orbit(t[:j-1],0)
   K={g for g in Q if all(g[x]==x for x in set(range(8))-X)};M=K&P;Kplus={g for g in K if even(g)}
   need((len(K),len(M),len(Kplus))==((120,10,60)if i==6 else(720,60,360)),'exact even obstruction')
   need(Kplus & P == M and len(Kplus)>len(M),'even kernel not contained')
   entry.update(prefix_length=j,root_orbit=sorted(x+1 for x in X),kernel=len(K),previous_kernel=len(M),even_kernel=len(Kplus))
  report.append(entry)
 out={'status':'PASS_LITERAL_CRITICAL_SYMMETRIC_EIGHT','rows':report,'whole_original_credit':0}
 a.out.write_text(json.dumps(out,indent=2)+'\n');print(out['status'])
if __name__=='__main__':main()
