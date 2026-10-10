#!/usr/bin/env python3
"""Public replay of the reviewed rank-four finite-cover theorem's certificates."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PINS={'phase256_export.json': '8d22baec4ddafcbb624300e7c65a23079982be724181b8282fafd512c70503ea', 'phase273_manifest.json': '9258d80ad8e29fcd0f985ed95dcbde457d255797292a6c3dd4f2f38f71f46b7b'}
def need(ok,msg):
    if not ok:raise RuntimeError('PHASE274_REJECT '+msg)
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for k in ['out','lean','packages']:ap.add_argument('--'+k,type=Path,required=True)
    a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output')
    for n,h in PINS.items():need(hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h,'manifest '+n)
    f=ROOT/'formal/dependency_manifest.json'
    need(hashlib.sha256(f.read_bytes()).hexdigest()=='4c716f4ff0ea4940311014c9853c0b8e5aaab8250f8cefdf9f8003845cfb02e3','dependency pins')
    dependencies=[]
    for row in json.loads(f.read_bytes())['packages']:
        path=a.packages/row['name']
        rev=subprocess.check_output(['git','-C',str(path),'rev-parse','HEAD'],text=True).strip()
        need(rev==row['rev'],'package revision '+row['name'])
        need(subprocess.run(['git','-C',str(path),'diff','--quiet','HEAD','--']).returncode==0,'clean package '+row['name'])
        dependencies.append(dict(name=row['name'],revision=rev))
    version=subprocess.check_output([a.lean,'--version'],text=True).strip();need('version 4.32.2,' in version,'Lean version')
    result=subprocess.run([sys.executable,'-B','-O',str(ROOT/'phase273_check.py'),'--out',str(a.out),
                           '--author-replay','--lean',str(a.lean),'--packages',str(a.packages)])
    need(result.returncode==0,'full independent replay')
    r=json.loads((a.out/'report.json').read_bytes())
    need(r['status']=='PASS' and r['independent_boundary_tests']==648 and r['independent_models']==6,'review scope')
    report=dict(status='PASS',seconds=r['seconds'],lean_version=version,dependencies=dependencies,
                scoped_Lean_declarations=5,independent_models=6,boundary_membership_checks=648,
                negative_controls=6,primary_files_required=False,
                scope='Complete written rank-four theorem independently accepted; Lean verifies affine avoidance/counting/parity steps, not topology or the complete cover theorem.')
    (a.out/'public_report.json').write_text(json.dumps(report,indent=2)+'\n');print('PHASE274_PUBLIC_PASS')
if __name__=='__main__':main()
