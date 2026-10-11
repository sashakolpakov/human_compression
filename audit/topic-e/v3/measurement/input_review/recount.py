#!/usr/bin/env python3
"""Distinct E recount: own extraction masks, metric loops and PDF event walk.
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
  if k=='L056' or k in ('L079','L021')and n==1:pass
  elif k=='L079' or k=='L043'and n>1:
   first=t.splitlines(keepends=True)[0];clean=first.rstrip('\r\n');require(first.endswith('\n'),'whole header line')
   if k=='L079':expect=f'{n} Ars Mathematica Contemporanea x (xxxx) 1–x'if n%2==0 else f'Ars Mathematica Contemporanea x (xxxx) 1–x {n}'
   else:expect=f'{n} DIMITRI LEEMANS, J ´ER ´EMIE MOERENHOUT, AND EUGENIA O’REILLY-REGUEIRO'if n%2==0 else f'PROJECTIVE LINEAR GROUPS AND CHIRAL POLYTOPES {n}'
   require(clean==expect,'observed running header');cuts.append((at,at+len(first)))
  else:
   require(t.endswith('\n'+str(n)),'isolated trailing folio');cuts.append((at+len(t)-len(str(n)),at+len(t)))
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

def source_events(pdf,page_texts,font_parser):
 reader=pypdf.PdfReader(pdf);fonts={};uses=Counter();out={};offset=0;visible_white=[]
 def identity(f):
  r=f.indirect_reference;obj=dict(idnum=r.idnum,generation=r.generation);buf=BytesIO();f.write_to_stream(buf)
  base=dict(font_dictionary_object=obj,font_dictionary_sha256=digest(buf.getvalue()),pdf_encoding_declaration=plain(f.get('/Encoding')))
  fid=digest(json.dumps(base,sort_keys=True).encode())
  if fid not in fonts:
   stream,mapping,strings=font_parser(f);fonts[fid]=dict(base,font=str(f.get('/BaseFont','')),mapping=mapping,strings=strings,stream=stream)
  return fid
 def walk(reader,content,res,active=None):
  stack=[]
  for operands,op in ContentStream(content,reader).operations:
   if op==b'q':stack.append(active)
   elif op==b'Q':active=stack.pop()
   elif op==b'Tf':active=res['/Font'][operands[0]].get_object()
   elif op==b'Do':
    x=res['/XObject'][operands[0]].get_object()
    if x.get('/Subtype')=='/Form':yield from walk(reader,x,x.get('/Resources',res),active)
   elif op in (b'Tj',b'TJ',b"'",b'"'):
    require(active is not None and active.get('/Subtype')=='/Type1','actual one-byte source font');fid=identity(active);enc,cmap=_cmap.get_encoding(active)
    for part in operands[0]if op==b'TJ'else[operands[-1]]:
     if not isinstance(part,(TextStringObject,ByteStringObject)):continue
     data=part.original_bytes if hasattr(part,'original_bytes')else bytes(part)
     for byte in data:
      raw=enc.get(byte,chr(byte))if isinstance(enc,dict)else bytes([byte]).decode(enc);text=''.join(cmap.get(c,c)for c in raw);name=fonts[fid]['mapping'].get(byte)
      require(name not in (None,'.notdef'),'actual glyph encoding');uses[fid,byte,text,name]+=1
      if text.isspace():
       strings=fonts[fid]['strings']
       if strings is None:visible=name!='space'
       else:
        from fontTools.pens.recordingPen import RecordingPen
        pen=RecordingPen();strings[name].draw(pen);visible=any(k not in ('endPath','closePath')for k,v in pen.value)
       if visible:visible_white.append((fid,byte,text,name))
      for j,ch in enumerate(text):
       if not ch.isspace():yield ch,(fid,byte,name,j,text)
 for n,(pg,t)in enumerate(zip(reader.pages,page_texts),1):
  expected=[(i,ch)for i,ch in enumerate(t)if not ch.isspace()];actual=list(walk(reader,pg.get_contents(),pg['/Resources']))
  require(len(actual)==len(expected),'all nonspace actual source events '+str(n))
  for (ch,event),(i,ch2)in zip(actual,expected):require(ch==ch2,'actual event/extraction equality');out[offset+i]=event
  offset+=len(t)+1
 require(not visible_white,'no unpriced visible whitespace glyphs')
 return out,fonts,uses

def run(packet,root):
 load=lambda n:json.loads((packet/n).read_text());man=load('manifest.json');require(digest((packet/'manifest.json').read_bytes())=='a615c0156be27a671b2a7d1a0d7140c3593e5bbd14fc96a80228e94b365a0b30','author freeze')
 for row in man['exports']:bound(packet,row)
 for row in man['retained_input_bindings']:bound(root,row)
 p=load('policy.json');spec=load('input_spec.json');expected=load('author_counts.json');aliases=load('glyph_aliases.json')['aliases'];audit=load('font_audit.json')
 sys.path.insert(0,str(packet));from font_tools import embedded # reviewed font-byte parser only; no metrics, masks or event-alignment helper.
 counts={};source_audit={};texts={};cells=0;hashes=0
 for key,row in p['documents'].items():
  path,_=bound(root,row);reader=pypdf.PdfReader(path);pages=[pg.extract_text()or''for pg in reader.pages];raw='\n'.join(pages);require(len(pages)==row['pages'],'whole page count');texts[key]=raw
  require(digest(raw.encode())==spec[key]['extraction_sha256'],'full text hash');require(spec[key]['included_spans']==[dict(start=0,end=len(raw),sha256=digest(raw.encode()))],'whole body retained')
  cuts=own_cuts(key,pages);require(cuts==[(c['start'],c['end'])for c in spec[key]['excluded_furniture']],'independent furniture match')
  cal=list(raw)
  if key in p['source_ids']:
   events,fonts,uses=source_events(path,pages,embedded)
   got={(fid,byte,text,name):n for(fid,byte,text,name),n in uses.items()};want={(x['font_identity'],x['encoded_byte'],x['decoded_text'],x['glyph_name']):x['occurrences']for x in audit[key]['encoded_glyph_classes']};require(got==want,'independent encoded class multiplicity')
   require(set(fonts)=={r['font_identity']for r in audit[key]['font_dictionaries']},'independent actual dictionary census')
   amap={(a['font_identity'],a['encoded_byte'],a['glyph_name']):a for a in aliases if a['source']==key};rep=[]
   for i,(fid,byte,name,j,text)in events.items():
    if (fid,byte,name)in amap:
     a=amap[fid,byte,name];require(len(text)==1 and j==0 and text==a['input'],'one actual calibrated glyph');require(len(a['output'])==1,'one observed representation');cal[i]=a['output'];rep.append((i,a['output']))
   require(sorted(rep)==sorted((g['offset'],g['output'])for g in spec[key]['glyph_substitutions']),'all calibrated occurrences independently located')
   source_audit[key]=dict(dictionaries=len(fonts),encoded_classes=len(uses),calibrated_occurrences=len(rep),unembedded=sum(f['stream']is None for f in fonts.values()),visible_whitespace_glyphs=0)
  else:require(not spec[key]['glyph_substitutions'],'literal Unicode replacement')
  variants={'raw_untrimmed':raw,'raw_selected':apply_mask(raw,cuts),'calibrated_selected':apply_mask(''.join(cal),cuts)};counts[key]={}
  for var,t in variants.items():
   counts[key][var]={}
   for normal in ['NFC','NFKC']:
    m=metric(t,normal);require(m==expected['documents'][key]['metrics'][var][normal],key+'/'+var+'/'+normal+' independent cells/hashes');counts[key][var][normal]=m;cells+=5;hashes+=2
 rawcells=0;rawhashes=0
 for cat in ['programs_and_data','operational_drivers','formal_files']:
  for row in p[cat]:
   _,b=bound(root,row)
   for normal in ['NFC','NFKC']:
    require(metric(b.decode(),normal)==expected['raw_files'][cat][row['path']]['metrics'][normal],'whole raw file independent metrics');rawcells+=5;rawhashes+=2
 for doc,roles in [('REQUIRED',{'required finite proof','required certificate data'}),('VALIDATION',{'validation only'})]:
  selected=[r for r in p['programs_and_data']if r['role']in roles];stem=Path(p['documents'][doc]['path']).with_suffix('.tex');tex=(root/stem).read_text();blocks=re.findall(r'\\begin\{CompleteProgram\}\n(.*?)\\end\{CompleteProgram\}',tex,re.S);require(len(blocks)==len(selected),'whole appendix block count');packed=lambda t:''.join(unicodedata.normalize('NFKC',t).split());body=packed(apply_mask(texts[doc],[(x['start'],x['end'])for x in spec[doc]['excluded_furniture']]))
  for row,block in zip(selected,blocks):
   code=bound(root,row)[1].decode();require(block in [code,code+'\n'],'whole exact raw block');require(body.count(packed(code))==1,'whole file printed exactly once')
 require(cells==390 and rawcells==250,'all640 cells');require(sum(v['dictionaries']for v in source_audit.values())==92 and sum(v['encoded_classes']for v in source_audit.values())==2086,'whole source font census')
 return dict(status='PASS_INDEPENDENT_RECOUNT',pdf_cells=cells,raw_cells=rawcells,text_hashes=hashes+rawhashes,source_audit=source_audit,program_appendices_whole=True,shared_low_level_font_parser_only=True,author_metric_selection_calibration_event_helpers_imported=False,scientific_execution=False,ratios_evaluated=False)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--packet',type=Path,required=True);a.add_argument('--study-root',type=Path,required=True);a.add_argument('--out',type=Path,required=True);x=a.parse_args();require(not x.out.exists(),'fresh output');r=run(x.packet,x.study_root);x.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
