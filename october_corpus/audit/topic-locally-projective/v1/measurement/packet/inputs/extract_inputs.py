#!/usr/bin/env python3
"""Recount seven whole PDFs and ten raw files; no scientific execution or ratios."""
from pathlib import Path
import argparse,json,re,unicodedata
import pypdf,fontTools
from font_tools import need,sha,actual_event_alignment
from pdf_text import extract
from calibration import aliases_from
from graphics_inventory import inventory
HERE=Path(__file__).resolve().parent
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
CATS=['programs','required_data','operational_drivers']
def load(n):return json.loads((HERE/n).read_text())
def metrics(t,n):
 t=unicodedata.normalize(n,t);c=' '.join(t.split())
 return dict(whitespace_tokens=len(c.split()),alphanumeric_units=len(re.findall(r'[^\W_]+',t)),characters_without_whitespace=sum(not x.isspace() for x in t),characters_with_collapsed_whitespace=len(c),utf8_bytes_with_collapsed_whitespace=len(c.encode()),collapsed_text_sha256=sha(c.encode()))
def bound(row,root):
 p=Path(row['path']);need(not p.is_absolute() and '..' not in p.parts,'safe relative input path');p=root/p;b=p.read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'exact whole input '+row['path']);return p,b

def furniture(key,raw,pages):
 out=[]
 for pg in pages:
  n=pg['page'];t=raw[pg['start']:pg['end']]
  if key=='L084':
   if n==1:continue
   literal='434 M.I. Hartley, D. Leemans\n';need(n==2 and t.startswith(literal),'literal second-page erratum header');a=0;b=len(literal)
  else:
   m=re.search(r'(?:^|\n)'+str(n)+r'\s*\Z',t);need(m is not None,'isolated trailing page number '+key);a=m.start()+(t[m.start()]=='\n');b=len(t)
  a+=pg['start'];b+=pg['start'];out.append(dict(page=n,start=a,end=b,literal=raw[a:b],sha256=sha(raw[a:b].encode())))
 return out

def selected(raw,row):
 parts=[];at=0
 for f in row['excluded_furniture']:parts.append(raw[at:f['start']]);at=f['end']
 parts.append(raw[at:]);return '\n'.join(parts)
def validate_selection(key,raw,row,pages,meta):
 need(row['pages']==len(pages) and row['page_bindings']==pages,'all physical pages '+key)
 need(row['extraction_sha256']==sha(raw.encode()),'whole raw extraction '+key)
 need(row['included_spans']==[dict(start=0,end=len(raw),sha256=sha(raw.encode()))],'whole document including tables/references')
 need(row['excluded_furniture']==furniture(key,raw,pages),'only exact running furniture')
 need(row['extraction_metadata']==meta and not meta['returned_extraction_changed'],'unchanged extraction/event metadata')
 if key=='L095':need(raw.count('arXiv:math/0307075v1  [math.GR]  5 Jul 2003')==1,'version banner retained exactly once')

def alias(event,aliases,key):
 if event is None:return None
 rows=[r for r in aliases if r['source']==key and r['font_identity']==event['font_identity'] and r['encoded_byte']==event['encoded_byte'] and r['glyph_name']==event['glyph_name']]
 need(len(rows)<=1,'unique actual dictionary/byte class');return rows[0] if rows else None

def calibrate(raw,fonts,pages,events,row,aliases,key):
 chars=list(raw);seen=set()
 for g in row['glyph_substitutions']:
  i=g['offset'];need(i not in seen and 0<=i<len(raw),'unique valid glyph offset');seen.add(i)
  need(g['input_codepoint']==f'U+{ord(raw[i]):04X}' and g['input_font']==fonts[i],'actual extracted font/character')
  need(events.get(i)==g['pdf_event'] and events.get(i) is not None,'actual PDF event/dictionary/byte')
  a=alias(events[i],aliases,key);need(a is not None and a['output']==g['output'] and a['kind']==g['kind'] and len(g['output'])==1,'one literal calibrated visible symbol')
  pg=pages[g['page']-1];lo,hi=g['context_start'],g['context_end'];need(pg['start']<=lo<=i<hi<=pg['end'] and sha(raw[lo:hi].encode())==g['context_sha256'],'bound local source context')
  need(g['page_offset']==i-pg['start'],'exact physical page offset')
  need(i not in row['extraction_metadata']['generated_newline_offsets'],'visible event not generated newline')
  need(not any(f['start']<=i<f['end'] for f in row['excluded_furniture']),'no calibrated glyph cut');chars[i]=g['output']
 for i,c in enumerate(raw):
  need(not((unicodedata.category(c) in ('Cc','Co') and c not in '\n\r\t') or c=='\ufffd') or i in seen,'all suspicious glyphs classified')
  need(alias(events.get(i),aliases,key) is None or i in seen,'every printable alias repaired')
 return ''.join(chars)

