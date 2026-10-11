#!/usr/bin/env python3
"""Bound full-PDF extraction and font-aware calibration; no ratio operation.

The selected() and metrics() rules match Topic E. Calibration deliberately does
not inherit Topic E's claim that every substitution preserves every metric.
Original texts are returned only to callers in the private study, not emitted.
"""
from pathlib import Path
import argparse,hashlib,json,re,unicodedata,copy
import pypdf
HERE=Path(__file__).resolve().parent
SOURCE_SPEC_SHA256='e7988784de320a02ee6ff27dfbbab055e6796d3e1e32d5342f122e8b35fa62fa'
REPLACEMENT_SPEC_SHA256={
 '393e1d741287b033e5e43bf1cc2a13a1789162787ab4bf21f3e2e3c5afd304a6',
 'a748129451f54d6aadff7589e0443ebb407996afca7cfe46d6dae31f22d89d95'}
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,msg):
    if not ok:raise ValueError(msg)
def selected(raw,binding):
    pieces=[]
    for span in binding['included_spans']:
        start=span['start']
        for f in binding['excluded_furniture']:
            if span['start']<=f['start']<f['end']<=span['end']:
                pieces.append(raw[start:f['start']]);start=f['end']
        pieces.append(raw[start:span['end']])
    return '\n'.join(pieces)
def metrics(text,form):
    t=unicodedata.normalize(form,text);collapsed=' '.join(t.split())
    return dict(whitespace_tokens=len(collapsed.split()),alphanumeric_units=len(re.findall(r'[^\W_]+',t)),
      characters_without_whitespace=sum(not c.isspace() for c in t),characters_with_collapsed_whitespace=len(collapsed),
      utf8_bytes_with_collapsed_whitespace=len(collapsed.encode()),collapsed_text_sha256=sha(collapsed.encode()))
def authorized(c,out,font):
    if c in '\uf8f1\uf8f2\uf8f3':return out==dict(zip('\uf8f1\uf8f2\uf8f3','⎧⎨⎩'))[c]
    if 'LASY' in font:return (c,out) in [('\x01','⊲'),('\x02','⊴'),('0','℧')]
    if 'CMEX' in font:return (c,out) in [('\x00','('),('\x01',')')]
    if 'LCIRCLE' in font:return c in 'st' and out=='●'
    if 'LINE10' in font:return (c,out) in [('\x11','/'),('Q','\\')]
    return False
def calibrate(raw,binding,key,fonts):
    chars=list(raw);seen=set()
    for row in binding['glyph_substitutions']:
        at=row['offset'];need(at not in seen,'duplicate calibration');seen.add(at)
        c=chr(int(row['input_codepoint'][2:],16));out=row['output']
        need(raw[at]==c and fonts[at]==row['input_font'],'glyph/font occurrence '+key)
        need(len(out)==1 and authorized(c,out,fonts[at]),'unauthorized or deleted visible glyph')
        p=binding['page_bindings'][row['page']-1]
        need(at==p['start']+row['page_offset'] and p['start']<=at<p['end'],'page calibration locator')
        a,b=row['context_start'],row['context_end']
        need(a<=at<b and sha(raw[a:b].encode())==row['context_sha256'],'calibration context')
        chars[at]=out
    for i,c in enumerate(raw):
        bad=(ord(c)<32 and c not in '\n\r\t') or unicodedata.category(c)=='Co' or c=='\ufffd'
        need(not bad or i in seen,'unclassified control/private-use glyph '+key)
        if any(x in fonts[i] for x in ('LASY','LCIRCLE','LINE10','CMEX')):
            known=(('LASY' in fonts[i] and c in '\x01\x020') or ('LCIRCLE' in fonts[i] and c in 'st') or ('LINE10' in fonts[i] and c in '\x11Q') or ('CMEX' in fonts[i] and c in '\x00\x01'))
            need(not known or i in seen,'unmapped known printable-font alias '+key)
    return ''.join(chars)
