#!/usr/bin/env python3
"""Whole five-original E input recount; no ratios, mathematical programs or Lean runs."""
import argparse,json,re,unicodedata
from pathlib import Path
import pypdf,fontTools
from font_tools import need,sha,actual_event_alignment
from pdf_text import extract
from calibration import aliases_from
from graphics_inventory import inventory
HERE=Path(__file__).resolve().parent
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
CATS=['programs_and_data','operational_drivers','formal_files']
def load(n):return json.loads((HERE/n).read_text())
def metrics(t,n):
 t=unicodedata.normalize(n,t);c=' '.join(t.split());return dict(whitespace_tokens=len(c.split()),alphanumeric_units=len(re.findall(r'[^\W_]+',t)),characters_without_whitespace=sum(not x.isspace() for x in t),characters_with_collapsed_whitespace=len(c),utf8_bytes_with_collapsed_whitespace=len(c.encode()),normalized_text_sha256=sha(t.encode()),collapsed_text_sha256=sha(c.encode()))
def bound(row,root):
 path=Path(row['path']);need(not path.is_absolute() and '..' not in path.parts,'safe relative input path');p=root/path;b=p.read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'whole bound input '+row['path']);return p,b

def furniture(key,raw,pages):
 out=[]
 for pg in pages:
  n=pg['page'];t=raw[pg['start']:pg['end']]
  if key=='L056' or (key in ['L079','L021'] and n==1):continue
  if key=='L079':
   literal=(f'{n} Ars Mathematica Contemporanea x (xxxx) 1–x\n' if n%2==0 else f'Ars Mathematica Contemporanea x (xxxx) 1–x {n}\n')
   need(t.startswith(literal),'literal source L079 header');a=0;b=len(literal)
  elif key=='L043' and n>1:
   literal=(f'{n} DIMITRI LEEMANS, J ´ER ´EMIE MOERENHOUT, AND EUGENIA O’REILLY-REGUEIRO\n' if n%2==0 else f'PROJECTIVE LINEAR GROUPS AND CHIRAL POLYTOPES {n}\n')
   need(t.startswith(literal),'literal source L043 header');a=0;b=len(literal)
  else:
   need(t.endswith('\n'+str(n)),'isolated trailing page number '+key+' '+str(n));a=len(t)-len(str(n));b=len(t)
  a+=pg['start'];b+=pg['start'];out.append(dict(page=n,start=a,end=b,literal=raw[a:b],sha256=sha(raw[a:b].encode())))
 return out

def selected(raw,row):
 result=[];last=0
 for f in row['excluded_furniture']:result.append(raw[last:f['start']]);last=f['end']
 result.append(raw[last:]);return '\n'.join(result)

def validate_policy(p):
 need(p['source_ids']==['L079','L083','L021','L056','L043'] and p['original_count']==5,'exact five originals')
 need(p['new_source_dispositions']==56 and p['retained_source_dispositions']==54,'all110 source dispositions')
 need({k:r['pages'] for k,r in p['documents'].items()}==dict(L079=9,L083=14,L021=11,L056=8,L043=25,U=20,A1=2,A2=1,A3=5,A4=2,A5=4,REQUIRED=20,VALIDATION=7),'whole13PDF128page boundary')
 need(p['whole_common']==['U'] and p['written_documents']==['U','A1','A2','A3','A4','A5'],'full common and all applications')
 need(p['applications']==dict(L083=['A1'],L079=['A2'],L021=['A3'],L056=['A4'],L043=['A5']),'correct source/application routing')
 need(p['required_printed_alternative']==['REQUIRED'] and p['optional_validation_printed_alternative']==['VALIDATION'],'distinct printed alternatives')
 rows=p['programs_and_data'];need(len(rows)==13 and len({r['sha256']for r in rows})==13 and all(r['whole_file']for r in rows),'six+six programs and mandatory JSON whole')
 need([r['role'] for r in rows]==['required finite proof']*6+['validation only']*6+['required certificate data'],'no required/optional relabeling')
 need(rows[-1]['bytes']==3982,'whole mandatory JSON')
 need(len(p['operational_drivers'])==5 and len(p['formal_files'])==7 and sum(r['declarations']for r in p['formal_files'])==42 and p['formal_declarations']==42 and p['new_formal_declarations']==9,'scoped drivers/formal evidence')
 need(p['primary_coordinate']==dict(variant='raw_untrimmed',normalization='NFC',unit='characters_without_whitespace'),'raw primary')
 need(p['units']==UNITS and p['normalizations']==['NFC','NFKC'] and p['variants']==['raw_untrimmed','raw_selected','calibrated_selected'],'all30 coordinates')
 sy=p['symmetry_policy'];need(sy['historical_software_cost'] is None and sy['inclusive_software_factor'] is None and sy['optional_validation'].startswith('Excluded on both sides'),'symmetric optional policy and unknown historical software')
 need('six required' in sy['conditional'] and 'mandatory JSON' in sy['conditional'] and sy['no_cross_topic_free_premise'] and sy['no_printed_plus_raw_double_charge'],'full conditional preacquisition')
 need(not p['factors_permitted'] and p['ratio'] is None and p['new_source_credit']==p['new_question_credit']==0 and not p['GAP_or_Lean_reexecution'],'inputs only')
 need(all(v is None for v in p['unknown_costs'].values()),'unknown not zero')

