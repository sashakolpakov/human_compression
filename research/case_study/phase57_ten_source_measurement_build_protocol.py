#!/usr/bin/env python3
"""Author-only nine-PDF / complete-ten-source lower-bound protocol builder.

Requires the separately inspected full rendering; refuses protocol overwrite.
The replay runner never invokes this author baseline builder.
"""
import hashlib, importlib.util, json, pathlib, subprocess, sys
P=pathlib.Path(__file__).resolve().parent
E=pathlib.Path('/private/tmp/phase57-ten-render-explore')
sha=lambda b:hashlib.sha256(b).hexdigest()
def bind(path):
    data=(P/path).read_bytes();return {'path':path,'sha256':sha(data),'bytes':len(data)}
def span(t,a,b,**kw):return {'start_codepoint':a,'end_codepoint_exclusive':b,'sha256_utf8':sha(t[a:b].encode()),**kw}
def load(path,name):
    s=importlib.util.spec_from_file_location(name,P/path);m=importlib.util.module_from_spec(s);sys.dont_write_bytecode=True;s.loader.exec_module(m);return m
def write(path,obj):
    if path.endswith(('source_extractions.json','source_acquisition.json')) and (P/path).exists():
        assert json.loads((P/path).read_text())==obj
        return
    with (P/path).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2,ensure_ascii=False);f.write('\n')
m=load('phase36_compress_forest_measurement.py','metrics57')
h=load('phase43_unified_lower_bound_measure.py','render57')
import pypdf
old7=json.loads((P/'phase43_unified_lower_bound_protocol.json').read_text())
oldC=json.loads((P/'phase51_compress_C_measurement_protocol.json').read_text())
docs={k:old7['documents'][k] for k in old7['source_keys']}
docs.update({k:oldC['documents'][k] for k in oldC['source_keys']})
extractions={}
for key,s in docs.items():
    text,pages,warnings=h.extract_primary(P/s['pdf_path'],pypdf)
    if s.get('extraction_format')=='N003_legacy_markers':text=''.join(f'\n--- PDF PAGE {i+1} ---\n'+q+'\n' for i,q in enumerate(pages))
    if s.get('extraction_format')=='N008_legacy_markers':text='\n\n'.join(f'[[PDF PAGE {i+1}; PRINTED {169+i}]]\n'+q for i,q in enumerate(pages))
    assert sha(text.encode())==s['extraction_sha256']
    assert len(pages)==s['pages']
    for page,ps in zip(pages,s['page_spans']):assert sha(page.encode())==ps['sha256_utf8']
    m.body_text(text,s)
    s['expected_extraction_warnings']=warnings
    s['phase57_reading']='Fresh primary extraction/hash/span replay. Inherit exact earlier audited full-body boundaries and reading scope; no claim of a new full mathematical reread.'
    extractions[key]={'pdf_path':s['pdf_path'],'pdf_sha256':s['pdf_sha256'],'extraction_sha256':sha(text.encode()),'pages':len(pages),'extraction_warnings':warnings,'boundary_protocol':('phase43_unified_lower_bound_protocol.json' if key in old7['source_keys'] else 'phase51_compress_C_measurement_protocol.json')}
s=bind('phase57_ten_source_measurement_sources/N016.pdf');text,pages,warnings=h.extract_primary(P/s['path'],pypdf);assert not warnings
assert text==(P/'phase57_ten_source_measurement_sources/N016.txt').read_text()
page_spans=[];cursor=0
for i,page in enumerate(pages):page_spans.append(span(text,cursor,cursor+len(page),physical_page=i+1));cursor+=len(page)+1
a=text.index('Abstract');b=text.index('\nReferences');ex=[]
def exclude(x,y,kind,page):
    assert a<=x<y<=b;ex.append(span(text,x,y,kind=kind,physical_page=page,exact_excluded_text=text[x:y]))
exclude(text.index('Key Words:',a),text.index('1 Introduction',a),'keywords_and_AMS_metadata',1)
for ps in page_spans:
    n=ps['physical_page'];u=ps['start_codepoint'];v=ps['end_codepoint_exclusive']
    if v<=b:
        assert text[u:v].endswith('\n'+str(n))
        exclude(v-len(str(n)),v,'printed_page_footer',n)
