#!/usr/bin/env python3
"""Independent F2^3 model of the exact marked endpoint counterexample."""
from pathlib import Path
import argparse,hashlib,json
PIN='3f1c343fde1a9cbf9a89e9bbb8c4f1006cdc23e5ce40442750fdf50aeff266e7'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def span(gs,mask):
 points={0}
 for i,g in enumerate(gs):
  if (mask>>i)&1:points|={x^g for x in tuple(points)}
 return points
def model(gs):
 par=[span(gs,m)for m in range(8)]
 bad=[(i,j)for i in range(8)for j in range(8)if par[i]&par[j]!=par[i&j]]
 return par,bad
def main():
 p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'fresh output')
 need(hashlib.sha256((a.packet/'manifest.json').read_bytes()).hexdigest()==PIN,'exact author edition')
 for r in json.loads((a.packet/'manifest.json').read_text())['exports']:
  b=(a.packet/r['path']).read_bytes();need(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],'exact export')
 old,ob=model([1,2,3]);new,nb=model([5,2,3])
 need(len(old[7])==4 and len(new[7])==8 and 4 not in old[7],'outside central coordinate')
 need(len(ob)==12 and not nb,'all128 intersection checks')
 need(all(len(new[m])==2**m.bit_count()for m in range(8)),'all coordinate subspace dimensions')
 need(old[6]&new[3]=={0,2} and old[6]&old[3]=={0,1,2,3},'literal invalid source equality')
 q=dict(status='PASS_DISTINCT_ENDPOINT_MODEL',author_manifest_sha256=PIN,model='Bitwise XOR on F2^3, with a=1,b=2,tau=4; no author or GAP imports.',old_order=4,new_order=8,old_intersections=64,new_intersections=64,old_failures=12,new_failures=0,source_equality_left_order=2,source_equality_right_order=4,formal_proof=False,source_credit=0,question_credit=0)
 a.out.write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q))
if __name__=='__main__':main()
