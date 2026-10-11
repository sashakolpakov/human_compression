#!/usr/bin/env python3
"""Whole L020 input recount; no ratios, mathematical programs or Lean runs."""
import argparse,json,re,unicodedata
from pathlib import Path
import pypdf,fontTools
from font_tools import need,sha,actual_event_alignment
from pdf_text import extract
from calibration import aliases_from
from graphics_inventory import inventory
HERE=Path(__file__).resolve().parent
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
CATS=['programs','operational_drivers','formal_files']
def load(n):return json.loads((HERE/n).read_text())
def metrics(t,n):
 t=unicodedata.normalize(n,t);c=' '.join(t.split());return dict(whitespace_tokens=len(c.split()),alphanumeric_units=len(re.findall(r'[^\W_]+',t)),characters_without_whitespace=sum(not x.isspace() for x in t),characters_with_collapsed_whitespace=len(c),utf8_bytes_with_collapsed_whitespace=len(c.encode()),normalized_text_sha256=sha(t.encode()),collapsed_text_sha256=sha(c.encode()))
def bound(row,root):
 path=Path(row['path']);need(not path.is_absolute() and '..' not in path.parts,'safe relative input path');p=root/path;b=p.read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'whole bound input '+row['path']);return p,b

def furniture(key,raw,pages):
 out=[]
 for pg in pages:
  n=pg['page'];t=raw[pg['start']:pg['end']]
  if key=='L020' and n>1:
   literal=(f'{n} JULIE DE SAEDELEER, DIMITRI LEEMANS, AND JESSICA MULPAS\n' if n%2==0 else f'RANK AUGMENTATION THEOREM FROM RANK 3 TO RANK 4 {n}\n')
   need(t.startswith(literal),'literal alternating source running header');a=0;b=len(literal)
  else:
   need(t.endswith('\n'+str(n)),'isolated final page number '+key);a=len(t)-len(str(n));b=len(t)
  a+=pg['start'];b+=pg['start'];out.append(dict(page=n,start=a,end=b,literal=raw[a:b],sha256=sha(raw[a:b].encode())))
 return out

def selected(raw,row):
 result=[];last=0
 for f in row['excluded_furniture']:result.append(raw[last:f['start']]);last=f['end']
 result.append(raw[last:]);return '\n'.join(result)

