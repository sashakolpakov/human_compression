"""Fail-closed boundary and actual-glyph controls, including Python -O."""
import copy,json,argparse
from pathlib import Path
import extract_inputs as h

def run(args):
 counts,audits,caches=h.replay(args);p=h.load('policy.json');spec=h.load('input_spec.json');aliases=h.load('glyph_aliases.json')['aliases'];tests=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError,IndexError,TypeError):tests.append(dict(name=name,rejected=True));return
  raise ValueError('CONTROL NOT REJECTED: '+name)
 def sm(key,fn):
  r=copy.deepcopy(spec[key]);fn(r);c=caches[key];h.validate_selection(key,c['raw'],r,c['pages'],c['meta'])
 reject('drop source reference page',lambda:sm('N007',lambda r:r['page_bindings'].pop()))
 reject('select only a principal proof span',lambda:sm('N007',lambda r:r['included_spans'][0].update(start=500)))
 reject('remove authored application text as footer',lambda:sm('A1',lambda r:r['excluded_furniture'][0].update(start=0)))
 reject('delete the retained arXiv version banner',lambda:sm('N007',lambda r:r['excluded_furniture'][0].update(end=r['excluded_furniture'][0]['end']+50)))
 reject('omit repeated running header classification',lambda:sm('N007',lambda r:r['excluded_furniture'].pop()))
 reject('count repeated Form visitor callback as second stamp',lambda:sm('N007',lambda r:r['extraction_metadata']['duplicate_callbacks'].clear()))
 c=caches['N007'];r0=spec['N007']
 def gm(fn):
  r=copy.deepcopy(r0);fn(r);h.calibrate(c['raw'],c['fonts'],c['pages'],c['events'],r,aliases)
 def actual_left(r):return next(x for x in r['glyph_substitutions'] if x['input_codepoint']=='U+000A')
 reject('omit visible newline-decoded left angle',lambda:gm(lambda r:r['glyph_substitutions'].remove(actual_left(r))))
 reject('misclassify actual left angle as generated newline',lambda:gm(lambda r:r['extraction_metadata']['generated_newline_offsets'].append(actual_left(r)['offset'])))
 reject('omit visible vertical extender',lambda:gm(lambda r:r['glyph_substitutions'].remove(next(x for x in r['glyph_substitutions'] if x['input_codepoint']=='U+000C'))))
 reject('invent combined arrow for mapsto bar piece',lambda:gm(lambda r:next(x for x in r['glyph_substitutions'] if x['pdf_event']['glyph_name']=='mapsto').update(output='↦')))
 reject('remove a visible graph stroke',lambda:gm(lambda r:next(x for x in r['glyph_substitutions'] if 'XYDASH' in x['input_font']).update(output='')))
 reject('replace source literal glyph with guessed mathematics',lambda:gm(lambda r:r['glyph_substitutions'][0].update(output='x')))
 reject('change actual font dictionary identity',lambda:gm(lambda r:r['glyph_substitutions'][0]['pdf_event'].update(font_identity='0'*64)))
 reject('change actual encoded byte',lambda:gm(lambda r:r['glyph_substitutions'][0]['pdf_event'].update(encoded_byte=255)))
 reject('double-count a glyph repair',lambda:gm(lambda r:r['glyph_substitutions'].append(copy.deepcopy(r['glyph_substitutions'][0]))))
 reject('change bound glyph context',lambda:gm(lambda r:r['glyph_substitutions'][0].update(context_sha256='0'*64)))
 pdf=h.bound(p['source'],args)[0]
 def alignment_mut(fn):
  meta=copy.deepcopy(c['meta']);fn(meta);h.source_events(pdf,c['raw'],c['fonts'],c['pages'],meta)
 reject('actual font alignment loses real left angle',lambda:alignment_mut(lambda m:m['generated_newline_offsets'].append(actual_left(r0)['offset'])))
 def missing_synthetic(m):
  i=next(i for i in m['generated_newline_offsets'] if 'CMEX' in c['fonts'][i]);m['generated_newline_offsets'].remove(i)
 reject('actual font alignment treats generated newline as visible angle',lambda:alignment_mut(missing_synthetic))
 def pm(fn):
  q=copy.deepcopy(p);fn(q);h.validate_policy(q)
 for name,fn in [
  ('count clauses as originals',lambda q:q.update(original_manuscripts=32)),
  ('silently claim N006 complete recovery',lambda q:q.update(N006_whole_original_credit=1)),
  ('omit full validation program',lambda q:q['programs'].clear()),
  ('validation becomes required uniform premise',lambda q:q.update(required_finite_programs=1)),
  ('silently zero full graphics',lambda q:q.update(graphics_cost=0)),
  ('silently zero retained external proofs',lambda q:q.update(retained_external_cost=0)),
  ('claim full geometry formalization',lambda q:q.update(full_formalization_claim=True)),
  ('calculate factor before distinct input acceptance',lambda q:q.update(factors_permitted=True)),
  ('omit full raw sensitivity',lambda q:q['variants'].pop(0))]:reject(name,lambda fn=fn:pm(fn))
 tex=(args.public_root/'papers/topic-diagonal/v1/programs.tex').read_text();code=h.bound(p['programs'][0],args)[1].decode();pdftext=caches['CODE']['texts']['raw_selected']
 reject('prune code by line range',lambda:h.code_inclusion(tex.replace('fontsize=','firstline=2,fontsize=',1),pdftext,code))
 reject('omit full literal code body',lambda:h.code_inclusion(tex,pdftext.replace('DIAGONAL_MODELS_COMPLETE','TRUNCATED'),code))
 reject('substitute different program',lambda:h.code_inclusion(tex.replace('diagonal_models.g','different.g'),pdftext,code))
 return counts,audits,dict(status='PASS',controls=tests,controls_run_under_optimization=not __debug__,scientific_programs_executed=False)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();h.need(not args.out.exists(),'fresh output');args.out.mkdir(parents=True)
 counts,audits,report=run(args)
 for name,obj in [('counts.json',counts),('font_audit.json',audits),('controls.json',report)]:(args.out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 print('PASS',len(report['controls']),'controls; no factors.')
if __name__=='__main__':main()
