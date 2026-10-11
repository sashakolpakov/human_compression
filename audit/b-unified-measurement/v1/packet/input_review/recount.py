#!/usr/bin/env python3
"""Distinct full-page recount; imports no measurement-author helper."""
import argparse, copy, hashlib, json, pathlib, re, unicodedata
import pypdf

PIN='e6f86129f414b960078738c0ae43cc799a78a3053c88af99965d605c9371c0b0'
def need(test,message):
    if not test:raise ValueError('B_INPUT_REJECT: '+message)
def sha(data):return hashlib.sha256(data).hexdigest()
def load(path):return json.loads(path.read_text())
def bound(root,row):
    path=pathlib.Path(row['path']);need(not path.is_absolute() and '..' not in path.parts,'relative path')
    data=(root/path).read_bytes()
    need(len(data)==row['bytes'] and sha(data)==row['sha256'],'exact full file '+str(path))
    return data
def manifest(root,pin):
    need(sha((root/'manifest.json').read_bytes())==pin,'frozen manifest')
    for row in load(root/'manifest.json')['exports']:bound(root,row)
def counts(text,norm):
    text=unicodedata.normalize(norm,text);flat=' '.join(text.split())
    previous=False;runs=0
    for c in text:
        current=c.isalnum()
        if current and not previous:runs+=1
        previous=current
    return dict(whitespace_tokens=len(text.split()),alphanumeric_units=runs,
      characters_without_whitespace=sum(not c.isspace() for c in text),
      characters_with_collapsed_whitespace=len(flat),utf8_bytes_with_collapsed_whitespace=len(flat.encode()),
      normalized_text_sha256=sha(text.encode()),collapsed_text_sha256=sha(flat.encode()))
def document(science,spec):
    bound(science,spec);texts=[];bindings=[];cuts=[];offset=0
    for number,page in enumerate(pypdf.PdfReader(science/spec['path']).pages,1):
        text=page.extract_text() or '';need(bool(text),'no empty page')
        bindings.append(dict(page=number,start=offset,end=offset+len(text),sha256=sha(text.encode()),empty_extraction=False))
        folio=re.search(r'(?:^|\n)'+str(number)+r'\s*$',text)
        need(folio is not None,'literal isolated terminal folio')
        start=folio.start()+int(text[folio.start()]=='\n')
        cuts.append(dict(page=number,start=offset+start,end=offset+len(text),literal=text[start:],sha256=sha(text[start:].encode())))
        offset+=len(text)+1;texts.append(text)
    raw='\n'.join(texts)
    need(spec['pages']==len(texts) and spec['page_bindings']==bindings,'every physical page')
    need(spec['extraction_sha256']==sha(raw.encode()),'whole extracted text')
    need(spec['included_spans']==[dict(start=0,end=len(raw),sha256=sha(raw.encode()))],'whole single source span')
    need(spec['excluded_furniture']==cuts,'exact folios only')
    need(spec['glyph_substitutions']==[],'no unreviewed glyph substitutions')
    selected=[];at=0
    for cut in cuts:selected.append(raw[at:cut['start']]);at=cut['end']
    selected.append(raw[at:]);selected='\n'.join(selected)
    need(all(unicodedata.category(c)!='Co' and c!='\ufffd' and (unicodedata.category(c)!='Cc' or c in '\n\r\t') for c in raw),'no unresolved control or private glyphs')
    variants=dict(raw_untrimmed=raw,raw_selected=selected,calibrated_selected=selected)
    return {v:{n:counts(s,n) for n in ['NFC','NFKC']} for v,s in variants.items()},selected
