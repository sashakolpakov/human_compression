#!/usr/bin/env python3
"""Complete additive input replay; no scientific program or formal execution."""
from pathlib import Path
import argparse,copy,csv,io,json,subprocess,sys
import pypdf
from extract_inputs import replay,load,need,sha,validate_one,H
from build_reader import reader,build

def semantic(c,spec,listing,completion):
 old=load('precount/baseline/author_counts.json');p=load('precount/policy.json');inherit=load('precount/inheritance.json');inventory=load('precount/raw_inventory.json')
 need(set(c['documents'])=={r['id']for r in load('precount/documents.json')['documents']},'all29 exact document IDs')
 need(set(c['raw_files_measured'])=={r['id']for r in inventory['contents']},'all203 exact raw IDs')
 need(all(c['documents'][k]==old['documents'][k]for k in inherit['reuse_document_ids']),'all630 inherited PDF cells')
 need((c['pdf_documents'],c['pdf_pages'],c['pdf_metric_cells'],c['raw_files'],c['raw_metric_cells'])==(29,286,870,203,2030),'complete dimensions')
 need(c['factors']is None and c['software_inclusive_factor']is None and c['new_original_credit']==0 and not c['input_accepted']and c['science_accepted'],'no premature factor/credit')
 need(completion['new_metrics_evaluated']and completion['new_raw_metrics_evaluated']and not completion['input_accepted']and completion['new_ratios']is None,'separate additive completion')
 for r in inventory['contents']:
  d=c['raw_files_measured'][r['id']]
  need(all(d[k]==r[k]for k in ['sha256','bytes','occurrence_ids','roles','coarse_roles','accounting_class','mathematical_premise','inherited_A9_raw_id']),'exact whole raw role and binding')
  if r['inherited_A9_raw_id']is not None:need(d['metrics']==old['raw_files_measured'][r['inherited_A9_raw_id']]['metrics'],'all450 inherited raw cells')
  need(set(d['metrics'])==set(p['normalizations']),'both raw normalizations')
  for n in p['normalizations']:need(set(d['metrics'][n])==set(p['metrics'])|{'collapsed_text_sha256'},'allfive raw units/hash')
 need({r['document']for r in listing['new_documents']}==set(spec)and all(r['executable_listings']==[]and r['masks']==[]and r['all_pages_viewed']for r in listing['new_documents']),'complete symmetric screen')
 need(listing['required_certificates_still_premises']and listing['software_inclusive_factor']is None and listing['historical_software_cost']is None,'required and unknown boundaries')
 repairs={'L003':33,'U_HEX':382,'U_STRUCT':8,'A9':0,'A10_MAIN':31,'A10_STRUCT':2,'A10_CORR':5,'A10_768':1}
 for r in load('document_map.json')['documents']:
  k=r['key'];d=c['documents'][k];need(d['pages']==r['pages']and d['pdf_sha256']==r['sha256']and d['glyph_substitutions']==repairs[k],'new whole PDFs and repair census')
  need(len(spec[k]['excluded_furniture'])==r['pages']and not spec[k]['excluded_listings'],'no body/listing exclusion')
  need(d['drawing_occurrences']==(423 if k=='L003'else 0),'drawing aliases disclosed')
 for d in c['documents'].values():
  need(set(d['metrics'])==set(p['variants']),'allthree variants')
  for v in p['variants']:
   need(set(d['metrics'][v])==set(p['normalizations']),'both normalizations')
   for n in p['normalizations']:need(set(d['metrics'][v][n])==set(p['metrics'])|{'collapsed_text_sha256'},'allfive units/hash')
 need(c['documents']['A9']!=old['documents']['A9']and c['documents']['A9']['pages']==1,'changed L121 adapter, no old11page double charge')
 return True