def validate_policy(p):
 need(p['source_ids']==['L084','L095'] and p['original_count']==2,'two distinct originals')
 need({k:r['pages'] for k,r in p['documents'].items()}=={'L084':2,'L095':15,'U':7,'TABLES':5,'A1':2,'A2':3,'CODE':6},'whole seven-PDF boundary')
 need(p['whole_common']==['U','TABLES'] and p['written_documents']==['U','TABLES','A1','A2'],'whole proof and all common tables')
 need(p['applications']=={'L084':['A1'],'L095':['A2']},'complete separate source applications')
 need(p['programme_printed_alternative']==['CODE'] and len(p['programs'])==6 and len({r['sha256'] for r in p['programs']})==6,'six unique whole programmes')
 need(all(r['whole_file'] and r['logical_role']=='required_finite_computation' for r in p['programs']),'all six required unpruned files')
 need(len(p['required_data'])==1 and p['required_data'][0]['bytes']==39150 and p['required_data'][0]['path'].endswith('/source_tables.json'),'whole required historical comparison data')
 need(len(p['output_data'])==11 and sum(r['bytes'] for r in p['output_data'])==3470182,'all output evidence separately inventoried')
 need(len(p['operational_drivers'])==3 and p['formal_files']==[],'three operational drivers, no formal module')
 need(p['units']==UNITS and p['normalizations']==['NFC','NFKC'] and p['variants']==['raw_untrimmed','raw_selected','calibrated_selected'],'all thirty coordinates')
 need(not p['cross_topic_discount'] and not p['factors_permitted'] and p['ratio'] is None,'input proposal only')
 need(all(v is None for v in p['unknown_costs'].values()),'external costs unknown')
 need('entire common proof+tables' in p['conditional_policy'] and 'all six whole required programs' in p['conditional_policy'] and 'full required historical comparison data' in p['conditional_policy'],'complete conditional acquisition')

def validate_scientific(p,root):
 protocol=load('protocol.json');data={}
 for r in protocol['scientific_bindings']:data[r['path']]=bound(r,root)[1]
 prefix='topic_LocallyProjective_volume/'
 for f in ['source_map.json','scope.json','software_boundary.json','computational_inputs.json','current_documents.json']:
  need(load('scientific_'+f)==json.loads(data[prefix+f]),'whole scientific metadata '+f)
 scope=load('scientific_scope.json');need(scope['complete_common_prerequisite'] and scope['application_to_application_proof_edges']==[] and scope['tables_part_of_whole_common'],'no unpaid sibling premise')
 sm=load('scientific_source_map.json');need(sm['source_ids']==['L084','L095'] and len(sm['rows'])==52 and sm['inherited_row_counts']=={'L084':18,'L095':34},'all inherited clauses and corrections')
 sw=load('scientific_software_boundary.json')
 for cat,old in [('programs','programs'),('required_data','required_comparison_data'),('output_data','complete_output_data')]:
  need(len(p[cat])==len(sw[old]),'full software category '+cat)
  for new,prev in zip(p[cat],sw[old]):need(new['path']==prefix+prev['path'] and all(new[k]==prev[k] for k in ['bytes','sha256']),'same whole software file')
 need(len(load('scientific_computational_inputs.json')['selected_file_pins'])==13,'all thirteen selected runtime/model pins; not full installation')
 return data

def appendix(tex,text,raw):
 names=re.findall(r'\\VerbatimInput(?:\[[^\]]*\])?\{([^}]+)\}',tex)
 expected=['programs/presentation.g','programs/ambient_marking.g','programs/local_geometry.g','programs/source_maximals.g','programs/quotient_census.g','accounting.py']
 need(names==expected and not re.search('firstline|lastline|firstnumber|lastnumber',tex),'whole six files printed once')
 pack=lambda s:''.join(unicodedata.normalize('NFKC',s).split()).replace('↪','').replace('⌋','')
 for name in names:need(pack(raw[name]) in pack(text),'complete printed file '+name)
 return dict(whole_files=6,printed_pages=6,pruning=False,required_data_not_in_code_pdf=True,raw_alternative_not_additive=True)

