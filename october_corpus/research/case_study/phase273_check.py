#!/usr/bin/env python3
"""Verify phase273/256 bindings and independently reconstruct the six raw surfaces.

--author-replay additionally recompiles all five Lean statements and replays the
frozen author's large-prime symbolic paths. Written topology is not machine proved.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent
AUTHOR_HASH='8d22baec4ddafcbb624300e7c65a23079982be724181b8282fafd512c70503ea'


def need(ok,message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bind(records):
    for name,digest in records.items():
        need(sha(ROOT/name)==digest,'binding mismatch: '+name)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True,type=Path)
    parser.add_argument('--author-replay',action='store_true')
    parser.add_argument('--verify-primary',action='store_true')
    parser.add_argument('--lean',default='/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean')
    parser.add_argument('--packages',default='/Users/sasha/bogachev/formal/.lake/packages')
    args=parser.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(),'fresh output directory required')
    out=args.out.resolve(); out.mkdir(parents=True)
    start=time.monotonic()
    review=json.loads((ROOT/'phase273_manifest.json').read_text())
    bind(review['files'])
    need(sha(ROOT/'phase256_export.json')==AUTHOR_HASH,'author manifest binding')
    author=json.loads((ROOT/'phase256_export.json').read_text())
    bind(author['files']); bind(author['frozen_dependencies'])
    primary=[]
    if args.verify_primary:
        sources=json.loads((ROOT/'phase256_sources.json').read_text())
        for row in sources['primary_sources']:
            need(sha(ROOT/row['path'])==row['sha256'],'primary binding: '+row['id'])
            primary.append(row['id'])
    process=subprocess.run([sys.executable,'-B','-O',str(ROOT/'phase273_independent_cells.py'),
                             '--models',str(ROOT/'phase256_voltage_models.json'),
                             '--out',str(out/'independent_cells.json')],capture_output=True,text=True,timeout=120)
    (out/'independent_cells.log').write_text(process.stdout+process.stderr)
    need(process.returncode==0,'independent cells replay')
    cells=json.loads((out/'independent_cells.json').read_text())
    expected=json.loads((ROOT/'phase273_independent_cells_report.json').read_text())
    need(cells==expected,'independent exact result')
    author_result=None
    if args.author_replay:
        command=[sys.executable,'-B','-O',str(ROOT/'phase256_check.py'),'--out',str(out/'author'),
                 '--lean',args.lean,'--packages',args.packages]
        if args.verify_primary:
            command.append('--verify-primary')
        process=subprocess.run(command,capture_output=True,text=True,timeout=180)
        (out/'author.log').write_text(process.stdout+process.stderr)
        need(process.returncode==0,'author replay')
        author_result=json.loads((out/'author/report.json').read_text())
        need(author_result['status']=='PASS' and author_result['new_Lean_declarations']==5
             and author_result['finite_models']==5 and len(author_result['controls'])==4,'author result scope')
    report={'status':'PASS','seconds':round(time.monotonic()-start,3),
            'review_manifest_sha256':sha(ROOT/'phase273_manifest.json'),
            'author_manifest_sha256':AUTHOR_HASH,'author_exports_bound':len(author['files']),
            'author_dependencies_bound':len(author['frozen_dependencies']),
            'review_exports_bound':len(review['files']),'primary_checked':primary,
            'independent_models':len(cells['results']),
            'independent_boundary_tests':sum(sum(f['boundary_membership_checks'] for f in r['fields']) for r in cells['results']),
            'independent_controls':cells['controls'],
            'fresh_author_replay':None if author_result is None else
               {k:author_result[k] for k in ['status','seconds','new_Lean_declarations','finite_models','controls']},
            'scope':'Bindings and bounded computations; written uniform surface theorem accepted by independent mathematical review, not fully formalized.'}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__=='__main__':
    main()
