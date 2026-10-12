#!/usr/bin/env python3
"""Compare freshly independent counts/events with the complete author records."""
from pathlib import Path
import copy,csv,json
import pypdf
from recount import require,digest

def load(p):return json.loads(p.read_text())
def check_payload(counts,spec,actual,baseline,raw_counts,text_hashes,raw_hashes,root):
 require(set(counts['documents'])==set(baseline['documents'])|{'L121','A9'},'complete 22-document set')
 require(set(counts['raw_files_measured'])==set(raw_counts),'complete 45-file set')
 require(counts['pdf_metric_cells']==660 and counts['raw_metric_cells']==450 and counts['pdf_pages']==240,'all coordinates/pages')
 require(counts['factors']is None and counts['software_inclusive_factor']is None and counts['new_original_credit']==0,'input only')
 for key,val in baseline['documents'].items():require(counts['documents'][key]==val,'600 old PDF cells/metadata literal')
 for key,val in baseline['raw_files_measured'].items():require(counts['raw_files_measured'][key]==val,'300 old raw cells/metadata literal')
 for key,val in actual['documents'].items():
  wanted=counts['documents'][key];row=spec[key];pdf=root/row['path'];pages=[pg.extract_text()or''for pg in pypdf.PdfReader(pdf).pages];raw='\n'.join(pages)
  require(wanted['pages']==val['pages']and wanted['pdf_sha256']==val['pdf_sha256'],'whole new PDF')
  require(row['included_spans']==[dict(start=0,end=len(raw),sha256=digest(raw.encode()))]and row['whole_document']and row['extraction_sha256']==digest(raw.encode()),'whole extracted body')
  require(row['excluded_listings']==[],'no listing/proof removal')
  start=0;expected_pages=[]
  for no,text in enumerate(pages,1):expected_pages.append(dict(page=no,start=start,end=start+len(text),sha256=digest(text.encode()),empty_extraction=not text));start+=len(text)+1
  require(row['page_bindings']==expected_pages,'every exact page boundary')
  require([(r['start'],r['end'])for r in row['excluded_furniture']]==[tuple(r)for r in val['furniture_cuts']],'independent furniture occurrences')
  for r in row['excluded_furniture']:require(raw[r['start']:r['end']]==r['literal']and digest(r['literal'].encode())==r['sha256'],'cut literal/hash')
  expect=sorted(val['glyph_repairs'],key=lambda r:r['offset']);got=row['glyph_substitutions'];require(len(got)==len(expect)==wanted['glyph_substitutions'],'complete glyph repairs')
  for old,new in zip(expect,got):
   require(new['start']==old['offset']and new['end']==old['offset']+1 and new['input']==old['input']and new['output']==old['output'],'exact independently inferred repair')
   ev=new['pdf_events'];require(len(ev)==1 and ev[0]['font_identity']==old['font_identity']and ev[0]['encoded_byte']==old['encoded_byte']and ev[0]['glyph_name']==old['glyph_name'],'actual dictionary/encoded glyph at offset')
   pg=expected_pages[new['page']-1];require(new['start']==pg['start']+new['page_offset']and pg['start']<=new['context_start']<=new['start']<new['end']<=new['context_end']<=pg['end'],'repair page/context')
   require(digest(raw[new['context_start']:new['context_end']].encode())==new['context_sha256'],'repair context bytes')
  for variant,norms in val['metrics'].items():
   for norm,own in norms.items():
    provided=wanted['metrics'][variant][norm];require(provided=={k:v for k,v in own.items()if k!='normalized_text_sha256'},'all60 independently counted PDF cells/hashes')
    require(text_hashes[key][variant][norm]==own['normalized_text_sha256'],'complete normalized PDF text hash')
 for key,val in raw_counts.items():
  provided=counts['raw_files_measured'][key]
  for norm,own in val['metrics'].items():
   require(provided['metrics'][norm]=={k:v for k,v in own.items()if k!='normalized_text_sha256'},'all450 independent raw cells/hashes')
   if key.startswith('L121_'):require(raw_hashes[key][norm]==own['normalized_text_sha256'],'whole new raw normalized hash')
 return True

