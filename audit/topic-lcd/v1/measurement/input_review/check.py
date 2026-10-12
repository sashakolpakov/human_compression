#!/usr/bin/env python3
"""Distinct input review. No mathematical enumeration or author arithmetic import."""
from pathlib import Path
from collections import Counter
import argparse,copy,json,hashlib,tempfile,shutil
from recount import run,require,digest,bound
PIN='3d4f1a989020ed6cf9e632263b785b79ecdf5d30765170760b8240f9c13d27cc'
DOCS=[('L050',11,'source'),('F017',17,'source'),('U_LCD',14,'common'),('A_F017',12,'application'),('A_L050',15,'application')]

def data(packet):return {f:json.loads((packet/f).read_text())for f in ['policy.json','document_map.json','listing_screen.json','whole_file_boundary.json','whole_file_counts.json','author_stage_counts.json','input_spec.json','science_bindings.json','graphics_inventory.json']}
def scope(x,root,packet):
 p=x['policy.json'];dm=x['document_map.json'];b=x['whole_file_boundary.json'];wc=x['whole_file_counts.json'];ls=x['listing_screen.json']
 require([(r['key'],r['pages'],r['role'])for r in dm['documents']]==DOCS,'five complete PDFs')
 require(dm['physical_pages']==69 and all(r['whole_document']for r in dm['documents']),'whole pages')
 require(p['primary']==dict(variant='calibrated_selected',normalization='NFC',unit='characters_without_whitespace'),'precount primary')
 require(p['originals']==['L050','F017']and p['variants']==['raw_untrimmed','raw_selected','calibrated_selected']and p['normalizations']==['NFC','NFKC'],'all coordinates')
 require(not p['factors_permitted']and p['ratio']is None and p['new_original_credit']==p['new_question_credit']==0,'no premature numbers or credits')
 require(all(v is None for v in p['unknowns'].values()),'unknown costs remain null')
 require(p['symmetric_program_boundary']['software_inclusive_factor']is None and b['software_inclusive_factor']is None and b['source_software']is None,'no asymmetric software factor')
 require(b['optional_validation_symmetric_exclusion']and b['unique_partial_declarations']==9 and not b['full_Lean'],'symmetric validation and partial formal scope')
 require(ls['required_certificates_remain_premises']and ls['optional_validation_excluded_both_sides']and ls['software_inclusive_factor']is None and not ls['final_L050_application_screen_pending'],'symmetric listing scope')
 gi=x['graphics_inventory.json'];require(gi['source_graphics_and_layout_cost']is None and gi['OCR_used']is False and gi['complete_visual_text_claim']is False,'unknown layout is not zero')
 require(all(d['graphic_cost']is None and d['full_visible_text_claim']is False for d in gi['documents']),'all graphics remain outside text proxy')
 require([(r['document'],len(r['pages']))for r in ls['documents']]==[(k,n)for k,n,_ in DOCS],'all pages screened')
 for row,doc in zip(ls['documents'],dm['documents']):
  require(row['pages']==list(range(1,doc['pages']+1))and row['pdf_sha256']==doc['sha256'],'same scientific edition listing screen')
  require(not row['masks']and not row['executable_listings'],'no listing cuts in these inspected documents')
  if doc['role']=='source':require(row['historical_software_cost']is None,'unknown original software')
 inv=json.loads((root/'topic_LCD_L050_application/program_inventory.json').read_text())
 prior=json.loads((packet/'previous_stage/known_file_boundary.json').read_text())
 wanted={r['path']:dict(r)for r in prior['files']}
 # Derive every L050 role from its accepted executable/data inventory.
 for row in inv['whole_executable_files']+inv['literal_data_and_retained_outputs']:
  old=row['role'];rel=row['path'];path='topic_LCD_L050_application/'+rel
  if old.startswith('OPERATIONAL'):role='operational_driver'
  elif old=='OPTIONAL_SMALL_VALIDATION':role='optional_validation'
  elif old=='RETAINED_COMPLETE_ENUMERATION_OUTPUT':role='required_finite_record'
  elif old=='PRESERVED_DERIVED_OR_RETAINED_COPY_WITH_ORIGINAL_ROLE':
   if rel.endswith('/run_enumerators.py'):role='operational_driver'
   elif rel.endswith('.g'):role='required_derived_certificate'
   else:role='required_program'
  elif old in ['REQUIRED_LITERAL_BASIS_OR_ACTION','REQUIRED_LITERAL_MATHEMATICAL_DATA','REQUIRED_COMMON_SCALAR_OUTPUT']:role='required_data'
  else:require(old in ['REQUIRED_COMPLETE_MATHEMATICAL_PROGRAM','REQUIRED_COMMON_SCALAR_CERTIFICATE','REQUIRED_RETAINED_COMPLETE_ENUMERATOR'],'known scientific role');role='required_program'
  wanted[path]=dict(path=path,bytes=row['bytes'],sha256=row['sha256'],role=role,mathematical_premise=role.startswith('required'),whole_file=True)
 for rel,role in [('formal/GraphCodeProjectors.lean','partial_formal_file'),('formal/TransitiveCodeBounds.lean','partial_formal_file'),('formal_scope.json','partial_formal_scope')]:
  path='topic_LCD_L050_application/'+rel;raw=(root/path).read_bytes();wanted[path]=dict(path=path,bytes=len(raw),sha256=digest(raw),role=role,mathematical_premise=False,whole_file=True)
 require(len(wanted)==127 and len(b['files'])==127,'all declared occurrences')
 for row in b['files']:
  require({k:row[k]for k in ['path','bytes','sha256','role','mathematical_premise','whole_file']}==wanted[row['path']],'exact accepted scientific file role')
 require(set(wanted)=={r['path']for r in b['files']},'no silent duplicate omission')
 groups={}
 for r in b['files']:groups.setdefault(r['sha256'],[]).append(r)
 require(len(groups)==len(b['unique_files'])==len(wc['files'])==102,'whole-content union')
 for r in wc['files']:
  rs=groups[r['sha256']];require(set(r['occurrences'])=={s['path']for s in rs},'all occurrences displayed')
  require(set(r['roles'])=={s['role']for s in rs}and r['mathematical_premise']==any(s['mathematical_premise']for s in rs),'no required role lost in union')
 require(wc['roles']==dict(Counter(r['role']for r in wc['files']))and wc['metric_cells']==1020,'correct raw inventory counts')
 old=json.loads((packet/'previous_stage/counts.json').read_text())
 require(all(x['author_stage_counts.json']['documents'][k]==v for k,v in old['documents'].items()),'120 prior PDF cells and hashes unchanged')
 oldraw=json.loads((packet/'previous_stage/known_file_counts.json').read_text())
 byhash={r['sha256']:r for r in wc['files']}
 require(all(r['metrics']==byhash[r['sha256']]['metrics']for r in oldraw['files']),'450 prior file cells unchanged')
 return dict(whole_documents=5,whole_pages=69,source_originals=2,dispositions_not_originals=True,whole_common_paid_once=True,required_files_preserved=True,source_software_unknown=True,no_factors=True)

