#!/usr/bin/env python3
"""Exact assembly/migration replay; no earlier group or formal calculation is rerun."""
from pathlib import Path
import argparse,collections,copy,hashlib,json,re,shutil,subprocess
HERE=Path(__file__).resolve().parent

def load(p):return json.loads(p.read_text())
def need(t,m):
 if not t:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def binding(p,e):need(p.is_file() and p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'binding '+str(p))
def envs(t):return [m.group(0) for m in re.finditer(r'\\begin\{(theorem|proposition|proof)\}[\s\S]*?\\end\{\1\}',t)]
def validate(scope,source,claims,bundles):
 need(scope['source_id']=='L003' and scope['source_pages']==21 and scope['predecessor_rows']==117 and scope['current_rows']==125 and scope['positive_rows']==73,'full source extent')
 rows=source['rows'];need(len(rows)==125 and len({r['id'] for r in rows})==125,'125 distinct dispositions')
 positive=[r for r in rows if r.get('kind')=='positive_table_row'];need(len(positive)==73,'all positive rows')
 states=collections.Counter(r['assembly_status'] for r in positive)
 need(states=={'STRUCTURE_ACCEPTED_DISTINCT_ROOT_REVIEW':35,'PREVIOUS_NAMED_IDENTIFICATION_ACCEPTED':29,'PRINTED_ORDER_REFUTED_CORRECTED_MODEL_ACCEPTED':2,'STRUCTURE_ACCEPTED_SEPARATELY':7},'entire structural partition')
 t48=next(r for r in positive if r['id']=='T4.8');need(t48['current_source_structure_status']=='corrected_nonsplit_shape' and t48['current_structure'][1][1][0]=='dot','actual corrected T4.8 stage')
 corr=[r for r in rows if r['id'].startswith('Section3_D')];need(len(corr)==9,'nine precise correlation clauses')
 need(next(r for r in corr if r['id']=='Section3_D5_geometry')['status']=='source explicitly experimental hypertope production; no flag-transitivity existence theorem claimed','experimental existence boundary')
 need(next(r for r in corr if r['id']=='Section3_D4_generators')['status']=='source three-letter facet list completed to four generators t,a,b,d for rank4','complete four-marker qualification')
 need(next(r for r in rows if r['id']=='Section9_genus4_example')['assembly_status']=='ISOLATED_ASSERTION_ACCEPTED_SEPARATELY','ancillary source assertion included')
 need(scope['whole_common_parts']==[23,14,4] and scope['L121_current_application_pages']==1 and scope['L003_complete_application_parts']==[7,4,4,2] and scope['unchanged_old_application_pages']==45,'entire written closure')
 need(scope['required_companions_complete'] is True and scope['software_inclusive_factor'] is None and scope['measurements'] is None and scope['whole_source_credit']==scope['new_question_credit']==scope['new_Lean']==0,'scope and no premature credit')
 need(scope['main_source_corrections'][:4]==['T5.8 full order5184000','T5.10 full order497664','12 ordinary local-period collapses','T8.11 literal final word not a torus period; actual localorder504/kernel determinant84'],'order and local-period corrections')
 need(len(claims['rows'])==117 and not any(r['principal_gap_after_accepted_inputs'] for r in claims['rows']),'accepted predecessor transfer complete')
 need([b['pages'] for b in bundles['bundles']]==[41,17] and [len(b['parts']) for b in bundles['bundles']]==[3,4],'complete bundle parts')
 return dict(predecessor_rows=117,current_rows=125,positive_rows=73,all42_structural_obligations_routed=True,common_pages=41,L121_adapter_pages=1,L003_application_pages=17)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--study-root',type=Path);ap.add_argument('--public-root',type=Path);ap.add_argument('--render',action='store_true');a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 if (HERE/'manifest.json').exists():
  for e in load(HERE/'manifest.json')['exports']:binding(HERE/e['path'],e)
 copies=load(HERE/'copy_routes.json')
 for e in copies:binding(HERE/e['destination'],e)
 for folder in ['base','shared_structures','finite_structures','correlations','order768']:
  p=HERE/'inputs'/folder
  for e in load(p/'manifest.json')['exports']:binding(p/e['path'],e)
 scope=load(HERE/'scope.json');source=load(HERE/'source_map.json');claims=load(HERE/'claim_map.json');bundles=load(HERE/'bundle_map.json');coverage=validate(scope,source,claims,bundles)
 base=HERE/'inputs/base';need(envs((base/'hexagonal_extensions.tex').read_text())==envs((HERE/'hexagonal_extensions.tex').read_text()),'all original theorem and proof environments')
 for f in ['finite_table.tex','local_corrections.tex']:need((base/f).read_bytes()==(HERE/f).read_bytes(),'unchanged finite/local table '+f)
 old=load(base/'source_map.json')['rows'];now={r['id']:r for r in claims['rows']}
 need(set(now)=={r['id'] for r in old} and all(now[r['id']]['predecessor_disposition']==r for r in old),'all exact predecessor dispositions')
 need([r['id'] for r in source['rows'] if r['id'].startswith('Section3_D')]==[r['id'] for r in load(HERE/'inputs/correlations/source_contract.json')['rows']],'exact correlation replacement IDs')
 for x,y in zip([r for r in source['rows'] if r['id'].startswith('Section3_D')],load(HERE/'inputs/correlations/source_contract.json')['rows']):need(x['status']==y['status'] and x['source_pages']==y['pages'],'literal nine-clause scope')
 oldlines=(base/'structural_table.tex').read_text().splitlines();newlines=(HERE/'structural_table.tex').read_text().splitlines()
 extract=lambda lines:{q.split(' & ')[0]:q.split(' & ')[:2] for q in lines if re.match(r'T\d+\.\d+ & ',q)}
 need(extract(oldlines)==extract(newlines) and len(extract(newlines))==73,'all literal printed group descriptions retained')
 program=load(HERE/'whole_file_inventory.json');occ=program['occurrences'];union=program['unique_contents'];freq=collections.Counter(r['sha256'] for r in occ)
 need(len(occ)==252 and len(union)==202 and {u['sha256']:len(u['occurrences']) for u in union}==dict(freq),'whole content union')
 required768=[r for r in occ if r['path']=='topic_A_L003_order768/verify.g'];need(len(required768)==1 and required768[0]['role']=='required mathematical program','required presentation calculation')
 need(all(r['role']=='optional validation' for r in occ if r['path']=='topic_A_L003_correlation_reduction/word_checks.py'),'correlation words only diagnostic')
 for folder in ['shared_structures','finite_structures','order768','correlations']:
  need(any(r['destination'].startswith('inputs/'+folder+'/') for r in copies),'whole packet '+folder)
 if a.study_root:
  for e in load(HERE/'accepted_input_bindings.json')['inputs']:binding(a.study_root/e['file']['path'],e['file'])
  binding(a.study_root/'sources/catalogue_L003.pdf',load(HERE/'accepted_input_bindings.json')['source'])
  for r in occ:
   root=a.study_root if r['root']=='study' else a.public_root
   if root:binding(root/r['path'],r)
 if a.public_root:need((a.public_root/'papers/topic-a/v3/umbrella.pdf').read_bytes()==(HERE/'retained/umbrella.pdf').read_bytes(),'entire unchanged old common')
 controls=[]
 def reject(name,field,mutate):
  args=[copy.deepcopy(scope),copy.deepcopy(source),copy.deepcopy(claims),copy.deepcopy(bundles)];mutate(args[field])
  try:validate(*args)
  except (ValueError,IndexError,KeyError,TypeError):controls.append(name)
  else:raise ValueError('survived control '+name)
 reject('drop source disposition',1,lambda x:x['rows'].pop())
 reject('duplicate named ID',1,lambda x:x['rows'][1].update(id=x['rows'][0]['id']))
 reject('restore unverified structural status',1,lambda x:next(r for r in x['rows'] if r['id']=='T3.1').update(assembly_status='UNVERIFIED'))
 reject('restore false split',1,lambda x:next(r for r in x['rows'] if r['id']=='T4.8').update(current_source_structure_status='printed_shape_under_explicit_brackets'))
 reject('claim diagram5 FT',1,lambda x:next(r for r in x['rows'] if r['id']=='Section3_D5_geometry').update(status='unconditional FT'))
 reject('lose fourth generator',1,lambda x:next(r for r in x['rows'] if r['id']=='Section3_D4_generators').update(status='t,a,b suffice'))
 reject('drop common companion',0,lambda x:x.update(whole_common_parts=[23,14]))
 reject('drop application companion',0,lambda x:x.update(L003_complete_application_parts=[7,4,4]))
 reject('restore printed order',0,lambda x:x['main_source_corrections'].__setitem__(0,'T5.8 full order2592000'))
 reject('claim source credit',0,lambda x:x.update(whole_source_credit=1))
 reject('invent software factor',0,lambda x:x.update(software_inclusive_factor=1))
 reject('omit bundle proof pages',3,lambda x:x['bundles'][1]['parts'].pop())
 reject('lost reviewed source route',2,lambda x:x['rows'][0].update(principal_gap_after_accepted_inputs=True))
 from pypdf import PdfReader
 page_texts=lambda p:[q.extract_text() for q in PdfReader(p).pages]
 for b in bundles['bundles']:
  alltexts=[]
  for f in b['parts']:binding(HERE/f['path'],f);alltexts+=page_texts(HERE/f['path'])
  need(alltexts==page_texts(HERE/b['path']) and len(alltexts)==b['pages'],'exact entire bundle content')
  need([hashlib.sha256(t.encode()).hexdigest() for t in alltexts]==b['page_text_sha256'],'bundle text hashes')
 rendered=None
 if a.render:
  out=a.out/'render';out.mkdir()
  for f in ['hexagonal_extensions.tex','structural_table.tex','finite_table.tex','local_corrections.tex']:shutil.copy2(HERE/f,out/f)
  for i in [1,2]:
   r=subprocess.run(['/opt/homebrew/bin/xelatex','-interaction=nonstopmode','-halt-on-error','hexagonal_extensions.tex'],cwd=out,capture_output=True,text=True,timeout=40);(a.out/f'render{i}.log').write_text(r.stdout+r.stderr);need(r.returncode==0,'fresh TeX')
  need(not any(w in r.stdout for w in ['Overfull','Underfull','Warning:','undefined','Missing character']),'clean final render')
  need(page_texts(out/'hexagonal_extensions.pdf')==page_texts(HERE/'hexagonal_extensions.pdf'),'seven exact new application pages');rendered=7
 report=dict(status='PASS_ASSEMBLY_NOT_ADMISSION',coverage=coverage,exact_payload_copies=len(copies),unchanged_application_environments=2,controls=controls,whole_file_occurrences=len(occ),unique_whole_contents=len(union),rendered_new_pages=rendered,retained_complete_bundle_pages=58,old_scientific_calculations_repeated=False,source_credit=0,measurements=None)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
