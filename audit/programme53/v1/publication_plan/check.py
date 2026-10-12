#!/usr/bin/env python3
"""Bounded publication-map check; no proof, extraction, GAP or Lean execution."""
from pathlib import Path
from copy import deepcopy
import argparse,ast,hashlib,json,re
from pypdf import PdfReader
H=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text())
def need(v,m):
 if not v:raise ValueError('A10_PUBLICATION: '+m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(p,r):need(p.is_file()and p.stat().st_size==r['bytes']and sha(p)==r['sha256'],'exact '+str(p))
def semantic(corpus,active,topic,registration,rows,raw):
 need((corpus['originals'],corpus['currently_measured_originals'],corpus['accessible_pending_complete_recovery'],corpus['editorial_originals'],corpus['archived_unavailable_originals'])==(106,53,52,1,55),'53/52/1/55 partition')
 a=corpus['measured_original_ids'];b=corpus['accessible_pending_original_ids'];e=corpus['editorial_original_ids'];need(len(a)==len(set(a))==53 and len(b)==len(set(b))==52 and e==['L022']and not(set(a)&set(b)or set(a)&set(e)or set(b)&set(e))and set(a+b+e)==set(corpus['active_original_ids']),'unique complete active partition')
 need('L003'in a and all(x in b for x in ['L044','L096']),'only accepted new scope')
 need(registration['source_ids']==['L003']and registration['all_ten_topic_ids_registered_again']is False,'only L003 new registration')
 need(topic['source_ids']==['L032','L034','F016','F013','L035','N009','L128','L012','L121','L003']and topic['whole_common_pages']==[23,14,4]and topic['whole_application_pages']==63,'whole common3 and10 applications')
 need((topic['source_sum'],topic['whole_common'],topic['application_sum'],topic['whole_written'])==(319016,108271,155199,263470),'accepted exact costs')
 need(topic['exact_fractions']==330 and topic['old_conditionals_preserved']==240,'complete numerical family')
 need(topic['software_inclusive_factor']is None and topic['whole_source_formalized']is False and topic['new_question_credit']==topic['new_Lean_declarations']==0,'no scalar or unsupported credit')
 need(len(rows)==16 and sum(r['physical_pages']for r in rows)==104,'16 whole native PDFs104pages')
 need([r['physical_pages']for r in rows if r['application_id'].startswith('U')]==[23,14,4],'whole common physical boundary')
 need([r['physical_pages']for r in rows if r['application_id'].startswith('A10')]==[7,4,4,2],'whole L003 companions')
 need(next(r['physical_pages']for r in rows if r['application_id']=='A9')==1,'complete changed L121 adapter')
 need({r['compiler']for r in rows[9:]}=={'xelatex','pdflatex'},'retain actual engines')
 need(len(raw['contents'])==203 and len(raw['occurrences'])==253 and sum(r['mathematical_premise']for r in raw['contents'])==99,'full raw closure')
 need(raw['accounting_class_counts']=={'required_program':28,'required_data':71,'operational':17,'optional_validation':5,'partial_formal':16,'output_receipt':66},'explicit disjoint classes')
 need(raw['roles_overlap']and raw['classes_disjoint']and raw['software_inclusive_factor']is None,'no overlap doublecharge')
 entries={r['original_id']:r for r in active['entries']};need(entries['L003']['current_principal_recovery']['status']=='ADMITTED_AND_MEASURED'and entries['L003']['current_principal_recovery']['source_dispositions']==125,'current corrected original status')
 need(entries['L003']['current_principal_recovery']['source_table_rows']==73 and not entries['L003']['current_principal_recovery']['whole_source_formalized'],'complete corrected table scope')
 need(entries['L121']['current_measurement_extension']['application_pages']==1,'current L121 routing')
 return True

def verify(study,repo,staged=None):
 study=Path(study);repo=Path(repo);stage=Path(staged)if staged else None
 if(H/'manifest.json').exists():
  for r in load(H/'manifest.json')['exports']:bind(H/r['path'],r)
 base=load(H/'baseline.json');plan=load(H/'copy_plan.json');rows=load(H/'catalogue_additions.json')['entries'];wr=load(H/'wrapper_routes.json')['files'];raw=load(H/'raw_routes.json')
 for r in plan['files']:bind((stage/r['public_path'])if stage else(study/r['study_path']),r)
 for r in load(H/'reused_science.json')['files']:bind(repo/r['path'],r)
 for r in load(H/'recount_retained_public.json')['files']:bind(repo/r['path'],r)
 for r in wr:bind((stage/r['public_path'])if stage else(H/r['proposal_path']),r)
 funcs={n.name:hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest()for n in ast.parse((repo/'scripts/verify_snapshot.py').read_text()).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))and n.name!='main'}
 need(all(funcs.get(k)==v for k,v in base['prior_nonmain_ASTs'].items())and len(base['prior_nonmain_ASTs'])==133,'133 prior ASTs preserved')
 # Current wrapper files are checked either in the explicit stage or in this private proposal.
 R=stage if stage else H/'wrappers'
 corpus=load(R/'audit/corpus/latest.json');topic=load(R/'audit/topic-a/v5/admission.json');registration=load(R/'audit/programme53/v1/new_original_registration.json');active=load(R/corpus['active_catalogue']['path'])
 for x in [corpus['active_catalogue'],corpus['snapshot']]:bind(R/x['path'],x)
 semantic(corpus,active,topic,registration,rows,raw)
 before=load(H/'baseline/audit/corpus/latest.json');need(set(corpus['measured_original_ids'])-set(before['measured_original_ids'])=={'L003'}and set(before['accessible_pending_original_ids'])-set(corpus['accessible_pending_original_ids'])=={'L003'},'one original moves partition')
 prioractive=load(H/'baseline'/before['active_catalogue']['path']);ea={x['original_id']:x for x in active['entries']};pa={x['original_id']:x for x in prioractive['entries']};changed={k for k in ea if ea[k]!=pa[k]};need(changed==set(topic['source_ids'])and all(ea[k]==pa[k]for k in ea if k not in changed),'10 routed records96 exact')
 for k in ['added_admissions','added_measurements']:need(corpus[k][:-1]==before[k]and corpus[k][-1]['path']=='audit/programme53/v1/new_original_registration.json','no duplicate source admission list')
 need(corpus['current_topic_replacements'][:-1]==before['current_topic_replacements'],'old topic registrations unchanged')
 for n in ['papers/topic-a/latest.json','papers/topic-affine/latest.json','papers/latest_catalogue.json','audit/overview/latest.json']:
  q=load(R/n)
  if n.endswith('topic-affine/latest.json'):bind(R/q['current_topic_pointer']['path'],q['current_topic_pointer'])
  if n=='papers/latest_catalogue.json':bind(R/q['unified_A_current_edition']['current_topic_pointer']['path'],q['unified_A_current_edition']['current_topic_pointer'])
  if n=='audit/overview/latest.json':need(q['recovered_originals']==53 and q['current_conditional_factors']==53,'current overview53');bind(R/q['admission']['path'],q['admission'])
 # Every proposed raw route is an exact scientific copy or an exact retained public file.
 idx={r['public_path']:r for r in plan['files']};idx.update({r['path']:r for r in load(H/'reused_science.json')['files']})
 for x in raw['occurrences']:need(x['public_path']in idx and all(x[k]==idx[x['public_path']][k]for k in ['bytes','sha256']),'all253 actual whole routes')
 report=load(H/'reports/stage_report.json');need(report['render']['papers']==16 and report['render']['pages']==104,'fresh accepted-compiler build evidence')
 for x in rows:
  b=next(q for q in report['render']['checks']if q['id']==x['id']);need(b['pages']==x['physical_pages']and b['compiler']==x['compiler']and b['exact_page_text']and not b['diagnostics'],'exact whole render evidence')
  texpath=(stage/x['tex'])if stage else(study/next(z['study_path']for z in plan['files']if z['public_path']==x['tex'])if x['tex']in idx and 'study_path'in idx[x['tex']]else repo/x['tex'])
  title=re.search(r'\\title\{([^{}]+)\}',texpath.read_text()).group(1);need(title==x['title'],'literal full title '+x['id'])
 readme=(R/'README.rst').read_text();tex=(R/'audit/protocol.tex').read_text();need('53 accessible originals'in readme and'52 await mathematical recovery'in readme and'fifty-three individual'in readme and'first twenty-seven'in readme and'1.210825'in readme and'12.288729'in readme,'current concise README')
 need('106=53'in tex and'}+52\\'in tex and'overview v19'in tex and'all 41 common pages'in tex,'current protocol scope')
 controls=[]
 mutations=[('missing common',lambda x:x[2].update(whole_common_pages=[23,14])),('missing companion',lambda x:x[4].pop()),('old L121 pages',lambda x:next(r for r in x[4]if r['application_id']=='A9').update(physical_pages=11)),('source IDs double registration',lambda x:x[3].update(source_ids=x[2]['source_ids'])),('unaccepted L044 credit',lambda x:x[0]['measured_original_ids'].append('L044')),('editorial counted',lambda x:x[0]['measured_original_ids'].append('L022')),('wrong pending',lambda x:x[0].update(accessible_pending_complete_recovery=51)),('lost required data',lambda x:x[5]['contents'].pop()),('demote required to output',lambda x:next(r for r in x[5]['contents']if r['mathematical_premise']).update(mathematical_premise=False)),('software ratio',lambda x:x[2].update(software_inclusive_factor=1)),('full Lean',lambda x:x[2].update(whole_source_formalized=True)),('new conjecture credit',lambda x:x[2].update(new_question_credit=1)),('wrong primary total',lambda x:x[2].update(whole_written=1)),('obsolete literal-source scope',lambda x:next(r for r in x[1]['entries']if r['original_id']=='L003')['current_principal_recovery'].update(source_dispositions=117))]
 for name,fn in mutations:
  z=deepcopy([corpus,active,topic,registration,rows,raw]);fn(z)
  try:semantic(*z)
  except(ValueError,KeyError,StopIteration):controls.append(name)
  else:raise ValueError('mutation survived '+name)
 return dict(status='PASS_PRIVATE_EXACT_A10_PUBLICATION_PROPOSAL',payload_files=len(plan['files']),packets=len(plan['packets']),wrapper_files=len(wr),retained_public_files=len(load(H/'reused_science.json')['files']),native_scientific_documents=16,native_pages=104,whole_contents=203,occurrences=253,required_contents=99,preserved_prior_nonmain_ASTs=133,changed_catalogue_records=10,unchanged_catalogue_records=96,counts=dict(active=106,measured=53,mathematical_pending=52,editorial=1,archived=55,topics=19),controls=controls,scientific_or_input_execution=False,root_publication_review_required=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);p.add_argument('--staged-root',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();q=verify(a.study_root,a.repo,a.staged_root);a.out.mkdir(parents=True,exist_ok=True);(a.out/'report.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q,indent=2))
