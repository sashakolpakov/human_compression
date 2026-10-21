#!/usr/bin/env python3
"""Bind the inspected private source spans and complete rendered denominator.

Author-only builder: requires the separately inspected exploratory rendering.
Never overwrites an existing protocol. The replay runner does not call this.
"""
import hashlib, importlib.util, json, pathlib, subprocess, sys
P=pathlib.Path(__file__).resolve().parent
E=pathlib.Path('/private/tmp/phase51-render-explore')
sha=lambda b:hashlib.sha256(b).hexdigest()
def bind(path):
    b=(P/path).read_bytes(); return {'path':path,'sha256':sha(b),'bytes':len(b)}
def span(t,a,b,**kw): return {'start_codepoint':a,'end_codepoint_exclusive':b,'sha256_utf8':sha(t[a:b].encode()),**kw}
def load(path,name):
    s=importlib.util.spec_from_file_location(name,P/path); m=importlib.util.module_from_spec(s);sys.dont_write_bytecode=True;s.loader.exec_module(m);return m
m=load('phase36_compress_forest_measurement.py','metrics')
h=load('phase38_compress_B_measurement.py','render_helpers')
e=json.loads((P/'phase51_compress_C_measurement_source_extractions.json').read_text())
docs={}
for key,s in e.items():
    t=(P/s['extraction_path']).read_text(); a=t.index('Abstract'); b=len(t) if key=='L088' else t.index('\nReferences'); ex=[]
    def add(x,y,kind,page):
        assert a<=x<y<=b
        ex.append(span(t,x,y,kind=kind,physical_page=page,exact_excluded_text=t[x:y]))
    if key=='L088':
        add(t.index('Keywords:',a),t.index('1. Introduction',a),'keywords_and_MSC_metadata',1)
        x=t.index('9. Acknowledgements',a); y=t.index('References',x)
        add(x,y,'acknowledgment_heading_and_funding_thanks',7)
        add(y,s['page_spans'][8]['start_codepoint'],'bibliography_author_affiliations_and_page8_navigation_but_not_postreference_figures',[7,8])
        for q in s['page_spans']:
            n=q['physical_page'];u=q['start_codepoint'];v=q['end_codepoint_exclusive']
            if n in [1,8]:continue
            header=f'I I G\nJJ II\nJ I\npage {n} / 10\ngo back\nfull screen\nclose\nquit\nACADEMIA\nPRESS\n'
            assert t[u:u+len(header)]==header
            add(u,u+len(header),'interactive_navigation_publisher_furniture',n)
    else:
        add(t.index('2010 Mathematics Subject Classiﬁcation.'),s['page_spans'][0]['end_codepoint_exclusive'],'MSC_keywords_funding_and_page1_footer',1)
        for q in s['page_spans'][1:]:
            n=q['physical_page'];u=q['start_codepoint']
            if u>=b:break
            header=t[u:].split('\n',1)[0]
            assert header.startswith(str(n)+' ') or header.endswith(' '+str(n))
            add(u,u+len(header),'running_title_or_author_header_and_page_number',n)
    docs[key]={**s,'body':span(t,a,b),'exclusions':sorted(ex,key=lambda z:z['start_codepoint']),
        'body_pages':([1,2,3,4,5,6,7,9,10] if key=='L088' else list(range(1,11))),
        'start_rule':'First Abstract heading, inclusive',
        'end_rule':('EOF; retain the mathematical figure pages 9 and 10 after References' if key=='L088' else 'Newline before References, exclusive; page11 bibliography/affiliations only'),
        'read_extent':'Fresh complete default-pypdf extraction read; every original PDF page visually inspected at 100dpi for body/exclusion boundaries. This is a measurement-boundary review, not a new independent proof review.',
        'retained':'All mathematical/historical prose, auxiliaries, proof material, diagram glyphs and captions. No OCR, glyph/control-character repairs, or hyphen joining.'}
    m.body_text(t,docs[key])
