#!/usr/bin/env python3
"""Freeze author metric protocol after complete visual inspection; never overwrites."""
import argparse, copy, hashlib, importlib.util, json, os, re, sys
from pathlib import Path
P=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def require(ok,msg):
    if not ok:raise ValueError(msg)
def bind(path):
    b=(P/path).read_bytes();return dict(path=path,sha256=sha(b),bytes=len(b))
def span(t,a,b):return dict(start_codepoint=a,end_codepoint_exclusive=b,sha256_utf8=sha(t[a:b].encode()))
def load(binding,name):
    require(bind(binding['path'])['sha256']==binding['sha256'],'Helper changed')
    s=importlib.util.spec_from_file_location(name,P/binding['path']);m=importlib.util.module_from_spec(s);sys.dont_write_bytecode=True;s.loader.exec_module(m);return m
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--render-dir',type=Path,required=True)
    ap.add_argument('--output',type=Path,default=P/'phase98_twelve_measurement_protocol.json');a=ap.parse_args();E=a.render_dir
    require(not os.path.lexists(a.output),'Fresh protocol required')
    raw=(P/'phase84_eleven_measurement_protocol.json').read_bytes()
    require(sha(raw)=='7862cfcaa472b52eb94aeca47f77f47afbf7c33ae2fc47df1a78651e84623962','Baseline changed')
    old=json.loads(raw);m=load(old['measurement_helper'],'metrics98');h=load(old['render_helper'],'render98')
    docs={k:copy.deepcopy(old['documents'][k]) for k in old['source_keys']}
    docs['N009']=json.loads((P/'phase98_twelve_measurement_N009_spec.json').read_text())
    recheck=json.loads((P/'phase98_twelve_measurement_source_recheck.json').read_text())
    import pypdf
    for key,s in docs.items():
        require(sha((P/s['pdf_path']).read_bytes())==s['pdf_sha256'],'PDF changed '+key)
        text,pages,warnings=h.extract_primary(P/s['pdf_path'],pypdf)
        if s.get('extraction_format')=='N003_legacy_markers':text=''.join(f'\n--- PDF PAGE {i+1} ---\n'+q+'\n' for i,q in enumerate(pages))
        if s.get('extraction_format')=='N008_legacy_markers':text='\n\n'.join(f'[[PDF PAGE {i+1}; PRINTED {169+i}]]\n'+q for i,q in enumerate(pages))
        require(sha(text.encode())==s['extraction_sha256'] and len(pages)==s['pages'],'Extraction changed '+key)
        require(warnings==s['expected_extraction_warnings'] and len(s['page_spans'])==len(pages),'Diagnostics changed '+key)
        for page,ps in zip(pages,s['page_spans']):require(sha(page.encode())==ps['sha256_utf8'],'Page changed '+key)
        body,_=m.body_text(text,s);require({f:m.metrics(body,f) for f in old['forms']}==recheck[key]['metrics'],'Count changed '+key)
    path='phase78_n009_integration_manuscript.md';bound=bind(path)
    require(bound['sha256']=='15dd00e3845526dc40bb0effa07652e32748958238759eae9a856d901071b801' and bound['bytes']==317916,'Manuscript changed')
    manuscript=(P/path).read_text();start=manuscript.index('The question addressed here');require(start==161,'Start changed')
    docs['Compress_12']={**bound,'body':span(manuscript,start,len(manuscript)),'exclusions':[],
      'start_rule':'First substantive introductory paragraph; only title and historical private-status heading excluded, as in predecessor',
      'end_rule':'EOF: all 26 numbered sections, source corrections, retained-input statements, eight complete code/data blocks and all references',
      'format':'markdown_tex'}
    body=(E/'replacement.md').read_text();presented=(E/'render.md').read_text();header=(E/'qed.tex').read_text()
    require(body==m.body_text(manuscript,docs['Compress_12'])[0],'Assembled body mismatch')
    rendered,pages,warnings=h.extract(pypdf.PdfReader(E/'replacement.pdf'));require(not warnings,'Extraction warning')
    ai,codes=h.ast_info(json.loads((E/'ast.json').read_text()))
    programs=['phase78_n009_integration_census.g','phase40_compress_operations_check.g','phase40_compress_operations_exhaustive.g',
      'phase41_chiral_cover_check.g','phase65_petrial_integration_check.py','phase78_n009_integration_finite.g',
      'phase78_n009_integration_data.g','phase78_n009_integration_run.py']
    complete=re.findall(r'```(?:gap|python)\n(.*?)\n```',body,re.S)
    require(len(complete)==8 and codes[-8:]==complete,'Eight full blocks required')
    for code,path in zip(complete,programs):require((code+'\n').encode()==(P/path).read_bytes(),'Appendix mismatch '+path)
    require(sum(len((c+'\n').encode()) for c in complete)==79874,'Complete code/data cost mismatch')
    require(len(pages)==83 and ai['code_blocks']==14,'Unexpected pagination/blocks')
    review=json.loads((P/'phase87_n009_integration_recent_audit.json').read_text())
    contract=copy.deepcopy(old['contract'])
    contract.update(source_manuscripts=12,intake=old['contract']['intake']+['N009'],
      independent_mathematical_status=review['status'],root_admission_status='Not independently certified by this measurement author; see separate root admission',
      principal_result_implication='The twelve specified corrected principal-result contracts, conditional on the explicit retained inputs, follow from the continuous phase78 manuscript as reviewed in phase87 and inherited earlier mathematical reviews.',
      measured_source_count=10,exact_twelve_source_factor_available=False,
      annotation_view='Full unannotated phase78 manuscript measured. Attribution readers are separate presentation layers; their added text requires a separate denominator.',
      N009_numbered_source_items=27,N009_source_tables=6,rows_are_not_a_theorem_count=True,
      obsolete_SmallGroups_input_removed_from_this_edition_only=True)
    contract.pop('exact_eleven_source_factor_available',None);contract.pop('contract_rows',None)
    contract['unproved_or_excluded']=[x for x in contract['unproved_or_excluded'] if x!='N009 is not an intake of this assembly']
    contract['retained_input_limits']=[x for x in contract['retained_input_limits'] if 'SmallGroups' not in x]+[
      'Complete TomLib J1 subgroup catalogue remains a substantive retained input',
      'GAP/NQ universal nilpotent quotient, exact subgroup arithmetic and complete coset enumeration remain trusted infrastructure; no replacement by Lean is asserted',
      'N009 retains the stated rank-three/rank-four/rank-five string-IP criteria and geometric universal-group interpretation',
      'N009 retains finite smooth-square quotient classification/structural descriptions and the exact exceptional infinite marked decomposition (source Theorem 5.3, quoted from McMullen–Schulte)',
      'The source Atlas presentations specify exact labels only; their completeness is not used by the new kernel census']
    contract['source_corrections']['N009']=['Corollary 3.7 has C2^3 bottom boundary and degenerate intermediate cases',
      'Table 4 literal rows e/f/h are distinguished from corrected target presentations',
      'Four Table 6 right labels require ordered dual type [16,4]',
      'Lemma 3.2 is marked quotient transport; square-quotient scope and small center exceptions remain explicit']
    bindings=['phase78_n009_integration_manifest.json','phase78_n009_integration_intake.json','phase78_n009_integration_ledger.json',
      'phase78_n009_integration_assembly.json','phase87_n009_integration_recent_audit.json','phase87_n009_integration_recent_audit.md',
      'phase87_n009_integration_recent_audit_manifest.json','phase84_eleven_measurement_protocol.json',
      'phase88_eleven_measurement_review_report.json','phase88_eleven_measurement_review_manifest.json',
      'phase88_eleven_measurement_review_metadata_erratum.md','phase98_twelve_measurement_N009_spec.json',
      'phase98_twelve_measurement_source_recheck.json','phase98_twelve_measurement_source_status.json',
      'phase98_twelve_measurement_visual_review.json']
    external=[{**bind(f),'role':'Byte-exact standalone duplicate of fully charged manuscript appendix; counted once in denominator'} for f in programs]
    for f in ['phase78_n009_integration_build.py','phase78_n009_integration_verify.py','phase87_n009_integration_recent_audit_check.py']:
        external.append({**bind(f),'role':'Integrity/reconstruction/independent-review infrastructure reported separately; no omitted mathematical branch is delegated here'})
    diagnostics=[x for x in (E/'replacement.log').read_text().splitlines() if re.search(r'Warning:|Overfull \\[hv]box|Underfull \\[hv]box|Missing character:|Missing glyph',x,re.I)]
    require(diagnostics==['Underfull \\hbox (badness 1173) in paragraph at lines 601--607','Underfull \\hbox (badness 5862) in paragraph at lines 4678--4685','Underfull \\hbox (badness 7030) in paragraph at lines 4678--4685','Underfull \\hbox (badness 1755) in paragraph at lines 4802--4819'],'Unreviewed diagnostic')
    raster={f.name:sha(f.read_bytes()) for f in sorted(E.glob('page-*.png'))};require(len(raster)==83,'Every raster required')
    visual=json.loads((P/'phase98_twelve_measurement_visual_review.json').read_text())
    require(visual['replacement']['all_pages_personally_viewed']==True and visual['replacement']['raster_sha256']==raster,'Visual review is not complete for exact final render')
    rendering=copy.deepcopy(old['render']);rendering.update(header=header,header_sha256=sha(header.encode()),
      extensions_to_prior_renderer='Only header glyph coverage: STIX Two Text fallback for ⁻⁸ⁱ⁴⁷⁶⁵₈; TeX textsubscript for ᵢⱼₜ. Same reader, main/monospace fonts, variables, presentation escaping and full-code wrapping. Literal math/code/table AST nodes unchanged. Subscript letters render semantically and extract as baseline letters; metrics are the actual PDF extraction without repair.')
    protocol=dict(schema='Compress_12_ten_primary_PDF_full_denominator_lower_bound_v1',status='author_protocol_pending_independent_measurement_review',date='2026-10-10',
      measurement_helper=old['measurement_helper'],render_helper=old['render_helper'],source_keys=old['source_keys']+['N009'],
      inherited_source_keys=old['source_keys'],replacement_keys=['Compress_12'],forms=old['forms'],metric_keys=old['metric_keys'],documents=docs,
      contract=contract,contract_bindings=[bind(f) for f in bindings],certificate_programs=[bind(f) for f in programs],external_costs=external,
      expected_toolchain=old['expected_toolchain'],render=rendering,
      expected_rendering=dict(assembled_markdown_sha256=sha(body.encode()),presentation_markdown_sha256=sha(presented.encode()),ast=ai,pages=len(pages),
        extraction_sha256=sha(rendered.encode()),metrics={f:m.metrics(rendered,f) for f in old['forms']},accepted_final_latex_diagnostics=diagnostics,
        literal_probes=old['expected_rendering']['literal_probes']+['K(d)','Q5.5','Q5.6','539264','107','McMullen'],raster_sha256=raster),
      counting_convention=dict(primary='NFC-normalized default-pypdf whitespace tokens: sum of ten complete cleaned source bodies / full twelve-source rendered replacement. N001 and L108 each have exactly zero numerator credit. Conservative conditional lower bound, never exact twelve-source factor.',
        sensitivity=old['counting_convention']['sensitivity'],source_boundaries='Nine old source specifications are field-for-field identical to phase84/88. Newly inspected N009 abstract through concluding remarks; exclude first-page publication metadata/thanks and only running furniture. All six tables and repeated table headings/rows retained. L088 post-reference diagrams continue to count.',
        source_repairs='None: default extraction is counted faithfully, including inherited font/control warnings and lost graphical formula placement. No OCR or mathematical text repair. N008 is Archer–Cara–Krempa; L035 title metadata correction is already applied in live status, frozen baseline unchanged.',
        denominator='All 26 sections through EOF, all inherited branches, all new universal-kernel/central/center/finite-classification arguments, all corrected source adapters and retained interfaces, all eight complete code/data blocks (79874 bytes), and all references. Only 161-codepoint initial title/status heading excluded. No required proof addendum external to this manuscript.',
        background='Conditional on exact reviewed retained background, not a proof-size bound after expanding all background theorems, software or transitive dependencies. N009 exceptional infinite marked decomposition and McMullen–Schulte remain retained; no SmallGroups catalogue in this edition. GAP/NQ and TomLib remain.',
        annotations='Full unannotated manuscript only. Margin-note editions and later standalone family/complement results not included or credited.',
        interpretation='Representation-sensitive manuscript-length lower bound under corrected principal-result contracts. Not whole-document equivalence, minimal-proof-length, labor saving, historical novelty, solved conjecture, or whole-manuscript Lean verification. Earlier seven/ten/eleven factors do not transfer.',
        source_reading_scope='Fresh hash/extraction/boundary checks for all ten acquired PDFs. Nine previous visual and mathematical readings inherited explicitly. All 22 new N009 primary pages and all 83 replacement pages personally visually inspected. Mathematical N009 source-contract acceptance is inherited from phase87, not independently re-reviewed in this measurement.'))
    with a.output.open('x') as f:json.dump(protocol,f,indent=2,ensure_ascii=False);f.write('\n')
    print(sha(a.output.read_bytes()))
if __name__=='__main__':main()