docs['N016']={'pdf_path':s['path'],'pdf_sha256':s['sha256'],'pdf_bytes':s['bytes'],'pages':len(pages),'extraction_path':'phase57_ten_source_measurement_sources/N016.txt','extraction_sha256':sha(text.encode()),'extraction_bytes':len(text.encode()),'page_spans':page_spans,'expected_extraction_warnings':warnings,'body':span(text,a,b),'exclusions':ex,'body_pages':list(range(1,8)),'start_rule':'First Abstract heading inclusive','end_rule':'Newline immediately before References on page7; page8 only references','read_extent':'Complete newly acquired eight-page author PDF text and every original page visually inspected; all statements, source corrections, examples and referenced inputs compared to frozen phase41 author-version adapter basis. No publisher-PDF equivalence claim.','retained':'Entire mathematical/historical body, including open-conjecture discussion and all finite example presentations; no inferred reconstruction of missing mirror-overbar extraction.'}
m.body_text(text,docs['N016'])
extractions['N016']={**docs['N016'],'primary_url':'https://gabrielcunningham.com/WhichChiralPolytopes.pdf','edition':'Author manuscript dated July25,2023, eight pages','acquired':'2026-10-10 by ordinary unprivileged curl; no credentials, bypass or escalation','frozen_adapter_basis':'phase41_chiral_cover_source_web.txt','basis_comparison':'Title, date, section/theorem labels, Theorem3.1, Corollaries3.3/3.4/3.7, five-family Example3.5, torus Example3.8 and section4 presentations/counts/conjecture match the frozen author-version basis. PDF visuals confirm lost mirror bars and existing rank-base/nonidentity-power qualifications; publisher-version limitation remains.'}
write('phase57_ten_source_measurement_source_extractions.json',extractions)
write('phase57_ten_source_measurement_source_acquisition.json',{'new_N016':{k:extractions['N016'][k] for k in ['pdf_path','pdf_sha256','pdf_bytes','pages','primary_url','edition','acquired','frozen_adapter_basis','basis_comparison']},'N001':{'url':'https://projecteuclid.org/journals/bulletin-of-the-belgian-mathematical-society-simon-stevin/volume-5/issue-2/Some-properties-of-inductively-minimal-geometries/10.36045/bbms/1103409005.pdf','ordinary_retrieval_result':'HTTP transfer returned1168-byte HTML access page, not PDF; no bypass/retry against access restriction','response_sha256':sha(pathlib.Path('/private/tmp/phase57-N001-publisher.response').read_bytes()),'faithful_primary_PDF_available':False,'numerator_credit':0,'older_browser_record_not_used_for_length':True},'borrowed_N016_interfaces':['Recursive string C+ group/polytope and marked covering correspondence: source [14], [5] Proposition3.13; retained as explicit background with corrected rank base','Depth-two regularity of chiral sections: source [14] Proposition9; retained','Five tight chiral families: source [7] Table4 and its cited Proposition11; retained classification/chirality interface; adapter uses exact selected older version','Smallest/mirror-cover context: source [12] Proposition4.1, [11] Corollary7.5 and Proposition3.16; target consequences rederived in integrated cover branch','Square-torus example: source Example3.8; explicit coordinate proof in integrated square model'], 'older_borrowed_originals_newly_reread':False,'private_source_PDF_export':False})
for key,path in [('Compress_10','phase45_ten_source_manuscript.md'),('required_erratum','phase45_ten_source_errata.md')]:
    binding=bind(path);t=(P/path).read_text();a=t.index('The question addressed here') if key=='Compress_10' else 0
    docs[key]={**binding,'body':span(t,a,len(t)),'exclusions':[],'start_rule':('First substantive introductory paragraph, after title/private status label' if key=='Compress_10' else 'BOF; complete title, hash, old/new correction wording and explanatory metadata count'),'end_rule':'EOF; no exclusions, including all four full programs and references/source inputs in base','format':'markdown_tex'}
erratum=json.loads((P/'phase45_ten_source_errata.json').read_text());base=(P/'phase45_ten_source_manuscript.md').read_text()
assert sha(base.encode())==erratum['manuscript_sha256']
for change in erratum['changes']:assert base.count(change['old'])==1 and change['new'] in (P/'phase45_ten_source_errata.md').read_text()
audit=json.loads((P/'phase52_ten_source_recent_audit.json').read_text())
contract={'source_manuscripts':10,'intake':audit['named_intake'],'independent_mathematical_status':audit['status'],'principal_result_implication':audit['admitted_implication'],'whole_document_every_assertion_rederived':False,'source_rows':audit['source_rows'],'retained_input_limits':audit['retained_input_limits'],'unproved_or_excluded':audit['unproved_or_excluded'],'new_conjecture_solution':False,'new_priority_claim':False,'new_Lean_component':False,'required_erratum':audit['required_erratum'],'measured_source_count':9,'zero_credit_sources':['N001'],'exact_ten_source_factor_available':False,'new_N016_primary_PDF_only_closes_author_version_measurement_gap':True,'annotation_view':'Separate root attribution/margin-note reader is outside this unannotated measurement and is not a proof dependency; its complete length needs a separate measurement if used.'}
bindings=['phase45_ten_source_manifest.json','phase45_ten_source_adapter_map.json','phase45_ten_source_errata.json','phase52_ten_source_recent_audit.json','phase52_ten_source_recent_audit.md','phase52_ten_source_recent_audit_manifest.json','phase43_unified_lower_bound_protocol.json','phase51_compress_C_measurement_protocol.json','phase41_chiral_cover_intake.json','phase41_chiral_cover_ledger.md','phase57_ten_source_measurement_source_acquisition.json']
programs=['phase37_compress_twogroups_census.g','phase40_compress_operations_check.g','phase40_compress_operations_exhaustive.g','phase41_chiral_cover_check.g']
external=[{**bind(f),'role':'Exact executable duplicate of fully included appendix; counted once in manuscript'} for f in programs]
for f in ['phase45_ten_source_verify.py','phase45_ten_source_verify.json','phase52_ten_source_recent_audit_check.py','phase52_ten_source_recent_audit_check.json']:
    external.append({**bind(f),'role':'Integrity/review infrastructure, separately reported; not mathematical proof abbreviation'})
