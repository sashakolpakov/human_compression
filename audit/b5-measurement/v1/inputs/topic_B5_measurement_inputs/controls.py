"""Fail-closed controls for complete B5 inputs and exact proof-role boundaries."""
import argparse,copy,json
from pathlib import Path
import extract_inputs as h

def run(args):
 counts,audits,cache=h.replay(args);p=h.load('policy.json');spec=h.load('input_spec.json');aliases=h.load('glyph_aliases.json')['aliases'];tests=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError,IndexError,TypeError):tests.append(dict(name=name,rejected=True));return
  raise ValueError('CONTROL NOT REJECTED: '+name)
 def sm(k,fn):
  r=copy.deepcopy(spec[k]);fn(r);c=cache[k];h.validate_selection(k,c['raw'],r,c['pages'],c['meta'])
 reject('omit final source address page',lambda:sm('L040',lambda r:r['page_bindings'].pop()))
 reject('remove source cover from primary input',lambda:sm('L040',lambda r:r['included_spans'][0].update(start=r['article_only_span']['start'])))
 reject('select only principal theorem spans',lambda:sm('L040',lambda r:r['included_spans'][0].update(end=10000)))
 reject('remove source abstract as page furniture',lambda:sm('L040',lambda r:r['excluded_furniture'][0].update(start=r['page_bindings'][1]['start'])))
 reject('remove substantive new common text',lambda:sm('U_ADD',lambda r:r['excluded_furniture'][0].update(start=0)))
 reject('omit source repeated header classification',lambda:sm('L040',lambda r:r['excluded_furniture'].pop()))
 reject('article sensitivity omits reference pages',lambda:sm('L040',lambda r:r['article_only_span'].update(end=50000)))
 reject('article sensitivity selects wrong first page',lambda:sm('L040',lambda r:r['article_only_span'].update(start=r['page_bindings'][2]['start'])))
 def gm(fn):
  r=copy.deepcopy(spec['L040']);fn(r);c=cache['L040'];h.validate_glyphs('L040',c['raw'],c['fonts'],c['pages'],c['events'],r,aliases)
 reject('drop visible control-decoded graph stroke',lambda:gm(lambda r:r['glyph_substitutions'].remove(next(x for x in r['glyph_substitutions'] if x['input']=='\x00'))))
 reject('invent full arrow from separate bar',lambda:gm(lambda r:next(x for x in r['glyph_substitutions'] if x['pdf_events'][0]['glyph_name']=='mapsto').update(output='↦')))
 reject('change actual font dictionary identity',lambda:gm(lambda r:r['glyph_substitutions'][0]['pdf_events'][0].update(font_identity='0'*64)))
 reject('change actual encoded byte',lambda:gm(lambda r:r['glyph_substitutions'][0]['pdf_events'][0].update(encoded_byte=255)))
 reject('duplicate one visible glyph repair',lambda:gm(lambda r:r['glyph_substitutions'].append(copy.deepcopy(r['glyph_substitutions'][0]))))
 reject('change bound local glyph context',lambda:gm(lambda r:r['glyph_substitutions'][0].update(context_sha256='0'*64)))
 def pm(fn):
  q=copy.deepcopy(p);fn(q);h.validate_policy(q)
 for name,fn in [
  ('count clauses as original manuscripts',lambda q:q.update(original_manuscripts_added=35)),
  ('invent a separate topic for L040',lambda q:q.update(new_topics=1)),
  ('discard old four B applications',lambda q:q.update(retain_all_four_old_applications=False)),
  ('deduct overlap from new common paper before reviewed unification',lambda q:q.update(new_common_whole_not_deduplicated=False)),
  ('omit complete old program bundle',lambda q:q.update(retain_complete_old_programs=False)),
  ('drop a complete validation file from printed cost',lambda q:q['programs'].pop(1)),
  ('promote finite validation to uniform premise',lambda q:q['programs'][1].update(role='required_finite_primitive_inputs')),
  ('omit auxiliary degree-eight program',lambda q:q.update(auxiliary_example_programs=0)),
  ('pay only principal required code before conditional result',lambda q:q.update(all_declared_code_prepurchased_for_conditional_results=False)),
  ('add raw and printed program costs together',lambda q:q.update(raw_and_printed_code_are_alternatives=False)),
  ('switch B primary away from full literal rendered and untrimmed PDFs',lambda q:q.update(primary='calibrated_selected')),
  ('zero unmeasured catalogue-construction cost',lambda q:q['unknown_costs'].update(primitive_catalogue_construction=0)),
  ('zero source graphic cost',lambda q:q['unknown_costs'].update(full_graphics=0)),
  ('claim full scientific Lean verification',lambda q:q.update(whole_source_formalized=True)),
  ('calculate factor before distinct input review',lambda q:q.update(factors_permitted=True)),
  ('omit full raw sensitivity',lambda q:q['variants'].pop(0))]:reject(name,lambda fn=fn:pm(fn))
 base='papers/topic-b/extensions/high-rank/v1/';tex=(args.public_root/(base+'program-appendix.tex')).read_text();pr={r['path'].removeprefix(base):h.bound(r,args)[1].decode() for r in p['programs']};t=cache['CODE']['texts']['raw_selected']
 reject('prune program by line ranges',lambda:h.code_inclusion(tex.replace('fontsize=','firstline=2,fontsize=',1),t,pr))
 reject('omit primitive catalogue program body',lambda:h.code_inclusion(tex,t.replace('PRIMITIVE_CATALOGUE','TRUNCATED'),pr))
 reject('omit validation program input',lambda:h.code_inclusion(tex.replace('programs/core_attachment.g','omitted.g'),t,pr))
 reject('omit auxiliary-example full text',lambda:h.code_inclusion(tex,t.replace('BOUNDARY_N8','TRUNCATED'),pr))
 return counts,audits,dict(status='PASS',controls=tests,controls_run_under_optimization=not __debug__,scientific_programs_executed=False)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();h.need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True);c,f,r=run(a)
 for n,o in [('counts.json',c),('font_audit.json',f),('controls.json',r)]:(a.out/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
 print('PASS',len(r['controls']),'controls; no factors.')
