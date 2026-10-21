"""Actual PDF font/event audit reused from the accepted Chamber input extractor.
No costs or mathematical results are inferred by these helpers.
"""
import hashlib,json,unicodedata
from pathlib import Path
from io import BytesIO
from collections import Counter
import pypdf
from pypdf import _cmap
from pypdf.generic import ContentStream,TextStringObject,ByteStringObject
from fontTools import t1Lib
from fontTools.cffLib import CFFFontSet
from fontTools.pens.recordingPen import RecordingPen

def need(ok,message):
    if not ok:raise ValueError('ADDITIONAL_INPUT_REJECT: '+message)
def sha(data):return hashlib.sha256(data).hexdigest()

def read_type1(data):
    """Read literal Type1 bytes, allowing absent unused Subrs/array slots.

    Some 2005 subset fonts omit Subrs altogether or leave unused Encoding
    entries as PostScript nulls. The standard FontTools convenience parser
    assumes both structures are populated. No used glyph is substituted.
    """
    from fontTools.misc import psLib,psCharStrings,eexec
    original=psLib.unpack_item
    def sparse(item):
        return None if item is None else original(item)
    try:
        psLib.unpack_item=sparse
        face=psLib.suckfont(data,'ascii')
    finally: psLib.unpack_item=original
    subrs=face['Private'].get('Subrs',[]);lenIV=face['Private'].get('lenIV',4)
    need(lenIV>=0,'nonnegative Type1 lenIV')
    for name,raw in face['CharStrings'].items():
        clear,_=eexec.decrypt(raw,4330)
        face['CharStrings'][name]=psCharStrings.T1CharString(clear[lenIV:],subrs=subrs)
    for i,raw in enumerate(subrs):
        if raw is not None:
            clear,_=eexec.decrypt(raw,4330);subrs[i]=psCharStrings.T1CharString(clear[lenIV:],subrs=subrs)
    return face


def embedded(font):
    """Read the actual Type1 program, with the PDF's encoding differences."""
    if font.get('/Subtype') == '/Type3':
        encoding=font['/Encoding'].get_object();mapping={};index=0
        for item in encoding['/Differences']:
            if isinstance(item,int):index=item
            else:mapping[index]=str(item).lstrip('/');index+=1
        strings={str(k).lstrip('/'):dict(type3_character_program=v.get_object().get_data()) for k,v in font['/CharProcs'].items()}
        return None,mapping,strings
    need(font.get('/Subtype') == '/Type1', 'one-byte source Type1 or literal Type3 font')
    descriptor=font.get('/FontDescriptor')
    if descriptor is None:
        need(str(font['/BaseFont']) == '/Times-Roman' and font.get('/Encoding') in (None,'/WinAnsiEncoding'),
             'only standard Times-Roman with default or explicit WinAnsi encoding is unembedded')
        if font.get('/Encoding') is None:
            from fontTools.encodings.StandardEncoding import StandardEncoding
            return None,dict(enumerate(StandardEncoding)),None
        from fontTools.agl import UV2AGL
        return None, {i:UV2AGL.get(ord(bytes([i]).decode('cp1252',errors='replace')),'.notdef') for i in range(256)}, None
    descriptor=descriptor.get_object()
    need('/FontFile' in descriptor or '/FontFile3' in descriptor, 'embedded source font program')
    if '/FontFile' in descriptor:
        data=descriptor['/FontFile'].get_object().get_data()
        face=read_type1(data)
        encoding,strings=face['Encoding'],face['CharStrings']
    else:
        data=descriptor['/FontFile3'].get_object().get_data()
        face=CFFFontSet();face.decompile(BytesIO(data),None)
        top=face[face.fontNames[0]]
        if 'charset' not in top.rawDict:
            # CFF's omitted charset operator has the specified default 0
            # (ISOAdobe). FontTools does not materialize this implicit default.
            from fontTools.cffLib import CharsetConverter
            need('ROS' not in top.rawDict and 'CharStrings' in top.rawDict,
                 'implicit ISOAdobe charset only for a name-keyed CFF font')
            top.charset=CharsetConverter()._read(top,0)
        encoding,strings=top.Encoding,top.CharStrings
    if isinstance(encoding,str):
        need(encoding=='StandardEncoding','known CFF named encoding')
        from fontTools.encodings.StandardEncoding import StandardEncoding
        encoding=StandardEncoding
    mapping=dict(enumerate(encoding))
    override=font.get('/Encoding')
    if override is not None: override=override.get_object()
    base_override = override.get('/BaseEncoding') if override and not isinstance(override,str) else override
    if base_override == '/StandardEncoding':
        from fontTools.encodings.StandardEncoding import StandardEncoding
        mapping=dict(enumerate(StandardEncoding))
    elif base_override == '/MacRomanEncoding':
        from fontTools.encodings.MacRoman import MacRoman
        mapping=dict(enumerate(MacRoman))
    elif base_override is not None and base_override != '/WinAnsiEncoding':
        raise ValueError('Unsupported explicit BaseEncoding '+str(base_override))
    if base_override == '/WinAnsiEncoding':
        from fontTools.agl import UV2AGL
        mapping={i:UV2AGL.get(ord(bytes([i]).decode('cp1252',errors='replace')),'.notdef') for i in range(256)}
    if override and not isinstance(override,str):
        for item in override.get('/Differences',[]):
            if isinstance(item,int): index=item
            else: mapping[index]=str(item).lstrip('/'); index+=1
    return sha(data),mapping,strings


