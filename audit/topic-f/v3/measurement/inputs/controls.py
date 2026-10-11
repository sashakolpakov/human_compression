#!/usr/bin/env python3
"""Scope and encoded-event rejection controls; no mathematical execution."""
import argparse,copy,json
from pathlib import Path
from extract_inputs import load,replay,validate_policy,calibrate,metrics,check_appendix
from calibration import aliases_from
from font_tools import need

def run(root):
 result,cache=replay(root);p=load('policy.json');spec=load('input_spec.json');aliases=load('glyph_aliases.json')['aliases'];out=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError,IndexError):out.append(name);return
  raise ValueError('control accepted '+name)
 def policy(name,fn):
  q=copy.deepcopy(p);fn(q);reject(name,lambda:validate_policy(q))
 policy('omit L014 original',lambda q:q['source_ids'].pop(0))
 policy('omit last accepted source page',lambda q:q['documents']['L007'].__setitem__('pages',21))
 policy('drop old application',lambda q:q['written_documents'].remove('A1'))
 policy('drop common paper',lambda q:q['written_documents'].remove('U'))
 policy('shorten new application',lambda q:q['documents']['A2'].__setitem__('pages',5))
 policy('replace full appendix by old four pages',lambda q:q['documents']['CODE'].__setitem__('pages',4))
 policy('add old appendix to new',lambda q:q['programme_printed_alternative'].append('OLD'))
 policy('prune validation file',lambda q:q['programs'].pop())
 policy('duplicate program instead of full roster',lambda q:q['programs'].__setitem__(0,q['programs'][1]))
 policy('promote sample to uniform premise',lambda q:q['programs'][1].__setitem__('logical_role','uniform_proof'))
 policy('discard exploratory scan',lambda q:q['programs'].pop(2))
 policy('omit operational driver',lambda q:q['operational_drivers'].pop())
 policy('omit inherited formal file',lambda q:q['formal_files'].pop(1))
 policy('claim twelve new declarations',lambda q:q.__setitem__('new_formal_declarations',12))
 policy('claim source instance formalized',lambda q:q['formal_files'][2].__setitem__('source_specific_instance',True))
 policy('free old theory',lambda q:q.__setitem__('old_Topic_F_common_free_premise',True))
 policy('conditional without all programs',lambda q:q.__setitem__('conditional_policy','After U only'))
 policy('unknown graphics assigned zero',lambda q:q['unknown_costs'].__setitem__('source_graphics_and_formula_layout',0))
 policy('unapproved factor',lambda q:q.__setitem__('ratio',2))
 policy('change primary after seeing counts',lambda q:q['primary_coordinate'].__setitem__('variant','calibrated_selected'))
 c=cache['L007']
 def glyph(name,mut):
  q=copy.deepcopy(spec['L007']);mut(q);reject(name,lambda:calibrate(c['raw'],c['fonts'],c['pages'],c['events'],q,aliases,'L007'))
 glyph('omit visible parenthesis control repair',lambda q: q['glyph_substitutions'].pop(next(i for i,g in enumerate(q['glyph_substitutions']) if g['pdf_event']['glyph_name']=='parenleftbig')))
 glyph('blackboard N changed to roman',lambda q:next(g for g in q['glyph_substitutions'] if g['pdf_event']['glyph_name']=='N').__setitem__('output','N'))
 glyph('actual dictionary object changed',lambda q:q['glyph_substitutions'][0]['pdf_event']['font_dictionary_object'].__setitem__('idnum',999))
 glyph('effective encoding changed',lambda q:q['glyph_substitutions'][0]['pdf_event'].__setitem__('effective_encoding_sha256','0'*64))
 glyph('original byte changed',lambda q:q['glyph_substitutions'][0]['pdf_event'].__setitem__('encoded_byte',255))
 glyph('occurrence moved',lambda q:q['glyph_substitutions'][0].__setitem__('offset',0))
 glyph('context changed',lambda q:q['glyph_substitutions'][0].__setitem__('context_sha256','0'*64))
 glyph('repair hidden as furniture',lambda q:q['excluded_furniture'].append(dict(start=q['glyph_substitutions'][0]['offset'],end=q['glyph_substitutions'][0]['offset']+1)))
 bad=load('font_audit.json');bad['L007']['encoded_glyph_classes'][0]['font_identity']='0'*64
 reject('changed full glyph audit',lambda:need(bad==load('font_audit.json'),'complete audit equality'))
 reject('remove all watermarks from primary',lambda:need(metrics(c['raw'].replace('Accepted manuscript',''),'NFC')==result['documents']['L007']['metrics']['raw_untrimmed']['NFC'],'literal primary'))
 reject('remove reference-only final page',lambda:need(metrics(c['raw'][:c['pages'][-1]['start']],'NFC')==result['documents']['L007']['metrics']['raw_untrimmed']['NFC'],'whole source refs'))
 tex=(root/'topic_F_L007_recovery/volume/program-appendix.tex').read_text();files={Path(r['path']).name:(root/r['path']).read_text() for r in p['programs']}
 reject('omit whole program from printed inclusion',lambda:check_appendix(tex.replace('{programs/central_lift.g}','{programs/MISSING.g}'),files,cache['CODE']))
 q=copy.deepcopy(cache['CODE']);q['texts']['raw_selected']=q['texts']['raw_selected'].replace('Exact mixed-modulus','Removed')
 reject('alter printed program content',lambda:check_appendix(tex,files,q))
 return dict(status='PASS_INPUT_CONTROLS',count=len(out),controls=out,scientific_programs_executed=False,factors_computed=False)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output');r=run(a.study_root);a.out.mkdir(parents=True);(a.out/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
