#!/usr/bin/env python3
"""Replay the reviewed point-cloning counterexample without private primary files."""
import argparse, hashlib, json
from pathlib import Path
import subprocess, sys
ROOT=Path(__file__).resolve().parent
PINS={'phase265_cloning_manifest.json': '99c2a317d3c9c6a2ba37265b61245f6e3c7a4256af901975c7f01d6623a8e976', 'phase268_manifest.json': 'eb952e4e625f9726f00fd7f82df0e996459b9436bdc861af34a61bafb7acd126'}
def need(b,s):
    if not b: raise RuntimeError('PHASE270_REJECT '+s)
def main():
    p=argparse.ArgumentParser(description=__doc__)
    for k in ['out','lean','packages']:p.add_argument('--'+k,type=Path,required=True)
    a=p.parse_args();checked=0
    for name,pin in PINS.items():
        need(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==pin,'manifest '+name)
        m=json.loads((ROOT/name).read_text())
        for r in m['exports']+m.get('retained_bindings',[]):
            rel=Path(r['path']);need(not rel.is_absolute() and '..' not in rel.parts,'relative path')
            if rel.parts[0]=='sources':continue
            f=ROOT/rel;need(f.stat().st_size==r['bytes'] and hashlib.sha256(f.read_bytes()).hexdigest()==r['sha256'],'frozen '+str(rel));checked+=1
    q=subprocess.run([sys.executable,'-B','-O',str(ROOT/'phase268_check.py'),'--out',str(a.out),'--lean',str(a.lean),'--packages',str(a.packages)])
    need(q.returncode==0,'review replay')
    print('PHASE270_PASS',checked,'frozen public bindings; primary full texts not required')
if __name__=='__main__':main()
