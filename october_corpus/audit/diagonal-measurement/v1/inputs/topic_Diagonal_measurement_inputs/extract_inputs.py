#!/usr/bin/env python3
"""Replay complete N007 input costs; glyph metadata never edits raw extraction."""
from pathlib import Path
import argparse,json,re,unicodedata
import pypdf,fontTools
from font_tools import need,sha,actual_event_alignment
from pdf_text import extract as literal_extract,BANNER
from calibration import output
HERE=Path(__file__).resolve().parent
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
KEYS={'N007','U','A1','CODE'}
def load(name):return json.loads((HERE/name).read_text())
def metrics(text,form):
 text=unicodedata.normalize(form,text);c=' '.join(text.split())
 return dict(whitespace_tokens=len(c.split()),alphanumeric_units=len(re.findall(r'[^\W_]+',text)),characters_without_whitespace=sum(not x.isspace() for x in text),characters_with_collapsed_whitespace=len(c),utf8_bytes_with_collapsed_whitespace=len(c.encode()),collapsed_text_sha256=sha(c.encode()))
def bound(row,args):
 root={'sources':args.sources_root,'public':args.public_root}[row['root']];path=root/row['path'];data=path.read_bytes()
 need(len(data)==row['bytes'] and sha(data)==row['sha256'],'exact whole input '+row['path']);return path,data

def furniture(key,raw,pages):
 out=[]
 for pg in pages:
  n=pg['page'];t=raw[pg['start']:pg['end']]
  if key=='N007':
   if n==1:
    a=t.rfind('\n1\n'+BANNER)+1;need(a>0,'isolated page number before retained banner');b=a+1
   else:
    literal=f'{n} CLAUDIO ALEXANDRE PIEDADE AND PHILIPPE TRANCHIDA\n' if n%2==0 else f'THEj-DIAGONALS TWISTING {n}\n';need(t.startswith(literal),'exact repeated source header');a=0;b=len(literal)
  else:
   m=re.search(r'(?:^|\n)'+str(n)+r'\s*\Z',t);need(m is not None,'isolated footer');a=m.start()+(t[m.start()]=='\n');b=len(t)
  a+=pg['start'];b+=pg['start'];out.append(dict(page=n,start=a,end=b,literal=raw[a:b],sha256=sha(raw[a:b].encode())))
 return out

def validate_selection(key,raw,row,pages,meta):
 need(row['pages']==len(pages) and row['page_bindings']==pages,'every physical page '+key)
 need(row['extraction_sha256']==sha(raw.encode()),'complete raw extraction '+key)
 need(row['included_spans']==[dict(start=0,end=len(raw),sha256=sha(raw.encode()))],'whole manuscript including references')
 need([{k:x[k] for k in ('page','start','end','literal','sha256')} for x in row['excluded_furniture']]==furniture(key,raw,pages),'only literal repeated furniture')
 need(meta==row['extraction_metadata'],'generated newline/Form metadata exact')
 need(meta['returned_extraction_changed'] is False,'raw extraction unchanged')
 if key=='N007':need(raw.count(BANNER)==1,'one retained version banner')

def selected(raw,row):
 parts=[];at=0
 for f in row['excluded_furniture']:parts.append(raw[at:f['start']]);at=f['end']
 parts.append(raw[at:]);return '\n'.join(parts)

def alias(event,aliases):
 if event is None:return None
 rows=[r for r in aliases if r['font_identity']==event['font_identity'] and r['encoded_byte']==event['encoded_byte'] and r['glyph_name']==event['glyph_name']]
 need(len(rows)<=1,'unique actual dictionary/encoding class');return rows[0]['output'] if rows else None

