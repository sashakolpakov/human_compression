#!/usr/bin/env python3
"""Author exploration render; does not admit a length ratio or visual review."""
import argparse,hashlib,importlib.util,json,os,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def require(ok,msg):
    if not ok:raise ValueError(msg)
def load(name,path,expected):
    require(sha((ROOT/path).read_bytes())==expected,'Helper hash changed')
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    m=importlib.util.module_from_spec(spec);sys.dont_write_bytecode=True;spec.loader.exec_module(m);return m
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output-dir',type=Path,required=True)
    a=p.parse_args();out=a.output_dir.absolute();require(not os.path.lexists(out),'Fresh output directory required')
    raw=(ROOT/'phase84_eleven_measurement_protocol.json').read_bytes()
    require(sha(raw)=='7862cfcaa472b52eb94aeca47f77f47afbf7c33ae2fc47df1a78651e84623962','Baseline changed')
    old=json.loads(raw)
    h=load('phase98_render',old['render_helper']['path'],old['render_helper']['sha256'])
    m=load('phase98_metrics',old['measurement_helper']['path'],old['measurement_helper']['sha256'])
    predecessor=load('phase98_predecessor','phase84_eleven_measurement.py','48eab4238059d5477164454ba446551ecff7cdd17e02d468902cb6529391880e')
    source=(ROOT/'phase78_n009_integration_manuscript.md').read_bytes()
    require(sha(source)=='15dd00e3845526dc40bb0effa07652e32748958238759eae9a856d901071b801','Manuscript changed')
    text=source.decode();start=text.index('The question addressed here');require(start==161,'Body start changed')
    body=text[start:];presented=predecessor.presentation_copy(body)
    out.mkdir(parents=True);(out/'replacement.md').write_text(body);(out/'render.md').write_text(presented)
    header=old['render']['header']+'\n'+''.join('\\newunicodechar{'+c+'}{{\\numeralfallback\\char"'+format(ord(c),'X')+'\\relax}}\n' for c in '⁻⁸ⁱ⁴⁷⁶⁵₈')
    for c,letter in [('ᵢ','i'),('ⱼ','j'),('ₜ','t')]:header+='\\newunicodechar{'+c+'}{\\textsubscript{'+letter+'}}\n'
    (out/'qed.tex').write_text(header)
    commands=[]
    def run(label,cmd):
        r=subprocess.run(cmd,cwd=out,text=True,capture_output=True)
        (out/(label+'.stdout.txt')).write_text(r.stdout);(out/(label+'.stderr.txt')).write_text(r.stderr)
        commands.append(dict(label=label,argv=cmd,returncode=r.returncode))
        require(r.returncode==0,'Command failed '+label);return r
    progs={n:h.program_info(n) for n in ['pandoc','xelatex','gs']}
    pandoc=progs['pandoc']['path'];reader='--from='+old['render']['reader']
    for label,md in [('ast','render.md'),('source-ast','replacement.md')]:
        run(label,[pandoc,md,reader,'--to=json','--output='+label+'.json'])
    ast=json.loads((out/'ast.json').read_text());source_ast=json.loads((out/'source-ast.json').read_text())
    def nodes(node,typ):
        found=[]
        def walk(n):
            if isinstance(n,dict):
                if n.get('t')==typ:found.append(n['c'])
                for v in n.values():walk(v)
            elif isinstance(n,list):
                for v in n:walk(v)
        walk(node);return found
    require(all(nodes(ast,t)==nodes(source_ast,t) for t in ['Math','CodeBlock','Table']),'AST math/code/table changed')
    info,codes=h.ast_info(ast)
    blocks=re.findall(r'```(gap|python)\n(.*?)\n```',body,re.S)
    paths=['phase78_n009_integration_census.g','phase40_compress_operations_check.g','phase40_compress_operations_exhaustive.g','phase41_chiral_cover_check.g','phase65_petrial_integration_check.py','phase78_n009_integration_finite.g','phase78_n009_integration_data.g','phase78_n009_integration_run.py']
    require([l for l,c in blocks]==['gap']*4+['python','gap','gap','python'],'Eight full appendix blocks required')
    require(codes[-8:]==[c for l,c in blocks],'Full blocks not at end of AST')
    for (_,code),path in zip(blocks,paths):require((code+'\n').encode()==(ROOT/path).read_bytes(),'Full appendix differs '+path)
    require(sum(len((c+'\n').encode()) for l,c in blocks)==79874,'Full code/data byte cost differs')
    template=run('template',[pandoc,'--print-default-template=latex']);(out/'default-template.tex').write_text(template.stdout)
    args=[reader,'--standalone','--to=latex','--include-in-header=qed.tex']
    for v in old['render']['variables']:args+=['--variable',v]
    run('latex',[pandoc,'render.md',*args,'--output=replacement.tex'])
    diagnostics=[]
    for i in [1,2]:
        run('xelatex-pass'+str(i),[progs['xelatex']['path'],'-interaction=nonstopmode','-halt-on-error','-recorder','replacement.tex'])
        log=(out/'replacement.log').read_text();(out/f'xelatex-pass{i}.log').write_text(log)
        diagnostics.append([s for s in log.splitlines() if re.search(r'Warning:|Overfull \\[hv]box|Underfull \\[hv]box|Missing character:|Missing glyph',s,re.I)])
    import pypdf
    extracted,pages,warnings=h.extract(pypdf.PdfReader(out/'replacement.pdf'))
    (out/'replacement_extraction.txt').write_text(extracted)
    norm=lambda s:re.sub(r'\s+','',s)
    cursor=0
    for i,code in enumerate(codes):
        at=norm(extracted).find(norm(code),cursor);require(at>=0,'Extracted code block missing '+str(i));cursor=at+len(norm(code))
    require(extracted.count('■')==info['qed_marks'],'Proof marker loss')
    raster=run('rasterize',[progs['gs']['path'],'-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r130','-sOutputFile=page-%02d.png','replacement.pdf'])
    report=dict(status='AUTHOR_EXPLORATION_NOT_VISUALLY_REVIEWED',body_start=start,body_sha256=sha(body.encode()),presentation_sha256=sha(presented.encode()),
                pages=len(pages),ast=info,diagnostics=diagnostics,extraction_warnings=warnings,extraction_sha256=sha(extracted.encode()),
                metrics={f:m.metrics(extracted,f) for f in old['forms']},all_code_complete=True,full_code_data_bytes=79874,
                programs=progs,commands=commands,raster_sha256={f.name:sha(f.read_bytes()) for f in sorted(out.glob('page-*.png'))})
    (out/'exploration.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','pages','ast','diagnostics','metrics']}))
if __name__=='__main__':main()
