#!/usr/bin/env python3
"""Distinct input audit and semantic rejection controls; no author scoring imports."""
from pathlib import Path
import argparse,copy,json,subprocess,sys,shutil,time
import recount as R
import font_bindings as F

def controls(packet,study):
 passed=[]
 def reject(name,call):
  try:call()
  except (ValueError,KeyError,IndexError) as e:passed.append(dict(name=name,rejected=True,reason=str(e)));return
  raise ValueError('control accepted: '+name)
 p=R.read(packet/'policy.json')
 def bad(name,mut):
  q=copy.deepcopy(p);mut(q);reject(name,lambda:R.boundary(q))
 bad('drop_source_last_page',lambda q:q['documents']['L020'].update(pages=18))
 bad('omit_required_counterproof',lambda q:q['applications'].update(L020=['A1']))
 bad('omit_common',lambda q:q.update(whole_common=[]))
 bad('free_old_B',lambda q:q.update(old_Topic_B_common_free_premise=True))
 bad('double_count_previous_appendix',lambda q:q.update(old_two_page_program_appendix='added'))
 bad('prune_validation_program',lambda q:q['programs'].pop(1))
 bad('partial_program',lambda q:q['programs'][0].update(whole_file=False))
 bad('validation_called_uniform_premise',lambda q:q['programs'][1].update(logical_role='required_uniform_theorem'))
 bad('omit_driver',lambda q:q['operational_drivers'].pop())
 bad('inflate_formal_scope',lambda q:q.update(formal_declarations=16))
 bad('unknown_graphics_zero',lambda q:q['unknown_costs'].update(graphics_and_layout=0))
 bad('factor_before_adoption',lambda q:q.update(factors_permitted=True,ratio=1))
 bad('switch_primary_to_calibrated',lambda q:q['primary_coordinate'].update(variant='calibrated_selected'))
 bad('conditional_counterproof_free',lambda q:q.update(conditional_policy='whole common only'))
 specs=R.read(packet/'input_spec.json');path=study/specs['L020']['path']
 def baddoc(name,mut):
  d=copy.deepcopy(specs['L020']);mut(d);reject(name,lambda:R.document('L020',path,d))
 baddoc('trim_title_body',lambda d:d['included_spans'][0].update(start=1))
 baddoc('furniture_eats_body',lambda d:d['excluded_furniture'][1].update(end=d['excluded_furniture'][1]['end']+1))
 baddoc('omit_alias',lambda d:d['glyph_substitutions'].pop())
 baddoc('wrong_alias_visible_symbol',lambda d:d['glyph_substitutions'][0].update(output='Γ'))
 baddoc('wrong_alias_context',lambda d:d['glyph_substitutions'][0].update(context_sha256='0'*64))
 audits=R.read(packet/'font_audit.json')
 for name,mut in [
  ('wrong_font_dictionary_bytes',lambda a:a['L020']['font_dictionaries'][0].update(font_dictionary_sha256='0'*64)),
  ('wrong_effective_encoding',lambda a:a['L020']['font_dictionaries'][0]['effective_encoding'].update({'71':'N'})),
  ('wrong_actual_class_count',lambda a:a['L020']['encoded_glyph_classes'][0].update(occurrences=a['L020']['encoded_glyph_classes'][0]['occurrences']+1)),
  ('wrong_actual_outline',lambda a:next(c for c in a['L020']['encoded_glyph_classes'] if c['font']=='/ZSYTRN+CMSY10' and c['encoded_byte']==71)['glyph_evidence'].update(outline_sha256='0'*64))]:
  a=copy.deepcopy(audits);mut(a);reject(name,lambda:F.verify(packet,study,audits_override=a))
 d=copy.deepcopy(specs);d['L020']['glyph_substitutions'][0]['pdf_event']['font_dictionary_object']['idnum']=109
 reject('alias_transferred_to_wrong_actual_dictionary',lambda:F.verify(packet,study,specs_override=d))
 row=copy.deepcopy(p['programs'][0]);row['sha256']='0'*64;reject('whole_program_byte_corruption',lambda:R.bound(study,row))
 # Independent state-machine stress: NBSP/Unicode whitespace, script compatibility,
 # underscore separating alphanumeric runs, literal printed hyphen and tab remain governed by policy.
 text='\t𝒢_N\u00a0a-\nb  '
 m=R.measure(text,'NFC');R.need([m[k] for k in ['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']]==[3,4,6,8,11],'literal Unicode counter fixture')
 return passed

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--copy-replay',action='store_true');ap.add_argument('--xelatex',default='xelatex');a=ap.parse_args();start=time.monotonic();R.need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 here=Path(__file__).resolve().parent
 if (here/'manifest.json').exists():
  for r in R.read(here/'manifest.json')['exports']:R.bound(here,r)
 r=R.audit(a.packet,a.study_root);f=F.verify(a.packet,a.study_root);c=controls(a.packet,a.study_root)
 for name,obj in [('recount.json',r),('font_review.json',f),('controls.json',c)]:
  (a.out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 author=None
 if a.copy_replay:
  copyto=a.out/'export_only_author';copyto.mkdir()
  for row in R.read(a.packet/'manifest.json')['exports']+[{'path':'manifest.json'}]:
   target=copyto/row['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a.packet/row['path'],target)
  cmd=[sys.executable,'-B','-O',str(copyto/'check.py'),'--study-root',str(a.study_root.resolve()),'--out',str(a.out/'author_replay'),'--render','--xelatex',a.xelatex]
  q=subprocess.run(cmd,capture_output=True);(a.out/'author.stdout').write_bytes(q.stdout);(a.out/'author.stderr').write_bytes(q.stderr);R.need(q.returncode==0,'export-only author replay');author=R.read(a.out/'author_replay/report.json');R.need(author['status']=='PASS_COMPLETE_L020_INPUT_PROPOSAL' and author['controls']==23 and author['reader_pages']==2 and author['reader_page_texts_match'],'exact bounded copied author replay')
 result=dict(status='PASS_DISTINCT_L020_INPUT_REVIEW',author_manifest_sha256=R.PIN,pdf_metric_cells=150,raw_metric_cells=80,text_hashes=92,pages=33,source_dictionaries=23,source_encoded_classes=528,actual_calibrated_events=112,independent_controls=len(c),state_machine_fixture=True,author_copy_replay=author,scientific_programs_executed=False,factors_computed=False,author_scoring_imported=False,elapsed_seconds=round(time.monotonic()-start,3))
 (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
