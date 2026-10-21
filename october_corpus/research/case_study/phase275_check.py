#!/usr/bin/env python3
"""Replay the Hermitian audit with exact archived proof bytes and no primary PDFs."""
import argparse, hashlib, importlib.util, json
from pathlib import Path
import subprocess, sys, time
ROOT=Path(__file__).resolve().parent
PIN='825b81d2e6a697ac5ccc485026e7feafe341dbcf6b7379bdef142f80c01f3f9c'
ALIASES={'hermitian_unital_proof.md':'phase275_hermitian_unital_proof.md'}
def need(b,s):
    if not b:raise RuntimeError('PHASE275_REJECT '+s)
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for k in ['out','gap','lean','packages']:ap.add_argument('--'+k,type=Path,required=True)
    a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh raw output')
    f=ROOT/'phase210_review_manifest.json';need(hashlib.sha256(f.read_bytes()).hexdigest()==PIN,'frozen review manifest')
    m=json.loads(f.read_text());checked=0;omitted=[]
    for r in m['exports']+m['retained_inputs']:
        rel=Path(r['path']);need(not rel.is_absolute() and '..' not in rel.parts,'relative path')
        if rel.parts[0]=='sources' or rel.suffix=='.olean':omitted.append(str(rel));continue
        f=ROOT/ALIASES.get(str(rel),str(rel));need(f.stat().st_size==r['bytes'] and hashlib.sha256(f.read_bytes()).hexdigest()==r['sha256'],'frozen '+str(rel));checked+=1
    version=subprocess.check_output([a.lean,'--version'],text=True).strip();need('version 4.32.2,' in version,'Lean version')
    spec=importlib.util.spec_from_file_location('frozen_phase210',ROOT/'phase210_check.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    # Only source-evidence paths change. All mathematical programs, target
    # statements, mutations and execution checks are the frozen implementation.
    mod.RETAINED={ALIASES.get(k,k):v for k,v in mod.RETAINED.items() if not k.startswith('sources/')}
    sys.argv=[str(ROOT/'phase210_check.py'),'--output-dir',str(a.out),'--gap',str(a.gap),'--lean',str(a.lean),'--packages',str(a.packages)]
    start=time.monotonic();mod.main()
    r=json.loads((a.out/'report.json').read_text());need(r['new_formal_declarations']==13 and r['explicit_transport_pairs']==18612,'complete stated replay')
    report=dict(status='PASS',seconds=round(time.monotonic()-start,3),frozen_public_bindings_checked=checked,omitted_primary_or_build_bindings=omitted,archived_proof_aliases=ALIASES,lean_version=version,new_formal_declarations=13,retained_formal_declarations=1,explicit_transport_pairs=18612,root_semantic_review='ACCEPTED_IN_SEPARATE_PHASE275_REVIEW',scope='Complete written Hermitian-unital question proof; thirteen actual norm-shell Lean declarations, not whole geometric formalization.')
    (a.out/'public_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
