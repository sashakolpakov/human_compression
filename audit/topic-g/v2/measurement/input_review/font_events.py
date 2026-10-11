#!/usr/bin/env python3
"""Independent PDF event/encoding audit; no imports from the author packet."""
import hashlib, io, json, collections
from pypdf import PdfReader, _cmap
from pypdf.generic import ContentStream, TextStringObject, ByteStringObject
from fontTools import agl
from fontTools.cffLib import CFFFontSet
from fontTools.misc import psLib, psCharStrings, eexec
from fontTools.encodings.StandardEncoding import StandardEncoding
from fontTools.pens.recordingPen import RecordingPen

def sha(b):return hashlib.sha256(b).hexdigest()
def need(b,s):
    if not b:raise ValueError(s)
def encoded_face(font):
    d=font.get('/FontDescriptor')
    if d is None:
        need(str(font['/BaseFont'])=='/Times-Roman','unembedded font');return None,{32:'space'},None
    d=d.get_object();ref=d.get('/FontFile') or d.get('/FontFile3');data=ref.get_object().get_data()
    if '/FontFile' in d:
        # Retained fontTools interpreter, with null unused slots accepted.
        save=psLib.unpack_item
        def unpack(x):return None if x is None else save(x)
        psLib.unpack_item=unpack
        try:f=psLib.suckfont(data,'ascii')
        finally:psLib.unpack_item=save
        subrs=f['Private'].get('Subrs',[]);skip=f['Private'].get('lenIV',4);need(skip>=0,'Type1 lenIV')
        def decrypt(b):return psCharStrings.T1CharString(eexec.decrypt(b,4330)[0][skip:],subrs=subrs)
        strings={k:decrypt(b) for k,b in f['CharStrings'].items()}
        for i,b in enumerate(subrs):
            if b is not None:subrs[i]=decrypt(b)
        enc=f['Encoding']
    else:
        c=CFFFontSet();c.decompile(io.BytesIO(data),None);f=c[c.fontNames[0]];enc=f.Encoding;strings=f.CharStrings
    if isinstance(enc,str):need(enc=='StandardEncoding','CFF named encoding');enc=StandardEncoding
    mapping=dict(enumerate(enc));override=font.get('/Encoding')
    need(not override or isinstance(override,str) or override.get('/BaseEncoding') is None,'observed dictionary encoding has no BaseEncoding override')
    if isinstance(override,str):
        need(override=='/WinAnsiEncoding','named PDF encoding')
        mapping={i:agl.UV2AGL.get(ord(bytes([i]).decode('cp1252',errors='replace')),'.notdef') for i in range(256)}
    elif override:
        for item in override.get('/Differences',[]):
            if isinstance(item,int):i=item
            else:mapping[i]=str(item).lstrip('/');i+=1
    return sha(data),mapping,strings

