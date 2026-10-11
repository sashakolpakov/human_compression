"""Boundary, actual-event and whole-software mutation controls; works under -O."""
from pathlib import Path
import copy,json,argparse
import extract_inputs as h

def run(args):
 counts,audits,caches=h.replay(args);p=h.load('policy.json');spec=h.load('input_spec.json');aliases=h.load('glyph_aliases.json')['aliases'];tests=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError,IndexError,TypeError):tests.append(dict(name=name,rejected=True));return
  raise ValueError('CONTROL NOT REJECTED: '+name)
 def sm(key,fn):
  row=copy.deepcopy(spec[key]);fn(row);c=caches[key];h.validate_selection(key,c['raw'],row,c['pages'],c['meta'])
 for k in ['N007','N006']:
  reject('drop last source page '+k,lambda k=k:sm(k,lambda r:r['page_bindings'].pop()))
  reject('select principal proof only '+k,lambda k=k:sm(k,lambda r:r['included_spans'][0].update(start=500)))
  reject('drop version banner '+k,lambda k=k:sm(k,lambda r:r['excluded_furniture'][0].update(end=r['excluded_furniture'][0]['end']+50)))
 reject('remove application body as furniture',lambda:sm('A2HN',lambda r:r['excluded_furniture'][0].update(start=0)))
 reject('count duplicate Form callback as extra banner',lambda:sm('N007',lambda r:r['extraction_metadata']['duplicate_callbacks'].clear()))
 def gm(key,fn):
  r=copy.deepcopy(spec[key]);fn(r);c=caches[key];h.calibrate(c['raw'],c['fonts'],c['pages'],c['events'],r,aliases,key)
 first=lambda r:r['glyph_substitutions'][0]
 for key in ['N007','N006']:
  for label,fn in [('font dictionary',lambda r:first(r)['pdf_event'].update(font_identity='0'*64)),('encoded byte',lambda r:first(r)['pdf_event'].update(encoded_byte=255)),('context',lambda r:first(r).update(context_sha256='0'*64)),('duplicate event',lambda r:r['glyph_substitutions'].append(copy.deepcopy(first(r)))),('unbound symbol',lambda r:first(r).update(output='x'))]:
   reject('change '+label+' '+key,lambda key=key,fn=fn:gm(key,fn))
 def glyph(r,name):return next(x for x in r['glyph_substitutions'] if x['pdf_event']['glyph_name']==name)
 reject('drop actual whitespace-decoded angle',lambda:gm('N007',lambda r:r['glyph_substitutions'].remove(next(x for x in r['glyph_substitutions'] if x['input_codepoint']=='U+000A'))))
 reject('visible angle becomes generated newline',lambda:gm('N007',lambda r:r['extraction_metadata']['generated_newline_offsets'].append(next(x['offset'] for x in r['glyph_substitutions'] if x['input_codepoint']=='U+000A'))))
 reject('collapse eight circle fragments into a single glyph',lambda:gm('N006',lambda r:glyph(r,'c16').update(output='')))
 reject('curve assigned to wrong quadrant',lambda:gm('N006',lambda r:glyph(r,'c16').update(output='◝')))
 reject('underbrace tip silently omitted',lambda:gm('N006',lambda r:r['glyph_substitutions'].remove(glyph(r,'bracehtipdownleft'))))
 reject('proxy disguised as literal symbol',lambda:gm('N006',lambda r:glyph(r,'c16').update(kind='visible_symbol')))
 reject('large product decoded as letter Q',lambda:gm('N006',lambda r:glyph(r,'producttext').update(output='Q')))
 reject('mapsto bar changed to combined arrow',lambda:gm('N007',lambda r:glyph(r,'mapsto').update(output='↦')))
 def pm(fn):
  q=copy.deepcopy(p);fn(q);h.validate_policy(q)
 for name,fn in [
  ('clauses counted as originals',lambda q:q.update(original_manuscripts=59)),
  ('omit HN companion',lambda q:q['replacements'].pop('A2HN')),
  ('omit nine-case companion',lambda q:q['replacements'].pop('A2nine')),
  ('old common theory substituted',lambda q:q['replacements']['U'].update(pages=5)),
  ('omit full witness file',lambda q:q['programs'].pop(9)),
  ('omit full validation file',lambda q:q['programs'].pop(0)),
  ('omit required decoding driver',lambda q:q['required_drivers'].pop()),
  ('duplicate same raw program',lambda q:q['programs'].__setitem__(0,copy.deepcopy(q['programs'][1]))),
  ('finite proof file mislabeled validation',lambda q:q['programs'][2].update(role='validation')),
  ('full graphics priced zero',lambda q:q['unknown_costs'].update(full_graphics=0)),
  ('external classification priced zero',lambda q:q['unknown_costs'].update(retained_classification_proofs=0)),
  ('proxy declared literal Unicode',lambda q:q['diagram_proxy_policy'].update(literal_unicode_extraction=True)),
  ('text-only alternative suppressed',lambda q:q['diagram_proxy_policy'].update(text_only_alternative=False)),
  ('raw sensitivity suppressed',lambda q:q['variants'].pop(0)),
  ('later Fischer exceptions added',lambda q:q['source_exceptions_outside_this_edition'].clear()),
  ('factor before input adoption',lambda q:q.update(factors_permitted=True)),
  ('new question credit',lambda q:q.update(new_question_credit=1)),
  ('reused eight Lean declarations counted twice',lambda q:q.update(partial_formal_declarations=25))]:reject(name,lambda fn=fn:pm(fn))
 def em(fn):
  e=copy.deepcopy(h.load('external_data.json'));fn(e);h.validate_external(e)
 reject('external binary data omitted',lambda:em(lambda e:e['inputs'].pop()))
 reject('compact word discount',lambda:em(lambda e:e.update(compact_word_discount=True)))
 reject('installed data silently dropped',lambda:em(lambda e:e['installed_files_once_by_identical_hash'].pop()))
 tex=(args.public_root/'papers/topic-diagonal/v1/programs.tex').read_text();code=h.bound(p['programs'][-1],args)[1].decode();txt=caches['CODEold']['texts']['raw_selected']
 reject('old validation appendix pruned',lambda:h.code_inclusion(tex.replace('fontsize=','firstline=2,fontsize=',1),txt,code))
 reject('old validation body truncated',lambda:h.code_inclusion(tex,txt.replace('DIAGONAL_MODELS_COMPLETE','TRUNCATED'),code))
 return counts,audits,dict(status='PASS',controls=tests,controls_run_under_optimization=not __debug__,scientific_programs_executed=False)

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--public-root',type=Path,required=True);a.add_argument('--sources-root',type=Path,required=True);a.add_argument('--out',type=Path,required=True);args=a.parse_args();h.need(not args.out.exists() and not args.out.is_symlink(),'fresh output');args.out.mkdir(parents=True)
 counts,audits,report=run(args)
 for name,obj in [('counts.json',counts),('font_audit.json',audits),('controls.json',report)]:(args.out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 print('PASS',len(report['controls']),'controls; no factors.')
