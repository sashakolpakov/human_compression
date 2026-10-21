#!/usr/bin/env python3
"""Create an exact publication proposal, never mutate public or frozen inputs."""
from pathlib import Path
import hashlib,json,csv,subprocess
S=Path('/Users/sasha/medusa/research/leemans'); P=Path('/Users/sasha/medusa/math_compression'); HERE=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def save(n,x):(HERE/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def bind(p):return dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size)
def items(m):
 e=m['exports'];return [dict(v,path=k) for k,v in e.items()] if isinstance(e,dict) else e
rows={};packets=[];study={};public_files=[p for p in P.rglob('*') if p.is_file() and '.git' not in p.parts]

def add(p,dest,action,role,packet=None):
 p=p.resolve();r=dict(source=str(p),destination=dest,sha256=sha(p),bytes=p.stat().st_size,action=action,role=role,packets=[])
 if packet:r['packets']=[packet]
 if dest in rows:
  assert rows[dest]['sha256']==r['sha256']
  rows[dest]['packets']=sorted(set(rows[dest]['packets']+r['packets']))
 else:rows[dest]=r
 if p.is_relative_to(S):study[str(p.relative_to(S))]=dict(public_path=dest,sha256=r['sha256'],bytes=r['bytes'],purpose=role)
 return r

def packet(name,src,dest,action,role,required=True):
 root=Path(src);mf=root/'manifest.json';m=load(mf);rr=items(m)
 for r in rr:
  p=root/r['path'];assert sha(p)==r['sha256'] and p.stat().st_size==r['bytes'];assert not p.is_symlink()
  add(p,str(Path(dest)/r['path']),action,role,name)
 add(mf,str(Path(dest)/'manifest.json'),action,role,name)
 packets.append(dict(id=name,source=str(root),destination=dest,action=action,role=role,required_for_current_replay=required,manifest=bind(mf),exports=len(rr),export_bytes=sum(x['bytes'] for x in rr),copy_rule='exact manifest plus every declared export; exclude all unlisted local files'))

# Current whole scientific/review/input editions. All complete packets are pinned.
for name,d,dest,role in [
 ('integrated','corpus161_N005_integrated','papers/topic-operations/v1/integrated','current_science_and_complete_programs'),
 ('citations','topic_Operations_sibling_citations_v1','papers/topic-operations/v1/citations','current_science_citation_editions'),
 ('integrated_review','corpus161_N005_integrated_root_review','audit/topic-operations/v1/integrated_review','distinct_migration_acceptance_and_complete_precursors_for_review'),
 ('citation_review','topic_Operations_sibling_citations_root_review','audit/topic-operations/v1/citation_review','distinct_citation_acceptance'),
 ('boundary','topic_Operations_input_contract_v1','audit/topic-operations/v1/boundary','complete_dependency_and_citation_proposal_history'),
 ('inputs','topic_Operations_measurement_inputs_v1','audit/topic-operations/v1/measurement/inputs','accepted_measurement_inputs_with_historical_author_status'),
 ('input_review','topic_Operations_inputs_root_review','audit/topic-operations/v1/measurement/input_review','distinct_complete_input_acceptance'),
 ('author_replay','corpus161_N005_integrated_author_replay','audit/topic-operations/v1/author_replay','author_replay_provenance_not_independent_acceptance'),
 ('adapter_review','corpus161_N005_adapters_root_review','audit/topic-operations/v1/precursor_reviews/adapters','accepted_precursor_proof_and_finite_certificate_review')]:packet(name,S/d,dest,'copy_exact',role)
# Original early reviews are historical provenance, not new logical premises.
for name,d in [('tree_review','corpus161_N005_independent_review'),('hnn_review','corpus161_N005_HNN_independent_review'),('three_notes_review','corpus161_N005_three_notes_independent_review')]:
 packet(name,S/d,'audit/topic-operations/v1/precursor_reviews/'+name,'copy_exact_recommended','historical_proof_review_provenance',False)
for name,rel,role in [
 ('existing_N007','papers/topic-diagonal/v1','retained_current_N007_validation_and_old_citation_baseline'),
 ('existing_N006','papers/topic-diagonal/v2','retained_current_N006_companions_programs_formal_and_old_citation_baseline'),
 ('old_inputs','audit/diagonal-measurement/v2/packet/inputs','byte_identical_prior_input_evidence'),
 ('old_input_review','audit/diagonal-measurement/v2/packet/input_review','prior_input_acceptance'),
 ('old_numerical','audit/diagonal-measurement/v2/packet','historical_two_original_numerical_provenance_only'),
 ('old_numerical_review','audit/diagonal-measurement/v2/independent_review','historical_two_original_numerical_acceptance_only'),
 ('nonfirm_review','corrections/nonfirm-hnn/v1/independent_review','accepted_separate_literal_correction_provenance'),
 ('twist_review','corrections/affine-twist/v1/independent_review','accepted_separate_literal_correction_provenance')]:packet(name,P/rel,rel,'reuse_exact_existing_public',role,name not in ['old_numerical','old_numerical_review','nonfirm_review','twist_review'])

