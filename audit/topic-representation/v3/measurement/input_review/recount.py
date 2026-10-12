#!/usr/bin/env python3
"""Independent character-state recount and PDF selection; no author helper imports.
The local font_events.py is an unchanged prior distinct independent review helper.
"""
import argparse,collections,hashlib,json,pathlib,re,unicodedata
from pypdf import PdfReader
from font_events import inspect
from boundary import need,sha,read,bound

def metrics(text,form):
    text=unicodedata.normalize(form,text);out=[];gap=False;words=alpha=nonspace=0;inword=inalpha=False
    for ch in text:
        w=not ch.isspace();a=ch.isalnum();words+=w and not inword;alpha+=a and not inalpha;inword=w;inalpha=a;nonspace+=w
        if w:
            if gap:out.append(' ')
            out.append(ch);gap=False
        elif out:gap=True
    c=''.join(out)
    return dict(whitespace_tokens=words,alphanumeric_units=alpha,characters_without_whitespace=nonspace,characters_with_collapsed_whitespace=len(c),utf8_bytes_with_collapsed_whitespace=len(c.encode()),collapsed_text_sha256=sha(c.encode()))

def apply(raw,edits):
    out=[];pos=0
    for a,b,value in sorted(edits):
        need(pos<=a<b<=len(raw),'disjoint literal edits');out.extend([raw[pos:a],value]);pos=b
    out.append(raw[pos:]);return ''.join(out)

SOURCE_ALIASES={('CMSY10','mapsto'):'⊢',('CMSY10','G'):'𝒢',('CMSY10','L'):'ℒ',('CMSY10','O'):'𝒪',('CMSY10','P'):'𝒫',('MSBM10','K'):'𝕂',('MSBM10','R'):'ℝ',('MSBM10','Z'):'ℤ'}
F010_ALIASES={('CMEX10','parenleftbig'):'(',('CMEX10','parenrightbig'):')',('CMEX10','braceleftbig'):'{',('CMEX10','bracerightbig'):'}',('CMEX10','braceleftBigg'):'{',('CMEX10','bracelefttp'):'⎧',('CMEX10','braceleftbt'):'⎩',('CMEX10','braceleftmid'):'⎨',('CMEX10','braceex'):'⎪',('CMEX10','unionsqdisplay'):'⨆',('CMEX10','tildewide'):'˜',('CMEX7','tildewide'):'˜',('CMSY10','mapsto'):'∣',('CMSY10','G'):'𝒢'}

def extract(path):
    reader=PdfReader(path);texts=[];fonts=[];pages=[];offset=0;visitor=[];images=[]
    for n,p in enumerate(reader.pages,1):
        pieces=[];f=[]
        def visit(s,cm,tm,font,size):pieces.append(s);f.extend([str(font.get('/BaseFont','')) if font else '']*len(s))
        t=p.extract_text(visitor_text=visit)or'';direct=p.extract_text()or'';need(t==direct,'visitor does not change extraction')
        texts.append(t);fonts.append(f);pages.append(dict(page=n,start=offset,end=offset+len(t),sha256=sha(t.encode()),empty_extraction=not t));offset+=len(t)+1
        visitor.append(dict(page=n,visitor_equals_returned=t==''.join(pieces),visitor_length=len(''.join(pieces)),returned_length=len(t)))
        for im in p.images:images.append(dict(page=n,name=im.name,width=im.image.width,height=im.image.height,sha256=sha(im.data)))
    return reader,texts,fonts,pages,visitor,images

