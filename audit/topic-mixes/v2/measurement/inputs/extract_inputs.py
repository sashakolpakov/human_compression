#!/usr/bin/env python3
"""L016 inputs for enlarged Mixes; no factors."""
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
  if key=='L016' and n>1:
   line=t.split('\n',1)[0]
   expected=(str(n)+' DIMITRI LEEMANS AND MICAEL TOLEDO') if n%2==0 else ('F AITHFUL AND THIN NON-POLYTOPAL MANIPLEXES '+str(n))
   need(line==expected,'exact running source header');a=pg['start'];b=a+len(line)+1
  else:
   m=re.search(r'(?:^|\n)'+str(n)+r'\s*\Z',t);need(m is not None,'isolated physical footer')
   a=pg['start']+m.start()+(t[m.start()]=='\n');b=pg['end']
  cuts.append(dict(page=n,start=a,end=b,literal=raw[a:b],sha256=sha(raw[a:b].encode())))
 return cuts

def validate_selection(key,raw,row,pages,meta):
 need(row['page_bindings']==pages and row['pages']==len(pages),'all physical pages')
 need(row['extraction_sha256']==sha(raw.encode()) and row['included_spans']==[dict(start=0,end=len(raw),sha256=sha(raw.encode()))],'complete source/replacement')
 need(row['excluded_furniture']==furniture(key,raw,pages),'only isolated physical footers')
 need(row['extraction_metadata']==meta and not meta['returned_extraction_changed'],'literal returned extraction')

def validate_policy(p):
 need(p['source_id']=='L016' and p['original_manuscripts']==1 and p['source_rows']==19,'one newly measured source with19 dispositions')
 need(p['source']['pages']==12 and p['topic_originals']==['F005','L016'] and p['new_originals']==['L016'],'complete enlarged topic')
 need(p['topic_assignment']=='Enlarged existing Mixes: F005 and L016' and not p['registered_new_topic'],'no new singleton')
 need(set(p['replacements'])=={'U1','A3','REQ','VAL'} and [p['replacements'][k]['pages']for k in ['U1','A3','REQ','VAL']]==[4,6,2,3],'whole added documents')
 w=p['whole_topic_boundary'];need(w['common_documents']==['retained:U','U1'] and w['applications']=={'MX1':['retained:A1','retained:A2'],'MX2':['A3']},'whole common and applications')
 need(w['whole_U5_paid_once'] and w['whole_new_U4_paid_once'] and w['all_three_application_papers_paid'],'no free shared theory')
 need(w['source_documents']==['retained:F005','L016'] and w['required_raw_programs']==['topic_Mix_F005_recovery/check_coprime.g','topic_Mix_L016_recovery/base_certificate.g'] and w['required_printed_alternative']=='REQ','exact source and required-program closure')
 need(p['whole_old_common_required'] and p['whole_new_common_required'] and p['no_free_cross_topic_import'] and not p['overlap_discount'],'full dependence closure')
 need([r['role']for r in p['programs']]==['required_finite_certificate','optional_validation','optional_validation'] and [r['mathematical_premise']for r in p['programs']]==[True,False,False],'actual program roles')
 need(p['required_printed_reused_program']['path']=='topic_Mix_F005_recovery/check_coprime.g','whole earlier required certificate')
 need(len(p['drivers'])==2 and len(p['formal'])==1 and p['partial_lean_declarations']==6 and not p['end_to_end_formalization'],'partial formal scope and drivers')
 need('symmetrically' in p['optional_validation_comparison'] and p['printed_raw_alternatives_never_additive'],'symmetric validation/alternative code')
 need(not p['source_executable_listing'] and p['source_historical_software_cost'] is None and p['unknown_costs']==dict(retained_external_proofs=None,full_graphics=None,full_formalization=None,runtime=None),'unknown costs, not zero or absent')
 need(p['units']==UNITS and p['normalizations']==['NFC','NFKC'] and p['variants']==['raw_untrimmed','raw_selected','calibrated_selected'],'all30 coordinates')
 need(p['primary'].startswith('raw_untrimmed/NFC/characters_without_whitespace') and p['whole_documents'],'complete raw primary')
 need([p[x]for x in ['pdf_documents','pdf_pages','pdf_metric_cells','raw_files','raw_metric_cells']]==[5,27,150,6,60],'new input counts')
 need([p[x]for x in ['retained_pdf_documents','retained_pdf_metric_cells','retained_raw_files','retained_raw_metric_cells']]==[6,180,7,70],'exact retained count boundary')
 need(not p['factors_permitted'] and p['ratio'] is None and p['new_scientific_credit']==0,'no factors or credits')

