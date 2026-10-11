#!/usr/bin/env python3
"""Audit proposed exact routes and bounded copied-packet replays; no public writes."""
from pathlib import Path
import argparse,copy,hashlib,json,re,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent
OLD_S=Path('/Users/sasha/medusa/research/leemans');OLD_P=Path('/Users/sasha/medusa/math_compression')
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,m):
 if not x:raise ValueError('OPERATIONS_MAP_REJECT: '+m)
def remap(p,a):
 p=Path(p)
 if p.is_relative_to(OLD_S):
  rel=str(p.relative_to(OLD_S))
  if a.published:
   need(rel in a.route_aliases,'declared public alias '+rel);return a.public_root/a.route_aliases[rel]['public_path']
  return a.study_root/rel
 if p.is_relative_to(OLD_P):return a.public_root/p.relative_to(OLD_P)
 return p
def exports(m):
 e=m['exports'];return [dict(v,path=k) for k,v in e.items()] if isinstance(e,dict) else e

def validate(p,c,w,e,a):
 need(not p['public_changes_made'] and not p['ratios_computed'] and p['source_credit_change']==p['question_credit_change']==0,'proposal only')
 dest={r['destination']:r for r in p['artifacts']};need(len(dest)==len(p['artifacts']),'unique destination')
 for r in dest.values():
  q=Path(r['destination']);need(not q.is_absolute() and '..' not in q.parts,'safe public-relative destination')
  src=remap(r['source'],a);need(src.is_file() and not src.is_symlink() and sha(src)==r['sha256'] and src.stat().st_size==r['bytes'],'exact source '+r['source'])
  need(not any(x in q.parts for x in ['private_source','private_data','__pycache__']) and not q.name.endswith(('.png','.jpg','.olean')),'no raw primary/image/cache export')
 for k in p['packets']:
  mf=remap(k['manifest']['path'],a);need(sha(mf)==k['manifest']['sha256'],'packet freeze '+k['id'])
  er=exports(load(mf));need(len(er)==k['exports'],'complete export count')
  for r in er+[dict(path='manifest.json',sha256=sha(mf),bytes=mf.stat().st_size)]:
   d=str(Path(k['destination'])/r['path']);need(d in dest and all(dest[d][x]==r[x] for x in ['sha256','bytes']),'every complete packet export '+d)
 for old,r in p['study_aliases'].items():
  need(r['public_path'] in dest and dest[r['public_path']]['sha256']==r['sha256'],'exact original-to-public alias')
  need(sha(remap(OLD_S/old,a))==r['sha256'],'original alias remains exact')
 policy=load(remap(OLD_S/'topic_Operations_measurement_inputs_v1/policy.json',a))
 need(p['counts']==dict(originals=3,source_records=140,current_scientific_documents=6,current_scientific_pages=61,audit_documents=11,audit_pages=161,whole_program_files=23,required_programs=17,validation_programs=6,required_input_drivers=2,operational_drivers=5,unique_Lean_files=3,partial_Lean_declarations=17,new_N005_Lean_declarations=0),'exact complete boundary')
 need(set(p['current_pdfs'])==set(policy['replacements']),'all eight whole replacement PDFs')
 for k,r in p['current_pdfs'].items():
  need(all(r[x]==policy['replacements'][k][x] for x in ['sha256','bytes','pages']),'current document identity '+k)
  need(dest[r['public_path']]['sha256']==r['sha256'],'current route '+k)
 need({x['id']:x['records'] for x in p['source_contracts']}=={'N005':81,'N006':27,'N007':32},'all source dispositions')
 for r in p['source_contracts']:need(dest[r['public_path']]['sha256']==r['sha256'],'source contract binding')
 need({r['id'] for r in p['source_inputs']}=={'N005','N006','N007'} and sum(r['pages'] for r in p['source_inputs'])==94,'three complete originals')
 for r in p['source_inputs']:
  need(r['publication_action']=='never_export_user_supplied_primary' and all(x['sha256']!=r['sha256'] for x in dest.values()),'no original redistributed')
 needed=load(remap(OLD_S/'topic_Operations_measurement_inputs_v1/software_inventory.json',a))
 for cat in ['programs','required_input_drivers','operational_drivers','formal_files']:
  need([{k:v for k,v in r.items() if k!='public_path'} for r in w[cat]]==needed[cat],'whole files and exact roles '+cat)
  for r in w[cat]:need(dest[r['public_path']]['sha256']==r['sha256'],'software route '+r['id'])
 need(len({r['sha256'] for r in w['programs']})==23,'within-topic unique programme hashes')
 need(sum(r['logical_premise'] for r in w['programs'])==17,'required versus validation')
 scientific=[r for r in c['documents'] if r['scientific_current']]
 need(len(scientific)==6 and sum(r['pages'] for r in scientific)==61 and len(c['documents'])==8,'whole scientific and printed-alternative routes')
 for r in c['documents']:
  need(r['tex'] in r['tex_inputs'] and r['pdf'] in dest,'wrapper and PDF')
  actual=remap(dest[r['tex']]['source'],a).read_text()
  work=Path(r['tex']).parent
  for f in re.findall(r'\\(?:input|VerbatimInput)(?:\[[^\]]*\])?\{([^}]+)\}',actual):
   path=work/f
   if not path.suffix:path=path.with_suffix('.tex')
   need(str(path) in r['tex_inputs'],'complete direct TeX input '+str(path))
  need(all(x in dest for x in r['tex_inputs']),'every complete catalogue input')
 need(p['external_boundary']==dict(required_representation_files=4,required_representation_bytes=21960689,installed_catalogue_algorithm_files=16,installed_catalogue_algorithm_bytes=2516249,full_classical_proof_cost=None,graphics_cost=None,external_redistribution=False),'complete external costs')
 need(e['external']['unknown_proof_cost'] is None and e['retained']['all_external_proof_costs'] is None,'unknown is not zero')
 need(p['packets'][5]['id']=='inputs' and any(k['id']=='input_review' and k['manifest']['sha256']=='edb9e44fe49f5cd32ce66a909cef4e0324861d3026d9863417d23417768960d7' for k in p['packets']),'accepted input edition')
 return dict(status='PASS',packets=len(p['packets']),artifact_routes=len(dest),original_aliases=len(p['study_aliases']),source_records=140,whole_scientific_documents=6,whole_scientific_pages=61,whole_programs=23,required_drivers=2,ratio=None)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--stage-replays',action='store_true');ap.add_argument('--published',action='store_true');a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh output');a.out.mkdir(parents=True)
 if (HERE/'manifest.json').exists():
  for r in exports(load(HERE/'manifest.json')):need(sha(HERE/r['path'])==r['sha256'] and (HERE/r['path']).stat().st_size==r['bytes'],'frozen proposal '+r['path'])
 p,c,w,e=[load(HERE/n) for n in ['publication_map.json','catalogue_proposal.json','software_routes.json','external_and_retained.json']]
 a.route_aliases=p['study_aliases'];report=validate(p,c,w,e,a);tests=[]
 def reject(name,fn):
  pp,cc,ww,ee=copy.deepcopy((p,c,w,e));fn(pp,cc,ww,ee)
  try:validate(pp,cc,ww,ee,a)
  except (ValueError,KeyError):tests.append(dict(control=name,rejected=True));return
  raise RuntimeError('accepted bad map '+name)
 reject('omitted complete program',lambda p,c,w,e:w['programs'].pop())
 reject('decoder demoted to operational',lambda p,c,w,e:w['required_input_drivers'][0].update(role='operational_only'))
 reject('missing Harada Norton application',lambda p,c,w,e:p['current_pdfs'].pop('A2HN'))
 reject('historical common substituted for current',lambda p,c,w,e:p['current_pdfs']['U'].update(sha256='dba314b02f883aaa4cb858dedd141b4d7737b34ce1747af32c29952ee63dc86e'))
 reject('missing full export',lambda p,c,w,e:p['artifacts'].pop(0))
 reject('source contract narrowed',lambda p,c,w,e:p['source_contracts'][0].update(records=80))
 reject('retained classification priced zero',lambda p,c,w,e:p['external_boundary'].update(full_classical_proof_cost=0))
 reject('primary PDF added to exports',lambda p,c,w,e:p['artifacts'].append(dict(source=str(a.study_root/p['source_inputs'][0]['study_path']),destination='papers/primary.pdf',sha256=p['source_inputs'][0]['sha256'],bytes=p['source_inputs'][0]['bytes'],action='copy_exact',role='primary')))
 reject('partial TeX inputs',lambda p,c,w,e:c['documents'][0]['tex_inputs'].pop())
 reject('formal claim expanded',lambda p,c,w,e:p['counts'].update(new_N005_Lean_declarations=17))
 replays=[]
 if a.stage_replays:
  public=a.out/'public';study=a.out/'study';public.mkdir();study.mkdir()
  for r in p['artifacts']:
   q=public/r['destination'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(remap(r['source'],a),q)
  for old,r in p['study_aliases'].items():
   q=study/old;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(public/r['public_path'],q)
  cmds=[('integrated',[sys.executable,'-B','-O',str(study/'corpus161_N005_integrated/check.py'),'--out',str(a.out/'integrated_replay')]),('migration_review',[sys.executable,'-B','-O',str(study/'corpus161_N005_integrated_root_review/check.py'),'--packet',str(study/'corpus161_N005_integrated'),'--out',str(a.out/'migration_review.json')]),('citations',[sys.executable,'-B','-O',str(study/'topic_Operations_sibling_citations_v1/check.py'),'--study-root',str(study),'--public-root',str(public),'--out',str(a.out/'citation_replay')]),('boundary',[sys.executable,'-B','-O',str(study/'topic_Operations_input_contract_v1/check.py'),'--study-root',str(study),'--public-root',str(public),'--out',str(a.out/'boundary_replay')])]
  for name,cmd in cmds:
   r=subprocess.run(cmd,capture_output=True,text=True);(a.out/(name+'.log')).write_text(r.stdout+r.stderr);need(r.returncode==0,'copied-only replay '+name);replays.append(dict(name=name,status='PASS',source_reextraction=False,scientific_programs_run=False,Lean_run=False,render_run=False))
 report.update(controls=tests,copied_export_only_replays=replays,public_tree_modified=False,ratio=None)
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
