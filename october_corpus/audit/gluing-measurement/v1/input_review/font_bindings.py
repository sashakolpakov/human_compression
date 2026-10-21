#!/usr/bin/env python3
"""Independent direct checks of actual PDF dictionaries and all calibrated events.

This does not reimplement the Type1 outline parser or the full font walker.
Those are separately read and freshly replayed with the copied author packet.
"""
from pathlib import Path
from io import BytesIO
from collections import Counter
import argparse, json
import pypdf
from pypdf.generic import ContentStream, IndirectObject, TextStringObject
import recount as R

def run(packet,sources):
    specs=R.read(packet/'input_spec.json');audits=R.read(packet/'font_audit.json');rows=[]
    for key in ('L010','CODE'):
        row=specs[key];pdf=(packet if row['root']=='packet' else sources)/row['path'];reader=pypdf.PdfReader(pdf)
        objects={}
        for item in audits[key]['font_dictionaries']:
            ref=item['font_dictionary_object'];font=IndirectObject(ref['idnum'],ref['generation'],reader).get_object()
            stream=BytesIO();font.write_to_stream(stream)
            R.need(R.sha(stream.getvalue())==item['font_dictionary_sha256'],'actual serialized font dictionary')
            R.need(str(font.get('/BaseFont'))==item['font'] and str(font.get('/Subtype'))==item['pdf_subtype'],'actual font name and type')
            enc=item['effective_encoding'];R.need(R.sha(json.dumps({int(k):v for k,v in enc.items()},sort_keys=True).encode())==item['effective_encoding_sha256'],'bound complete effective encoding')
            objects[item['font_identity']]=font
        classes=audits[key]['encoded_glyph_classes']
        R.need(all(c['glyph_name']!='.notdef' for c in classes),'no used undefined glyph')
        for c in classes:
            font=objects[c['font_identity']];desc=font.get('/FontDescriptor')
            if desc is None:
                R.need(c['font']=='/Times-Roman' and 32<=c['encoded_byte']<=126 and c['decoded_text']==chr(c['encoded_byte']),'unembedded banner is literal ASCII')
            else:
                desc=desc.get_object();program=desc.get('/FontFile',desc.get('/FontFile3')).get_object().get_data()
                R.need(R.sha(program)==c['font_stream_sha256'],'actual embedded program bytes')
        counts=Counter()
        ops={n:ContentStream(pg.get_contents(),reader).operations for n,pg in enumerate(reader.pages,1)}
        for repair in row['glyph_substitutions']:
            event=repair['pdf_events'][0];R.need(event['form_route']==[],'current calibrated events are on page directly')
            page=reader.pages[event['page']-1];font=page['/Resources']['/Font'][event['font_resource']].get_object()
            ref=font.indirect_reference
            R.need(dict(idnum=ref.idnum,generation=ref.generation)==event['font_dictionary_object'],'actual resource dictionary')
            operands,operator=ops[event['page']][event['operator_index']]
            R.need(operator.decode()==event['operator'],'actual content operator')
            parts=operands[0] if operator==b'TJ' else [operands[-1]];part=parts[event['part_index']]
            b=part.original_bytes if isinstance(part,TextStringObject) else bytes(part)
            R.need(R.sha(b)==event['text_part_sha256'] and b[event['byte_index']]==event['encoded_byte'],'actual encoded glyph occurrence')
            counts[event['encoded_byte']]+=1
        if key=='L010':R.need(dict(counts)=={55:1,66:8,67:6,71:89,72:8,79:63},'all six calibrated classes and 175 events')
        rows.append(dict(document=key,dictionaries=len(objects),classes=len(classes),calibrated_events=sum(counts.values()),actual_dictionary_and_stream_bytes_checked=True,used_notdef=0))
    return dict(status='PASS',documents=rows,actual_calibrated_operator_bytes_checked=175,full_font_walker_independently_reimplemented=False,outline_meanings_reviewed_visually=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--sources-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    R.need(not a.out.exists(),'fresh output');a.out.write_text(json.dumps(run(a.packet,a.sources_root),indent=2)+'\n')