policy=load(S/'topic_Operations_measurement_inputs_v1/policy.json');sw=load(S/'topic_Operations_measurement_inputs_v1/software_inventory.json')

def mapped(p,role='exact_bound_dependency'):
 p=Path(p)
 if p.is_relative_to(P):return add(p,str(p.relative_to(P)),'reuse_exact_existing_public',role)['destination']
 if p.is_relative_to(S) and str(p.relative_to(S)) in study:return study[str(p.relative_to(S))]['public_path']
 # Earlier unchanged program copies alias current files; no duplicate program charge.
 aliases=[r for r in rows.values() if r['sha256']==sha(p) and r['bytes']==p.stat().st_size]
 if aliases:
  r=sorted(aliases,key=lambda x:('papers/topic-operations' not in x['destination'],len(x['destination'])))[0]
 else:
  matches=[q for q in public_files if q.stat().st_size==p.stat().st_size and sha(q)==sha(p)]
  assert matches,'unmapped exact dependency '+str(p)
  q=sorted(matches,key=lambda x:len(str(x)))[0];r=add(q,str(q.relative_to(P)),'reuse_exact_existing_public',role)
 if p.is_relative_to(S):study[str(p.relative_to(S))]=dict(public_path=r['destination'],sha256=sha(p),bytes=p.stat().st_size,purpose=role)
 return r['destination']

sources=[]
for k,r in policy['sources'].items():sources.append(dict(id=k,study_path=r['path'],sha256=r['sha256'],bytes=r['bytes'],pages=r['pages'],publication_action='never_export_user_supplied_primary',role='exact_original_for_source_and_measurement_replay'))
for r in policy['scientific_bindings']:mapped((S if r['root']=='sources' else P)/r['path'])
# Every literal absolute binding that the frozen boundary checker actually traverses.
source_names={str(S/r['path']) for r in policy['sources'].values()}
def walk(x):
 if isinstance(x,dict):
  yield x
  for y in x.values():yield from walk(y)
 elif isinstance(x,list):
  for y in x:yield from walk(y)
for n in ['contract','software_inventory','programme_representations','external_data','retained_inputs','source_qualifications','common_correspondence','citation_proposals','evidence_map']:
 for r in walk(load(S/('topic_Operations_input_contract_v1/'+n+'.json'))):
  q=r.get('path')
  if isinstance(q,str) and q.startswith('/') and isinstance(r.get('sha256'),str) and len(r['sha256'])==64 and q not in source_names and (q.startswith(str(S)) or q.startswith(str(P))):mapped(q,'frozen_boundary_checker_binding_or_historical_alias')
# Precise software file ownership and validation/formal separation.
software={}
for cat in ['programs','required_input_drivers','operational_drivers','formal_files']:
 software[cat]=[dict(r,public_path=mapped(r['path'],'whole_'+cat)) for r in sw[cat]]
software.update({k:sw[k] for k in ['direct_program_edges','application_roots','aliases_not_double_charged','unique_partial_formal_declarations','new_N005_formal_declarations','representation_rule']})
# Exact current catalogue and all complete TeX inputs.
docs=[]
for r in load(S/'corpus161_N005_integrated/documents.json')['documents']:
 base=S/'corpus161_N005_integrated';docs.append(dict(r,tex=mapped(base/r['tex']),pdf=mapped(base/r['pdf']),tex_inputs=[mapped(base/f) for f in r['tex_inputs']],scientific_current=r['role']=='scientific_paper'))
for key,name,stem in [('A1','N007','diagonal-twistings'),('A2','N006','wreath_applications')]:
 base=S/'topic_Operations_sibling_citations_v1'/name;r=policy['replacements'][key]
 docs.append(dict(id=name+'.current_application',title=stem.replace('-',' ').replace('_',' '),tex=mapped(base/(stem+'.tex')),pdf=mapped(base/(stem+'.pdf')),tex_inputs=[mapped(base/(stem+'.tex')),mapped(base/'preamble.tex')],pages=r['pages'],role='scientific_paper',scientific_current=True))