def alias(event,aliases,key):
 if event is None:return None
 hits=[r for r in aliases if r['source']==key and r['font_identity']==event['font_identity'] and r['encoded_byte']==event['encoded_byte'] and r['glyph_name']==event['glyph_name']]
 need(len(hits)<=1,'unique actual dictionary/byte alias');return hits[0] if hits else None

def calibrate(raw,fonts,pages,events,row,aliases,key):
 chars=list(raw);seen=set()
 for g in row['glyph_substitutions']:
  i=g['offset'];need(i not in seen and 0<=i<len(raw),'unique valid glyph');seen.add(i)
  need(g['input_codepoint']==f'U+{ord(raw[i]):04X}' and g['input_font']==fonts[i],'actual font and character')
  need(events.get(i)==g['pdf_event'] and events.get(i) is not None,'actual original encoded event')
  a=alias(events[i],aliases,key);need(a is not None and a['output']==g['output'] and a['kind']==g['kind'] and len(g['output'])==1,'visible symbol calibration')
  pg=pages[g['page']-1];lo,hi=g['context_start'],g['context_end'];need(pg['start']<=lo<=i<hi<=pg['end'] and sha(raw[lo:hi].encode())==g['context_sha256'] and g['page_offset']==i-pg['start'],'bound source occurrence')
  need(i not in row['extraction_metadata']['generated_newline_offsets'] and not any(f['start']<=i<f['end'] for f in row['excluded_furniture']),'visible glyph never furniture/generated newline');chars[i]=g['output']
 for i,ch in enumerate(raw):
  need(not ((unicodedata.category(ch) in ('Cc','Co') and ch not in '\n\r\t') or ch=='\ufffd') or i in seen,'every problematic extraction classified')
  need(alias(events.get(i),aliases,key) is None or i in seen,'all printable aliases repaired')
 return ''.join(chars)