def validate_retained(old,accepted):
 need(old==accepted,'every accepted F005 cell and boundary retained without reextraction')
 need(old['pdf_metric_cells']==180 and old['raw_metric_cells']==70 and set(old['documents'])=={'F005','U','A1','A2','CODE1','CODE2'},'accepted complete F005 counts')

def validate_science(scientific):
 s=scientific['topic_Mix_L016_recovery/scope.json'];r=scientific['topic_Mix_L016_root_adoption/review.json']
 need(len(s['source_rows'])==19 and len(s['proof_contexts'])==20,'all L016 dispositions and proof contexts')
 b=next(x for x in s['source_rows']if x['id']=='B3')
 need(b['disposition']=='disproved_literal_auxiliary_with_repair','literal thin-base qualification')
 need(r['status']=='ROOT_ACCEPTED_L016_CORRECTED_PRINCIPAL_CONTRACT' and r['source_dispositions']==19 and not r['whole_source_formalized'],'accepted corrected scope, partial formalization')
 need({x['id']for x in r['excluded_ancillary_or_unanswered']}=={'A1','Q1','A3','B5'},'visible ancillary and unanswered exclusions')
 need(r['source_historical_software_cost'] is None and r['full_retained_external_proof_cost'] is None,'retained source costs unknown')

def validate_source_code_boundary(b):
 need(set(b['sources'])=={'F005','L016'} and b['sources']['F005']['physical_pages']==list(range(1,22)) and b['sources']['L016']['physical_pages']==list(range(1,13)),'both full source executable boundaries')
 need(all(x['embedded_executable_listings']==[] and x['whole_source_text_retained'] and x['source_software_cost'] is None for x in b['sources'].values()),'no source-only executable charge or invented zero software cost')
 need(b['written_algorithms_and_proof_prose_retained_on_both_sides'] and not b['source_only_executable_charge'] and not b['unmatched_software_comparison_resolved'] and not b['factors_evaluated'],'written/code symmetry and unresolved historical software')

def code_inclusion(tex,raw,programs,events,cuts):
 names=re.findall(r'\\VerbatimInput(?:\[[^\]]*\])?\{([^}]+)\}',tex)
 need(names==list(programs),'all complete program inputs in order');need(not re.search('firstline|lastline|firstnumber|lastnumber',tex),'no code pruning')
 furniture_positions={i for cut in cuts for i in range(cut['start'],cut['end'])}
 clean=''.join(c for i,c in enumerate(raw) if i not in furniture_positions)
 pack=lambda s:''.join(unicodedata.normalize('NFKC',s).split())
 for name,code in programs.items():need(pack(code) in pack(clean),'whole printed code '+name)
 return dict(full_files=len(programs),no_pruning=True,ignored_wrap_marker_characters=0)

