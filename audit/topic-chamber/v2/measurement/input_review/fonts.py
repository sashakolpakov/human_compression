"""Independent reconstruction of the used PDF fonts and original byte occurrences.

Only the pinned PDF/FontTools libraries are imported, never the author's
extractor, calibration, font-audit or reconciliation implementation.
"""
import collections, hashlib, json
from io import BytesIO
import pypdf
from pypdf import _cmap
from pypdf.generic import ContentStream, TextStringObject, ByteStringObject
from fontTools.cffLib import CFFFontSet
from fontTools.encodings.StandardEncoding import StandardEncoding
from fontTools.agl import UV2AGL, toUnicode
from fontTools.misc import psLib, psCharStrings, eexec
from fontTools.pens.recordingPen import RecordingPen

def require(c,m):
    if not c: raise ValueError(m)
def digest(b): return hashlib.sha256(b).hexdigest()

def type1(data):
    original=psLib.unpack_item
    def sparse(item): return None if item is None else original(item)
    psLib.unpack_item=sparse
    try: face=psLib.suckfont(data,'ascii')
    finally: psLib.unpack_item=original
    subrs=face['Private'].get('Subrs',[]); skip=face['Private'].get('lenIV',4)
    require(skip>=0,'Supported encrypted Type1 charstrings')
    def decrypt(b): return psCharStrings.T1CharString(eexec.decrypt(b,4330)[0][skip:],subrs=subrs)
    for n,b in list(face['CharStrings'].items()): face['CharStrings'][n]=decrypt(b)
    for i,b in enumerate(subrs):
        if b is not None: subrs[i]=decrypt(b)
    return face

def face(font):
    subtype=str(font['/Subtype']); name=str(font.get('/BaseFont',font.get('/Name','')))
    if subtype=='/Type3':
        program=None; chars={str(k)[1:]:v.get_object().get_data() for k,v in font['/CharProcs'].items()}; enc={}
    elif '/FontDescriptor' not in font:
        require(name=='/Times-Roman' and str(font.get('/Encoding'))=='/WinAnsiEncoding','Only standard banner font unembedded')
        program=None; chars=None;enc={}
    else:
        descriptor=font['/FontDescriptor'].get_object()
        if '/FontFile' in descriptor:
            program=descriptor['/FontFile'].get_object().get_data(); f=type1(program);encoding=f['Encoding'];chars=f['CharStrings']
        else:
            program=descriptor['/FontFile3'].get_object().get_data(); f=CFFFontSet();f.decompile(BytesIO(program),None);top=f[f.fontNames[0]];encoding=top.Encoding;chars=top.CharStrings
        if isinstance(encoding,str):
            require(encoding=='StandardEncoding','Supported named font encoding');encoding=StandardEncoding
        enc=dict(enumerate(encoding))
    decl=font.get('/Encoding');decl=decl.get_object() if decl is not None else None
    base=decl.get('/BaseEncoding') if isinstance(decl,dict) else decl
    if base=='/StandardEncoding': enc=dict(enumerate(StandardEncoding))
    elif base=='/WinAnsiEncoding': enc={i:UV2AGL.get(ord(bytes([i]).decode('cp1252',errors='replace')),'.notdef') for i in range(256)}
    else: require(base is None,'Supported explicit base encoding')
    if isinstance(decl,dict):
        at=0
        for x in decl.get('/Differences',[]):
            if isinstance(x,int): at=x
            else:enc[at]=str(x)[1:];at+=1
    return name,program,enc,chars

