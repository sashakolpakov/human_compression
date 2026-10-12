#!/usr/bin/env python3
"""Distinct LCD recount: own extraction masks, metric loops and PDF event walk.
Only the reviewed low-level embedded-font parser is shared and disclosed.
No author metric, furniture, calibration or replay function is imported.
"""
from pathlib import Path
from collections import Counter
from io import BytesIO
import argparse,json,hashlib,unicodedata,re,sys
import pypdf
from pypdf.generic import ContentStream,TextStringObject,ByteStringObject
from pypdf import _cmap

def require(ok,msg):
 if not ok:raise ValueError(msg)
def digest(b):return hashlib.sha256(b).hexdigest()
def metric(t,normal):
 t=unicodedata.normalize(normal,t);words=t.split();c=' '.join(words);runs=0;prior=False;nonspace=0
 for ch in t:
  flag=ch.isalnum()
  if flag and not prior:runs+=1
  prior=flag;nonspace+=not ch.isspace()
 return dict(whitespace_tokens=len(words),alphanumeric_units=runs,characters_without_whitespace=nonspace,characters_with_collapsed_whitespace=len(c),utf8_bytes_with_collapsed_whitespace=len(c.encode('utf-8')),normalized_text_sha256=digest(t.encode()),collapsed_text_sha256=digest(c.encode()))
def bound(root,row):
 rel=Path(row['path']);require(not rel.is_absolute()and'..'not in rel.parts,'relative path');f=root/rel;b=f.read_bytes();require(len(b)==row['bytes']and digest(b)==row['sha256'],'binding '+str(rel));return f,b

def own_cuts(k,pages):
 cuts=[];at=0
 for n,t in enumerate(pages,1):
  if k=='L050':
   if n==1:expect='MATHEMATICAL COMMUNICATIONS 239\n'
   elif n%2==0:expect=f'{n+238} D. Leemans and B. G. Rodrigues\n'
   else:expect=f'Linear codes with complementary duals {n+238}\n'
   require(t.startswith(expect),'journal header');cuts.append((at,at+len(expect)))
  elif k=='F017'and n>1:
   ranges=[(2,2,'2 BACKGROUND AND DEFINITIONS'),(3,5,'3 SPECIAL LCD CODES FROM GRAPHS'),(6,10,'4 UNIFORM SUBSET GRAPHS'),(11,13,'5 STRONGLY REGULAR GRAPHS'),(14,14,'6 OTHER LCD CODES FROM GRAPHS'),(15,15,'7 CONCLUSION'),(16,17,'REFERENCES')]
   label=next(label for lo,hi,label in ranges if lo<=n<=hi);expect=label+' '+str(n)+'\n'
   require(t.startswith(expect),'manuscript header');cuts.append((at,at+len(expect)))
  else:
   stripped=t.rstrip();mark='\n'+str(n);require(stripped.endswith(mark),'isolated trailing folio')
   cuts.append((at+len(stripped)-len(str(n)),at+len(t)))
  at+=len(t)+1
 return cuts

def apply_mask(t,cuts):
 mask=bytearray(b'\1')*len(t)
 for a,b in cuts:
  require(0<=a<b<=len(t),'valid cut');require(all(mask[a:b]),'disjoint cuts');mask[a:b]=bytes(b-a)
 # Every removed run becomes one separator, exactly preserving the declared selection convention.
 out=[];inside=False
 for i,ch in enumerate(t):
  if mask[i]:out.append(ch);inside=False
  elif not inside:out.append('\n');inside=True
 return ''.join(out)

def plain(v):
 v=v.get_object()if hasattr(v,'get_object')else v
 if isinstance(v,dict):return {str(k):plain(w)for k,w in sorted(v.items())}
 if isinstance(v,list):return [plain(w)for w in v]
 return v if v is None or isinstance(v,(bool,int,float))else str(v)

