#!/usr/bin/env python3
"""Small exact models of the period-containment hypothesis; not the all-group proof."""
import argparse,itertools,json

def need(x,m):
 if not x:raise RuntimeError(m)
def subgroup(gs):
 s={0}
 for g in gs:s|={x^g for x in tuple(s)}
 return frozenset(s)
def subgroups(n):return sorted({subgroup(x for x in range(1<<n) if mask>>x&1) for mask in range(1<<(1<<n))},key=lambda s:(len(s),tuple(sorted(s))))
def image(A,N):return frozenset(frozenset(a^n for n in N) for a in A)
def good(A,B,N):return image(A,N)&image(B,N)==image(A&B,N)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();S=subgroups(3);count=0
 for A,B,L,N in itertools.product(S,repeat=4):
  if not N<=L or A&L!={0} or B&L!={0} or not good(A,B,N):continue
  for M in S:
   if M<=N:need(good(A,B,M),'valid smaller period failed');count+=1
 A=subgroup([1]);B=subgroup([2]);M=subgroup([3]);whole=subgroup([1,2]);trivial=subgroup([])
 need(good(A,B,whole) and not good(A,B,M),'nonfaithful coarse quotient counterexample')
 need(good(A,B,trivial) and not good(A,B,M) and not M<=trivial,'missing period containment counterexample')
 report=dict(status='PASS',valid_finite_cases=count,positive_model='All subgroups of the elementary abelian group C2^3, all admissible A,B,L,N,M.',controls=[dict(omitted='faithfulness under the point quotient',group='C2^2',A=[0,1],B=[0,2],N=[0,1,2,3],M=[0,3],coarse_intersection=True,finer_intersection=False),dict(omitted='M contained in N',group='C2^2',A=[0,1],B=[0,2],L=[0],N=[0],M=[0,3],coarse_intersection=True,finer_intersection=False)],scope='Finite controls only; the quantified group theorem is the Lean proof.')
 from pathlib import Path
 p=Path(a.out);need(not p.exists(),'fresh output');p.write_text(json.dumps(report,indent=2)+'\n');print('AFFINE_PERIOD_CONTROLS_PASS',count)
if __name__=='__main__':main()