def tables(c):
 def table(header,rows):
  o=io.StringIO(newline='');w=csv.writer(o,lineterminator='\n');w.writerow(header);w.writerows(rows);return o.getvalue()
 p=load('policy.json');rows=[]
 for k,d in c['documents'].items():
  for v in p['variants']:
   for n in p['normalizations']:
    for m in p['metrics']:rows.append([k,v,n,m,d['metrics'][v][n][m]])
 raw=[]
 for k,d in c['raw_files_measured'].items():
  for n in p['normalizations']:
   for m in p['metrics']:raw.append([k,d['accounting_class'],d['mathematical_premise'],n,m,d['metrics'][n][m]])
 return {'pdf_counts.csv':table(['document','variant','normalization','metric','count'],rows),'raw_counts.csv':table(['content','accounting_class','mathematical_premise','normalization','metric','count'],raw)}

def controls(c,cache):
 done=[]
 def rejects(name,f):
  try:f()
  except(ValueError,KeyError,AssertionError):done.append(name)
  else:raise ValueError('control survived: '+name)
 base=[c,load('input_spec.json'),load('listing_screen.json'),load('completion.json')]
 def mutate(name,f):
  x=copy.deepcopy(base);f(x);rejects(name,lambda:semantic(*x))
 mutate('drop whole common supplement',lambda x:x[0]['documents'].pop('U_HEX'))
 mutate('drop shared structural common',lambda x:x[0]['documents'].pop('U_STRUCT'))
 mutate('drop L003 companion',lambda x:x[0]['documents'].pop('A10_768'))
 mutate('restore old11page L121',lambda x:x[0]['documents'].update(A9=load('precount/baseline/author_counts.json')['documents']['A9']))
 mutate('alter inherited PDF count',lambda x:x[0]['documents']['U']['metrics']['calibrated_selected']['NFC'].update(characters_without_whitespace=0))
 mutate('alter inherited raw count',lambda x:x[0]['raw_files_measured']['F001']['metrics']['NFC'].update(whitespace_tokens=0))
 mutate('drop new required content',lambda x:x[0]['raw_files_measured'].pop('F046'))
 target=next(k for k,r in c['raw_files_measured'].items()if r['accounting_class']=='required_data'and r['inherited_A9_raw_id']is None)
 mutate('consumed saved image demoted to output',lambda x:x[0]['raw_files_measured'][target].update(accounting_class='output_receipt',mathematical_premise=False))
 mutate('erase overlapping occurrence roles',lambda x:x[0]['raw_files_measured'][target].update(roles=[]))
 mutate('software unknown becomes zero',lambda x:x[0].update(software_inclusive_factor=0))
 mutate('premature input acceptance',lambda x:x[0].update(input_accepted=True))
 mutate('new original credit',lambda x:x[0].update(new_original_credit=1))
 mutate('delete proof prose as code',lambda x:x[1]['L003']['excluded_listings'].append({'page':10}))
 mutate('required certificates optional',lambda x:x[2].update(required_certificates_still_premises=False))
 mutate('historical software zero',lambda x:x[2].update(historical_software_cost=0))
 mutate('remove source page',lambda x:x[0]['documents']['L003'].update(pages=20))
 mutate('omit sensitivity',lambda x:x[0]['documents']['A10_CORR']['metrics'].pop('raw_untrimmed'))
 mutate('drawing occurrences omitted',lambda x:x[0]['documents']['L003'].update(drawing_occurrences=0))
 def row_mut(name,key,f):
  row=copy.deepcopy(base[1][key]);f(row);rejects(name,lambda:validate_one(key,row,*cache[key]))
 row_mut('wrong actual bracket','A10_CORR',lambda r:next(g for g in r['glyph_substitutions']if g['pdf_events'][0]['glyph_name']=='bracerightbig').update(output=']'))
 row_mut('remove visible TAB brace','A10_CORR',lambda r:r['glyph_substitutions'].__delitem__(next(i for i,g in enumerate(r['glyph_substitutions'])if g['input']=='\t')))
 row_mut('wrong actual encoded byte','L003',lambda r:r['glyph_substitutions'][0]['pdf_events'][0].update(encoded_byte=0))
 row_mut('wrong dictionary identity','U_HEX',lambda r:r['glyph_substitutions'][0]['pdf_events'][0].update(font_dictionary_sha256='0'*64))
 row_mut('wrong event context','U_HEX',lambda r:r['glyph_substitutions'][0].update(context_sha256='0'*64))
 row_mut('mapsto component merged into arrow','U_HEX',lambda r:next(g for g in r['glyph_substitutions']if g['pdf_events'][0]['glyph_name']=='mapsto').update(output='↦'))
 row_mut('remove graphic NUL event','L003',lambda r:r['drawing_occurrences'].__delitem__(next(i for i,g in enumerate(r['drawing_occurrences'])if g['input']=='\x00')))
 row_mut('drawing alias becomes invented line','L003',lambda r:r['glyph_substitutions'].append(dict(**r['drawing_occurrences'][0],output='─')))
 row_mut('delete references as furniture','L003',lambda r:r['excluded_furniture'][-1].update(end=r['page_bindings'][-1]['end']))
 row_mut('drop footer mask','A9',lambda r:r['excluded_furniture'].pop())
 row_mut('generated whitespace becomes glyph','A10_CORR',lambda r:r['extraction_metadata']['generated_newline_offsets'].append(0))
 row_mut('wrong source running title','L003',lambda r:r['excluded_furniture'][2].update(literal='other title'))
 return done

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='xelatex');v=ap.parse_args();need(not v.out.exists(),'fresh output');v.out.mkdir(parents=True)
 if(H/'manifest.json').exists():
  for e in load('manifest.json')['exports']:
   b=(H/e['path']).read_bytes();need(len(b)==e['bytes']and sha(b)==e['sha256'],'frozen export '+e['path'])
 for e in load('helper_provenance.json'):
  b=(H/e['path']).read_bytes();need(len(b)==e['bytes']and sha(b)==e['sha256'],'exact helper')
 cmd=[sys.executable,'-B','-O',str(H/'precount/check.py'),'--study-root',str(v.study_root),'--public-root',str(v.public_root),'--out',str(v.out/'precount_report.json')]
 r=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);need(r.returncode==0,'accepted precount replay '+r.stdout)
 counts,cache=replay(v.study_root,v.public_root);need(counts==load('author_counts.json'),'all870PDF/2030raw cells and hashes');semantic(counts,load('input_spec.json'),load('listing_screen.json'),load('completion.json'))
 for n,t in tables(counts).items():need(t==(H/n).read_text(),'complete CSV '+n)
 need(reader()==(H/'reader.tex').read_text(),'reader exact input derivation');tests=controls(counts,cache);render=None
 if v.render:
  render=build(v.out/'reader',v.xelatex);old=pypdf.PdfReader(H/'reader.pdf');fresh=pypdf.PdfReader(v.out/'reader/reader.pdf');need(len(old.pages)==len(fresh.pages)==3,'three reader pages');need([p.extract_text()for p in old.pages]==[p.extract_text()for p in fresh.pages],'exact reader page text');render['pages']=3
 report=dict(status='PASS_COMPLETE_ADDITIVE_INPUT_REPLAY',precount_controls=22,controls=tests,PDF_cells=870,raw_cells=2030,unchanged_PDF_cells=630,unchanged_raw_cells=450,physical_pages=286,new_PDFs=8,new_PDF_pages=57,new_Type1_font_dictionaries=104,new_encoded_Type1_classes=1743,Type0_dictionaries_outside_Type1_walker=26,mathematical_repair_classes=50,mathematical_repair_occurrences=462,drawing_classes=32,drawing_occurrences=423,whole_raw_contents=203,whole_raw_occurrences=253,required_contents=99,raw_files_executed=False,formal_executed=False,reader=render,factors=None,software_inclusive_factor=None)
 (v.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