def inspect(pdf,texts,fontchars):
    reader=PdfReader(pdf);faces={};classes=collections.Counter();events={};spaces=[];forms=[];allrefs={};offset=0
    def identify(font):
        ref=font.indirect_reference;return (ref.idnum,ref.generation)
    def getface(font):
        fid=identify(font)
        if fid not in faces:
            stream,mapping,strings=encoded_face(font)
            buf=io.BytesIO();font.write_to_stream(buf)
            faces[fid]=(stream,mapping,strings,sha(json.dumps(mapping,sort_keys=True).encode()),sha(buf.getvalue()))
            allrefs[fid]=str(font['/BaseFont'])
        return faces[fid]
    for pn,(page,text,fs) in enumerate(zip(reader.pages,texts,fontchars),1):
        tokens=[]
        def walk(stream,resources,route=(),inherited=None):
            current=inherited;stack=[]
            for oi,(args,op) in enumerate(ContentStream(stream,reader).operations):
                if op==b'q':stack.append(current)
                elif op==b'Q':current=stack.pop()
                elif op==b'Tf':current=(str(args[0]),resources['/Font'][args[0]].get_object())
                elif op==b'Do':
                    x=resources['/XObject'][args[0]].get_object()
                    if x.get('/Subtype')=='/Form':
                        step=dict(operator_index=oi,resource=str(args[0]),stream_sha256=sha(x.get_data()))
                        forms.append(dict(page=pn,route=list(route)+( [step])))
                        walk(x,x.get('/Resources',resources),route+(step,),current)
                if op not in (b'Tj',b'TJ',b"'",b'"'):continue
                need(current is not None,'missing font');resource,font=current;fid=identify(font);name=str(font['/BaseFont'])
                need(font['/Subtype']=='/Type1','one-byte source face')
                streamsha,mapping,strings,encsha,dictsha=getface(font);encoding,cmap=_cmap.get_encoding(font)
                parts=args[0] if op==b'TJ' else [args[-1]]
                for pi,part in enumerate(parts):
                    if not isinstance(part,(TextStringObject,ByteStringObject)):continue
                    raw=part.original_bytes
                    for bi,byte in enumerate(raw):
                        s=encoding.get(byte,chr(byte)) if isinstance(encoding,dict) else bytes([byte]).decode(encoding)
                        s=''.join(cmap.get(c,c) for c in s);need(s,'empty actual glyph')
                        gn=mapping.get(byte);need(gn and gn!='.notdef','visible glyph resolves in actual dictionary')
                        outline=None
                        if strings is not None:
                            pen=RecordingPen();strings[gn].draw(pen);outline=sha(json.dumps(pen.value).encode())
                        classes[fid,name,byte,s,gn,streamsha,encsha,outline]+=1
                        ev=dict(page=pn,form_route=list(route),operator_index=oi,operator=op.decode(),part_index=pi,byte_index=bi,encoded_byte=byte,font_resource=resource,font=name,text_part_sha256=sha(raw),decoded_text=s,decoded_codepoints=[f'U+{ord(c):04X}' for c in s],glyph_name=gn,font_stream_sha256=streamsha)
                        for di,c in enumerate(s):
                            e=dict(ev,decoded_character_index=di)
                            if c.isspace():
                                if strings is not None:need(all(x[0] in ('endPath','closePath') for x in pen.value),'visible glyph decoded as space')
                                else:need(gn=='space','unembedded space')
                                spaces.append(e)
                            else:tokens.append((c,name,e,fid,encsha))
        walk(page.get_contents(),page['/Resources'])
        loc=[i for i,c in enumerate(text) if not c.isspace()];need(len(loc)==len(tokens),'all nonspace characters have exact events')
        for i,(c,name,ev,fid,encsha) in zip(loc,tokens):
            need(text[i]==c and fs[i]==name,'byte vs extraction and font');events[offset+i]=dict(event=ev,font_dictionary=list(fid),effective_encoding_sha256=encsha,font_dictionary_sha256=faces[fid][4])
        offset+=len(text)+1
    rows=[]
    for (fid,name,byte,s,gn,stream,encoding,outline),n in sorted(classes.items()):
        rows.append(dict(font_dictionary=list(fid),font=name,encoded_byte=byte,decoded_text=s,glyph_name=gn,occurrences=n,font_stream_sha256=stream,effective_encoding_sha256=encoding,outline_sha256=outline))
    grouped=collections.defaultdict(set)
    for fid,name in allrefs.items():grouped[name].add(faces[fid][3])
    collisions={name:len(v) for name,v in grouped.items() if len(v)>1}
    return events,dict(font_dictionaries=[dict(font_dictionary=list(fid),font=allrefs[fid],font_stream_sha256=v[0],effective_encoding_sha256=v[3],font_dictionary_sha256=v[4]) for fid,v in sorted(faces.items())],classes=rows,nonspace_characters=len(events),actual_space_events=spaces,forms=forms,distinct_font_dictionaries=len(faces),basefont_encoding_collisions=collisions)
