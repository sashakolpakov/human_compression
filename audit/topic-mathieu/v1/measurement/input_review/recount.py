#!/usr/bin/env python3
"""Independent L073 count/event review. No author helper imports.
Metric and CFF checking structure reuses this reviewer's independent L037 checker.
"""
import argparse,copy,hashlib,io,json,re,unicodedata
from collections import Counter
from pathlib import Path
from pypdf import PdfReader
from fontTools.cffLib import CFFFontSet
from fontTools.pens.recordingPen import RecordingPen
AUTHOR_SHA='bbef6f90211122f5b5db138bfadd8bb1538bd88f1d6dd7b41dd175e268512de2'
PDFS={'L073':('sources/catalogue_L073.pdf',9),'U':('corpus161_L073_modular/common.pdf',2),'A1':('corpus161_L073_modular/mathieu-census.pdf',5),'CLASSES':('corpus161_L073_recovery/class-tables.pdf',10),'ROWS':('corpus161_L073_recovery/source-rows.pdf',9),'CODE':('corpus161_L073_recovery/required-programs.pdf',11)}
# Actual PDF dictionary identities, not font-name cache keys. Fonts checked below.
MAP={35:{68:('D','𝒟'),69:('E','ℰ'),72:('H','ℋ'),79:('O','𝒪')},51:{77:('M','𝔐'),88:('X','𝔛')}}
NAMES={35:'/LFMHLC+CMSY10',51:'/KTQRSA+EUFM10'}
EXPECTED_OCCURRENCES={(35,68):6,(35,69):5,(35,72):9,(35,79):3,(51,77):447,(51,88):2}
CATEGORIES={'programs':7,'required_raw_data':2,'drivers':3,'generated_outputs':10}
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
def need(b,m):
 if not b:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def th(s):return sha(s.encode())
