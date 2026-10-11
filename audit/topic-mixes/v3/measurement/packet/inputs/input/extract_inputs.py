#!/usr/bin/env python3
"""Whole three-source Mixes inputs; no factors. Font helpers are attributed."""
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
 f={'sources':args.sources_root,'public':args.public_root,'packet':H}[row['root']]/p;b=f.read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'bound whole input '+str(p));return f,b
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
  if key=='F007':
   if n>1:
    expected=(f'23 Page {n} of 29 Journal of Algebraic Combinatorics (2026) 64:23 ' if n%2==0 else f'Journal of Algebraic Combinatorics (2026) 64:23 Page {n} of 29 23 ')
    need(t.startswith(expected+'\n'),'exact complete running journal header')
    a=pg['start'];b=a+len(expected)+1;cuts.append(dict(page=n,role='running_header',start=a,end=b,literal=raw[a:b],sha256=sha(raw[a:b].encode())))
   tail='0123456789().: V,-vol 123' if n==1 else '123'
   need(t.endswith(tail),'exact publisher footer extraction')
   a=pg['end']-len(tail);b=pg['end'];role='publisher_footer'
  else:
   m=re.search(r'(?:^|\n)'+str(n)+r'\s*\Z',t);need(m is not None,'isolated physical footer');a=pg['start']+m.start()+(t[m.start()]=='\n');b=pg['end'];role='physical_footer'
  cuts.append(dict(page=n,role=role,start=a,end=b,literal=raw[a:b],sha256=sha(raw[a:b].encode())))
 return cuts

def validate_selection(key,raw,row,pages,meta):
 need(row['page_bindings']==pages and row['pages']==len(pages),'all physical pages')
 need(row['extraction_sha256']==sha(raw.encode()) and row['included_spans']==[dict(start=0,end=len(raw),sha256=sha(raw.encode()))],'complete source/replacement')
 need(row['excluded_furniture']==furniture(key,raw,pages),'only exact declared running headers/publisher or physical footers')
 need(row['extraction_metadata']==meta and not meta['returned_extraction_changed'],'literal returned extraction')

def validate_policy(p):
 need(p['originals']==['F005','L016','F007'] and p['new_source']=='F007','three exact originals')
 need(p['primary']=='raw_untrimmed/NFC/characters_without_whitespace' and p['variants']==['raw_untrimmed','raw_selected','calibrated_selected'] and p['normalizations']==['NFC','NFKC'] and p['units']==UNITS,'predeclared thirty coordinates')
 w=p['whole_topic_boundary'];need(w==dict(source_documents=['F005','L016','F007'],common_documents=['U','U1','U2'],applications={'F005':['A1','A2'],'L016':['A3'],'F007':['A4','A5']},source_pages=62,common_pages=13,application_pages=27,no_free_old_common=True,companion_is_application=True),'entire three common and five application papers')
 need([p['new_documents'][k]['pages']for k in ['F007','U2','A4','A5']]==[29,4,5,4],'all new pages')
 b=p['software_boundary'];need(len(b['required_full_programs'])==2 and len(b['optional_full_programs'])==6 and len(b['drivers'])==6 and len(b['formal'])==3,'whole software inventory')
 need(all(x['role']=='required_finite_certificate' for x in b['required_full_programs']) and all(not x.get('mathematical_premise',x.get('uniform_mathematical_premise',False))for x in b['optional_full_programs']),'required versus optional premises')
 need(b['partial_declarations']==12 and not b['full_source_formalized'] and b['dual_role_companion_checker_charged_once'],'partial formal and duplicate roles')
 need(p['symmetry']==dict(manuscript_comparison_excludes_executable_listings_both_sides=True,program_inventory_separate=True,optional_validation_is_not_a_conditional_prerequisite=True,software_inclusive_factor=None,unprovided_historical_software=None,proof_prose_algorithms_and_presentations_retained=True),'symmetric code boundary and unknown source software')
 need(p['scope']==dict(F005_rows=35,L016_rows=19,F007_numbered=48,F007_additional=6,F007_page25_chain_class_paragraph='not recovered',F007_problems1_and2='unanswered',F007_problem3='natural reconstruction; arbitrary isomorphism for finite posets with connected flag graph; no general infinite arbitrary-isomorphism or priority claim'),'complete qualified contract')
 need(p['whole_documents'] and not p['overlap_discount'] and not p['factors_permitted'] and p['ratio'] is None and p['new_scientific_credit']==0 and all(v is None for v in p['unknown_costs'].values()),'whole boundary, unknowns, no factors/credits')

def validate_retained(retained,old0,old1):
 need(old1['retained_accepted_inputs']==old0,'earlier two-source nesting exact')
 expected={**old0['documents'],**old1['documents']};need(retained['documents']==expected,'all330 retained PDF cells remain unchanged')
 er={c:{**old0['raw_files'][c],**old1['raw_files'][c]}for c in ['programs','drivers','formal']};need(retained['raw_files']==er,'all130 retained raw cells remain unchanged')
 need(len(expected)==11 and sum(len(x)for x in er.values())==13,'retained complete files')

def validate_boundary(b,p):
 need(b['new_source']['sha256']==p['new_documents']['F007']['sha256'] and b['new_source']['physical_pages']==list(range(1,30)),'all source listing pages')
 need(b['new_source']['embedded_executable_blocks']==[] and b['new_source']['embedded_optional_validation']==[] and b['new_source']['masks']==[] and b['new_replacement_masks']=={'U2':[],'A4':[],'A5':[]},'symmetric empty listing masks with positive source reading')
 need(b['source_software_cost'] is None and b['no_ratio_evaluated'] and b['source_proof_prose_and_formulas_retained'],'no missing software assigned zero')