def replay(root):
 p=load('policy.json');validate_policy(p);need(sha((HERE/'policy.json').read_bytes())==load('policy_freeze.json')['policy_sha256'],'policy fixed before counts')
 need(pypdf.__version__=='6.13.0' and fontTools.__version__=='4.63.0','pinned PDF/font engines')
 scientific={r['path']:bound(r,root)[1]for r in p['scientific_bindings']}
 for filename in ['bibliography_acceptance.json','science_adoption.json']:
  info=load(filename)
  for key in ['manifest','binding','root_adoption','review_manifest']:
   if key in info and isinstance(info[key],dict):bound(info[key],root)
 for r in load('additional_bindings.json')['bindings']:bound(r,root)
 need(load('retained_inputs.json')==json.loads((root/'topic_E_chiral_extension_bibliography_v2/retained_inputs.json').read_text()),'exact retained dependencies')
 scope=load('scientific_scope.json');need(scope==json.loads(scientific['topic_E_chiral_extension_bibliography_v2/scope.json']),'unchanged complete scientific scope')
 for local,remote in [('source_map.json','source_map.json'),('retained_source_maps.json','retained_source_maps.json'),('program_scope.json','program_scope.json'),('formal_scope.json','formal/scope.json')]:
  need(load(local)==json.loads(scientific['topic_E_chiral_extension_bibliography_v2/'+remote]),'exact inherited '+local)
 spec=load('input_spec.json');need(set(spec)==set(p['documents']),'all PDFs')
 aliases=load('glyph_aliases.json')['aliases'];need(aliases==aliases_from(load('font_audit.json')),'source-specific actual outline rules')
 docs={};audits={};graphs={};cache={}
 for key,row in p['documents'].items():
  need(all(spec[key][k]==v for k,v in row.items()),'same input identity');path,_=bound(row,root);raw,fonts,pages,meta=extract(path,False)
  need(raw=='\n'.join(pg.extract_text() or ''for pg in pypdf.PdfReader(path).pages),'returned text unaltered')
  need(len(pages)==row['pages'] and spec[key]['page_bindings']==pages and spec[key]['extraction_metadata']==meta,'all page/event metadata')
  need(spec[key]['extraction_sha256']==sha(raw.encode()) and spec[key]['included_spans']==[dict(start=0,end=len(raw),sha256=sha(raw.encode()))],'whole title/body/figures/refs')
  need(spec[key]['excluded_furniture']==furniture(key,raw,pages),'only exact furniture')
  events,audit=actual_event_alignment(path,raw,fonts,pages,type1_math_only=True,generated_newline_offsets=set(meta['generated_newline_offsets']));audits[key]=audit
  if key in p['source_ids']:need(not audit['unchanged_type0_dictionaries'],'all source fonts audited by encoded event')
  else:need(not events and not spec[key]['glyph_substitutions'],'replacement Unicode text unchanged')
  cal=calibrate(raw,fonts,pages,events,spec[key],aliases,key);texts=dict(raw_untrimmed=raw,raw_selected=selected(raw,spec[key]),calibrated_selected=selected(cal,spec[key]))
  docs[key]=dict(pdf_sha256=row['sha256'],pages=row['pages'],furniture_cuts=len(spec[key]['excluded_furniture']),glyph_repairs=len(spec[key]['glyph_substitutions']),metrics={v:{n:metrics(t,n)for n in p['normalizations']}for v,t in texts.items()});graphs[key]=inventory(path,key);cache[key]=dict(raw=raw,fonts=fonts,pages=pages,meta=meta,events=events,texts=texts)
 need(audits==load('font_audit.json'),'all actual font dictionaries/encoded classes/outline evidence')
 need(graphs==load('graphics_inventory.json'),'all vector/image/form evidence preserved')
 rawcounts={};rawprograms={}
 for cat in CATS:
  rawcounts[cat]={}
  for row in p[cat]:
   _,b=bound(row,root);rawcounts[cat][row['path']]=dict(bytes=len(b),sha256=sha(b),metrics={n:metrics(b.decode(),n)for n in p['normalizations']})
   if cat=='programs_and_data':rawprograms[Path(row['path']).name]=b.decode()
 # The exact scientific manifest binds appendix TeX. Whole blocks must equal whole raw files.
 manifest=json.loads(scientific['topic_E_chiral_extension_bibliography_v2/manifest.json'])
 rows={r['path']:r for r in manifest['exports']};base=root/'topic_E_chiral_extension_bibliography_v2';appstats={}
 compact=lambda t:''.join(unicodedata.normalize('NFKC',t).split())
 for doc,stem,roles in [('REQUIRED','required-programs',{'required finite proof','required certificate data'}),('VALIDATION','validation-programs',{'validation only'})]:
  tex=bound(rows[stem+'.tex'],base)[1].decode();blocks=re.findall(r'\\begin\{CompleteProgram\}\n(.*?)\\end\{CompleteProgram\}',tex,re.S)
  names=[Path(r['path']).name for r in p['programs_and_data']if r['role']in roles];need(len(blocks)==len(names),'complete appendix block count')
  printed=compact(cache[doc]['texts']['raw_selected'])
  for name,block in zip(names,blocks):
   need(block==rawprograms[name] or block==rawprograms[name]+'\n','whole exact appendix source '+name)
   need(printed.count(compact(rawprograms[name]))==1,'whole printed file once '+name)
  appstats[doc]=dict(pages=p['documents'][doc]['pages'],files=names,whole_raw_bytes=sum(r['bytes']for r in p['programs_and_data']if r['role']in roles),printed_raw_alternatives=True)
 srcaud=[audits[k]for k in p['source_ids']]
 return dict(status='AUTHOR_INPUT_REPLAY_PASS_PENDING_DISTINCT_INPUT_REVIEW',originals=5,source_dispositions=110,pdf_documents=13,physical_pages=128,pdf_metric_cells=390,raw_metric_cells=250,documents=docs,raw_files=rawcounts,appendices=appstats,formal_files=7,formal_declarations=42,source_font_dictionaries=sum(len(r['font_dictionaries'])for r in srcaud),source_glyph_classes=sum(len(r['encoded_glyph_classes'])for r in srcaud),source_calibrated_classes=19,source_calibrated_occurrences=279,ratio=None,scientific_programs_executed=False,unknown_costs=p['unknown_costs']),cache

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output directory')
 if (HERE/'manifest.json').exists():
  for r in load('manifest.json')['exports']:bound(r,HERE)
 result,_=replay(a.study_root)
 if (HERE/'author_counts.json').exists():need(result==load('author_counts.json'),'exact whole count reproduction')
 a.out.mkdir(parents=True);(a.out/'counts.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('PASS:13 PDFs/128 pages;390 PDF +250 raw cells; no factors.')
if __name__=='__main__':main()
