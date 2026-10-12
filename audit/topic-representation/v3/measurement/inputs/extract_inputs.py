#!/usr/bin/env python3
"""Whole Representation successor inputs; no factors. Reused helpers explicitly attributed."""
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
 p=Path(row['path']);need(not p.is_absolute() and '..' not in p.parts,'safe exact input path')
 f={'sources':args.study_root,'public':args.public_root,'packet':H}[row['root']]/p;b=f.read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'bound whole input '+str(p));return f,b
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
  if key=='L126' and n>1:
   expected=(str(n)+' DIMITRI LEEMANS, KLARA STOKES, AND PHILIPPE TRANCHIDA\n') if n%2==0 else ('GROUPS REPRESENTED BY INCIDENCE GEOMETRIES '+str(n)+'\n')
   need(t.startswith(expected),'literal source running header');a=pg['start'];b=a+len(expected);role='running_header_and_page_number'
  else:
   m=re.search(r'(?:^|\n)'+str(n)+r'\s*\Z',t);need(m is not None,'isolated physical page number');a=pg['start']+m.start()+(t[m.start()]=='\n');b=pg['end'];role='physical_page_number'
  cuts.append(dict(page=n,role=role,start=a,end=b,literal=raw[a:b],sha256=sha(raw[a:b].encode())))
 return cuts

def validate_selection(key,raw,row,pages,meta):
 need(row['page_bindings']==pages and row['pages']==len(pages),'all physical pages')
 need(row['extraction_sha256']==sha(raw.encode()) and row['included_spans']==[dict(start=0,end=len(raw),sha256=sha(raw.encode()))],'complete source/replacement')
 need(row['excluded_furniture']==furniture(key,raw,pages),'only exact source headers or physical page numbers')
 need(row['extraction_metadata']==meta and not meta['returned_extraction_changed'],'literal returned extraction')

def validate_policy(p,d,r):
 need(p==load('policy_before_counts.json')==load('protocol_freeze/policy.json'),'precount policy unchanged')
 need(d==load('protocol_freeze/document_map.json') and r==load('protocol_freeze/raw_file_map.json'),'precount whole document/file maps unchanged')
 need(p['primary']==dict(variant='calibrated_selected',normalization='NFC',unit='characters_without_whitespace',reason='Preserve the exact admitted F010/Representation coordinate, rather than silently changing the primary policy during an extension.'),'fixed inherited primary')
 need(p['variants']==['raw_untrimmed','raw_selected','calibrated_selected'] and p['normalizations']==['NFC','NFKC'] and p['units']==UNITS,'all thirty coordinates')
 need([(x['key'],x['pages'])for x in d['documents']]==[('F010',13),('L126',13),('U_R',13),('R1',4),('R2',12),('CODE',16)],'all71 physical pages')
 need(d['physical_pages']==71 and d['written_pages']==55 and d['reusable_exact_rows']==['F010'] and d['new_pdf_extraction_rows']==['L126','U_R','R1','R2','CODE'],'only old SOURCE reused')
 need(d['pair_map'][0]['prepaid_documents']==d['pair_map'][1]['prepaid_documents']==['U_R'] and d['no_sibling_application_dependency'],'shared theorem is in U')
 need(d['pair_map'][1]['required_files']==['certificate/check.py','certificate/graph.json'],'required whole graph code and data')
 counts={role:sum(x['role']==role for x in r['files'])for role in ['optional_validation','required_finite_certificate','required_graph_data','current_orchestration_driver','partial_formal_evidence']}
 need(counts==dict(optional_validation=9,required_finite_certificate=1,required_graph_data=1,current_orchestration_driver=2,partial_formal_evidence=4),'all17 complete files and roles')
 need(len(r['files'])==r['raw_file_count']==17 and r['partial_declarations']==22 and all(x['whole_file']for x in r['files']),'whole raw files and partial declarations')
 need(all(x is None for x in p['unknowns'].values()) and p['ratio'] is None and not p['factors_permitted'] and p['symmetric_program_rule']['software_inclusive_factor'] is None,'no invented unknowns/factors')
 need(load('written_listing_boundary.json')['masks']=={k:[]for k in ['F010','L126','U_R','R1','R2']},'symmetric manuscript empty listing masks')

def validate_manifest(row,args):
 f,b=bound(dict(root='sources',**row),args);m=json.loads(b)
 for x in m['exports']:
  q=Path(x['path']);need(not q.is_absolute() and '..'not in q.parts,'safe manifest export');data=(f.parent/q).read_bytes();need(len(data)==x['bytes'] and sha(data)==x['sha256'],'accepted export '+str(q))

