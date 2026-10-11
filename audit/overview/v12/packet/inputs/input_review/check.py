#!/usr/bin/env python3
"""Replay the distinct input review without importing author counting code."""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
R=Path(__file__).resolve().parent
def need(ok,msg):
 if not ok: raise ValueError(msg)
def main():
 p=argparse.ArgumentParser();p.add_argument('--author',required=True,type=Path);p.add_argument('--public-root',required=True,type=Path);p.add_argument('--sources-root',required=True,type=Path);p.add_argument('--out',required=True,type=Path);a=p.parse_args()
 for b in json.loads((R/'manifest.json').read_text())['exports']:
  raw=(R/b['path']).read_bytes();need(len(raw)==b['bytes'] and hashlib.sha256(raw).hexdigest()==b['sha256'],'review export '+b['path'])
 subprocess.run([sys.executable,'-B','-O',str(R/'recount.py'),'--author',str(a.author),'--public-root',str(a.public_root),'--sources-root',str(a.sources_root),'--out',str(a.out)],check=True)
 need(json.loads((a.out/'recount.json').read_text())==json.loads((R/'recount.json').read_text()),'fresh independent recount equals frozen review')
 print('PASS: frozen independent review and all600 metric cells/120 hashes reproduced')
if __name__=='__main__':main()