def events_from_pdf(pdf,pages,embedded):
 """Independent full event walk, including literal Type0 Unicode events."""
 reader=pypdf.PdfReader(pdf);fonts={};unicode_fonts={};uses=Counter();out={};offset=0
 def identify(f):
  r=f.indirect_reference;buf=BytesIO();f.write_to_stream(buf)
  base=dict(font_dictionary_object=dict(idnum=r.idnum,generation=r.generation),font_dictionary_sha256=digest(buf.getvalue()),pdf_encoding_declaration=plain(f.get('/Encoding')))
  fid=digest(json.dumps(base,sort_keys=True).encode())
  if f['/Subtype']=='/Type0':
   unicode_fonts[fid]=dict(base,font=str(f.get('/BaseFont','')),subtype='/Type0')
  elif fid not in fonts:
   require(f['/Subtype']=='/Type1','known one-byte font')
   stream,mapping,strings=embedded(f)
   fonts[fid]=dict(base,font=str(f.get('/BaseFont','')),stream=stream,mapping=mapping,strings=strings)
  return fid
 def walk(content,res,active=None):
  stack=[]
  for operands,op in ContentStream(content,reader).operations:
   if op==b'q':stack.append(active)
   elif op==b'Q':active=stack.pop()
   elif op==b'Tf':active=res['/Font'][operands[0]].get_object()
   elif op==b'Do':
    x=res['/XObject'][operands[0]].get_object()
    if x.get('/Subtype')=='/Form':yield from walk(x,x.get('/Resources',res),active)
   elif op in (b'Tj',b'TJ',b"'",b'"'):
    require(active is not None,'selected font');fid=identify(active);enc,cmap=_cmap.get_encoding(active)
    for part in operands[0]if op==b'TJ'else[operands[-1]]:
     if not isinstance(part,(TextStringObject,ByteStringObject)):continue
     data=part.original_bytes if hasattr(part,'original_bytes')else bytes(part)
     if active['/Subtype']=='/Type0':
      require(isinstance(enc,str),'Type0 declared decoder');decoded=data.decode(enc)
      for c in decoded:
       for ch in cmap.get(c,c):
        if not ch.isspace():yield ch,None
      continue
     for byte in data:
      raw=enc.get(byte,chr(byte))if isinstance(enc,dict)else bytes([byte]).decode(enc)
      text=''.join(cmap.get(c,c)for c in raw);name=fonts[fid]['mapping'].get(byte)
      require(name not in(None,'.notdef'),'effective encoding');uses[fid,byte,text,name]+=1
      if text.isspace():
       from fontTools.pens.recordingPen import RecordingPen
       require(fonts[fid]['strings']is not None,'embedded whitespace outline')
       pen=RecordingPen();fonts[fid]['strings'][name].draw(pen)
       require(not any(k not in('endPath','closePath')for k,v in pen.value),'no visible whitespace omitted')
      for j,ch in enumerate(text):
       if not ch.isspace():yield ch,(fid,byte,name,j,text)
 for n,(pg,t)in enumerate(zip(reader.pages,pages),1):
  actual=list(walk(pg.get_contents(),pg['/Resources']));expected=[(i,ch)for i,ch in enumerate(t)if not ch.isspace()]
  require(len(actual)==len(expected),f'whole event cardinality p{n}: {len(actual)} vs {len(expected)}')
  for (ch,event),(i,extractch)in zip(actual,expected):
   require(ch==extractch,f'whole literal event equality p{n} offset{i}: {ch!r}/{extractch!r}')
   if event is not None:out[offset+i]=event
  offset+=len(t)+1
 return out,fonts,uses,unicode_fonts

def representative(font,glyph,decoded):
 """Rules independently transcribed from the visually inspected outlines."""
 script=dict(zip('BDEFGHJOPQS','ℬ𝒟ℰℱ𝒢ℋ𝒥𝒪𝒫𝒬𝒮'))
 if 'CMBSY'in font:return {'D':'𝓓','Q':'𝓠'}.get(glyph,decoded)
 if 'CMSY'in font:return '⊢'if glyph=='mapsto'else script.get(glyph,decoded)
 if 'MSBM'in font:return {'C':'ℂ','F':'𝔽','Q':'ℚ','R':'ℝ'}.get(glyph,decoded)
 if 'CMEX'in font:
  m={'parenleftbig':'(','parenleftbigg':'(','parenrightbig':')','parenrightbigg':')','floorleftbigg':'⌊','floorrightbigg':'⌋','summationtext':'∑','summationdisplay':'∑','producttext':'∏','productdisplay':'∏'}
  return m.get(glyph,decoded)
 if 'CMMIB'in font and glyph=='dotlessj':return 'ȷ'
 return decoded

