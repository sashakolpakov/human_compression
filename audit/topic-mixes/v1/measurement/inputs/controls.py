"""Negative input controls; no scientific GAP or Lean execution."""
from copy import deepcopy
import re
import extract_inputs as E
from font_tools import embedded,validate_unembedded_banner

def run(args,cache):
 rejected=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError,IndexError) as e:rejected.append(dict(name=name,message=str(e)));return
  raise ValueError('CONTROL_ACCEPTED: '+name)
 p=E.load('policy.json')
 def policy(name,edit):
  q=deepcopy(p);edit(q);reject(name,lambda:E.validate_policy(q))
 for name,edit in [
 ('drop complete common paper',lambda q:q['replacements'].pop('U')),
 ('drop additive exception proof',lambda q:q['replacements'].pop('A2')),
 ('drop second complete appendix',lambda q:q['replacements'].pop('CODE2')),
 ('shorten main application',lambda q:q['replacements']['A1'].__setitem__('pages',7)),
 ('drop source reference page',lambda q:q['source'].__setitem__('pages',20)),
 ('discount common theory',lambda q:q.__setitem__('whole_common_papers_charged',False)),
 ('make exception a free prior result',lambda q:q.__setitem__('whole_additive_application_charged',False)),
 ('discount overlap',lambda q:q.__setitem__('overlap_discount',True)),
 ('cross-topic discount',lambda q:q.__setitem__('cross_topic_discount',True)),
 ('omit required computation',lambda q:q['programs'].pop(0)),
 ('demote finite premise to diagnostic',lambda q:q['programs'][0].__setitem__('role','finite_validation')),
 ('promote validation to uniform premise',lambda q:q['programs'][1].__setitem__('uniform_mathematical_premise',True)),
 ('drop driver inventory',lambda q:q['drivers'].pop()),
 ('claim full formalization',lambda q:q.__setitem__('whole_source_formalized',True)),
 ('omit all-program prepayment',lambda q:q.__setitem__('all_declared_code_prepurchased_for_conditional_results',False)),
 ('charge both printed and raw code',lambda q:q.__setitem__('raw_and_printed_code_are_alternatives',False)),
 ('unknown graphics becomes zero',lambda q:q['unknown_costs'].__setitem__('full_graphics',0)),
 ('omit retained proof unknown',lambda q:q['unknown_costs'].pop('retained_external_proofs')),
 ('change primary after counts',lambda q:q.__setitem__('primary','calibrated_selected')),
 ('allow premature factor',lambda q:q.__setitem__('factors_permitted',True)),
 ('claim unanswered problems solved',lambda q:q.__setitem__('source_questions_excluded',0)),
 ('omit raw sensitivity',lambda q:q['variants'].remove('raw_untrimmed'))]:policy(name,edit)
 spec=E.load('input_spec.json');aliases=E.load('glyph_aliases.json')['aliases'];c=cache['F005'];r=spec['F005']
 def selection(name,edit):
  q=deepcopy(r);edit(q);reject(name,lambda:E.validate_selection('F005',c['raw'],q,c['pages'],c['meta']))
 selection('drop whole-body span',lambda q:q.__setitem__('included_spans',[]))
 selection('omit one physical page',lambda q:q['page_bindings'].pop())
 selection('delete body as furniture',lambda q:q['excluded_furniture'][0].__setitem__('start',0))
 selection('change full extraction',lambda q:q.__setitem__('extraction_sha256','0'*64))
 def glyph(name,edit):
  q=deepcopy(r);edit(q);reject(name,lambda:E.validate_glyphs('F005',c['raw'],c['fonts'],c['pages'],c['events'],q,aliases))
 glyph('change observed output',lambda q:q['glyph_substitutions'][0].__setitem__('output','X'))
 glyph('drop observed occurrence',lambda q:q['glyph_substitutions'].pop())
 glyph('duplicate occurrence',lambda q:q['glyph_substitutions'].append(deepcopy(q['glyph_substitutions'][0])))
 glyph('change original font byte',lambda q:q['glyph_substitutions'][0]['pdf_events'][0].__setitem__('encoded_byte',0))
 glyph('change observed context',lambda q:q['glyph_substitutions'][0].__setitem__('context_sha256','0'*64))
 glyph('invent expanded symbol',lambda q:q['glyph_substitutions'][0].__setitem__('output','XX'))
 for key in ['CODE1','CODE2']:
  rows=[x for x in p['programs'] if x['printed_document']==key];pr={x['printed_path']:E.bound(x,args)[1].decode() for x in rows};cc=cache[key]
  texrow=next(x for x in p['scientific_bindings'] if x['path']==p['replacements'][key]['path'].replace('.pdf','.tex'))
  tex=E.bound(texrow,args)[1].decode()
  def printed(t=tex,programs=pr):return E.code_inclusion(t,cc['raw'],programs,cc['events'],spec[key]['excluded_furniture'])
  reject('prune printed '+key,lambda:printed(tex.replace('fontsize=\\scriptsize','firstline=2,fontsize=\\scriptsize',1)))
  q=deepcopy(pr);q[next(iter(q))]+='\nMISSING_COMPLETE_PROGRAM_SENTINEL;';reject('omit full raw contents '+key,lambda:printed(programs=q))
 reject('unsupported unembedded font',lambda:embedded({'/Subtype':'/Type1','/BaseFont':'/Helvetica'}))
 reject('nonASCII unembedded banner',lambda:validate_unembedded_banner(200,'È'))
 reject('wrong literal banner decoding',lambda:validate_unembedded_banner(65,'B'))
 q=deepcopy(p['source']);q['sha256']='0'*64;reject('changed complete source',lambda:E.bound(q,args))
 return dict(status='PASS',python_optimization_safe=True,rejected=len(rejected),controls=rejected,scientific_programs_executed=False,factors_evaluated=False)