for key,path in [('Compress_C','phase40_compress_operations_manuscript.md'),('lattice_bridge','phase45_ten_source_toroid_bridge.md')]:
    binding=bind(path);t=(P/path).read_text();a=t.index('This manuscript recovers') if key=='Compress_C' else 0
    docs[key]={**binding,'body':span(t,a,len(t)),'exclusions':[],
        'start_rule':('After title and private-version label; first substantive paragraph retained' if key=='Compress_C' else 'BOF, including the entire title, date/status paragraph, every proof, citation and source/proof accounting paragraph'),
        'end_rule':'EOF; no exclusions','format':'markdown_tex'}
audit=json.loads((P/'phase44_operations_recent_audit.json').read_text())
intake=json.loads((P/'phase40_compress_operations_intake.json').read_text())
contract={'source_manuscripts':2,'source_versions':audit['source_map'],'replacement':'Complete Compress_C plus entire required lattice bridge','independent_mathematical_status':audit['status'],'principal_clause_rows':[r for r in audit['statement_rows'] if r['principal']], 'principal_clause_count':18,'whole_document_equivalence':False,'retained_inputs':audit['retained_inputs'],
    'excluded_claims':['L108 is not an intake source','N013 comparative claim against every example of its reference9 is not independently verified','N013 auxiliary S(P) isomorphism is not used/proved','N013 Remark4.1 has a rank>=4 qualification; blanket rank3 version is not credited','No absence of all rank>=5 C-groups: the exhaustive result concerns thin regular geometries','No conjecture, priority, complete Lean formalization or ten-source integration claim'],
    'corrections':['L088 printed figure labels Gamma3/Gamma4 are transposed relative to definitions; definitions control','C alone retained target toroidal identifications. Entire independently approved additive bridge is essential and charged here. Frozen historical review-status statements are preserved, not silently updated.']}
