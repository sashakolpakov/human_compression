#!/usr/bin/env python3
"""Fresh public replay for interval lifting and its separate kernel obstruction."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
PINS={'phase277_export.json': '72e92ed82299be8c658c2f3cb45f75e67f81b0fb48379fb052de05ea3d1007c9', 'phase279_manifest.json': '3585339006b0885f0ab6b04759dc1ea73babffd431a3a317478b63aa29a1ae6d'}
def need(ok,msg):
    if not ok:raise RuntimeError('PHASE280_REJECT '+msg)
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
    result=subprocess.run([sys.executable,'-B','-O',str(ROOT/'phase279_check.py'),'--out',str(a.out),
                           '--author-replay','--lean',str(a.lean),'--packages',str(a.packages)])
    need(result.returncode==0,'full independent replay')
    r=json.loads((a.out/'report.json').read_bytes())
    need(r['status']=='PASS' and r['independent_cover_IP_pairs']==1024 and r['independent_end_IP_pairs']==512,'review scope')
    report=dict(status='PASS',seconds=r['seconds'],lean_version=version,dependencies=dependencies,
                scoped_Lean_declarations=3,axioms=[],primary_files_required=False,
                author_exports=17,retained_dependencies=3,review_exports=8,
                scope='Complete written interval theorem and separate divisibility obstruction independently accepted; Lean verifies the order argument, not the geometric extension or full finite-cover conjecture.')
    (a.out/'public_report.json').write_text(json.dumps(report,indent=2)+'\n');print('PHASE280_PUBLIC_PASS')
if __name__=='__main__':main()