def controls(packet,root):
 x=data(packet);scope(x,root,packet);results=[]
 def reject(label,func):
  try:func()
  except(ValueError,KeyError,IndexError,TypeError)as e:results.append(dict(name=label,rejected=True,reason=str(e)[:170]));return
  raise ValueError('control accepted: '+label)
 def sc(label,mut):
  y=copy.deepcopy(x);mut(y);reject(label,lambda:scope(y,root,packet))
 sc('omit entire L050 application',lambda z:z['document_map.json']['documents'].pop())
 sc('turn full common into selected excerpts',lambda z:z['document_map.json']['documents'][2].update(whole_document=False))
 sc('choose metric after observations',lambda z:z['policy.json']['primary'].update(variant='raw_untrimmed'))
 sc('replace unknown historical software by zero',lambda z:z['whole_file_boundary.json'].update(source_software=0))
 sc('publish software-inclusive scalar',lambda z:z['policy.json']['symmetric_program_boundary'].update(software_inclusive_factor=1))
 sc('claim full Lean',lambda z:z['whole_file_boundary.json'].update(full_Lean=True))
 sc('double reused formal declarations',lambda z:z['whole_file_boundary.json'].update(unique_partial_declarations=18))
 sc('treat unavailable layout as zero',lambda z:z['graphics_inventory.json'].update(source_graphics_and_layout_cost=0))
 sc('count source-only executable listing',lambda z:z['listing_screen.json']['documents'][0]['masks'].append({'start':20,'end':100}))
 sc('hide compulsory enumerator',lambda z:z['whole_file_boundary.json']['files'].pop(0))
 sc('demote required program',lambda z:z['whole_file_boundary.json']['files'][0].update(mathematical_premise=False,role='optional_validation'))
 sc('discard duplicate occurrence from union',lambda z:z['whole_file_counts.json']['files'][0]['occurrences'].pop())
 sc('silently alter inherited coordinate',lambda z:z['author_stage_counts.json']['documents']['L050']['variants']['raw_selected']['NFC'].update(characters_without_whitespace=1))
 # The following corrupt actual semantic evidence and run the independent recount,
 # bypassing the outer immutable hash check so rejection is not merely a pin test.
 tests=[
 ('drop source body range','input_spec.json',lambda z:z['F017']['included_spans'][0].update(end=100)),
 ('mask genuine abstract','input_spec.json',lambda z:z['L050']['excluded_furniture'].append(dict(start=100,end=200))),
 ('wrong mapsto-piece proxy','glyph_aliases.json',lambda z:next(r for r in z['aliases']if r['glyph_name']=='mapsto').update(output='↦')),
 ('omit actual script-H repair','input_spec.json',lambda z:z['A_L050']['glyph_substitutions'].remove(next(r for r in z['A_L050']['glyph_substitutions']if r['output']=='ℋ'))),
 ('alter actual encoding identity','font_audit.json',lambda z:z['U_LCD']['font_dictionaries'][0].update(effective_encoding_sha256='0'*64)),
 ('alter actual outline evidence','font_audit.json',lambda z:z['L050']['encoded_glyph_classes'][0]['glyph_evidence'].update(outline_sha256='0'*64)),
 ('alter retained Type0 dictionary','font_audit.json',lambda z:z['A_F017']['unchanged_type0_dictionaries'][0].update(font_dictionary_sha256='0'*64)),
 ('alter one new PDF cost','author_stage_counts.json',lambda z:z['documents']['A_L050']['variants']['raw_untrimmed']['NFC'].update(characters_without_whitespace=1)),
 ('alter one whole-file cost','whole_file_counts.json',lambda z:z['files'][0]['metrics']['NFC'].update(characters_without_whitespace=1))]
 for label,name,mut in tests:
  with tempfile.TemporaryDirectory(prefix='LCD-semantic-',dir='/private/tmp')as td:
   d=Path(td)
   for f in packet.glob('*'):
    if f.is_file():shutil.copy2(f,d/f.name)
   z=json.loads((d/name).read_text());mut(z);(d/name).write_text(json.dumps(z))
   reject(label,lambda d=d:run(d,root))
 return results

