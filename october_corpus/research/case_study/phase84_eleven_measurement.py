#!/usr/bin/env python3
"""Replay the complete eleven-source integrated manuscript with all five programs PDF-length experiment.

Requires the private primary PDFs. Writes only a NEW output directory. Does not
execute the geometry certificates, copy primary sources, or establish a proof.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, os, platform, re, subprocess, sys, unicodedata
from pathlib import Path
HERE=Path(__file__).resolve().parent
PROTOCOL_NAME='phase84_eleven_measurement_protocol.json'
PROTOCOL_SHA256='7862cfcaa472b52eb94aeca47f77f47afbf7c33ae2fc47df1a78651e84623962'
sha=lambda b:hashlib.sha256(b).hexdigest()

def read_bound(path, expected):
    data=path.read_bytes()
    if sha(data)!=expected: raise ValueError('Bound input changed: '+str(path))
    return data

def load_helper(root, binding, name):
    read_bound(root/binding['path'],binding['sha256'])
    spec=importlib.util.spec_from_file_location(name,root/binding['path'])
    module=importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode=True
    spec.loader.exec_module(module)
    return module

def presentation_copy(text):
    r"""Only escape prose notation that Markdown would mistake for emphasis.

    Entire fenced/indented code, inline code, and delimited math stay byte exact.
    Outside them, underscores and duality stars after capital letters are
    escaped. The reader separately disables raw TeX so E\S remains a literal
    set difference. No prose, mathematical symbol or code token is deleted.
    """
    protected=re.compile(r'```[^\n]*\n.*?\n```|(?m:^(?: {4}[^\n]*(?:\n|$))+)|`[^`\n]+`|\\\[.*?\\\]|\\\(.*?\\\)|\$\$.*?\$\$|(?<!\\)\$[^$\n]+\$',re.S)
    def escape(s): return re.sub(r'(?<=[A-Z])\*(?!\*)',r'\\*',s.replace('_',r'\_'))
    chunks=[]; cursor=0
    for match in protected.finditer(text):
        chunks.extend([escape(text[cursor:match.start()]),match.group()]); cursor=match.end()
    chunks.append(escape(text[cursor:])); return ''.join(chunks)

def write_json(path,data):
    with path.open('x',encoding='utf-8') as f: json.dump(data,f,indent=2,ensure_ascii=False); f.write('\n')

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input-root',type=Path,default=HERE)
    ap.add_argument('--protocol',type=Path,default=HERE/PROTOCOL_NAME)
    ap.add_argument('--output-dir',type=Path,required=True)
    ap.add_argument('--rasterize',action='store_true')
    ap.add_argument('--allow-toolchain-drift',action='store_true',help='Diagnostic only; changed results need fresh review')
    args=ap.parse_args(); root=args.input_root.resolve(); out=args.output_dir.expanduser().absolute()
    if os.path.lexists(out): raise FileExistsError('Refusing existing output directory: '+str(out))
    p=json.loads(read_bound(args.protocol,PROTOCOL_SHA256))
    m=load_helper(root,p['measurement_helper'],'phase84_bound_metrics')
    h=load_helper(root,p['render_helper'],'phase84_bound_render')
    import pypdf
    programs={k:h.program_info(k) for k in ['pandoc','xelatex']+(['gs'] if args.rasterize else [])}
    drift={}
    for k in ['pandoc','xelatex']:
        if programs[k]['first_line']!=p['expected_toolchain'][k+'_first_line']: drift[k]=programs[k]['first_line']
    if pypdf.__version__!=p['expected_toolchain']['pypdf']: drift['pypdf']=pypdf.__version__
    if drift and not args.allow_toolchain_drift: raise RuntimeError('Toolchain drift: '+json.dumps(drift))
    for binding in p['contract_bindings']+p['external_costs']: read_bound(root/binding['path'],binding['sha256'])
    inherited=json.loads(read_bound(root/'phase57_ten_source_measurement_protocol.json','95971c144cc73ef4321d18ad1ab8bdd347796b39ce2e9dc2e81f4b028ea22063'))
    for key in p['source_keys']:
        if p['documents'][key]!=inherited['documents'][key]: raise ValueError('Inherited source specification changed: '+key)
    docs={}
    for key in p['source_keys']:
        s=p['documents'][key]; read_bound(root/s['pdf_path'],s['pdf_sha256'])
        text,pages,warnings=h.extract_primary(root/s['pdf_path'],pypdf)
        if s.get('extraction_format')=='N003_legacy_markers': text=''.join(f'\n--- PDF PAGE {i+1} ---\n'+q+'\n' for i,q in enumerate(pages))
        if s.get('extraction_format')=='N008_legacy_markers': text='\n\n'.join(f'[[PDF PAGE {i+1}; PRINTED {169+i}]]\n'+q for i,q in enumerate(pages))
        if warnings!=s['expected_extraction_warnings']: raise ValueError('Primary extraction diagnostics changed: '+key)
        if sha(text.encode())!=s['extraction_sha256'] or len(pages)!=s['pages']: raise ValueError('Primary extraction changed: '+key)
        for page,binding in zip(pages,s['page_spans']):
            if sha(page.encode())!=binding['sha256_utf8']: raise ValueError('Primary page changed: '+key)
        body,ex=m.body_text(text,s)
        docs[key]={'pdf_path':s['pdf_path'],'pdf_sha256':s['pdf_sha256'],'pdf_pages':len(pages),'body_pages':s['body_pages'],'fresh_extraction_sha256':sha(text.encode()),'extraction_warnings':warnings,'selected_body':s['body'],'exclusions':ex,'cleaned_body_sha256':sha(body.encode()),'metrics':{f:m.metrics(body,f) for f in p['forms']},'nonwhitespace_control_codepoints':sorted({ord(c) for c in body if ord(c)<32 and not c.isspace()})}
    pieces=[]
    for key in p['replacement_keys']:
        s=p['documents'][key]; text=read_bound(root/s['path'],s['sha256']).decode()
        body,_=m.body_text(text,s); pieces.append(body)
    body=p['render']['join'].join(pieces); presented=presentation_copy(body)
    if sha(body.encode())!=p['expected_rendering']['assembled_markdown_sha256']: raise ValueError('Assembly changed')
    if sha(presented.encode())!=p['expected_rendering']['presentation_markdown_sha256']: raise ValueError('Presentation transform changed')
    out.mkdir(parents=False)
    (out/'replacement.md').write_text(body); (out/'render.md').write_text(presented)
    (out/'qed.tex').write_text(p['render']['header'])
    if sha(p['render']['header'].encode())!=p['render']['header_sha256']: raise ValueError('Header hash mismatch')
    commands=[]
    def run(label,argv):
        r=subprocess.run(argv,cwd=out,capture_output=True,text=True)
        (out/(label+'.stdout.txt')).write_text(r.stdout); (out/(label+'.stderr.txt')).write_text(r.stderr)
        commands.append({'label':label,'argv':argv,'cwd':str(out),'returncode':r.returncode})
        if r.returncode: raise RuntimeError(label+' failed; inspect '+str(out))
        return r
    pandoc=programs['pandoc']['path']; readeropt='--from='+p['render']['reader']
    run('ast',[pandoc,'render.md',readeropt,'--to=json','--output=ast.json'])
    ai,codes=h.ast_info(json.loads((out/'ast.json').read_text()))
    if ai!=p['expected_rendering']['ast']: raise ValueError('AST changed')
    # Compare the source AST as well: the transform must preserve every math
    # node, code block, table, proof marker and displayed-formula body.
    run('source-ast',[pandoc,'replacement.md',readeropt,'--to=json','--output=source-ast.json'])
    original=json.loads((out/'source-ast.json').read_text())
    def typed_nodes(node,typ):
        result=[]
        def walk(x):
            if isinstance(x,dict):
                if x.get('t')==typ: result.append(x['c'])
                for y in x.values(): walk(y)
            elif isinstance(x,list):
                for y in x: walk(y)
        walk(node); return result
    final_ast=json.loads((out/'ast.json').read_text())
    for typ in ['Math','CodeBlock','Table']:
        if typed_nodes(original,typ)!=typed_nodes(final_ast,typ): raise ValueError('Presentation altered '+typ)
    program_blocks=re.findall(r'```(gap|python)\n(.*?)\n```',body,re.S)
    full_codes=[code for language,code in program_blocks]
    if [language for language,code in program_blocks]!=['gap']*4+['python'] or codes[-5:]!=full_codes:
        raise ValueError('Complete GAP/Python appendices changed')
    if len(p['certificate_programs'])!=5: raise ValueError('Five complete programs required')
    for code,binding in zip(full_codes,p['certificate_programs']):
        if (code+'\n').encode()!=read_bound(root/binding['path'],binding['sha256']): raise ValueError('Executable differs from full appendix')
    options=[readeropt,'--standalone','--to=latex','--include-in-header=qed.tex']
    for v in p['render']['variables']: options+=['--variable',v]
    template=run('template',[pandoc,'--print-default-template=latex']); (out/'default-template.tex').write_text(template.stdout)
    run('latex',[pandoc,'render.md',*options,'--output=replacement.tex'])
    pass_warnings=[]
    for n in [1,2]:
        run('xelatex-pass'+str(n),[programs['xelatex']['path'],'-interaction=nonstopmode','-halt-on-error','-recorder','replacement.tex'])
        log=(out/'replacement.log').read_text(); (out/f'xelatex-pass{n}.log').write_text(log)
        pass_warnings.append([x for x in log.splitlines() if re.search(r'Warning:|Overfull \\[hv]box|Underfull \\[hv]box|Missing character:|Missing glyph',x,re.I)])
    if pass_warnings[-1]!=p['expected_rendering']['accepted_final_latex_diagnostics']: raise RuntimeError('Changed final diagnostics: '+repr(pass_warnings[-1]))
    reader=pypdf.PdfReader(out/'replacement.pdf'); rendered,pages,warnings=h.extract(reader)
    (out/'replacement_extraction.txt').write_text(rendered)
    if warnings: raise RuntimeError('Replacement extraction warnings: '+str(warnings))
    norm=lambda x:re.sub(r'\s+','',x)
    cursor=0
    for code in codes:
        where=norm(rendered).find(norm(code),cursor)
        if where<0: raise ValueError('Complete code block missing in extracted PDF')
        cursor=where+len(norm(code))
    # Exact small prose notation probes catch the initially observed Markdown
    # interpretation failures. They supplement, not replace, the visual review.
    for probe in p['expected_rendering']['literal_probes']:
        if norm(probe) not in norm(rendered): raise ValueError('Lost literal notation: '+probe)
    rendered_metrics={f:m.metrics(rendered,f) for f in p['forms']}; baseline=p['expected_rendering']
    checks={'pages':len(pages)==baseline['pages'],'extraction_hash':sha(rendered.encode())==baseline['extraction_sha256'],'metrics':rendered_metrics==baseline['metrics'],'all_qed_marks':rendered.count('■')==ai['qed_marks'],'all_eleven_code_blocks_complete_and_ordered':True,'all_five_GAP_and_Python_programs_byte_exact':True,'math_code_table_AST_unchanged':True,'literal_notation_probes':True,'final_latex_diagnostics_exactly_reviewed':True,'source_extractions_exact':True,'nine_source_specifications_identical_to_phase57':True}
    if not all(checks.values()) and not args.allow_toolchain_drift: raise ValueError('Rendered baseline changed: '+str(checks))
    raster_hashes={}
    if args.rasterize:
        r=run('rasterize',[programs['gs']['path'],'-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r130','-sOutputFile=page-%02d.png','replacement.pdf'])
        if re.search(r'Error|Warning|repair',r.stdout+'\n'+r.stderr,re.I): raise RuntimeError('Rasterizer diagnostic requires review')
        raster_hashes={f.name:sha(f.read_bytes()) for f in sorted(out.glob('page-*.png'))}
        checks['all_page_rasters_match_author_visual_baseline']=raster_hashes==baseline['raster_sha256']
        if not checks['all_page_rasters_match_author_visual_baseline'] and not args.allow_toolchain_drift: raise ValueError('Raster baseline changed')
    sums={f:{k:sum(docs[d]['metrics'][f][k] for d in p['source_keys']) for k in p['metric_keys']} for f in p['forms']}
    ratios={f:{k:{'numerator':sums[f][k],'denominator':rendered_metrics[f][k],'factor':sums[f][k]/rendered_metrics[f][k]} for k in p['metric_keys']} for f in p['forms']}
    fonts=set()
    for page in reader.pages:
        for ref in page['/Resources'].get_object().get('/Font',{}).get_object().values(): fonts.add(str(ref.get_object().get('/BaseFont')))
    tex_inputs={}
    for line in (out/'replacement.fls').read_text().splitlines():
        if line.startswith('INPUT '):
            q=Path(line[6:]); q=q if q.is_absolute() else out/q
            if q.is_file() and out not in q.resolve().parents: tex_inputs[str(q.resolve())]=sha(q.read_bytes())
    report={'schema':'Compress_11_nine_source_conservative_PDF_lower_bound_v1','status':'reproducible_author_measurement_pending_independent_review','protocol_sha256':PROTOCOL_SHA256,'runner_sha256':sha(Path(__file__).read_bytes()),'output_directory':str(out),'environment':{'python':sys.version,'python_executable':sys.executable,'platform':platform.platform(),'unicode_database':unicodedata.unidata_version,'pypdf_version':pypdf.__version__,'pypdf_module_sha256':sha(Path(pypdf.__file__).read_bytes()),'programs':programs,'toolchain_drift':drift},'contract':p['contract'],'contract_bindings':p['contract_bindings'],'source_documents':docs,'source_body_sums':sums,'replacement':{'inputs':[p['documents'][k] for k in p['replacement_keys']],'raw_markdown_metrics':{f:m.metrics(body,f) for f in p['forms']},'rendered_metrics':rendered_metrics,'rendered_extraction_sha256':sha(rendered.encode()),'pages':len(pages),'complete_integrated_lattice_proof_included':True,'all_four_complete_GAP_appendices_included':True,'complete_Python_appendix_included':True,'Petrial_corrections_and_infinite_proof_fully_charged':True,'required_reference_erratum_incorporated_not_double_appended':True},'conservative_lower_bounds_under_declared_convention':ratios,'N001_credit':0,'L108_credit':0,'exact_eleven_source_factor':None,'rendering':{'ast':ai,'commands':commands,'xelatex_pass_diagnostics':pass_warnings,'embedded_font_names':sorted(fonts),'tex_input_hashes':tex_inputs,'checks':checks,'raster_sha256':raster_hashes,'visual_review_automated':False},'external_costs':p['external_costs'],'counting_convention':p['counting_convention'],'source_text_exported':False,'source_pdf_exported':False,'whole_document_equivalence_claim':False,'mathematical_proof_check_performed_by_this_runner':False}
    # Recheck bound local inputs after render: no frozen input may change mid-run.
    for binding in p['contract_bindings']+p['external_costs']+[p['measurement_helper'],p['render_helper']]:
        read_bound(root/binding['path'],binding['sha256'])
    for key in p['source_keys']:
        d=p['documents'][key]; read_bound(root/d['pdf_path'],d['pdf_sha256'])
    for key in p['replacement_keys']:
        d=p['documents'][key]; read_bound(root/d['path'],d['sha256'])
    read_bound(args.protocol,PROTOCOL_SHA256)
    report['rendering']['checks']['bound_inputs_unchanged_after_run']=True
    write_json(out/'report.json',report)
    write_json(out/'manifest.json',{'files':{f.name:sha(f.read_bytes()) for f in sorted(out.iterdir()) if f.is_file()},'source_text_or_pdf_included':False})
    print(json.dumps({'status':report['status'],'report_sha256':sha((out/'report.json').read_bytes()),'NFC':ratios['NFC'],'NFKC':ratios['NFKC'],'checks':checks},indent=2))

if __name__=='__main__': main()
