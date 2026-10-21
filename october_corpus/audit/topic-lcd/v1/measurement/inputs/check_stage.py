"""Portable complete LCD input check; never computes factors."""
from pathlib import Path
import argparse,copy,hashlib,json,shutil,subprocess,sys
from collections import Counter
from extract_inputs import H,load,metrics,replay,sha,transformed,validate_one
from font_tools import need

def bound(path,row):
 b=path.read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'whole-file binding '+str(path))

def raw_files(study):
 p=load('whole_file_boundary.json')
 need(p==load('protocol_file_roles/whole_file_boundary.json'),'complete-file boundary with exact operational-role clarification')
 old_boundary=load('protocol_addition_L050/whole_file_boundary.json');clarified=copy.deepcopy(old_boundary)
 next(r for r in clarified['files']if r['path']=='topic_LCD_L050_application/check.py')['role']='operational_driver'
 next(r for r in clarified['unique_files']if 'topic_LCD_L050_application/check.py'in r['occurrences'])['roles']=['operational_driver']
 need(p==clarified,'only the declared operational-role clarification')
 need(p['software_inclusive_factor'] is None and p['source_software'] is None,'unknown software remains unknown')
 need(p['unique_partial_declarations']==9 and p['full_Lean'] is False,'partial formal scope counted once')
 need(len(p['files'])==127 and len(p['unique_files'])==102,'all occurrences and unique whole files')
 for r in p['files']:bound(study/r['path'],r)
 for r in p['original_inventory_bindings']:bound(study/r['path'],r)
 rows=[]
 priority=['required_program','required_derived_certificate','required_data','required_finite_record','optional_validation','operational_driver','partial_formal_file','partial_formal_scope']
 for r in p['unique_files']:
  b=(study/r['path']).read_bytes();bound(study/r['path'],r)
  occurrences=[x for x in p['files']if x['sha256']==r['sha256']]
  need(r['occurrences']==[x['path']for x in occurrences] and r['roles']==sorted({x['role']for x in occurrences}),'exact whole-content deduplication')
  need(r['mathematical_premise']==any(x['mathematical_premise']for x in occurrences),'required premise not demoted')
  role=next(x for x in priority if x in r['roles'])
  rows.append(dict(**r,role=role,metrics={n:metrics(b.decode('utf-8'),n)for n in p['normalizations']}))
 need(len({r['sha256']for r in rows})==102,'no repeated content counted twice')
 old=load('previous_stage/known_file_counts.json')
 byhash={r['sha256']:r for r in rows}
 for r in old['files']:need(r['metrics']==byhash[r['sha256']]['metrics'],'all450 prior F017 file cells unchanged')
 return dict(status='COMPLETE_LCD_FILE_INVENTORY_NO_SOFTWARE_FACTOR',files=rows,occurrence_bindings=p['files'],metric_cells=10*len(rows),whole_bytes=sum(r['bytes']for r in rows),roles=dict(Counter(r['role']for r in rows)),duplicate_content_groups=[r['occurrences']for r in rows if len(r['occurrences'])>1],software_inclusive_factor=None,final_topic_closure=True,previous_F017_cells_unchanged=450)

def validate_result(x):
 need(x==load('author_stage_counts.json'),'exact all-variant metric vectors and text hashes')
 need(x['complete_topic_boundary'] and x['ratio'] is None and x['software_inclusive_factor'] is None,'no premature complete-topic factor')

