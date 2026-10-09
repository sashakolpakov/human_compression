#!/usr/bin/env python3
"""Fuse and independently recognize a complete source-bound sporadic census."""
import argparse, hashlib, json, os, shutil, subprocess, time
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('group',choices=['J1','M11','M12','J2'])
    ap.add_argument('--require-2t',action='store_true')
    ap.add_argument('--gap',default=os.environ.get('GAP') or shutil.which('gap')); a=ap.parse_args()
    if not a.gap: ap.error('Set GAP or pass --gap')
    stem='phase6_sporadic_'+a.group+('_2T' if a.require_2t else '')
    progress_path=HERE/(stem+'_progress.json'); progress=json.loads(progress_path.read_text())
    assert progress['all_borels_complete'] and set(progress['completed'])=={str(i) for i in range(1,progress['total_borels']+1)}
    assert sha(HERE/'phase6_sporadic_search.g')==progress['executed_script_sha256']
    for item in progress['completed'].values(): assert sha(HERE/item['checkpoint'])==item['sha256']
    for run in progress['runs']:
        assert sha(HERE/run['log'])==run['log_sha256']
        assert run['executed_script_sha256']==progress['executed_script_sha256']
        assert run['status'] in ['complete','interrupted']
        if run['status']=='complete': assert run['passed']
    prereq={progress_path.name:sha(progress_path),'phase4_geometry_checks.g':sha(HERE/'phase4_geometry_checks.g')}
    runs=[]
    for stage,marker in [('fuse','FULL_CENSUS_PASS'),('verify','ALL_WITNESSES_PASS')]:
        script=HERE/f'phase6_sporadic_{stage}.g'; digest=sha(script); log=HERE/f'{stem}_{stage}.log'
        cmd=(f'GROUP_NAME:="{a.group}";CHECKPOINT_DIR:="{stem}_checkpoints";'
             f'OUTPUT_FILE:="{stem}_representatives.g";WITNESS_FILE:="{stem}_representatives.g";'
             f'REQUIRE_2T:={str(a.require_2t).lower()};Read("{script.name}");QUIT;')
        start=time.monotonic()
        with log.open('w') as f: r=subprocess.run([a.gap,'-q','-c',cmd],cwd=HERE,stdout=f,stderr=subprocess.STDOUT)
        out=log.read_text(); passed=r.returncode==0 and marker in out and 'Error,' not in out and sha(script)==digest
        runs.append(dict(script=script.name,executed_sha256=digest,log=log.name,log_sha256=sha(log),seconds=time.monotonic()-start,exit_code=r.returncode,passed=passed,completion_marker=marker))
        print(stage,'PASS' if passed else 'FAIL',round(runs[-1]['seconds'],3),flush=True)
        if not passed: break
    for name,digest in prereq.items(): assert sha(HERE/name)==digest
    report=dict(group=a.group,require_2t=a.require_2t,runs=runs,prerequisites=prereq,passed=len(runs)==2 and all(r['passed'] for r in runs))
    (HERE/(stem+'_final_checks.json')).write_text(json.dumps(report,indent=2)+'\n')
    if not report['passed']: raise SystemExit(1)
if __name__=='__main__': main()
