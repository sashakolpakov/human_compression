"""Bounded wrong-boundary/event controls; no scientific computation."""
from copy import deepcopy
from extract_inputs import *
def run(result,cache):
 rejected=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError,TypeError,IndexError):rejected.append(name);return
  raise RuntimeError('NEGATIVE CONTROL ACCEPTED: '+name)
 p=load('policy.json')
 def policy(name,fn):
  q=deepcopy(p);fn(q);reject(name,lambda:validate_policy(q))
 policy('drop earlier source',lambda q:q['originals'].pop(0))
 policy('drop companion application',lambda q:q['whole_topic_boundary']['applications']['F007'].pop())
 policy('free old common',lambda q:q['whole_topic_boundary']['common_documents'].pop(0))
 policy('selected rather than raw primary',lambda q:q.update(primary='calibrated_selected/NFC/characters_without_whitespace'))
 policy('omit reference-only companion page',lambda q:q['new_documents']['A5'].update(pages=3))
 policy('drop required certificate',lambda q:q['software_boundary']['required_full_programs'].pop())
 policy('diagnostic promoted to premise',lambda q:q['software_boundary']['optional_full_programs'][-1].update(mathematical_premise=True))
 policy('full formalization claim',lambda q:q['software_boundary'].update(full_source_formalized=True))
 policy('optional validation required for conditional',lambda q:q['symmetry'].update(optional_validation_is_not_a_conditional_prerequisite=False))
 policy('unknown software assigned zero',lambda q:q['symmetry'].update(unprovided_historical_software=0))
 policy('software compression figure inserted',lambda q:q['symmetry'].update(software_inclusive_factor=1))
 policy('Problem3 infinite arbitrary claim',lambda q:q['scope'].update(F007_problem3='all infinite isomorphisms'))
 policy('source p25 paragraph claimed recovered',lambda q:q['scope'].update(F007_page25_chain_class_paragraph='recovered'))
 policy('one program counted in two roles',lambda q:q['software_boundary'].update(dual_role_companion_checker_charged_once=False))
 policy('overlap discount',lambda q:q.update(overlap_discount=True))
 c=cache['F007'];s=load('input_spec.json')['F007'];a=load('glyph_aliases.json')['aliases']
 def glyph(name,fn):
  ss,ee,aa=deepcopy(s),deepcopy(c['events']),deepcopy(a);fn(ss,ee,aa);reject(name,lambda:validate_glyphs('F007',c['raw'],c['fonts'],c['pages'],ee,ss,aa))
 glyph('drop one actual alias',lambda s,e,a:s['glyph_substitutions'].pop())
 glyph('invent output glyph',lambda s,e,a:s['glyph_substitutions'][0].update(output='A'))
 glyph('shift repair boundary',lambda s,e,a:s['glyph_substitutions'][0].update(start=s['glyph_substitutions'][0]['start']+1))
 glyph('replace actual dictionary identity',lambda s,e,a:e[s['glyph_substitutions'][0]['start']].update(font_identity='0'*64))
 glyph('replace effective encoding identity',lambda s,e,a:e[s['glyph_substitutions'][0]['start']].update(effective_encoding_sha256='0'*64))
 glyph('wrong encoded byte',lambda s,e,a:e[s['glyph_substitutions'][0]['start']].update(encoded_byte=65))
 glyph('duplicate repair',lambda s,e,a:s['glyph_substitutions'].append(deepcopy(s['glyph_substitutions'][0])))
 glyph('truncate multicharacter Greek alias',lambda s,e,a:next(x for x in s['glyph_substitutions']if len(x['input'])>1).update(end=next(x for x in s['glyph_substitutions']if len(x['input'])>1)['start']+1))
 for name,fn in [('drop whole source page',lambda s:s['page_bindings'].pop()),('trim source introduction',lambda s:s['included_spans'][0].update(start=100)),('broaden running header cut',lambda s:s['excluded_furniture'][0].update(end=s['excluded_furniture'][0]['end']+1)),('modify primary extraction hash',lambda s:s.update(extraction_sha256='0'*64))]:
  ss=deepcopy(s);fn(ss);reject(name,lambda ss=ss:validate_selection('F007',c['raw'],ss,c['pages'],c['meta']))
 ret=deepcopy(result['retained_accepted_inputs']);ret['documents']['F005']['metrics']['raw_untrimmed']['NFC']['characters_without_whitespace']+=1
 old0=load('retained/F005_author_counts.json');old1=load('retained/L016_author_counts.json');reject('alter accepted old input cell',lambda:validate_retained(ret,old0,old1))
 b=load('source_code_boundary.json');b['new_source']['masks']=[{'start':0,'end':20}];reject('silent source manuscript deletion',lambda:validate_boundary(b,p))
 return dict(status='PASS',rejected=len(rejected),controls=rejected,scope='Boundary, unchanged-input, actual-byte and selection controls. No mathematical, GAP or Lean replay.')
