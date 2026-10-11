#!/usr/bin/env python3
"""Replay complete N007/N006 input costs; glyph metadata never edits raw extraction."""
from pathlib import Path
import argparse,json,re,unicodedata
import pypdf,fontTools
from font_tools import need,sha,actual_event_alignment
from pdf_text import extract as literal_extract,BANNER,BANNERS
from calibration import aliases_from
HERE=Path(__file__).resolve().parent
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
KEYS={'N007','N006','U','A1','A2','A2nine','A2HN','CODEold'}
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
  elif key=='N006':
   if n==1:
    a=t.rfind('\n1\n'+BANNERS[key])+1;need(a>0,'source page number before retained banner');b=a+1
   else:
    literal=f'{n}\n';need(t.startswith(literal),'exact leading source page number');a=0;b=len(literal)
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
 if key in BANNERS:need(raw.count(BANNERS[key])==1,'one retained version banner')

def selected(raw,row):
 parts=[];at=0
 for f in row['excluded_furniture']:parts.append(raw[at:f['start']]);at=f['end']
 parts.append(raw[at:]);return '\n'.join(parts)

def alias(event,aliases,key):
 if event is None:return None
 rows=[r for r in aliases if r['source']==key and r['font_identity']==event['font_identity'] and r['encoded_byte']==event['encoded_byte'] and r['glyph_name']==event['glyph_name']]
 need(len(rows)<=1,'unique actual dictionary/encoding class');return rows[0] if rows else None

def calibrate(raw,fonts,pages,events,row,aliases,key):
 chars=list(raw);seen=set()
 for g in row['glyph_substitutions']:
  i=g['offset'];need(i not in seen and 0<=i<len(raw),'unique glyph offset');seen.add(i)
  need(g['input_codepoint']==f'U+{ord(raw[i]):04X}' and g['input_font']==fonts[i],'actual decoded font/character')
  need(events.get(i)==g['pdf_event'] and events.get(i) is not None,'actual literal PDF byte/event')
  a=alias(events[i],aliases,key);need(a is not None and a['output']==g['output'] and a['kind']==g['kind'] and len(g['output'])==1,'one bound symbol or proposed graphical primitive')
  pg=pages[g['page']-1];a,b=g['context_start'],g['context_end'];need(pg['start']<=a<=i<b<=pg['end'] and sha(raw[a:b].encode())==g['context_sha256'],'exact local glyph evidence')
  need(g['page_offset']==i-pg['start'],'physical page offset')
  need(i not in row['extraction_metadata']['generated_newline_offsets'],'actual glyph is not generated line break')
  need(not any(f['start']<=i<f['end'] for f in row['excluded_furniture']),'visible glyph not cut')
  chars[i]=g['output']
 for i,c in enumerate(raw):
  need(not ((unicodedata.category(c) in ('Cc','Co') and c not in '\n\r\t') or c=='\ufffd') or i in seen,'all suspect glyphs classified')
  need(alias(events.get(i),aliases,key) is None or i in seen,'every actual visible glyph alias repaired')
 return ''.join(chars)

def source_events(pdf,raw,fonts,pages,meta,key):
 events,audit=actual_event_alignment(pdf,raw,fonts,pages,type1_math_only=True,generated_newline_offsets=set(meta['generated_newline_offsets']))
 skipped=audit['unchanged_type0_dictionaries']
 if key=='N007':
  need(len(skipped)==1,'only N007 version-banner Type0 font')
  fname=skipped[0]['font'];banner=''.join(c for c,f in zip(raw,fonts) if f==fname);need(banner==BANNERS[key],'only exact once-retained version banner outside Type1 outline audit')
  audit['source_unicode_banner']=dict(literal=banner,retained_in_every_coordinate=True,scope='Only Type0 version stamp; all authored body Type1 glyphs aligned. Duplicate Form visitor callback is not an extra rendered text event.')
 else:
  need(not skipped,'all N006 source text fonts are audited Type1')
  audit['source_unicode_banner']=dict(literal=BANNERS[key],retained_in_every_coordinate=True,scope='Banner has actual audited Type1 events, with no skipped font or duplicate Form callback.')
 return events,audit

