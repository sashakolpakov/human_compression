"""Recount two new PDFs and fifteen complete files; preserve accepted A vectors; no factors."""
from pathlib import Path
import argparse,hashlib,json,re,unicodedata
import pypdf,fontTools
from pdf_text import extract
from font_tools import actual_event_alignment,need
from calibration import output
H=Path(__file__).resolve().parent

def sha(b):return hashlib.sha256(b).hexdigest()
def load(n):return json.loads((H/n).read_text())
def put(n,x):(H/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def metrics(t,n):
 t=unicodedata.normalize(n,t);c=' '.join(t.split())
 return dict(whitespace_tokens=len(c.split()),alphanumeric_units=len(re.findall(r'[^\W_]+',t)),characters_without_whitespace=sum(not x.isspace()for x in t),characters_with_collapsed_whitespace=len(c),utf8_bytes_with_collapsed_whitespace=len(c.encode()),collapsed_text_sha256=sha(c.encode()))
def furniture(key,raw,pages):
 cuts=[]
 for pg in pages:
  n=pg['page'];t=raw[pg['start']:pg['end']]
  if key=='L121' and n>1:
   expected=(str(n)+' FERNANDES, LEEMANS, PIEDADE, AND WEISS\n')if n%2==0 else('TWO F AMILIES OF LOCALLY TOROIDAL REGULAR 4-HYPERTOPES ARISING FROM TOROIDS '+str(n)+'\n')
   need(t.startswith(expected),'literal source running header');a=pg['start'];b=a+len(expected);role='running_header_with_printed_page'
  else:
   m=re.search(r'(?:^|\n)'+str(n)+r'\s*\Z',t);need(m is not None,'trailing physical page number');a=pg['start']+m.start()+(t[m.start()]=='\n');b=pg['end'];role='physical_page_number'
  cuts.append(dict(page=n,start=a,end=b,role=role,literal=raw[a:b],sha256=sha(raw[a:b].encode())))
 return cuts

def prepare_one(key,row,raw,fonts,pages,meta,events,audit):
 subs=[];aliases=[]
 for r in audit['encoded_glyph_classes']:
  value=output(r)
  if value is not None:aliases.append(dict(document=key,**r,output=value,output_codepoint=f'U+{ord(value):04X}'))
 for at,event in sorted(events.items()):
  if event['decoded_character_index']!=0:continue
  value=output(event)
  if value is None:continue
  n=len(event['decoded_text']);pg=pages[event['page']-1];left=max(pg['start'],at-32);right=min(pg['end'],at+n+32)
  subs.append(dict(start=at,end=at+n,input=event['decoded_text'],input_font=fonts[at],output=value,page=event['page'],page_offset=at-pg['start'],context_start=left,context_end=right,context_sha256=sha(raw[left:right].encode()),pdf_events=[events[at+i]for i in range(n)]))
 return dict(**row,extraction_sha256=sha(raw.encode()),page_bindings=pages,extraction_metadata=meta,included_spans=[dict(start=0,end=len(raw),sha256=sha(raw.encode()))],excluded_furniture=furniture(key,raw,pages),excluded_listings=[],glyph_substitutions=subs),aliases

def validate_one(key,row,raw,fonts,pages,meta,events,audit):
 expected,aliases=prepare_one(key,{k:row[k]for k in ['key','path','pages','role','whole_document','bytes','sha256']},raw,fonts,pages,meta,events,audit)
 need(row==expected,'exact page/furniture/actual-event calibration '+key)
 covered=set()
 for s in row['glyph_substitutions']:
  a,b=s['start'],s['end'];need(raw[a:b]==s['input'],'literal repair input');need(not covered.intersection(range(a,b)),'no overlapping repairs');covered.update(range(a,b))
  need(all(fonts[i]==s['input_font'] for i in range(a,b)),'repair exact font');need(not set(range(a,b)).intersection(meta['generated_newline_offsets']),'no generated newline repair')
  need(not any(max(a,f['start'])<min(b,f['end'])for f in row['excluded_furniture']),'no repair hidden by furniture')
 for i,c in enumerate(raw):
  need(not ((unicodedata.category(c)in('Cc','Co') and c not in '\r\n\t') or c=='\ufffd')or i in covered,'all control/private-use glyphs accounted')
  if i in events and c.isspace():need(output(events[i]) is None or i in covered,'visible whitespace preserved')
 return aliases

def transformed(raw,row,calibrated=False):
 edits=[(f['start'],f['end'],'\n')for f in row['excluded_furniture']]
 if calibrated:edits.extend((g['start'],g['end'],g['output'])for g in row['glyph_substitutions'])
 result=[];at=0
 for a,b,v in sorted(edits):need(at<=a<b,'disjoint edits');result.extend([raw[at:a],v]);at=b
 result.append(raw[at:]);return ''.join(result)

def resolve(row,study,public):return dict(study=study,public=public)[row['root']]/row['path']
def bound(path,row):
 b=path.read_bytes();need(len(b)==row['bytes']and sha(b)==row['sha256'],'whole file '+str(path));return b

def replay(study_root,public_root,prepare=False):
 p=load('policy.json');need(p==load('precount/policy.json'),'unchanged frozen pre-count policy')
 need(pypdf.__version__=='6.13.0'and fontTools.__version__=='4.63.0','pinned extraction versions')
 old=load('precount/baseline/author_counts.json')
 baseline=public_root/'audit/topic-a/v3/measurement/packet/inputs/input'
 for name in ['author_counts.json','manifest.json','policy.json','raw_inventory.json']:
  need((H/'precount/baseline'/name).read_bytes()==(baseline/name).read_bytes(),'exact accepted baseline '+name)
 for row in load('precount/documents.json')['documents']:bound(resolve(row['file'],study_root,public_root),row['file'])
 for row in load('precount/bindings.json')['references']:bound(resolve(row,study_root,public_root),row)
 docs=dict(old['documents']);spec={};audits={};alias_rows=[];cache={};text_hashes={}
 for row in load('document_map.json')['documents']:
  path=study_root/row['path'];bound(path,row);key=row['key']
  raw,fonts,pages,meta=extract(path,False);need(len(pages)==row['pages'],'complete PDF pages')
  need(raw=='\n'.join(pg.extract_text()or''for pg in pypdf.PdfReader(path).pages),'literal uninstrumented extraction')
  events,audits[key]=actual_event_alignment(path,raw,fonts,pages,type1_math_only=False,generated_newline_offsets=set(meta['generated_newline_offsets']))
  spec[key],aliases=prepare_one(key,row,raw,fonts,pages,meta,events,audits[key]);validate_one(key,spec[key],raw,fonts,pages,meta,events,audits[key]);alias_rows.extend(aliases)
  texts=dict(raw_untrimmed=raw,raw_selected=transformed(raw,spec[key]),calibrated_selected=transformed(raw,spec[key],True))
  docs[key]=dict(pdf_sha256=row['sha256'],pages=len(pages),glyph_substitutions=len(spec[key]['glyph_substitutions']),metrics={v:{n:metrics(t,n)for n in p['normalizations']}for v,t in texts.items()})
  text_hashes[key]={v:{n:sha(unicodedata.normalize(n,t).encode())for n in p['normalizations']}for v,t in texts.items()}
  cache[key]=(raw,fonts,pages,meta,events,audits[key])
 if prepare:
  put('input_spec.json',spec);put('glyph_aliases.json',{'aliases':alias_rows});put('font_audit.json',audits);put('new_text_hashes.json',text_hashes)
 else:
  need(spec==load('input_spec.json')and alias_rows==load('glyph_aliases.json')['aliases']and audits==load('font_audit.json')and text_hashes==load('new_text_hashes.json'),'exact new calibration, furniture, font evidence and hashes')
 raw_files=dict(old['raw_files_measured']);new_raw_hashes={}
 for row in load('precount/raw_inventory.json')['files']:
  b=bound(resolve(row['file'],study_root,public_root),row['file']);t=b.decode('utf8');m={n:metrics(t,n)for n in p['normalizations']}
  if row['id']in old['raw_files_measured']:need(m==old['raw_files_measured'][row['id']]['metrics'],'unchanged old whole raw vectors')
  else:raw_files[row['id']]=dict(file=row['file'],role=row['role'],metrics=m);new_raw_hashes[row['id']]={n:sha(unicodedata.normalize(n,t).encode())for n in p['normalizations']}
 if prepare:put('new_raw_text_hashes.json',new_raw_hashes)
 else:need(new_raw_hashes==load('new_raw_text_hashes.json'),'new whole raw hashes')
 need(all(docs[k]==v for k,v in old['documents'].items())and all(raw_files[k]==v for k,v in old['raw_files_measured'].items()),'all900 inherited cells preserved exactly')
 result=dict(status='AUTHOR_INPUTS_PENDING_DISTINCT_REVIEW',policy_sha256=sha((H/'policy.json').read_bytes()),pdf_documents=22,pdf_pages=240,pdf_metric_cells=660,raw_files=45,raw_metric_cells=450,unchanged_pdf_metric_cells=600,unchanged_raw_metric_cells=300,new_pdf_metric_cells=60,new_raw_metric_cells=150,documents=docs,raw_files_measured=raw_files,factors=None,software_inclusive_factor=None,new_original_credit=0,science_accepted=True,input_accepted=False)
 return result,cache
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--prepare',action='store_true');a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True);result,_=replay(a.study_root,a.public_root,a.prepare);(a.out/'counts.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('PASS660PDF/450rawcells; 900 unchanged; no factors')
