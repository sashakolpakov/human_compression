"""Eight new whole PDF inputs and complete raw closure; exact inherited vectors, no factors."""
from pathlib import Path
import argparse,hashlib,json,re,unicodedata
import pypdf,fontTools
from pdf_text import extract
from font_tools import actual_event_alignment,need
from calibration import output,drawing
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
  if key=='L003' and n>1:
   expected=(str(n)+' MARIA ELISA FERNANDES, DIMITRI LEEMANS, AND ASIA IVI ´C WEISS\n')if n%2==0 else('HEXAGONAL EXTENSIONS OF TOROIDAL MAPS AND HYPERMAPS '+str(n)+'\n')
   need(t.startswith(expected),'literal source running header page '+str(n));a=pg['start'];b=a+len(expected);role='running_header_with_printed_page'
  else:
   m=re.search(r'(?:^|\n)'+str(n)+r'\s*\Z',t);need(m is not None,'trailing physical page number '+key+str(n));a=pg['start']+m.start()+(t[m.start()]=='\n');b=pg['end'];role='physical_page_number'
  cuts.append(dict(page=n,start=a,end=b,role=role,literal=raw[a:b],sha256=sha(raw[a:b].encode())))
 return cuts

def event_row(at,event,raw,fonts,pages,events):
 n=len(event['decoded_text']);pg=pages[event['page']-1];left=max(pg['start'],at-32);right=min(pg['end'],at+n+32)
 return dict(start=at,end=at+n,input=event['decoded_text'],input_font=fonts[at],page=event['page'],page_offset=at-pg['start'],context_start=left,context_end=right,context_sha256=sha(raw[left:right].encode()),pdf_events=[events[at+i]for i in range(n)])
def prepare_one(key,row,raw,fonts,pages,meta,events,audit):
 subs=[];graphics=[]
 for at,event in sorted(events.items()):
  if event['decoded_character_index']!=0:continue
  value=output(event)
  if value is not None:subs.append(dict(**event_row(at,event,raw,fonts,pages,events),output=value))
  if drawing(event):graphics.append(dict(**event_row(at,event,raw,fonts,pages,events),treatment='RETAIN_LITERAL_EXTRACTED_ALIAS'))
 return dict(**row,extraction_sha256=sha(raw.encode()),page_bindings=pages,extraction_metadata=meta,included_spans=[dict(start=0,end=len(raw),sha256=sha(raw.encode()))],excluded_furniture=furniture(key,raw,pages),excluded_listings=[],glyph_substitutions=subs,drawing_occurrences=graphics)
def validate_one(key,row,raw,fonts,pages,meta,events,audit):
 expected=prepare_one(key,{k:row[k]for k in ['key','path','pages','role','whole_document','bytes','sha256']},raw,fonts,pages,meta,events,audit)
 need(row==expected,'exact page/furniture/actual-event calibration '+key)
 covered=set();graphics=set()
 for s in row['drawing_occurrences']:graphics.update(range(s['start'],s['end']))
 for s in row['glyph_substitutions']:
  a,b=s['start'],s['end'];need(raw[a:b]==s['input'],'literal repair input');need(not covered.intersection(range(a,b)),'no overlapping repairs');covered.update(range(a,b))
  need(all(fonts[i]==s['input_font']for i in range(a,b)),'repair exact font');need(not set(range(a,b)).intersection(meta['generated_newline_offsets']),'no generated newline repair')
  need(not any(max(a,f['start'])<min(b,f['end'])for f in row['excluded_furniture']),'no repair hidden by furniture')
 need(not covered.intersection(graphics),'graphic aliases never repaired')
 for i,c in enumerate(raw):
  need(not ((unicodedata.category(c)in('Cc','Co')and c not in '\r\n\t')or c=='\ufffd')or i in covered|graphics,'all control/private-use glyphs accounted '+key+':'+str(i))
  if i in events and c.isspace():need(output(events[i])is None or i in covered,'visible whitespace preserved')
 return True

def transformed(raw,row,calibrated=False):
 edits=[(f['start'],f['end'],'\n')for f in row['excluded_furniture']]
 if calibrated:edits.extend((g['start'],g['end'],g['output'])for g in row['glyph_substitutions'])
 result=[];at=0
 for a,b,v in sorted(edits):need(at<=a<b,'disjoint edits');result.extend([raw[at:a],v]);at=b
 result.append(raw[at:]);return ''.join(result)
def resolve(row,study,public):return dict(study=study,public=public)[row['root']]/row['path']
def bound(path,row):
 b=path.read_bytes();need(len(b)==row['bytes']and sha(b)==row['sha256'],'whole file '+str(path));return b

def audit_new(study_root,private_cache=False):
 spec={};audits={};cache={}
 saved_m=load('private/extraction_metadata.json')if private_cache else None
 saved_e=load('private/events.json')if private_cache else None
 for row in load('document_map.json')['documents']:
  path=study_root/row['path'];bound(path,row);key=row['key']
  if private_cache:
   raw=(H/'private'/f'{key}_raw.txt').read_text();fonts=saved_m[key]['fonts'];pages=saved_m[key]['pages'];meta=saved_m[key]['meta'];events={int(k):v for k,v in saved_e[key].items()};audits[key]=load('font_audit.json')[key]
  else:
   raw,fonts,pages,meta=extract(path,False)
   need(raw=='\n'.join(pg.extract_text()or''for pg in pypdf.PdfReader(path).pages),'literal uninstrumented extraction')
   events,audits[key]=actual_event_alignment(path,raw,fonts,pages,type1_math_only=(key!='L003'),generated_newline_offsets=set(meta['generated_newline_offsets']))
  need(len(pages)==row['pages'],'complete PDF pages')
  spec[key]=prepare_one(key,row,raw,fonts,pages,meta,events,audits[key]);validate_one(key,spec[key],raw,fonts,pages,meta,events,audits[key]);cache[key]=(raw,fonts,pages,meta,events,audits[key])
 return spec,audits,cache