def evidence(chars,name):
    if chars is None:return {'kind':'unembedded_standard_glyph','visible':name!='space','outline_sha256':None}
    glyph=chars[name]
    if isinstance(glyph,bytes):
        require(b'/W 38' in glyph and b'/H 38' in glyph and b'/IM true' in glyph and b'/BPC 1' in glyph,'Actual one-bit bullet mask')
        bits=glyph.split(b'ID ',1)[1].split(b'\nEI',1)[0]
        require(len(bits)==190,'38 complete bitmap rows')
        rows=[[bool(bits[5*y+x//8]&(128>>(x%8))) for x in range(38)] for y in range(38)]
        require(rows==rows[::-1] and all(row==row[::-1] for row in rows),'Symmetric round bullet bitmap')
        require(0<sum(map(sum,rows))<38*38,'Nonempty nonrectangular bullet')
        return {'kind':'Type3_image_mask_character_program','visible':True,'character_program_sha256':digest(glyph),'character_program_bytes':len(glyph),'bitmap_dimensions':[38,38],'image_mask':True,'outline_sha256':None}
    pen=RecordingPen();glyph.draw(pen)
    return {'kind':'embedded_Type1_outline','visible':any(x[0] not in ('closePath','endPath') for x in pen.value),'outline_sha256':digest(json.dumps(pen.value).encode())}

def visible_character(key,font,byte,decoded,glyph):
    # Manual visible identities independently checked in the actual outline panels.
    if key=='L008' and font.endswith('+CMEX10'):
        table={12:('\f','⏐','vextendsingle'),16:('\x10','(','parenleftBig'),17:('\x11',')','parenrightBig'),48:('\uf8eb','⎛','parenlefttp'),49:('\uf8f6','⎞','parenrighttp'),64:('\uf8ed','⎝','parenleftbt'),65:('\uf8f8','⎠','parenrightbt'),84:('T','⋂','intersectiontext'),92:('\\','⋂','intersectiondisplay')}
        if byte in table:
            raw,out,name=table[byte];require((decoded,glyph)==(raw,name),'Actual delimiter/intersection glyph');return out
    if key=='L008' and font.endswith('+CMSY10') and byte==71:
        require(decoded=='G' and glyph=='G','Actual script G');return '𝒢'
    if key=='N016' and font.endswith('+CMSY10') and chr(byte) in 'KLMPQRT':
        require(decoded==chr(byte) and glyph==chr(byte),'Actual script letter')
        return dict(zip('KLMPQRT','𝒦ℒℳ𝒫𝒬ℛ𝒯'))[chr(byte)]
    if key=='N016' and font=='/F91' and byte==136:
        require(decoded=='\x88' and glyph=='a136','Actual bitmap bullet');return '•'
    return decoded

def audit(path,key,raw,raw_fonts,pages,expected,substitutions):
    reader=pypdf.PdfReader(path);faces={};fonts={};counts=collections.Counter();outline={};events={};aligned=0
    def get(font):
        ref=font.indirect_reference; ident=(ref.idnum,ref.generation)
        if ident not in faces:
            b=BytesIO();font.write_to_stream(b);fonts[ident]=digest(b.getvalue());faces[ident]=face(font)
        return ident,faces[ident]
    def walk(content,resources,current=None):
        stack=[]
        for operands,op in ContentStream(content,reader).operations:
            if op==b'q':stack.append(current)
            elif op==b'Q':current=stack.pop()
            elif op==b'Tf':current=resources['/Font'][operands[0]].get_object()
            elif op==b'Do':
                obj=resources['/XObject'][operands[0]].get_object()
                if obj.get('/Subtype')=='/Form':yield from walk(obj,obj.get('/Resources',resources),current)
            if op not in (b'Tj',b'TJ',b"'",b'"'):continue
            require(current is not None,'Text has actual font')
            ident,(name,program,mapping,chars)=get(current);encoding,cmap=_cmap.get_encoding(current)
            pieces=operands[0] if op==b'TJ' else [operands[-1]]
            for item in pieces:
                if not isinstance(item,(TextStringObject,ByteStringObject)):continue
                for byte in item.original_bytes:
                    text=encoding.get(byte,chr(byte)) if isinstance(encoding,dict) else bytes([byte]).decode(encoding)
                    decoded=''.join(cmap.get(c,c) for c in text); glyph=mapping[byte]
                    ev=evidence(chars,glyph);counts[ident,byte,decoded,glyph]+=1;outline[ident,byte,decoded,glyph]=ev
                    out=visible_character(key,name,byte,decoded,glyph)
                    yield ident,name,byte,decoded,glyph,ev,out
    repairs=[]
    for pno,page in enumerate(reader.pages,1):
        actual=list(walk(page.get_contents(),page['/Resources']))
        b=pages[pno-1]; offsets=[i for i in range(b['start'],b['end']) if not raw[i].isspace() or (key=='L008' and raw[i]=='\f' and raw_fonts[i].endswith('+CMEX10'))]
        at=0
        for ident,name,byte,decoded,glyph,ev,out in actual:
            if decoded.isspace() and not ev['visible']:continue
            for j,c in enumerate(decoded):
                require(at<len(offsets),'No excess original glyph event');pos=offsets[at];at+=1
                require((raw[pos],raw_fonts[pos])==(c,name),'Actual font/byte alignment with extraction')
                events[pos]=(ident,name,byte,decoded,glyph)
                if out!=decoded:
                    require(len(decoded)==len(out)==1,'One visible glyph replacement')
                    repairs.append((pos,out))
        require(at==len(offsets),'All extracted glyphs aligned');aligned+=at
    expected_counts={}
    for c in expected['encoded_glyph_classes']:
        o=c['font_dictionary_object']; ident=(o['idnum'],o['generation']); k=(ident,c['encoded_byte'],c['decoded_text'],c['glyph_name'])
        expected_counts[k]=c['occurrences'];require(outline[k]==c['glyph_evidence'],'Actual embedded outline/bitmap identity')
        require(fonts[ident]==c['font_dictionary_sha256'],'Actual font dictionary bytes')
        require((digest(faces[ident][1]) if faces[ident][1] else None)==c['font_stream_sha256'],'Actual embedded font stream')
        measured=visible_character(key,faces[ident][0],k[1],k[2],k[3]);agl=toUnicode(k[3])
        if measured==k[2] and agl!=k[2]:
            import unicodedata
            known={'prime':'′','square':'□','triangleleftequal':'⊴','negationslash':'̸','angbracketleft':'⟨','angbracketright':'⟩','diamondmath':'⋄'}
            require(unicodedata.normalize('NFKC',agl)==k[2] or known.get(k[3])==k[2],'Every unchanged exceptional glyph reviewed')
    require(counts==expected_counts,'All original encoded glyph classes and counts')
    require(len(fonts)==len(expected['font_dictionaries']),'All actual PDF font dictionaries')
    got=sorted((x['offset'],x['output']) for x in substitutions)
    require(sorted(repairs)==got,'Exactly all occurrence-bound repairs from actual used glyphs')
    for row in substitutions:
        ident,name,byte,decoded,glyph=events[row['offset']]; e=row['pdf_event'];obj=e['font_dictionary_object']
        require((obj['idnum'],obj['generation'])==ident and e['encoded_byte']==byte and e['glyph_name']==glyph and e['font_dictionary_sha256']==fonts[ident], 'Repair binds actual source dictionary and byte')
    return {'font_dictionaries':len(fonts),'encoded_classes':len(counts),'aligned_characters':aligned,'repairs':len(repairs),'actual_outlines_or_masks_compared':len(outline),'glyph_metadata_only':True}
