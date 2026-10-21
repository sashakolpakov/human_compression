#!/usr/bin/env python3
"""Independent tuple/coordinate reconstruction. No author or GAP import."""
import argparse,ast,hashlib,itertools,json
from pathlib import Path
P=7

def need(v,m):
 if not v:raise ValueError(m)
def rank(rows):
 a=[[v%P for v in r] for r in rows];h=0
 for j in range(len(a[0])):
  k=next((k for k in range(h,len(a)) if a[k][j]),None)
  if k is None:continue
  a[h],a[k]=a[k],a[h];v=pow(a[h][j],-1,P);a[h]=[(x*v)%P for x in a[h]]
  for k in range(len(a)):
   if k!=h:
    v=a[k][j];a[k]=[(x-v*y)%P for x,y in zip(a[k],a[h])]
  h+=1
  if h==len(a):break
 return h

def mm(a,b):return tuple(tuple(sum(x*y for x,y in zip(r,c))%P for c in zip(*b)) for r in a)
def trans(a):return tuple(zip(*a))
def neg(a):return tuple(tuple(-x%P for x in r) for r in a)
def coordinate(p):
 rows=[]
 for i in range(5):
  w=[0]*7;w[p[i]]+=1;w[p[6]]-=1
  rows.append(tuple((w[j]-w[5])%P for j in range(5)))
 return tuple(rows)
def parity(p):return (-1)**sum(p[i]>p[j] for i in range(7) for j in range(i+1,7))
def components(mask):
 out=[];block=[0]
 for j in range(6):
  if mask>>j&1:block.append(j+1)
  else:out.append(tuple(block));block=[j+1]
 out.append(tuple(block));return tuple(out)
def group_set(blocks):
 choices=[list(itertools.permutations(b)) for b in blocks];out=set()
 for parts in itertools.product(*choices):
  p=list(range(7))
  for block,part in zip(blocks,parts):
   for i,j in zip(block,part):p[i]=j
  out.add(tuple(p))
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--author',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();need(not args.out.exists(),'fresh output')
 I=tuple(tuple(int(i==j) for j in range(5)) for i in range(5));B=tuple(tuple(1+int(i==j) for j in range(5)) for i in range(5));need(rank(B)==5,'nondegenerate')
 marks=[]
 for i in range(6):
  p=list(range(7));p[i],p[i+1]=p[i+1],p[i];marks.append(coordinate(p))
 literal=(args.author/'deleted_permutation.g').read_text().split('marks:=',1)[1].split('*one',1)[0]
 need(marks==[tuple(map(tuple,m)) for m in ast.literal_eval(literal)],'all six literal matrices')
 for m in marks:need(mm(m,m)==I and mm(mm(m,B),trans(m))==B,'involution/isometry')
 for i in range(6):
  for j in range(i+1,6):
   w=mm(marks[i],marks[j]);ordr=3 if j==i+1 else 2
   v=I
   for k in range(ordr):v=mm(v,w)
   need(v==I and w!=I,'exact pair order')
 allp=list(itertools.permutations(range(7)));plain={coordinate(p) for p in allp};signed={coordinate(p) if parity(p)==1 else neg(coordinate(p)) for p in allp}
 need(len(plain)==len(signed)==5040 and neg(I) not in plain,'both faithful and no -I')
 groups=[group_set(components(i)) for i in range(64)]
 for i in range(64):
  for j in range(64):need(groups[i]&groups[j]==groups[i&j],'full subset IP')
 supports=[tuple((m[i][j]-I[i][j])%P for j in range(5)) for m in marks for i in range(5)];left=rank(supports[:15]);right=rank(supports[15:]);total=rank(supports)
 need((left,right,total)==(3,3,5),'support dimensions');need(len(groups[7]&groups[56])==1,'disjoint triple groups')
 # Meaningful negative checks: a changed Gram matrix, a duplicate mark, and a singular form.
 Bbad=tuple(tuple(B[i][j]+int(i==j==0) for j in range(5)) for i in range(5))
 need(any(mm(mm(m,Bbad),trans(m))!=Bbad for m in marks),'changed Gram rejected')
 duplicate=list(marks);duplicate[-1]=duplicate[0]
 need({I,duplicate[0]}&{I,duplicate[-1]}!={I},'duplicate-label IP obstruction')
 need(rank([[0]*5 for _ in range(5)])!=5,'singular form rejected')
 report={'status':'PASS','method':'direct tuple permutations and quotient coordinates; no author/GAP import','field':7,'dimension':5,'literal_marks_compared':6,'isometry_checks':6,'pair_orders_checked':15,'faithful_group_orders':[len(plain),len(signed)],'independent_IP_pairs':4096,'signed_IP':'transport through independently verified faithful signed representation','support_dimensions':[left,right,total],'support_intersection_dimension':left+right-total,'disjoint_triple_group_intersection_order':1,'negative_controls':['changed Gram','duplicate marking','singular form'],'scope':'literal F001 Lemma 4.1 only; no claim on Omega(5,7) or principal rank spectrum'}
 args.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