def document(root,key,row):
    p=root/row['path'];need(sha(p.read_bytes())==row['pdf_sha256'],'PDF hash '+key)
    texts=[];fonts=[];pages=[];at=0
    for i,page in enumerate(pypdf.PdfReader(p).pages,1):
        chunks=[];local=[]
        def visitor(t,cm,tm,f,size):
            chunks.append(t);local.extend([str(f.get('/BaseFont','')) if f else '']*len(t))
        t=page.extract_text(visitor_text=visitor) or ''
        need(t==''.join(chunks) and len(t)==len(local),'font alignment '+key)
        texts.append(t);fonts.extend(local);fonts.append('')
        pages.append({'page':i,'start':at,'end':at+len(t),'sha256':sha(t.encode()),'empty_extraction':not t});at+=len(t)+1
    raw='\n'.join(texts);fonts=fonts[:-1]
    need(len(texts)==row['pages'] and pages==row['page_bindings'],'physical pages '+key)
    need(sha(raw.encode())==row['extraction_sha256'],'extraction '+key)
    need(row['included_spans']==[{'start':0,'end':len(raw),'sha256':sha(raw.encode()),'role':row['included_spans'][0]['role']}],'complete-document scope '+key)
    previous=0
    for f in row['excluded_furniture']:
        a,b=f['start'],f['end'];need(previous<=a<b<=len(raw),'ordered furniture');previous=b
        need(sha(raw[a:b].encode())==f['sha256'],'furniture binding')
        need(raw[a:b]==f['literal'],'furniture literal')
    calibrated=calibrate(raw,row,key,fonts)
    return raw,selected(raw,row),selected(calibrated,row),fonts
def main():
    p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,default=HERE.parent);p.add_argument('--replacement-spec',type=Path,default=HERE/'replacement_input_spec.json');p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'Fresh output required');a.out.mkdir(parents=True)
    sb=(HERE/'source_input_spec.json').read_bytes();rb=a.replacement_spec.read_bytes()
    need(sha(sb)==SOURCE_SPEC_SHA256,'Pinned proposed full source boundary')
    need(sha(rb) in REPLACEMENT_SPEC_SHA256,'Pinned proposed complete replacement boundary')
    s=json.loads(sb);r=json.loads(rb)
    need(pypdf.__version__==s['pypdf_version']==r['pypdf_version'],'pypdf version')
    need(set(s['sources'])=={'L032','L034','F016','F013','L035','N009'},'All six sources')
    need(set(r['ours'])=={'U_A','A1','A2','A3','A4','A5','A6','code'},'Whole common paper, six applications and appendix')
    docs=s['sources']|r['ours'];rows={};cached={};selected_text={}
    for key,b in docs.items():
        raw,before,after,fonts=document(a.study_root,key,b);cached[key]=(raw,fonts);selected_text[key]=after
        sensitivities={}
        for form in ('NFC','NFKC'):
            old,new=metrics(before,form),metrics(after,form)
            sensitivities[form]={'calibrated_minus_raw':{k:new[k]-old[k] for k in old if k!='collapsed_text_sha256'},'raw_selected_sha256':old['collapsed_text_sha256'],'calibrated_selected_sha256':new['collapsed_text_sha256']}
        rows[key]={'pages':b['pages'],'changes':len(b['glyph_substitutions']),'metric_calibration_sensitivity':sensitivities}
    need(len(r['required_programs'])==4,'All four complete programs')
    for row in r['required_programs']:
        data=(a.study_root/row['path']).read_bytes()
        need(sha(data)==row['sha256'] and len(data)==row['bytes'],'Required program binding')
        need(re.sub(r'\s+','',data.decode()) in re.sub(r'\s+','',selected_text['code']),'Every full program in the charged appendix')
    controls=[]
    for label,mutate in [('deleted_visible_glyph',lambda b:b['glyph_substitutions'][0].update(output='')),('shifted_occurrence',lambda b:b['glyph_substitutions'][0].update(offset=b['glyph_substitutions'][0]['offset']+1)),('wrong_font',lambda b:b['glyph_substitutions'][0].update(input_font='/wrong'))]:
        b=copy.deepcopy(docs['F013']);mutate(b)
        try:calibrate(cached['F013'][0],b,'F013',cached['F013'][1])
        except ValueError:controls.append(label)
        else:raise ValueError('Control accepted '+label)
    report={'status':'PASS_INPUT_AND_CALIBRATION_DIAGNOSTICS_ONLY','source_spec_sha256':sha(sb),'replacement_spec_sha256':sha(rb),'checker_sha256':sha(Path(__file__).read_bytes()),'pypdf_version':pypdf.__version__,'source_pages':93,'replacement_pages':71,'documents':rows,'full_required_programs_bound_and_included':4,'negative_controls_rejected':controls,
      'no_primary_text_redistributed':True,'no_lengths_or_factors_adopted':True,'ratio':None}
    (a.out/'report.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'status':report['status'],'documents':len(rows),'calibrations':sum(x['changes'] for x in rows.values()),'controls':controls,'ratio':None}))
if __name__=='__main__':main()
