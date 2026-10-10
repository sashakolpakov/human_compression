#!/usr/bin/env python3
"""Author baseline builder: nine acquired PDFs / full eleven-source replacement.

Requires the already inspected render in --render-dir. Refuses overwrite. The
replay runner does not invoke this builder; no primary source is exported.
"""
import argparse, copy, hashlib, importlib.util, json, pathlib, re, sys
P=pathlib.Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def bind(path):
    b=(P/path).read_bytes();return {'path':path,'sha256':sha(b),'bytes':len(b)}
def span(t,a,b):return {'start_codepoint':a,'end_codepoint_exclusive':b,'sha256_utf8':sha(t[a:b].encode())}
def load(path,name,expected):
    assert sha((P/path).read_bytes())==expected
    s=importlib.util.spec_from_file_location(name,P/path);m=importlib.util.module_from_spec(s);sys.dont_write_bytecode=True;s.loader.exec_module(m);return m
def write(path,obj):
    with path.open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2,ensure_ascii=False);f.write('\n')
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--render-dir',type=pathlib.Path,required=True)
    ap.add_argument('--output',type=pathlib.Path,default=P/'phase84_eleven_measurement_protocol.json')
    a=ap.parse_args(); E=a.render_dir
    if a.output.exists():raise FileExistsError('Refusing existing protocol')
    oldpath=P/'phase57_ten_source_measurement_protocol.json'
    assert sha(oldpath.read_bytes())=='95971c144cc73ef4321d18ad1ab8bdd347796b39ce2e9dc2e81f4b028ea22063'
    old=json.loads(oldpath.read_text())
    m=load(old['measurement_helper']['path'],'metrics84',old['measurement_helper']['sha256'])
    h=load(old['render_helper']['path'],'render84',old['render_helper']['sha256'])
    import pypdf
    docs={k:copy.deepcopy(old['documents'][k]) for k in old['source_keys']}
    recheck=json.loads((P/'phase84_eleven_measurement_source_recheck.json').read_text())
    for key,s in docs.items():
        assert sha((P/s['pdf_path']).read_bytes())==s['pdf_sha256']
        text,pages,warnings=h.extract_primary(P/s['pdf_path'],pypdf)
        if s.get('extraction_format')=='N003_legacy_markers':text=''.join(f'\n--- PDF PAGE {i+1} ---\n'+q+'\n' for i,q in enumerate(pages))
        if s.get('extraction_format')=='N008_legacy_markers':text='\n\n'.join(f'[[PDF PAGE {i+1}; PRINTED {169+i}]]\n'+q for i,q in enumerate(pages))
        assert sha(text.encode())==s['extraction_sha256'] and len(pages)==s['pages']
        assert warnings==s['expected_extraction_warnings']
        assert len(s['page_spans'])==len(pages)
        for page,binding in zip(pages,s['page_spans']):assert sha(page.encode())==binding['sha256_utf8']
        body,_=m.body_text(text,s)
        assert {f:m.metrics(body,f) for f in old['forms']}==recheck[key]['metrics']
    path='phase65_petrial_integration_manuscript.md'; b=bind(path)
    assert b['sha256']=='6d302a2e7c696c916de97d2deef409c3053879999539be99a3fe72c9506205a1'
    manuscript=(P/path).read_text(); start=manuscript.index('The question addressed here');assert start==161
    docs['Compress_11']={**b,'body':span(manuscript,start,len(manuscript)),'exclusions':[],
        'start_rule':'First substantive introductory paragraph; only title and historical private-status heading excluded, exactly as prior convention',
        'end_rule':'EOF; every proof, correction, retained-input statement, reference and all five full programs included',
        'format':'markdown_tex'}
    body=(E/'replacement.md').read_text();presented=(E/'render.md').read_text();header=(E/'qed.tex').read_text()
    assert body==m.body_text(manuscript,docs['Compress_11'])[0]
    assert header==old['render']['header']
    assert body.replace("N013's",'N013’s').count('Recognition lemma O1.1 supplies the content needed from N013’s quoted Theorem 2.2.')==1
    rendered,pages,warnings=h.extract(pypdf.PdfReader(E/'replacement.pdf'));assert not warnings
    ai,codes=h.ast_info(json.loads((E/'ast.json').read_text()))
    programs=['phase37_compress_twogroups_census.g','phase40_compress_operations_check.g','phase40_compress_operations_exhaustive.g','phase41_chiral_cover_check.g','phase65_petrial_integration_check.py']
    complete=re.findall(r'```(?:gap|python)\n(.*?)\n```',body,re.S)
    assert len(complete)==5 and codes[-5:]==complete
    for code,path in zip(complete,programs):assert (code+'\n').encode()==(P/path).read_bytes()
    assert len(pages)==57 and ai['code_blocks']==11
    audit=json.loads((P/'phase70_petrial_integration_recent_audit.json').read_text())
    root=json.loads((P/'phase76_eleven_source_root_audit.json').read_text())
    contract={
        'source_manuscripts':11,'intake':old['contract']['intake']+['L108'],
        'independent_mathematical_status':audit['status'],'root_admission_status':root['status'],
        'principal_result_implication':'The eleven specified principal-result contracts, with their explicit source corrections and retained inputs, follow from the continuous phase65 manuscript.',
        'whole_document_every_assertion_rederived':False,'contract_rows':87,'rows_are_not_a_theorem_count':True,
        'retained_input_limits':old['contract']['retained_input_limits']+['L108 primary PDF absent; mathematical source reading uses complete authored browser rendering, which contributes no PDF-length credit'],
        'unproved_or_excluded':[x for x in old['contract']['unproved_or_excluded'] if x!='N009 and L108 not admitted sources']+['N009 is not an intake of this assembly'],
        'source_corrections':{'L108':['unconditional automorphism embedding replaced by exact action kernel','geometric Petrie length need not equal chamber-step order'],
            'older_sources':'All earlier corrected source contracts remain as stated in full manuscript and bound ledger'},
        'new_conjecture_solution':False,'new_priority_claim':False,'new_Lean_component':False,
        'reference_erratum':'The formerly additive phase45 reference correction is already incorporated in phase65; no obsolete second erratum is appended.',
        'measured_source_count':9,'zero_credit_sources':['N001','L108'],'exact_eleven_source_factor_available':False,
        'annotation_view':'Phase79 attribution notes and generated reader are a separate presentation layer outside this baseline, not mathematical premises or a measured eleven-source annotation edition.'}
    bindings=['phase65_petrial_integration_manifest.json','phase65_petrial_integration_ledger.json','phase65_petrial_integration_assembly.json',
      'phase70_petrial_integration_recent_audit.json','phase70_petrial_integration_recent_audit.md','phase70_petrial_integration_recent_audit_manifest.json',
      'phase76_eleven_source_root_audit.json','phase57_ten_source_measurement_protocol.json',
      'phase63_ten_source_measurement_recent_audit_report.json','phase63_ten_source_measurement_recent_audit_manifest.json',
      'phase63_ten_source_measurement_recent_audit_metadata_erratum.json','phase84_eleven_measurement_source_recheck.json',
      'phase84_eleven_measurement_source_status.json','phase84_eleven_measurement_visual_review.json']
    external=[{**bind(f),'role':'Exact executable duplicate of fully included appendix; charged once in manuscript'} for f in programs]
    for f in ['phase65_petrial_integration_build.py','phase65_petrial_integration_verify.py','phase65_petrial_integration_verify.json',
              'phase70_petrial_integration_recent_check.py','phase70_petrial_integration_recent_check.json']:
        external.append({**bind(f),'role':'Integrity/review infrastructure separately reported; no missing mathematical proof body is delegated here'})
    diagnostics=[x for x in (E/'replacement.log').read_text().splitlines() if re.search(r'Warning:|Overfull \\[hv]box|Underfull \\[hv]box|Missing character:|Missing glyph',x,re.I)]
    assert diagnostics==['Underfull \\hbox (badness 5862) in paragraph at lines 3948--3955','Underfull \\hbox (badness 7030) in paragraph at lines 3948--3955','Underfull \\hbox (badness 1755) in paragraph at lines 4034--4046']
    raster={f.name:sha(f.read_bytes()) for f in sorted(E.glob('page-*.png'))};assert len(raster)==57
    protocol={
      'schema':'Compress_11_nine_primary_PDF_full_denominator_lower_bound_v1','status':'author_protocol_pending_independent_measurement_review','date':'2026-10-10',
      'measurement_helper':old['measurement_helper'],'render_helper':old['render_helper'],
      'source_keys':old['source_keys'],'replacement_keys':['Compress_11'],'forms':old['forms'],'metric_keys':old['metric_keys'],
      'documents':docs,'contract':contract,'contract_bindings':[bind(f) for f in bindings],
      'certificate_programs':[bind(f) for f in programs],'external_costs':external,'expected_toolchain':old['expected_toolchain'],
      'render':{**copy.deepcopy(old['render']),
          'extensions_to_prior_renderer':'None: exact same phase57 header, reader, fonts, variables and presentation transform. Literal mathematical/code/table AST nodes and complete extracted programs checked. The same three underfull paragraph warnings occur at new line numbers; no overfull or missing glyph accepted.'},
      'expected_rendering':{'assembled_markdown_sha256':sha(body.encode()),'presentation_markdown_sha256':sha(presented.encode()),
        'ast':ai,'pages':len(pages),'extraction_sha256':sha(rendered.encode()),'metrics':{f:m.metrics(rendered,f) for f in old['forms']},
        'accepted_final_latex_diagnostics':diagnostics,
        'literal_probes':old['expected_rendering']['literal_probes']+['K(c)','Petrial','kerρ','core_G(⟨a⟩)'],
        'raster_sha256':raster},
      'counting_convention':{
        'primary':'NFC-normalized default-pypdf extraction; sum of nine cleaned full source bodies / complete rendered eleven-source replacement. N001 and L108 each receive exactly zero numerator credit. This is a conservative lower bound in the declared metric, not an exact eleven-source factor.',
        'sensitivity':old['counting_convention']['sensitivity'],
        'source_boundaries':'Every acquired PDF, page extraction, selected body, excluded span and complete document specification is byte/field identical to the independently reviewed phase57/63 protocol and freshly checked. This inherits phase43 six-PDF boundaries, phase51 L088/N013 boundaries, and phase57 N016 author-PDF boundaries. L088 post-reference diagrams count. N008 author name is Krempa, as corrected in phase63.',
        'source_repairs':old['counting_convention']['source_repairs'],
        'denominator':'Complete substantive phase65 manuscript through EOF: all new K(c)/O0/Petrial arguments, all older branches, entire lattice bridge, all source corrections, all five complete programs including optional Petrial controls, retained-input interfaces, source-version discussion and references. Only title/historical status heading excluded. The reference erratum is incorporated; not appended again.',
        'background':old['counting_convention']['background'],
        'annotations':'Separate phase79 attribution-margin layer is not included or claimed measured. Its added text is not a mathematical premise; a ratio for that reader requires its full denominator.',
        'interpretation':'Representation-sensitive conditional principal-result manuscript-length lower bound, pending independent measurement review. No whole-document equivalence, minimal-proof-length, effort, novelty, conjecture-resolution or broad Lean claim. Prior seven/ten-source factors are not transferred.',
        'source_reading_scope':'Fresh extraction/hash/boundary replay for all nine PDFs; original visual/source-mathematical reading is inherited explicitly from the bound earlier audits. No new PDF exists for N001/L108; browser reading is not PDF visual review. Every new replacement PDF page was visually inspected.'}}
    write(a.output,protocol);print('protocol SHA256',sha(a.output.read_bytes()))
if __name__=='__main__':main()
