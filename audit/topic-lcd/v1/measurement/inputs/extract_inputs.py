"""Recount the complete fixed LCD manuscript/file input boundary; no factors."""
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
 return dict(whitespace_tokens=len(c.split()),alphanumeric_units=len(re.findall(r'[^\W_]+',t)),characters_without_whitespace=sum(not x.isspace()for x in t),characters_with_collapsed_whitespace=len(c),utf8_bytes_with_collapsed_whitespace=len(c.encode()),normalized_text_sha256=sha(t.encode()),collapsed_text_sha256=sha(c.encode()))
def furniture(key,raw,pages):
 cuts=[]
 headers={2:'2 BACKGROUND AND DEFINITIONS',3:'3 SPECIAL LCD CODES FROM GRAPHS',4:'3 SPECIAL LCD CODES FROM GRAPHS',5:'3 SPECIAL LCD CODES FROM GRAPHS',6:'4 UNIFORM SUBSET GRAPHS',7:'4 UNIFORM SUBSET GRAPHS',8:'4 UNIFORM SUBSET GRAPHS',9:'4 UNIFORM SUBSET GRAPHS',10:'4 UNIFORM SUBSET GRAPHS',11:'5 STRONGLY REGULAR GRAPHS',12:'5 STRONGLY REGULAR GRAPHS',13:'5 STRONGLY REGULAR GRAPHS',14:'6 OTHER LCD CODES FROM GRAPHS',15:'7 CONCLUSION',16:'REFERENCES',17:'REFERENCES'}
 for pg in pages:
  n=pg['page'];t=raw[pg['start']:pg['end']]
  if key=='L050':
   page=n+238;expected=('MATHEMATICAL COMMUNICATIONS '+str(page)+'\n')if n==1 else ((str(page)+' D. Leemans and B. G. Rodrigues\n')if n%2==0 else('Linear codes with complementary duals '+str(page)+'\n'))
   need(t.startswith(expected),'literal journal running header');a=pg['start'];b=a+len(expected);role='running_header_with_printed_page'
  elif key=='F017' and n>1:
   expected=headers[n]+' '+str(n)+'\n';need(t.startswith(expected),'literal manuscript running header');a=pg['start'];b=a+len(expected);role='running_section_header_with_page'
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

def replay(study_root,prepare=False):
 p=load('policy.json');d=load('document_map.json')
 need(p==load('protocol_addition_L050/policy.json') and d==load('protocol_addition_L050/document_map.json'),'fixed current pre-count boundary')
 old=load('protocol_freeze/policy.json');need(all(p[k]==old[k]for k in ['primary','variants','normalizations','units','unit_definitions','unknowns']),'unchanged measurement policy')
 need(p['primary']==dict(variant='calibrated_selected',normalization='NFC',unit='characters_without_whitespace'),'fixed primary')
 need(pypdf.__version__=='6.13.0' and fontTools.__version__=='4.63.0','pinned parsers')
 need(not p['factors_permitted'] and p['ratio'] is None and d['complete_topic_boundary'],'inputs only; no ratios before independent acceptance')
 need([(r['key'],r['pages'])for r in d['documents']]==[('L050',11),('F017',17),('U_LCD',14),('A_F017',12),('A_L050',15)],'exact complete document extent')
 need(d['physical_pages']==69,'all69 pages')
 docs={};spec={};audits={};alias_rows=[];cache={}
 for row in d['documents']:
  path=study_root/row['path'];b=path.read_bytes();need(len(b)==row['bytes']and sha(b)==row['sha256'],'whole PDF pin');key=row['key']
  raw,fonts,pages,meta=extract(path,False);need(len(pages)==row['pages'],'full page extent');need(raw=='\n'.join(pg.extract_text()or''for pg in pypdf.PdfReader(path).pages),'literal uninstrumented extraction')
  events,audits[key]=actual_event_alignment(path,raw,fonts,pages,type1_math_only=key=='A_F017',generated_newline_offsets=set(meta['generated_newline_offsets']))
  spec[key],aliases=prepare_one(key,row,raw,fonts,pages,meta,events,audits[key]);validate_one(key,spec[key],raw,fonts,pages,meta,events,audits[key]);alias_rows.extend(aliases)
  texts=dict(raw_untrimmed=raw,raw_selected=transformed(raw,spec[key]),calibrated_selected=transformed(raw,spec[key],True))
  docs[key]=dict(pdf_sha256=row['sha256'],pages=len(pages),calibration_occurrences=len(spec[key]['glyph_substitutions']),furniture_occurrences=len(spec[key]['excluded_furniture']),variants={v:{n:metrics(t,n)for n in p['normalizations']}for v,t in texts.items()})
  cache[key]=(raw,fonts,pages,meta,events,audits[key])
 if prepare:
  put('input_spec.json',spec);put('glyph_aliases.json',{'aliases':alias_rows});put('font_audit.json',audits)
 else:
  need(spec==load('input_spec.json') and alias_rows==load('glyph_aliases.json')['aliases']and audits==load('font_audit.json'),'all frozen event/outline/furniture evidence')
 previous=load('previous_stage/counts.json')
 need(all(docs[k]==v for k,v in previous['documents'].items()),'all120 prior PDF cells and full text hashes unchanged')
 result=dict(status='COMPLETE_INPUT_PROPOSAL_PENDING_DISTINCT_REVIEW',documents=docs,PDF_metric_cells=150,physical_pages=69,complete_topic_boundary=True,ratio=None,software_inclusive_factor=None,new_original_credit=0,source_wide_scientific_acceptance=True,independent_input_acceptance=False)
 return result,cache
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--prepare',action='store_true');a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True);result,_=replay(a.study_root,a.prepare);(a.out/'counts.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('PASS150PDFcells/69pages; no factors')
