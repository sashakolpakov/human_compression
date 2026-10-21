#!/usr/bin/env python3
"""Complete-document measurement inputs and actual-font replay; no factors."""
from pathlib import Path
import argparse,copy,json,re,unicodedata
import pypdf,fontTools
from font_tools import sha,need,actual_event_alignment
from calibration import glyph_alias
HERE=Path(__file__).resolve().parent
KEYS={'F015','L028','U_M','M1','M_CODE','U_CE','CE1','CE_CODE'}
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']

def metrics(text,form):
 text=unicodedata.normalize(form,text);collapsed=' '.join(text.split())
 return dict(whitespace_tokens=len(collapsed.split()),alphanumeric_units=len(re.findall(r'[^\W_]+',text)),characters_without_whitespace=sum(not c.isspace() for c in text),characters_with_collapsed_whitespace=len(collapsed),utf8_bytes_with_collapsed_whitespace=len(collapsed.encode()),collapsed_text_sha256=sha(collapsed.encode()))

def selected(raw,row):
 parts=[];at=0
 for f in row['excluded_furniture']:parts.append(raw[at:f['start']]);at=f['end']
 parts.append(raw[at:]);return '\n'.join(parts)

def expected_furniture(key,raw,pages):
 out=[]
 for pg in pages:
  n=pg['page'];t=raw[pg['start']:pg['end']];pair=None
  if key=='F015':
   if n>1:
    literal=f'the electronic journal of combinatorics 30(2) (2023), #P2.20 {n}'
    need(t.endswith(literal),'literal repeated source footer');pair=(len(t)-len(literal),len(t))
  elif key=='L028' and n>1:
   literal=f'{n} F. BUEKENHOUT, D. LEEMANS, AND P. TRANCHIDA\n' if n%2==0 else f'A NEW ALGORITHM FOR CHIRAL POLYTOPES {n}\n'
   need(t.startswith(literal),'literal repeated source header');pair=(0,len(literal))
  else:
   m=re.search(r'(?:^|\n)'+str(n)+r'\s*\Z',t);need(m is not None,'isolated page number')
   pair=(m.start()+(t[m.start()]=='\n'),len(t))
  if pair:
   a,b=pair;a+=pg['start'];b+=pg['start'];out.append(dict(page=n,start=a,end=b,literal=raw[a:b],sha256=sha(raw[a:b].encode())))
 return out

def validate_selection(key,raw,row,pages):
 need(row['pages']==len(pages) and row['page_bindings']==pages,'all physical pages '+key)
 need(row['extraction_sha256']==sha(raw.encode()),'complete extraction '+key)
 need(len(row['included_spans'])==1,'one complete-document span')
 span=row['included_spans'][0]
 need((span['start'],span['end'],span['sha256'])==(0,len(raw),sha(raw.encode())),'whole manuscript, no proof-span selection')
 expected=expected_furniture(key,raw,pages)
 need([{k:f[k] for k in ('page','start','end','literal','sha256')} for f in row['excluded_furniture']]==expected,'only exact repeated furniture/page numbers')

def calibrate(key,raw,fonts,pages,events,row,aliases):
 chars=list(raw);seen=set()
 for g in row['glyph_substitutions']:
  i=g['offset'];need(i not in seen and 0<=i<len(raw),'unique in-range glyph');seen.add(i)
  need(f'U+{ord(raw[i]):04X}'==g['input_codepoint'] and fonts[i]==g['input_font'],'actual extracted character/font')
  need(events.get(i)==g['pdf_event'] and events.get(i) is not None,'actual PDF font dictionary/byte/event')
  out=glyph_alias(key,raw[i],fonts[i],events[i],aliases)
  need(out==g['output'] and len(out)==1,'one declared visible glyph, no speculative substitution')
  pg=pages[g['page']-1];need(pg['start']<=i<pg['end'] and g['page_offset']==i-pg['start'],'physical glyph location')
  a,b=g['context_start'],g['context_end'];need(pg['start']<=a<=i<b<=pg['end'] and sha(raw[a:b].encode())==g['context_sha256'],'exact glyph context')
  need(not any(f['start']<=i<f['end'] for f in row['excluded_furniture']),'no glyph repair hidden in deleted furniture')
  chars[i]=out
 for i,c in enumerate(raw):
  bad=(unicodedata.category(c) in ('Cc','Co') and c not in '\n\r\t') or c=='\ufffd'
  need(not bad or i in seen,'all control/private glyphs classified')
  need(glyph_alias(key,c,fonts[i],events.get(i),aliases) is None or i in seen,'every authorized glyph occurrence repaired')
 return ''.join(chars)

