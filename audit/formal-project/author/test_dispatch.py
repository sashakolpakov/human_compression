#!/usr/bin/env python3
"""Bounded synthetic-checker tests of orchestration, never proof certificates."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent

FAKE_CHECKER = r'''import argparse, hashlib, json, os
from pathlib import Path
p=argparse.ArgumentParser()
for name in ('lean','packages','out'):p.add_argument('--'+name,required=True)
p.add_argument('--jobs',type=int)
a=p.parse_args(); out=Path(a.out);out.mkdir()
key=Path(__file__).parent.name
root=Path(__file__).resolve().parents[1 if key=='scripts' else 3]
mode=json.loads((root/'fixture_mode.json').read_text())
component='legacy' if key=='scripts' else 'topic-b'
behavior=mode.get(component,'pass')
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
report={'status':'PASS','fixture_only_no_lean_invoked':True,'forwarded_jobs':a.jobs,
 'inherited_lean_path':os.environ.get('LEAN_PATH'),
 'inherited_lean_src_path':os.environ.get('LEAN_SRC_PATH'),
 'inherited_python_optimize':os.environ.get('PYTHONOPTIMIZE')}
if component=='legacy':
 files=sorted((root/'research/case_study/formal').glob('M*.lean'))
 report.update(checker_sha256=sha(Path(__file__)),modules=[{
  'module':f.stem,'source_path':str(f.relative_to(root)),'source_sha256':sha(f),
  'exit_code':0,'axiom_reports':[{'declaration':f.stem+'.t','axioms':[]}]} for f in files])
 if behavior=='omitted_module':report['modules'].pop()
 report.update(compiled_modules=len(report['modules']),module_count=len(report['modules']),
               axiom_declarations=len(report['modules']))
else:
 base=root/'papers/topic-b/v2'
 report.update(source_sha256=sha(base/'formal/ResidualGeneration.lean'),
  author_manifest_sha256=sha(base/'manifest.json'),
  axioms=[{'name':'Fixture.t','axioms':[]}],
  executions=[{'label':n,'returncode':0 if n=='ResidualGeneration' else 1}
   for n in ('ResidualGeneration','without_membership','without_outside','without_maximality')],
  altered_countermodel_rejected=True,finite_hypothesis_countermodels=[{}, {}, {}])
 if behavior=='wrong_hash':report['source_sha256']='0'*64
 if behavior=='mutate_source':
  with (base/'formal/ResidualGeneration.lean').open('a') as f:f.write('\n-- changed\n')
 if behavior=='failed_control':report['executions'][1]['returncode']=0
if behavior!='missing_report':(out/'report.json').write_text(json.dumps(report))
raise SystemExit(7 if behavior=='nonzero_with_pass' else 0)
'''


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def fixture(path, mode):
    write(path/'scripts/check_lean.py', FAKE_CHECKER)
    write(path/'papers/topic-b/v2/check.py', FAKE_CHECKER)
    write(path/'fixture_mode.json', json.dumps(mode))
    for name in ('M1', 'M2'):
        write(path/f'research/case_study/formal/{name}.lean', 'theorem t : True := by trivial\n')
        write(path/f'research/case_study/formal/{name}.check.json', '{}')
    for name in ('lakefile.lean', 'lean-toolchain', 'dependency_manifest.json'):
        write(path/'research/case_study/formal'/name, 'fixture only')
    write(path/'papers/topic-b/v2/formal/ResidualGeneration.lean', 'theorem t : True := by trivial\n')
    write(path/'papers/topic-b/v2/formal/scope.json', json.dumps({'reported_declarations':['Fixture.t']}))
    write(path/'papers/topic-b/v2/formal/dependency_manifest.json', '{}')
    write(path/'papers/topic-b/v2/manifest.json', '{}')
    write(path/'fake-lean', 'This fixture never runs a Lean compiler.\n')
    (path/'packages').mkdir()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out', type=Path, required=True)
    a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(), 'fresh test output required')
    out=a.out.resolve();out.mkdir(parents=True)
    rows=[]
    cases=[
        ('default_all', {}, [], 'PASS_FULL_CONFIGURED_PROJECT', 3),
        ('only_topic_b', {}, ['--components','topic-b'], 'PASS_PARTIAL', 1),
        ('only_legacy', {}, ['--components','legacy'], 'PASS_PARTIAL', 2),
        ('legacy_process_failure', {'legacy':'nonzero_with_pass'}, [], 'FAIL', 0),
        ('topic_b_process_failure', {'topic-b':'nonzero_with_pass'}, [], 'FAIL', 2),
        ('missing_child_report', {'topic-b':'missing_report'}, ['--components','topic-b'], 'FAIL', 0),
        ('wrong_source_hash', {'topic-b':'wrong_hash'}, ['--components','topic-b'], 'FAIL', 0),
        ('omitted_legacy_module', {'legacy':'omitted_module'}, ['--components','legacy'], 'FAIL', 0),
        ('changed_source_during_run', {'topic-b':'mutate_source'}, ['--components','topic-b'], 'FAIL', 0),
        ('weakened_control_passed', {'topic-b':'failed_control'}, ['--components','topic-b'], 'FAIL', 0),
        ('dangling_output_symlink', {}, ['--components','topic-b'], None, None),
        ('output_inside_checkout', {}, ['--components','topic-b'], None, None),
        ('mixed_all_selection', {}, ['--components','all','legacy'], None, None),
        ('duplicate_selection', {}, ['--components','topic-b','topic-b'], None, None),
    ]
    for name, mode, extra, status, count in cases:
        case=out/name;case.mkdir();root=case/'repo';fixture(root,mode)
        target=case/'result'
        if name=='dangling_output_symlink':target.symlink_to(case/'missing')
        if name=='output_inside_checkout':target=root/'forbidden-output'
        command=[sys.executable,'-B','-O',str(HERE/'check_project_lean.py'),
                 '--repo',str(root),'--lean',str(root/'fake-lean'),
                 '--packages',str(root/'packages'),'--out',str(target),'--jobs','3',*extra]
        env=dict(os.environ,LEAN_PATH='must-not-reach-child',LEAN_SRC_PATH='must-not-reach-child',PYTHONOPTIMIZE='2')
        result=subprocess.run(command,capture_output=True,env=env,text=True,timeout=20)
        write(case/'stdout',result.stdout);write(case/'stderr',result.stderr)
        need((result.returncode==0)==(status is not None and status.startswith('PASS')),name+': exit status')
        row=dict(name=name,exit_code=result.returncode,expected_status=status,
                 fixture_only_no_mathematical_verification=True)
        if status:
            r=json.loads((target/'report.json').read_text())
            need(r['status']==status and r['fresh_source_count']==count,name+': coverage/status')
            need(r['all_configured_sources_recompiled_this_invocation']==(status=='PASS_FULL_CONFIGURED_PROJECT'),name+': full label')
            if name=='only_topic_b':
                need(r['components']['legacy']['status']=='NOT_SELECTED' and len(r['unchecked_sources'])==2,name+': legacy omitted')
            if name=='only_legacy':
                need(r['components']['topic-b']['status']=='NOT_SELECTED' and len(r['unchecked_sources'])==1,name+': B omitted')
            if name=='legacy_process_failure':
                need(r['components']['topic-b']['status']=='NOT_RUN_AFTER_FAILURE',name+': fail fast')
            for key,c in r['components'].items():
                if c['status']=='PASS':
                    child=json.loads((target/c['report_path']).read_text())
                    need(child['forwarded_jobs']==(3 if key=='legacy' else None),name+': jobs interface')
                    need(all(child[n] is None for n in ('inherited_lean_path','inherited_lean_src_path','inherited_python_optimize')),name+': environment')
                    need(sha(target/c['report_path'])==c['report_sha256'],name+': preserved report')
            row.update(report_sha256=sha(target/'report.json'),fresh_source_count=count)
            write(case/'wrapper_report.json',json.dumps(r,indent=2)+'\n')
        else:
            need(not (target/'report.json').exists(),name+': output rejected before dispatch')
        rows.append(row)
    report=dict(status='PASS_ORCHESTRATION_FIXTURES_ONLY',runner_sha256=sha(HERE/'check_project_lean.py'),
        test_sha256=sha(Path(__file__)),cases=rows,case_count=len(rows),actual_lean_compilations=0,
        scope='Synthetic child checkers exercise dispatch, fresh-report validation, failure propagation and partial-coverage labels. They prove no mathematical theorem.')
    write(out/'report.json',json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status=report['status'],cases=len(rows),actual_lean_compilations=0)))


if __name__=='__main__':main()
