#!/usr/bin/env python3
"""Independent A/Affine input recount: pypdf only, no author helper imports."""
import argparse, hashlib, io, json, unicodedata, re
from pathlib import Path
from collections import Counter
import pypdf

def need(x,msg):
    if not x: raise ValueError(msg)
def sha(x):return hashlib.sha256(x).hexdigest()
def load(p):return json.loads(Path(p).read_text())
def metric(text,norm):
    s=unicodedata.normalize(norm,text); runs=[];current=[];alnum=0;inword=False
    for c in s:
        if c.isalnum():
            if not inword:alnum+=1
            inword=True
        else:inword=False
        if c.isspace():
            if current:runs.append(''.join(current));current=[]
        else:current.append(c)
    if current:runs.append(''.join(current))
    collapsed=' '.join(runs)
    return dict(whitespace_tokens=len(runs),alphanumeric_units=alnum,characters_without_whitespace=sum(map(len,runs)),characters_with_collapsed_whitespace=len(collapsed),utf8_bytes_with_collapsed_whitespace=len(collapsed.encode()),collapsed_text_sha256=sha(collapsed.encode()))
def bound(row,roots):
    p=roots[row['root']]/row['path'];data=p.read_bytes();need(sha(data)==row['sha256'] and len(data)==row['bytes'],'file '+str(p));return p

def extraction(pdf,key):
    reader=pypdf.PdfReader(pdf);pages=[];strings=[];fonts=[];duplicates=0;pos=0
    for i,page in enumerate(reader.pages,1):
        calls=[]
        def visitor(text,cm,tm,font,size):calls.append((text,font))
        text=page.extract_text(visitor_text=visitor) or ''
        if ''.join(t for t,f in calls)!=text:
            permitted='arXiv:2610.09711v1  [math.GR]  7 Oct 2026'
            need(key=='L128' and i==1,'Unexpected visitor discrepancy')
            indices=[j for j,(t,f) in enumerate(calls) if t==permitted and f is None and j and calls[j-1][0]==t]
            need(len(indices)==1,'Unexpected duplicate banner');del calls[indices[0]];duplicates+=1
        need(''.join(t for t,f in calls)==text,'Visitor output still disagrees')
        fchars=[str(f.get('/BaseFont',f.get('/Name',''))) if f else '' for t,f in calls for c in t]
        need(len(fchars)==len(text),'Font-character count')
        pages.append(dict(page=i,start=pos,end=pos+len(text),sha256=sha(text.encode()),empty_extraction=not text))
        strings.append(text);fonts.extend(fchars);fonts.append('');pos+=len(text)+1
    need(duplicates==(key=='L128'),'Duplicate event count')
    return '\n'.join(strings),fonts[:-1],pages,reader

def selected(raw,fonts,pages,row,key):
    b=row['boundary'];need(b['page_bindings']==pages,'Page texts '+key)
    need(b['extraction_sha256']==sha(raw.encode()),'Raw text '+key)
    spans=b['included_spans'];need(len(spans)==1 and spans[0]['start']==0 and spans[0]['end']==len(raw) and spans[0]['sha256']==sha(raw.encode()),'Full document '+key)
    cut=[];last=-1
    for x in b['excluded_furniture']:
        a,z=x['start'],x['end'];need(last<=a<z<=len(raw),'Cut order');last=z
        need(raw[a:z]==x['literal'] and sha(raw[a:z].encode())==x['sha256'],'Cut text')
        p=pages[x['page']-1];need(p['start']<=a<z<=p['end'],'Cut page')
        if key not in ('L032','L034','F016','F013','L035','N009','L128','L012'):
            need(z==p['end'] and raw[a:z]=='\n'+str(x['page']),'Own cut not footer')
        cut.append((a,z,'\n'))
    edits=[];covered=set()
    for x in b['glyph_substitutions']:
        a=x['start'] if 'start' in x else x['offset'];z=x.get('end',a+1)
        literal=x['input'] if 'input' in x else chr(int(x['input_codepoint'][2:],16))
        need(raw[a:z]==literal and all(fonts[k]==x['input_font'] for k in range(a,z)),'Font/glyph occurrence '+key)
        p=pages[x['page']-1];need(a==p['start']+x['page_offset'],'Glyph page offset')
        need(p['start']<=x['context_start']<=a<z<=x['context_end']<=p['end'],'Glyph context range')
        need(sha(raw[x['context_start']:x['context_end']].encode())==x['context_sha256'],'Glyph context')
        need(len(x['output'])==1 and not covered.intersection(range(a,z)),'Glyph replacement');covered.update(range(a,z));edits.append((a,z,x['output']))
    for i,c in enumerate(raw):
        if (ord(c)<32 and c not in '\n\r\t') or unicodedata.category(c)=='Co' or c=='\ufffd':need(i in covered,'Unexplained glyph '+key)
    def edit(seq):
        bystart={a:(z,t) for a,z,t in seq};need(len(bystart)==len(seq),'Overlapping starts');out=[];i=0
        while i<len(raw):
            if i in bystart:
                z,t=bystart[i];need(not any(i<j<z for j in bystart),'Overlapping edits');out.append(t);i=z
            else:out.append(raw[i]);i+=1
        # An endpoint cut outputs its declared newline already. Collapsed metrics
        # ignore the extra separator used by the older helper at document end.
        return ''.join(out)
    return dict(raw_untrimmed=raw,raw_selected=edit(cut),calibrated_selected=edit(cut+edits))

