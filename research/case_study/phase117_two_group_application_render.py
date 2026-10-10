#!/usr/bin/env python3
"""A normal-page author rendering of A, not a source/replacement ratio.

Complete mathematical prose, tables, references and the certificate interface
are included. Four full external programs/data and U remain additional charged
proof inputs; this PDF's page count is never the complete proof-package cost.
"""
import argparse, hashlib, importlib.util, json, re, shutil, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-dir',type=Path,required=True)
    ap.add_argument('--rasterize',action='store_true')
    a=ap.parse_args();out=a.output_dir
    if out.exists(): raise SystemExit('Refusing existing output directory')
    source=ROOT/'phase117_two_group_application.md';body=source.read_text()
    p=json.loads((ROOT/'phase98_twelve_measurement_protocol.json').read_text())
    if sha((ROOT/'phase98_twelve_measurement_protocol.json').read_bytes())!='f297f3509ba598b5fc375e101a21e7381049d38d6cb27717c5287cc77b89f0ee':
        raise SystemExit('Rendering protocol changed')
    helper=ROOT/'phase98_twelve_measurement.py'
    if sha(helper.read_bytes())!='4bf9e51773a6c719c90132cc2ea82ae16d038a77a9e5e74a99333a588fa479ec':
        raise SystemExit('Rendering transform helper changed')
    sys.dont_write_bytecode=True
    spec=importlib.util.spec_from_file_location('phase117_render_transform',helper)
    h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h)
    out.mkdir(parents=True)
    (out/'source.md').write_text(body);(out/'render.md').write_text(h.presentation_copy(body))
    (out/'header.tex').write_text(p['render']['header'])
    commands=[]
    def run(label,args):
        r=subprocess.run(args,cwd=out,capture_output=True,text=True)
        (out/(label+'.stdout')).write_text(r.stdout);(out/(label+'.stderr')).write_text(r.stderr)
        commands.append(dict(label=label,argv=args,returncode=r.returncode))
        if r.returncode:raise RuntimeError(label+' failed')
    pandoc=shutil.which('pandoc');xelatex=shutil.which('xelatex')
    if not pandoc or not xelatex: raise RuntimeError('Pandoc/XeLaTeX unavailable')
    reader='--from='+p['render']['reader']
    for n in ['source','render']:
        run(n+'-ast',[pandoc,n+'.md',reader,'--to=json','--output='+n+'.json'])
    def nodes(tree,typ):
        found=[]
        def walk(x):
            if isinstance(x,dict):
                if x.get('t')==typ:found.append(x['c'])
                for y in x.values():walk(y)
            elif isinstance(x,list):
                for y in x:walk(y)
        walk(tree);return found
    ast0=json.loads((out/'source.json').read_text());ast1=json.loads((out/'render.json').read_text())
    for typ in ['Math','Table','CodeBlock']:
        if nodes(ast0,typ)!=nodes(ast1,typ):raise RuntimeError('Changed '+typ)
    opts=[reader,'--standalone','--to=latex','--include-in-header=header.tex']
    variables=['geometry:margin=1in','papersize:a4','fontsize:11pt','mainfont:STIXGeneral','monofont:Menlo']
    for v in variables:opts+=['--variable',v]
    run('latex',[pandoc,'render.md',*opts,'--output=application.tex'])
    for n in [1,2]:run('xelatex'+str(n),[xelatex,'-interaction=nonstopmode','-halt-on-error','application.tex'])
    log=(out/'application.log').read_text()
    diagnostics=[x for x in log.splitlines() if re.search(r'Warning:|Overfull \\[hv]box|Underfull \\[hv]box|Missing character:|Missing glyph',x,re.I)]
    import pypdf
    pdf=pypdf.PdfReader(out/'application.pdf')
    extracted='\n'.join(page.extract_text() or '' for page in pdf.pages)
    (out/'application_extraction.txt').write_text(extracted)
    if a.rasterize:run('rasterize',[shutil.which('gs'),'-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile=page-%02d.png','application.pdf'])
    if source.read_text()!=body: raise RuntimeError('Manuscript changed during rendering; discard output')
    report=dict(status='author_render_not_independently_reviewed',manuscript=dict(path=source.name,sha256=sha(source.read_bytes())),
      page_format=dict(variables=variables),pages=len(pdf.pages),commands=commands,diagnostics=diagnostics,
      AST_preserved=True,PDF_sha256=sha((out/'application.pdf').read_bytes()),
      complete_external_programs_included_in_pdf=False,external_programs_fully_charged_separately=True,
      umbrella_included_in_pdf=False,umbrella_required_and_charged_separately=True,
      complete_proof_package_pages=None,source_ratio=None,visual_inspection_completed=False)
    (out/'render_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(pages=len(pdf.pages),diagnostics=diagnostics,complete_package_cost=None,ratio=None)))
if __name__=='__main__':main()