def replay(args):
 p=load('policy.json');validate_policy(p);protocol=load('protocol.json')
 need(pypdf.__version__==protocol['pypdf_version']=='6.13.0' and fontTools.__version__==protocol['fonttools_version']=='4.63.0','pinned parser versions')
 need(sha((HERE/'policy.json').read_bytes())==load('protocol_preparation.json')['policy_sha256'],'policy fixed before evaluation')
 for row in protocol['local_bindings']:bound(row,HERE)
 scientific=validate_scientific(p,args.study_root);spec=load('input_spec.json');need(set(spec)==set(p['documents']),'all seven inputs')
 aliases=load('glyph_aliases.json')['aliases'];need(aliases==aliases_from(load('font_audit.json')),'actual dictionary-bound calibration rules')
 need(len(aliases)==8 and sum(r['occurrences'] for r in aliases)==61,'all eight literal classes/sixty-one occurrences')
 docs={};audits={};cache={};graphics={}
 for key,row in p['documents'].items():
  need(all(spec[key][k]==v for k,v in row.items()),'same input identity in policy/spec');pdf,_=bound(row,args.study_root)
  raw,fonts,pages,meta=extract(pdf,False);need(raw=='\n'.join(pg.extract_text() or '' for pg in pypdf.PdfReader(pdf).pages),'literal raw extraction unchanged')
  validate_selection(key,raw,spec[key],pages,meta)
  events,audit=actual_event_alignment(pdf,raw,fonts,pages,type1_math_only=True,generated_newline_offsets=set(meta['generated_newline_offsets']))
  if key in p['source_ids']:need(not audit['unchanged_type0_dictionaries'],'all source glyph fonts actually audited')
  else:need(not events and not spec[key]['glyph_substitutions'],'own Type0 text unchanged')
  audits[key]=audit;cal=calibrate(raw,fonts,pages,events,spec[key],aliases,key)
  texts={'raw_untrimmed':raw,'raw_selected':selected(raw,spec[key]),'calibrated_selected':selected(cal,spec[key])}
  docs[key]=dict(pdf_sha256=row['sha256'],pages=row['pages'],furniture_cuts=len(spec[key]['excluded_furniture']),glyph_repairs=len(spec[key]['glyph_substitutions']),metrics={v:{n:metrics(t,n) for n in p['normalizations']} for v,t in texts.items()})
  cache[key]=dict(raw=raw,fonts=fonts,pages=pages,meta=meta,events=events,texts=texts);graphics[key]=inventory(pdf,key)
 need(audits==load('font_audit.json'),'fresh full event/font-class evidence')
 need(graphics==load('graphics_inventory.json'),'all image/form/vector presence')
 raw_counts={};raw_programs={}
 for cat in CATS:
  raw_counts[cat]={}
  for row in p[cat]:
   _,b=bound(row,args.study_root);raw_counts[cat][row['path']]=dict(bytes=len(b),sha256=sha(b),metrics={n:metrics(b.decode(),n) for n in p['normalizations']})
   if cat=='programs':raw_programs[row['path'].split('topic_LocallyProjective_volume/',1)[1]]=b.decode()
 for row in p['output_data']:bound(row,args.study_root)
 check=appendix(scientific['topic_LocallyProjective_volume/required-programs.tex'].decode(),cache['CODE']['texts']['raw_selected'],raw_programs)
 return dict(status='INPUT_REPLAY_PASS_PENDING_DISTINCT_INPUT_REVIEW',originals=2,pdf_documents=7,physical_pages=40,pdf_metric_cells=210,raw_metric_cells=100,documents=docs,raw_files=raw_counts,appendix=check,output_evidence_files=11,output_evidence_bytes=3470182,ratio=None,scientific_programs_executed=False,formal_declarations=0,unknown_costs=p['unknown_costs']),cache

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output directory')
 if (HERE/'manifest.json').exists():
  for r in load('manifest.json')['exports']:bound(r,HERE)
 r,_=replay(a);a.out.mkdir(parents=True);(a.out/'counts.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print('PASS: seven whole PDFs/40 pages; 210 PDF and 100 raw-file cells; no ratios.')
if __name__=='__main__':main()
