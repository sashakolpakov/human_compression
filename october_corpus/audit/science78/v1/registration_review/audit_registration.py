"""Distinct registration checks; never writes to the public repository."""
from pathlib import Path
import ast, copy, hashlib, importlib.util, json, subprocess, sys
if sys.flags.optimize: raise RuntimeError('optimized reviewer checks forbidden')
R=Path('/Users/sasha/medusa/math_compression')
W=Path(__file__).resolve().parent
def need(x,m):
    if not x: raise RuntimeError(m)
def load(p): return json.loads((R/p).read_text())
def pin(p):
    b=p.read_bytes(); return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
history=load('audit/science78/v1/history_routes.json');routes=history['routes']
def git(*args): return subprocess.check_output(['git',*args],cwd=R)
need(git('rev-parse','HEAD').decode().strip()==history['baseline_commit'],'exact baseline commit')
changed=set(git('diff','--name-only','HEAD').decode().splitlines())
need(changed==set(routes),'exact eight changed historical pointers/documents')
for name,row in routes.items():
    raw=git('show',history['baseline_commit']+':'+name)
    need(raw==(R/row['path']).read_bytes(),'historical bytes differ from Git: '+name)
newpaths=git('ls-files','--others','--exclude-standard').decode().splitlines()
prefixes=['audit/recoveries/L059/v1/','papers/recoveries/L059/v1/','audit/science78/v1/']
singles={'scripts/check_science78.py','scripts/check_science78_history.py','audit/corpus/accessible106/updates/corrected-unmeasured78-catalogue.json','audit/corpus/updates/accessible106-corrected-unmeasured78.json'}
need(all(n in singles or any(n.startswith(p)for p in prefixes)for n in newpaths),'unrelated new public file')
need(not any(n.endswith('.md')for n in newpaths),'new public Markdown')
c=load('audit/corpus/latest.json');old=load(routes['audit/corpus/latest.json']['path'])
cat=load(c['active_catalogue']['path']);oldcat=load(old['active_catalogue']['path'])
allowed={'accessible_pending_complete_recovery','admitted_principal_originals','measurement_pending_original_ids','handled_mathematical_original_ids','status','entries','review_revision','handled_mathematical_originals','previous_catalogue','current_recovery_counts'}
need(set(cat)==set(oldcat),'catalogue schema')
need(all(cat[k]==oldcat[k]for k in set(cat)-allowed),'unrelated catalogue property')
need(len(cat['entries'])==106 and sum(a!=b for a,b in zip(cat['entries'],oldcat['entries']))==1,'exactly one original changed')
need([a['original_id']for a,b in zip(cat['entries'],oldcat['entries'])if a!=b]==['L059'],'only L059 changed')
need(cat['previous_catalogue']==old['active_catalogue'],'historical catalogue route')
native=load('papers/catalogue_corrected_unmeasured.json');oldnative=load(routes['papers/catalogue_corrected_unmeasured.json']['path'])
need(all(native[k]==oldnative[k]for k in set(oldnative)-{'original_ids','root_publication_gate','entries'}),'unrelated native catalogue data')
need(native['root_publication_gate']=='audit/science78/v1/root_integration.json','native gate route')
spec=importlib.util.spec_from_file_location('new_gate',R/'scripts/check_science78.py');gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
a=load('audit/recoveries/L059/v1/admission.json');scope=load('audit/recoveries/L059/v1/scope_routes.json')
controls=[]
mutations=[('change measured original list',lambda c,a,s:c['measured_original_ids'].append('L059')),
 ('close final question',lambda c,a,s:a['open_questions'].update(final_problem='proved')),
 ('close arxiv question',lambda c,a,s:a['open_questions'].update(arxiv_only='proved')),
 ('erase 2014 subdivision results',lambda c,a,s:a['counts'].update(subdivisions=[0,0])),
 ('count corrected scope as literal source equivalence',lambda c,a,s:a.update(all_original_assertions_claimed=True)),
 ('promote L046 prematurely',lambda c,a,s:c['accessible_pending_original_ids'].remove('L046')),
 ('add private fallback',lambda c,a,s:a.update(private_runtime_fallback=True)),
 ('erase external proof component',lambda c,a,s:a['complete_acquired_proofs'].pop('subdivision_actions'))]
for label,change in mutations:
    cc,aa,ss=copy.deepcopy((c,a,scope));change(cc,aa,ss)
    try:gate.semantics(cc,old,aa,ss)
    except (ValueError,KeyError):controls.append(label)
    else:raise RuntimeError('damaged scope accepted: '+label)
def main_node(s):
    return next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef)and n.name=='main')
oldtext=(R/routes['scripts/verify_snapshot.py']['path']).read_text()
replacements={
 '    L046_history = check_L046_previous()':'    science78_history = check_previous_science78()\n    L046_history = science78_history[\'previous\']',
 '    science72 = L046_history[\'science77\']':'    science72 = check_science78()',
 '    L046_correction = check_L046_current()':'    L046_correction = science78_history[\'correction\']',
 "    print('PASS: L046 bounded count correction; all original dispositions unchanged and 116 exact cells still pending.')":"    print('PASS: historical L046 bounded correction preserved; L059 complete corrected principal recovery adds one original.')"}
for before,after in replacements.items():
    need(oldtext.count(before)==1,'unique main edit');oldtext=oldtext.replace(before,after)
need(ast.dump(main_node(oldtext))==ast.dump(main_node((R/'scripts/verify_snapshot.py').read_text())),'exact reviewed main routing')
bindings=[pin(R/n)for n in sorted(changed|set(newpaths))]
(W/'candidate_bindings.json').write_text(json.dumps(bindings,indent=2)+'\n')
report=dict(status='PASS_DISTINCT_L059_REGISTRATION_AUDIT',baseline=history['baseline_commit'],old_tracked_changed=len(changed),new_public_files=len(newpaths),candidate_files_rehashed=len(bindings),unchanged_original_rows=105,independent_damage_controls=controls,main_change='exact four reviewed routing substitutions',public_edits=False)
(W/'audit_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
