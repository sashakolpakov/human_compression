#!/usr/bin/env python3
"""Whole-document additions to existing Topics A and C; no factors."""
from pathlib import Path
import argparse,json,re,unicodedata
import pypdf,fontTools
from font_tools import need,sha,actual_event_alignment
from pdf_text import extract as literal_extract,BANNER
from calibration import output
H=Path(__file__).resolve().parent
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
KEYS={'L128','L068','A7','A_CODE_NEW','U_C_INC','C5','C_CODE_NEW'}
def load(n):return json.loads((H/n).read_text())
def bound(row,args):
 f={'public':args.public_root,'sources':args.sources_root,'packet':H}[row['root']]/row['path'];b=f.read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'bound whole input '+row['path']);return f,b

def metrics(s,form):
 s=unicodedata.normalize(form,s);c=' '.join(s.split());return dict(whitespace_tokens=len(c.split()),alphanumeric_units=len(re.findall(r'[^\W_]+',s)),characters_without_whitespace=sum(not x.isspace() for x in s),characters_with_collapsed_whitespace=len(c),utf8_bytes_with_collapsed_whitespace=len(c.encode()),collapsed_text_sha256=sha(c.encode()))

def furniture(key,raw,pages):
 cuts=[]
 for pg in pages:
  n=pg['page'];t=raw[pg['start']:pg['end']]
  if key=='L128':
   if n==1:a=t.rfind('\n1\n'+BANNER)+1;need(a>0,'first source page number');b=a+1
   else:literal=str(n)+'\n';need(t.startswith(literal),'source page number');a=0;b=len(literal)
  elif key=='L068':
   if n==1:continue
   number=n+192;literal=f'{number} J Algebr Comb (2012) 35:193–214\n' if n%2==0 else f'J Algebr Comb (2012) 35:193–214 {number}\n';need(t.startswith(literal),'journal running header');a=0;b=len(literal)
  else:
   m=re.search(r'(?:^|\n)'+str(n)+r'\s*\Z',t);need(m is not None,'isolated footer');a=m.start()+(t[m.start()]=='\n');b=len(t)
  a+=pg['start'];b+=pg['start'];cuts.append(dict(page=n,start=a,end=b,literal=raw[a:b],sha256=sha(raw[a:b].encode())))
 return cuts

def validate_selection(key,raw,row,pages,meta):
 need(row['page_bindings']==pages and row['pages']==len(pages),'all physical pages')
 need(row['extraction_sha256']==sha(raw.encode()) and row['included_spans']==[dict(start=0,end=len(raw),sha256=sha(raw.encode()))],'whole authored manuscript')
 need(row['excluded_furniture']==furniture(key,raw,pages),'exact repeated furniture only')
 need(row['extraction_metadata']==meta and not meta['returned_extraction_changed'],'precise generated whitespace and Form metadata')
 if key=='L128':need(raw.count(BANNER)==1,'version stamp retained exactly once')

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

def audit_font(key,pdf,raw,fonts,pages,meta):
 e,a=actual_event_alignment(pdf,raw,fonts,pages,type1_math_only=key!='L068',generated_newline_offsets=set(meta['generated_newline_offsets']))
 if key=='L128':
  skipped=a['unchanged_type0_dictionaries'];need(len(skipped)==1,'one Unicode version stamp');font=skipped[0]['font'];need(''.join(c for c,f in zip(raw,fonts) if f==font)==BANNER,'only exact stamp excluded from body outline audit');a['source_unicode_banner']=dict(literal=BANNER,font=font,retained_in_all_variants=True)
 return e,a