for name,base,stem,key in [('N006.nine',P/'papers/topic-diagonal/v2/papers/sporadic','sporadic_certificates','A2nine'),('N006.HN',P/'papers/topic-diagonal/v2/papers/harada-norton','harada_norton','A2HN')]:
 docs.append(dict(id=name,title=stem.replace('_',' '),tex=mapped(base/(stem+'.tex')),pdf=mapped(base/(stem+'.pdf')),tex_inputs=[mapped(base/(stem+'.tex'))],pages=policy['replacements'][key]['pages'],role='scientific_companion',scientific_current=True))
docs.append(dict(id='N007.programs',title='Complete finite validation program',tex=mapped(P/'papers/topic-diagonal/v1/programs.tex'),pdf=mapped(P/'papers/topic-diagonal/v1/programs.pdf'),tex_inputs=[mapped(P/'papers/topic-diagonal/v1'/r) for r in ['programs.tex','preamble.tex','programs/diagonal_models.g']],pages=2,role='partial_printed_program_alternative',scientific_current=False))
pdfmap={k:dict(r,public_path=mapped((S if r['root']=='sources' else P)/r['path'])) for k,r in policy['replacements'].items()}
contracts=[]
for k,r in load(S/'topic_Operations_input_contract_v1/source_qualifications.json')['contracts'].items():contracts.append(dict(id=k,records=policy['source_rows'][k],public_path=mapped(r['path']),sha256=r['sha256'],bytes=r['bytes']))
plan=dict(format='operations-publication-plan-v1',status='PRIVATE_EXACT_MAPPING_PROPOSAL_NOT_PUBLIC_ADMISSION',author_role='enumeration_volume authored the integrated science, citations, input proposal and this routing plan; this is not a distinct scientific or input acceptance.',public_baseline=subprocess.check_output(['git','rev-parse','HEAD'],cwd=P,text=True).strip(),destinations_provisional=True,public_changes_made=False,ratios_computed=False,source_credit_change=0,question_credit_change=0,packets=packets,artifacts=sorted(rows.values(),key=lambda r:r['destination']),study_aliases=study,source_inputs=sources,current_pdfs=pdfmap,source_contracts=contracts,counts=dict(originals=3,source_records=140,current_scientific_documents=6,current_scientific_pages=61,audit_documents=11,audit_pages=161,whole_program_files=23,required_programs=17,validation_programs=6,required_input_drivers=2,operational_drivers=5,unique_Lean_files=3,partial_Lean_declarations=17,new_N005_Lean_declarations=0),external_boundary=dict(required_representation_files=4,required_representation_bytes=21960689,installed_catalogue_algorithm_files=16,installed_catalogue_algorithm_bytes=2516249,full_classical_proof_cost=None,graphics_cost=None,external_redistribution=False),scientific_priorities=['The whole integrated common theory replaces earlier common editions for the current three-original topic; old common PDFs remain historical archives, not free current premises.','The N006 application is the complete 8+5+4 page bundle; the nine-case note alone omits HN.','The exact revised N006/N007 citation editions use reviewed common correspondences; all 18 theorem/proof environments are unchanged.','No unrestricted nonfirm HNN result, general Shephard Helly result, general finite-diagram question answer or Fischer-exception cost is silently imported.'],pending_before_publication=['Input proposal 3b0d503d is accepted at edb9e44f; numerical calculation/review is now authorized but not performed by this mapping packet.','Separate numerical calculation and independent arithmetic review, if science and numerical admission are combined.','Root publication adapter/current guide/admission and standard-verifier guard; current proposed routes are not installed.','Current guide must supersede historical pending labels without altering frozen author or prior admission bytes.'])
save('publication_map.json',plan);save('catalogue_proposal.json',dict(documents=docs,scientific_entries=6,printed_alternative_entries=2,catalogue_action='Change current routes or add precise companion routes without deleting archived editions. No new original count follows from extra document entries.'))
save('software_routes.json',software);save('external_and_retained.json',dict(retained=load(S/'topic_Operations_input_contract_v1/retained_inputs.json'),external=load(S/'topic_Operations_measurement_inputs_v1/external_data.json'),reader_requirement='All data and retained classification/normal-form costs remain explicit; full unknown proof and graphic costs are null, not zero. The 4 Atlas files and installed catalogue files are user-supplied, not copied by this plan.'))
with (HERE/'artifact_map.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['source','destination','sha256','bytes','action','role']);w.writeheader();w.writerows({k:r[k] for k in w.fieldnames} for r in plan['artifacts'])
print(json.dumps(dict(packets=len(packets),artifacts=len(rows),private_study_aliases=len(study),scientific_documents=6,ratio=None)))
