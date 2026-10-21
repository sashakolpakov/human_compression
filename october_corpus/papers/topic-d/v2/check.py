#!/usr/bin/env python3
"""Verify exact Topic D bindings; optionally replay full programs, Lean and TeX.

This is an author verifier, not an independent mathematical review. Source PDFs
and the historical proof bank are external, optional byte-verification inputs.
No primary source text is exported. No measurement or new credit is inferred.
"""
import argparse,copy,hashlib,json,os,re,shutil,subprocess,sys
from pathlib import Path
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent
DOCS=['umbrella','commuting-involutions','suzuki-polyhedra','hall-janko-geometries','program-appendix']
REQUIRED={'phase110_commuting_pairs_integration_finite.g','phase5_j2_search.g','phase5_j2_fuse.g','phase5_j2_verify.g','phase4_geometry_checks.g'}
DIAGNOSTICS={'phase110_commuting_pairs_integration_formula.py','phase10_suzuki_marked_fields_check.py','phase10_suzuki_marked_groups_check.g'}
DRIVERS={'phase110_commuting_pairs_integration_run.py','phase164_enumeration_run.py'}
def need(ok,message):
 if not ok:raise RuntimeError(message)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def local(name):
 p=(ROOT/name).resolve();need(p.is_relative_to(ROOT),'Escaping local path');return p
def binding(r,base=ROOT):
 p=base/r['path'];need(p.is_file() and p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'Changed bound file: '+r['path'])
def validate(scope):
 need(scope['source_ids']==['L066','L074','L104'] and scope['intake_closed'],'Wrong source boundary')
 expected=[f'{s}.{i}' for s,n in [('L066',16),('L074',17),('L104',4)] for i in range(1,n+1)]
 need([r['id'] for r in scope['contracts']]==expected and scope['contract_count']==37,'Incomplete or changed clause set')
 for r in scope['documents']:binding(r)
 for key,r in scope['proof_spans'].items():
  text=local(r['path']).read_text();a,b=r['start_codepoint'],r['end_codepoint_exclusive'];need(0<=a<b<=len(text),'Bad span bounds')
  need(hashlib.sha256(text[a:b].encode()).hexdigest()==r['sha256_utf8'],'Changed proof span: '+key)
 for row in scope['contracts']:
  need(row['current_proof_spans'] and all(x in scope['proof_spans'] for x in row['current_proof_spans']),'Missing proof reference')
  need(row['source_pages'] and all(1<=i<=scope['sources'][row['source_id']]['pages'] for i in row['source_pages']),'Bad source page')
 need(scope['contracts'][-1]['current_status']=='excluded_secondary_assertions_in_printed_main_article_and_supplement','L104 omissions lost')
 names={p['path'] for p in scope['program_inventory']}
 need(names==REQUIRED|DIAGNOSTICS|DRIVERS and len(scope['program_inventory'])==10,'Incomplete complete-program boundary')
 for p in scope['program_inventory']:
  binding(dict(path=p['copy'],bytes=p['bytes'],sha256=p['sha256']))
  need(p['category']==('driver' if p['path'] in DRIVERS else 'mathematical_program'),'Wrong program category')
 c=scope['cost_scope'];need(c['full_common_paper_charged_once_in_this_topic'] and not c['cross_topic_discount'],'Common theory charge changed')
 need(c['full_mathematical_programs']==8 and c['required_programs']==5 and c['additional_diagnostic_programs']==3 and c['complete_drivers']==2,'Wrong cost boundary')
 need(c['ratio'] is None and c['historical_program_cost'] is None and c['image_cost'] is None,'Invented or premature cost')
 binding(scope['formal_scope'])
 fs=json.loads(local('formal/scope.json').read_text())
 need(len(fs['modules'])==2 and sum(len(r['declarations']) for r in fs['modules'])==10,'Wrong scoped formal inventory')
 for r in fs['modules']:binding(dict(path='formal/'+r['file'],bytes=r['bytes'],sha256=r['sha256']))
 return {'clauses':37,'proof_spans':len(scope['proof_spans']),'documents':len(scope['documents']),'programs':10,'formal_declarations':10}
def code_inclusion():
 text=local('program-appendix.tex').read_text();names=re.findall(r'\\VerbatimInput\[[^\]]*\]\{programs/([^}]+)\}',text)
 need(len(names)==8 and set(names)==REQUIRED|DIAGNOSTICS,'Incomplete printed program list')
 parts=[]
 for page in PdfReader(local('program-appendix.pdf')).pages:
  def visit(t,cm,tm,font,size):
   if font and 'Menlo' in str(font.get('/BaseFont','')):parts.append(t)
  page.extract_text(visitor_text=visit)
 norm=lambda t:''.join(c for c in t if not c.isspace())
 source=norm(''.join(local('programs/'+n).read_text() for n in names));printed=norm(''.join(parts))
 need(source==printed,'PDF does not include the eight full programs in order')
 return {'programs':names,'nonspace_code_characters':len(source),'exact_nonspace_text':True,'note':'Whitespace from code layout is excluded from this byte-to-PDF inclusion test; raw executable bytes are bound separately.'}