def calibrate(raw,fonts,pages,events,row,aliases):
 chars=list(raw);seen=set()
 for g in row['glyph_substitutions']:
  i=g['offset'];need(i not in seen and 0<=i<len(raw),'unique glyph offset');seen.add(i)
  need(g['input_codepoint']==f'U+{ord(raw[i]):04X}' and g['input_font']==fonts[i],'actual decoded font/character')
  need(events.get(i)==g['pdf_event'] and events.get(i) is not None,'actual literal PDF byte/event')
  need(alias(events[i],aliases)==g['output'] and len(g['output'])==1,'one visible primitive')
  pg=pages[g['page']-1];a,b=g['context_start'],g['context_end'];need(pg['start']<=a<=i<b<=pg['end'] and sha(raw[a:b].encode())==g['context_sha256'],'exact local glyph evidence')
  need(g['page_offset']==i-pg['start'],'physical page offset')
  need(i not in row['extraction_metadata']['generated_newline_offsets'],'actual glyph is not generated line break')
  need(not any(f['start']<=i<f['end'] for f in row['excluded_furniture']),'visible glyph not cut')
  chars[i]=g['output']
 for i,c in enumerate(raw):
  need(not ((unicodedata.category(c) in ('Cc','Co') and c not in '\n\r\t') or c=='\ufffd') or i in seen,'all suspect glyphs classified')
  need(alias(events.get(i),aliases) is None or i in seen,'every actual visible glyph alias repaired')
 return ''.join(chars)

def source_events(pdf,raw,fonts,pages,meta):
 events,audit=actual_event_alignment(pdf,raw,fonts,pages,type1_math_only=True,generated_newline_offsets=set(meta['generated_newline_offsets']))
 skipped=audit['unchanged_type0_dictionaries'];need(len(skipped)==1 and skipped[0]['font']=='/HQMHGW+NimbusRoman-Regular','only exact Unicode version-banner font')
 banner=''.join(c for c,f in zip(raw,fonts) if f=='/HQMHGW+NimbusRoman-Regular');need(banner==BANNER,'Type0 exception is only once-retained version banner')
 audit['source_unicode_banner']=dict(literal=banner,retained_in_every_coordinate=True,scope='Only Type0 version stamp; all authored body Type1 glyphs aligned. Duplicate Form visitor callback is not an extra rendered text event.')
 return events,audit

def validate_policy(p):
 need(p['original_manuscripts']==1 and p['source_id']=='N007' and p['source_rows']==32 and p['proof_spans']==13,'one original and exact accepted clause boundary')
 need(p['required_finite_programs']==0 and p['validation_programs']==1 and len(p['programs'])==1 and len(p['drivers'])==2 and len(p['formal'])==1,'complete program inventory')
 need(p['units']==UNITS and p['variants']==['raw_untrimmed','raw_selected','calibrated_selected'] and p['normalizations']==['NFC','NFKC'],'all thirty coordinates')
 need(not p['factors_permitted'] and p['ratio'] is None,'input stage has no factor')
 need(p['N006_whole_original_credit']==p['new_source_credit']==p['new_question_credit']==0 and not p['full_formalization_claim'],'scope and no credit inflation')
 need(all(p[k] is None for k in ('retained_external_cost','graphics_cost','historical_software_cost')),'unknown costs remain null')

def code_inclusion(tex,text,code):
 names=re.findall(r'\\VerbatimInput(?:\[[^\]]*\])?\{([^}]+)\}',tex);need(names==['programs/diagonal_models.g'],'one full code input')
 need(not re.search('firstline|lastline|firstnumber|lastnumber',tex),'no line pruning')
 pack=lambda x:''.join(unicodedata.normalize('NFKC',x).split()).replace('↪','').replace('⌋','')
 need(pack(code) in pack(text),'complete literal program included')
 return dict(complete_files=1,required_finite_premises=0,validation_files=1,no_range_pruning=True,display_wrap_markers_counted=True)