def validate_policy(p):
 need(p['original_manuscripts_added']==2 and p['source_ids']==['L128','L068'] and p['source_originals_after_update']=={'A':7,'C':5} and p['new_topic_count']==0,'two originals added to existing topics')
 need(p['source_rows']=={'L128':14,'L068':17} and p['proof_spans']=={'L128':7,'L068':9},'accepted scientific boundary')
 need(len(p['new_programs'])==2 and len(p['old_C_required_programs'])==2 and len(p['drivers'])==3 and len(p['formal'])==2 and len(p['whole_common_papers'])==2,'complete shared/common/code closure')
 need(p['shared_program']['sha256']==p['old_C_required_programs'][0]['sha256'],'whole shared program counted once')
 need(not p['factors_permitted'] and p['ratio'] is None and p['no_new_mathematical_credit'],'no input-stage factors or mathematical credit')
 need(all(x is None for x in p['unknown_costs'].values()),'unknown costs null')
 need(p['units']==UNITS and p['variants']==['raw_untrimmed','raw_selected','calibrated_selected'] and p['normalizations']==['NFC','NFKC'],'all thirty coordinates')
 need(set(p['sources'])=={'L128','L068'} and set(p['replacements'])==KEYS-{'L128','L068'},'complete source and replacement inventory')
 need(p['pdf_documents']==7 and p['pdf_pages']==48 and p['pdf_metric_cells']==210 and p['raw_metric_cells']==80,'all full-document coordinates')
 need(p['whole_topic_rules']=={'A':{'previous_originals':6,'added_originals':['L128'],'retain_all_previous_applications':True,'retain_full_previous_common':True,'additional_common':[],'new_application':'A7','old_program_bundle_retained':True,'new_printed_program':'A_CODE_NEW','new_required_files':1},'C':{'previous_originals':4,'added_originals':['L068'],'retain_all_previous_applications':True,'retain_full_previous_common':True,'additional_common':['U_C_INC'],'new_application':'C5','old_program_bundle_retained':True,'old_required_files':2,'new_required_files':1,'shared_existing_file_charged_once':True,'new_printed_program':'C_CODE_NEW'}},'whole umbrella, applications and code are paid once in each existing topic')
 need(not p['full_formalization_claim'] and p['partial_formal_declarations']==9,'nine scoped formal declarations only')
 need(p['A_primary']=='Unchanged accepted calibrated_selected NFC nonspace characters; all other coordinates retained.' and p['C_primary']=='Unchanged accepted whole rendered L108 text + raw_untrimmed PDFs for all remaining C documents, including these additions; selected/calibrated sensitivities remain separate.','unchanged whole-topic representation policies')

def code_inclusion(tex,text,code,name):
 need(re.findall(r'\\VerbatimInput(?:\[[^\]]*\])?\{([^}]+)\}',tex)==[name],'one full additional program')
 need(not re.search('firstline|lastline|firstnumber|lastnumber',tex),'no line pruning')
 pack=lambda s:''.join(unicodedata.normalize('NFKC',s).split()).replace('↪','').replace('⌋','').replace(',→','')
 need(pack(code) in pack(text),'whole literal file present')
 return dict(complete_files=1,no_pruning=True,wrap_markers_included_in_cost=True)