def main():
    ap=argparse.ArgumentParser()
    for name in ['inputs','science','study-root','public-root','out']:ap.add_argument('--'+name,type=pathlib.Path,required=True)
    a=ap.parse_args();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
    manifest(a.inputs,PIN);policy=load(a.inputs/'policy.json');manifest(a.science,policy['author_manifest']['sha256'])
    review=policy['scientific_review_manifest'];bound(a.study_root,review);manifest((a.study_root/review['path']).parent,review['sha256'])
    for row in policy['retained_public_bindings']:bound(a.public_root,row)
    old=load(a.public_root/'audit/b5-measurement/v1/packet/results.json')
    retained=load(a.inputs/'retained_source_counts.json');sources=[]
    for row in old['rows']:
        sources.append(dict(variant=row['variant'],normalization=row['normalization'],unit=row['unit'],
          sources={x['source']:x['source_cost'] for x in row['individual']},
          source_representations={x['source']:x['source_representation'] for x in row['individual']},
          L040_article_only=row['article_only_sensitivity']['L040_article_cost']))
    need(retained['coordinates']==sources and len(sources)==30,'all150 sources and30 article-only cells')
    need(policy['originals']==retained['source_order']==['N001','N003','N008','L030','L040'],'five originals')
    need(all(s['source_representations']['N001']=='literal_authored_rendering' for s in sources),'N001 available authored text')
    specs=load(a.inputs/'input_spec.json');expected=load(a.inputs/'author_counts.json');docs={};selected_pdf={}
    need(set(specs)=={'U_B','B1','B2','B3','B4','B5','CODE'},'all documents')
    for key,spec in specs.items():
        need(all(spec[k]==v for k,v in policy['replacements'][key].items()),'same fixed document')
        docs[key],selected_pdf[key]=document(a.science,spec)
        need(docs[key]==expected['documents'][key]['metrics'],'every PDF coordinate and hash')
    need([specs[k]['pages'] for k in ['U_B','B1','B2','B3','B4','B5','CODE']]==[16,3,4,4,5,11,7],'whole50 pages')
    for row in old['rows']:
        for key in ['B1','B3','B4','CODE']:
            past=row['printed_program_cost'] if key=='CODE' else next(x['application_cost'] for x in row['individual'] if x['application']==key)
            need(docs[key][row['variant']][row['normalization']][row['unit']]==past,'120 unchanged application/code cells')
    raw_files={}
    for cat in ['programs','drivers','formal']:
        for row in policy[cat]:
            data=bound(a.science,row);metrics={n:counts(data.decode(),n) for n in ['NFC','NFKC']}
            need(metrics==expected['raw_files'][cat][row['path']]['metrics'],'whole raw metrics')
            need(row['path'] not in raw_files,'no duplicate raw file');raw_files[row['path']]=metrics
    need(len(raw_files)==8 and [len(policy[c]) for c in ['programs','drivers','formal']]==[4,2,2],'all8 complete raw files')
    appendix=(a.science/'program-appendix.tex').read_text()
    names=re.findall(r'\\VerbatimInput(?:\[[^\]]*\])?\{([^}]+)\}',appendix)
    need(names==[r['path'] for r in policy['programs']] and not re.search('firstline|lastline|firstnumber|lastnumber',appendix),'all4 literal complete code inclusions')
    pack=lambda s:''.join(unicodedata.normalize('NFKC',s).split()).replace('↪','').replace('⌋','')
    for name in names:need(pack((a.science/name).read_text()) in pack(selected_pdf['CODE']),'actual complete printed program')
    need(policy['whole_common_once'] and policy['full_applications']==['B1','B2','B3','B4','B5'] and policy['raw_and_printed_programs_alternatives'],'whole common/acquisition boundary')
    need(all(x is None for x in policy['unknown_costs'].values()),'unknowns remain null')
    need(policy['partial_formal_declarations']==14 and policy['new_formal_declarations']==0 and not policy['new_scientific_credit'] and not policy['factors_permitted'] and policy['ratio'] is None,'no new scientific/formal or factor credit')
    controls=[]
    for name,edit in [
      ('omit last common page',lambda s:s['page_bindings'].pop()),
      ('select only proof text',lambda s:s['included_spans'][0].update(start=500)),
      ('remove body as furniture',lambda s:s['excluded_furniture'][0].update(start=0)),
      ('invent symbol correction',lambda s:s['glyph_substitutions'].append(dict(output='x'))),
      ('alter page text binding',lambda s:s['page_bindings'][0].update(sha256='0'*64))]:
        changed=copy.deepcopy(specs['U_B']);edit(changed)
        try:document(a.science,changed)
        except ValueError:controls.append(name)
        else:raise ValueError('negative control accepted '+name)
    report=dict(status='PASS_DISTINCT_B_INPUT_RECOUNT',pdf_metric_cells=210,raw_metric_cells=80,retained_source_cells=150,retained_article_only_cells=30,
      unchanged_prior_application_code_cells=120,documents=docs,raw_files=raw_files,source_coordinates=sources,negative_controls=controls,
      font_scope='Actual byte/CID/dictionary/outline walker is separately reviewed and replayed, not reimplemented by this independent page/count checker.',ratio=None,new_credit=0)
    (a.out/'recount.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({k:report[k] for k in ['status','pdf_metric_cells','raw_metric_cells','retained_source_cells','retained_article_only_cells','negative_controls']}))
if __name__=='__main__':main()
