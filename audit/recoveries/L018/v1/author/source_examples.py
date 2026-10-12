#!/usr/bin/env python3
"""Exact source illustrations and corrected perimeter conventions, no census."""
import itertools,json,argparse
from pathlib import Path

def require(c,m):
 if not c:raise ValueError(m)
def partial(w,h,a,p,perimeter=False):
 for x,y,wi,hi in p:require(x>=0 and y>=0 and x+wi<=w and y+hi<=h and wi*hi==a,'invalid rectangle')
 require(len({tuple(sorted(z[2:]))for z in p})==len(p),'congruent pieces')
 for i,(x,y,wi,hi)in enumerate(p):
  for xx,yy,ww,hh in p[:i]:require(x+wi<=xx or xx+ww<=x or y+hi<=yy or yy+hh<=y,'overlap')
 if perimeter:
  sides=[[],[],[],[]]
  for x,y,wi,hi in p:
   if y==0:sides[0].append((x,x+wi))
   if x+wi==w:sides[1].append((y,y+hi))
   if y+hi==h:sides[2].append((x,x+wi))
   if x==0:sides[3].append((y,y+hi))
  for rows,L in zip(sides,[w,h,w,h]):
   pos=0
   for lo,hi in sorted(rows):require(lo==pos,'side gap or overlap');pos=hi
   require(pos==L,'side incomplete')
 return True

def reconstruct():
 p84=[(72,0,12,84),(0,0,16,63),(16,0,56,18),(0,63,48,21),(48,42,24,42)]
 p360=[(0,0,240,45),(240,0,120,90),(0,180,60,180),(60,252,100,108),(160,306,200,54),(0,45,80,135),(310,90,50,216)]
 partial(84,84,1008,p84,True);partial(360,360,10800,p360,True)
 shapes=[(36,300),(40,270),(48,225),(72,150),(75,144)]
 sums={0}
 for a,b in shapes:sums|={x+y for x in tuple(sums)for y in (a,b)}
 require(216 in sums and 72+144==216,'216 correction witness');require(160 in sums and 40+48+72==160,'160 claim false')
 require(360-min(240,80,60)-min(120,50,200)==250,'width bound')
 require(360-min(45,90)-min(180,108,54)==261,'height bound')
 require(not any(w<=250 and h<=261 for w,h in [(36,300),(300,36)]),'hole example')
 # A 270-high piece starting at y=45 reaches315, above every top-boundary
 # bottom in this example (at most306), so it necessarily intersects it.
 require(45+270>max(180,252,306),'overlap example')
 a=120;unordered=[(d,a//d)for d in range(1,11)if a%d==0 and d<=a//d and d<=14 and a//d<=60]
 orientations=[(w,h)for a,b in unordered for w,h in sorted({(a,b),(b,a)})if w<=60 and h<=14]
 require(len(unordered)==7 and len(orientations)==8,'rectangle reversal counterexample')
 defects=[]
 for n in range(3,1001):
  ws=((n-1)//2,(n+1)//2)if n%2 else(n//2-1,n//2+1)
  require(ws[0]>0 and sum(ws)==n and ws[0]!=ws[1],'defect construction')
  defects.append((n,n*(ws[1]-ws[0])))
 return {'perimeter84':p84,'perimeter360':p360,'unused360':shapes,'printed_gap216_impossibility_false':True,'gap216_witness':[72,144],'gap160_possible_but_insufficient':True,'hole_bound':[250,261],'rectangle_orientation_counts':[7,8],'defect_range_checked':[3,1000]}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();d=reconstruct();a.out.write_text(json.dumps(d,indent=2)+'\n');print('PASS source examples and qualifications')