def replay(args):
 p=load('policy.json');validate_policy(p);spec=load('input_spec.json');need(set(spec)==KEYS,'all seven full PDFs');protocol=load('protocol.json')
 need(pypdf.__version__==protocol['pypdf_version']=='6.13.0' and fontTools.__version__==protocol['fonttools_version']=='4.63.0','pinned libraries')
 for r in protocol['local_bindings']:
  b=(H/r['path']).read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'bound local input '+r['path'])
 if (H/'manifest.json').exists():
  for r in load('manifest.json')['exports']:
   f=Path(r['path']);need(not f.is_absolute() and '..' not in f.parts,'safe export');b=(H/f).read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'frozen export '+str(f))
 scientific={r['path']:bound(r,args)[1] for r in p['scientific_bindings']}
 need({k:json.loads(v) for k,v in scientific.items() if not k.endswith('programs.tex')}==load('source_boundary.json'),'exact accepted contracts and distinct reviews')
 for r in p['retained_numerical_inputs']+p['old_C_required_programs']+p['whole_common_papers']:bound(r,args)
 need(bound(p['shared_program'],args)[1]==bound(p['old_C_required_programs'][0],args)[1],'actual byte-identical shared C program')
 aliases=load('glyph_aliases.json')['aliases'];need(len(aliases)==27 and sum(x['occurrences'] for x in aliases)==286,'full calibration census');docs={};audits={};cache={}
 for key,row in (p['sources']|p['replacements']).items():
  need(all(spec[key][k]==v for k,v in row.items()),'same policy/spec input');pdf,_=bound(row,args);raw,fonts,pages,meta=literal_extract(pdf,key=='L128')
  need(raw=='\n'.join(x.extract_text() or '' for x in pypdf.PdfReader(pdf).pages),'raw equals uninstrumented returned extraction');validate_selection(key,raw,spec[key],pages,meta);events={}
  if key in ('L128','L068','U_C_INC','C5','C_CODE_NEW'):events,audits[key]=audit_font(key,pdf,raw,fonts,pages,meta)
  edits=validate_glyphs(key,raw,fonts,pages,events,spec[key],aliases);texts=dict(raw_untrimmed=raw,raw_selected=transform(raw,spec[key]),calibrated_selected=transform(raw,spec[key],edits))
  docs[key]=dict(pdf_sha256=row['sha256'],pages=row['pages'],furniture_cuts=len(spec[key]['excluded_furniture']),glyph_repairs=len(edits),metrics={v:{n:metrics(t,n) for n in p['normalizations']} for v,t in texts.items()});cache[key]=dict(raw=raw,fonts=fonts,pages=pages,meta=meta,events=events,texts=texts)
 need(audits==load('font_audit.json'),'fresh actual font dictionaries/encodings/outlines')
 expect=[dict(document=key,font=r['font'],font_identity=r['font_identity'],encoded_byte=r['encoded_byte'],glyph_name=r['glyph_name'],input=r['decoded_text'],output=output(r),output_name=unicodedata.name(output(r)),occurrences=r['occurrences'],glyph_evidence=r['glyph_evidence']) for key,a in audits.items() for r in a['encoded_glyph_classes'] if output(r) is not None];need(aliases==expect,'aliases from every actual visible class')
 raw_counts={};raw_files={}
 for category,rows in [('new_programs',p['new_programs']),('shared_existing',[p['shared_program']]),('drivers',p['drivers']),('formal',p['formal'])]:
  raw_counts[category]={}
  for r in rows:
   _,b=bound(r,args);raw_files[r['path']]=b;raw_counts[category][r['path']]=dict(bytes=len(b),sha256=sha(b),role=r['role'],metrics={n:metrics(b.decode(),n) for n in p['normalizations']})
 newcode=p['new_programs'][1];need((H/'programs/phase179_livingstone_check.g').read_bytes()==raw_files[newcode['path']],'unchanged whole source-incidence program copy')
 appendices={'A':code_inclusion(scientific['papers/topic-a/extensions/diagram-symmetries/v1/programs.tex'].decode(),cache['A_CODE_NEW']['texts']['raw_selected'],raw_files[p['new_programs'][0]['path']].decode(),'minimal_rank_three.g'),'C':code_inclusion((H/'livingstone_additional_program.tex').read_text(),cache['C_CODE_NEW']['texts']['raw_selected'],raw_files[newcode['path']].decode(),'programs/phase179_livingstone_check.g')}
 result=dict(status='AUTHOR_INPUTS_PENDING_DISTINCT_REVIEW',original_manuscripts_added=2,source_ids=['L128','L068'],existing_topics=['A','C'],new_topics=0,pdf_documents=7,pdf_pages=48,pdf_metric_cells=210,raw_metric_cells=80,documents=docs,raw_files=raw_counts,appendices=appendices,ratio=None,new_scientific_credit=0,scientific_programs_executed=False,full_formalization_claim=False,unknown_costs=p['unknown_costs'])
 return result,audits,cache

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True);result,audits,_=replay(a)
 for name,obj in [('counts.json',result),('font_audit.json',audits)]:(a.out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 print('PASS 210 PDF and 80 raw cells; two originals added to A/C, no factors.')
if __name__=='__main__':main()
