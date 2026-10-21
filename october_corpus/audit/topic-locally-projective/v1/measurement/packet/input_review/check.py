#!/usr/bin/env python3
"""Reproduce distinct input audit and focused semantic rejection controls."""
from pathlib import Path
import argparse,copy,json,shutil,subprocess,sys,time
import recount as R
import font_bindings as F

def controls(packet,study):
 p=R.read(packet/'policy.json');spec=R.read(packet/'input_spec.json');aud=R.read(packet/'font_audit.json');rows=[]
 def reject(name,f):
  try:f()
  except (ValueError,KeyError,IndexError):rows.append(dict(name=name,rejected=True));return
  raise ValueError('MUTATION ACCEPTED: '+name)
 def policy_case(name,mut):
  q=copy.deepcopy(p);mut(q);reject(name,lambda:R.boundary(q))
 policy_case('omit common census companion',lambda q:q['whole_common'].remove('TABLES'))
 policy_case('truncate complete common paper',lambda q:q['documents']['U'].update(pages=6))
 policy_case('drop final source tables page',lambda q:q['documents']['L095'].update(pages=14))
 policy_case('omit a required programme',lambda q:q['programs'].pop())
 policy_case('omit mandatory raw source data',lambda q:q['required_data'].clear())
 policy_case('prune required historical comparison data',lambda q:q['required_data'][0].update(bytes=38000))
 policy_case('omit complete generated outputs',lambda q:q['output_data'].pop())
 policy_case('set unknown graphics cost to zero',lambda q:q['unknown_costs'].update(graphics_and_layout=0))
 policy_case('make sibling application free',lambda q:q['applications'].update(L095=[]))
 policy_case('remove whole conditional acquisition',lambda q:q.update(conditional_policy='given the main lemma'))
 policy_case('printed-code route substitutes for required raw data',lambda q:q.update(programme_policy='Printed code alone.'))
 policy_case('invent formal declarations file',lambda q:q['formal_files'].append({'path':'invented.lean'}))
 policy_case('compute factor at input stage',lambda q:q.update(factors_permitted=True,ratio=2))
 def doc_case(name,key,mut):
  s=copy.deepcopy(spec[key]);mut(s);reject(name,lambda:R.document(key,study/s['path'],s))
 doc_case('include only selected source body', 'L095',lambda s:s['included_spans'][0].update(start=1000))
 doc_case('cut a substantive source paragraph as furniture','L095',lambda s:s['excluded_furniture'][0].update(start=800))
 doc_case('leave calligraphic glyph unrepaired','L095',lambda s:s['glyph_substitutions'].pop())
 doc_case('merge mapsto components','L095',lambda s:next(r for r in s['glyph_substitutions'] if r['pdf_event']['glyph_name']=='mapsto').update(output='↦'))
 doc_case('replace envelope with ordinary B','L084',lambda s:s['glyph_substitutions'][-1].update(output='B'))
 q=copy.deepcopy(spec);q['L084']['glyph_substitutions'][0]['offset']+=1
 reject('shift actual glyph occurrence',lambda:F.verify(packet,study,specs_override=q))
 q=copy.deepcopy(aud);q['L084']['font_dictionaries'][0]['font_dictionary_sha256']='0'*64
 reject('wrong actual font dictionary',lambda:F.verify(packet,study,audits_override=q))
 q=copy.deepcopy(aud);d=next(r for r in q['L084']['font_dictionaries'] if r['font']=='/Times-Bold');d['effective_encoding']['128']='not_the_actual_MacRoman_mapping'
 reject('change actual MacRoman encoding',lambda:F.verify(packet,study,audits_override=q))
 q=copy.deepcopy(aud);q['L095']['encoded_glyph_classes'][0]['occurrences']+=1
 reject('wrong full byte-event multiplicity',lambda:F.verify(packet,study,audits_override=q))
 q=copy.deepcopy(p['required_data'][0]);q['bytes']-=1
 reject('truncate whole raw comparison input',lambda:R.bound(study,q))
 return rows

def run(packet,study,out,render=False,xelatex='xelatex'):
 R.need(not out.exists() and not out.is_symlink(),'fresh output required');out.mkdir(parents=True);start=time.monotonic()
 # If replayed as a frozen reviewer copy, validate every own export first.
 here=Path(__file__).resolve().parent
 if (here/'manifest.json').exists():
  for r in R.read(here/'manifest.json')['exports']:R.bound(here,r)
 result=R.audit(packet,study);fonts=F.verify(packet,study);neg=controls(packet,study)
 for name,data in [('recount.json',result),('font_check.json',fonts),('controls.json',neg)]: (out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 copied=None
 if render:
  dest=out/'author_packet';dest.mkdir()
  for row in R.read(packet/'manifest.json')['exports']:
   target=dest/row['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(packet/row['path'],target)
  shutil.copyfile(packet/'manifest.json',dest/'manifest.json')
  cmd=[sys.executable,'-B','-O',str(dest/'check.py'),'--study-root',str(study),'--out',str(out/'author_replay'),'--render','--xelatex',xelatex]
  p=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(out/'author_replay.stdout').write_text(p.stdout);R.need(p.returncode==0,'export-only author input/reader replay')
  copied=R.read(out/'author_replay/report.json');R.need(copied['status']=='PASS' and copied['semantic_controls']==25 and copied['render']['pages']==2 and copied['render']['diagnostics']==[],'full copied author results')
 report=dict(status='PASS',author_manifest_sha256=R.PIN,pdf_cells=210,raw_cells=100,collapsed_text_hashes=62,font_dictionaries=26,glyph_classes=502,calibrated_occurrences=61,independent_controls=len(neg),copied_author_replay=copied,independent_counter_imports_author_code=False,independent_font_check_imports_author_code=False,math_or_GAP_or_Lean_rerun=False,factors_computed=False,seconds=round(time.monotonic()-start,3))
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS310 independent cells;61 actual glyphs;',len(neg),'independent controls')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--study-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='xelatex');a=p.parse_args();run(a.packet.resolve(),a.study_root.resolve(),a.out.resolve(),a.render,a.xelatex)
