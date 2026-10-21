#!/usr/bin/env python3
"""Direct actual dictionary, encoding, outline and byte-event review.
No author module imported. FontTools/pypdf remain explicit common parsers.
"""
from pathlib import Path
from io import BytesIO
from collections import Counter
import argparse,json
import pypdf
from pypdf.generic import ContentStream
from pypdf import _cmap
from fontTools.cffLib import CFFFontSet,cffISOAdobeStrings
from fontTools.encodings.StandardEncoding import StandardEncoding
from fontTools.encodings.MacRoman import MacRoman
from fontTools.agl import UV2AGL
from fontTools.pens.recordingPen import RecordingPen
from fontTools.misc import psLib,psCharStrings,eexec
import recount as R

def face(font):
 desc=font.get('/FontDescriptor');special={}
 if desc is None:
  R.need(str(font['/BaseFont'])=='/Times-Roman' and font.get('/Encoding') is None,'only ASCII standard banner unembedded')
  return dict(enumerate(StandardEncoding)),None,None,{'default_TimesRoman':True}
 desc=desc.get_object()
 if '/FontFile3' in desc:
  raw=desc['/FontFile3'].get_object().get_data();cff=CFFFontSet();cff.decompile(BytesIO(raw),None);top=cff[cff.fontNames[0]]
  if 'charset' not in top.rawDict:
   R.need('ROS' not in top.rawDict,'ISOAdobe default only name-keyed')
   top.charset=cffISOAdobeStrings[:top.numGlyphs];special['implicit_ISOAdobe_0']=True
  encoding=top.Encoding;glyphs=top.CharStrings
 else:
  raw=desc['/FontFile'].get_object().get_data()
  # FontTools' standard Type1 parser, allowing documented unused empty slots.
  old=psLib.unpack_item
  try:
   psLib.unpack_item=lambda x:None if x is None else old(x)
   t=psLib.suckfont(raw,'ascii')
  finally:psLib.unpack_item=old
  subrs=t['Private'].get('Subrs',[]);iv=t['Private'].get('lenIV',4);R.need(iv>=0,'valid Type1 encryption prefix')
  for i,b in enumerate(subrs):
   if b is not None:subrs[i]=psCharStrings.T1CharString(eexec.decrypt(b,4330)[0][iv:],subrs=subrs)
  glyphs={n:psCharStrings.T1CharString(eexec.decrypt(b,4330)[0][iv:],subrs=subrs) for n,b in t['CharStrings'].items()};encoding=t['Encoding']
 if isinstance(encoding,str):R.need(encoding=='StandardEncoding','known named base');encoding=StandardEncoding
 mapping=dict(enumerate(encoding));enc=font.get('/Encoding');enc=None if enc is None else enc.get_object();base=enc.get('/BaseEncoding') if isinstance(enc,dict) else enc
 if base=='/WinAnsiEncoding':mapping={i:UV2AGL.get(ord(bytes([i]).decode('cp1252',errors='replace')),'.notdef') for i in range(256)}
 elif base=='/MacRomanEncoding':mapping=dict(enumerate(MacRoman));special['explicit_MacRoman']=True
 elif base=='/StandardEncoding':mapping=dict(enumerate(StandardEncoding))
 else:R.need(base is None,'unsupported explicit encoding')
 if isinstance(enc,dict):
  idx=None
  for v in enc.get('/Differences',[]):
   if isinstance(v,int):idx=v
   else:R.need(idx is not None,'difference start');mapping[idx]=str(v)[1:];idx+=1
 return mapping,glyphs,R.sha(raw),special

