import sys
if sys.flags.optimize:
    raise RuntimeError('ordinary Python required')
from pathlib import Path
import ast, copy, hashlib, importlib.util, json, os, shutil, subprocess, types

B=Path('/Users/sasha/medusa/research/leemans/reboot_20261013')
W=Path('/Users/sasha/medusa/research/leemans/algebra/coxeter_quotients/publication_work')
R=W/'trial01'
PUBLIC=Path('/Users/sasha/medusa/math_compression')
OUT=Path(__file__).parent/'independent01'
BASE='5cbf9a6908d3a4cb20d1184297764ae8c6d596ab'
AUD='audit/science89/v1'
HISTORY=['README.rst','audit/completion.rst','audit/corpus/latest.json',
         'papers/latest_catalogue.json','papers/catalogue_corrected_unmeasured.json',
         'papers/catalogue_principal_refutations.json','scripts/verify_snapshot.py',
         'audit/protocol.tex','audit/protocol.pdf']

def need(v,m):
    if not v: raise ValueError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b))
def load(p):return json.loads(p.read_text())
def check_pin(root,row):
    p=root/row['path'];b=p.read_bytes()
    need(len(b)==row['bytes'] and sha(b)==row['sha256'],'bound file '+str(p))
def module(name,p):
    s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

OUT.mkdir()
need(sha((W/'registration_ready.json').read_bytes())=='de020248e063774b55e30a12ab8cbaf93b6c4cab410dad76d8746b4c6e5a681a','ready pin')
need(sha((W/'registration_handoff_manifest.json').read_bytes())=='2ee87ade33c686a4d24c1ae87bcad2230cf2f5af617326d25ec783e1dbf0efdd','handoff pin')
handoff=load(W/'registration_handoff_manifest.json')
for row in handoff['files']:check_pin(W,row)
candidate=load(W/'candidate_manifest.json')
for row in candidate['files']:
    check_pin(R,row);check_pin(PUBLIC,row)

# Compare against Git's actual object inventory, independently of the author's
# predecessor_tree.json and current checker.
raw=subprocess.check_output(['git','ls-tree','-rz','--full-tree',BASE],cwd=PUBLIC)
routes=load(R/AUD/'history_routes.json')['routes']
need(set(routes)==set(HISTORY),'exact nine historic routes')
tree=[];links=[];changed=[]
for entry in raw.split(b'\0'):
    if not entry:continue
    info,name=entry.split(b'\t',1);mode,kind,oid=info.decode().split();name=name.decode()
    need(kind=='blob','only tracked blob entries')
    row=dict(path=name,mode=mode,git_object=oid);tree.append(row)
    p=R/name
    if name in HISTORY:p=R/routes[name]['path']
    elif name=='provenance/publication_manifest.json':p=R/AUD/'manifest_history/predecessor_publication_manifest.json'
    if mode=='120000':
        need(p.is_symlink(),'retained symlink '+name);data=os.readlink(p).encode();links.append(dict(path=name,target=os.readlink(p)))
    else:
        need(p.is_file() and not p.is_symlink(),'retained regular file '+name);data=p.read_bytes()
        need(bool(p.stat().st_mode&0o111)==(mode=='100755'),'retained mode '+name)
    need(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==oid,'Git baseline bytes '+name)
    if name in HISTORY and (R/name).read_bytes()!=data:changed.append(name)

old=load(R/routes['audit/corpus/latest.json']['path']);current=load(R/'audit/corpus/latest.json')
for key in old:
    if any(word in key for word in ['measured','measurement','compression']):
        if key in ('measurement_pending_original_ids','scientific_unmeasured_original_ids'):
            need(current[key]==sorted(old[key]+['L033']),'only L033 added unmeasured')
        else:need(current[key]==old[key],'old measurement field '+key)
before=load(R/old['active_catalogue']['path']);after=load(R/current['active_catalogue']['path'])
need([e['original_id']for e in before['entries']]==[e['original_id']for e in after['entries']],'source ordering')
mutated=[a['original_id']for a,b in zip(before['entries'],after['entries'])if a!=b]
need(mutated==['L033'],'only one source entry')
for ident in old['measured_original_ids']:
    a=next(e for e in before['entries']if e['original_id']==ident)
    b=next(e for e in after['entries']if e['original_id']==ident)
    need(a==b,'exact measured entry '+ident)
oldtext=(R/routes['scripts/verify_snapshot.py']['path']).read_text();newtext=(R/'scripts/verify_snapshot.py').read_text()
def functions(t):return {n.name:n for n in ast.parse(t).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
of,nf=functions(oldtext),functions(newtext)
for name,n in of.items():
    if name=='main':continue
    need(ast.dump(n,include_attributes=False)==ast.dump(nf[name],include_attributes=False),'old AST '+name)
    need(ast.get_source_segment(oldtext,n)==ast.get_source_segment(newtext,nf[name]),'old literal function '+name)
need(set(nf)-set(of)=={'check_previous_science89','check_science89'},'only two added verifier functions')
oldcalls=[n.func.id for n in ast.walk(of['main'])if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)]
newcalls=[n.func.id for n in ast.walk(nf['main'])if isinstance(n,ast.Call)and isinstance(n.func,ast.Name)]
need(newcalls==[{'check_previous_science88':'check_previous_science89','check_science88':'check_science89'}.get(x,x)for x in oldcalls],'unchanged main call coverage')

