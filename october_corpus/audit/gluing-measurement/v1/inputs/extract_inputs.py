#!/usr/bin/env python3
"""Complete independent Gluing topic inputs; no factors."""
from pathlib import Path
import argparse,json,re,unicodedata
import pypdf,fontTools
from font_tools import need,sha,actual_event_alignment
from pdf_text import extract as literal_extract
from calibration import output
H=Path(__file__).resolve().parent
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
def load(n):return json.loads((H/n).read_text())
def bound(row,args):
 f={'public':args.public_root,'sources':args.sources_root,'packet':H}[row['root']]/row['path'];b=f.read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'bound whole input '+row['path']);return f,b

def metrics(s,form):
 s=unicodedata.normalize(form,s);c=' '.join(s.split());return dict(whitespace_tokens=len(c.split()),alphanumeric_units=len(re.findall(r'[^\W_]+',s)),characters_without_whitespace=sum(not x.isspace() for x in s),characters_with_collapsed_whitespace=len(c),utf8_bytes_with_collapsed_whitespace=len(c.encode()),collapsed_text_sha256=sha(c.encode()))

def alias(event,key,aliases):
 if event is None:return None
 rows=[x for x in aliases if x['document']==key and x['font_identity']==event['font_identity'] and x['encoded_byte']==event['encoded_byte'] and x['glyph_name']==event['glyph_name']];need(len(rows)<=1,'unique actual glyph class');return rows[0] if rows else None

def validate_glyphs(key,raw,fonts,pages,events,row,aliases):
 covered=set();edits=[]
 for g in row['glyph_substitutions']:
  a,b=g['start'],g['end'];need(0<=a<b<=len(raw) and not covered.intersection(range(a,b)),'one disjoint visible glyph span');covered.update(range(a,b))
  need(raw[a:b]==g['input'] and all(fonts[j]==g['input_font'] for j in range(a,b)),'complete literal decoded glyph')
  need([events.get(j) for j in range(a,b)]==g['pdf_events'] and events.get(a) is not None,'all original byte events')
  event=events[a];need(event['decoded_character_index']==0 and event['decoded_text']==g['input'],'one actual glyph, not a sequence of guessed symbols')
  need([events[j]['decoded_character_index'] for j in range(a,b)]==list(range(b-a)),'one glyph decoded across exact consecutive characters')
  r=alias(event,key,aliases);need(r is not None and g['output']==r['output'] and len(g['output'])==1,'one observed visible glyph substitute')
  pg=pages[g['page']-1];x,y=g['context_start'],g['context_end'];need(pg['start']<=x<=a<b<=y<=pg['end'] and sha(raw[x:y].encode())==g['context_sha256'] and g['page_offset']==a-pg['start'],'exact local context')
  need(not covered.intersection(row['extraction_metadata']['generated_newline_offsets']),'no generated newline reclassified')
  need(not any(max(a,f['start'])<min(b,f['end']) for f in row['excluded_furniture']),'no glyph lost in furniture')
  edits.append((a,b,g['output']))
 for i,c in enumerate(raw):
  need(not ((unicodedata.category(c) in ('Cc','Co') and c not in '\r\n\t') or c=='\ufffd') or i in covered,'all suspicious glyphs classified')
  need(alias(events.get(i),key,aliases) is None or i in covered,'all actual aliases included once')
 return edits

def transform(raw,row,edits=()):
 all_edits=sorted([(x['start'],x['end'],'\n') for x in row['excluded_furniture']]+list(edits));parts=[];at=0
 for a,b,value in all_edits:need(at<=a<b,'disjoint exact selection/calibration');parts.extend([raw[at:a],value]);at=b
 parts.append(raw[at:]);return ''.join(parts)

def furniture(key,raw,pages):
 cuts=[]
 for pg in pages:
  n=pg['page'];t=raw[pg['start']:pg['end']]
  if key=='L010' and n>=2:
   literal=f'{n} DIMITRI LEEMANS AND JESSICA MULPAS\n' if n%2==0 else f'GLUING METHODS FOR STRING C-GROUPS {n}\n';need(t.startswith(literal),'exact source running header');a=0;b=len(literal)
  else:
   m=re.search(r'(?:^|\n)'+str(n)+r'\s*\Z',t);need(m is not None,'isolated physical footer');a=m.start()+(t[m.start()]=='\n');b=len(t)
  a+=pg['start'];b+=pg['start'];cuts.append(dict(page=n,start=a,end=b,literal=raw[a:b],sha256=sha(raw[a:b].encode())))
 return cuts

