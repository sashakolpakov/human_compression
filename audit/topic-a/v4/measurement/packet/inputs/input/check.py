#!/usr/bin/env python3
"""Portable frozen-input replay; no mathematical programs or formal builds."""
from pathlib import Path
import argparse,copy,csv,hashlib,io,json,subprocess,sys
import pypdf
from extract_inputs import replay,load,need,sha,validate_one,H
from build_reader import reader,build

def semantic(c,spec,listing,completion):
 old=load('precount/baseline/author_counts.json');p=load('precount/policy.json')
 need(set(c['documents'])==set(old['documents'])|{'L121','A9'} and set(c['raw_files_measured'])=={r['id']for r in load('precount/raw_inventory.json')['files']},'full exact counted IDs')
 need(all(c['documents'][k]==v for k,v in old['documents'].items())and all(c['raw_files_measured'][k]==v for k,v in old['raw_files_measured'].items()),'all old vectors unchanged')
 need((c['pdf_documents'],c['pdf_pages'],c['pdf_metric_cells'],c['raw_files'],c['raw_metric_cells'])==(22,240,660,45,450),'complete dimensions')
 need(c['factors']is None and c['software_inclusive_factor']is None and c['new_original_credit']==0 and not c['input_accepted']and c['science_accepted'],'no premature rate/credit')
 need(completion['new_metrics_evaluated']and not completion['input_accepted']and completion['new_ratios']is None,'separate additive extraction status')
 need({r['document']for r in listing['new_documents']}=={'L121','A9'}and all(r['executable_listings']==[]and r['masks']==[]and r['all_pages_viewed']for r in listing['new_documents']),'actual symmetric listing screen')
 need(listing['required_certificates_still_premises']and listing['software_inclusive_factor']is None,'required evidence not optional')
 for k,pages,repairs in [('L121',12,18),('A9',11,51)]:
  need(c['documents'][k]['pages']==pages and c['documents'][k]['glyph_substitutions']==repairs and len(spec[k]['excluded_furniture'])==pages and not spec[k]['excluded_listings'],'allnewpage/calibrationboundary')
  need(set(c['documents'][k]['metrics'])==set(p['variants']),'complete three variants')
  for v in p['variants']:
   need(set(c['documents'][k]['metrics'][v])==set(p['normalizations']),'both normalizations')
   for n in p['normalizations']:need(set(c['documents'][k]['metrics'][v][n])==set(p['metrics'])|{'collapsed_text_sha256'},'five units and hash')
 return True

def tables(c):
 def table(header,rows):
  o=io.StringIO(newline='');w=csv.writer(o,lineterminator='\n');w.writerow(header);w.writerows(rows);return o.getvalue()
 rows=[]
 for k,d in c['documents'].items():
  for v in load('policy.json')['variants']:
   for n in load('policy.json')['normalizations']:
    for m in load('policy.json')['metrics']:rows.append([k,v,n,m,d['metrics'][v][n][m]])
 raw=[]
 for k,d in c['raw_files_measured'].items():
  for n in load('policy.json')['normalizations']:
   for m in load('policy.json')['metrics']:raw.append([k,n,m,d['metrics'][n][m]])
 return {'pdf_counts.csv':table(['document','variant','normalization','metric','count'],rows),'raw_counts.csv':table(['file','normalization','metric','count'],raw)}

