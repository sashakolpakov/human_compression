#!/usr/bin/env python3
"""Exact remaining L050 rank/difference-space bridges; no weight enumeration.

The whole inherited constructor is retained in steiner_construction.py.  The
complete weight files and their separately accepted enumeration method remain
explicit dependencies, not reconstructed from consistency conditions here.
"""
import argparse,hashlib,json,math
from pathlib import Path
import numpy as np
from steiner_construction import steiner_blocks,graph105,srg_check,rank_mod,need


def rank(A,p):return rank_mod(np.asarray(A).tolist(),p)

def rref(A,p=3):
 a=np.asarray(A,dtype=np.int64).copy()%p;piv=[]
 for j in range(a.shape[1]):
  rs=np.flatnonzero(a[len(piv):,j])
  if not len(rs):continue
  i=len(piv);q=i+int(rs[0]);a[[i,q]]=a[[q,i]];a[i]=a[i]*pow(int(a[i,j]),-1,p)%p
  for q in range(len(a)):
   if q!=i and a[q,j]:a[q]=(a[q]-a[q,j]*a[i])%p
  piv.append(j)
  if len(piv)==len(a):break
 return a[:len(piv)],piv

def same(A,B,p=3):
 a,_=rref(A,p);b,_=rref(B,p)
 return np.array_equal(a,b)

