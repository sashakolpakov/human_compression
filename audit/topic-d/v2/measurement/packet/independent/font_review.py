#!/usr/bin/env python3
"""Independently align source text bytes with extraction and embedded outlines."""
from pathlib import Path
from collections import Counter
from io import BytesIO
import argparse, hashlib, json
from pypdf import PdfReader, _cmap
from pypdf.generic import ContentStream, TextStringObject, ByteStringObject
from fontTools import t1Lib
from fontTools.cffLib import CFFFontSet
from fontTools.pens.recordingPen import RecordingPen

def need(ok, message):
    if not ok: raise ValueError(message)

def sha(data): return hashlib.sha256(data).hexdigest()

def embedded(font):
    descriptor = font['/FontDescriptor']
    kind = next(k for k in ('/FontFile', '/FontFile3') if k in descriptor)
    data = descriptor[kind].get_object().get_data()
    if kind == '/FontFile':
        face = t1Lib.T1Font.__new__(t1Lib.T1Font)
        face.data = data; face.encoding = 'ascii'; face.parse()
        encoding, strings = face.font['Encoding'], face.font['CharStrings']
    else:
        face = CFFFontSet(); face.decompile(BytesIO(data), None)
        top = face[face.fontNames[0]]; encoding, strings = top.Encoding, top.CharStrings
    mapping = dict(enumerate(encoding))
    override = font.get('/Encoding')
    if override and not isinstance(override, str):
        for item in override.get('/Differences', []):
            if isinstance(item, int): index = item
            else: mapping[index] = str(item).lstrip('/'); index += 1
    return kind, sha(data), mapping, strings

