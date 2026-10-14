"""Review integrity plus independent small controls; not a mathematical prover."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Normal Python required before filesystem work')
sys.dont_write_bytecode=True
import argparse,hashlib,json,shutil,subprocess,os
from pathlib import Path

def need(ok,msg):
    if not ok:raise ValueError(msg)
def main():
    a=argparse.ArgumentParser();a.add_argument('--study',type=Path,required=True);a.add_argument('--repo',type=Path,required=True);a.add_argument('--out',type=Path,required=True);q=a.parse_args()
    base=Path(__file__).resolve().parent;out=q.out.resolve();need(not out.exists() and not out.is_relative_to(base),'Fresh external output required')
    roots={Path('/Users/sasha/medusa/research/leemans'):q.study.resolve(),Path('/Users/sasha/medusa/math_compression'):q.repo.resolve()}
    def verify(p,row):
        b=p.read_bytes();need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'Changed pin: '+str(p))
    for r in json.loads((base/'manifest.json').read_text())['exports']:
        p=(base/r['path']).resolve();need(p.is_relative_to(base),'Unsafe export');verify(p,r)
    dependencies=json.loads((base/'dependencies.json').read_text())
    for r in dependencies:
        p=Path(r['path']);target=None
        for old,new in roots.items():
            if p.is_relative_to(old):target=new/p.relative_to(old);break
        need(target is not None,'Unknown namespace');verify(target,r)
    review=json.loads((base/'review.json').read_text());need(review['status']=='ACCEPTED_L052_GENERAL_RESIDUE_THEORY' and review['whole_original_credit']==0,'Review scope')
    out.mkdir(parents=True);shutil.copy2(base/'controls.py',out/'controls.py');env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
    p=subprocess.run([sys.executable,str(out/'controls.py')],capture_output=True,env=env,timeout=45)
    (out/'controls.stdout').write_bytes(p.stdout);(out/'controls.stderr').write_bytes(p.stderr);need(p.returncode==0,'Independent controls failed')
    need(json.loads((out/'controls_report.json').read_text())==json.loads((base/'controls_report.json').read_text()),'Independent result changed')
    report=dict(status='PASS_L052_DISTINCT_REVIEW_REPLAY',dependencies=len(dependencies),independent_controls=True,mathematical_review='Written distinct review acquired; not proved by this script',whole_original_credit=0)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