def ownfonts(reader):
    allfonts={}
    for i,p in enumerate(reader.pages,1):
        for ref in p['/Resources'].get('/Font',{}).values():
            d=ref.get_object();stream=io.BytesIO();d.write_to_stream(stream);db=stream.getvalue()
            ident=f'{ref.idnum}:{ref.generation}' if hasattr(ref,'idnum') else sha(db)
            u=d.get('/ToUnicode');ds=d.get('/DescendantFonts');desc=(ds[0].get_object().get('/FontDescriptor') if ds else d.get('/FontDescriptor'));desc=desc.get_object() if desc else {}
            embed={k:sha(desc[k].get_object().get_data()) for k in ('/FontFile','/FontFile2','/FontFile3') if k in desc}
            need(u is not None and embed,'Own unembedded or unmapped font')
            rec=dict(dictionary_id=ident,dictionary_sha256=sha(db),base_font=str(d.get('/BaseFont','')),subtype=str(d.get('/Subtype','')),encoding=str(d.get('/Encoding','')),to_unicode_sha256=sha(u.get_object().get_data()),embedded_streams=embed,pages=[])
            if ident in allfonts:need({k:v for k,v in rec.items() if k!='pages'}=={k:v for k,v in allfonts[ident].items() if k!='pages'},'Dictionary collision')
            else:allfonts[ident]=rec
            allfonts[ident]['pages'].append(i)
    for r in allfonts.values():r['pages']=sorted(set(r['pages']))
    return list(allfonts.values())

def recount(packet,roots):
    need(pypdf.__version__=='6.13.0','pypdf version')
    m=load(packet/'manifest.json');need(sha((packet/'manifest.json').read_bytes())=='321f406f81f2ffe5436785c7e23cf328c301faed3aa37a077b0693d53124f51d','Exact input freeze')
    for x in m['exports']:need(sha((packet/x['path']).read_bytes())==x['sha256'],'Changed export')
    spec=load(packet/'input_spec.json');want=load(packet/'author_counts.json');base=load(packet/'baseline_documents.json');audit=load(packet/'own_font_audit.json');rawrows=load(packet/'raw_inventory.json');result={};cache={};cells=0;hashes=0;dicts=0;inherited=0
    for key,row in spec.items():
        pdf=bound(row['file'],roots);raw,fonts,pages,reader=extraction(pdf,key);texts=selected(raw,fonts,pages,row,key)
        metrics={v:{n:metric(t,n) for n in ('NFC','NFKC')} for v,t in texts.items()}
        need(metrics==want['documents'][key]['metrics'],'Metric mismatch '+key);cells+=30;hashes+=6
        if key in base:
            need(metrics==base[key]['metrics'],'Inherited source cost changed')
            prior=load(roots['public']/row['legacy_spec']);prior=prior.get('sources',prior)[key];need(prior==row['boundary'],'Inherited source boundary changed');inherited+=30
        else:
            fa=ownfonts(reader);need(fa==audit[key]['dictionaries'],'New actual font dictionaries '+key);dicts+=len(fa)
            need(row['boundary']['glyph_substitutions']==[],'New speculative glyph substitution')
        result[key]=dict(pages=len(pages),metrics=metrics,source_calibrations=len(row['boundary']['glyph_substitutions']));cache[key]=texts
    rawresults={}
    for row in rawrows:
        data=bound(row['file'],roots).read_text();metrics={n:metric(data,n) for n in ('NFC','NFKC')}
        need(metrics==want['raw_files_measured'][row['id']]['metrics'],'Raw metrics '+row['id']);hashes+=2
        rawresults[row['id']]=dict(role=row['role'],metrics=metrics)
    inclusion=[]
    for row in rawrows:
        if row['role']!='required_program_or_data':continue
        key=row['printed_in'];f=bound(row['file'],roots);texpath=bound(spec[key]['tex'],roots);tex=texpath.read_text();short=f.relative_to(texpath.parent).as_posix();data=f.read_text()
        if short.startswith('required-code/'):
            blocks=re.findall(r'\\begin\{CompleteProgram\}\n(.*?)\\end\{CompleteProgram\}',tex,re.S);need(blocks.count(data)==1,'Full literal data/program inclusion')
        else:
            opts=re.findall(r'\\VerbatimInput(?:\[([^]]*)\])?\{'+re.escape(short)+r'\}',tex);need(len(opts)==1 and not any(s in opts[0] for s in ('firstline','lastline','firstnumber')),'Full external source file')
        prog=''.join(data.split());printed=''.join(c for c in cache[key]['raw_selected'] if not c.isspace() and c not in '↪⌋');need(prog in printed,'Printed full-file inclusion '+row['id']);inclusion.append(row['id'])
    return dict(status='PASS',method='Independent extraction visitor, masks, counters and dictionary census; imports pypdf only, no author code or font parser.',pdf_cells=cells,raw_cells=len(rawrows)*10,collapsed_hashes=hashes,inherited_source_cells=inherited,new_font_dictionary_instances=dicts,source_glyph_calibrations=sum(result[k]['source_calibrations'] for k in base),documents=result,raw_files=rawresults,whole_computation_files=inclusion,full_source_outline_audit='Exact prior accepted policies and actual source-font/context bindings reused; no new outline inference.',ratios=None)

def main():
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--study-root',type=Path,required=True);p.add_argument('--public-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=recount(a.packet,{'study':a.study_root,'public':a.public_root});a.out.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n');print({k:v for k,v in r.items() if k not in ('documents','raw_files')})
if __name__=='__main__':main()