def replay(args):
 p=load('policy.json');validate_policy(p);spec=load('input_spec.json');need(set(spec)==KEYS,'four complete PDFs')
 protocol=load('protocol.json')
 need(pypdf.__version__==protocol['pypdf_version']=='6.13.0' and fontTools.__version__==protocol['fonttools_version']=='4.63.0','pinned extraction libraries')
 for row in protocol['local_bindings']:
  data=(HERE/row['path']).read_bytes();need(len(data)==row['bytes'] and sha(data)==row['sha256'],'bound local extraction input '+row['path'])
 if (HERE/'manifest.json').exists():
  for row in load('manifest.json')['exports']:
   r=Path(row['path']);need(not r.is_absolute() and '..' not in r.parts,'safe export path');data=(HERE/r).read_bytes();need(len(data)==row['bytes'] and sha(data)==row['sha256'],'frozen export '+str(r))
 scientific={r['path']:bound(r,args)[1] for r in p['scientific_bindings']}
 scope=load('source_boundary.json')
 for name in ['contract.json','source_clause_map.json','formal/scope.json']:
  need(scope[name]==json.loads(scientific['papers/topic-diagonal/v1/'+name]),'exact unchanged scientific scope '+name)
 need(len(scope['source_clause_map.json']['rows'])==32 and len(scope['source_clause_map.json']['proof_spans'])==13 and scope['formal/scope.json']['declarations']==8,'accepted clause and partial Lean scopes')
 aliases=load('glyph_aliases.json')['aliases'];need(len(aliases)==17 and sum(x['occurrences'] for x in aliases)==237,'complete actual glyph alias census')
 documents={};audits={};cache={}
 for key,row in {'N007':p['source'],**p['replacements']}.items():
  need(all(spec[key][k]==v for k,v in row.items()),'policy/spec same PDF')
  pdf,_=bound(row,args);raw,fonts,pages,meta=literal_extract(pdf,key=='N007')
  need(raw=='\n'.join(x.extract_text() or '' for x in pypdf.PdfReader(pdf).pages),'instrumented extraction equals independent uninstrumented pypdf result')
  validate_selection(key,raw,spec[key],pages,meta);events={}
  if key=='N007':events,audits[key]=source_events(pdf,raw,fonts,pages,meta)
  calibrated=calibrate(raw,fonts,pages,events,spec[key],aliases)
  texts=dict(raw_untrimmed=raw,raw_selected=selected(raw,spec[key]),calibrated_selected=selected(calibrated,spec[key]))
  documents[key]=dict(pdf_sha256=row['sha256'],pages=row['pages'],furniture_cuts=len(spec[key]['excluded_furniture']),glyph_repairs=len(spec[key]['glyph_substitutions']),metrics={v:{n:metrics(t,n) for n in p['normalizations']} for v,t in texts.items()})
  cache[key]=dict(raw=raw,fonts=fonts,pages=pages,meta=meta,events=events,texts=texts)
 need(audits==load('font_audit.json'),'fresh complete actual font audit')
 expected_aliases=[dict(font=r['font'],font_identity=r['font_identity'],encoded_byte=r['encoded_byte'],glyph_name=r['glyph_name'],input=r['decoded_text'],output=output(r),output_name=unicodedata.name(output(r)),occurrences=r['occurrences'],glyph_evidence=r['glyph_evidence']) for r in audits['N007']['encoded_glyph_classes'] if output(r) is not None]
 need(aliases==expected_aliases,'complete calibration follows actual visible classes')
 raw_counts={};raw_files={}
 for category in ['programs','drivers','formal']:
  raw_counts[category]={}
  for row in p[category]:
   _,data=bound(row,args);raw_files[row['path']]=data
   raw_counts[category][row['path']]=dict(bytes=len(data),sha256=sha(data),role=row['role'],metrics={n:metrics(data.decode(),n) for n in p['normalizations']})
 appendix=code_inclusion(scientific['papers/topic-diagonal/v1/programs.tex'].decode(),cache['CODE']['texts']['raw_selected'],raw_files[p['programs'][0]['path']].decode())
 result=dict(status='AUTHOR_INPUT_REPLAY_PASS_PENDING_DISTINCT_REVIEW',original_manuscripts=1,source_id='N007',pdf_documents=4,pdf_pages=24,pdf_metric_cells=120,raw_metric_cells=40,documents=documents,raw_files=raw_counts,appendix=appendix,ratio=None,scientific_programs_executed=False,full_formalization_claim=False,unknown_costs=dict(retained_external=None,historical_software=None,full_graphics=None,full_formalization=None))
 return result,audits,cache

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();need(not args.out.exists(),'fresh output');args.out.mkdir(parents=True)
 result,audits,_=replay(args)
 for name,obj in [('counts.json',result),('font_audit.json',audits)]:(args.out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 print('PASS: 1 original, 4 complete PDFs/24 pages, 120 PDF and 40 raw metric cells; no factors.')
if __name__=='__main__':main()
