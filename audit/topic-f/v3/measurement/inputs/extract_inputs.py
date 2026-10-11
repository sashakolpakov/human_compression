#!/usr/bin/env python3
"""Expanded Topic F input recount; no ratios, mathematical programs or Lean runs."""
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
  n=pg['page'];t=raw[pg['start']:pg['end']];cuts=[]
  if key=='L007':
   first='Accepted manuscript\n';need(t.startswith(first),'literal accepted watermark once');cuts.append((0,len(first)))
   if n>1:
    line=t[len(first):].split('\n',1)[0]+'\n'
    expected=f'{n} Ars Math. Contemp.\n' if n%2==0 else f'T.-T. Konget al.: Chiral 3-polytopes of order 2pm {n}\n'
    need(line==expected,'literal accepted running header');cuts.append((len(first),len(first)+len(line)))
  elif key=='L014' and n>1:
   line=t.split('\n',1)[0]+'\n'
   need((n%2==0 and line.startswith(str(n)+' DONG-DONG HOU,') and line.endswith('QU\n')) or line==f'STRING C-GROUPS OF ORDER 4 pm {n}\n','literal L014 running header');cuts.append((0,len(line)))
  else:
   need(t.endswith('\n'+str(n)),'isolated final page number '+key);cuts.append((len(t)-len(str(n)),len(t)))
  for a,b in cuts:
   a+=pg['start'];b+=pg['start'];out.append(dict(page=n,start=a,end=b,literal=raw[a:b],sha256=sha(raw[a:b].encode())))
 return out

def selected(raw,row):
 result=[];last=0
 for f in row['excluded_furniture']:result.append(raw[last:f['start']]);last=f['end']
 result.append(raw[last:]);return '\n'.join(result)