def validate_selection(key,raw,row,pages,meta):
 need(row['page_bindings']==pages and row['pages']==len(pages),'all physical pages')
 need(row['extraction_sha256']==sha(raw.encode()) and row['included_spans']==[dict(start=0,end=len(raw),sha256=sha(raw.encode()))],'complete source/replacement')
 need(row['excluded_furniture']==furniture(key,raw,pages),'only repeated headers or isolated footers')
 need(row['extraction_metadata']==meta and not meta['returned_extraction_changed'],'literal returned extraction')

def validate_policy(p):
 need(p['source_id']=='L010' and p['original_manuscripts']==1 and p['source_rows']==23,'one source and exact recorded scope')
 need(p['topic']=='Gluing: supported orbits and synchronized trees' and p['source']['pages']==15,'fixed independent topic/source edition')
 need(set(p['replacements'])=={'U1','U2','A1','CODE'} and [p['replacements'][k]['pages'] for k in ['U1','U2','A1','CODE']]==[5,6,5,4],'both whole common papers/application/program appendix')
 need(p['whole_common_papers_charged'] and p['existing_B_common_is_not_a_prerequisite'] and p['cross_topic_discount'] is False,'full independent common theory charge')
 need(len(p['programs'])==3 and p['principal_required_programs']==0 and p['validation_programs']==3 and all(r['role']=='finite_validation' and not r['uniform_mathematical_premise'] for r in p['programs']),'three complete diagnostics, no finite premises')
 need(len(p['drivers'])==3 and len(p['formal'])==2 and p['partial_formal_declarations']==10 and not p['whole_source_formalized'],'driver and formal roles')
 need(p['all_declared_code_prepurchased_for_conditional_results'] and p['raw_and_printed_code_are_alternatives'],'complete program prepayment and alternatives')
 need(not p['factors_permitted'] and p['ratio'] is None and p['new_scientific_credit']==0,'no factors/credits')
 need(set(p['unknown_costs'])=={'full_graphics','historical_software','retained_external_proofs','full_formalization'} and all(v is None for v in p['unknown_costs'].values()),'all four unknown costs stay null')
 need(p['units']==UNITS and p['normalizations']==['NFC','NFKC'] and p['variants']==['raw_untrimmed','raw_selected','calibrated_selected'],'all thirty coordinates')
 need([p[x] for x in ['pdf_documents','pdf_pages','pdf_metric_cells','raw_files','raw_metric_cells']]==[5,35,150,8,80],'complete input counts')

def code_inclusion(tex,raw,programs,events,cuts):
 names=re.findall(r'\\VerbatimInput(?:\[[^\]]*\])?\{([^}]+)\}',tex);need(names==list(programs),'all three full program inputs in order');need(not re.search('firstline|lastline|firstnumber|lastnumber',tex),'no code pruning')
 # Only actual font events used by fvextra's wrap markers are removed for this
 # inclusion check. They remain present in every measured PDF coordinate.
 wrap={i for i,e in events.items() if e['glyph_name'] in ('arrowhookleft','arrowright','floorright') and any(x in e['font'] for x in ('CMMI','CMSY'))}
 furniture_positions={i for cut in cuts for i in range(cut['start'],cut['end'])}
 clean=''.join(c for i,c in enumerate(raw) if i not in wrap and i not in furniture_positions)
 pack=lambda s:''.join(unicodedata.normalize('NFKC',s).split())
 for name,code in programs.items():need(pack(code) in pack(clean),'whole printed code '+name)
 return dict(full_files=3,no_pruning=True,wrap_markers_retained_in_counts=True,actual_marker_characters_ignored_only_for_inclusion=len(wrap))

