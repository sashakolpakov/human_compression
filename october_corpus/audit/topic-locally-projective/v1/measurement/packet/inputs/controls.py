"""Bounded semantic input controls; no scientific group calculation."""
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
import argparse,json
import extract_inputs as E
from font_tools import need

def checks(root):
 result,cache=E.replay(SimpleNamespace(study_root=root));p=E.load('policy.json');spec=E.load('input_spec.json');aliases=E.load('glyph_aliases.json')['aliases'];tests=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError,IndexError,TypeError):tests.append(dict(name=name,rejected=True));return
  raise ValueError('CONTROL_ACCEPTED: '+name)
 def policy(name,change):
  q=deepcopy(p);change(q);reject(name,lambda:E.validate_policy(q))
 policy('omit common full table companion',lambda q:q['whole_common'].remove('TABLES'))
 policy('omit table document from written sum',lambda q:q['written_documents'].remove('TABLES'))
 policy('make sibling application a prepaid premise',lambda q:q['applications']['L084'].append('A2'))
 policy('drop required full accounting program',lambda q:q['programs'].pop(3))
 policy('repeat ambient marking alias',lambda q:q['programs'].__setitem__(1,deepcopy(q['programs'][0])))
 policy('omit historical comparison data',lambda q:q['required_data'].clear())
 policy('prune a required full program',lambda q:q['programs'][0].update(whole_file=False))
 policy('add nonexistent formal proof',lambda q:q['formal_files'].append('fiction.lean'))
 policy('silently omit output storage',lambda q:q['output_data'].pop())
 policy('replace missing classical cost by zero',lambda q:q['unknown_costs'].update(full_retained_classical_proofs=0))
 policy('enable premature factor',lambda q:q.update(factors_permitted=True))
 policy('replace fifteen-page preprint by journal length',lambda q:q['documents']['L095'].update(pages=12))
 policy('forget full program preacquisition',lambda q:q.update(conditional_policy='only theory is prepaid'))
 c=cache['L095'];r=spec['L095']
 def select(name,change):
  q=deepcopy(r);change(q);reject(name,lambda:E.validate_selection('L095',c['raw'],q,c['pages'],c['meta']))
 select('cut bibliography or body span',lambda q:q['included_spans'][0].update(end=q['included_spans'][0]['end']-10))
 select('remove title or version banner as furniture',lambda q:q['excluded_furniture'].insert(0,dict(page=1,start=0,end=50,literal=c['raw'][:50],sha256=E.sha(c['raw'][:50].encode()))))
 select('alter actual physical page hash',lambda q:q['page_bindings'][0].update(sha256='0'*64))
 def glyph(name,change):
  q=deepcopy(r);change(q);reject(name,lambda:E.calibrate(c['raw'],c['fonts'],c['pages'],c['events'],q,aliases,'L095'))
 glyph('omit printable alias event',lambda q:q['glyph_substitutions'].pop())
 glyph('change calibrated calligraphic symbol',lambda q:q['glyph_substitutions'][0].update(output='X'))
 glyph('wrong original encoded byte',lambda q:q['glyph_substitutions'][0]['pdf_event'].update(encoded_byte=88))
 glyph('merge same-named font dictionaries',lambda q:q['glyph_substitutions'][0]['pdf_event'].update(font_identity='0'*64))
 glyph('remove original glyph context binding',lambda q:q['glyph_substitutions'][0].update(context_sha256='0'*64))
 glyph('drop a visible glyph as generated whitespace',lambda q:q['extraction_metadata']['generated_newline_offsets'].append(q['glyph_substitutions'][0]['offset']))
 glyph('count same visible event twice',lambda q:q['glyph_substitutions'].append(deepcopy(q['glyph_substitutions'][0])))
 # Actual new parser cases, tested independently of stored count values.
 import pypdf
 from font_tools import embedded
 from fontTools.cffLib import CFFFontSet
 from io import BytesIO
 fonts=pypdf.PdfReader(root/p['documents']['L084']['path']).pages[0]['/Resources']['/Font'];defaults=[];mac=[]
 for name,ref in fonts.items():
  f=ref.get_object();descriptor=f.get('/FontDescriptor')
  if descriptor is None or '/FontFile3' not in descriptor.get_object():continue
  face=CFFFontSet();face.decompile(BytesIO(descriptor.get_object()['/FontFile3'].get_object().get_data()),None);top=face[face.fontNames[0]]
  if 'charset' not in top.rawDict:
   need('ROS' not in top.rawDict,'actual omitted charset is name-keyed');_,mapping,strings=embedded(f);need('A' in strings,'literal ISOAdobe capital A present');defaults.append(str(f['/BaseFont']))
  if str(f.get('/Encoding'))=='/MacRomanEncoding':
   _,m,_=embedded(f);need(m[222]=='fi','actual MacRoman byte222 is fi');mac.append(str(f['/BaseFont']))
 need(len(defaults)==4 and mac==['/Times-Bold'],'exact actual CFF default/MacRoman cases')
 # Two deliberately false effective-encoding conclusions must be rejected.
 reject('MacRoman fi relabelled as WinAnsi Thorn',lambda:need(m[222]=='Thorn','actual MacRoman byte'))
 reject('zero implicit CFF charset font count',lambda:need(not defaults,'actual default charset fonts'))
 return dict(status='PASS',semantic_negative_controls=len(tests),controls=tests,positive_replay=dict(pdf_metric_cells=result['pdf_metric_cells'],raw_metric_cells=result['raw_metric_cells']),parser_cases=dict(implicit_CFF_ISOAdobe_fonts=defaults,explicit_MacRoman_fonts=mac),scientific_programs_executed=False)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh control output');r=checks(a.study_root);a.out.mkdir(parents=True);(a.out/'controls.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print('PASS',r['semantic_negative_controls'],'semantic controls')
if __name__=='__main__':main()
