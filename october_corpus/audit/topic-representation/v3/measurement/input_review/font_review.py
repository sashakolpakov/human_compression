#!/usr/bin/env python3
"""Independent source glyph/specification reconciliation and corruptions."""
import argparse,collections,copy,io,json,pathlib,unicodedata
from pypdf import PdfReader,_cmap
from pypdf.generic import ContentStream,TextStringObject,ByteStringObject
from fontTools import agl
from fontTools.pens.recordingPen import RecordingPen
from boundary import need,sha,read
from recount import SOURCE_ALIASES
from font_events import encoded_face
SPECIAL={'negationslash':'̸','angbracketleft':'⟨','angbracketright':'⟩','unionsq':'⊔','square':'□','dblarrowheadright':'↠','prime':'′','multicloseright':'⋊'}

def compare(audit,theirs):
    index={(tuple(x['font_dictionary']),x['encoded_byte'],x['decoded_text']):x for x in audit['classes']};dictionaries={tuple(x['font_dictionary']):x for x in audit['font_dictionaries']}
    need(len(theirs['encoded_glyph_classes'])==len(index)==649 and len(theirs['font_dictionaries'])==len(dictionaries)==24,'all actual source classes and dictionaries')
    for x in theirs['encoded_glyph_classes']:
        obj=x['font_dictionary_object'];key=((obj['idnum'],obj['generation']),x['encoded_byte'],x['decoded_text']);a=index[key]
        need(all(x[k]==a[k] for k in ['font','glyph_name','occurrences','font_stream_sha256','effective_encoding_sha256']),'actual glyph class and counts')
        need(x['font_dictionary_sha256']==dictionaries[key[0]]['font_dictionary_sha256'],'actual dictionary bytes')
        need(x['glyph_evidence'].get('outline_sha256')==a['outline_sha256'],'actual outline')
    for x in theirs['font_dictionaries']:
        obj=x['font_dictionary_object'];a=dictionaries[obj['idnum'],obj['generation']]
        need(all(x[k]==a[k] for k in ['font','font_stream_sha256','font_dictionary_sha256','effective_encoding_sha256']),'font dictionary identity')
        need(sha(json.dumps({int(k):v for k,v in x['effective_encoding'].items()},sort_keys=True).encode())==a['effective_encoding_sha256'],'actual complete encoding map')
    need(sum(x['aligned_characters']for x in theirs['pages'])==audit['aligned_characters']==35651,'all source nonspace events')
    need(len(theirs['actual_space_events'])==len(audit['actual_space_events']),'all actual whitespace')
    for a,b in zip(audit['actual_space_events'],theirs['actual_space_events']):need(all(b[k]==v for k,v in a.items()),'actual whitespace/glyph evidence')
    for x in audit['classes']:
        pair=(x['font'].split('+')[-1],x['glyph_name']);expected=SPECIAL.get(x['glyph_name'],agl.toUnicode(x['glyph_name']))
        need(pair in SOURCE_ALIASES or unicodedata.normalize('NFKC',x['decoded_text'])==unicodedata.normalize('NFKC',expected),'every glyph classified '+str(pair))
    return True

def specifications(evidence,spec):
    need(set(spec)=={'L126','U_R','R1','R2','CODE'},'all newly extracted specifications')
    for key,row in spec.items():
        e=evidence[key];need(e['pages']==row['page_bindings'],'all exact page offsets/hashes')
        need(row['extraction_sha256']==e['extraction_sha256'],'literal extraction binding')
        expected=e['furniture'];actual=[{k:x[k]for k in ['start','end','sha256']}for x in row['excluded_furniture']];need(actual==expected,'only independently identified furniture')
        need(len(row['glyph_substitutions'])==len(e['calibrations']),'all alias occurrences, no extra own substitutions')
        for x,g in zip(row['glyph_substitutions'],e['calibrations']):
            need(x['start']==g['offset'] and x['end']==g['offset']+1 and x['input']==g['input'] and x['output']==g['output'],'actual visible glyph span/output')
            event=x['pdf_events'][0];need(len(x['pdf_events'])==1 and all(event[k]==v for k,v in g['event']['event'].items()),'literal PDF text event')
            fd=event['font_dictionary_object'];need([fd['idnum'],fd['generation']]==g['event']['font_dictionary'],'actual event font dictionary')
            need(all(event[k]==g['event'][k]for k in ['effective_encoding_sha256','font_dictionary_sha256']),'actual event encoding/dictionary')
    return True