def validate_policy(p):
 need(p['source_ids']==['L020'] and p['original_count']==1 and p['source_dispositions']==19,'one original19 clauses')
 need({k:r['pages'] for k,r in p['documents'].items()}==dict(L020=19,U=5,A1=3,COUNTER=3,CODE=3),'complete five-PDF33page boundary')
 need(p['whole_common']==['U'] and p['written_documents']==['U','A1','COUNTER'] and p['applications']=={'L020':['A1','COUNTER']},'whole common and counterproof application')
 need(p['programme_printed_alternative']==['CODE'] and p['old_two_page_program_appendix']=='replaced, not added','whole new appendix only')
 need(len(p['programs'])==3 and len({r['sha256'] for r in p['programs']})==3 and all(r['whole_file'] for r in p['programs']),'three full unique math/validation programs')
 need([r['logical_role'] for r in p['programs']]==['required_finite_certificates_for_three_source_examples','bounded_validation_not_uniform_premise','transparent_S18_certificate_supporting_complete_written_proof'],'exact distinct program roles')
 need(len(p['operational_drivers'])==3 and len(p['formal_files'])==2 and [r['declarations'] for r in p['formal_files']]==[2,13] and p['formal_declarations']==15,'three drivers/two scoped Lean files')
 need(p['primary_coordinate']==dict(variant='raw_untrimmed',normalization='NFC',unit='characters_without_whitespace'),'raw primary')
 need(p['units']==UNITS and p['normalizations']==['NFC','NFKC'] and p['variants']==['raw_untrimmed','raw_selected','calibrated_selected'],'all thirty coordinates')
 need('complete3page counterproof' in p['conditional_policy'] and 'all three complete' in p['conditional_policy'],'full preacquisition and local boundary')
 need(not p['cross_topic_discount'] and not p['old_Topic_B_common_free_premise'],'no free earlier theory')
 need(not p['factors_permitted'] and p['ratio'] is None and p['new_source_credit']==p['new_question_credit']==0,'inputs only')
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
 need(pypdf.__version__=='6.13.0' and fontTools.__version__=='4.63.0','pinned PDF/font engine')
 scientific={r['path']:bound(r,root)[1] for r in p['scientific_bindings']}
 scope=load('scientific_scope.json');need(scope==json.loads(scientific['topic_B_L020_positive_v2/scope.json']) and len(scope['source_rows'])==19,'all source dispositions unchanged')
 need(load('inherited_formal_scope.json')==json.loads(scientific['topic_B_L020_case_three_formal/scope.json']),'whole inherited formal scope')
 need(load('appendix_bindings.json')==json.loads(scientific['topic_B_L020_complete_programs/bindings.json']),'complete appendix scope')
 spec=load('input_spec.json');need(set(spec)==set(p['documents']),'all PDFs')
 aliases=load('glyph_aliases.json')['aliases'];need(aliases==aliases_from(load('font_audit.json')),'source-specific actual outline rules')
 docs={};audits={};graphs={};cache={}
 for key,row in p['documents'].items():
  need(all(spec[key][k]==v for k,v in row.items()),'same input identity');path,_=bound(row,root);raw,fonts,pages,meta=extract(path,False)
  need(raw=='\n'.join(pg.extract_text() or '' for pg in pypdf.PdfReader(path).pages),'returned text unaltered')
  need(len(pages)==row['pages'] and spec[key]['page_bindings']==pages and spec[key]['extraction_metadata']==meta,'all page/event metadata')
  need(spec[key]['extraction_sha256']==sha(raw.encode()) and spec[key]['included_spans']==[dict(start=0,end=len(raw),sha256=sha(raw.encode()))],'whole title/body/figures/refs')
  need(spec[key]['excluded_furniture']==furniture(key,raw,pages),'only exact furniture')
  if key=='L020':need(raw.count('arXiv:2212.12563v1  [math.GR]  23 Dec 2022')==1,'banner retained once')
  events,audit=actual_event_alignment(path,raw,fonts,pages,type1_math_only=True,generated_newline_offsets=set(meta['generated_newline_offsets']));audits[key]=audit
  if key=='L020':need(not audit['unchanged_type0_dictionaries'],'all source encoded fonts audited')
  else:need(not events and not spec[key]['glyph_substitutions'],'replacement Unicode text unchanged')
  cal=calibrate(raw,fonts,pages,events,spec[key],aliases,key);texts=dict(raw_untrimmed=raw,raw_selected=selected(raw,spec[key]),calibrated_selected=selected(cal,spec[key]))
  docs[key]=dict(pdf_sha256=row['sha256'],pages=row['pages'],furniture_cuts=len(spec[key]['excluded_furniture']),glyph_repairs=len(spec[key]['glyph_substitutions']),metrics={v:{n:metrics(t,n) for n in p['normalizations']} for v,t in texts.items()});graphs[key]=inventory(path,key);cache[key]=dict(raw=raw,fonts=fonts,pages=pages,meta=meta,events=events,texts=texts)
 need(audits==load('font_audit.json'),'all actual font dictionaries/encoded classes/outline evidence')
 need(graphs==load('graphics_inventory.json'),'all vector/image/form evidence preserved')
 rawcounts={};rawprograms={}
 for cat in CATS:
  rawcounts[cat]={}
  for row in p[cat]:
   _,b=bound(row,root);rawcounts[cat][row['path']]=dict(bytes=len(b),sha256=sha(b),metrics={n:metrics(b.decode(),n) for n in p['normalizations']})
   if cat=='programs':rawprograms[Path(row['path']).name]=b.decode()
 tex=scientific['topic_B_L020_complete_programs/programs.tex'].decode();names=re.findall(r'\\VerbatimInput(?:\[[^\]]*\])?\{([^}]+)\}',tex)
 need(names==list(rawprograms) and not re.search(r'firstline|lastline|firstnumber|lastnumber',tex),'all three whole programs included once')
 compact=lambda t:''.join(unicodedata.normalize('NFKC',t).split());printed=compact(cache['CODE']['texts']['raw_selected'])
 for n,t in rawprograms.items():need(printed.count(compact(t))==1,'complete printed file once '+n)
 return dict(status='AUTHOR_INPUT_REPLAY_PASS_PENDING_DISTINCT_REVIEW',originals=1,source_dispositions=19,pdf_documents=5,physical_pages=33,pdf_metric_cells=150,raw_metric_cells=80,documents=docs,raw_files=rawcounts,appendix=dict(whole_files=3,pages=3,whole_raw_bytes=sum(r['bytes'] for r in p['programs']),replaces_old_two_page=True,printed_raw_alternative=True),formal_files=2,formal_declarations=15,source_glyph_classes=528,source_calibrated_classes=2,source_calibrated_occurrences=112,ratio=None,scientific_programs_executed=False,unknown_costs=p['unknown_costs']),cache

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output directory')
 if (HERE/'manifest.json').exists():
  for r in load('manifest.json')['exports']:bound(r,HERE)
 result,_=replay(a.study_root)
 if (HERE/'author_counts.json').exists():need(result==load('author_counts.json'),'exact whole count reproduction')
 a.out.mkdir(parents=True);(a.out/'counts.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('PASS: five PDFs/33 pages;150 PDF +80 raw cells; no factors.')
if __name__=='__main__':main()
