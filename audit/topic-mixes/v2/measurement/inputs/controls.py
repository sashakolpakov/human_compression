"""Fail-closed boundary and glyph controls; no scientific execution."""
from copy import deepcopy
import extract_inputs as E
from font_tools import embedded,validate_unembedded_banner

def run(args,cache):
 rejected=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError,IndexError)as e:rejected.append(dict(name=name,message=str(e)));return
  raise ValueError('CONTROL_ACCEPTED: '+name)
 p=E.load('policy.json')
 def policy(name,edit):
  q=deepcopy(p);edit(q);reject(name,lambda:E.validate_policy(q))
 for name,edit in [
 ('omit new common paper',lambda q:q['replacements'].pop('U1')),
 ('omit new complete application',lambda q:q['replacements'].pop('A3')),
 ('omit prior whole common paper',lambda q:q['whole_topic_boundary']['common_documents'].pop(0)),
 ('omit prior exceptional application',lambda q:q['whole_topic_boundary']['applications']['MX1'].pop()),
 ('omit prior source',lambda q:q['whole_topic_boundary']['source_documents'].pop(0)),
 ('drop source reference page',lambda q:q['source'].__setitem__('pages',11)),
 ('shorten new application',lambda q:q['replacements']['A3'].__setitem__('pages',5)),
 ('free prior common theory',lambda q:q['whole_topic_boundary'].__setitem__('whole_U5_paid_once',False)),
 ('discount overlapping theories',lambda q:q.__setitem__('overlap_discount',True)),
 ('register new singleton',lambda q:q.__setitem__('registered_new_topic',True)),
 ('omit earlier required certificate',lambda q:q['whole_topic_boundary']['required_raw_programs'].pop(0)),
 ('demote required certificate',lambda q:q['programs'][0].__setitem__('mathematical_premise',False)),
 ('promote optional validation',lambda q:q['programs'][1].__setitem__('mathematical_premise',True)),
 ('asymmetric optional comparison',lambda q:q.__setitem__('optional_validation_comparison','replacement-only charge is a compression factor')),
 ('add printed and raw forms',lambda q:q.__setitem__('printed_raw_alternatives_never_additive',False)),
 ('omit operational driver',lambda q:q['drivers'].pop()),
 ('claim full formalization',lambda q:q.__setitem__('end_to_end_formalization',True)),
 ('unknown historical software zero',lambda q:q.__setitem__('source_historical_software_cost',0)),
 ('unknown graphics zero',lambda q:q['unknown_costs'].__setitem__('full_graphics',0)),
 ('drop retained-proof unknown',lambda q:q['unknown_costs'].pop('retained_external_proofs')),
 ('change primary',lambda q:q.__setitem__('primary','calibrated_selected/NFC/characters_without_whitespace')),
 ('omit raw variant',lambda q:q['variants'].remove('raw_untrimmed')),
 ('permit premature factors',lambda q:q.__setitem__('factors_permitted',True)),
 ('new source credit',lambda q:q.__setitem__('new_scientific_credit',1))]:policy(name,edit)
 science=E.load('source_boundary.json');q=deepcopy(science)
 next(x for x in q['topic_Mix_L016_recovery/scope.json']['source_rows']if x['id']=='B3')['disposition']='unqualified_recovery'
 reject('erase literal Lemma3.5 correction',lambda:E.validate_science(q))
 q=deepcopy(science);q['topic_Mix_L016_root_adoption/review.json']['excluded_ancillary_or_unanswered'].pop()
 reject('hide ancillary or unanswered exclusion',lambda:E.validate_science(q))
 q=E.load('source_code_boundary.json');q['source_only_executable_charge']=True
 reject('count only source executable',lambda:E.validate_source_code_boundary(q))
 q=E.load('source_code_boundary.json');q['sources']['F005']['source_software_cost']=0
 reject('unavailable source verification priced zero',lambda:E.validate_source_code_boundary(q))
 accepted=__import__('json').loads(E.bound(p['reused_accepted_inputs']['counts'],args)[1]);q=deepcopy(accepted)
 q['documents']['U']['metrics']['raw_untrimmed']['NFC']['characters_without_whitespace']-=1
 reject('revise accepted F005 cell',lambda:E.validate_retained(q,accepted))
 spec=E.load('input_spec.json');aliases=E.load('glyph_aliases.json')['aliases'];c=cache['L016'];r=spec['L016']
 def selection(name,edit):
  q=deepcopy(r);edit(q);reject(name,lambda:E.validate_selection('L016',c['raw'],q,c['pages'],c['meta']))
 selection('omit whole body',lambda q:q.__setitem__('included_spans',[]))
 selection('omit physical page',lambda q:q['page_bindings'].pop())
 selection('delete body as furniture',lambda q:q['excluded_furniture'][0].__setitem__('start',0))
 selection('alter literal extraction',lambda q:q.__setitem__('extraction_sha256','0'*64))
 def glyph(name,edit):
  q=deepcopy(r);edit(q);reject(name,lambda:E.validate_glyphs('L016',c['raw'],c['fonts'],c['pages'],c['events'],q,aliases))
 glyph('change observed glyph',lambda q:q['glyph_substitutions'][0].__setitem__('output','X'))
 glyph('drop observed occurrence',lambda q:q['glyph_substitutions'].pop())
 glyph('duplicate glyph occurrence',lambda q:q['glyph_substitutions'].append(deepcopy(q['glyph_substitutions'][0])))
 glyph('change actual encoded byte',lambda q:q['glyph_substitutions'][0]['pdf_events'][0].__setitem__('encoded_byte',0))
 glyph('change local glyph context',lambda q:q['glyph_substitutions'][0].__setitem__('context_sha256','0'*64))
 glyph('expand one glyph into guessed symbols',lambda q:q['glyph_substitutions'][0].__setitem__('output','XX'))
 for key,texname in [('REQ','required_program.tex'),('VAL','optional_validation.tex')]:
  rows=[x for x in p['programs']if x['printed_document']==key]
  if key=='REQ':rows=[p['required_printed_reused_program']]+rows
  pr={x['printed_path']:E.bound(x,args)[1].decode()for x in rows};cc=cache[key];tex=(E.H/texname).read_text()
  def printed(t=tex,programs=pr):return E.code_inclusion(t,cc['raw'],programs,cc['events'],spec[key]['excluded_furniture'])
  reject('prune printed '+key,lambda:printed(tex.replace('fontsize=','firstline=2,fontsize=',1)))
  q=deepcopy(pr);q[next(iter(q))]+='\nMISSING_COMPLETE_PROGRAM_SENTINEL;';reject('omit full program bytes '+key,lambda:printed(programs=q))
 reject('unsupported unembedded font',lambda:embedded({'/Subtype':'/Type1','/BaseFont':'/Helvetica'}))
 reject('nonASCII unembedded banner',lambda:validate_unembedded_banner(200,'È'))
 reject('wrong literal banner decoding',lambda:validate_unembedded_banner(65,'B'))
 q=deepcopy(p['source']);q['sha256']='0'*64;reject('changed source PDF',lambda:E.bound(q,args))
 return dict(status='PASS',python_optimization_safe=True,rejected=len(rejected),controls=rejected,scientific_programs_executed=False,factors_evaluated=False)