def run(study,packet,recount):
    a=read(packet/'font_audit.json');s=read(packet/'input_spec.json');e=recount['evidence'];compare(e['L126']['font_audit'],a['L126']);specifications(e,s)
    # Current own Unicode faces are bound independently as dictionaries; no
    # claim of a Type1-outline audit for these Type0 faces is made.
    type0=[];own_math=[]
    docs={x['key']:x for x in read(packet/'protocol_freeze/document_map.json')['documents']}
    for key in ['U_R','R1','R2','CODE']:
        reader=PdfReader(study/docs[key]['path']);seen={}
        for page in reader.pages:
            for ref in page['/Resources']['/Font'].values():
                f=ref.get_object()
                if f.get('/Subtype')!='/Type0':continue
                b=io.BytesIO();f.write_to_stream(b);seen[(ref.idnum,ref.generation)]=dict(font=str(f['/BaseFont']),font_dictionary_sha256=sha(b.getvalue()),encoding=str(f['/Encoding']),ToUnicode_sha256=sha(f['/ToUnicode'].get_object().get_data()))
        need(len(seen)==len(a[key]['unchanged_type0_dictionaries']),'all unmodified Unicode dictionaries')
        for x in a[key]['unchanged_type0_dictionaries']:
            fd=x['font_dictionary_object'];r=seen[fd['idnum'],fd['generation']];need(x['font']==r['font'] and x['font_dictionary_sha256']==r['font_dictionary_sha256'] and x['pdf_encoding_declaration']==r['encoding'],'own literal Unicode font binding');type0.append(dict(document=key,font_dictionary=[fd['idnum'],fd['generation']],**r))
        frequencies=collections.Counter();details={}
        def walk(stream,resources):
            current=None
            for args,op in ContentStream(stream,reader).operations:
                if op==b'Tf':current=resources['/Font'][args[0]].get_object()
                elif op==b'Do':
                    obj=resources['/XObject'][args[0]].get_object()
                    if obj.get('/Subtype')=='/Form':walk(obj,obj.get('/Resources',resources))
                if op not in (b'Tj',b'TJ',b"'",b'"') or current.get('/Subtype')!='/Type1':continue
                font=current;fid=font.indirect_reference.idnum;streamsha,encoding,glyphs=encoded_face(font);dec,cmap=_cmap.get_encoding(font)
                chunks=args[0]if op==b'TJ'else[args[-1]]
                for part in chunks:
                    if not isinstance(part,(TextStringObject,ByteStringObject)):continue
                    for byte in part.original_bytes:
                        s=dec.get(byte,chr(byte))if isinstance(dec,dict)else bytes([byte]).decode(dec);s=''.join(cmap.get(c,c)for c in s);name=encoding[byte];pen=RecordingPen();glyphs[name].draw(pen);k=(fid,byte,s);frequencies[k]+=1;details[k]=dict(font=str(font['/BaseFont']),glyph_name=name,font_stream_sha256=streamsha,effective_encoding_sha256=sha(json.dumps(encoding,sort_keys=True).encode()),outline_sha256=sha(json.dumps(pen.value).encode()))
        for page in reader.pages:walk(page.get_contents(),page['/Resources'])
        need(len(frequencies)==len(a[key]['encoded_glyph_classes']),'all own Type1 math classes')
        for x in a[key]['encoded_glyph_classes']:
            k=(x['font_dictionary_object']['idnum'],x['encoded_byte'],x['decoded_text']);v=details[k];need(x['occurrences']==frequencies[k]and all(x[z]==v[z]for z in ['font','glyph_name','font_stream_sha256','effective_encoding_sha256'])and x['glyph_evidence']['outline_sha256']==v['outline_sha256'],'own actual math outline and multiplicity');own_math.append(dict(document=key,encoded_byte=k[1],decoded_text=k[2],occurrences=frequencies[k],**v))
    changes=[('changed_outline',lambda x:x['encoded_glyph_classes'][0]['glyph_evidence'].update(outline_sha256='0'*64)),('wrong_dictionary',lambda x:x['encoded_glyph_classes'][0]['font_dictionary_object'].update(idnum=0)),('wrong_encoding',lambda x:x['font_dictionaries'][0]['effective_encoding'].update({'0':'space'})),('omit_class',lambda x:x['encoded_glyph_classes'].pop()),('wrong_multiplicity',lambda x:x['encoded_glyph_classes'][0].update(occurrences=0)),('discard_space',lambda x:x['actual_space_events'].pop())];controls=[]
    for name,f in changes:
        x=copy.deepcopy(a['L126']);f(x)
        try:compare(e['L126']['font_audit'],x)
        except (ValueError,KeyError):controls.append(dict(name=name,rejected=True))
        else:raise ValueError('accepted font corruption '+name)
    for name,f in [('mapsto_as_full_arrow',lambda x:next(g for g in x['L126']['glyph_substitutions']if g['output']=='⊢').update(output='↦')),('omit_alias',lambda x:x['L126']['glyph_substitutions'].pop()),('lose_page',lambda x:x['R1']['page_bindings'].pop()),('drop_body_as_furniture',lambda x:x['L126']['excluded_furniture'][0].update(end=999))]:
        x=copy.deepcopy(s);f(x)
        try:specifications(e,x)
        except (ValueError,KeyError):controls.append(dict(name=name,rejected=True))
        else:raise ValueError('accepted specification corruption '+name)
    return dict(status='PASS_INDEPENDENT_SOURCE_FONT_AND_SPECIFICATION_REVIEW',source_font_dictionaries=24,source_glyph_classes=649,source_actual_nonspace_events=35651,source_substitutions=28,own_substitutions=0,unchanged_Type0_dictionaries=type0,own_Type1_math_classes=own_math,controls=controls,primary_font_or_raster_exported=False)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--study-root',type=pathlib.Path,required=True);p.add_argument('--packet',type=pathlib.Path,required=True);p.add_argument('--recount',type=pathlib.Path,required=True);p.add_argument('--out',type=pathlib.Path,required=True);x=p.parse_args();need(not x.out.exists(),'fresh output');r=run(x.study_root,x.packet,read(x.recount));x.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='unchanged_Type0_dictionaries'}))