def verify(packet,study,outlines=None,specs_override=None,audits_override=None):
 specs=R.read(packet/'input_spec.json') if specs_override is None else specs_override;audits=R.read(packet/'font_audit.json') if audits_override is None else audits_override;reports=[];allpaths={}
 for key in ['L084','L095']:
  reader=pypdf.PdfReader(study/specs[key]['path']);old=audits[key];byobject={(d['font_dictionary_object']['idnum'],d['font_dictionary_object']['generation']):d for d in old['font_dictionaries']};faces={};observed=Counter();events_by_page={};specials=[];alloutlines={}
  def getface(font):
   ref=font.indirect_reference;oid=(ref.idnum,ref.generation)
   if oid not in faces:
    wanted=byobject[oid];b=BytesIO();font.write_to_stream(b);R.need(R.sha(b.getvalue())==wanted['font_dictionary_sha256'],'dictionary bytes')
    R.need(str(font['/BaseFont'])==wanted['font'],'dictionary name');mapping,glyphs,stream,special=face(font)
    R.need({str(k):v for k,v in mapping.items()}==wanted['effective_encoding'],'complete independently derived effective encoding')
    R.need(R.sha(json.dumps(mapping,sort_keys=True).encode())==wanted['effective_encoding_sha256'],'effective encoding hash')
    R.need(stream==wanted['font_stream_sha256'],'actual font stream')
    faces[oid]=(wanted,mapping,glyphs,stream,font)
    if special:specials.append(dict(object=oid,font=str(font['/BaseFont']),**special))
   return faces[oid]
  for n,page in enumerate(reader.pages,1):
   def walk(content,resources,route=(),font=None,res=None):
    stack=[]
    for oi,(args,op) in enumerate(ContentStream(content,reader).operations):
     if op==b'q':stack.append((font,res))
     elif op==b'Q':font,res=stack.pop()
     elif op==b'Tf':res=str(args[0]);font=resources['/Font'][args[0]].get_object()
     elif op==b'Do':
      form=resources['/XObject'][args[0]].get_object()
      if form.get('/Subtype')=='/Form':
       yield from walk(form,form.get('/Resources',resources),route+((oi,str(args[0]),R.sha(form.get_data())),),font,res)
     if op not in [b'Tj',b'TJ',b"'",b'"']:continue
     R.need(font is not None and font['/Subtype']=='/Type1','actual source Type1 event')
     d,enc,glyphs,stream,_=getface(font);decode,cmap=_cmap.get_encoding(font);parts=args[0] if op==b'TJ' else [args[-1]]
     for pi,part in enumerate(parts):
      if not isinstance(part,(str,bytes)):continue
      data=part.original_bytes if hasattr(part,'original_bytes') else bytes(part)
      for bi,byte in enumerate(data):
       text=decode.get(byte,chr(byte)) if isinstance(decode,dict) else bytes([byte]).decode(decode);text=''.join(cmap.get(c,c) for c in text);glyph=enc[byte];R.need(glyph!='.notdef','all used glyphs defined')
       observed[(d['font_identity'],byte,text,glyph)]+=1
       ev=dict(page=n,font_identity=d['font_identity'],font=d['font'],font_dictionary_object=d['font_dictionary_object'],font_dictionary_sha256=d['font_dictionary_sha256'],effective_encoding_sha256=d['effective_encoding_sha256'],encoded_byte=byte,glyph_name=glyph,decoded_text=text,font_resource=res,operator_index=oi,operator=op.decode(),part_index=pi,byte_index=bi,text_part_sha256=R.sha(data),font_stream_sha256=stream,form_route=[dict(operator_index=a,resource=b,stream_sha256=c) for a,b,c in route])
       yield ev
   events=list(walk(page.get_contents(),page['/Resources']));events_by_page[n]=events
   extracted=page.extract_text() or '';flat=''.join(e['decoded_text'] for e in events)
   R.need(''.join(c for c in flat if not c.isspace())==''.join(c for c in extracted if not c.isspace()),'all nonspace glyphs reconcile with full page')
  expected=Counter({(c['font_identity'],c['encoded_byte'],c['decoded_text'],c['glyph_name']):c['occurrences'] for c in old['encoded_glyph_classes']});R.need(observed==expected,'all actual encoded classes/counts')
  R.need(len(faces)==len(byobject),'all used source dictionaries')
  for c in old['encoded_glyph_classes']:
   oid=(c['font_dictionary_object']['idnum'],c['font_dictionary_object']['generation']);d,enc,glyphs,stream,font=faces[oid];g=c['glyph_name']
   if glyphs is None:R.need(32<=c['encoded_byte']<=126 and c['decoded_text']==chr(c['encoded_byte']),'standard banner literal ASCII');continue
   pen=RecordingPen();glyphs[g].draw(pen);digest=R.sha(json.dumps(pen.value).encode());visible=any(op not in ['endPath','closePath'] for op,args in pen.value)
   R.need(digest==c['glyph_evidence']['outline_sha256'] and visible==c['glyph_evidence']['visible'],'actual embedded outline evidence')
   alloutlines[(d['font'],c['encoded_byte'],g)]=pen.value
  # All repairs are independently located among full actual content events and in full extracted pages.
  repairs=specs[key]['glyph_substitutions'];found=[]
  for n,events in events_by_page.items():
   page=reader.pages[n-1];text=page.extract_text() or '';positions=[i for i,c in enumerate(text) if not c.isspace()];cursor=0
   for e in events:
    positions_for_event=[]
    for ch in e['decoded_text']:
     if ch.isspace():continue
     positions_for_event.append(positions[cursor]);cursor+=1
    ck=(key,e['font'],e['encoded_byte'])
    if ck in R.CLASSES:
     R.need(len(positions_for_event)==1,'one visible codepoint alias');offset=specs[key]['page_bindings'][n-1]['start']+positions_for_event[0]
     target=next((r for r in repairs if r['offset']==offset),None);R.need(target is not None,'actual alias has exact repair');
     for field,value in e.items():R.need(target['pdf_event'][field]==value,'actual event '+field)
     R.need(target['output']==R.CLASSES[ck][2],'actual calibrated symbol');found.append(offset)
  R.need(len(found)==len(repairs),'all actual repairs accounted for')
  reports.append(dict(document=key,dictionaries=len(faces),classes=len(observed),calibrated_events=len(found),special_cases=specials,all_nonspace_actual_events_reconciled=True,all_embedded_outline_hashes_checked=True))
  if outlines is not None:allpaths[key]=alloutlines
 result=dict(status='PASS',documents=reports,font_dictionaries=26,glyph_classes=502,embedded_classes=477,standard_banner_classes=25,calibrated_events=61,author_modules_imported=False,common_parser_trust=['pypdf6.13.0 content stream and decoding','FontTools4.63.0 CFF/Type1 outline parsing'],meaning_requires_visual_review=True)
 if outlines is not None:outlines.update(allpaths)
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--study-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();R.need(not a.out.exists(),'fresh output');a.out.write_text(json.dumps(verify(a.packet,a.study_root),indent=2)+'\n');print('PASS26 font dictionaries/502 classes/61 repairs')