body=(E/'replacement.md').read_text();presented=(E/'render.md').read_text();header=(E/'qed.tex').read_text()
assert body=='\n\n'.join(m.body_text((P/docs[k]['path']).read_text(),docs[k])[0] for k in ['Compress_10','required_erratum'])
rendered,pages,warnings=h.extract(pypdf.PdfReader(E/'replacement.pdf'));assert not warnings
ast=json.loads(subprocess.check_output(['pandoc',str(E/'render.md'),'--from=markdown+tex_math_single_backslash-raw_tex','--to=json']));ai,codes=h.ast_info(ast)
forms=['NFC','NFKC'];metric_keys=oldC['metric_keys']
protocol={'schema':'Compress_10_nine_primary_PDF_full_denominator_lower_bound_v1','status':'author_protocol_pending_independent_measurement_review','date':'2026-10-10','measurement_helper':bind('phase36_compress_forest_measurement.py'),'render_helper':bind('phase43_unified_lower_bound_measure.py'),'source_keys':list(extractions),'replacement_keys':['Compress_10','required_erratum'],'forms':forms,'metric_keys':metric_keys,'documents':docs,'contract':contract,'contract_bindings':[bind(f) for f in bindings],'certificate_programs':[bind(f) for f in programs],'external_costs':external,'expected_toolchain':oldC['expected_toolchain'],
 'render':{'reader':oldC['render']['reader'],'variables':oldC['render']['variables'],'header':header,'header_sha256':sha(header.encode()),'join':'\n\n','page_join':'\n','extensions_to_prior_renderer':'Same literal-PDF metric and phase51 proposed Unicode/prose-notation presentation transform. To prevent clipping in full ten-source text, additionally allow anywhere code wrapping without decorative glyphs, seqsplit inline-code wrapping and 6em emergency stretch. Exact math/code/table AST nodes and full-program extraction are checked. Three exact underfull paragraph warnings are disclosed for visual review; no missing glyph/overfull diagnostics accepted.'},
 'expected_rendering':{'assembled_markdown_sha256':sha(body.encode()),'presentation_markdown_sha256':sha(presented.encode()),'ast':ai,'pages':len(pages),'extraction_sha256':sha(rendered.encode()),'metrics':{f:m.metrics(rendered,f) for f in forms},'accepted_final_latex_diagnostics':['Underfull \\hbox (badness 5862) in paragraph at lines 3645--3652','Underfull \\hbox (badness 7030) in paragraph at lines 3645--3652','Underfull \\hbox (badness 1755) in paragraph at lines 3713--3722'],'literal_probes':['E\\S','E\\T','F*','K=L*','B̃_r','P̂','{4,4}_(2,2)',"Recognition lemma O1.1 supplies the content needed from N013’s quoted Theorem 2.2."],'raster_sha256':{f.name:sha(f.read_bytes()) for f in sorted((E/'replacement').glob('page-*.png'))}},
 'counting_convention':{'primary':'NFC-normalized default-pypdf extraction; sum of nine cleaned full source bodies / full rendered ten-source replacement and entire required erratum. N001 receives exactly zero numerator credit; therefore this is a conservative lower bound, not an exact ten-source factor.','sensitivity':'NFKC with identical boundaries; alphanumeric runs, nonwhitespace and collapsed-whitespace codepoints, and UTF-8 bytes also reported','source_boundaries':'Inherit exact frozen phase43 boundaries for its six acquired PDFs and phase51 for L088/N013, with fresh hash/extraction replay. New N016 author PDF Abstract through References minus keyword/AMS/footer furniture. Post-reference L088 diagrams count.','source_repairs':'None. Original line-end hyphens, ligatures, control glyphs and extraction gaps remain literal. N003/N008 legacy page wrappers are reproduced then excluded by bound spans; these contribute no tokens. Drawn diagram edges are not encoded as additional prose.','denominator':'Complete substantive integrated manuscript through EOF, all four full programs, complete internal lattice proof, all source/dependency accounting and references; then entire required additive erratum including hash and old/new wording. No proof/code/reference-body exclusions. Frozen bytes are not edited.','background':'All declared retained theorem/catalogue inputs remain conditional. Their interfaces/citations count in replacement; external proof bodies/data are not expanded. Exact executable duplicates are verified, not charged twice.','annotations':'Separate attribution-margin annotation layer and its generated reader are outside this baseline; annotation length is not silently treated as measured. No annotation is a mathematical premise.','interpretation':'Representation-sensitive conditional manuscript-length lower bound, pending independent measurement review. Not every-assertion equivalence, minimal proof length, effort compression, novelty, an open-conjecture result, or the prior seven-source ratio.'}}
write('phase57_ten_source_measurement_protocol.json',protocol)
print('protocol SHA256',sha((P/'phase57_ten_source_measurement_protocol.json').read_bytes()))
