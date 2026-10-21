"""Audit actual Identity-H replacement glyphs as well as their ToUnicode maps."""
import json
import unicodedata
from collections import Counter
from io import BytesIO
from pypdf import PdfReader, _cmap
from pypdf.generic import ContentStream, TextStringObject, ByteStringObject
from fontTools.cffLib import CFFFontSet
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen
from font_tools import need, sha, font_identity

def serialized(obj):
    stream=BytesIO();obj.write_to_stream(stream);return stream.getvalue()

def audit(pdf,raw,fonts,pages):
    reader=PdfReader(pdf);faces={};identities={};classes={};uses=Counter();page_reports=[]
    for page_number,page in enumerate(reader.pages,1):
        events=[]
        def walk(stream,resources,initial_font=None):
            font=initial_font;stack=[]
            for operands,op in ContentStream(stream,reader).operations:
                if op==b'q':stack.append(font)
                elif op==b'Q':font=stack.pop()
                elif op==b'Tf':font=resources['/Font'][operands[0]].get_object()
                elif op==b'Do':
                    form=resources['/XObject'][operands[0]].get_object()
                    if form.get('/Subtype')=='/Form':walk(form,form.get('/Resources',resources),font)
                if op not in (b'Tj',b'TJ',b"'",b'"') or font.get('/Subtype')!='/Type0':continue
                fid,identity=font_identity(font)
                if fid not in faces:
                    need(str(font.get('/Encoding'))=='/Identity-H','replacement Identity-H font')
                    desc=font['/DescendantFonts'][0].get_object();fd=desc['/FontDescriptor'].get_object()
                    encoding,cmap=_cmap.get_encoding(font);need(encoding=='utf-16-be','two-byte Identity-H decoder')
                    if '/FontFile3' in fd:
                        binary=fd['/FontFile3'].get_object().get_data();cff=CFFFontSet();cff.decompile(BytesIO(binary),None);top=cff[cff.fontNames[0]]
                        need(tuple(top.ROS)==('Adobe','Identity',0),'explicit CFF CID system')
                        glyphs=top.CharStrings;kind='embedded_CID_CFF';names={int(n[3:]):n for n in glyphs.keys() if n.startswith('cid')}
                    else:
                        need('/FontFile2' in fd and str(desc.get('/CIDToGIDMap'))=='/Identity','literal TrueType identity CID map')
                        binary=fd['/FontFile2'].get_object().get_data();tt=TTFont(BytesIO(binary));glyphs=tt.getGlyphSet();kind='embedded_TrueType';names=dict(enumerate(tt.getGlyphOrder()))
                    faces[fid]=(cmap,glyphs,names,kind)
                    identities[fid]=dict(identity,font=str(font['/BaseFont']),descendant_dictionary_sha256=sha(serialized(desc)),
                                         ToUnicode_sha256=sha(font['/ToUnicode'].get_object().get_data()),
                                         embedded_program_sha256=sha(binary),kind=kind,
                                         used_decoder='Identity-H then exact ToUnicode map',glyph_index_sha256=sha(json.dumps(names,sort_keys=True).encode()))
                cmap,glyphs,names,kind=faces[fid]
                parts=operands[0] if op==b'TJ' else [operands[-1]]
                for part in parts:
                    if not isinstance(part,(TextStringObject,ByteStringObject)):continue
                    data=part.original_bytes if hasattr(part,'original_bytes') else bytes(part)
                    need(len(data)%2==0,'whole two-byte CID stream')
                    for at in range(0,len(data),2):
                        cid=int.from_bytes(data[at:at+2],'big');need(chr(cid) in cmap,'explicit Unicode mapping for each used CID')
                        decoded=cmap[chr(cid)];need(isinstance(decoded,str) and decoded,'mapped glyph text')
                        need(cid in names and names[cid]!='.notdef','actual embedded glyph exists')
                        key=(fid,cid,decoded)
                        if key not in classes:
                            glyph=names[cid];pen=RecordingPen();glyphs[glyph].draw(pen)
                            visible=any(op not in ('closePath','endPath') for op,args in pen.value)
                            need(not(decoded.isspace() and visible),'visible glyph must not be discarded as whitespace')
                            need(not any(unicodedata.category(c) in ('Cc','Co') or c=='\ufffd' for c in decoded),'no unclassified Type0 control/private/replacement glyph')
                            classes[key]=dict(font_identity=fid,font=str(font['/BaseFont']),cid=cid,decoded_text=decoded,glyph_name=glyph,
                                              visible_outline=visible,outline_sha256=sha(json.dumps(pen.value).encode()),kind=kind)
                        uses[key]+=1;events.append((str(font['/BaseFont']),decoded,fid,cid))
        walk(page['/Contents'],page['/Resources'])
        unicode_names={name for name,decoded,fid,cid in events}
        pg=pages[page_number-1];cursor=pg['start'];count=0
        for name,decoded,fid,cid in events:
            for c in decoded:
                if c.isspace():continue
                while cursor<pg['end'] and (raw[cursor].isspace() or fonts[cursor] not in unicode_names):cursor+=1
                need(cursor<pg['end'] and raw[cursor]==c and fonts[cursor]==name,'actual Unicode font stream matches returned text')
                cursor+=1;count+=1
        need(not any(not raw[i].isspace() and fonts[i] in unicode_names for i in range(cursor,pg['end'])),'no unaccounted Unicode extraction')
        page_reports.append(dict(page=page_number,glyph_events=len(events),nonspace_characters_aligned=count))
    return dict(status='ALL_USED_UNICODE_CLASSES_BOUND',actual_font_dictionaries=identities,
                encoded_glyph_classes=[dict(classes[k],occurrences=uses[k]) for k in sorted(classes)],pages=page_reports,
                full_font_programs_exported=False,calibration_rule='No own Unicode glyph substitution; exact ToUnicode output remains literal. Every used outline is bound; complete-page visual review supplies semantic interpretation. This is not a claim of independent isolated inspection of every outline.')