def visible(document, name, glyph, byte):
    if document == 'L066' and 'LMMathExtension' in name:
        if glyph.startswith('bracketleft'): return '['
        if glyph.startswith('bracketright'): return ']'
        return {'bracelefttp':'⎧','braceleftmid':'⎨','braceleftbt':'⎩','braceex':'⎪'}[glyph]
    if document == 'L074' and 'CMEX' in name:
        return {'bracelefttp':'⎧','braceleftmid':'⎨','braceleftbt':'⎩'}[glyph]
    if 'CMSY' in name: return {'B':'ℬ','D':'𝒟','K':'𝒦','P':'𝒫','L':'ℒ'}[glyph]
    if 'LCIRCLE' in name: return '○'
    if 'LINE' in name: return {4:'╱',12:'╲'}[byte]
    raise ValueError('Unreviewed calibration font')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--proposal',type=Path,required=True)
    ap.add_argument('--study',type=Path,required=True); ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args(); need(not args.out.exists(),'Fresh output required')
    spec=json.loads((args.proposal/'source_input_spec.json').read_text())['sources']
    documents={}; failures=[]
    for key,row in spec.items():
        reader=PdfReader(args.study/row['path']); fonts={}; uses=Counter(); occurrences=[]; offset=0; pages=[]
        declared={g['offset']:g for g in row['glyph_substitutions']}
        for pno,page in enumerate(reader.pages,1):
            need(not page['/Resources'].get('/XObject'),'Unexpected unvisited text form')
            chunks=[]; textfonts=[]
            def visitor(text,cm,tm,font,size):
                chunks.append(text);textfonts.extend([str(font.get('/BaseFont','')) if font else '']*len(text))
            text=page.extract_text(visitor_text=visitor) or ''
            need(text==''.join(chunks),'Extraction visitor agreement')
            extracted=[(offset+i,c,textfonts[i]) for i,c in enumerate(text) if not c.isspace()]
            events=[];font=None;resource=None;stack=[]
            for op_index,(operands,op) in enumerate(ContentStream(page.get_contents(),reader).operations):
                if op==b'q':stack.append((font,resource))
                elif op==b'Q':font,resource=stack.pop()
                elif op==b'Tf':
                    resource=str(operands[0]);font=page['/Resources']['/Font'][operands[0]].get_object()
                if op not in (b'Tj',b'TJ',b"'",b'"'):continue
                need(font is not None and font.get('/Subtype')=='/Type1','One-byte Type1 source assumption')
                name=str(font['/BaseFont']);encoding,cmap=_cmap.get_encoding(font)
                if name not in fonts:fonts[name]=embedded(font)
                else:
                    desc=font['/FontDescriptor'];kind=fonts[name][0]
                    need(sha(desc[kind].get_object().get_data())==fonts[name][1],'Same named font stream')
                parts=operands[0] if op==b'TJ' else [operands[-1]]
                for part_index,part in enumerate(parts):
                    if not isinstance(part,(TextStringObject,ByteStringObject)):continue
                    data=part.original_bytes if hasattr(part,'original_bytes') else bytes(part)
                    for byte_index,byte in enumerate(data):
                        c=encoding.get(byte,chr(byte)) if isinstance(encoding,dict) else bytes([byte]).decode(encoding)
                        c=''.join(cmap.get(x,x) for x in c)
                        need(len(c)==1 and not c.isspace(),'No actual source whitespace or multi-character glyph')
                        binding=dict(page=pno,operator_index=op_index,operator=op.decode(),
                            part_index=part_index,byte_index=byte_index,decoded_character_index=0,
                            encoded_byte=byte,font_resource=resource,font=name,text_part_sha256=sha(data),
                            decoded_codepoint=f'U+{ord(c):04X}')
                        events.append((c,name,byte,op_index,part_index,byte_index,binding))
                        uses[(name,byte,c)]+=1
            need(len(events)==len(extracted),'All actual glyphs aligned with extraction')
            for (at,c,name),(d,n,byte,op_index,part_index,byte_index,binding) in zip(extracted,events):
                need(c==d and name==n,'Actual glyph/extracted font order')
                if at not in declared:continue
                rec=declared[at];kind,digest,mapping,strings=fonts[name];glyph=mapping[byte]
                if 'pdf_event' in rec:need(rec['pdf_event']==binding,'Complete declared PDF event binding')
                pen=RecordingPen();strings[glyph].draw(pen)
                expected=visible(key,name,glyph,byte)
                actual=dict(offset=at,page=pno,page_offset=at-offset,font=name,encoded_byte=byte,
                    input_codepoint=f'U+{ord(c):04X}',operator_index=op_index,part_index=part_index,
                    byte_index=byte_index,glyph_name=glyph,font_stream_kind=kind,font_stream_sha256=digest,
                    outline_sha256=sha(json.dumps(pen.value).encode()),expected_output=expected,
                    declared_output=rec['output'],pdf_event=binding)
                occurrences.append(actual)
                if rec['output']!=expected:failures.append(dict(document=key,**actual))
            pages.append(dict(page=pno,actual_glyphs=len(events),all_nonwhitespace_characters_aligned=True))
            offset+=len(text)+1
        need(len(occurrences)==len(declared),'All calibrations independently aligned')
        documents[key]=dict(pages=pages,physical_pages=len(reader.pages),embedded_fonts=len(fonts),
            font_streams=[dict(font=n,kind=v[0],sha256=v[1]) for n,v in sorted(fonts.items())],
            actual_glyphs=sum(uses.values()),actual_whitespace_glyphs=0,calibrated_occurrences=occurrences,
            unique_calibrated_encoded_glyphs=len({(r['font'],r['encoded_byte']) for r in occurrences}))
    result=dict(status='PASS_INDEPENDENT_GLYPH_IDENTITIES' if not failures else 'CORRECTION_REQUIRED_GLYPH_IDENTITIES',
        proposal_manifest_sha256=sha((args.proposal/'manifest.json').read_bytes()),
        checker_sha256=sha(Path(__file__).read_bytes()),documents=documents,corrections=failures,
        author_functions_imported=False,shared_dependencies=['pypdf6.13.0','fontTools4.63.0'],
        primary_text_images_fonts_exported=False,ratio=None)
    args.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(status=result['status'],corrections=len(failures),
        actual_glyphs={k:d['actual_glyphs'] for k,d in documents.items()})))

if __name__=='__main__':main()