def replay(args):
 p=load('policy.json');need(p==load('policy_before_counts.json'),'pre-count policy unchanged');validate_policy(p);proto=load('protocol.json');spec=load('input_spec.json')
 need(pypdf.__version__==proto['pypdf_version']=='6.13.0' and fontTools.__version__==proto['fonttools_version']=='4.63.0','pinned PDF/font packages')
 for r in proto['local_bindings']:
  data=(H/r['path']).read_bytes();need(len(data)==r['bytes'] and sha(data)==r['sha256'],'fixed local spec '+r['path'])
 if (H/'manifest.json').exists():
  for r in load('manifest.json')['exports']:bound(dict(root='packet',**r),args)
 for r in p['acceptances']:
  f,b=bound(r,args);m=json.loads(b)
  for x in m['exports']:
   q=Path(x['path']);need(not q.is_absolute() and '..'not in q.parts,'safe accepted export');data=(f.parent/q).read_bytes();need(len(data)==x['bytes'] and sha(data)==x['sha256'],'accepted export '+str(q))
 for r in load('source_boundary.json')['bindings']:bound(r,args)
 old0=json.loads(bound(p['retained_counts'][0],args)[1]);old1=json.loads(bound(p['retained_counts'][1],args)[1]);retained=load('retained_counts.json');validate_retained(retained,old0,old1)
 for k,r in p['retained_documents'].items():
  _,b=bound(r,args);need(retained['documents'][k]['pdf_sha256']==sha(b),'whole retained PDF '+k)
 for category in ['required_full_programs','optional_full_programs','drivers','formal']:
  for r in p['software_boundary'][category]:bound(r,args)
 validate_boundary(load('source_code_boundary.json'),p)
 adoption=json.loads(bound(next(r for r in load('source_boundary.json')['bindings']if r['path'].endswith('root_adoption/adoption.json')),args)[1])
 need(adoption['status']=='ROOT_ACCEPTED_F007_CORRECTED_PRINCIPAL_PROOF' and adoption['numbered_results']==48 and adoption['additional_dispositions']==6 and adoption['required_new_programs']==0 and adoption['optional_new_diagnostics']==2 and not adoption['complete_Lean'],'accepted corrected science and formal limits')
 aliases=load('glyph_aliases.json')['aliases'];docs={};audits={};cache={}
 need(set(spec)==set(p['new_documents']),'exact new PDF roster')
 for key,row in p['new_documents'].items():
  need(all(spec[key][k]==v for k,v in row.items()),'policy/spec exact binding');pdf,_=bound(row,args)
  raw,fonts,pages,meta=literal_extract(pdf,False);need(raw=='\n'.join(x.extract_text()or''for x in pypdf.PdfReader(pdf).pages),'literal uninstrumented extraction')
  validate_selection(key,raw,spec[key],pages,meta)
  events,audits[key]=actual_event_alignment(pdf,raw,fonts,pages,type1_math_only=key!='F007',generated_newline_offsets=set(meta['generated_newline_offsets']))
  edits=validate_glyphs(key,raw,fonts,pages,events,spec[key],aliases)
  texts=dict(raw_untrimmed=raw,raw_selected=transform(raw,spec[key]),calibrated_selected=transform(raw,spec[key],edits))
  docs[key]=dict(pdf_sha256=row['sha256'],pages=len(pages),furniture_cuts=len(spec[key]['excluded_furniture']),glyph_repairs=len(edits),metrics={v:{n:metrics(t,n)for n in p['normalizations']}for v,t in texts.items()})
  cache[key]=dict(raw=raw,fonts=fonts,pages=pages,meta=meta,events=events,texts=texts)
 need(audits==load('font_audit.json'),'complete actual font dictionary/effective encoding audit')
 expected=[dict(document=k,font=r['font'],font_identity=r['font_identity'],encoded_byte=r['encoded_byte'],glyph_name=r['glyph_name'],input=r['decoded_text'],output=output(r),output_name=unicodedata.name(output(r)),occurrences=r['occurrences'],glyph_evidence=r['glyph_evidence'])for k,a in audits.items()for r in a['encoded_glyph_classes']if output(r)is not None]
 need(expected==aliases,'exact observed glyph aliases')
 raws={}
 for cat,rows in p['new_raw_files'].items():
  raws[cat]={}
  for r in rows:
   _,data=bound(r,args);raws[cat][r['path']]=dict(bytes=len(data),sha256=sha(data),role=r['role'],metrics={n:metrics(data.decode(),n)for n in p['normalizations']})
 result=dict(status='AUTHOR_INPUTS_PENDING_DISTINCT_REVIEW',originals=p['originals'],documents=docs,raw_files=raws,retained_accepted_inputs=retained,retained_cells_unchanged=True,retained_PDFs_reextracted=False,new_PDF_cells=120,new_raw_cells=40,retained_PDF_cells=330,retained_raw_cells=130,whole_topic_boundary=p['whole_topic_boundary'],software_boundary=p['software_boundary'],unknown_costs=p['unknown_costs'],ratio=None,software_inclusive_factor=None,scientific_programs_executed=False,whole_source_formalized=False,new_scientific_credit=0)
 return result,audits,cache

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();need(not args.out.exists(),'fresh output');args.out.mkdir(parents=True);result,fonts,_=replay(args)
 for n,o in [('counts.json',result),('font_audit.json',fonts)]:(args.out/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
 print('PASS new120PDF/40raw, retained330PDF/130raw unchanged; no factors.')