def replay(args):
 p=load('policy.json');validate_policy(p);spec=load('input_spec.json');need(set(spec)=={'L016','U1','A3','REQ','VAL'},'five complete new PDFs')
 proto=load('protocol.json');need(pypdf.__version__==proto['pypdf_version']=='6.13.0' and fontTools.__version__==proto['fonttools_version']=='4.63.0','pinned libraries')
 for row in proto['local_bindings']:
  data=(H/row['path']).read_bytes();need(len(data)==row['bytes'] and sha(data)==row['sha256'],'bound input '+row['path'])
 if (H/'manifest.json').exists():
  for row in load('manifest.json')['exports']:
   f=Path(row['path']);need(not f.is_absolute() and '..'not in f.parts,'safe export');data=(H/f).read_bytes();need(len(data)==row['bytes'] and sha(data)==row['sha256'],'frozen export '+str(f))
 scientific={r['path']:bound(r,args)[1]for r in p['scientific_bindings']}
 science={k:json.loads(v)for k,v in scientific.items()if k.endswith('.json')}
 need(science==load('source_boundary.json'),'exact source/review boundaries');validate_science(science)
 reused={k:json.loads(bound(r,args)[1])for k,r in p['reused_accepted_inputs'].items()if isinstance(r,dict)}
 old=reused['counts'];validate_retained(old,reused['counts'])
 for k,row in {'F005':reused['policy']['source'],**reused['policy']['replacements']}.items():
  _,data=bound(row,args);need(old['documents'][k]['pdf_sha256']==sha(data),'unchanged retained PDF '+k)
 for cat in ['programs','drivers','formal']:
  for row in reused['policy'][cat]:
   _,data=bound(row,args);need(old['raw_files'][cat][row['path']]['sha256']==sha(data),'unchanged retained raw input')
 aliases=load('glyph_aliases.json')['aliases'];docs={};audits={};cache={}
 for key,row in {'L016':p['source'],**p['replacements']}.items():
  need(all(spec[key][k]==v for k,v in row.items()),'policy/spec match');pdf,_=bound(row,args)
  raw,fonts,pages,meta=literal_extract(pdf,False);need(raw=='\n'.join(x.extract_text()or''for x in pypdf.PdfReader(pdf).pages),'literal uninstrumented extraction')
  validate_selection(key,raw,spec[key],pages,meta)
  events,audits[key]=actual_event_alignment(pdf,raw,fonts,pages,type1_math_only=key!='L016',generated_newline_offsets=set(meta['generated_newline_offsets']))
  edits=validate_glyphs(key,raw,fonts,pages,events,spec[key],aliases)
  texts=dict(raw_untrimmed=raw,raw_selected=transform(raw,spec[key]),calibrated_selected=transform(raw,spec[key],edits))
  docs[key]=dict(pdf_sha256=row['sha256'],pages=len(pages),furniture_cuts=len(spec[key]['excluded_furniture']),glyph_repairs=len(edits),metrics={v:{n:metrics(t,n)for n in p['normalizations']}for v,t in texts.items()})
  cache[key]=dict(raw=raw,fonts=fonts,pages=pages,meta=meta,events=events,texts=texts)
 need(audits==load('font_audit.json'),'actual font dictionaries/classes')
 expect=[dict(document=k,font=r['font'],font_identity=r['font_identity'],encoded_byte=r['encoded_byte'],glyph_name=r['glyph_name'],input=r['decoded_text'],output=output(r),output_name=unicodedata.name(output(r)),occurrences=r['occurrences'],glyph_evidence=r['glyph_evidence'])for k,a in audits.items()for r in a['encoded_glyph_classes']if output(r)is not None]
 need(expect==aliases,'exact observed aliases')
 raws={};files={}
 for cat in ['programs','drivers','formal']:
  raws[cat]={}
  for r in p[cat]:
   _,b=bound(r,args);files[r['path']]=b;raws[cat][r['path']]=dict(bytes=len(b),sha256=sha(b),role=r['role'],metrics={n:metrics(b.decode(),n)for n in p['normalizations']})
 pr=p['required_printed_reused_program'];_,b=bound(pr,args);files[pr['path']]=b
 inclusion={}
 for key,texname in [('REQ','required_program.tex'),('VAL','optional_validation.tex')]:
  rows=[r for r in p['programs']if r['printed_document']==key]
  if key=='REQ':rows=[pr]+rows
  programs={r['printed_path']:files[r['path']].decode()for r in rows}
  inclusion[key]=code_inclusion((H/texname).read_text(),cache[key]['raw'],programs,cache[key]['events'],spec[key]['excluded_furniture'])
 result=dict(status='AUTHOR_INPUTS_PENDING_DISTINCT_REVIEW',topic='Enlarged Mixes',topic_originals=['F005','L016'],new_originals=['L016'],new_pdf_documents=5,new_pdf_pages=27,new_pdf_metric_cells=150,new_raw_metric_cells=60,documents=docs,raw_files=raws,retained_accepted_inputs=old,retained_cells_unchanged=True,retained_PDFs_reextracted=False,program_inclusion=inclusion,ratio=None,new_scientific_credit=0,scientific_programs_executed=False,whole_source_formalized=False,unknown_costs=p['unknown_costs'],validation_comparison=p['optional_validation_comparison'])
 return result,audits,cache

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();need(not args.out.exists(),'fresh output');args.out.mkdir(parents=True);r,f,_=replay(args)
 for n,o in [('counts.json',r),('font_audit.json',f)]:(args.out/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
 print('PASS new150PDF/60raw cells; retained180PDF/70raw cells unchanged; no factors.')
