#!/usr/bin/env python3
"""Fuse the complete independent census and verify all final representatives."""
import argparse,hashlib,json,os,shutil,subprocess,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--gap',default=os.environ.get('GAP') or shutil.which('gap'));a=ap.parse_args()
    if not a.gap:ap.error('GAP unavailable: set GAP or pass --gap')
    progress=json.loads((HERE/'phase5_j2_progress.json').read_text())
    assert progress['all_146_borels_complete'] and set(progress['completed'])=={str(i) for i in range(1,147)}
    assert sha(HERE/'phase5_j2_search.g')==progress['executed_script_sha256']
    for run in progress['runs']:
        assert run['passed'] and sha(HERE/run['log'])==run['log_sha256']
    for item in progress['completed'].values():assert sha(HERE/item['checkpoint'])==item['sha256']
    prerequisites={'phase5_j2_progress.json':sha(HERE/'phase5_j2_progress.json'),'phase4_geometry_checks.g':sha(HERE/'phase4_geometry_checks.g')}
    runs=[]
    for name,marker in [('phase5_j2_fuse','FULL_CENSUS_PASS'),('phase5_j2_verify','ALL_WITNESSES_PASS')]:
        source=HERE/(name+'.g');log=HERE/(name+'.log');digest=sha(source);start=time.monotonic()
        with log.open('w') as f:r=subprocess.run([a.gap,'-q',str(source.relative_to(REPO))],cwd=REPO,stdout=f,stderr=subprocess.STDOUT)
        out=log.read_text();passed=r.returncode==0 and marker in out and 'Error,' not in out and sha(source)==digest
        runs.append(dict(script=source.name,executed_sha256=digest,log=log.name,log_sha256=sha(log),seconds=time.monotonic()-start,passed=passed,exit_code=r.returncode,completion_marker=marker))
        print(name,'PASS' if passed else 'FAIL',round(runs[-1]['seconds'],3),flush=True)
        if not passed:break
    for name,digest in prerequisites.items():assert sha(HERE/name)==digest
    report=dict(runs=runs,prerequisites=prerequisites,passed=len(runs)==2 and all(r['passed'] for r in runs))
    (HERE/'phase5_j2_final_checks.json').write_text(json.dumps(report,indent=2)+'\n')
    if not report['passed']:raise SystemExit(1)
if __name__=='__main__':main()
