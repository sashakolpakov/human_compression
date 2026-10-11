#!/usr/bin/env python3
"""Independent boundary, retained authority, reader and semantic-control audit."""
import argparse,copy,json,hashlib,re
from pathlib import Path
from collections import Counter
from pypdf import PdfReader
from recount import need,sha,load,bound,extraction,selected
IDS=['L032','L034','F016','F013','L035','N009','L128','L012']
OWN=['U']+[f'A{i}' for i in range(1,9)]+['CODE_A','CODE_AFFINE','CODE_DIAGRAM']

def contract(p,s,r):
    need(p['source_ids']==IDS and list(s)==IDS+OWN,'Whole source/replacement roster')
    need(p['common_documents']==['U'] and p['application_documents']==OWN[1:9] and p['complete_program_appendices']==OWN[9:],'Whole shared and local components')
    need(p['source_to_application']==dict(zip(IDS,OWN[1:9])),'Source-to-application contract')
    need([sum(s[k]['pages'] for k in group) for group in (IDS,['U'],OWN[1:9],OWN[9:])]==[119,23,45,30],'Complete physical documents')
    need([p[x] for x in ('pdf_documents','physical_pages','source_pages','common_pages','application_pages','program_appendix_pages')]==[20,217,119,23,45,30],'Declared full boundary')
    need(p['primary']['variant']=='calibrated_selected' and p['primary']['normalization']=='NFC' and p['primary']['metric']=='characters_without_whitespace','Prespecified primary')
    need(p['variants']==['raw_untrimmed','raw_selected','calibrated_selected'] and p['normalizations']==['NFC','NFKC'],'All source representation sensitivities')
    need(len(p['metrics'])==5 and len(set(p['metrics']))==5,'Five units')
    need(Counter(x['role'] for x in r)==dict(required_program_or_data=11,inherited_auxiliary=3,current_operational_driver=2,partial_formal_evidence=14),'Raw program/data/auxiliary/formal separation')
    need(len({x['file']['path'] for x in r})==len(r)==p['raw_files']==30,'No omitted or duplicated raw files')
    need(Counter(x.get('printed_in') for x in r if x['role']=='required_program_or_data')==dict(CODE_A=4,CODE_AFFINE=6,CODE_DIAGRAM=1),'Whole program/data print closure')
    need(p['programs_are_alternate_representations'] is True,'No double software charge')
    need(p['ratios'] is None and p['symmetric_software_factors'] is None,'No numerical factors or unsupported software factors')
    need(len(p['unknown_costs'])==5 and all(x is None for x in p['unknown_costs'].values()),'No zero for unknown cost')
    need(p['new_credit']==dict(source=0,question=0,formal=0),'No new credit')
    need(not p['new_science_execution'] and not p['new_formal_compile'],'No inflated scientific replay claim')

