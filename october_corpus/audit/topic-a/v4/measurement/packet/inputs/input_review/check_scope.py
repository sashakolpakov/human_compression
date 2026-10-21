#!/usr/bin/env python3
"""Independent policy/whole-file audit. No author validator imports."""
from pathlib import Path
from collections import Counter
import copy,hashlib,json
from recount import require,metric,digest

PRECOUNT='045ede7fd4e71149354f5c6d8c6f52fe71cac3cfde599a7d69474b145829ab02'
SOURCES=['L032','L034','F016','F013','L035','N009','L128','L012','L121']
REQUIRED={'cubic/certificate.py','cubic/kernel_certificate.g','square/certificate.py','square/kernel_certificate.g','finite/countermodel.py','finite/exact_groups.g','finite/finite_models.py','finite/model_data.json','cubic_relation/check.py'}
RUNNERS={'cubic/check.py','square/check.py','finite/check.py','check.py'}
FORMAL={'finite/formal/SectionFive.lean','finite/formal/dependency_manifest.json'}

def load(p):return json.loads(p.read_text())
def actual(row,roots):
 p=roots[row['root']]/row['path'];b=p.read_bytes();require(len(b)==row['bytes']and digest(b)==row['sha256'],'actual whole file '+row['path']);return p,b

def semantic(policy,docs,inventory,acquisition,scope):
 require(policy['source_ids']==SOURCES,'all nine originals')
 require(policy['application_documents']==['A'+str(i)for i in range(1,10)]and policy['common_documents']==['U'],'whole common and nine apps')
 require(policy['pdf_documents']==22 and policy['physical_pages']==240,'complete physical boundary')
 require(policy['source_pages']==131 and policy['common_pages']==23 and policy['application_pages']==56 and policy['program_appendix_pages']==30,'complete page roles')
 require(policy['required_complete_files']==20 and policy['raw_files']==45,'full mathematical program/data boundary')
 require(policy['auxiliary_scripts']==3 and policy['current_operational_drivers']==6 and policy['partial_formal_modules']==15 and policy['partial_formal_dependency_manifests']==1,'all operational/formal scopes')
 require(policy['ratios']is None and policy['symmetric_software_factors']is None,'no premature or asymmetric factors')
 require(all(v is None for v in policy['unknown_costs'].values())and scope['source_software_cost']is None,'unknown costs null')
 require(scope['full_Lean']is False and acquisition['full_Lean']is False,'partial formal scope')
 require(scope['accepted_source_rows']==27 and scope['new_question_credit']==0,'source clauses not original/question credits')
 require(policy['no_sibling_application_premise_for_L121']and not acquisition['sibling_application_premise']and acquisition['common_acquired_in_full'],'full U acquired without sibling')
 require('No complete enlarged printed appendix exists' in policy['printed_program_scope'],'old appendix is not enlarged closure')
 rows=docs['documents'];require(len(rows)==22 and len({r['id']for r in rows})==22,'22 unique documents')
 require({r['id']for r in rows}==set(SOURCES+['U']+['A'+str(i)for i in range(1,10)]+['CODE_A','CODE_AFFINE','CODE_DIAGRAM']),'exact document set')
 require(all(r['whole_document']for r in rows)and sum(r['pages']for r in rows)==240,'whole pages')
 require({r['id']:r['pages']for r in rows if r['id']in('L121','A9','U')}==dict(L121=12,A9=11,U=23),'new source/application/full U')
 files=inventory['files'];require(len(files)==45 and len({r['id']for r in files})==45 and len({r['file']['sha256']for r in files})==45,'45 complete unique contents')
 require(all(r['whole_file']for r in files),'no fragment charge')
 new=[r for r in files if r['id'].startswith('L121_')];require(len(new)==15,'new whole file closure')
 prefix='topic_A_L121_application/'
 relative={r['file']['path'].removeprefix(prefix):r for r in new}
 require(set(relative)==REQUIRED|RUNNERS|FORMAL,'actual exact new file routes')
 for name,r in relative.items():
  wanted='required_data'if name.endswith('model_data.json')else'required_program'if name in REQUIRED else'operational_validation_runner'if name in RUNNERS else'partial_formal_module'if name.endswith('.lean')else'partial_formal_dependency_manifest'
  require(r['role']==wanted,'actual role '+name);require(r['mathematical_premise']==(name in REQUIRED),'premise role '+name)
 require(set(acquisition['required_new_file_ids'])=={relative[n]['id']for n in REQUIRED},'all nine acquired mathematical files')
 require(acquisition['required_old_file_ids']==['P%02d'%i for i in range(1,12)],'all old required files retained')
 require(policy['inherited_PDF_metric_cells']==600 and policy['inherited_raw_metric_cells']==300 and policy['expected_new_PDF_metric_cells']==60 and policy['expected_new_raw_metric_cells']==150,'metric coordinate boundary')
 return True

