#!/usr/bin/env python3
"""Exact terminal-derived certificate; no complement search or fp enumeration."""
from pathlib import Path
import argparse,subprocess
from accepted_image import group_code

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--gap',default='/opt/homebrew/bin/gap');a=p.parse_args();a.out.mkdir(exist_ok=False,parents=True)
 tail='''D:=DerivedSeriesOfGroup(G);;P:=Last(D);;Assert(0,List(D,Size)=[13271040,3317760,368640,122880,1920,120]);;Assert(0,DerivedSubgroup(P)=P);;ee:=Elements(P);;ii:=Filtered(ee,x->Order(x)=2);;Assert(0,Length(ii)=1);;Print("AMBIENT_ORDER ",Size(G)," DERIVED_ORDERS ",List(D,Size),"\\n");;Print("PERFECT_RESIDUAL_GENERATORS ",GeneratorsOfGroup(P),"\\n");;Print("UNIQUE_INVOLUTION ",ii[1],"\\n");;Print("ELEMENT_ORDER_HISTOGRAM ",Collected(List(ee,Order)),"\\n");;Print("PASS_NO_A5_SUBGROUP\\n");;QUIT;\n'''
 q=a.out/'input.g';q.write_text(group_code('T4.8')+tail)
 with (a.out/'stdout').open('wb') as o,(a.out/'stderr').open('wb') as e:r=subprocess.run([a.gap,'-q','-T',str(q)],stdout=o,stderr=e,timeout=45)
 if r.returncode or 'PASS_NO_A5_SUBGROUP' not in (a.out/'stdout').read_text() or (a.out/'stderr').read_text().strip():raise ValueError('obstruction certificate failed')
 print('PASS_NO_A5_SUBGROUP')
if __name__=='__main__':main()
