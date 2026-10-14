"""Independent literal cyclic-action and primary-input checks; no author imports."""
import sys
if sys.flags.optimize:raise SystemExit('Ordinary Python required')
from pathlib import Path
from html.parser import HTMLParser
from itertools import combinations
from math import factorial
import json,hashlib,re
P=Path('/Users/sasha/medusa/research/leemans/corpus106_L036_orbit_bound_v1');O=Path(__file__).resolve().parent

def need(b,msg):
 if not b:raise ValueError(msg)
def parts(n,low=1):
 if not n:yield []
 for x in range(low,n+1):
  for tail in parts(n-x,x):yield [x]+tail
rows=[]
for n in range(1,11):
 for partition in parts(n):
  g=[];start=0
  for length in partition:
   g.extend(list(range(start+1,start+length))+[start]);start+=length
  power=list(range(n));powers=[]
  while not powers or power!=list(range(n)):
   powers.append(power);power=[g[x]for x in power]
  pairs=set(combinations(range(n),2));left=set(pairs);count=0;orb=[]
  while left:
   p=min(left);orbit={p};q=tuple(sorted(g[i]for i in p))
   while q!=p:orbit.add(q);q=tuple(sorted(g[i]for i in q))
   need(orbit<=left,'orbit partition');left-=orbit;count+=1;orb.append(len(orbit))
  fixed_counts=[];formula=[]
  for h in powers:
   actual=sum(tuple(sorted(h[i]for i in p))==p for p in pairs)
   f=sum(h[i]==i for i in range(n));f2=sum(h[h[i]]==i for i in range(n));twice=f*f-2*f+f2
   need(2*actual==twice,'individual fixed pair formula');fixed_counts.append(actual);formula.append(twice)
  need(sum(fixed_counts)==len(powers)*count and sum(formula)==2*len(powers)*count,'orbit averaging')
  need(count*len(powers)>=len(pairs),'coarse orbit-size bound')
  rows.append(dict(partition=partition,cyclic_group_order=len(powers),pair_orbits=sorted(orb),elements_checked=len(powers)))
class Plain(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.data=[]
 def handle_data(self,x):self.data.append(x)
raw=(P/'atlas_ru.html').read_text();p=Plain();p.feed(raw);s=' '.join(' '.join(p.data).split())
need('Order = 145926144000'in s and 'Out = 1.'in s,'primary order/out')
section=raw.split('<A NAME="maxs">',1)[1].split('Some [shorter]',1)[0];p=Plain();p.feed(section);maxs=' '.join(' '.join(p.data).split());need('5:4 × A 5 , with generators'in maxs,'actual Ru maximal-section entry')
order=2**14*3**3*5**3*7*13*29;m=5*4*(factorial(5)//2);need(order==145926144000 and m==1200 and order%m==0,'independent group arithmetic')
n=order//m;X=n*(n-1)//2;lower=(X+order-1)//order
need(lower==50669 and (lower-1)*order<X<=lower*order and 1511*order<X,'lower and contradiction')
result=dict(status='PASS_INDEPENDENT_L036_REVIEW_CONTROLS',cycle_types=len(rows),permutation_elements=sum(r['elements_checked']for r in rows),rows=rows,atlas_url='https://brauer.maths.qmul.ac.uk/Atlas/spor/Ru/',atlas_sha256=hashlib.sha256((P/'atlas_ru.html').read_bytes()).hexdigest(),group_order=order,maximal_order=m,conjugates=n,unordered_pairs=X,lower_bound=lower,source_row=1511,exact_total=None)
(O/'independent.json').write_text(json.dumps(result,indent=2)+'\n');print({k:v for k,v in result.items()if k!='rows'})