def controls(p,d,i,a,s):
 base=[p,d,i,a,s];result=[]
 def test(name,mutate):
  x=copy.deepcopy(base);mutate(x)
  try:semantic(*x)
  except (ValueError,KeyError,TypeError)as e:result.append(dict(name=name,status='REJECTED',reason=str(e)));return
  raise ValueError('Accepted control: '+name)
 test('omit full common',lambda x:x[0].update(common_documents=[]))
 test('omit inherited application',lambda x:x[0]['application_documents'].remove('A8'))
 test('drop original source',lambda x:x[0]['source_ids'].remove('L121'))
 test('truncate new source pages',lambda x:next(r for r in x[1]['documents']if r['id']=='L121').update(pages=11))
 test('truncate complete application',lambda x:next(r for r in x[1]['documents']if r['id']=='A9').update(whole_document=False))
 test('claim enlarged printed code',lambda x:x[0].update(printed_program_scope='complete enlarged printed appendix'))
 test('assign unknown source code zero',lambda x:x[4].update(source_software_cost=0))
 test('assign unknown graphics zero',lambda x:x[0]['unknown_costs'].update(full_graphical_structure=0))
 test('claim end to end formalization',lambda x:x[4].update(full_Lean=True))
 test('charge an asymmetric software ratio',lambda x:x[0].update(symmetric_software_factors=1.0))
 test('missing required data',lambda x:x[2]['files'].remove(next(r for r in x[2]['files']if r['role']=='required_data')))
 test('demote required relation checker',lambda x:next(r for r in x[2]['files']if r['file']['path'].endswith('cubic_relation/check.py')).update(mathematical_premise=False))
 test('promote top operational driver',lambda x:next(r for r in x[2]['files']if r['id']=='L121_FILE15').update(role='required_program',mathematical_premise=True))
 test('omit required acquisition',lambda x:x[3]['required_new_file_ids'].pop())
 test('give A9 free sibling application',lambda x:x[3].update(sibling_application_premise=True))
 test('turn 27 clauses into question credit',lambda x:x[4].update(new_question_credit=27))
 test('drop inherited metrics',lambda x:x[0].update(inherited_PDF_metric_cells=570))
 return result

def run(packet,roots):
 pre=packet/'precount';require(digest((pre/'manifest.json').read_bytes())==PRECOUNT,'fixed policy predates measurement')
 for row in load(pre/'manifest.json')['exports']:
  b=(pre/row['path']).read_bytes();require(len(b)==row['bytes']and digest(b)==row['sha256'],'precount immutable export')
 p=load(pre/'policy.json');d=load(pre/'documents.json');i=load(pre/'raw_inventory.json');a=load(pre/'acquisition_routes.json');s=load(pre/'source_scope.json');semantic(p,d,i,a,s)
 bindings=load(pre/'bindings.json')
 for row in bindings['references']:actual(row,roots)
 for row in bindings['baseline_copy_files']:
  b=(pre/row['path']).read_bytes();require(len(b)==row['bytes']and digest(b)==row['sha256'],'literal baseline copy')
 baseline=load(pre/'baseline/author_counts.json');oldraw=load(pre/'baseline/raw_inventory.json');oldspec=load(roots['public']/'audit/topic-a/v3/measurement/packet/inputs/input/input_spec.json')
 for row in d['documents']:
  actual(row['file'],roots)
  if row['id']in oldspec:
   require(row['file']['sha256']==oldspec[row['id']]['file']['sha256'],'unchanged old PDF')
 byid={r['id']:r for r in oldraw}
 raw={}
 for row in i['files']:
  path,b=actual(row['file'],roots);m={n:metric(b.decode(),n)for n in('NFC','NFKC')};raw[row['id']]=dict(role=row['role'],metrics=m)
  if row['id']in byid:
   require(row['inherited_record']==byid[row['id']],'unchanged old raw role/coverage')
   for n in m:
    want=baseline['raw_files_measured'][row['id']]['metrics'][n]
    require({k:m[n][k]for k in want}==want,'independent old raw recount')
 return dict(status='PASS_INDEPENDENT_WHOLE_INPUT_SCOPE',PDFs=22,pages=240,raw_files=45,new_raw_files=15,raw_cells_independently_counted=450,old_PDF_cells_preserved_by_literal_binding=600,complete_required_files=20,full_new_printed_program_representation=None,software_factors=None,controls=controls(p,d,i,a,s),raw_counts=raw)
