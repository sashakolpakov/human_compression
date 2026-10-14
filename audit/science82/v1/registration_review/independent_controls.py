import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
from pathlib import Path
import copy,hashlib,importlib.util,json,re,subprocess,os
R=Path('/Users/sasha/medusa/math_compression');O=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('science82_distinct',R/'scripts/check_science82.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def load(name):return json.loads((R/name).read_text())
c=load('audit/corpus/latest.json');h=load('audit/science82/v1/history_routes.json')['routes'];old=load(h['audit/corpus/latest.json']['path']);cat=load(c['active_catalogue']['path']);before=load(old['active_catalogue']['path'])
ids=[x['original_id']for x in cat['entries']];assert len(ids)==len(set(ids))==106
A=set(c['admitted_original_ids']);P=set(c['accessible_pending_original_ids']);F={'F003'};E={'L022'}
assert len(A)==82 and len(P)==22 and not A&P and not(A|P)&(F|E) and A|P|F|E==set(ids)
assert set(c['handled_mathematical_original_ids'])==A|F
assert set(c['measurement_pending_original_ids'])<=A and len(c['measurement_pending_original_ids'])==29
assert len(A-set(c['measurement_pending_original_ids']))==53
mutable={'status','admitted_principal_originals','accessible_pending_complete_recovery','handled_mathematical_originals','review_revision','previous_catalogue','current_recovery_counts','measurement_pending_original_ids','handled_mathematical_original_ids','entries'}
assert set(cat)==set(before)
assert all(cat[k]==before[k]for k in set(before)-mutable)
assert cat['previous_catalogue']==old['active_catalogue']
for key in ['measurement_pending_original_ids','handled_mathematical_original_ids']:
 assert cat[key]==sorted(before[key]+['L045'])
changed=[x['original_id']for x,y in zip(before['entries'],cat['entries'])if x!=y];assert changed==['L045']
native=load('papers/catalogue_corrected_unmeasured.json');prior=load(h['papers/catalogue_corrected_unmeasured.json']['path']);assert native['entries'][:-15]==prior['entries']
assert len({x['id']for x in native['entries']})==len(native['entries'])
new=native['entries'][-15:];assert sum(x['physical_pages']for x in new)==58
inputs={}
for row in new:
 tex=R/row['tex'];names=re.findall(r'\\(?:input|include|includegraphics)(?:\[[^\]]*\])?\{([^}]+)\}',tex.read_text());paths=[str((tex.parent/name).relative_to(R))for name in names];assert paths==row['tex_inputs'];assert all((R/p).is_file()for p in paths);inputs[row['id']]=paths
original=m.load
cases=[('principal refutation lost','audit/corpus/latest.json',lambda x:x['handled_mathematical_original_ids'].remove('F003')),('other original altered',c['active_catalogue']['path'],lambda x:x['entries'][0].update(original_id='CORRUPTED')),('L045 qualifications lost',c['active_catalogue']['path'],lambda x:next(e for e in x['entries']if e['original_id']=='L045')['current_principal_recovery'].update(source_qualifications=[])),('old native entry altered','papers/catalogue_corrected_unmeasured.json',lambda x:x['entries'][0].update(title='CORRUPTED')),('duplicate native original','papers/catalogue_corrected_unmeasured.json',lambda x:x['original_ids'].append('L045')),('native table input omitted','papers/catalogue_corrected_unmeasured.json',lambda x:next(e for e in x['entries']if e['id']=='L045-finite_lie-4').update(tex_inputs=[])),('wrong operational status','audit/science82/v1/operational_review.json',lambda x:x.update(status='PENDING'))]
controls=[]
for label,path,fn in cases:
 damaged=copy.deepcopy(load(path));fn(damaged)
 def mocked(root,name,path=path,damaged=damaged):return copy.deepcopy(damaged)if str(name)==path else original(root,name)
 m.load=mocked
 try:m.verify(R,False)
 except (ValueError,KeyError,AssertionError):controls.append(label)
 else:raise RuntimeError('Damaged decoded input accepted: '+label)
 finally:m.load=original
try:m.verify(R,True)
except FileNotFoundError as e:
 assert 'root_integration.json'in str(e);controls.append('pre-gate candidate cannot self-admit')
else:raise RuntimeError('Candidate admitted without root gate')
newraw=subprocess.check_output(['git','-C',str(R),'ls-files','--others','--exclude-standard','-z'])
all_newpaths=[x.decode()for x in newraw.split(b'\0')if x]
transient={'audit/protocol.aux','audit/protocol.log','audit/protocol.out'}
newpaths=[p for p in all_newpaths if p not in transient]
assert all(not p.endswith('.md')for p in newpaths)
allowed=['audit/recoveries/L045/','papers/recoveries/L045/','audit/science82/']
exact={'scripts/check_science82.py','scripts/check_science82_history.py','audit/corpus/accessible106/updates/corrected-unmeasured82-catalogue.json','audit/corpus/updates/accessible106-corrected-unmeasured82.json'}
assert all(p in exact or any(p.startswith(s)for s in allowed)for p in newpaths),[p for p in newpaths if p not in exact and not any(p.startswith(s)for s in allowed)]
report=dict(status='PASS_DISTINCT_REGISTRATION_CONTROLS',originals=106,only_changed_original=changed,counts=dict(recovered=82,refuted=1,handled=83,pending=22,measured=53,unmeasured=29,editorial=1),all_other_catalogue_top_fields_unchanged=True,native_manuscripts=15,native_pages=58,literal_inputs=inputs,independent_decoded_input_controls=controls,new_paths=len(newpaths),excluded_native_transients=sorted(set(all_newpaths)&transient),new_markdown=0,new_path_scope_exact=True,full_history_repeated=False,census_repeated=False,public_writes=False)
(O/'independent_report.json').write_text(json.dumps(report,indent=2)+'\n')
(O/'new_paths.json').write_text(json.dumps(newpaths,indent=2)+'\n');print(json.dumps(report))