def controls(scope):
 results=[]
 def reject(name,change):
  c=copy.deepcopy(scope);change(c)
  try:validate(c)
  except RuntimeError as e:results.append({'name':name,'rejected':True,'reason':str(e)})
  else:raise RuntimeError('Control accepted: '+name)
 reject('drop a principal source row',lambda c:c['contracts'].pop(0))
 reject('drop a complete required program',lambda c:c['program_inventory'].pop(0))
 reject('change a proof boundary',lambda c:c['proof_spans']['Support.1'].__setitem__('start_codepoint',1))
 reject('change program hash',lambda c:c['program_inventory'][0].__setitem__('sha256','0'*64))
 reject('erase L104 printed-body omissions',lambda c:c['contracts'][-1].__setitem__('current_status','all_assertions_proved'))
 reject('discount common theory across topics',lambda c:c['cost_scope'].__setitem__('cross_topic_discount',True))
 reject('replace unknown historical code cost by zero',lambda c:c['cost_scope'].__setitem__('historical_program_cost',0))
 return results
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--study-root',type=Path);ap.add_argument('--programs',action='store_true');ap.add_argument('--formal',action='store_true');ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default=shutil.which('xelatex'));ap.add_argument('--gap',default=shutil.which('gap'));ap.add_argument('--lean',type=Path);ap.add_argument('--packages',type=Path);a=ap.parse_args()
 need(not os.path.lexists(a.out),'Output must be fresh');out=a.out.resolve();out.mkdir(parents=True)
 scope=json.loads(local('scope.json').read_text());res=validate(scope);res['controls']=controls(scope);res['code_pdf']=code_inclusion()
 if local('manifest.json').is_file():
  manifest=json.loads(local('manifest.json').read_text())
  for r in manifest['exports']:binding(r)
  res['manifest_sha256']=sha(local('manifest.json'));res['exports_verified']=len(manifest['exports'])
 external=[]
 if a.study_root:
  for key,r in scope['predecessor'].items():binding(r,a.study_root);external.append(key)
  for sid,s in scope['sources'].items():
   binding(s['primary'],a.study_root);need(len(PdfReader(a.study_root/s['primary']['path']).pages)==s['pages'],'Wrong primary page count');external.append(sid)
 res['external_byte_checks']=external;res['external_inputs_not_supplied']=not bool(a.study_root)
 def run(name,cmd):
  p=subprocess.run(cmd,capture_output=True,text=True,timeout=1800);(out/(name+'.log')).write_text(p.stdout+p.stderr);need(p.returncode==0,'Replay failed: '+name);return p
 if a.programs:
  for part in ['small','j2']:run(part,[sys.executable,'-B','-O',str(local('programs/phase164_enumeration_run.py')),'--part',part,'--output-dir',str(out/part),'--gap',a.gap])
  res['program_replays']=['small','j2']
 if a.formal:
  cmd=[sys.executable,'-B','-O',str(local('formal/check.py')),'--out',str(out/'formal')]
  if a.lean:cmd+=['--lean',str(a.lean)]
  if a.packages:cmd+=['--packages',str(a.packages)]
  run('formal',cmd);res['formal_replayed']=True
 if a.render:
  need(a.xelatex,'XeLaTeX required');render=out/'render';render.mkdir()
  for r in scope['documents']:
   if r['path'].endswith('.tex'):
    p=render/r['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(local(r['path']),p)
  shutil.copytree(local('programs'),render/'programs')
  checks=[]
  for name in DOCS:
   for i in range(2):
    p=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error',name+'.tex'],cwd=render,capture_output=True,text=True);need(p.returncode==0,'TeX failed: '+name)
   log=(render/(name+'.log')).read_text();need(not any(x in log for x in ['Overfull','Missing character','LaTeX Warning','Package hyperref Warning']),'TeX diagnostic: '+name)
   old=PdfReader(local(name+'.pdf'));new=PdfReader(render/(name+'.pdf'));need(len(old.pages)==len(new.pages),'Render page count')
   need(all(x.extract_text()==y.extract_text() for x,y in zip(old.pages,new.pages)),'Render text changed: '+name)
   checks.append({'document':name,'pages':len(old.pages),'per_page_text_identical':True,'diagnostics':[]})
  res['render']=checks
 res.update(status='PASS',independent_mathematical_review=False,source_credit_increment=0,question_credit_increment=0,ratio=None)
 (out/'report.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'status':'PASS','clauses':37,'controls':len(res['controls']),'out':str(out)}))
if __name__=='__main__':main()