def replay(args):
 p=load('policy.json');d=load('document_map.json');r=load('raw_file_map.json');validate_policy(p,d,r)
 proto=load('protocol.json');need(pypdf.__version__==proto['pypdf_version']=='6.13.0' and fontTools.__version__==proto['fonttools_version']=='4.63.0','parser versions')
 for x in proto['local_bindings']:
  b=(H/x['path']).read_bytes();need(len(b)==x['bytes'] and sha(b)==x['sha256'],'fixed extraction boundary '+x['path'])
 if (H/'manifest.json').exists():
  for x in load('manifest.json')['exports']:bound(dict(root='packet',**x),args)
 for name in ['scientific_author_manifest','scientific_independent_review','scientific_migration_review','scientific_root_adoption','prior_input_author_manifest','prior_independent_input_review','prior_root_input_adoption']:
  validate_manifest(p[name],args)
 for x in load('source_boundary.json')['bindings']:bound(dict(root='sources',**x),args)
 adoption=json.loads((args.study_root/Path(p['scientific_root_adoption']['path']).parent/'adoption.json').read_text())
 need(adoption['no_sibling_application_dependency'] and adoption['source_dispositions']==31 and adoption['retained_F010_blocks']==6,'accepted complete corrected science')
 for x in d['documents']:bound(dict(root='sources',**x),args)
 old=load('inherited/author_counts.json')['documents']['F010'];ret=load('inherited/accepted_F010_counts.json');need(old==ret,'every accepted F010 source coordinate unchanged')
 external_old=json.loads((args.study_root/Path(p['prior_input_author_manifest']['path']).parent/'author_counts.json').read_text())['documents']['F010'];need(old==external_old,'unchanged source coordinate against actual accepted report')
 external_spec=json.loads((args.study_root/Path(p['prior_input_author_manifest']['path']).parent/'source_input_spec.json').read_text());need(load('inherited/source_input_spec.json')==external_spec,'all inherited source event/furniture bindings unchanged')
 need(ret['pdf_sha256']==d['documents'][0]['sha256'] and ret['pages']==13,'exact inherited source edition')
 need(load('inherited/source_input_spec.json')['sources']['F010']['pdf_sha256']==ret['pdf_sha256'],'inherited furniture and glyph policy')
 aliases=load('glyph_aliases.json')['aliases'];spec=load('input_spec.json');docs={'F010':ret};audits={};cache={}
 need(set(spec)==set(p['new_documents']),'all five newly extracted PDFs')
 for key,row in p['new_documents'].items():
  need(all(spec[key][k]==v for k,v in row.items()),'policy/spec exact PDF');pdf,_=bound(row,args)
  raw,fonts,pages,meta=literal_extract(pdf,False);need(raw=='\n'.join(x.extract_text()or''for x in pypdf.PdfReader(pdf).pages),'literal uninstrumented extraction')
  validate_selection(key,raw,spec[key],pages,meta)
  events,audits[key]=actual_event_alignment(pdf,raw,fonts,pages,type1_math_only=key!='L126',generated_newline_offsets=set(meta['generated_newline_offsets']))
  edits=validate_glyphs(key,raw,fonts,pages,events,spec[key],aliases)
  texts=dict(raw_untrimmed=raw,raw_selected=transform(raw,spec[key]),calibrated_selected=transform(raw,spec[key],edits))
  docs[key]=dict(pdf_sha256=row['sha256'],pages=len(pages),calibrations=len(edits),furniture_occurrences=len(spec[key]['excluded_furniture']),variants={v:{n:metrics(t,n)for n in p['normalizations']}for v,t in texts.items()})
  cache[key]=dict(raw=raw,fonts=fonts,pages=pages,meta=meta,events=events,texts=texts)
 need(audits==load('font_audit.json'),'actual complete dictionary/encoding/outline audit')
 expected=[dict(document=k,font=r['font'],font_identity=r['font_identity'],encoded_byte=r['encoded_byte'],glyph_name=r['glyph_name'],input=r['decoded_text'],output=output(r),output_name=unicodedata.name(output(r)),occurrences=r['occurrences'],glyph_evidence=r['glyph_evidence'])for k,a in audits.items()for r in a['encoded_glyph_classes']if output(r)is not None]
 need(expected==aliases,'exact viewed alias classes')
 raws={}
 for row in r['files']:
  _,data=bound(dict(root='sources',**row),args);raws[row['key']]=dict(bytes=len(data),sha256=sha(data),role=row['role'],metrics={n:metrics(data.decode(),n)for n in p['normalizations']})
 appendix=load('appendix_boundary.json');tex=bound(dict(root='sources',**appendix['tex']),args)[1].decode();inc=re.findall(r'\\VerbatimInput\[[^\]]*\]\{([^}]+)\}',tex)
 need(inc==appendix['whole_file_inclusions'] and len(inc)==10 and not re.search(r'firstline|lastline|firstnumber|lastnumber',tex),'ten whole unpruned code files')
 need({str((Path('volume')/x).as_posix()).replace('volume/../','')for x in inc}=={x['key']for x in r['files']if x['role']in ['optional_validation','required_finite_certificate']},'exact whole programme roster')
 result=dict(status='AUTHOR_COMPLETE_INPUT_PROPOSAL_PENDING_INDEPENDENT_REVIEW',originals=['F010','L126'],documents=docs,raw_files=raws,inherited_F010_source_exact=True,inherited_PDF_cells=30,new_PDF_cells=150,PDF_cells=180,raw_cells=170,physical_pages=71,manuscript_pages=55,program_appendix_pages=16,science_reexecuted=False,complete_source_formalization=False,ratio=None,software_inclusive_factor=None,new_source_credit=0,new_question_credit=0)
 return result,cache

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,default=Path('/Users/sasha/medusa/math_compression'));ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();need(not args.out.exists(),'fresh output');args.out.mkdir(parents=True);result,_=replay(args);(args.out/'counts.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('PASS180PDF/170rawcells including30unchangedF010sourcecells; no ratios')
