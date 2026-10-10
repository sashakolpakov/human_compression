#!/usr/bin/env python3
"""Check frozen277/279 bindings, independent finite model and optional fresh Lean replay."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent
AUTHOR='72e92ed82299be8c658c2f3cb45f75e67f81b0fb48379fb052de05ea3d1007c9'


def need(ok,message):
    if not ok:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True,type=Path)
    parser.add_argument('--author-replay',action='store_true')
    parser.add_argument('--verify-primary',action='store_true')
    parser.add_argument('--lean',default='/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean')
    parser.add_argument('--packages',default='/Users/sasha/bogachev/formal/.lake/packages')
    args=parser.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(),'fresh output directory required')
    out=args.out.resolve();out.mkdir(parents=True);start=time.monotonic()
    review=json.loads((ROOT/'phase279_manifest.json').read_text())
    for path,digest in review['files'].items():
        need(sha(ROOT/path)==digest,'review binding: '+path)
    need(sha(ROOT/'phase277_export.json')==AUTHOR,'author manifest binding')
    author=json.loads((ROOT/'phase277_export.json').read_text())
    for row in author['exports']+author['dependencies']:
        need(sha(ROOT/row['path'])==row['sha256'],'author binding: '+row['path'])
    primary=[]
    if args.verify_primary:
        for row in json.loads((ROOT/'phase277_sources.json').read_text())['primary_sources']:
            need(sha(ROOT/row['path'])==row['sha256'],'primary binding: '+row['id'])
            primary.append(row['id'])
    process=subprocess.run([sys.executable,'-B','-O',str(ROOT/'phase279_independent_model.py'),
                            '--out',str(out/'independent_model.json')],capture_output=True,text=True,timeout=120)
    (out/'independent_model.log').write_text(process.stdout+process.stderr)
    need(process.returncode==0,'independent model')
    result=json.loads((out/'independent_model.json').read_text())
    need(result==json.loads((ROOT/'phase279_independent_model_report.json').read_text()),'exact independent result')
    source_result=json.loads((ROOT/'phase277_obstruction_report.json').read_text())
    for key in ['base_parabolic_orders','cover_parabolic_orders','base_IP_failures']:
        need(result[key]==source_result[key],'independent semantic comparison: '+key)
    fresh=None
    if args.author_replay:
        command=[sys.executable,'-B','-O',str(ROOT/'phase277_check.py'),'--out',str(out/'author'),
                 '--lean',args.lean,'--packages',args.packages]
        if args.verify_primary:
            command.append('--verify-primary')
        process=subprocess.run(command,capture_output=True,text=True,timeout=180)
        (out/'author.log').write_text(process.stdout+process.stderr)
        need(process.returncode==0,'fresh author replay')
        r=json.loads((out/'author/report.json').read_text())
        need(r['status']=='PASS' and r['new_Lean_declarations']==3 and r['axioms']==[]
             and len(r['controls'])==3,'author replay scope')
        fresh={key:r[key] for key in ['status','seconds','new_Lean_declarations','axioms','controls']}
    report={'status':'PASS','seconds':round(time.monotonic()-start,3),
            'review_manifest_sha256':sha(ROOT/'phase279_manifest.json'),'author_manifest_sha256':AUTHOR,
            'review_exports_bound':len(review['files']),'author_exports_bound':len(author['exports']),
            'author_dependencies_bound':len(author['dependencies']),'primary_checked':primary,
            'independent_cover_IP_pairs':result['cover_IP_pairs'],'independent_end_IP_pairs':result['end_IP_pairs'],
            'semantic_comparison':'All64 parabolic orders and all base intersection failures agree',
            'independent_controls':result['controls'],'fresh_author_replay':fresh,
            'scope':'Exact interval theorem and non-polytopal obstruction accepted by written review; finite examples and three scoped order proofs do not prove all-rank finite infinitude.'}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':
    main()