def glyph_evidence(strings,glyph):
    if strings is None:
        return dict(kind='unembedded_standard_glyph',visible=glyph!='space',outline_sha256=None)
    obj=strings[glyph]
    if isinstance(obj,dict) and 'type3_character_program' in obj:
        b=obj['type3_character_program']
        need(b'BI' in b and b'/IM true' in b and b'/W 38' in b and b'/H 38' in b,'literal Type3 bitmap glyph format')
        return dict(kind='Type3_image_mask_character_program',visible=True,character_program_sha256=sha(b),character_program_bytes=len(b),bitmap_dimensions=[38,38],image_mask=True,outline_sha256=None)
    pen=RecordingPen();obj.draw(pen)
    return dict(kind='embedded_Type1_outline',visible=any(op not in ('endPath','closePath') for op,args in pen.value),outline_sha256=sha(json.dumps(pen.value).encode()))


def font_identity(font):
    """Bind the actual PDF dictionary separately from its shared embedded stream."""
    data=BytesIO();font.write_to_stream(data)
    ref=getattr(font,'indirect_reference',None)
    object_id=None if ref is None else dict(idnum=ref.idnum,generation=ref.generation)
    declaration=font.get('/Encoding')
    if declaration is not None: declaration=declaration.get_object()
    def plain(value):
        value=value.get_object() if hasattr(value,'get_object') else value
        if isinstance(value,dict):return {str(k):plain(v) for k,v in sorted(value.items())}
        if isinstance(value,list):return [plain(v) for v in value]
        if value is None or isinstance(value,(bool,int,float)):return value
        return str(value)
    info=dict(font_dictionary_object=object_id,font_dictionary_sha256=sha(data.getvalue()),
              pdf_encoding_declaration=plain(declaration))
    return sha(json.dumps(info,sort_keys=True).encode()),info