def validate_policy(p):
 need(p['source_ids']==['L014','L007'] and p['original_count']==2 and p['source_dispositions']==63 and p['inherited_L014_rows']==25 and p['L007_rows']==38,'two full original contracts')
 need({k:r['pages'] for k,r in p['documents'].items()}==dict(L014=12,L007=22,U=7,A1=5,A2=6,CODE=9),'all six PDFs61pages')
 need(p['whole_common']==['U'] and p['written_documents']==['U','A1','A2'] and p['applications']=={'L014':['A1'],'L007':['A2']},'whole common and both applications')
 need(p['programme_printed_alternative']==['CODE'],'whole appendix')
 need(len(p['programs'])==9 and len({r['sha256'] for r in p['programs']})==9 and all(r['whole_file'] and r['logical_role']=='validation_not_uniform_proof_premise' for r in p['programs']),'nine unique full validation programs')
 need(len(p['operational_drivers'])==4 and len(p['formal_files'])==3 and [r['declarations'] for r in p['formal_files']]==[5,4,3] and p['formal_declarations']==12 and p['new_formal_declarations']==3,'four drivers /three scoped Lean files')
 need(all(r['whole_file'] for cat in CATS for r in p[cat]),'all whole raw files')
 need(all(not r['source_specific_instance'] for r in p['formal_files']),'no full source formalization')
 need(p['primary_coordinate']==dict(variant='raw_untrimmed',normalization='NFC',unit='characters_without_whitespace'),'raw primary')
 need(p['units']==UNITS and p['normalizations']==['NFC','NFKC'] and p['variants']==['raw_untrimmed','raw_selected','calibrated_selected'],'all thirty coordinates')
 need('entire U and all nine complete' in p['conditional_policy'] and 'no program is a uniform proof premise' in p['conditional_policy'],'full acquisition')
 need(not p['cross_topic_discount'] and not p['old_Topic_F_common_free_premise'],'no free earlier theory')
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
 for r in load('science_adoption.json')['bindings']:bound(r,root)
 need(load('scientific_scope.json')==json.loads(scientific['topic_F_L007_recovery/volume/scope.json']),'complete reviewed scientific scope')
 spec=load('input_spec.json');need(set(spec)==set(p['documents']),'all PDFs')
 aliases=load('glyph_aliases.json')['aliases'];need(aliases==aliases_from(load('font_audit.json')),'source-specific actual outline rules')
 docs={};audits={};graphs={};cache={}
 for key,row in p['documents'].items():
  need(all(spec[key][k]==v for k,v in row.items()),'same input identity');path,_=bound(row,root);raw,fonts,pages,meta=extract(path,'L007' if key=='L007' else False)
  need(raw=='\n'.join(pg.extract_text() or '' for pg in pypdf.PdfReader(path).pages),'returned text unaltered')
  need(len(pages)==row['pages'] and spec[key]['page_bindings']==pages and spec[key]['extraction_metadata']==meta,'all page/event metadata')
  need(spec[key]['extraction_sha256']==sha(raw.encode()) and spec[key]['included_spans']==[dict(start=0,end=len(raw),sha256=sha(raw.encode()))],'whole title/body/figures/refs')
  need(spec[key]['excluded_furniture']==furniture(key,raw,pages),'only exact furniture')
  if key=='L007':need(raw.count('Accepted manuscript')==22 and len(meta['duplicate_callbacks'])==22,'each watermark retained once')
  if key=='L014':need(raw.count('arXiv:2407.10388v1  [math.GR]  15 Jul 2024')==1,'original arXiv banner retained')
  events,audit=actual_event_alignment(path,raw,fonts,pages,type1_math_only=True,generated_newline_offsets=set(meta['generated_newline_offsets']));audits[key]=audit
  if key in ('L014','L007'):need(not audit['unchanged_type0_dictionaries'],'all source encoded fonts audited')
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
 appendix=check_appendix(scientific['topic_F_L007_recovery/volume/program-appendix.tex'].decode(),rawprograms,cache['CODE'])
 return dict(status='AUTHOR_INPUT_REPLAY_PASS_PENDING_DISTINCT_REVIEW',originals=2,source_dispositions=63,pdf_documents=6,physical_pages=61,pdf_metric_cells=180,raw_metric_cells=160,documents=docs,raw_files=rawcounts,appendix=appendix,formal_files=3,formal_declarations=12,new_formal_declarations=3,source_glyph_classes=sum(len(audits[k]['encoded_glyph_classes']) for k in ('L014','L007')),source_font_dictionaries=sum(len(audits[k]['font_dictionaries']) for k in ('L014','L007')),source_calibrated_classes=len(aliases),source_calibrated_occurrences=sum(r['occurrences'] for r in aliases),ratio=None,scientific_programs_executed=False,unknown_costs=p['unknown_costs']),cache

def check_appendix(tex,rawprograms,cache):
 names=re.findall(r'\\VerbatimInput(?:\[[^\]]*\])?\{([^}]+)\}',tex)
 need(len(names)==9 and set(names)=={'programs/'+n for n in rawprograms} and len(set(names))==9 and not re.search(r'firstline|lastline|firstnumber|lastnumber',tex),'nine complete files printed once')
 # Rendering-only continuation arrows are stripped only for byte-inclusion proof,
 # never for any measured coordinate.
 compact=lambda t:''.join(unicodedata.normalize('NFKC',t).split()).replace('↪','').replace('↩','').replace('⌋','')
 need(all(not any(c in t for c in ['↪','↩','⌋']) for t in rawprograms.values()),'continuation marks absent from all raw files')
 printed=compact(cache['texts']['raw_selected'])
 for n,t in rawprograms.items():need(printed.count(compact(t))==1,'complete printed file once '+n)
 return dict(whole_files=9,pages=9,whole_raw_bytes=sum(len(t.encode()) for t in rawprograms.values()),printed_raw_alternative=True,uniform_finite_premises=0,validation_files=9,rendering_only_removed_for_inclusion=['↪','↩','⌋'],measured_wrap_characters_preserved=True)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output directory')
 if (HERE/'manifest.json').exists():
  for r in load('manifest.json')['exports']:bound(r,HERE)
 result,_=replay(a.study_root)
 if (HERE/'author_counts.json').exists():need(result==load('author_counts.json'),'exact whole count reproduction')
 a.out.mkdir(parents=True);(a.out/'counts.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('PASS: six PDFs/61 pages;180 PDF +160 raw cells; no factors.')
if __name__=='__main__':main()
