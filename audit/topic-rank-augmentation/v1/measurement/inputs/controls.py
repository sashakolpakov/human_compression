#!/usr/bin/env python3
"""Bounded integrity controls on the input boundary and actual glyph events."""
import argparse,copy,json
from pathlib import Path
from extract_inputs import HERE,load,replay,validate_policy,calibrate,metrics
from font_tools import need

def run(root):
 result,cache=replay(root);p=load('policy.json');spec=load('input_spec.json');aliases=load('glyph_aliases.json')['aliases'];out=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError,IndexError):out.append(name);return
  raise ValueError('control accepted '+name)
 def policy(name,fn):
  q=copy.deepcopy(p);fn(q);reject(name,lambda:validate_policy(q))
 policy('drop counterproof application',lambda q:q['applications'].__setitem__('L020',['A1']))
 policy('drop common written cost',lambda q:q['written_documents'].remove('U'))
 policy('omit last source page',lambda q:q['documents']['L020'].__setitem__('pages',18))
 policy('retain old incomplete appendix',lambda q:q['documents']['CODE'].__setitem__('pages',2))
 policy('add old appendix',lambda q:q['programme_printed_alternative'].append('OLD'))
 policy('prune program file',lambda q:q['programs'].pop())
 policy('discard diagnostics',lambda q:q['programs'].pop(1))
 policy('promote bounded models to uniform premise',lambda q:q['programs'][1].__setitem__('logical_role','uniform_theorem_premise'))
 policy('omit operational driver',lambda q:q['operational_drivers'].pop())
 policy('omit inherited formal file',lambda q:q['formal_files'].pop())
 policy('misstate formal declaration count',lambda q:q.__setitem__('formal_declarations',2))
 policy('free earlier Topic B common',lambda q:q.__setitem__('old_Topic_B_common_free_premise',True))
 policy('conditional counterproof omitted',lambda q:q.__setitem__('conditional_policy','After whole common; local application only'))
 policy('unknown graphic cost zero',lambda q:q['unknown_costs'].__setitem__('graphics_and_layout',0))
 policy('invent numerical factor',lambda q:q.__setitem__('ratio',1))
 policy('silently change primary coordinate',lambda q:q['primary_coordinate'].__setitem__('variant','calibrated_selected'))
 c=cache['L020']
 def glyph(name,mut):
  q=copy.deepcopy(spec['L020']);mut(q);reject(name,lambda:calibrate(c['raw'],c['fonts'],c['pages'],c['events'],q,aliases,'L020'))
 glyph('omit printable script G calibration',lambda q:q['glyph_substitutions'].pop(0))
 glyph('blackboard symbol changed to roman',lambda q:next(g for g in q['glyph_substitutions'] if g['pdf_event']['glyph_name']=='N').__setitem__('output','N'))
 glyph('actual font dictionary changed',lambda q:q['glyph_substitutions'][0]['pdf_event']['font_dictionary_object'].__setitem__('idnum',47))
 glyph('actual encoded byte changed',lambda q:q['glyph_substitutions'][0]['pdf_event'].__setitem__('encoded_byte',78))
 glyph('source occurrence moved',lambda q:q['glyph_substitutions'][0].__setitem__('offset',0))
 glyph('context hash changed',lambda q:q['glyph_substitutions'][0].__setitem__('context_sha256','0'*64))
 reject('erase diagram-bearing source page',lambda:need(metrics(c['raw'][:c['pages'][5]['start']]+c['raw'][c['pages'][5]['end']:],'NFC')==result['documents']['L020']['metrics']['raw_untrimmed']['NFC'],'all vector labels/source page kept'))
 return dict(status='PASS_INPUT_CONTROLS',controls=out,count=len(out),scientific_programs_executed=False,factors_computed=False)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output');r=run(a.study_root);a.out.mkdir(parents=True);(a.out/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