bindings=['phase40_compress_operations_manifest.json','phase40_compress_operations_intake.json','phase40_compress_operations_ledger.json','phase44_operations_recent_audit.md','phase44_operations_recent_audit.json','phase44_operations_recent_audit_manifest.json']
external=[]
for path,role in [('phase40_compress_operations_check.g','Exact executable duplicate of included Appendix A; not counted twice'),('phase40_compress_operations_exhaustive.g','Exact executable duplicate of included Appendix B; not counted twice'),('phase40_compress_operations_verify.py','Execution/integrity wrapper; separate infrastructure cost'),('phase40_compress_operations_verify.json','Author finite-certificate report'),('phase40_compress_operations_check.log','Author construction log'),('phase40_compress_operations_exhaustive.log','Author exhaustive-census log'),('phase40_compress_operations_exhaustive_classes.json','Finite class certificate output'),('phase40_compress_operations_source_freeze.json','Bound group-data/toolchain metadata')]:external.append({**bind(path),'role':role})
header=(E/'qed.tex').read_text(); presented=(E/'render.md').read_text(); body=(E/'replacement.md').read_text()
assert body=='\n\n'.join(m.body_text((P/docs[k]['path']).read_text(),docs[k])[0] for k in ['Compress_C','lattice_bridge'])
import pypdf
rendered,pages,warnings=h.extract(pypdf.PdfReader(E/'replacement.pdf'));assert not warnings
ast=json.loads(subprocess.check_output(['pandoc',str(E/'render.md'),'--from=markdown+tex_math_single_backslash-raw_tex','--to=json']))
ai,codes=h.ast_info(ast)
forms=['NFC','NFKC'];metric_keys=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
protocol={'schema':'Compress_C_two_primary_PDF_complete_denominator_v1','status':'author_measurement_protocol_pending_independent_review','date':'2026-10-10','measurement_helper':bind('phase36_compress_forest_measurement.py'),'render_helper':bind('phase38_compress_B_measurement.py'),'source_keys':['L088','N013'],'replacement_keys':['Compress_C','lattice_bridge'],'forms':forms,'metric_keys':metric_keys,'documents':docs,'contract':contract,'contract_bindings':[bind(f) for f in bindings],'certificate_programs':[bind(f) for f in ['phase40_compress_operations_check.g','phase40_compress_operations_exhaustive.g']],'external_costs':external,
    'expected_toolchain':{'pypdf':'6.13.0','pandoc_first_line':'pandoc 3.10','xelatex_first_line':'XeTeX 3.141592653-2.6-0.999998 (TeX Live 2026/Homebrew)'},
    'render':{'reader':'markdown+tex_math_single_backslash-raw_tex','variables':['pagestyle:empty','geometry:margin=1in','papersize:letter','fontsize:10pt','mainfont:STIXGeneral','monofont:Menlo'],'header':header,'header_sha256':sha(header.encode()),'join':'\n\n','page_join':'\n',
        'extensions_to_phase38_renderer':'Same source extraction, normalization, metric, 10pt/letter/1-inch layout. Rendering-only presentation copy escapes prose underscores and duality stars after capital letters, preserving all delimited math/code; raw TeX disabled so literal set differences do not become commands. STIXGeneral body/Menlo mono/STIX Two Text script-digit fallback prevent missing glyphs. Code continuation arrows suppressed. Exact math/code/table AST and full code PDF token preservation checked. One exact underfull spacing diagnostic is disclosed and visually accepted by author; no missing/overfull warnings accepted.'},
    'expected_rendering':{'assembled_markdown_sha256':sha(body.encode()),'presentation_markdown_sha256':sha(presented.encode()),'ast':ai,'pages':len(pages),'extraction_sha256':sha(rendered.encode()),'metrics':{f:m.metrics(rendered,f) for f in forms},'accepted_final_latex_diagnostics':['Underfull \\hbox (badness 1490) in paragraph at lines 632--642'],'literal_probes':['E\\S','E\\T','F*','K=L*','B̃_r','P̂','{4,4}_(2,2)'],'raster_sha256':{f.name:sha(f.read_bytes()) for f in sorted((E/'replacement').glob('page-*.png'))}},
    'counting_convention':{'primary':'NFC-normalized default pypdf extraction; sum of whitespace-delimited tokens from both cleaned full source bodies divided by complete rendered replacement plus full lattice bridge, including both complete GAP appendices','sensitivity':'NFKC same rule; alphanumeric runs, nonwhitespace codepoints, collapsed-whitespace codepoints, UTF-8 bytes also reported','repairs':'None in source extraction. Original line-end hyphens, ligatures, legacy font/control-character artefacts and mathematical/diagram glyphs remain literal before normalization. Text extraction does not encode the geometric information in drawn edges or images.','source_exclusions':'Only exact hash-bound title/byline/date/arXiv/page/navigation/keyword/MSC/acknowledgment/bibliography/affiliation metadata. Both post-bibliography L088 figure pages retained.','denominator':'Entire substantive C through Appendices A/B, including mixed References and retained inputs section; entire lattice note including title/version/status/source accounting. No theorem/proof/code/metadata removed from bridge. Conservative mixed bibliographic and dependency prose also counts.','imports':'Named retained background remains conditional proof cost. Its replacement interfaces/disclosures count; external theorem proof bodies and group catalogue data are not expanded.','certificates':'Both GAP programs count in full once. Exact executable duplicates and outputs/wrapper bytes separately listed, not silently treated as free external lemmas.','interpretation':'Candidate representation-sensitive conditional main-result manuscript length factor. Not whole-document equivalence, shortest-proof complexity, effort ratio or automatic proof check. A value below one means expansion under this metric. No existing seven-source or four-source factor is transferred.'}}
target=P/'phase51_compress_C_measurement_protocol.json'
with target.open('x',encoding='utf-8') as f:json.dump(protocol,f,indent=2,ensure_ascii=False);f.write('\n')
print(target.name,sha(target.read_bytes()))