def run(packet,root):
 load=lambda n:json.loads((packet/n).read_text())
 # During preparation this function can inspect a draft; final check.py pins the freeze.
 p=load('policy.json');spec=load('input_spec.json');wanted=load('author_stage_counts.json');audit=load('font_audit.json');docmap=load('document_map.json')
 sys.path.insert(0,str(packet));from font_tools import embedded
 pdfcells=0;fontstats={};counts={};aliasseen=[]
 for row in docmap['documents']:
  key=row['key'];path,_=bound(root,row);reader=pypdf.PdfReader(path);pages=[pg.extract_text()or''for pg in reader.pages];raw='\n'.join(pages)
  require(len(pages)==row['pages'],'complete pages');require(digest(raw.encode())==spec[key]['extraction_sha256'],'literal full extraction')
  require(spec[key]['included_spans']==[dict(start=0,end=len(raw),sha256=digest(raw.encode()))],'all extracted characters retained')
  require(not spec[key]['excluded_listings'],'no executable listing identified');cuts=own_cuts(key,pages)
  require(cuts==[(c['start'],c['end'])for c in spec[key]['excluded_furniture']],'independent furniture boundary')
  events,fonts,uses,unicode_fonts=events_from_pdf(path,pages,embedded)
  expectuses={(r['font_identity'],r['encoded_byte'],r['decoded_text'],r['glyph_name']):r['occurrences']for r in audit[key]['encoded_glyph_classes']}
  require(dict(uses)==expectuses,'complete independent glyph census')
  from fontTools.pens.recordingPen import RecordingPen
  for r in audit[key]['encoded_glyph_classes']:
   pen=RecordingPen();fonts[r['font_identity']]['strings'][r['glyph_name']].draw(pen)
   require(r['glyph_evidence']==dict(kind='embedded_Type1_outline',visible=any(op not in('endPath','closePath')for op,args in pen.value),outline_sha256=digest(json.dumps(pen.value).encode())),'actual embedded outline evidence')
  require(set(fonts)=={r['font_identity']for r in audit[key]['font_dictionaries']},'actual font dictionaries')
  for r in audit[key]['font_dictionaries']:
   f=fonts[r['font_identity']]
   require(r['font_stream_sha256']==f['stream'],'actual embedded font stream')
   require(r['effective_encoding_sha256']==digest(json.dumps(f['mapping'],sort_keys=True).encode()),'effective byte encoding')
  wantunicode={digest(json.dumps({k:r[k]for k in['font_dictionary_object','font_dictionary_sha256','pdf_encoding_declaration']},sort_keys=True).encode()):{k:r[k]for k in['font_dictionary_object','font_dictionary_sha256','pdf_encoding_declaration','font','subtype']}for r in audit[key]['unchanged_type0_dictionaries']}
  require(unicode_fonts==wantunicode,'literal Unicode dictionary census')
  cal=list(raw);rep=[]
  for at,(fid,byte,name,j,text)in events.items():
   output=representative(fonts[fid]['font'],name,text)
   if output!=text:
    require(j==0 and len(text)==len(output)==1,'one symbol per repaired event');cal[at]=output;rep.append((at,output))
  require(sorted(rep)==[(g['start'],g['output'])for g in spec[key]['glyph_substitutions']],'independently located repairs')
  for g in spec[key]['glyph_substitutions']:
   require(raw[g['start']:g['end']]==g['input'],'literal repair input')
   require(digest(raw[g['context_start']:g['context_end']].encode())==g['context_sha256'],'repair local context')
  for(fid,byte,text,name),count in uses.items():
   output=representative(fonts[fid]['font'],name,text)
   if output!=text:aliasseen.append((key,fid,byte,name,text,count,output))
  texts=dict(raw_untrimmed=raw,raw_selected=apply_mask(raw,cuts),calibrated_selected=apply_mask(''.join(cal),cuts));counts[key]={}
  for var,t in texts.items():
   counts[key][var]={}
   for norm in ['NFC','NFKC']:
    m=metric(t,norm);require(m==wanted['documents'][key]['variants'][var][norm],key+'/'+var+'/'+norm+' exact cells and hashes');counts[key][var][norm]=m;pdfcells+=5
  fontstats[key]=dict(Type1_dictionaries=len(fonts),unchanged_Type0_dictionaries=len(unicode_fonts),glyph_classes=len(uses),repairs=len(rep),all_nonspace_events_independently_aligned=True,visible_whitespace_glyphs=0)
 expectedaliases=[(r['document'],r['font_identity'],r['encoded_byte'],r['glyph_name'],r['decoded_text'],r['occurrences'],r['output'])for r in load('glyph_aliases.json')['aliases']]
 require(sorted(aliasseen)==sorted(expectedaliases),'complete alias inventory')
 boundary=load('whole_file_boundary.json');wc=load('whole_file_counts.json');groups={};rawcells=0
 for row in boundary['files']:
  _,b=bound(root,row);require(row['whole_file'],'whole raw occurrence');groups.setdefault(digest(b),[]).append(row)
 require(len(groups)==102 and len(boundary['files'])==127,'full file counts')
 require({r['sha256']for r in boundary['unique_files']}==set(groups),'exact content deduplication')
 for row in wc['files']:
  _,b=bound(root,row);require(set(row['occurrences'])=={r['path']for r in groups[row['sha256']]},'all duplicate occurrences')
  for norm in['NFC','NFKC']:
   require(metric(b.decode('utf-8'),norm)==row['metrics'][norm],'independent whole raw-file counts');rawcells+=5
 require(rawcells==1020 and pdfcells==150,'all final cells')
 return dict(status='PASS_INDEPENDENT_INPUT_RECOUNT',pdf_cells=pdfcells,raw_unique_cells=rawcells,raw_occurrences=127,unique_raw_contents=102,physical_pages=69,font_audit=fontstats,alias_classes=len(aliasseen),author_arithmetic_masks_calibration_event_helpers_imported=False,shared_low_level_embedded_font_parser=True,scientific_execution=False,ratios_evaluated=False)

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--packet',type=Path,required=True);a.add_argument('--study-root',type=Path,required=True);a.add_argument('--out',type=Path,required=True);x=a.parse_args();require(not x.out.exists(),'fresh output');r=run(x.packet,x.study_root);x.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))

