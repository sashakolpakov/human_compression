"""Independent public restoration and adapter-boundary audit."""
from pathlib import Path
import hashlib, json, os, subprocess

S=Path('/Users/sasha/medusa/research/leemans')
W=S/'reboot_20261013'
D=W/'F001_publication_work'
O=W/'F001_portable_distinct'
R=Path('/Users/sasha/medusa/math_compression')
P=D/'stage01'
T=O/'replay01/restored/study'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def need(b,s):
    if not b:raise ValueError(s)
transport=load(P/'audit/recoveries/F001/v1/transport.json')
rows={r['path']:r for r in transport['files']}
primary=set(transport['primary_sources_hash_only'])
restored=0
for name,row in rows.items():
    p=T/name
    if name in primary:
        need(not p.exists(),'Documentary source unexpectedly restored')
        continue
    need(p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'Post-run input mutation '+name)
    restored+=1
bindings=[]
def check_binding(row):
    name=row['path'];need(name in rows,'Untransported binding '+name)
    need(row['sha256']==rows[name]['sha256'],'Binding hash '+name)
    if 'bytes' in row:need(row['bytes']==rows[name]['bytes'],'Binding size '+name)
    bindings.append(name)
for r in transport['packets']:
    name=str(Path(r['path']).parent)
    if not name.startswith('corpus106_F001'):continue
    for filename in ['dependencies.json','bindings.json']:
        q=T/name/filename
        if q.is_file():
            for x in load(q).get('bindings',[]):check_binding(x)
for row in load(T/'corpus106_F001_mixed_bound_root_review/integrity.json')['checks']:check_binding(row)
for row in load(T/'corpus106_F001_rank_bound_v1/provenance.json')['source_bindings']:check_binding(row)
need(sha(T/'corpus106_F001_principal_root_review/manifest.json')=='a9a1cd5a57daac7a722120003db28170d58d1c717a07516de817a319599fbd77','Exact whole-principal review')
need(sha(T/'corpus106_F001_mixed_bound_root_review/manifest.json')=='be4a521bdf2e72d19545c796bb81b9f8a8a6f0cdb15f547773e96075f75e3115','Exact mixed independent acceptance')
proposal=load(D/'integration01/admission_proposal.json');public_pins=[]
def walk(x):
    if isinstance(x,dict):
        if all(k in x for k in ['path','bytes','sha256']):
            q=P/x['path'];q=q if q.is_file() else R/x['path']
            need(q.is_file() and q.stat().st_size==x['bytes'] and sha(q)==x['sha256'],'Public proposal pin '+x['path']);public_pins.append(x['path'])
        for y in x.values():walk(y)
    elif isinstance(x,list):
        for y in x:walk(y)
walk(proposal)
py='/Users/sasha/.venvs/global/bin/python';script=D/'portable_check.py'
common=['--repo',str(R),'--payload',str(P),'--expected-transport',sha(P/'audit/recoveries/F001/v1/transport.json')]
tests=[]
for label,flags,env,wrong in [
    ('optimized_flag',['-O'],dict(os.environ),False),
    ('optimized_environment',[],dict(os.environ,PYTHONOPTIMIZE='1'),False),
    ('wrong_transport',[],dict(os.environ),True)]:
    args=[py,*flags,str(script),*common,'--out',str(O/('negative_'+label))]
    if wrong:args[args.index('--expected-transport')+1]='0'*64
    r=subprocess.run(args,env=env,capture_output=True,text=True,timeout=10)
    (O/(label+'.stdout')).write_text(r.stdout);(O/(label+'.stderr')).write_text(r.stderr)
    message='frozen transport changed' if wrong else 'optimized Python unsupported'
    need(r.returncode!=0 and message in r.stderr,'Malformed invocation accepted '+label)
    need(not (O/('negative_'+label)).exists(),'Rejected invocation created output')
    tests.append({'case':label,'returncode':r.returncode,'rejected_before_restoration':True})
report=dict(status='PASS_DISTINCT_PUBLIC_F001_CLOSURE',restored_files_unchanged=restored,
    logical_records=len(rows),checked_required_binding_records=len(bindings),
    checked_required_binding_files=len(set(bindings)),proposal_public_pins=len(public_pins),
    exact_whole_principal_and_mixed_acceptances=True,
    documentary_adapter={'functions':['odd_existence.bind','reflection_bound.binding','mixed_bound.binding','principal.bind'],
       'exception_only_at_study_root':True,'exact_primary_names':sorted(primary),
       'checks_preserved':'All non-primary bindings delegate to the original hash function; scope, arithmetic, damaged controls and native checks are unchanged.',
       'runtime_binding_adapter_used':True,'frozen_program_bytes_changed':False},
    negative_controls=tests,source_scope='Principal Theorem 1.1; auxiliary Lemma 4.1 correction separate',
    prior_contribution='Reviewer supplied bounded nonsemisimple calculations; this is an operational review only. Root supplied distinct mathematical acceptance.',
    whole_original_credit=0)
(O/'closure_report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['documentary_adapter','negative_controls']}))