def extract(pdf,key,row,aliases):
 need(sha(pdf.read_bytes())==row['pdf_sha256'],'bound PDF '+key)
 texts=[];fonts=[];pages=[];at=0
 for n,page in enumerate(pypdf.PdfReader(pdf).pages,1):
  chunks=[];local=[]
  def visitor(t,cm,tm,f,size):chunks.append(t);local.extend([str(f.get('/BaseFont',f.get('/Name',''))) if f else '']*len(t))
  t=page.extract_text(visitor_text=visitor) or '';need(t==''.join(chunks) and len(t)==len(local) and t,'complete nonempty extraction')
  pages.append(dict(page=n,start=at,end=at+len(t),sha256=sha(t.encode()),empty_extraction=False));at+=len(t)+1;texts.append(t);fonts.extend(local);fonts.append('')
 raw='\n'.join(texts);fonts=fonts[:-1];validate_selection(key,raw,row,pages)
 events={};audit=None
 if key in ('F015','L028','U_CE','CE1','CE_CODE'):events,audit=actual_event_alignment(pdf,raw,fonts,pages,type1_math_only=key in ('U_CE','CE1','CE_CODE'))
 calibrated=calibrate(key,raw,fonts,pages,events,row,aliases)
 return dict(raw_untrimmed=raw,raw_selected=selected(raw,row),calibrated_selected=selected(calibrated,row)),audit,dict(raw=raw,fonts=fonts,pages=pages,events=events)

def load_json(name):return json.loads((HERE/name).read_text())

def resolve(path,args,pub):
 r=pub['locations'][path];base={'public':args.public_root,'sources':args.sources_root,'packet':HERE}[r['root']]
 need(base is not None,'explicit source root required');return base/r['path']

def bound(row,args,pub):
 p=resolve(row['path'],args,pub);data=p.read_bytes();need(len(data)==row['bytes'] and sha(data)==row['sha256'],'bound whole input '+row['path']);return data

def validate_policy(p,b):
 need(p['originals']==b['original_manuscripts']==2 and set(p['source_roster'])=={'F015','L028'} and set(p['replacement_roster'])==KEYS-{'F015','L028'},'two originals and six complete replacement documents')
 need(len(p['complete_programs'])==4 and len(p['separate_drivers'])==3 and len(p['separate_formal_files'])==2,'complete program/driver/formal inventory')
 need(p['units']==UNITS and p['variants']==['raw_untrimmed','raw_selected','calibrated_selected'] and p['normalizations']==['NFC','NFKC'],'all thirty coordinates')
 need(p['factors_permitted'] is False and p['ratio'] is None and b['ratio'] is None,'no premature factor')
 need(all(b[k] is None and p[k] is None for k in ['retained_external_cost','graphics_cost','historical_software_cost']),'unknown external/graphic/software costs are null')
 need(b['new_source_credit']==b['new_question_credit']==b['new_formal_credit']==0 and not b['full_formalization_claim'],'no extra mathematical or full formal credit')
 need({k:len(v['rows']) for k,v in b['contracts'].items()}=={'F015':32,'L028':32},'exact inherited clauses, not original count')

def code_inclusion(tex,raw_pdf,code_rows,raw_files):
 inputs=re.findall(r'\\VerbatimInput(?:\[[^\]]*\])?\{([^}]+)\}',tex)
 need(len(inputs)==len(code_rows) and {Path(x).name for x in inputs}=={Path(r['path']).name for r in code_rows},'whole program inputs exactly once')
 need(not re.search(r'firstline|lastline|firstnumber|lastnumber',tex),'no line-range pruning')
 # Only this inclusion test ignores display-wrap hooks. They stay in measured PDF text.
 packed=lambda s:''.join(unicodedata.normalize('NFKC',s).split()).replace('↪','').replace('⌋','').replace(',→','')
 text=packed(raw_pdf)
 for r in code_rows:need(packed(raw_files[r['path']].decode()) in text,'entire literal program appears in appendix '+r['path'])
 return dict(complete_files=len(inputs),whole_file_inclusions=inputs,no_range_pruning=True,wrap_markers_counted_in_pdf_metrics=True)

