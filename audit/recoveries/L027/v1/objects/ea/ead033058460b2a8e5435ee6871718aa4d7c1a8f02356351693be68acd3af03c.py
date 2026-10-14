import sys
if sys.flags.optimize:raise SystemExit('normal Python required')
from pathlib import Path
import itertools,json
O=Path(__file__).parent
# GF25=F5[w]/(w^2-2), implemented without author or CAS imports.
def add(x,y):return ((x%5+y%5)%5)+5*((x//5+y//5)%5)
def neg(x):return add(0,(-x%5)+5*(-(x//5)%5))
def mul(x,y):return ((x%5*(y%5)+2*(x//5)*(y//5))%5)+5*((x%5*(y//5)+(x//5)*(y%5))%5)
def inverse(x):return next(y for y in range(1,25)if mul(x,y)==1)
def vadd(v,w):return tuple(add(x,y)for x,y in zip(v,w))
def scale(a,v):return tuple(mul(a,x)for x in v)
module_rows=[]
for d in range(25):
 if d in [0,1,4]:continue
 c=6;e=7;f=mul(add(1,neg(mul(d,d))),inverse(e));v=(mul(add(1,neg(d)),c),mul(e,c));V={(0,0)};todo=[v]
 while todo:
  z=todo.pop()
  if z in V:continue
  old=list(V);new={vadd(x,scale(t,z))for x in old for t in range(5)};V|=new
  for x,y in new:
   todo.append((add(mul(d,x),neg(mul(f,y))),neg(add(mul(e,x),mul(d,y)))))
   todo.append((x,neg(y)))
 assert (c,0)in V
 module_rows.append([d,len(V)])
heis=[]
for p in [3,5,7]:
 def mm(A,B):return tuple(sum(A[3*i+k]*B[3*k+j]for k in range(3))%p for i in range(3)for j in range(3))
 def form(x,y,z,i,j):
  D=[(-1)**j,(-1)**(i+j),(-1)**i];return tuple(v*D[k%3]%p for k,v in enumerate([1,0,0,x,1,0,z,y,1]))
 gs=[form(0,0,0,1,0),form(1,0,0,1,0),form(0,-1,0,0,1),form(0,0,0,0,1)]
 def closure(sub):
  V={form(0,0,0,0,0)};queue=list(V)
  while queue:
   a=queue.pop()
   for b in sub:
    c=mm(a,b)
    if c not in V:V.add(c);queue.append(c)
  return V
 G=closure(gs);A=closure(gs[:3]);B=closure(gs[1:]);D=closure(gs[1:3]);F={form(x,y,z,i,j)for x,y,z,i,j in itertools.product(range(p),range(p),range(p),range(2),range(2))};FA={form(x,-j,z,i,j)for x,z,i,j in itertools.product(range(p),range(p),range(2),range(2))};FB={form(i,y,z,i,j)for y,z,i,j in itertools.product(range(p),range(p),range(2),range(2))};assert G==F and A==FA and B==FB and A&B==D and len(D)==4*p
 heis.append([p,len(G),len(A),len(B),len(D)])
report=dict(status='PASS_NO_AUTHOR_IMPORT_ODD_CONTROLS',GF25_module_cases=module_rows,literal_heisenberg_groups=heis,scope='Supplementary exact field/module/intersection controls; uniform proof reviewed separately');(O/'independent.json').write_text(json.dumps(report,indent=2)+'\n');print(len(module_rows),heis)