def main():
 a=argparse.ArgumentParser();a.add_argument('--packet',type=Path,required=True);a.add_argument('--study-root',type=Path,required=True);a.add_argument('--out',type=Path,required=True);a.add_argument('--skip-controls',action='store_true');v=a.parse_args();require(not v.out.exists(),'fresh output');v.out.mkdir(parents=True)
 raw=(v.packet/'manifest.json').read_bytes();require(digest(raw)==PIN,'exact author freeze');m=json.loads(raw)
 for r in m['exports']:bound(v.packet,r)
 for r in json.loads((v.packet/'science_bindings.json').read_text())['bindings']:
  p=Path(r['path']);require(p.parts[-3]=='leemans','known science path');bound(v.study_root,dict(r,path=str(p.relative_to('/Users/sasha/medusa/research/leemans'))))
 s=scope(data(v.packet),v.study_root,v.packet);r=run(v.packet,v.study_root);c=[]if v.skip_controls else controls(v.packet,v.study_root)
 result=dict(status='PASS_DISTINCT_MEASUREMENT_INPUT_AUDIT',author_manifest_sha256=PIN,scope=s,recount=r,controls=c,science_replayed=False,large_enumerations_repeated=False,ratios=False)
 (v.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(status=result['status'],PDF_cells=r['pdf_cells'],raw_cells=r['raw_unique_cells'],controls=len(c))))
if __name__=='__main__':main()