def mac(counts,n,k):
 need(len(counts)==n+1 and counts[0]==1 and sum(counts)==3**k,'complete enumerator shape')
 out=[]
 for j in range(n+1):
  value=sum(c*sum((-1)**s*2**(j-s)*math.comb(i,s)*math.comb(n-i,j-s)
    for s in range(max(0,j-n+i),min(i,j)+1))for i,c in enumerate(counts)if c)
  need(value>=0 and value%3**k==0,'MacWilliams coefficient');out.append(value//3**k)
 need(sum(out)==3**(n-k),'dual total');return out

def inspect(en):
 blocks,_=steiner_blocks();graphs={105:np.array(graph105(),dtype=np.int64)};Hs={}
 for t,n in [(0,253),(1,176),(2,120)]:
  bs=[b for b in blocks if not b&((1<<t)-1)]
  H=np.array([[(b>>i)&1 for b in bs]for i in range(t,23)],dtype=np.int64)
  A=np.array([[int(x!=y and (x&y).bit_count()==3)for y in bs]for x in bs],dtype=np.int64)
  graphs[n]=A;Hs[n]=H
 params={105:(105,72,51,45),120:(120,77,52,44),176:(176,105,68,54),253:(253,140,87,65)}
 exceptional={105:{2:104,3:20},120:{3:21,7:119,11:99},176:{3:21,5:175,7:175,17:155},253:{2:252,3:23,5:230,7:252}}
 spectra={105:[(72,1),(9,20),(-3,84)],120:[(77,1),(11,20),(-3,99)],176:[(105,1),(17,21),(-3,154)],253:[(140,1),(25,22),(-3,230)]}
 report={}
 for n,A in graphs.items():
  srg_check(A.tolist(),params[n]);I=np.eye(n,dtype=np.int64);J=np.ones((n,n),dtype=np.int64)
  v,k,l,m=params[n];r=spectra[n][1][0];s=spectra[n][2][0]
  need(np.array_equal(A@A,(l-m)*A+(k-m)*I+m*J),'integer SRG identity')
  need(r+s==l-m and r*s==m-k,'spectral quadratic')
  need(sum(d for x,d in spectra[n])==n and sum(x*d for x,d in spectra[n])==0,'multiplicities')
  detprimes=set()
  for eigen,mul in spectra[n]:
   q=abs(eigen);p=2
   while p*p<=q:
    if q%p==0:
     detprimes.add(p)
     while q%p==0:q//=p
    p+=1
   if q>1:detprimes.add(q)
  need(detprimes==set(exceptional[n]),'complete exceptional primes')
  actual={p:rank(A,p)for p in exceptional[n]};need(actual==exceptional[n],'all exceptional ranks')
  basis,_=rref(A);raw=(str(n)+' '+str(len(basis))+'\n'+''.join(''.join(map(str,row))+'\n'for row in basis)).encode()
  f=en/'bases'/f'{n}_adjacency.txt'
  need(f.read_bytes()==raw,'literal accepted adjacency basis')
  report[n]={'parameters':params[n],'spectrum':spectra[n],'exceptional_prime_ranks':actual,'every_other_prime_rank':n,'basis_sha256':hashlib.sha256(raw).hexdigest()}
 # The source's difference code in Proposition2.
 H=Hs[120]%3;A=graphs[120]%3;I=np.eye(120,dtype=np.int64);J=np.ones((120,120),dtype=np.int64)
 E=(np.eye(21,dtype=np.int64)[:20]-np.eye(21,dtype=np.int64)[20])%3
 S,piv=rref(A[1:]-A[0]);T=E@H%3;ones=np.ones((1,120),dtype=np.int64)
 need(np.array_equal(H@H.T%3,np.eye(21,dtype=np.int64)),'120 Gram identity')
 need(same(S,T) and len(S)==20,'difference code is incidence augmentation')
 need(rank(S@S.T%3,3)==19 and rank(np.concatenate([S,ones]),3)==20,'difference hull constant line')
 need(np.all(S@(A+I)%3==0) and rank(A+I,3)==100,'reflexive code is exact difference dual')
 B=(J-I-A)%3
 need(rank(B,3)==99 and rank(np.concatenate([B,ones]),3)==100 and same(A+I,np.concatenate([B,ones])),'difference dual constant plus orthogonal complement')
 # J-A is the symmetric projection H^T H onto this incidence image.
 need(np.all((J-A)%3==(H.T@H)%3),'120 orthogonal projection')
 raw=('120 20\n'+''.join(''.join(map(str,row))+'\n'for row in S)).encode()
 need(raw==(en/'bases/120_differences.txt').read_bytes(),'literal accepted difference basis')
 wt={}
 for name,k,d,count,dualcount in [('120_adjacency',21,30,112,33600),('120_differences',20,30,112,43680)]:
  obj=json.loads((en/(name+'.json')).read_text());v=obj['weight_counts'];dual=mac(v,120,k)
  need(obj['length']==120 and obj['basis_rows']==k and obj['coefficient_vectors']==3**k,'bound full enumeration dimensions')
  need(next(i for i in range(1,121)if v[i])==d and v[d]==count,'code minimum')
  need(not any(dual[1:6]) and dual[6]==dualcount,'dual minimum')
  wt[name]={'dimension':k,'distance':d,'minimum_words':count,'dual_distance':6,'dual_minimum_words':dualcount}
 # LCD alone is insufficient for complement duality: C4 over F3.
 A4=np.array([[int((i-j)%4 in (1,3))for j in range(4)]for i in range(4)],dtype=np.int64)
 B4=np.ones((4,4),dtype=np.int64)-np.eye(4,dtype=np.int64)-A4
 need(rank(A4,3)==rank(A4@A4,3)==2 and rank(B4,3)==4,'LCD converse counterexample')
 return {'status':'PASS','ranks':report,'difference120':{'dimension':20,'hull_dimension':1,'constant_in_hull':True,'dual_equals_reflexive_graph_code':True,'dual_equals_graph_dual_plus_constant':True,'basis_sha256':hashlib.sha256(raw).hexdigest()},'weights120':wt,'lcd_not_complement_dual':{'graph':'C4','prime':3,'code_rank':2,'code_square_rank':2,'complement_rank':4},'no_full_enumeration_repeated':True}

def main():
 p=argparse.ArgumentParser();p.add_argument('--enumerations',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 result=inspect(a.enumerations);(a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