def run(packet,roots):
    p=load(packet/'policy.json');s=load(packet/'input_spec.json');r=load(packet/'raw_inventory.json');contract(p,s,r)
    bindings=load(packet/'bindings.json');evidence=load(packet/'inherited_evidence.json');refs=bindings['references']+bindings['scientific_and_review_exports']+[x['binding'] for x in evidence['public_records']]+evidence['own_visual_records']+load(packet/'helper_provenance.json')['base_methods']
    for x in refs:bound(x,roots)
    science=roots['study']/'topic_A_affine_unified';review=load(roots['study']/'topic_A_affine_independent_review/review.json')
    need(review['preserved_science']['source_dispositions']==102 and not review['preserved_science']['old_principal_contracts_changed'],'Exact inherited scope')
    need(review['computation_and_Lean']['unchanged_whole_required_program_data_files']==11 and not review['computation_and_Lean']['complete_volume_formalized'],'Computation/formal scientific boundary')
    inv=load(science/'program_inventory.json');formal=load(science/'formal_scope.json')
    need(len(inv['required_complete_files'])==11 and len(formal['modules'])==14,'Inventory authority')
    for x in inv['required_complete_files']:
        matching=[v for v in r if v['file']['path']=='topic_A_affine_unified/'+x['path']];need(len(matching)==1 and matching[0]['file']['sha256']==x['sha256'],'Scientific required file missing')
    for x in formal['modules']:
        y=x['current'];need(any(v['file']['path']=='topic_A_affine_unified/'+y['path'] and v['file']['sha256']==y['sha256'] for v in r),'Formal evidence dropped')
    listing=load(packet/'written_listing_boundary.json')
    for x in listing['unique_files']:bound(dict(root='study',**x),roots)
    def closure(path,seen=None):
        seen=set() if seen is None else seen
        if path in seen:return seen
        seen.add(path);text=(science/path).read_text()
        for name in re.findall(r'\\(?:input|include)\{([^}]+)\}',text):
            child=name if name.endswith('.tex') else name+'.tex';closure(child,seen)
        return seen
    for key in OWN[:9]:
        tex=s[key]['tex']['path'].removeprefix('topic_A_affine_unified/');actual=closure(tex)
        need(actual==set(listing['documents'][key]),'Full TeX dependency closure '+key)
        for f in actual:need(not re.search(r'\\(?:VerbatimInput|lstinputlisting|inputminted|begin\{(?:verbatim|Verbatim|CompleteProgram|lstlisting|minted)\})',(science/f).read_text()),'Embedded executable syntax '+key)
    # The two source screens are previously independently accepted and bound,
    # not newly inferred by regex from contemporary replacement papers.
    screen=load(roots['study']/'embedded_validation_listing_audit/topic_screen.json')
    selected_screens=[x for x in screen['topics'] if x['topic'] in ('A','Affine')]
    need(len(selected_screens)==2 and set(sum([x['source_ids'] for x in selected_screens],[]))==set(IDS),'All eight inherited source listing screens')
    need(all(x['status']=='RETAIN_WITH_PRECISE_MANUSCRIPT_ONLY_LABEL' for x in selected_screens),'Source-only listing conflict')
    # Bind the full retained listing evidence itself through the accepted manifests.
    for folder in ('embedded_validation_listing_audit','embedded_listing_root_review'):
        directory=roots['study']/folder
        for x in load(directory/'manifest.json')['exports']:need(sha((directory/x['path']).read_bytes())==x['sha256'],'Retained listing evidence')
    counts=load(packet/'author_counts.json');tex=(packet/'input_reader.tex').read_text();pdf=PdfReader(packet/'input_reader.pdf')
    need(len(pdf.pages)==2,'Whole reader')
    rows=re.findall(r'^(L032|L034|F016|F013|L035|N009|L128|L012|U|A[1-8]) & .*? & (\d+) & ([\d,]+) \\\\',tex,re.M)
    need(len(rows)==17,'All reader source/scientific rows')
    for key,pages,count in rows:need(int(pages)==s[key]['pages'] and int(count.replace(',',''))==counts['documents'][key]['metrics']['calibrated_selected']['NFC']['characters_without_whitespace'],'Reader data '+key)
    code_rows=re.findall(r'^(Two-group computation|Affine computation|Diagram computation).*? & (\d+) & ([\d,]+) \\\\',tex,re.M)
    need(len(code_rows)==3,'Full reader program inventory')
    for (_,pages,count),key in zip(code_rows,OWN[9:]):need(int(pages)==s[key]['pages'] and int(count.replace(',',''))==counts['documents'][key]['metrics']['calibrated_selected']['NFC']['characters_without_whitespace'],'Reader appendix data')
    fulltext=' '.join((x.extract_text() or '') for x in pdf.pages)
    need('unknown' in fulltext and 'fourteen' in fulltext and 'eleven' in fulltext and '119' in fulltext and '217' in fulltext,'Reader qualification missing')
    controls=[]
    changes=[('drop old source',lambda p,s,r:p['source_ids'].pop()),('free common',lambda p,s,r:p.update(common_documents=[])),('omit application',lambda p,s,r:p['application_documents'].pop()),('misroute original',lambda p,s,r:p['source_to_application'].update(L012='A1')),('drop page',lambda p,s,r:s['A6'].update(pages=10)),('shorten common',lambda p,s,r:s['U'].update(pages=22)),('drop raw coordinate',lambda p,s,r:p['variants'].pop()),('drop Unicode sensitivity',lambda p,s,r:p['normalizations'].pop()),('change primary',lambda p,s,r:p['primary'].update(variant='raw_untrimmed')),('drop required data',lambda p,s,r:r.pop(1)),('required to optional',lambda p,s,r:r[0].update(role='optional_validation')),('duplicate file',lambda p,s,r:r.__setitem__(1,copy.deepcopy(r[0]))),('lose printed code',lambda p,s,r:r[0].update(printed_in='CODE_DIAGRAM')),('double print and raw',lambda p,s,r:p.update(programs_are_alternate_representations=False)),('unknown software zero',lambda p,s,r:p['unknown_costs'].update(historical_external_programs_and_data=0)),('software factor',lambda p,s,r:p.update(symmetric_software_factors=1)),('input ratio',lambda p,s,r:p.update(ratios=1)),('new original credit',lambda p,s,r:p['new_credit'].update(source=1)),('full formal rerun claim',lambda p,s,r:p.update(new_formal_compile=True))]
    for name,change in changes:
        pp,ss,rr=copy.deepcopy((p,s,r));change(pp,ss,rr)
        try:contract(pp,ss,rr)
        except (ValueError,KeyError):controls.append(name)
        else:raise ValueError('Control accepted '+name)
    # Occurrence/font/context and own-furniture controls run the independent walker.
    cached={}
    for key in ('L032','L128','U'):
        raw,fonts,pages,_=extraction(bound(s[key]['file'],roots),key);cached[key]=(raw,fonts,pages)
    mutations=[('erase glyph','L032',lambda b:b['glyph_substitutions'][0].update(output='')),('wrong actual font','L032',lambda b:b['glyph_substitutions'][0].update(input_font='/Bogus')),('shift actual glyph','L032',lambda b:b['glyph_substitutions'][0].update(offset=b['glyph_substitutions'][0]['offset']+1)),('wrong span context','L128',lambda b:b['glyph_substitutions'][0].update(context_sha256='0'*64)),('proof as footer','U',lambda b:b['excluded_furniture'][0].update(start=0)),('truncate whole boundary','U',lambda b:b['included_spans'][0].update(end=b['included_spans'][0]['end']-1))]
    for name,key,change in mutations:
        row=copy.deepcopy(s[key]);change(row['boundary'])
        try:selected(*cached[key],row,key)
        except (ValueError,KeyError):controls.append(name)
        else:raise ValueError('Glyph/boundary control accepted '+name)
    return dict(status='PASS',bound_external_records=len(refs),scientific_dispositions=102,whole_scientific_TeX_files=len(listing['unique_files']),inherited_source_screen_ids=IDS,reader_data_rows=20,rejected_controls=controls,listing_basis='Exact prior accepted eight-source screen plus full current 38-file TeX closure and distinct root proof-reading authority; not a new full primary-source reading.',repeated_GAP_or_Lean=False,ratios=None)

def main():
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--study-root',type=Path,required=True);p.add_argument('--public-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=run(a.packet,dict(study=a.study_root,public=a.public_root));a.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
if __name__=='__main__':main()