def controls(args):
 base=copy.deepcopy(args[:2]);rest=args[2:];out=[]
 def reject(name,change):
  x=copy.deepcopy(base);change(x)
  try:check_payload(*x,*rest)
  except(ValueError,KeyError,IndexError,TypeError)as e:out.append(dict(name=name,status='REJECTED',reason=str(e)));return
  raise ValueError('surviving independent control '+name)
 reject('change one new PDF unit',lambda x:x[0]['documents']['L121']['metrics']['raw_untrimmed']['NFC'].update(whitespace_tokens=0))
 reject('change one inherited PDF unit',lambda x:x[0]['documents']['U']['metrics']['calibrated_selected']['NFC'].update(characters_without_whitespace=0))
 reject('change one new raw-file unit',lambda x:x[0]['raw_files_measured']['L121_FILE01']['metrics']['NFC'].update(whitespace_tokens=0))
 reject('change one inherited raw-file unit',lambda x:x[0]['raw_files_measured']['P01']['metrics']['NFC'].update(whitespace_tokens=0))
 reject('drop untrimmed sensitivity',lambda x:x[0]['documents']['A9']['metrics'].pop('raw_untrimmed'))
 reject('truncate whole body span',lambda x:x[1]['L121']['included_spans'][0].update(end=10))
 reject('remove source last page as furniture',lambda x:x[1]['L121']['excluded_furniture'][-1].update(end=x[1]['L121']['page_bindings'][-1]['end']))
 reject('delete mathematical presentation as executable listing',lambda x:x[1]['L121']['excluded_listings'].append({'page':10}))
 reject('alter a bracket-component output',lambda x:next(r for r in x[1]['L121']['glyph_substitutions']if r['pdf_events'][0]['glyph_name']=='bracketlefttp').update(output='{'))
 reject('collapse tail and arrow',lambda x:next(r for r in x[1]['A9']['glyph_substitutions']if r['pdf_events'][0]['glyph_name']=='mapsto').update(output='↦'))
 reject('wrong actual encoded byte',lambda x:x[1]['L121']['glyph_substitutions'][0]['pdf_events'][0].update(encoded_byte=0))
 reject('wrong dictionary identity',lambda x:x[1]['A9']['glyph_substitutions'][0]['pdf_events'][0].update(font_identity='0'*64))
 reject('false local context',lambda x:x[1]['A9']['glyph_substitutions'][0].update(context_sha256='0'*64))
 reject('omit visible script glyph',lambda x:x[1]['A9']['glyph_substitutions'].pop())
 return out

def run(packet,root,actual,scope):
 counts=load(packet/'author_counts.json');spec=load(packet/'input_spec.json');baseline=load(packet/'precount/baseline/author_counts.json');th=load(packet/'new_text_hashes.json');rh=load(packet/'new_raw_text_hashes.json')
 args=(counts,spec,actual,baseline,scope['raw_counts'],th,rh,root);check_payload(*args)
 pdf_rows=list(csv.DictReader((packet/'pdf_counts.csv').open()));raw_rows=list(csv.DictReader((packet/'raw_counts.csv').open()))
 require(len(pdf_rows)==660 and len(raw_rows)==450,'all CSV cells')
 pd={(r['document'],r['variant'],r['normalization'],r['metric']):int(r['count'])for r in pdf_rows};rd={(r['file'],r['normalization'],r['metric']):int(r['count'])for r in raw_rows}
 require(len(pd)==660 and len(rd)==450,'no duplicate CSV keys')
 for(k,v,n,m),num in pd.items():require(num==counts['documents'][k]['metrics'][v][n][m],'PDF CSV value')
 for(k,n,m),num in rd.items():require(num==counts['raw_files_measured'][k]['metrics'][n][m],'raw CSV value')
 return dict(status='PASS_ALL_AUTHOR_RECORDS_MATCH_INDEPENDENT_RECOUNT',new_PDF_cells=60,inherited_PDF_cells_literal=600,raw_cells=450,PDF_CSV_cells=660,raw_CSV_cells=450,new_PDF_hashes=12,new_raw_hashes=30,controls=controls(args),ratios=None)
