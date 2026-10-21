#!/usr/bin/env python3
"""Independent byte-class/content walk; shared reviewed font-program parser only.

Does not call author extraction, event alignment, aliases, selection or counts.
The low-level embedded-font decoder is intentionally reused and disclosed; actual
dictionary identity, whole content traversal, byte census and CFF defaults are
independently checked. Raster inspection is separate.
"""
from pathlib import Path
from collections import Counter
from io import BytesIO
import argparse, importlib.util, json, hashlib
import pypdf
from pypdf.generic import ContentStream,TextStringObject,ByteStringObject
from pypdf import _cmap
from fontTools.cffLib import CFFFontSet,cffISOAdobeStrings

def sha(x):return hashlib.sha256(x).hexdigest()
def need(ok,s):
    if not ok:raise ValueError(s)
def plain(v):
    if hasattr(v,'get_object'):v=v.get_object()
    if isinstance(v,dict):return {str(k):plain(x) for k,x in sorted(v.items())}
    if isinstance(v,list):return [plain(x) for x in v]
    return v if v is None or isinstance(v,(int,float,bool)) else str(v)
def audit(packet,public,sources):
    spec=json.loads((packet/'input_spec.json').read_text());expected=json.loads((packet/'font_audit.json').read_text())
    sp=importlib.util.spec_from_file_location('reviewed_font_parser',packet/'font_tools.py');parser=importlib.util.module_from_spec(sp);sp.loader.exec_module(parser)
    roots=dict(public=public,sources=sources,packet=packet);out={};total=Counter()
    for key,row in spec.items():
        path=roots[row['root']]/row['path'];pdf=pypdf.PdfReader(path);faces={};unicodefaces={};uses=Counter();cff=[]
        def face(f):
            stream=BytesIO();f.write_to_stream(stream);ref=f.indirect_reference
            info=dict(font_dictionary_object=dict(idnum=ref.idnum,generation=ref.generation),font_dictionary_sha256=sha(stream.getvalue()),pdf_encoding_declaration=plain(f.get('/Encoding')))
            fid=sha(json.dumps(info,sort_keys=True).encode())
            if f['/Subtype']=='/Type0':unicodefaces[fid]=dict(info,font=str(f['/BaseFont']));return None
            if fid not in faces:
                digest,mapping,glyphs=parser.embedded(f)
                effective=sha(json.dumps(mapping,sort_keys=True).encode())
                faces[fid]=dict(info,font=str(f.get('/BaseFont',f.get('/Name'))),effective_encoding_sha256=effective,effective_encoding={str(k):v for k,v in sorted(mapping.items())},font_stream_sha256=digest,mapping=mapping,glyphs=glyphs)
                fd=f.get('/FontDescriptor')
                if fd is not None and '/FontFile3' in fd.get_object():
                    ff=CFFFontSet();ff.decompile(BytesIO(fd.get_object()['/FontFile3'].get_object().get_data()),None);top=ff[ff.fontNames[0]]
                    missing='charset' not in top.rawDict
                    if missing:
                        need('ROS' not in top.rawDict and top.numGlyphs<=len(cffISOAdobeStrings),'non-CID ISOAdobe default legal')
                        need(list(glyphs.keys())==cffISOAdobeStrings[:top.numGlyphs],'actual complete default charset order')
                    cff.append(dict(dictionary=info['font_dictionary_object'],font=faces[fid]['font'],omitted_charset=missing,numGlyphs=top.numGlyphs,default='ISOAdobe first nGlyphs' if missing else None))
            return fid
        def walk(stream,res,current=None):
            stack=[]
            for args,op in ContentStream(stream,pdf).operations:
                if op==b'q':stack.append(current)
                elif op==b'Q':current=stack.pop()
                elif op==b'Tf':current=res['/Font'][args[0]].get_object()
                elif op==b'Do':
                    obj=res['/XObject'][args[0]].get_object()
                    if obj.get('/Subtype')=='/Form':walk(obj,obj.get('/Resources',res),current)
                elif op in (b'Tj',b'TJ',b"'",b'"'):
                    need(current is not None,'every string has explicit current font');fid=face(current)
                    if fid is None:continue
                    enc,cmap=_cmap.get_encoding(current);parts=args[0] if op==b'TJ' else [args[-1]]
                    for part in parts:
                        if not isinstance(part,(TextStringObject,ByteStringObject)):continue
                        data=part.original_bytes if hasattr(part,'original_bytes') else bytes(part)
                        for byte in data:
                            text=enc.get(byte,chr(byte)) if isinstance(enc,dict) else bytes([byte]).decode(enc)
                            text=''.join(cmap.get(ch,ch) for ch in text)
                            glyph=faces[fid]['mapping'][byte];need(glyph not in (None,'','.notdef'),'all actual used bytes resolve')
                            uses[fid,byte,text,glyph]+=1
        for pg in pdf.pages:walk(pg.get_contents(),pg['/Resources'])
        if key in expected:
            exp=expected[key];need(set(faces)=={r['font_identity'] for r in exp['font_dictionaries']},'exact actual dictionaries')
            for f in exp['font_dictionaries']:
                actual=faces[f['font_identity']]
                for k in ['font_dictionary_object','font_dictionary_sha256','pdf_encoding_declaration','effective_encoding_sha256','effective_encoding','font_stream_sha256']:
                    need(actual[k]==f[k],'font dictionary/encoding independent check '+key+' '+k)
            want=Counter({(r['font_identity'],r['encoded_byte'],r['decoded_text'],r['glyph_name']):r['occurrences'] for r in exp['encoded_glyph_classes']})
            need(uses==want,'independent complete encoded-byte class census '+key)
        else:need(not faces,'unaudited own PDFs use only unchanged Unicode fonts')
        actual_visible=[]
        for (fid,byte,text,glyph),n in uses.items():
            if text.isspace():
                evidence=parser.glyph_evidence(faces[fid]['glyphs'],glyph)
                if evidence['visible']:actual_visible.append(dict(font=faces[fid]['font'],byte=byte,glyph=glyph,occurrences=n,decoded=repr(text)))
        out[key]=dict(font_dictionaries=len(faces),unicode_dictionaries=len(unicodefaces),encoded_classes=len(uses),encoded_events=sum(uses.values()),cff_fonts=cff,visible_whitespace_classes=actual_visible,macroman_dictionaries=[f['font_dictionary_object'] for f in faces.values() if f['pdf_encoding_declaration']=='/MacRomanEncoding'])
        total.update(dict(dictionaries=len(faces),encoded_classes=len(uses),encoded_events=sum(uses.values())))
    need(total['dictionaries']==36 and total['encoded_classes']==805,'complete global font boundary')
    return dict(status='PASS',method='Independent content-stream and dictionary/class census; shared reviewed low-level font parser; no independent PDF renderer claim',totals=dict(total),documents=out,CFF_primary_reference=dict(url='https://adobe-type-tools.github.io/font-tech-notes/pdfs/5176.CFF.pdf',date_accessed='2026-10-11',locator='Technical Note 5176, section 13, physical page 23, Table 22; Table 9 physical page 15',claim='Omitted charset is 0 (ISOAdobe); predefined prefix permitted for non-CID fonts.'))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--sources-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');r=audit(a.packet,a.public_root,a.sources_root);a.out.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print('PASS',r['totals'])