# Additional false-admission tests exercise the actual semantics routine.
guard=module('independent_science89_guard',R/'scripts/check_science89.py')
params=load(R/AUD/'registration_parameters.json');spec=params['source_spec'];proposal=load(R/spec['proposal']['path']);admission=load(R/guard.admission_path())
cases=[('same-size measured permutation',lambda c,a:c['measured_original_ids'].reverse()),
       ('different old disposition pointer',lambda c,a:c['current_principal_disposition_registration'].update(sha256='0'*64)),
       ('measurement reassignment',lambda c,a:c['measurement_pending_original_ids'].__setitem__(0,'WRONG_ID')),
       ('journal scope substitution',lambda c,a:a.update(scope_note='Complete 25-page journal edition.')),
       ('different accepted source contents',lambda c,a:a['accepted_proposal_contents'].update(source_edition='different edition')),
       ('software factor invented',lambda c,a:a.update(software_inclusive_factor=2)),
       ('lost source id',lambda c,a:a.update(source_ids=[])),
       ('wrong shared publication gate',lambda c,a:a.update(shared_registration_gate='audit/science88/v1/root_integration.json'))]
rejected=[]
for label,change in cases:
    c,a=copy.deepcopy((current,admission));change(c,a)
    try:guard.semantics(c,old,a,spec,proposal)
    except (ValueError,KeyError):rejected.append(label)
    else:raise ValueError('false admission accepted '+label)

# Exercise the unchanged history wrapper's real pointer restoration and literal
# symlinks. The intercepted historical evaluator only observes its input view;
# no historical mathematical checker is executed or claimed to have passed.
F=OUT/'history_fixture';F.mkdir()
for name,row in routes.items():
    for target,source in [(F/name,R/name),(F/row['path'],R/row['path'])]:
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
(F/AUD/'history_routes.json').write_text(json.dumps(dict(baseline_commit=BASE,routes=routes)))
for row in links:
    p=F/row['path'];p.parent.mkdir(parents=True,exist_ok=True);p.symlink_to(row['target'])
history=module('independent_science89_history',R/'scripts/check_science89_history.py');observed=[]
def fake_spec(name,path):
    need(path.read_bytes()==(R/routes['scripts/verify_snapshot.py']['path']).read_bytes(),'exact archived evaluator supplied')
    return types.SimpleNamespace(loader=types.SimpleNamespace(exec_module=lambda m:None))
def fake_module(s):
    m=types.SimpleNamespace()
    def previous():
        for name,row in routes.items():need((m.ROOT/name).read_bytes()==(R/row['path']).read_bytes(),'restored historical route '+name)
        for row in links:need((m.ROOT/row['path']).is_symlink()and os.readlink(m.ROOT/row['path'])==row['target'],'literal history symlink')
        observed.append('nine routes and two literal symlinks observed');return {'observer_only':True}
    m.check_previous_science88=previous
    m.check_science88=lambda:dict(counts=dict(corrected_recoveries=88,refuted=9,handled=97,mathematical_pending=8),observer_only=True)
    return m
history.importlib=types.SimpleNamespace(util=types.SimpleNamespace(spec_from_file_location=fake_spec,module_from_spec=fake_module))
history.verify(F);need(len(observed)==1,'actual history wrapper executed once')
bad=F/routes['README.rst']['path'];bad.write_bytes(bad.read_bytes()+b'\nchanged')
try:history.verify(F)
except ValueError:observed.append('changed historic input rejected before view')
else:raise ValueError('damaged history accepted')

# Real final verification must refuse the gate-free candidate.
try:guard.verify(R,True)
except FileNotFoundError as exc:need(str(exc.filename).endswith('audit/science89/v1/root_integration.json'),'missing exact root gate');gate_rejected=True
else:raise ValueError('ungated candidate admitted')

report=dict(status='PASS_INDEPENDENT_SCIENCE89_REGISTRATION_AUDIT',
    handoff_files=len(handoff['files']),candidate_files=len(candidate['files']),
    installed_candidate_exact=True,git_baseline=BASE,git_paths=len(tree),
    baseline_mutable_paths_changed=changed,symlinks=links,only_changed_source=mutated,
    measured_entries_preserved=len(old['measured_original_ids']),old_functions=len(of)-1,
    main_call_coverage_preserved=True,extra_false_admissions=rejected,history_control=observed,
    historical_mathematics_executed=False,ungated_candidate_rejected=gate_rejected,
    native_pdf=pin(R/'audit/protocol.pdf'),public_writes=False)
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n')
(OUT/'git_inventory.json').write_text(json.dumps(tree,indent=2)+'\n')
print(json.dumps(report))
