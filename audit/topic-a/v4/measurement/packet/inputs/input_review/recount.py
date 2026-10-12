#!/usr/bin/env python3
"""Distinct additive L121 recount: own extraction masks, metric loops and PDF event walk.
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

def own_cuts(key,pages):
 cuts=[];at=0
 for n,t in enumerate(pages,1):
  if key=='L121' and n>=2:
   title='TWO F AMILIES OF LOCALLY TOROIDAL REGULAR 4-HYPERTOPES ARISING FROM TOROIDS'
   expected=(str(n)+' FERNANDES, LEEMANS, PIEDADE, AND WEISS\n') if n%2==0 else(title+' '+str(n)+'\n')
   require(t.startswith(expected),'exact independently identified running head');cuts.append((at,at+len(expected)))
  else:
   require(t.endswith('\n'+str(n)),'isolated complete trailing folio');cuts.append((at+len(t)-len(str(n)),at+len(t)))
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
 # Directly inspected actual embedded outlines; no semantics-driven symbol repair.
 if 'MSBM' in font and glyph=='Z':return 'ℤ'
 if 'CMSY' in font:
  if glyph=='U':return '𝒰'
  if glyph=='mapsto':return '⊢' # the tail component, not the separate arrow
 if 'CMEX' in font:
  return {'parenleftbig':'(','parenrightbig':')','parenleftbigg':'(','parenrightbigg':')',
          'braceleftBigg':'{','summationtext':'∑','summationdisplay':'∑',
          'bracketlefttp':'⎡','bracketleftex':'⎢','bracketleftbt':'⎣',
          'bracketrighttp':'⎤','bracketrightex':'⎥','bracketrightbt':'⎦'}.get(glyph,decoded)
 return decoded

def preliminary(packet,root):
 sys.path.insert(0,str(packet));from font_tools import embedded
 docmap=json.loads((packet/'document_map.json').read_text());audit=json.loads((packet/'font_audit.json').read_text());result={}
 for row in docmap['documents']:
  key=row['key'];pdf,b=bound(root,row);reader=pypdf.PdfReader(pdf);pages=[p.extract_text()or''for p in reader.pages];raw='\n'.join(pages)
  events,fonts,uses,unicode_fonts=events_from_pdf(pdf,pages,embedded)
  require(not unicode_fonts,'all new fonts are Type1')
  expected={(r['font_identity'],r['encoded_byte'],r['decoded_text'],r['glyph_name']):r['occurrences']for r in audit[key]['encoded_glyph_classes']}
  require(dict(uses)==expected,'independent encoded class census '+key)
  require(set(fonts)=={r['font_identity']for r in audit[key]['font_dictionaries']},'complete dictionary census')
  from fontTools.pens.recordingPen import RecordingPen
  for r in audit[key]['encoded_glyph_classes']:
   pen=RecordingPen();fonts[r['font_identity']]['strings'][r['glyph_name']].draw(pen)
   require(r['glyph_evidence']==dict(kind='embedded_Type1_outline',visible=any(op not in('endPath','closePath')for op,args in pen.value),outline_sha256=digest(json.dumps(pen.value).encode())),'actual encoded outline')
  for r in audit[key]['font_dictionaries']:
   require(r['font_stream_sha256']==fonts[r['font_identity']]['stream'],'font stream')
   require(r['effective_encoding_sha256']==digest(json.dumps(fonts[r['font_identity']]['mapping'],sort_keys=True).encode()),'effective encoding')
  cuts=own_cuts(key,pages);cal=list(raw);repairs=[]
  for at,(fid,byte,name,j,decoded)in events.items():
   out=representative(fonts[fid]['font'],name,decoded)
   if out!=decoded:
    require(j==0 and len(decoded)==len(out)==1,'one calibrated symbol per actual event');cal[at]=out;repairs.append(dict(offset=at,input=decoded,output=out,font_identity=fid,encoded_byte=byte,glyph_name=name))
  repaired_offsets={r['offset']for r in repairs}
  for at,ch in enumerate(raw):
   if (unicodedata.category(ch)in('Cc','Co')and ch not in '\r\n\t')or ch=='\ufffd':require(at in repaired_offsets,'no unexplained control/private-use glyph')
  texts=dict(raw_untrimmed=raw,raw_selected=apply_mask(raw,cuts),calibrated_selected=apply_mask(''.join(cal),cuts))
  result[key]=dict(pages=len(pages),pdf_sha256=digest(b),raw_text_sha256=digest(raw.encode()),dictionaries=len(fonts),encoded_classes=len(uses),glyph_events=sum(uses.values()),all_nonspace_events_aligned=True,furniture_cuts=cuts,glyph_repairs=repairs,metrics={v:{n:metric(t,n)for n in('NFC','NFKC')}for v,t in texts.items()})
 return dict(status='PASS_PRELIMINARY_INDEPENDENT_AUDIT',documents=result,ratios=None,shared_low_level_font_parser_only=True)

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--packet',type=Path,required=True);a.add_argument('--study-root',type=Path,required=True);a.add_argument('--out',type=Path,required=True);x=a.parse_args()
 require(not x.out.exists(),'fresh output');r=preliminary(x.packet,x.study_root);x.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
