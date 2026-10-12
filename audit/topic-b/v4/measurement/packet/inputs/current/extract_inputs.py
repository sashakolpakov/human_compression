"""Four complete new PDFs and nine whole new files; accepted B inputs stay exact."""
from pathlib import Path
import argparse,hashlib,json,re,unicodedata,copy
import pypdf,fontTools
from pdf_text import extract
from font_tools import actual_event_alignment,need
from unicode_fonts import audit as unicode_audit
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
 for pg in pages:
  n=pg['page'];t=raw[pg['start']:pg['end']]
  if key=='L047' and n>1:
   # Exact running head: first line contains the physical page and repeated title/authors.
   expected=([str(n)+' PETER J. CAMERON, MARIA ELISA FERNANDES, DIMITRI LEEMANS,AND MARK MIXER',str(n)+' PETER J. CAMERON, MARIA ELISA FERNANDES, DIMITRI LEEMANS, AND MARK MIXER']if n%2==0 else['STRING C-GROUPS AS TRANSITIVE SUBGROUPS OF S n '+str(n)])
   first=t.split('\n',1)[0];need(first in expected,'literal source running head');a=pg['start'];b=a+len(first)+1;role='repeated_running_head_and_page_number'
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

def code_inclusion(tex,text,files):
 names=re.findall(r'\\VerbatimInput(?:\[[^\]]*\])?\{([^}]+)\}',tex)
 need(names==list(files)and not re.search('firstline|lastline|firstnumber|lastnumber',tex),'six complete unpruned program files')
 def packed(s):return ''.join(unicodedata.normalize('NFKC',s).split()).replace('↪','').replace('⌋','').replace('→','')
 body=packed(text)
 for n,t in files.items():need(packed(t)in body,'entire printed program '+n)
 return dict(files=6,all_lines_included=True,normalization_only_for_inclusion_not_counts=True,wrap_glyphs_retained_in_all_measured_variants=True)

def replay(study,public,prepare=False):
 p=load('policy.json');need(p==load('precount/policy.json'),'unchanged precount policy');need(pypdf.__version__==p['toolchain']['pypdf']and fontTools.__version__==p['toolchain']['fonttools'],'pinned parser versions')
 old=load('precount/baseline/author_counts.json');retained=load('precount/baseline/retained_source_counts.json')
 for r in load('precount/bindings.json')['baseline_files']:
  need(bound(H/'precount/baseline'/r['path'],r)==bound(public/'audit/b-unified-measurement/v1/packet/inputs'/r['path'],r),'exact accepted baseline')
 docs=copy.deepcopy(old['documents']);spec={};audits={};aliases=[];hashes={};cache={};texts_by_key={}
 for d in load('precount/documents.json')['documents']:
  pdf=resolve(d['file'],study,public);bound(pdf,d['file'])
  if d['inherited']:continue
  key=d['key'];row=dict(key=key,path=d['file']['path'],pages=d['pages'],role=d['role'],whole_document=True,bytes=d['file']['bytes'],sha256=d['file']['sha256'])
  raw,fonts,pages,meta=extract(pdf,False);need(len(pages)==row['pages'],'complete PDF pages');need(raw=='\n'.join(pg.extract_text()or''for pg in pypdf.PdfReader(pdf).pages),'unaltered raw PDF extraction')
  events,audit=actual_event_alignment(pdf,raw,fonts,pages,type1_math_only=key!='L047',generated_newline_offsets=set(meta['generated_newline_offsets']))
  uni=unicode_audit(pdf,raw,fonts,pages)if key!='L047'else None
  audits[key]=dict(type1_symbols=audit,unicode_fonts=uni)
  spec[key],newaliases=prepare_one(key,row,raw,fonts,pages,meta,events,audit);validate_one(key,spec[key],raw,fonts,pages,meta,events,audit);aliases.extend(newaliases)
  texts=dict(raw_untrimmed=raw,raw_selected=transformed(raw,spec[key]),calibrated_selected=transformed(raw,spec[key],True));texts_by_key[key]=texts
  docs[key]=dict(pdf_sha256=row['sha256'],pages=len(pages),glyph_repairs=len(spec[key]['glyph_substitutions']),metrics={v:{n:metrics(t,n)for n in p['normalizations']}for v,t in texts.items()})
  hashes[key]={v:{n:sha(unicodedata.normalize(n,t).encode())for n in p['normalizations']}for v,t in texts.items()};cache[key]=(raw,fonts,pages,meta,events,audit)
 oldraw=copy.deepcopy(old['raw_files']);newraw={}
 for r in load('precount/raw_inventory.json')['files']:
  data=bound(resolve(r['file'],study,public),r['file']);m={n:metrics(data.decode('utf8'),n)for n in p['normalizations']}
  if r['inherited']:need(m==oldraw[r['category']][r['old_path']]['metrics'],'unchanged old whole-file vector')
  else:newraw[r['id']]=dict(file=r['file'],role=r['role'],category=r['category'],metrics=m)
 source_coordinates=copy.deepcopy(retained['coordinates'])
 for r in source_coordinates:r['sources']['L047']=docs['L047']['metrics'][r['variant']][r['normalization']][r['unit']];r['source_representations']['L047']='complete_PDF_'+r['variant']
 code_files={str(Path(r['file']['path']).relative_to('topic_B_L047_candidate_v2')):resolve(r['file'],study,public).read_text()for r in load('precount/raw_inventory.json')['files']if r['id'].startswith('NEW_PROGRAM')}
 included=code_inclusion((study/'topic_B_L047_candidate_v2/program-appendix.tex').read_text(),texts_by_key['CODE6']['raw_selected'],code_files)
 result=dict(status='AUTHOR_INPUTS_PENDING_DISTINCT_REVIEW',originals=p['originals'],documents=docs,retained_source_coordinates=retained,source_coordinates=source_coordinates,raw_files=oldraw,new_raw_files=newraw,inherited_own_PDF_cells=210,inherited_source_cells=150,inherited_article_sensitivity_cells=30,inherited_raw_cells=80,new_PDF_cells=120,new_raw_cells=90,total_main_document_cells=480,total_raw_cells=170,program_inclusion=included,whole_programs=10,drivers=5,partial_Lean_files=2,partial_declarations=14,new_declarations=0,science_adopted=True,input_accepted=False,factors=None,software_inclusive_comparison=None,source_software_cost=None,full_graphics_cost=None,external_proofs_cost=None,source_credit=0,question_credit=0)
 observations={'input_spec.json':spec,'font_audit.json':audits,'glyph_aliases.json':{'aliases':aliases},'new_text_hashes.json':hashes}
 for n,obj in observations.items():
  if prepare:put(n,obj)
  else:need(obj==load(n),'exact actual extraction/font/alias evidence '+n)
 return result,cache
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--prepare',action='store_true');a=ap.parse_args();need(not a.out.exists(),'fresh out');need(not a.prepare or not(H/'manifest.json').exists(),'cannot prepare frozen packet');a.out.mkdir(parents=True);c,_=replay(a.study_root,a.public_root,a.prepare);(a.out/'counts.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n');print('PASS input extraction; no factors')