def validate_policy(p):
 need(p['original_manuscripts']==2 and p['source_rows']==dict(N007=32,N006=27),'two originals and exact accepted clause boundaries')
 need(set(p['sources'])=={'N007','N006'} and set(p['replacements'])==KEYS-set(p['sources']),'whole source/application boundary')
 need({k:v['pages'] for k,v in p['replacements'].items()}==dict(U=8,A1=5,A2=8,A2nine=5,A2HN=4,CODEold=2),'whole enlarged common paper and every companion')
 need(len(p['programs'])==19 and len(p['required_drivers'])==2 and len(p['drivers'])==4 and len(p['formal'])==3,'complete software inventory')
 need(len({x['path'] for cat in ['programs','required_drivers','drivers','formal'] for x in p[cat]})==28,'distinct whole files')
 need(sum(x['role']=='validation' for x in p['programs'])==p['validation_GAP_files']==3,'three complete validations')
 need(sum(x['role']=='required_finite_proof_or_complete_witness' for x in p['programs'])==p['required_GAP_or_witness_files']==16,'sixteen complete finite proof/witness files')
 need(p['required_decoding_drivers']==2 and p['operational_drivers']==4 and p['unique_formal_files']==3 and p['partial_formal_declarations']==17,'honest driver/formal scope')
 need(p['units']==UNITS and p['variants']==['raw_untrimmed','raw_selected','calibrated_selected'] and p['normalizations']==['NFC','NFKC'],'all thirty coordinates')
 need(not p['factors_permitted'] and p['ratio'] is None,'input stage has no factor')
 need(p['new_source_credit']==p['new_question_credit']==0,'no credit inflation')
 need(all(v is None for v in p['unknown_costs'].values()),'external/graphic costs unknown, not zero')
 need(p['source_exceptions_outside_this_edition']==['Fi22','Fi24prime'] and p['later_exception_certificates_not_added_here'],'exact published recovery boundary')
 need(p['diagram_proxy_policy']['status']=='PROPOSED_PENDING_DISTINCT_REVIEW' and not p['diagram_proxy_policy']['literal_unicode_extraction'] and p['diagram_proxy_policy']['geometry_cost'] is None,'explicit proposal and unknown geometry')
 need(p['diagram_proxy_policy']['text_only_alternative'] and p['diagram_proxy_policy']['raw_unaltered'],'both alternative coordinates retained')

def code_inclusion(tex,text,code):
 names=re.findall(r'\\VerbatimInput(?:\[[^\]]*\])?\{([^}]+)\}',tex);need(names==['programs/diagonal_models.g'],'one full old code input')
 need(not re.search('firstline|lastline|firstnumber|lastnumber',tex),'no line pruning')
 pack=lambda x:''.join(unicodedata.normalize('NFKC',x).split()).replace('↪','').replace('⌋','')
 need(pack(code) in pack(text),'complete literal program included')
 return dict(complete_files=1,required_finite_premises=0,validation_files=1,no_range_pruning=True,display_wrap_markers_counted=True,alternative_to='papers/topic-diagonal/v1/programs/diagonal_models.g',added_to_same_raw_file=False)

def validate_external(e):
 required=[x for x in e['inputs'] if x['stage_role'].startswith('required')]
 need(len(required)==e['required_representation_files']==4 and sum(x['bytes'] for x in required)==e['required_representation_bytes']==21960689,'complete exact external representations')
 installed=e['installed_files_once_by_identical_hash']
 need(len(installed)==16 and len({x['sha256'] for x in installed})==16 and sum(x['bytes'] for x in installed)==e['installed_file_bytes_once']==2516249,'complete inherited installed data/algorithm boundary')
 need(e['unknown_proof_cost'] is None and not e['compact_word_discount'] and not e['cross_topic_overlap_discount'],'outside proof cost unknown, no word or cross-topic discount')
 return dict(required_representation_files=4,required_representation_bytes=21960689,listed_installed_files=16,listed_installed_bytes=2516249,classification_proof_cost=None,measurement_rechecks_actual_data=False,scope='Exact retained ledgers bound; optional external byte-only audit is separate. Neither GAP algorithms nor scientific assertions rerun for measurement.')

def external_ledger_identity(e,scientific):
 nine=json.loads(scientific['papers/topic-diagonal/v2/papers/sporadic/retained_inputs.json'])
 hn=json.loads(scientific['papers/topic-diagonal/v2/papers/harada-norton/retained_inputs.json'])
 expected=nine['external_atlas_inputs']+hn['binary_files']
 need(len(expected)==len(e['inputs']),'all inherited external representation entries')
 for old in expected:
  matches=[x for x in e['inputs'] if x['filename']==old['filename']]
  need(len(matches)==1 and all(matches[0][k]==v for k,v in old.items()),'literal inherited representation pin '+old['filename'])
 expected_files=nine['files']+hn['installed_catalogue_inputs']
 need({x['sha256'] for x in expected_files}=={x['sha256'] for x in e['installed_files_once_by_identical_hash']},'exact catalogue/algorithm hash union')
 for old in expected_files:
  current=next(x for x in e['installed_files_once_by_identical_hash'] if x['sha256']==old['sha256'])
  need(current['bytes']==old['bytes'],'exact full catalogue/algorithm bytes')