def load(p):return json.loads(p.read_text())
def pin(p):return {'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
def same(a,b,m):need(a==b,m)
def counts(s,n):
 s=unicodedata.normalize(n,s);w=s.split();c=' '.join(w);runs=0;inside=False
 for ch in s:
  if ch.isalnum():
   if not inside:runs+=1
   inside=True
  else:inside=False
 return dict(zip(UNITS,[len(w),runs,sum(not ch.isspace() for ch in s),len(c),len(c.encode())]),normalized_text_sha256=th(s),collapsed_text_sha256=th(c))
def apply(s,changes):
 for a,b,t in sorted(changes,reverse=True):s=s[:a]+t+s[b:]
 return s

def extract(study):
 docs={};texts={};pages={};cuts={}
 for k,(path,np) in PDFS.items():
  pp=[p.extract_text() for p in PdfReader(study/path).pages];need(len(pp)==np,'all pages '+k);body='\n'.join(pp);offset=0;cc=[]
  for i,p in enumerate(pp,1):
   if k=='L073':
    # The journal footer uses variable spacing in raw extraction. Identify the
    # complete last line, then require its collapsed content, not author offsets.
    footer=p.rsplit('\n',1)[-1];need(' '.join(footer.split())==f'the electronic journal of combinatorics 17 (2010), #N4 {i}','literal journal footer')
   else:footer=str(i);need(p.endswith('\n'+footer),'isolated footer '+k)
   a=offset+len(p)-len(footer);b=offset+len(p);cc.append(dict(page=i,start=a,end=b,literal=footer,sha256=th(footer)));offset+=len(p)+1
  docs[k]={'pdf_sha256':sha((study/path).read_bytes()),'pages':np,'furniture_cuts':np,'glyph_repairs':472 if k=='L073' else 0};texts[k]=body;pages[k]=pp;cuts[k]=cc
 return docs,texts,pages,cuts

def glyphs(study,pages):
 r=PdfReader(study/PDFS['L073'][0]);event=[];extracted=[];fonts={};drawings={};offset=0
 for pn,page in enumerate(r.pages,1):
  chunks=[]
  def visitor(t,cm,tm,f,size):chunks.append((t,f))
  same(page.extract_text(visitor_text=visitor),pages[pn-1],'visitor returned text');same(''.join(t for t,f in chunks),pages[pn-1],'visitor unmodified text')
  local=0
  for t,f in chunks:
   ident=getattr(f,'indirect_reference',None);fid=ident.idnum if ident else None
   if fid in MAP:
    need(f['/BaseFont']==NAMES[fid],'dictionary font identity')
    for j,ch in enumerate(t):
     b=ord(ch)
     if b in MAP[fid]:extracted.append(dict(page=pn,page_offset=local+j,start=offset+local+j,end=offset+local+j+1,input=ch,output=MAP[fid][b][1],dictionary=fid))
   local+=len(t)
  current=None;stack=[]
  for oi,(args,op) in enumerate(page.get_contents().operations):
   if op==b'q':stack.append(current)
   elif op==b'Q':current=stack.pop()
   elif op==b'Tf':current=str(args[0])
   if op not in [b'Tj',b'TJ',b"'",b'"']:continue
   f=page['/Resources']['/Font'][current];ident=f.indirect_reference;fid=ident.idnum
   if fid not in MAP:continue
   need(f['/BaseFont']==NAMES[fid],'content dictionary identity')
   enc=f['/Encoding'];dif=[]
   if isinstance(enc,str):need(enc=='/WinAnsiEncoding','base encoding')
   else:need(enc['/BaseEncoding']=='/WinAnsiEncoding','base encoding');dif=enc.get('/Differences',[])
   emap={i:chr(i) for i in range(65,91)};at=None
   for x in dif:
    if isinstance(x,int):at=x
    else:emap[at]=str(x)[1:];at+=1
   tu=f['/ToUnicode'].get_data().decode() if '/ToUnicode' in f else ''
   # Relevant ASCII letters are not remapped by this font's ToUnicode CMap.
   for b in MAP[fid]:
    need(emap[b]==chr(b),'effective ASCII encoding at calibrated byte')
    for block in re.findall(r'beginbf(?:char|range)(.*?)endbf(?:char|range)',tu,re.S):
     for line in block.splitlines():
      hx=re.findall(r'<([0-9A-Fa-f]+)>',line)
      if len(hx)==2 and int(hx[0],16)==b:need(bytes.fromhex(hx[1]).decode('utf-16-be')==chr(b),'calibrated ToUnicode letter')
      if len(hx)==3 and int(hx[0],16)<=b<=int(hx[1],16):need(int(hx[2],16)+b-int(hx[0],16)==b,'calibrated ToUnicode range')
   stream=f['/FontDescriptor']['/FontFile3'].get_data()
   if fid not in fonts:
    fonts[fid]={'font':str(f['/BaseFont']),'dictionary':fid,'encoding':str(enc) if isinstance(enc,str) else {'base':str(enc['/BaseEncoding']),'differences':list(dif)},'to_unicode_present':bool(tu),'to_unicode_sha256':th(tu) if tu else None,'font_stream_sha256':sha(stream)}
    cff=CFFFontSet();cff.decompile(io.BytesIO(stream),None);cs=cff[cff.fontNames[0]].CharStrings;drawings[fid]={}
    for b,(gn,out) in MAP[fid].items():
     pen=RecordingPen();cs[gn].draw(pen);need(bool(pen.value),'visible CFF outline');drawings[fid][b]={'glyph':gn,'output':out,'drawing':pen.value,'drawing_sha256':th(json.dumps(pen.value,separators=(',',':')))}
   parts=args[0] if op==b'TJ' else [args[-1]]
   for pi,part in enumerate(parts):
    if not isinstance(part,(str,bytes)):continue
    raw=part.original_bytes if hasattr(part,'original_bytes') else bytes(part)
    for bi,b in enumerate(raw):
     if b in MAP[fid]:
      event.append(dict(page=pn,operator_index=oi,operator=op.decode(),part_index=pi,byte_index=bi,encoded_byte=b,font_resource=current,font_dictionary_object={'idnum':fid,'generation':ident.generation},text_part_sha256=sha(raw),glyph_name=emap[b],font_stream_sha256=sha(stream),input=chr(b),output=MAP[fid][b][1]))
  offset+=len(pages[pn-1])+1
 need(len(event)==len(extracted)==472,'all calibration occurrences')
 for e,x in zip(event,extracted):
  need(e['page']==x['page'] and e['input']==x['input'] and e['font_dictionary_object']['idnum']==x['dictionary'],'byte-to-extraction alignment');e.update({k:v for k,v in x.items() if k!='dictionary'})
 same(Counter((e['font_dictionary_object']['idnum'],e['encoded_byte']) for e in event),Counter(EXPECTED_OCCURRENCES),'six actual glyph multiplicities')
 return event,fonts,drawings

def boundary(p,b):
 same(p['primary'],'raw_untrimmed NFC characters_without_whitespace; all complete physical pages including titles, table wrappers, references and furniture','exact primary convention')
 need(p['source_clauses']==14 and p['physical_source_rows']==431 and p['rank_two_classes']==81 and p['rank_three_classes']==431,'scientific scope')
 need(p['replacement_complete_pages']==37 and p['pdf_pages']==46 and p['source_primary_complete_pages']==9,'whole extent')
 need(p['whole_common_paper_charged'] and p['old_monolithic_document_is_predecessor_only'] and p['no_old_umbrella_or_other_application_premise'] and p['no_L095_special_group_theorem'] and not p['cross_topic_discount'],'no free proof crossing')
 same(b['written']['replacement_documents'],['U','A1','CLASSES','ROWS'],'complete written output')
 same(b['conditional']['application_documents'],['A1','CLASSES','ROWS'],'full conditional application')
 same(b['conditional']['prepaid_common_documents'],['U'],'full prepaid common')
 paths=lambda cat:[r['path'] for r in p[cat]]
 same(b['computation_printed']['replacement_documents'],['U','A1','CLASSES','ROWS','CODE'],'whole printed alternative')
 same(b['computation_printed']['required_raw_files'],paths('required_raw_data'),'mandatory raw JSON with printed code')
 same(b['computation_raw']['required_raw_files'],paths('programs')+paths('required_raw_data'),'all raw programs and JSON')
 same(b['conditional']['additional_prepaid_raw_data'],paths('required_raw_data'),'conditional raw data')
 same(b['conditional']['prepaid_program_representation_alternatives'],{'printed':['CODE'],'raw':paths('programs')},'whole alternative acquisition')
 need(sum(r['bytes'] for r in p['required_raw_data'])==83965,'both mandatory JSON byte costs')
 need(all(len(p[c])==n for c,n in CATEGORIES.items()),'whole raw categories')
 need(p['formal']==[] and p['formal_declarations']==0,'no formal claim')
 need(all(x is None for x in p['unknown_costs'].values()) and p['ratio'] is None and not p['factors_permitted'],'unknown not zero and no factors')


def main(study,author,out):
 need(not out.exists() and not out.is_symlink(),'fresh output');out.mkdir(parents=True)
 need(sha((author/'manifest.json').read_bytes())==AUTHOR_SHA,'exact author freeze')
 man=load(author/'manifest.json')
 for e in man['exports']:same(pin(author/e['path']),{k:e[k] for k in ['bytes','sha256']},'unchanged author export')
 spec=load(author/'input_spec.json');policy=load(author/'policy.json');a=load(author/'author_counts.json');b=load(author/'accounting_boundary.json');boundary(policy,b)
 for bind in policy['scientific_bindings']:same(pin(study/bind['path']),{k:bind[k] for k in ['bytes','sha256']},'scientific binding')
 docs,texts,pages,cuts=extract(study);event,fonts,drawings=glyphs(study,pages['L073'])
 for k in PDFS:
  same(pin(study/PDFS[k][0]),{x:spec[k][x] for x in ['bytes','sha256']},'PDF bytes')
  same(cuts[k],spec[k]['excluded_furniture'],'independent exact furniture '+k)
  same(spec[k]['included_spans'],[{'start':0,'end':len(texts[k]),'sha256':th(texts[k])}],'complete included PDF '+k)
  off=0
  for i,(page,r) in enumerate(zip(pages[k],spec[k]['page_bindings']),1):need(r['page']==i and r['start']==off and r['end']==off+len(page) and r['sha256']==th(page),'page binding');off+=len(page)+1
  furniture=[(x['start'],x['end'],'\n') for x in cuts[k]];rep=[(e['start'],e['end'],e['output']) for e in event] if k=='L073' else []
  variants={'raw_untrimmed':texts[k],'raw_selected':apply(texts[k],furniture),'calibrated_selected':apply(texts[k],furniture+rep)}
  docs[k]['metrics']={v:{n:counts(t,n) for n in ['NFC','NFKC']} for v,t in variants.items()};same(docs[k],a['documents'][k],'all metrics/hash '+k)
 for e,r in zip(event,spec['L073']['glyph_substitutions']):
  for k in ['page','page_offset','start','end','input','output']:same(e[k],r[k],'calibration occurrence '+k)
  for k in ['operator_index','operator','part_index','byte_index','encoded_byte','font_resource','font_dictionary_object','text_part_sha256','glyph_name','font_stream_sha256']:same(e[k],r['pdf_events'][0][k],'actual encoded event '+k)
  need(th(texts['L073'][r['context_start']:r['context_end']])==r['context_sha256'],'bound context')
 need(len(spec['L073']['glyph_substitutions'])==472,'exact calibration cardinality')
 raw={}
 for cat,rows in a['raw_files'].items():
  same(set(rows),set(r['path'] for r in policy[cat]),'whole raw paths '+cat);raw[cat]={}
  for path,record in rows.items():
   p=study/path;same(pin(p),{k:record[k] for k in ['bytes','sha256']},'whole raw pin');m={n:counts(p.read_text(),n) for n in ['NFC','NFKC']};same(m,record['metrics'],'whole raw metrics and hashes');raw[cat][path]={'bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'metrics':m}
 tex=(study/'corpus161_L073_recovery/required-programs.tex').read_text();actual=re.findall(r'\\VerbatimInput(?:\[[^\]]*\])?\{([^}]+)\}',tex)
 same(actual,[str(Path(r['path']).relative_to('corpus161_L073_recovery')) for r in policy['programs']],'seven complete printed programs')
 need('firstline' not in tex and 'lastline' not in tex,'no program line pruning')
 compact=lambda t:''.join(unicodedata.normalize('NFKC',t).split())
 full_printed=compact(apply(texts['CODE'],[(x['start'],x['end'],'\n') for x in cuts['CODE']]))
 for r in policy['programs']:need(compact((study/r['path']).read_text()) in full_printed,'every printable program character included '+r['path'])
 correction=load(author/'prior_visual_receipt_correction.json');need('29' in correction['old'] and '30' in correction['corrected'] and correction['scientific_or_metric_change'] is False,'receipt-only correction');same(pin(study/correction['frozen_receipt']['path']),{k:correction['frozen_receipt'][k] for k in ['bytes','sha256']},'old receipt unchanged')
 need(docs['CLASSES']['pages']+docs['ROWS']['pages']+docs['CODE']['pages']==30,'correct unchanged page arithmetic')
 controls=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError):controls.append(name);return
  raise ValueError('control failed '+name)
 def bad_boundary(name,mut):
  pp=copy.deepcopy(policy);bb=copy.deepcopy(b);mut(pp,bb);reject(name,lambda:boundary(pp,bb))
 bad_boundary('drop class tables from written output',lambda p,b:b['written']['replacement_documents'].remove('CLASSES'))
 bad_boundary('conditional application body only',lambda p,b:b['conditional'].__setitem__('application_documents',['A1']))
 bad_boundary('omit raw data in printed route',lambda p,b:b['computation_printed'].__setitem__('required_raw_files',[]))
 bad_boundary('prune one raw program',lambda p,b:b['computation_raw']['required_raw_files'].pop(0))
 bad_boundary('omit conditional data acquisition',lambda p,b:b['conditional'].__setitem__('additional_prepaid_raw_data',[]))
 bad_boundary('free old common proof',lambda p,b:p.__setitem__('cross_topic_discount',True))
 bad_boundary('unknown catalogue cost zero',lambda p,b:p['unknown_costs'].__setitem__('full_catalogue_construction_and_algorithm_proofs',0))
 bad_boundary('invent formal declarations',lambda p,b:p.__setitem__('formal_declarations',1))
 bad_boundary('wrong whole page count',lambda p,b:p.__setitem__('pdf_pages',45))
 bad_boundary('omit output inventory',lambda p,b:p['generated_outputs'].pop())
 bad_boundary('invent factor',lambda p,b:p.__setitem__('ratio',1))
 bad_boundary('silently change primary convention',lambda p,b:p.__setitem__('primary','calibrated_selected NFC characters_without_whitespace'))
 reject('application reference page omitted',lambda:same(counts('\n'.join(pages['A1'][:-1]),'NFC'),docs['A1']['metrics']['raw_untrimmed']['NFC'],'lost reference page'))
 reject('source final table and references omitted',lambda:same(counts('\n'.join(pages['L073'][:-1]),'NFC'),docs['L073']['metrics']['raw_untrimmed']['NFC'],'lost final source page'))
 reject('raw primary silently selected',lambda:same(docs['L073']['metrics']['raw_untrimmed'],docs['L073']['metrics']['raw_selected'],'changed raw primary'))
 reject('omit all 472 visible typeface repairs',lambda:same(docs['L073']['metrics']['raw_selected'],docs['L073']['metrics']['calibrated_selected'],'uncalibrated'))
 reject('script H changed to plain H',lambda:same(event[0]['output'],'H','wrong visible font'))
 reject('wrong actual dictionary at first occurrence',lambda:same(event[0]['font_dictionary_object'],{'idnum':51,'generation':0},'wrong dictionary'))
 reject('wrong actual encoded byte',lambda:same(event[0]['encoded_byte'],79,'wrong encoded byte'))
 firstpath=policy['required_raw_data'][0]['path'];reject('trim historical JSON metadata',lambda:same(counts((study/firstpath).read_text()[:1000],'NFC'),raw['required_raw_data'][firstpath]['metrics']['NFC'],'whole raw JSON lost'))
 result={'status':'PASS','author_manifest_sha256':AUTHOR_SHA,'independent_pdf_cells':180,'independent_raw_cells':220,'normalized_and_collapsed_text_hashes_compared':160,'input_pages':46,'calibrated_occurrences':472,'actual_glyph_classes':6,'document_counts':docs,'raw_counts':raw,'furniture':cuts,'actual_calibration_events':event,'actual_fonts':fonts,'outlines':{str(fid):{str(byte):{k:v for k,v in d.items() if k!='drawing'} for byte,d in rr.items()} for fid,rr in drawings.items()},'complete_printed_programs':7,'mandatory_data_bytes':83965,'unchanged_table_code_pages':30,'negative_controls':controls,'author_helpers_imported':False,'GAP_or_science_replayed':False,'factors_computed':False}
 (out/'recount.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 # Optional local inspection data is intentionally not exported by the review.
 (out/'outline_drawings_private.json').write_text(json.dumps(drawings,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:result[k] for k in ['status','independent_pdf_cells','independent_raw_cells','normalized_and_collapsed_text_hashes_compared','input_pages','calibrated_occurrences','complete_printed_programs','mandatory_data_bytes']}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);p.add_argument('--author',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();s=a.study_root.resolve();main(s,a.author.resolve() if a.author else s/'topic_L073_measurement_inputs',a.out)