def replay(args):
 protocol=load_json('protocol.json')
 if (HERE/'manifest.json').exists():
  for row in load_json('manifest.json')['exports']:
   rel=Path(row['path']);need(not rel.is_absolute() and '..' not in rel.parts,'safe frozen export')
   data=(HERE/rel).read_bytes();need(len(data)==row['bytes'] and sha(data)==row['sha256'],'frozen author export '+str(rel))
 for row in protocol['local_bindings']:
  data=(HERE/row['path']).read_bytes();need(len(data)==row['bytes'] and sha(data)==row['sha256'],'fixed local input '+row['path'])
 p=load_json('policy.json');pub=load_json('publication_binding.json');b=load_json('source_contract_boundary.json');validate_policy(p,b)
 need(pypdf.__version__==protocol['pypdf_version']=='6.13.0' and fontTools.__version__==protocol['fonttools_version']=='4.63.0','pinned parser versions')
 for row in pub['admissions'].values():
  data=(args.public_root/row['path']).read_bytes();need(len(data)==row['bytes'] and sha(data)==row['sha256'],'accepted scientific admission')
 accepted={row['path']:bound(row,args,pub) for row in p['accepted_scientific_bindings']}
 for key,ledger,scope in [('F015','topic_Matching_volume_v2/source_clause_map.json','topic_Matching_volume_v2/scope.json'),('L028','phase282_source_ledger.json','phase282_scope.json')]:
  m=json.loads(accepted[ledger]);q=json.loads(accepted[scope]);c=b['contracts'][key]
  need(c['rows']==m['rows'] and c['proof_spans']==m['proof_spans'] and c['scope']==q,'exact accepted scientific contract '+key)
 aliases=load_json('proposed_aliases.json')['aliases'];need(len(aliases)==52 and sum(x['occurrences'] for x in aliases)==660,'complete alias census')
 specs=load_json('source_input_spec.json')['sources']|load_json('replacement_input_spec.json')['ours'];need(set(specs)==KEYS,'all documents')
 allrows=p['source_roster']|p['replacement_roster'];documents={};audits={};private={}
 for key,row in specs.items():
  need(row['path']==allrows[key]['path'] and row['pdf_sha256']==allrows[key]['sha256'],'policy/spec same input')
  texts,audit,cache=extract(resolve(row['path'],args,pub),key,row,aliases);private[key]=dict(texts=texts,cache=cache)
  documents[key]=dict(pdf_sha256=row['pdf_sha256'],pages=row['pages'],furniture_cuts=len(row['excluded_furniture']),glyph_repairs=len(row['glyph_substitutions']),metrics={v:{n:metrics(t,n) for n in p['normalizations']} for v,t in texts.items()})
  if audit:audits[key]=audit
 need(audits==load_json('font_audit.json'),'fresh actual font dictionaries/glyph outlines and event alignment')
 raw_files={};raw_counts={}
 for category in ['complete_programs','separate_drivers','separate_formal_files']:
  raw_counts[category]={}
  for row in p[category]:
   data=bound(row,args,pub);raw_files[row['path']]=data
   raw_counts[category][row['path']]=dict(bytes=len(data),sha256=sha(data),topic=row['topic'],role=row['role'],metrics={n:metrics(data.decode(),n) for n in p['normalizations']})
 appendix={}
 for topic,doc,texkey in [('Matching','M_CODE','programs_tex'),('ChiralEnumeration','CE_CODE','chiral_programs_tex')]:
  tex=bound(pub['appendix_tex'][texkey],args,pub).decode();rows=[r for r in p['complete_programs'] if r['topic']==topic]
  appendix[topic]=code_inclusion(tex,private[doc]['texts']['raw_selected'],rows,raw_files)
 # The newly printed scripts are exact copies of the published complete originals.
 for row in p['complete_programs']:
  if row['topic']=='ChiralEnumeration':need((HERE/'programs'/Path(row['path']).name).read_bytes()==raw_files[row['path']],'unchanged appendix program copy')
 result=dict(status='AUTHOR_INPUT_REPLAY_PASS_PENDING_DISTINCT_REVIEW',original_manuscripts=2,pdf_documents=8,pdf_pages=68,pdf_metric_cells=240,raw_metric_cells=90,documents=documents,raw_files=raw_counts,appendices=appendix,ratio=None,scientific_programs_executed=False,full_formalization_claim=False,unknown_costs=dict(retained_external=None,historical_software=None,full_graphics=None,full_formalization=None))
 return result,audits,private

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh output');a.out.mkdir(parents=True)
 result,audits,_=replay(a)
 for file,data in [('counts.json',result),('font_audit.json',audits)]: (a.out/file).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 print('PASS: 2 originals; 8 PDFs/68 pages; 240 PDF and 90 whole-file metric cells; no factors.')
if __name__=='__main__':main()
