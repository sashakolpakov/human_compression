#!/usr/bin/env python3
"""Portable complete E extension check. Optional scientific runs are reported honestly."""
import argparse,copy,hashlib,json,os,re,shutil,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def need(b,m):
 if not b:raise ValueError('E_CHIRAL_REJECT '+m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def binding(base,row):
 p=base/row['path'];need(p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'binding '+row['path'])
def validate(scope,source,old,proof,program,formal):
 need(scope['new_originals']==['L056','L043'] and scope['retained_originals']==['L079','L083','L021'],'five originals')
 need(scope['whole_common_paid_once'] is True and scope['new_source_credit']==scope['new_question_credit']==0 and scope['ratios'] is None,'no admission/ratio')
 need(len(source['rows'])==56 and len({r['id'] for r in source['rows']})==56 and len(old['records'])==54,'all 110 dispositions')
 rows={r['id']:r for r in source['rows']}
 for k in ['L043.T1.4b','L043.L5.12','L056.L4.3']:
  need('correct' in rows[k]['disposition'] or 'correction' in rows[k]['disposition'],'source correction '+k)
 need('10 modulo11' in rows['L043.T1.4b']['qualification'],'residue10 correction')
 for k in ['L043.T8','L043.T10','L043.Table1','L043.Table2']:need('not_re' in rows[k]['disposition'],'ancillary scope '+k)
 for r in source['rows']:
  for lab in r['proof_interfaces']:need(lab in proof['labels'] or lab in proof['additional_interfaces'],'complete interface '+lab)
 expected={'required_finite.g':'required finite proof','exceptional_amalgams.g':'required finite proof','exceptional_small.g':'required finite proof','small_rotation_exclusions.g':'required finite proof','psl2_square_bound_check.py':'required finite proof','verify_square_witnesses.py':'required finite proof','psl2_square_witnesses.json':'required certificate data','validation.g':'validation only','pointed_models.g':'validation only','source_clause_571.g':'validation only','psl2_square_witnesses.g':'validation only','psl2_nested_witnesses.g':'validation only','psl2_intersection_check.g':'validation only'}
 need({Path(r['path']).name:r['role'] for r in program['files']}==expected,'whole required/validation/data boundary')
 need(program['raw_and_printed_alternatives_not_additive'] is True and 'symmetrically' in program['measurement_policy'],'symmetric alternatives')
 need(formal['reported_declarations']==42 and formal['new_declarations']==9 and len(formal['modules'])==7,'scoped formal inventory')
 need(sum(len(r['declarations']) for r in formal['modules'])==42 and len(formal['not_formalized'])>=6,'partial formal boundary')
 return True

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--study-root',type=Path);ap.add_argument('--public-root',type=Path);ap.add_argument('--verify-inputs',action='store_true');ap.add_argument('--programs',action='store_true');ap.add_argument('--formal',action='store_true');ap.add_argument('--render',action='store_true');ap.add_argument('--gap',default='/opt/homebrew/bin/gap');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');ap.add_argument('--lean',default='/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean');ap.add_argument('--packages',default='/Users/sasha/bogachev/formal/.lake/packages');a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh output');a.out.mkdir(parents=True);out=a.out.resolve();started=time.monotonic()
 exports=[]
 if (ROOT/'manifest.json').exists():
  exports=load(ROOT/'manifest.json')['exports']
  for row in exports:binding(ROOT,row)
 names=['scope.json','source_map.json','retained_source_maps.json','proof_map.json','program_scope.json','formal/scope.json'];objects=[load(ROOT/n) for n in names];validate(*objects)
 scope,source,old,proof,program,formal=objects
 for row in program['files']:binding(ROOT,row)
 for row in formal['modules']:binding(ROOT/'formal',dict(path=row['file'],bytes=row['bytes'],sha256=row['sha256']))
 for key,row in proof['contexts'].items():
  lines=(ROOT/row['path']).read_text().splitlines(keepends=True);raw=''.join(lines[row['start_line']-1:row['end_line']]).encode();need(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'complete proof span '+key)
 need(len(proof['contexts'])==proof['count'],'span count')
 migration=load(ROOT/'migration.json');pat=r'\\begin\{(theorem|lemma|proposition|corollary|proof)\}.*?\\end\{\1\}'
 for row in migration['records']:
  binding(ROOT,row['current_binding']);envs=[m.group() for m in re.finditer(pat,(ROOT/row['current']).read_text(),re.S)];need([hashlib.sha256(x.encode()).hexdigest() for x in envs]==row['environment_hashes'],'32 unchanged proof environments')
 checked_inputs=[]
 if a.verify_inputs:
  need(a.study_root is not None,'--study-root for inputs');pins=load(ROOT/'bindings.json')
  for category in ['sources','retained_primary','prior_proof_and_acceptance']:
   for row in pins[category]:binding(a.study_root,row);checked_inputs.append(row)
  for row in migration['records']:
   binding(a.study_root,row['prior_binding']);oldenv=[m.group() for m in re.finditer(pat,(a.study_root/row['prior']).read_text(),re.S)];need([hashlib.sha256(x.encode()).hexdigest() for x in oldenv]==row['environment_hashes'],'literal migration '+row['prior'])
  if a.public_root:
   for row in pins['canonical_formal']:binding(a.public_root,row);checked_inputs.append(row)
 # Semantic scope controls change the actual supplied objects, not expected success labels.
 controls=[]
 mutations=[('omit_new_original',lambda x:x[0]['new_originals'].pop()),('unpay_common',lambda x:x[0].update(whole_common_paid_once=False)),('source_credit',lambda x:x[0].update(new_source_credit=2)),('drop_source_row',lambda x:x[1]['rows'].pop()),('drop_old_contract',lambda x:x[2]['records'].pop()),('unbound_interface',lambda x:x[1]['rows'][0].update(proof_interfaces=['invented'])),('hide_correction',lambda x:next(r for r in x[1]['rows'] if r['id']=='L043.L5.12').update(disposition='proved')),('hide_residue',lambda x:next(r for r in x[1]['rows'] if r['id']=='L043.T1.4b').update(qualification='none')),('claim_full_T8',lambda x:next(r for r in x[1]['rows'] if r['id']=='L043.T8').update(disposition='proved')),('omit_data',lambda x:x[4]['files'].pop()),('demote_required_program',lambda x:x[4]['files'][1].update(role='validation only')),('promote_validation',lambda x:next(r for r in x[4]['files'] if r['path'].endswith('pointed_models.g')).update(role='required finite proof')),('add_code_alternatives',lambda x:x[4].update(raw_and_printed_alternatives_not_additive=False)),('full_formal_claim',lambda x:x[5].update(not_formalized=[])),('wrong_formal_count',lambda x:x[5].update(reported_declarations=99))]
 for name,change in mutations:
  obj=copy.deepcopy(objects);change(obj)
  try:validate(*obj)
  except (ValueError,KeyError):controls.append({'name':name,'rejected':True})
  else:raise ValueError('Control accepted '+name)
 runs=[];env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
 def run(cmd,cwd,stem,timeout=900):
  t=time.monotonic();p=subprocess.run(list(map(str,cmd)),cwd=cwd,env=env,capture_output=True,text=True,timeout=timeout);(out/(stem+'.stdout')).write_text(p.stdout);(out/(stem+'.stderr')).write_text(p.stderr);need(p.returncode==0 and not re.search(r'(^|\n)(Error,|Syntax error:|Traceback)',p.stdout+p.stderr),'child '+stem);return p,round(time.monotonic()-t,3)
 if a.programs:
  work=out/'program_work';(work/'research/leemans').mkdir(parents=True);pr=work/'programs';pr.mkdir()
  for row in program['files']:shutil.copyfile(ROOT/row['path'],pr/Path(row['path']).name)
  markers={'required_finite.g':'TOPIC_E_REQUIRED_FINITE_PASS','exceptional_amalgams.g':'EXCEPTIONAL_AMALGAMS_PASS','exceptional_small.g':'EXCEPTIONAL_SMALL_PASS','small_rotation_exclusions.g':'SMALL_ROTATION_EXCLUSIONS_PASS','psl2_square_bound_check.py':'ALL_EXACT_INTEGER_CHECKS_PASSED','verify_square_witnesses.py':'"all_passed": true','validation.g':'TOPIC_E_VALIDATION_PASS','pointed_models.g':'POINTED_PASS','source_clause_571.g':'PSL571_PASS','psl2_square_witnesses.g':'PASS','psl2_nested_witnesses.g':'PASS','psl2_intersection_check.g':'PASS: containing intersection'}
  for row in program['files']:
   f=pr/Path(row['path']).name
   if f.suffix=='.json':continue
   cmd=[a.gap,'-T','-b','-r','-q',f] if f.suffix=='.g' else [sys.executable,'-B',f]
   p,secs=run(cmd,work,'program_'+f.stem);need(markers[f.name] in p.stdout,'completion '+f.name)
   runs.append({'file':row,'seconds':secs,'stdout_sha256':sha(out/('program_'+f.stem+'.stdout')),'assertions_enabled':True if f.suffix=='.py' else None})
 if a.formal:
  run([sys.executable,'-B','-O',ROOT/'formal/check.py','--out',out/'formal','--lean',a.lean,'--packages',a.packages],out,'formal_driver',1800)
 if a.render:
  run([sys.executable,'-B','-O',ROOT/'render.py','--out',out/'render','--xelatex',a.xelatex,'--compare'],out,'render_driver',1800)
 result={'status':'PASS','seconds':round(time.monotonic()-started,3),'frozen_exports_checked':len(exports),'source_dispositions':56,'retained_dispositions':54,'proof_contexts':len(proof['contexts']),'unchanged_environments':sum(r['environments'] for r in migration['records']),'input_bindings_checked':len(checked_inputs),'controls':controls,'programs_fresh':runs,'formal_fresh':load(out/'formal/report.json') if a.formal else None,'render_fresh':load(out/'render/report.json') if a.render else None,'not_run':[name for name,yes in [('programs',a.programs),('formal',a.formal),('render',a.render)] if not yes],'no_ratio':True,'no_new_credit':True,'checker_sha256':sha(Path(__file__))}
 (out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','seconds':result['seconds'],'programs':len(runs),'formal':a.formal,'render':a.render,'report':str(out/'report.json')}))
if __name__=='__main__':main()