def controls(cache,result,raw):
 out=[];spec=load('input_spec.json')
 def reject(name,fn):
  try:fn()
  except (RuntimeError,ValueError,AssertionError,KeyError,TypeError,IndexError):out.append(dict(name=name,rejected=True));return
  raise RuntimeError('CONTROL ACCEPTED: '+name)
 def row_test(key,name,edit):
  r=copy.deepcopy(spec[key]);edit(r)
  reject(name,lambda:validate_one(key,r,*cache[key]))
 row_test('L050','drop one whole source page',lambda r:r['page_bindings'].pop())
 row_test('U_LCD','remove a common-paper page',lambda r:r['included_spans'][0].update(end=r['page_bindings'][-1]['start']))
 row_test('F017','exclude genuine first-page abstract as furniture',lambda r:r['excluded_furniture'].append(dict(start=200,end=300)))
 row_test('L050','remove the publisher bibliographic line',lambda r:r['excluded_furniture'][0].update(end=r['excluded_furniture'][0]['end']+40))
 row_test('U_LCD','wrong printable sum calibration',lambda r:next(g for g in r['glyph_substitutions']if g['output']=='∑').update(output='P'))
 row_test('U_LCD','drop a genuine control-byte bracket',lambda r:r['glyph_substitutions'].remove(next(g for g in r['glyph_substitutions']if '\x00' in g['input'])))
 row_test('U_LCD','collapse tail and adjacent arrow to one mapsto glyph',lambda r:next(g for g in r['glyph_substitutions']if g['output']=='⊢').update(output='↦'))
 row_test('F017','discard private-use dotless-j event',lambda r:r['glyph_substitutions'].remove(next(g for g in r['glyph_substitutions']if g['output']=='ȷ')))
 row_test('A_F017','wrong blackboard font repair',lambda r:r['glyph_substitutions'][0].update(output='F'))
 row_test('L050','alter exact source font dictionary identity',lambda r:r['glyph_substitutions'][0]['pdf_events'][0].update(font_identity='0'*64))
 row_test('F017','alter effective encoded byte',lambda r:r['glyph_substitutions'][0]['pdf_events'][0].update(encoded_byte=255))
 row_test('U_LCD','alter effective font encoding identity',lambda r:r['glyph_substitutions'][0]['pdf_events'][0].update(effective_encoding_sha256='0'*64))
 altered=copy.deepcopy(cache['U_LCD'][-1]);altered['encoded_glyph_classes'][0]['glyph_evidence']['outline_sha256']='0'*64
 reject('alter actual glyph outline evidence',lambda:need(altered==load('font_audit.json')['U_LCD'],'exact outline metadata'))
 # Check binding directly: the row validator compares extraction metadata, not the PDF bytes.
 b=copy.deepcopy(load('document_map.json')['documents'][0]);b['sha256']='0'*64
 reject('whole-source hash mutation',lambda:bound(Path(CURRENT_STUDY)/b['path'],b))
 x=copy.deepcopy(result);x['documents']['L050']['variants']['calibrated_selected']['NFC']['characters_without_whitespace']+=1
 reject('change one calibrated count',lambda:validate_result(x))
 x=copy.deepcopy(result);x['documents']['F017']['variants']['raw_untrimmed']['NFKC']['normalized_text_sha256']='0'*64
 reject('change a retained raw sensitivity hash',lambda:validate_result(x))
 for key,value in [('complete_topic_boundary',False),('ratio',1),('software_inclusive_factor',0),('new_original_credit',1)]:
  x=copy.deepcopy(result);x[key]=value;reject('premature '+key,lambda x=x:validate_result(x))
 x=copy.deepcopy(raw);x['files'].pop()
 reject('drop a whole mandatory/declared file',lambda:need(x==raw,'complete raw-file vector'))
 x=copy.deepcopy(raw);next(r for r in x['files']if r['role']=='required_program')['mathematical_premise']=False
 reject('relabel a required certificate as optional',lambda:need(x==raw,'required roles preserved'))
 row_test('A_L050','drop the new application table/reference page',lambda r:r['page_bindings'].pop())
 row_test('A_L050','retain a newly identified script-H alias',lambda r:next(g for g in r['glyph_substitutions']if g['output']=='ℋ').update(output='H'))
 x=copy.deepcopy(raw);x['occurrence_bindings'].pop()
 reject('hide a repeated required-file occurrence',lambda:need(x==raw,'all occurrence bindings visible'))
 return out

def main():
 global CURRENT_STUDY
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--prepare-raw',action='store_true');ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();CURRENT_STUDY=a.study_root
 need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 if (H/'manifest.json').exists():
  for r in load('manifest.json')['exports']:bound(H/r['path'],r)
 for folder in ['protocol_freeze','protocol_addition_F017','protocol_known_files','protocol_addition_L050','protocol_file_roles']:
  for r in load(folder+'/manifest.json')['exports']:bound(H/folder/r['path'],r)
 p=load('policy.json')
 bound(H/p['previous_policy_manifest']['path'],p['previous_policy_manifest'])
 for key in ['common_author_manifest','common_root_adoption','F017_author_manifest','F017_distinct_root_review','L050_author_manifest','L050_distinct_root_review','previous_stage_manifest']:bound(a.study_root/p[key]['path'],p[key])
 for r in load('helper_provenance.json')['helpers']:bound(H/r['path'],r)
 result,cache=replay(a.study_root);validate_result(result);raw=raw_files(a.study_root)
 if a.prepare_raw:(H/'whole_file_counts.json').write_text(json.dumps(raw,ensure_ascii=False,indent=2)+'\n')
 else:need(raw==load('whole_file_counts.json'),'all known whole-file metrics')
 checks=controls(cache,result,raw)
 render=None
 if a.render:
  from pypdf import PdfReader
  from build_reader import tex
  need(tex()==(H/'reader.tex').read_text(),'exact generated reader')
  run=subprocess.run([sys.executable,'-B',str(H/'build_reader.py'),'--out',str(a.out/'render'),'--xelatex',a.xelatex],text=True,capture_output=True)
  (a.out/'render.log').write_text(run.stdout+run.stderr);need(run.returncode==0,'fresh reader build')
  old=[p.extract_text()for p in PdfReader(H/'reader.pdf').pages];new=[p.extract_text()for p in PdfReader(a.out/'render/reader.pdf').pages]
  need(len(old)==2 and old==new,'two exact reader page texts');render=dict(pages=2,exact_page_text=True,diagnostics=json.loads((a.out/'render/diagnostics.json').read_text()))
 report=dict(status='PASS_COMPLETE_INPUT_PROPOSAL_PENDING_DISTINCT_REVIEW',PDF_metric_cells=150,known_file_metric_cells=raw['metric_cells'],pages=69,repairs={k:v['calibration_occurrences']for k,v in result['documents'].items()},controls=checks,reader_render=render,complete_topic_boundary=True,ratio=None,software_inclusive_factor=None,large_mathematical_programs_rerun=False)
 for name,obj in [('counts.json',result),('whole_file_counts.json',raw),('report.json',report)]:(a.out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 print('PASS150PDF/'+str(raw['metric_cells'])+' unique raw cells/69pages/'+str(len(checks))+' controls; no factors')
if __name__=='__main__':main()