def replay(args):
 p=load('policy.json');validate_policy(p);spec=load('input_spec.json');need(set(spec)=={'L010','U1','U2','A1','CODE'},'five whole PDFs');proto=load('protocol.json');need(pypdf.__version__==proto['pypdf_version']=='6.13.0' and fontTools.__version__==proto['fonttools_version']=='4.63.0','pinned extraction libraries')
 for row in proto['local_bindings']:
  data=(H/row['path']).read_bytes();need(len(data)==row['bytes'] and sha(data)==row['sha256'],'bound local input '+row['path'])
 if (H/'manifest.json').exists():
  for row in load('manifest.json')['exports']:
   f=Path(row['path']);need(not f.is_absolute() and '..' not in f.parts,'safe exported path');data=(H/f).read_bytes();need(len(data)==row['bytes'] and sha(data)==row['sha256'],'frozen export '+str(f))
 scientific={r['path']:bound(r,args)[1] for r in p['scientific_bindings']};need({k:json.loads(v) for k,v in scientific.items() if k.endswith('.json')}==load('source_boundary.json'),'exact source and proof packet boundaries')
 aliases=load('glyph_aliases.json')['aliases'];docs={};audits={};cache={}
 for key,row in {'L010':p['source'],**p['replacements']}.items():
  need(all(spec[key][k]==v for k,v in row.items()),'policy/spec same input');pdf,_=bound(row,args);raw,fonts,pages,meta=literal_extract(pdf,False);need(raw=='\n'.join(x.extract_text() or '' for x in pypdf.PdfReader(pdf).pages),'raw unchanged from uninstrumented pypdf');validate_selection(key,raw,spec[key],pages,meta)
  events,audits[key]=actual_event_alignment(pdf,raw,fonts,pages,type1_math_only=key!='L010',generated_newline_offsets=set(meta['generated_newline_offsets']));edits=validate_glyphs(key,raw,fonts,pages,events,spec[key],aliases);texts=dict(raw_untrimmed=raw,raw_selected=transform(raw,spec[key]),calibrated_selected=transform(raw,spec[key],edits))
  docs[key]=dict(pdf_sha256=row['sha256'],pages=len(pages),furniture_cuts=len(spec[key]['excluded_furniture']),glyph_repairs=len(edits),metrics={v:{n:metrics(t,n) for n in p['normalizations']} for v,t in texts.items()});cache[key]=dict(raw=raw,fonts=fonts,pages=pages,meta=meta,events=events,texts=texts)
 need(audits==load('font_audit.json'),'all actual font dictionaries and byte events')
 expect=[dict(document=k,font=r['font'],font_identity=r['font_identity'],encoded_byte=r['encoded_byte'],glyph_name=r['glyph_name'],input=r['decoded_text'],output=output(r),output_name=unicodedata.name(output(r)),occurrences=r['occurrences'],glyph_evidence=r['glyph_evidence']) for k,a in audits.items() for r in a['encoded_glyph_classes'] if output(r) is not None];need(expect==aliases,'observed aliases only')
 raw_counts={};files={}
 for category in ['programs','drivers','formal']:
  raw_counts[category]={}
  for r in p[category]:
   _,data=bound(r,args);files[r['path']]=data;raw_counts[category][r['path']]=dict(bytes=len(data),sha256=sha(data),role=r['role'],metrics={n:metrics(data.decode(),n) for n in p['normalizations']})
 pr={r['printed_path']:files[r['path']].decode() for r in p['programs']}
 for r in p['programs']:need((H/r['printed_path']).read_bytes()==files[r['path']],'byte-identical printed program copy')
 included=code_inclusion(scientific['programs.tex'].decode(),cache['CODE']['raw'],pr,cache['CODE']['events'],spec['CODE']['excluded_furniture'])
 result=dict(status='AUTHOR_INPUTS_PENDING_DISTINCT_REVIEW',original_manuscripts=1,source_id='L010',topic=p['topic'],pdf_documents=5,pdf_pages=35,pdf_metric_cells=150,raw_metric_cells=80,documents=docs,raw_files=raw_counts,program_inclusion=included,ratio=None,new_scientific_credit=0,scientific_programs_executed=False,whole_source_formalized=False,unknown_costs=p['unknown_costs'])
 return result,audits,cache

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True);r,f,_=replay(a)
 for n,o in [('counts.json',r),('font_audit.json',f)]:(a.out/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
 print('PASS150 full-PDF and80 raw cells; no factors.')
