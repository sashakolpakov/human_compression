"""Bounded mutations of input boundaries, actual glyph events and metrics."""
from copy import deepcopy
from extract_inputs import need,load,validate_policy,calibrate,aliases_from,furniture,metrics,sha

def controls(cache):
 results=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError,IndexError,TypeError):results.append(dict(name=name,rejected=True));return
  raise ValueError('CONTROL_NOT_REJECTED: '+name)
 p=load('policy.json')
 for name,edit in [
  ('drop original',lambda x:x['source_ids'].pop()),
  ('omit source last page',lambda x:x['documents']['L043'].__setitem__('pages',24)),
  ('partial common theory',lambda x:x.__setitem__('whole_common',[])),
  ('wrong source application',lambda x:x['applications'].__setitem__('L079',['A1'])),
  ('omit second new application',lambda x:x['written_documents'].remove('A5')),
  ('omit mandatory JSON',lambda x:x['programs_and_data'].pop()),
  ('required program called validation',lambda x:x['programs_and_data'][0].__setitem__('role','validation only')),
  ('prune full file',lambda x:x['programs_and_data'][0].__setitem__('whole_file',False)),
  ('omit operational driver',lambda x:x['operational_drivers'].pop()),
  ('full formalization count',lambda x:x.__setitem__('formal_declarations',43)),
  ('one-sided software factor',lambda x:x['symmetry_policy'].__setitem__('inclusive_software_factor',2)),
  ('unknown software zero',lambda x:x['symmetry_policy'].__setitem__('historical_software_cost',0)),
  ('free other-topic common',lambda x:x['symmetry_policy'].__setitem__('no_cross_topic_free_premise',False)),
  ('allow numerical factor',lambda x:x.__setitem__('factors_permitted',True)),
  ('zero external proof cost',lambda x:x['unknown_costs'].__setitem__('full_external_classical_proofs',0)),
 ]:
  q=deepcopy(p);edit(q);reject(name,lambda q=q:validate_policy(q))
 specs=load('input_spec.json');aliases=load('glyph_aliases.json')['aliases']
 def checkglyph(k,r):
  x=cache[k];calibrate(x['raw'],x['fonts'],x['pages'],x['events'],r,aliases,k)
 for name,key,edit in [
  ('drop visible parenthesis','L021',lambda r:r['glyph_substitutions'].__delitem__(next(i for i,g in enumerate(r['glyph_substitutions'])if g['kind']=='visible_delimiter'))),
  ('wrong parenthesis output','L021',lambda r:next(g for g in r['glyph_substitutions']if g['kind']=='visible_delimiter').__setitem__('output',']')),
  ('changed actual encoded byte','L043',lambda r:r['glyph_substitutions'][0]['pdf_event'].__setitem__('encoded_byte',2)),
  ('changed dictionary identity','L056',lambda r:r['glyph_substitutions'][0]['pdf_event'].__setitem__('font_identity','0'*64)),
  ('changed occurrence context','L079',lambda r:r['glyph_substitutions'][0].__setitem__('context_sha256','0'*64)),
  ('duplicate alias event','L083',lambda r:r['glyph_substitutions'].append(deepcopy(r['glyph_substitutions'][0]))),
  ('suppress printable alias','L056',lambda r:r.__setitem__('glyph_substitutions',[])),
 ]:
  q=deepcopy(specs[key]);edit(q);reject(name,lambda q=q,key=key:checkglyph(key,q))
 for name,edit in [
  ('alter class multiplicity',lambda a:a['L021']['encoded_glyph_classes'].__setitem__(next(i for i,r in enumerate(a['L021']['encoded_glyph_classes'])if r['font_dictionary_object']['idnum']==226 and r['encoded_byte']==18),dict(next(r for r in a['L021']['encoded_glyph_classes']if r['font_dictionary_object']['idnum']==226 and r['encoded_byte']==18),occurrences=3))),
  ('discard effective dictionary',lambda a:a['L043'].__setitem__('encoded_glyph_classes',[r for r in a['L043']['encoded_glyph_classes']if r['font_dictionary_object']['idnum']!=172]))]:
  a=deepcopy(load('font_audit.json'));edit(a);reject(name,lambda a=a:aliases_from(a))
 # Exact fixture establishes whitespace, ligature and mathematical-letter sensitivity.
 t='A\t𝒫 ﬁ\nβ2';nfc=metrics(t,'NFC');nfkc=metrics(t,'NFKC')
 need(nfc['whitespace_tokens']==4 and nfc['alphanumeric_units']==4 and nfc['characters_without_whitespace']==5 and nfc['characters_with_collapsed_whitespace']==8 and nfc['utf8_bytes_with_collapsed_whitespace']==14,'NFC independent literal fixture')
 need(nfkc['characters_without_whitespace']==6 and nfkc['characters_with_collapsed_whitespace']==9 and nfkc['utf8_bytes_with_collapsed_whitespace']==10,'NFKC fixture preserves explicit normalization sensitivity')
 results.append(dict(name='literal five-unit NFC/NFKC fixture',passed=True))
 return dict(status='PASS',negative_controls=len(results)-1,metric_fixture=True,results=results)