def actual_event_alignment(path, raw, fonts, pages, type1_math_only=False, generated_newline_offsets=()):
    """Replay actual Type1 glyph events keyed by PDF dictionary, not BaseFont.

    Identically named fonts can have different PDF Encoding/Differences. The
    cache key binds the actual dictionary/object. Shared font-program streams
    remain separately identified; they never merge effective encodings.
    """
    reader=pypdf.PdfReader(path);result={};faces={};identities={};uses=Counter();spaces=[];page_data=[];forms=[];skipped={}
    for pno,page in enumerate(reader.pages,1):
        pb=pages[pno-1];cursor=0
        def stream_events(content,resources,route,initial_font=None,initial_resource=None):
            font=initial_font;resource=initial_resource;stack=[]
            for oi,(operands,op) in enumerate(ContentStream(content,reader).operations):
                if op==b'q': stack.append((font,resource))
                elif op==b'Q': font,resource=stack.pop()
                elif op==b'Tf':
                    resource=str(operands[0]);font=resources['/Font'][operands[0]].get_object()
                elif op==b'Do':
                    name=operands[0];obj=resources['/XObject'][name].get_object()
                    if obj.get('/Subtype')=='/Form':
                        subroute=route+[dict(operator_index=oi,resource=str(name),stream_sha256=sha(obj.get_data()))]
                        forms.append(dict(page=pno,route=subroute))
                        yield from stream_events(obj,obj.get('/Resources',resources),subroute,font,resource)
                if op not in (b'Tj',b'TJ',b"'",b'"'): continue
                need(font is not None,'actual font selected')
                if font.get('/Subtype') not in ('/Type1','/Type3'):
                    need(type1_math_only and font.get('/Subtype')=='/Type0','source Type1/Type3 or explicitly excluded replacement Type0 text')
                    fid,identity=font_identity(font)
                    skipped[fid]=dict(identity,font=str(font.get('/BaseFont','')),subtype='/Type0',scope='Unchanged replacement Unicode text; not a Type1 outline claim. Complete pages separately visually reviewed.')
                    continue
                name=str(font.get('/BaseFont',font.get('/Name','')));fid,identity=font_identity(font)
                if fid not in faces:
                    faces[fid]=embedded(font)
                    effective=faces[fid][1]
                    identities[fid]=dict(identity,font=name,pdf_subtype=str(font['/Subtype']),effective_encoding_sha256=sha(json.dumps(effective,sort_keys=True).encode()),
                        effective_encoding={str(k):v for k,v in sorted(effective.items())})
                stream,mapping,strings=faces[fid];encoding,cmap=_cmap.get_encoding(font)
                parts=operands[0] if op==b'TJ' else [operands[-1]]
                for pi,part in enumerate(parts):
                    if not isinstance(part,(TextStringObject,ByteStringObject)): continue
                    data=part.original_bytes if hasattr(part,'original_bytes') else bytes(part)
                    for bi,byte in enumerate(data):
                        decoded=encoding.get(byte,chr(byte)) if isinstance(encoding,dict) else bytes([byte]).decode(encoding)
                        decoded=''.join(cmap.get(c,c) for c in decoded)
                        need(bool(decoded),'nonempty decoded glyph text')
                        glyph=mapping.get(byte,'standard_'+decoded if stream is None else '')
                        need(bool(glyph) and glyph!='.notdef','actual embedded encoding resolves every used glyph')
                        event=dict(page=pno,form_route=route,operator_index=oi,operator=op.decode('ascii'),part_index=pi,
                            byte_index=bi,encoded_byte=byte,font_resource=resource,font=name,
                            font_identity=fid,**{k:v for k,v in identities[fid].items() if k not in ('font','effective_encoding','pdf_encoding_declaration')},
                            text_part_sha256=sha(data),decoded_text=decoded,decoded_codepoints=[f'U+{ord(c):04X}' for c in decoded],glyph_name=glyph,
                            font_stream_sha256=stream)
                        uses[fid,byte,decoded,glyph]+=1
                        for di,c in enumerate(decoded):
                            yield c,dict(event,decoded_character_index=di)
        actual=list(stream_events(page.get_contents(),page['/Resources'],[]))
        visible_spaces=set()
        for decoded,event in actual:
            if not decoded.isspace():continue
            _,_,strings=faces[event['font_identity']]
            evidence=glyph_evidence(strings,event['glyph_name'])
            spaces.append(dict(event,visible_outline=evidence['visible'],glyph_evidence=evidence))
            if evidence['visible']:visible_spaces.add((decoded,event['font']))
        audited_names={v['font'] for v in identities.values()}
        need(not audited_names.intersection(v['font'] for v in skipped.values()),'no Type0/Type1 name collision')
        need(all(raw[i]=='\n' for i in generated_newline_offsets),'only generated newline offsets excluded from glyph alignment')
        offsets=[i for i in range(pb['start'],pb['end']) if i not in generated_newline_offsets and (not type1_math_only or fonts[i] in audited_names) and (not raw[i].isspace() or (raw[i],fonts[i]) in visible_spaces)]
        for decoded,event in actual:
            name=event['font'];stream,mapping,strings=faces[event['font_identity']]
            if decoded.isspace() and not glyph_evidence(strings,event['glyph_name'])['visible']:continue
            need(cursor<len(offsets),'no excess actual glyphs')
            at=offsets[cursor]
            need(raw[at]==decoded and fonts[at]==name,f'actual byte/font versus extraction page{pno} offset{at}: {repr(decoded)} vs {repr(raw[at])}')
            result[at]=event;cursor+=1
        need(cursor==len(offsets),'every nonspace extracted source glyph has an original event')
        page_data.append(dict(page=pno,aligned_characters=cursor))
    classes=[]
    for (fid,byte,c,glyph),count in sorted(uses.items()):
        stream,mapping,strings=faces[fid];evidence=glyph_evidence(strings,glyph)
        classes.append(dict(font=identities[fid]['font'],font_identity=fid,
            font_dictionary_object=identities[fid]['font_dictionary_object'],font_dictionary_sha256=identities[fid]['font_dictionary_sha256'],
            effective_encoding_sha256=identities[fid]['effective_encoding_sha256'],encoded_byte=byte,decoded_text=c,
            decoded_codepoints=[f'U+{ord(d):04X}' for d in c],glyph_name=glyph,
            occurrences=count,font_stream_sha256=stream,glyph_evidence=evidence))
    audit=dict(all_nonspace_source_characters_aligned=not type1_math_only,all_audited_type1_type3_characters_aligned=True,replacement_type1_math_only=type1_math_only,unchanged_type0_dictionaries=list(skipped.values()),pages=page_data,
        actual_space_events=spaces,space_policy='All actual visible whitespace-decoded glyphs are aligned and counted with exact source byte/dictionary evidence; empty-outline spaces and generated whitespace remain unchanged. Ambiguous alignment fails closed.',
        form_xobjects_visited=forms,
        font_dictionaries=[dict(font_identity=fid,**info,font_stream_sha256=faces[fid][0]) for fid,info in sorted(identities.items())],
        font_streams=[dict(sha256=s,embedded=s is not None,dictionary_identities=sorted(fid for fid in faces if faces[fid][0]==s)) for s in sorted({f[0] for f in faces.values()},key=lambda x:x or '')],
        encoded_glyph_classes=classes,cache_key='actual PDF dictionary object plus dictionary bytes; effective encoding hash bound separately',primary_font_bytes_exported=False,font_stream_scope='font_streams inventories embedded Type1 programs only; Type3 character programs have separate glyph_evidence hashes and are not claimed to be absent ink.')
    return result,audit




