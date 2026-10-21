#!/usr/bin/env python3
"""Fresh ten-PDF extraction and exact boundary record; no source text exported."""
import copy, hashlib, importlib.util, json, os, sys
from pathlib import Path
P=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def require(ok,msg):
    if not ok:raise ValueError(msg)
def span(t,a,b):return dict(start_codepoint=a,end_codepoint_exclusive=b,sha256_utf8=sha(t[a:b].encode()))
def write(path,value):
    with path.open('x') as f:json.dump(value,f,indent=2,ensure_ascii=False);f.write('\n')
def load(binding,name):
    path=P/binding['path'];require(sha(path.read_bytes())==binding['sha256'],'Helper changed')
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.dont_write_bytecode=True;s.loader.exec_module(m);return m
def main():
    output=P/'phase98_twelve_measurement_source_recheck.json'
    specout=P/'phase98_twelve_measurement_N009_spec.json'
    require(not any(os.path.lexists(p) for p in [output,specout]),'Fresh outputs required')
    raw=(P/'phase84_eleven_measurement_protocol.json').read_bytes()
    require(sha(raw)=='7862cfcaa472b52eb94aeca47f77f47afbf7c33ae2fc47df1a78651e84623962','Baseline changed')
    old=json.loads(raw);m=load(old['measurement_helper'],'m98source');h=load(old['render_helper'],'h98source')
    import pypdf
    path='sources/phase17_gomi_loyola2018.pdf';pdf=(P/path).read_bytes()
    require(sha(pdf)=='0618a57cb5ff35c13587877818a2e77bce442cf2c561f204b6d5e5e095fa2fda','N009 PDF changed')
    text,pages,warnings=h.extract_primary(P/path,pypdf)
    require(len(pages)==22 and not warnings,'N009 extraction diagnostics changed')
    require(sha(text.encode())=='c35cf65a19974a8ee10230bcc8a1de4b044851d4f1af6534dba547ecf3534477','N009 extraction changed')
    offsets=[];at=0
    for i,page in enumerate(pages):offsets.append(at);at+=len(page)+1
    a=text.index('Abstract.');end=text.index('\nReferences\n')
    exclusions=[]
    def exclude(a,b,kind,page):
        exclusions.append({**span(text,a,b),'kind':kind,'physical_page':page,'exact_excluded_text':text[a:b]})
    # The first-page bottom block contains only received dates, MSC/keywords,
    # funding/thanks, copyright and printed page number; inspected in full.
    exclude(pages[0].index('Received by the editors'),len(pages[0]),'dates_MSC_keywords_acknowledgments_copyright_page_footer',1)
    for i in range(1,21):
        header=pages[i].split('\n',1)[0]+'\n'
        expected=(f'{i+1} Y. GOMI, M.L. LOYOLA, AND M.L.A.N. DE LAS PE ˜NAS\n' if (i+1)%2==0 else f'STRING C-GROUPS OF ORDER 1024 {i+1}\n')
        require(header==expected,'Unexpected page header '+str(i+1))
        exclude(offsets[i],offsets[i]+len(header),'running_title_or_author_header_and_printed_page',i+1)
    spec=dict(pdf_path=path,pdf_sha256=sha(pdf),pdf_bytes=len(pdf),pages=22,
      extraction_path='phase98_twelve_measurement_sources/N009_extraction.txt',extraction_sha256=sha(text.encode()),extraction_bytes=len(text.encode()),
      page_spans=[{**span(text,o,o+len(page)),'physical_page':i+1} for i,(o,page) in enumerate(zip(offsets,pages))],
      expected_extraction_warnings=warnings,body=span(text,a,end),exclusions=exclusions,body_pages=list(range(1,22)),
      start_rule='Abstract heading inclusive on printed/physical page 1; title, authors and journal furniture before it excluded',
      end_rule='Newline immediately before References on printed/physical page 21, after all concluding remarks; page 22 contains only affiliations',
      read_extent='All 22 original PDF pages individually visually inspected for complete source boundaries and mathematical/table inclusion; mathematical source-contract review inherited from phase87, not re-performed by this measurement',
      retained='All six numbered tables, all their continuation headings/rows, connected-diagram labels/caption, all formulas/proofs, quoted inputs, examples, corrections-as-originally-printed and concluding research discussion counted. No source text, symbol, table or OCR repair.',
      source_version='Published journal PDF: Contributions to Discrete Mathematics 13(1) (2018), 1–22, DOI 10.55016/ojs/cdm.v13i1.62475',
      primary_url='https://cdm.ucalgary.ca/article/download/62475/46803')
    docs={k:copy.deepcopy(old['documents'][k]) for k in old['source_keys']};docs['N009']=spec
    results={}
    for key,s in docs.items():
        require(sha((P/s['pdf_path']).read_bytes())==s['pdf_sha256'],'Source PDF changed '+key)
        tx,pg,wa=h.extract_primary(P/s['pdf_path'],pypdf)
        if s.get('extraction_format')=='N003_legacy_markers':tx=''.join(f'\n--- PDF PAGE {i+1} ---\n'+q+'\n' for i,q in enumerate(pg))
        if s.get('extraction_format')=='N008_legacy_markers':tx='\n\n'.join(f'[[PDF PAGE {i+1}; PRINTED {169+i}]]\n'+q for i,q in enumerate(pg))
        require(sha(tx.encode())==s['extraction_sha256'] and len(pg)==s['pages'],'Source extraction changed '+key)
        require(wa==s['expected_extraction_warnings'] and len(s['page_spans'])==len(pg),'Source diagnostics/pages changed '+key)
        for page,ps in zip(pg,s['page_spans']):require(sha(page.encode())==ps['sha256_utf8'],'Page changed '+key)
        body,ex=m.body_text(tx,s)
        # Durable full and cleaned texts stay in the expressly private source directory.
        dest=P/'phase98_twelve_measurement_sources'
        for suffix,val in [('fresh.txt',tx),('body.txt',body)]:
            with (dest/(key+'_'+suffix)).open('x') as f:f.write(val)
        results[key]=dict(pdf_path=s['pdf_path'],pdf_sha256=s['pdf_sha256'],pages=len(pg),extraction_sha256=sha(tx.encode()),
          warnings=wa,body_sha256=sha(body.encode()),body=s['body'],exclusion_count=len(ex),
          specification_sha256=sha(json.dumps(s,sort_keys=True,ensure_ascii=False).encode()),
          metrics={form:m.metrics(body,form) for form in old['forms']},nonwhitespace_control_codepoints=sorted({ord(c) for c in body if ord(c)<32 and not c.isspace()}))
    write(specout,spec);write(output,results)
    print(json.dumps({k:v['metrics']['NFC']['whitespace_tokens'] for k,v in results.items()}))
if __name__=='__main__':main()