def document(study,row):
    key=row['key'];path=bound(study,row);reader,texts,fonts,pages,visitor,images=extract(path);raw='\n'.join(texts);cuts=[]
    for pg,t in zip(pages,texts):
        n=pg['page'];start=pg['start']
        if key=='F010' and n==1:
            j=t.rfind('\n1\n')+1;need(j>0 and 'arXiv:2511.02410v2' in t[j+2:],'F010 banner retained');a,b=start+j,start+j+2
        elif key=='F010':
            header=t[:t.index('\n')+1];need(str(n)in header and ('ANTONIO'in header if n%2==0 else 'FINITE GROUPS REPRESENTED BY FINITE INCIDENCE GEOMETRIES'in header),'F010 first-line header');a,b=start,start+len(header)
        elif key=='L126' and n>1:
            header=(str(n)+' DIMITRI LEEMANS, KLARA STOKES, AND PHILIPPE TRANCHIDA\n')if n%2==0 else('GROUPS REPRESENTED BY INCIDENCE GEOMETRIES '+str(n)+'\n');need(t.startswith(header),'L126 running furniture');a,b=start,start+len(header)
        else:
            s=t.rstrip();tail=str(n);need(s.endswith(tail) and s[-len(tail)-1]=='\n','only isolated terminal page numeral');a,b=start+len(s)-len(tail),pg['end']
        cuts.append((a,b,'\n'))
    glyphs=[];audit={};events={}
    if key in ['F010','L126']:
        need(all(x['visitor_equals_returned']for x in visitor),'source visitor exact')
        events,audit=inspect(path,texts,fonts);aliases=F010_ALIASES if key=='F010' else SOURCE_ALIASES
        for i,e in events.items():
            ev=e['event'];lookup=(ev['font'].split('+')[-1],ev['glyph_name'])
            if lookup in aliases:
                need(len(ev['decoded_text'])==1,'one visible glyph one decoded char');glyphs.append((i,i+1,aliases[lookup]))
    # Current own PDFs use their literal Unicode extraction, with no repairs.
    selected=apply(raw,cuts);calibrated=apply(raw,cuts+glyphs)
    need(not any(unicodedata.category(c)in('Cc','Co') and c not in '\n\r\t' or c=='\ufffd' for c in calibrated),'no unclassified suspicious glyph')
    textsout={'raw_untrimmed':raw,'raw_selected':selected,'calibrated_selected':calibrated}
    result=dict(pdf_sha256=row['sha256'],pages=len(pages),calibrations=len(glyphs),furniture_occurrences=len(cuts),variants={k:{n:metrics(t,n)for n in ['NFC','NFKC']}for k,t in textsout.items()})
    evidence=dict(pages=pages,visitor=visitor,images=images,furniture=[dict(start=a,end=b,sha256=sha(raw[a:b].encode()))for a,b,_ in cuts],calibrations=[dict(offset=a,input=raw[a:b],output=v,event=events[a])for a,b,v in glyphs],font_audit=audit,extraction_sha256=sha(raw.encode()))
    return result,evidence

def run(study,packet):
    docs={};evidence={}
    for row in read(packet/'protocol_freeze/document_map.json')['documents']:docs[row['key']],evidence[row['key']]=document(study,row)
    old=read(study/'topic_Representation_measurement_inputs/author_counts.json')['documents']['F010'];need(docs['F010']==old,'independent F010 all30 cells and hashes equal inherited record')
    raws={}
    for row in read(packet/'protocol_freeze/raw_file_map.json')['files']:
        path=bound(study,row);b=path.read_bytes();raws[row['key']]=dict(bytes=len(b),sha256=sha(b),role=row['role'],metrics={n:metrics(b.decode(),n)for n in ['NFC','NFKC']})
    if (packet/'author_counts.json').exists():
        author=read(packet/'author_counts.json');need(docs==author['documents'],'all180PDFcells and36text hashes');need(raws==author['raw_files'],'all170 rawcells and34text hashes')
    return dict(status='PASS_INDEPENDENT_RECOUNT' if (packet/'author_counts.json').exists() else 'INDEPENDENT_RECOUNT_AWAITING_FROZEN_AUTHOR_COUNTS',documents=docs,raw_files=raws,evidence=evidence,pdf_cells=180,raw_cells=170,ratios=None)
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--study-root',type=pathlib.Path,required=True);a.add_argument('--packet',type=pathlib.Path,required=True);a.add_argument('--out',type=pathlib.Path,required=True);x=a.parse_args();need(not x.out.exists(),'fresh output');r=run(x.study_root,x.packet);x.out.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in r.items()if k not in ['documents','raw_files','evidence']}))
