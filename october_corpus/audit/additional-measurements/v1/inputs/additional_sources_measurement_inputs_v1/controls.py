"""Semantic boundary/encoding controls, run under Python -O."""
from pathlib import Path
import argparse,copy,json
import extract_inputs as h

def run(args):
 result,audits,cache=h.replay(args)
 policy=h.load_json('policy.json');boundary=h.load_json('source_contract_boundary.json');aliases=h.load_json('proposed_aliases.json')['aliases'];specs=h.load_json('source_input_spec.json')['sources']|h.load_json('replacement_input_spec.json')['ours'];tests=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError,IndexError,TypeError):tests.append(dict(name=name,rejected=True));return
  raise ValueError('CONTROL FAILED '+name)
 def select_mut(key,fn):
  r=copy.deepcopy(specs[key]);fn(r);h.validate_selection(key,cache[key]['cache']['raw'],r,cache[key]['cache']['pages'])
 reject('drop original reference page',lambda:select_mut('L028',lambda r:r['page_bindings'].pop()))
 reject('select only historical proof span',lambda:select_mut('F015',lambda r:r['included_spans'][0].update(start=100)))
 reject('delete unique first-page DOI',lambda:select_mut('F015',lambda r:r['excluded_furniture'].insert(0,dict(page=1,start=0,end=10,literal=cache['F015']['cache']['raw'][:10],sha256=h.sha(cache['F015']['cache']['raw'][:10].encode())))))
 reject('delete application paragraph as furniture',lambda:select_mut('CE1',lambda r:r['excluded_furniture'][0].update(start=0)))
 reject('leave repeated title header unclassified',lambda:select_mut('L028',lambda r:r['excluded_furniture'].pop()))
 def glyph_mut(fn):
  r=copy.deepcopy(specs['U_CE']);fn(r);c=cache['U_CE']['cache'];h.calibrate('U_CE',c['raw'],c['fonts'],c['pages'],c['events'],r,aliases)
 reject('omit actual control-font repair',lambda:glyph_mut(lambda r:r['glyph_substitutions'].pop()))
 reject('change actual encoded byte',lambda:glyph_mut(lambda r:r['glyph_substitutions'][0]['pdf_event'].update(encoded_byte=255)))
 reject('merge two mapsto pieces into one arrow',lambda:glyph_mut(lambda r:next(g for g in r['glyph_substitutions'] if g['pdf_event']['glyph_name']=='mapsto').update(output='↦')))
 reject('delete visible glyph',lambda:glyph_mut(lambda r:r['glyph_substitutions'][0].update(output='')))
 reject('invent source font identity',lambda:glyph_mut(lambda r:r['glyph_substitutions'][0]['pdf_event'].update(font_identity='0'*64)))
 reject('change glyph context',lambda:glyph_mut(lambda r:r['glyph_substitutions'][0].update(context_sha256='0'*64)))
 reject('double-count repaired character',lambda:glyph_mut(lambda r:r['glyph_substitutions'].append(copy.deepcopy(r['glyph_substitutions'][0]))))
 def policy_mut(fn):
  p,b=copy.deepcopy(policy),copy.deepcopy(boundary);fn(p,b);h.validate_policy(p,b)
 reject('count source clauses as originals',lambda:policy_mut(lambda p,b:p.update(originals=64)))
 reject('omit complete mathematical program',lambda:policy_mut(lambda p,b:p['complete_programs'].pop()))
 reject('silently price external proof as zero',lambda:policy_mut(lambda p,b:b.update(retained_external_cost=0)))
 reject('claim whole geometric Lean formalization',lambda:policy_mut(lambda p,b:b.update(full_formalization_claim=True)))
 reject('calculate ratios before independent input acceptance',lambda:policy_mut(lambda p,b:p.update(factors_permitted=True)))
 reject('omit raw untrimmed sensitivity',lambda:policy_mut(lambda p,b:p['variants'].pop(0)))
 pub=h.load_json('publication_binding.json');tex=h.bound(pub['appendix_tex']['chiral_programs_tex'],args,pub).decode();rows=[r for r in policy['complete_programs'] if r['topic']=='ChiralEnumeration'];raw={r['path']:h.bound(r,args,pub) for r in rows};pdf=cache['CE_CODE']['texts']['raw_selected']
 reject('prune program lines in appendix',lambda:h.code_inclusion(tex.replace('fontsize=','firstline=2,fontsize=',1),pdf,rows,raw))
 reject('omit complete program from appendix',lambda:h.code_inclusion(tex.replace('phase282_table_counts.py','absent.py'),pdf,rows,raw))
 reject('truncate literal program contents',lambda:h.code_inclusion(tex,pdf.replace('PHASE282_REJECT','TRUNCATED'),rows,raw))
 # Calibration effects are literal, not semantic; complete raw strings remain separately measured.
 h.need(result['pdf_metric_cells']==240 and result['raw_metric_cells']==90,'full grids')
 return result,dict(status='PASS',controls=tests,controls_run_under_optimization=not __debug__,scientific_programs_executed=False),audits

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();h.need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
 result,controls,audits=run(a)
 for name,v in [('counts.json',result),('controls.json',controls),('font_audit.json',audits)]: (a.out/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
 print('PASS',len(controls['controls']),'semantic controls; 240 PDF/90 raw cells; no scientific rerun or factors.')
if __name__=='__main__':main()