def controls(c,cache):
 done=[]
 def rejects(name,f):
  try:f()
  except(ValueError,KeyError,AssertionError):done.append(name)
  else:raise ValueError('control survived: '+name)
 base=[c,load('input_spec.json'),load('listing_screen.json'),load('completion.json')]
 def mutate(name,f):
  x=copy.deepcopy(base);f(x);rejects(name,lambda:semantic(*x))
 mutate('drop L121',lambda x:x[0]['documents'].pop('L121'))
 mutate('alter inherited PDF count',lambda x:x[0]['documents']['U']['metrics']['calibrated_selected']['NFC'].update(characters_without_whitespace=0))
 mutate('alter inherited raw count',lambda x:x[0]['raw_files_measured']['P01']['metrics']['NFC'].update(whitespace_tokens=0))
 mutate('drop new required file',lambda x:x[0]['raw_files_measured'].pop('L121_FILE01'))
 mutate('software unknown becomes zero',lambda x:x[0].update(software_inclusive_factor=0))
 mutate('premature input acceptance',lambda x:x[0].update(input_accepted=True))
 mutate('new original credit',lambda x:x[0].update(new_original_credit=1))
 mutate('delete proof prose as code',lambda x:x[1]['L121']['excluded_listings'].append({'page':10}))
 mutate('relabel required certificate optional',lambda x:x[2].update(required_certificates_still_premises=False))
 mutate('remove source page',lambda x:x[0]['documents']['L121'].update(pages=11))
 mutate('omit sensitivity',lambda x:x[0]['documents']['A9']['metrics'].pop('raw_untrimmed'))
 def row_mut(name,key,f):
  row=copy.deepcopy(base[1][key]);f(row);rejects(name,lambda:validate_one(key,row,*cache[key]))
 row_mut('wrong bracket component','L121',lambda r:r['glyph_substitutions'][0].update(output='{'))
 row_mut('remove source repair','L121',lambda r:r['glyph_substitutions'].pop())
 row_mut('wrong actual encoding byte','L121',lambda r:r['glyph_substitutions'][0]['pdf_events'][0].update(encoded_byte=0))
 row_mut('wrong actual dictionary','A9',lambda r:r['glyph_substitutions'][0]['pdf_events'][0].update(font_dictionary_sha256='0'*64))
 row_mut('wrong event context','A9',lambda r:r['glyph_substitutions'][0].update(context_sha256='0'*64))
 row_mut('remove visible printable brace repair','A9',lambda r:r['glyph_substitutions'].__delitem__(next(i for i,g in enumerate(r['glyph_substitutions'])if g['pdf_events'][0]['glyph_name']=='braceleftBigg')))
 row_mut('merge mapsto with arrow','A9',lambda r:next(g for g in r['glyph_substitutions']if g['pdf_events'][0]['glyph_name']=='mapsto').update(end=next(g for g in r['glyph_substitutions']if g['pdf_events'][0]['glyph_name']=='mapsto')['end']+1,output='↦'))
 row_mut('delete references as furniture','L121',lambda r:r['excluded_furniture'][-1].update(end=r['page_bindings'][-1]['end']))
 row_mut('drop footer mask','A9',lambda r:r['excluded_furniture'].pop())
 row_mut('generated whitespace becomes glyph','A9',lambda r:r['extraction_metadata']['generated_newline_offsets'].append(0))
 return done

def main():
 a=argparse.ArgumentParser();a.add_argument('--study-root',type=Path,required=True);a.add_argument('--public-root',type=Path,required=True);a.add_argument('--out',type=Path,required=True);a.add_argument('--render',action='store_true');a.add_argument('--xelatex',default='xelatex');v=a.parse_args();need(not v.out.exists(),'fresh output directory');v.out.mkdir(parents=True)
 if(H/'manifest.json').exists():
  for e in load('manifest.json')['exports']:
   b=(H/e['path']).read_bytes();need(len(b)==e['bytes']and sha(b)==e['sha256'],'frozen export '+e['path'])
 for e in load('helper_provenance.json'):
  b=(H/e['path']).read_bytes();need(len(b)==e['bytes']and sha(b)==e['sha256'],'exact inherited helper')
 cmd=[sys.executable,'-B','-O',str(H/'precount/check.py'),'--study-root',str(v.study_root),'--public-root',str(v.public_root),'--out',str(v.out/'precount_report.json')]
 r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);need(r.returncode==0,'precount replay '+r.stdout)
 counts,cache=replay(v.study_root,v.public_root);need(counts==load('author_counts.json'),'all660 PDF and450 raw cells/hashes');semantic(counts,load('input_spec.json'),load('listing_screen.json'),load('completion.json'))
 for name,t in tables(counts).items():need(t==(H/name).read_text(),'complete CSV '+name)
 need(reader()==(H/'reader.tex').read_text(),'exact reader source from input counts')
 tests=controls(counts,cache);render=None
 if v.render:
  render=build(v.out/'reader',v.xelatex);pdf=pypdf.PdfReader(H/'reader.pdf');fresh=pypdf.PdfReader(v.out/'reader/reader.pdf');need(len(pdf.pages)==len(fresh.pages)==2,'two reader pages');need([p.extract_text()for p in pdf.pages]==[p.extract_text()for p in fresh.pages],'exact reader page text');render['pages']=2
 report=dict(status='PASS_COMPLETE_ADDITIVE_INPUT_REPLAY',precount_controls=14,controls=tests,PDF_cells=660,raw_cells=450,unchanged_PDF_cells=600,unchanged_raw_cells=300,physical_pages=240,new_PDF_pages=23,new_font_dictionaries=36,new_encoded_classes=871,new_substitution_classes=17,new_substitution_occurrences=69,whole_raw_contents=45,required_whole_files=20,raw_files_executed=False,formal_executed=False,reader=render,factors=None,software_inclusive_factor=None)
 (v.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