def check_calibration_freeze():
 manifest=load('calibration_freeze/manifest.json')
 for r in manifest['bindings']:bound(H/r['path'],r)
 need(manifest['new_metrics_evaluated']is False,'calibration precedes scoring')
def replay(study_root,public_root,prepare=False):
 check_calibration_freeze();p=load('policy.json');need(p==load('precount/policy.json'),'unchanged frozen pre-count policy')
 need(pypdf.__version__=='6.13.0'and fontTools.__version__=='4.63.0','pinned extraction versions')
 old=load('precount/baseline/author_counts.json');inherit=load('precount/inheritance.json')
 for row in load('precount/documents.json')['documents']:bound(resolve(row['file'],study_root,public_root),row['file'])
 for row in load('precount/bindings.json')['references']:bound(resolve(row,study_root,public_root),row)
 spec,audits,cache=audit_new(study_root)
 need(spec==load('input_spec.json')and audits==load('font_audit.json'),'exact new calibration, furniture and font evidence')
 docs={k:old['documents'][k]for k in inherit['reuse_document_ids']};text_hashes={}
 for row in load('document_map.json')['documents']:
  key=row['key'];raw=cache[key][0]
  texts=dict(raw_untrimmed=raw,raw_selected=transformed(raw,spec[key]),calibrated_selected=transformed(raw,spec[key],True))
  docs[key]=dict(pdf_sha256=row['sha256'],pages=row['pages'],glyph_substitutions=len(spec[key]['glyph_substitutions']),drawing_occurrences=len(spec[key]['drawing_occurrences']),metrics={v:{n:metrics(t,n)for n in p['normalizations']}for v,t in texts.items()})
  text_hashes[key]={v:{n:sha(unicodedata.normalize(n,t).encode())for n in p['normalizations']}for v,t in texts.items()}
 inventory=load('precount/raw_inventory.json');occ={r['occurrence_id']:r for r in inventory['occurrences']};raw_files={};raw_hashes={}
 for row in inventory['contents']:
  bs=[bound(resolve(occ[i],study_root,public_root),occ[i])for i in row['occurrence_ids']];need(all(b==bs[0]for b in bs),'exact within-topic duplicate bytes')
  b=bs[0];t=b.decode('utf8');need(sha(b)==row['sha256']and len(b)==row['bytes'],'whole content binding')
  if row['inherited_A9_raw_id']is not None:
   prior=old['raw_files_measured'][row['inherited_A9_raw_id']];need(prior['file']['sha256']==row['sha256'],'exact old raw content');m=prior['metrics']
  else:m={n:metrics(t,n)for n in p['normalizations']}
  raw_files[row['id']]=dict(sha256=row['sha256'],bytes=row['bytes'],occurrence_ids=row['occurrence_ids'],roles=row['roles'],coarse_roles=row['coarse_roles'],accounting_class=row['accounting_class'],mathematical_premise=row['mathematical_premise'],inherited_A9_raw_id=row['inherited_A9_raw_id'],metrics=m)
  raw_hashes[row['id']]={n:sha(unicodedata.normalize(n,t).encode())for n in p['normalizations']}
 need(all(docs[k]==old['documents'][k]for k in inherit['reuse_document_ids']),'all630 inherited PDF cells preserved exactly')
 need(all(raw_files[r['id']]['metrics']==old['raw_files_measured'][r['inherited_A9_raw_id']]['metrics']for r in inventory['contents']if r['inherited_A9_raw_id']is not None),'all450 inherited raw cells preserved exactly')
 if prepare:put('new_text_hashes.json',text_hashes);put('raw_text_hashes.json',raw_hashes)
 else:need(text_hashes==load('new_text_hashes.json')and raw_hashes==load('raw_text_hashes.json'),'complete normalized text hashes')
 result=dict(status='AUTHOR_INPUTS_PENDING_DISTINCT_REVIEW',policy_sha256=sha((H/'policy.json').read_bytes()),pdf_documents=29,pdf_pages=286,pdf_metric_cells=870,raw_files=203,raw_metric_cells=2030,unchanged_pdf_metric_cells=630,unchanged_raw_metric_cells=450,new_pdf_metric_cells=240,new_raw_metric_cells=1580,documents=docs,raw_files_measured=raw_files,factors=None,software_inclusive_factor=None,new_original_credit=0,science_accepted=True,input_accepted=False)
 return result,cache
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--public-root',type=Path);ap.add_argument('--out',type=Path);ap.add_argument('--prepare-calibration',action='store_true');ap.add_argument('--prepare-counts',action='store_true');a=ap.parse_args()
 if a.prepare_calibration:
  need(not(H/'calibration_freeze/manifest.json').exists(),'preserve calibration freeze');s,au,_=audit_new(a.study_root,private_cache=True);put('input_spec.json',s);need(au==load('font_audit.json'),'private audit consistency');print('Prepared event/furniture spec; no metrics')
 else:
  need(a.public_root is not None and a.out is not None and not a.out.exists(),'fresh output plus roots');a.out.mkdir(parents=True);result,_=replay(a.study_root,a.public_root,a.prepare_counts);(a.out/'counts.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('PASS870PDF/2030rawcells;1080 inherited; no factors')
