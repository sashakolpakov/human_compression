"""Boundary, glyph and whole-topic controls; all assertions fail closed under -O."""
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
 reject('omit the final source page',lambda:sm('L068',lambda r:r['page_bindings'].pop()))
 reject('replace full source by selected principal spans',lambda:sm('L128',lambda r:r['included_spans'][0].update(start=500)))
 reject('remove journal title and DOI as furniture',lambda:sm('L068',lambda r:r['excluded_furniture'].append(dict(page=1,start=0,end=100))))
 reject('remove authored application paragraph as footer',lambda:sm('C5',lambda r:r['excluded_furniture'][0].update(start=0)))
 reject('delete retained arXiv version banner',lambda:sm('L128',lambda r:r['excluded_furniture'][0].update(end=r['excluded_furniture'][0]['end']+100)))
 reject('omit source running-header classification',lambda:sm('L068',lambda r:r['excluded_furniture'].pop()))
 reject('repeat Form metadata callback',lambda:sm('L128',lambda r:r['extraction_metadata']['duplicate_callbacks'].clear()))
 def gm(k,fn):
  r=copy.deepcopy(spec[k]);fn(r);c=cache[k];h.validate_glyphs(k,c['raw'],c['fonts'],c['pages'],c['events'],r,aliases)
 envelope=lambda r:next(x for x in r['glyph_substitutions'] if x['input']=='/letter')
 reject('truncate multicharacter decoding of one envelope glyph',lambda:gm('L068',lambda r:envelope(r).update(end=envelope(r)['start']+1)))
 reject('count one envelope as seven letters',lambda:gm('L068',lambda r:envelope(r).update(output='✉'*7)))
 reject('drop envelope glyph',lambda:gm('L068',lambda r:r['glyph_substitutions'].remove(envelope(r))))
 reject('invent full arrow from mapsto bar component',lambda:gm('L068',lambda r:next(x for x in r['glyph_substitutions'] if x['pdf_events'][0]['glyph_name']=='mapsto').update(output='↦')))
 reject('omit actual whitespace-decoded delimiter',lambda:gm('L128',lambda r:r['glyph_substitutions'].remove(next(x for x in r['glyph_substitutions'] if x['input']=='\f'))))
 reject('classify real delimiter as generated whitespace',lambda:gm('L128',lambda r:r['extraction_metadata']['generated_newline_offsets'].append(next(x for x in r['glyph_substitutions'] if x['input']=='\f')['start'])))
 reject('guess substitute from mathematical context',lambda:gm('L068',lambda r:r['glyph_substitutions'][0].update(output='x')))
 reject('change actual font identity',lambda:gm('L068',lambda r:r['glyph_substitutions'][0]['pdf_events'][0].update(font_identity='0'*64)))
 reject('change encoded byte',lambda:gm('L128',lambda r:r['glyph_substitutions'][0]['pdf_events'][0].update(encoded_byte=255)))
 reject('duplicate one actual glyph repair',lambda:gm('L128',lambda r:r['glyph_substitutions'].append(copy.deepcopy(r['glyph_substitutions'][0]))))
 reject('change glyph context',lambda:gm('L068',lambda r:r['glyph_substitutions'][0].update(context_sha256='0'*64)))
 def pm(fn):
  q=copy.deepcopy(p);fn(q);h.validate_policy(q)
 for name,fn in [
  ('count scientific clauses as original manuscripts',lambda q:q.update(original_manuscripts_added=31)),
  ('invent independent topic for each extension',lambda q:q.update(new_topic_count=2)),
  ('drop old exhaustive J1 census',lambda q:q['old_C_required_programs'].pop()),
  ('omit complete incidence common note',lambda q:q['whole_topic_rules']['C'].update(additional_common=[])),
  ('double-charge shared phase40 construction program',lambda q:q['whole_topic_rules']['C'].update(shared_existing_file_charged_once=False)),
  ('discard earlier C applications',lambda q:q['whole_topic_rules']['C'].update(retain_all_previous_applications=False)),
  ('give A its full umbrella for free',lambda q:q['whole_topic_rules']['A'].update(retain_full_previous_common=False)),
  ('omit old complete code appendix',lambda q:q['whole_topic_rules']['A'].update(old_program_bundle_retained=False)),
  ('omit whole new required program',lambda q:q['new_programs'].pop()),
  ('silently zero full graphics',lambda q:q['unknown_costs'].update(full_graphics=0)),
  ('silently zero retained external proofs',lambda q:q['unknown_costs'].update(external=0)),
  ('claim entire applications formally verified',lambda q:q.update(full_formalization_claim=True)),
  ('calculate factor before distinct input review',lambda q:q.update(factors_permitted=True)),
  ('omit untrimmed sensitivity',lambda q:q['variants'].pop(0)),
  ('switch C primary from literal complete representation',lambda q:q.update(C_primary='calibrated_selected'))]:reject(name,lambda fn=fn:pm(fn))
 tex=(h.H/'livingstone_additional_program.tex').read_text();code=h.bound(p['new_programs'][1],args)[1].decode();txt=cache['C_CODE_NEW']['texts']['raw_selected'];name='programs/phase179_livingstone_check.g'
 reject('prune whole required program to selected lines',lambda:h.code_inclusion(tex.replace('fontsize=','firstline=2,fontsize=',1),txt,code,name))
 reject('omit full literal program body',lambda:h.code_inclusion(tex,txt.replace('L068_P_AND_REPAIRED_Q_BRIDGE_PASS','TRUNCATED'),code,name))
 reject('substitute another program',lambda:h.code_inclusion(tex.replace(name,'different.g'),txt,code,name))
 return counts,audits,dict(status='PASS',controls=tests,controls_run_under_optimization=not __debug__,scientific_programs_executed=False)

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();h.need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 c,f,r=run(a)
 for n,o in [('counts.json',c),('font_audit.json',f),('controls.json',r)]:(a.out/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
 print('PASS',len(r['controls']),'controls; 210 PDF/80 raw cells, no factors.')
