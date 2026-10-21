#!/usr/bin/env python3
"""Run all J2 checks; requires a user-supplied primary supplementary archive."""
import argparse,hashlib,json,os,shutil,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--archive',type=Path,required=True);ap.add_argument('--gap',default=os.environ.get('GAP') or shutil.which('gap'));a=ap.parse_args()
    if not a.gap:ap.error('GAP not found: set GAP or pass --gap /path/to/gap')
    subprocess.run([sys.executable,str(HERE/'phase4_parse_j2.py'),'--archive',str(a.archive.resolve())],check=True,cwd=REPO)
    runs=[]
    for name,marker in [('phase4_verify_j2','VERIFICATION_COMPLETED'),('phase4_thin_j2','EXHAUSTION_COMPLETE'),('phase4_fuse_j2','FUSION_COMPLETE'),('phase4_identify_source','SOURCE_IDENTIFICATION_PASS'),('phase4_verify_thin_witnesses','THIN_WITNESSES_PASS')]:
        source=HERE/(name+'.g');log=HERE/(name+'.log');before=sha(source);start=time.monotonic()
        with log.open('w') as f:r=subprocess.run([a.gap,'-q',str(source.relative_to(REPO))],stdout=f,stderr=subprocess.STDOUT,cwd=REPO)
        seconds=time.monotonic()-start;out=log.read_text()
        passed=r.returncode==0 and marker in out and 'Error,' not in out and sha(source)==before
        runs.append(dict(script=source.name,executed_sha256=before,log=log.name,log_sha256=sha(log),seconds=seconds,exit_code=r.returncode,completion_marker=marker,passed=passed))
        print(name, 'PASS' if passed else 'FAIL',round(seconds,3),flush=True)
        if not passed:break
    report=dict(scope='Exact source-data recognition, independent all-rank thin enumeration, and Aut(J2)/type fusion; nonthin completeness is not independently enumerated.',runs=runs,passed=len(runs)==5 and all(r['passed'] for r in runs))
    (HERE/'phase4_j2_runs.json').write_text(json.dumps(report,indent=2)+'\n')
    if not report['passed']:raise SystemExit(1)
if __name__=='__main__':main()
