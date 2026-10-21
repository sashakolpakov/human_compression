#!/usr/bin/env python3
"""Replay the reviewed primitive-square proof without private primary files."""
import argparse, hashlib, json
from pathlib import Path
import subprocess, sys
ROOT=Path(__file__).resolve().parent
PINS={'phase266_manifest.json': '7c92dee573d004c7d91783fd135f94819eab66e49d8834987089acb06039bbb5', 'phase267_manifest.json': '02579a303d75dd13e01454db64f713fe89830aabd11191a5d06c6170cd1e4895'}
def need(b,s):
    if not b: raise RuntimeError('PHASE269_REJECT '+s)
def main():
    p=argparse.ArgumentParser(description=__doc__)
    for k in ['out','gap','lean','packages']:p.add_argument('--'+k,type=Path,required=True)
    a=p.parse_args();checked=0
    for name,pin in PINS.items():
        need(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==pin,'manifest '+name)
        m=json.loads((ROOT/name).read_text())
        for r in m['exports']+m['retained_bindings']:
            rel=Path(r['path']);need(not rel.is_absolute() and '..' not in rel.parts,'relative path')
            if rel.parts[0]=='sources':continue
            f=ROOT/rel;need(f.stat().st_size==r['bytes'] and hashlib.sha256(f.read_bytes()).hexdigest()==r['sha256'],'frozen '+str(rel));checked+=1
    q=subprocess.run([sys.executable,'-B','-O',str(ROOT/'phase267_check.py'),'--out',str(a.out),'--gap',str(a.gap),'--lean',str(a.lean),'--packages',str(a.packages)])
    need(q.returncode==0,'review replay')
    print('PHASE269_PASS',checked,'frozen public bindings; primary full texts not required')
if __name__=='__main__':main()