def replay(args):
 p=load('policy.json');validate_policy(p);spec=load('input_spec.json');need(set(spec)==KEYS,'eight complete PDFs')
 protocol=load('protocol.json')
 need(pypdf.__version__==protocol['pypdf_version']=='6.13.0' and fontTools.__version__==protocol['fonttools_version']=='4.63.0','pinned extraction libraries')
 for row in protocol['local_bindings']:
  data=(HERE/row['path']).read_bytes();need(len(data)==row['bytes'] and sha(data)==row['sha256'],'bound local extraction input '+row['path'])
 if (HERE/'manifest.json').exists():
  for row in load('manifest.json')['exports']:
   r=Path(row['path']);need(not r.is_absolute() and '..' not in r.parts,'safe export path');data=(HERE/r).read_bytes();need(len(data)==row['bytes'] and sha(data)==row['sha256'],'frozen export '+str(r))
 scientific={r['path']:bound(r,args)[1] for r in p['scientific_bindings']}
 scope=load('source_boundary.json');external_ledger_identity(load('external_data.json'),scientific)
 for key,name in [('contract','contract.json'),('source_clause_map','source_clause_map.json')]:need(scope['N007'][key]==json.loads(scientific['papers/topic-diagonal/v1/'+name]),'exact prior source clauses')
 need(len(scope['N007']['source_clause_map']['rows'])==32,'all N007 source rows')
 n6=json.loads(scientific['audit/topic-diagonal/v2/source_contract.json'])
 need(n6==scope['N006']['contract'],'exact N006 corrections and exclusions')
 aliases=load('glyph_aliases.json')['aliases'];need(aliases==aliases_from(load('font_audit.json')),'complete exact glyph mapping and reasons')
 documents={};audits={};cache={};alternatives={}
 for key,row in {**p['sources'],**p['replacements']}.items():
  need(all(spec[key][k]==v for k,v in row.items()),'policy/spec same PDF')
  pdf,_=bound(row,args);raw,fonts,pages,meta=literal_extract(pdf,key if key in p['sources'] else False)
  need(raw=='\n'.join(x.extract_text() or '' for x in pypdf.PdfReader(pdf).pages),'instrumented extraction equals uninstrumented pypdf')
  validate_selection(key,raw,spec[key],pages,meta);events={}
  if key in p['sources']:events,audits[key]=source_events(pdf,raw,fonts,pages,meta,key)
  calibrated=calibrate(raw,fonts,pages,events,spec[key],aliases,key)
  texts=dict(raw_untrimmed=raw,raw_selected=selected(raw,spec[key]),calibrated_selected=selected(calibrated,spec[key]))
  proxy=[g for g in spec[key]['glyph_substitutions'] if g['kind']=='graphical_proxy'];no_proxy=list(calibrated)
  for g in proxy:no_proxy[g['offset']]=' '
  text_only=selected(''.join(no_proxy),spec[key])
  alternatives[key]=dict(proxy_events_removed=len(proxy),rule='Each identified graphical-proxy event replaced by a separator; ordinary text/formulas/labels retained. Full geometry remains unknown, not zero.',metrics={n:metrics(text_only,n) for n in p['normalizations']})
  documents[key]=dict(pdf_sha256=row['sha256'],pages=row['pages'],furniture_cuts=len(spec[key]['excluded_furniture']),glyph_repairs=len(spec[key]['glyph_substitutions']),graphical_proxy_events=len(proxy),metrics={v:{n:metrics(t,n) for n in p['normalizations']} for v,t in texts.items()})
  cache[key]=dict(raw=raw,fonts=fonts,pages=pages,meta=meta,events=events,texts=texts)
 need(audits==load('font_audit.json'),'fresh actual dictionary/encoding audit')
 need(aliases==aliases_from(audits),'fresh calibration follows actual classes')
 raw_counts={};raw_files={}
 for category in ['programs','required_drivers','drivers','formal']:
  raw_counts[category]={}
  for row in p[category]:
   _,data=bound(row,args);raw_files[row['path']]=data
   raw_counts[category][row['path']]=dict(bytes=len(data),sha256=sha(data),role=row['role'],metrics={n:metrics(data.decode(),n) for n in p['normalizations']})
 old=next(x for x in p['programs'] if x['application']=='N007')
 appendix=code_inclusion(scientific['papers/topic-diagonal/v1/programs.tex'].decode(),cache['CODEold']['texts']['raw_selected'],raw_files[old['path']].decode())
 previous=load('prior_count_reference.json')
 for k,oldkey in [('N007','N007'),('A1','A1'),('CODEold','CODE')]:need(documents[k]['metrics']==previous['documents'][oldkey]['metrics'],'unchanged prior document metrics '+k)
 result=dict(status='AUTHOR_INPUT_REPLAY_PASS_PENDING_DISTINCT_REVIEW',original_manuscripts=2,pdf_documents=8,pdf_pages=66,pdf_metric_cells=240,raw_metric_cells=280,documents=documents,text_only_sensitivity=alternatives,text_only_sensitivity_cells=80,raw_files=raw_counts,old_appendix=appendix,external=validate_external(load('external_data.json')),ratio=None,scientific_programs_executed=False,full_formalization_claim=False,unknown_costs=p['unknown_costs'])
 return result,audits,cache

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();need(not args.out.exists() and not args.out.is_symlink(),'fresh output');args.out.mkdir(parents=True)
 result,audits,_=replay(args)
 for name,obj in [('counts.json',result),('font_audit.json',audits)]:(args.out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 print('PASS: 2 originals, 8 complete PDFs/66 pages, 240 PDF and 280 raw metric cells; no factors.')
if __name__=='__main__':main()
