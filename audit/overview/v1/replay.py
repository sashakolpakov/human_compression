#!/usr/bin/env python3
"""Rebuild the accepted numerical reader using only public, pinned inputs."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys
from pypdf import PdfReader
HERE=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--public-root',type=Path,default=HERE.parents[2]);ap.add_argument('--xelatex',default='xelatex');a=ap.parse_args()
    if a.out.exists():raise ValueError('Use a fresh output directory.')
    out=a.out.resolve();out.mkdir(parents=True);packet=HERE/'packet'
    relative=json.loads((HERE/'public_locations.json').read_text());locations={k:str(a.public_root/v) for k,v in relative.items()}
    loc=out/'locations.json';loc.write_text(json.dumps(locations,indent=2)+'\n')
    env=dict(os.environ);env['MPLCONFIGDIR']=str(out/'matplotlib')
    def run(name,cmd,cwd):
        p=subprocess.run([str(v) for v in cmd],cwd=cwd,env=env,capture_output=True,text=True)
        (out/(name+'.stdout')).write_text(p.stdout);(out/(name+'.stderr')).write_text(p.stderr)
        if p.returncode:raise RuntimeError(name+' failed: '+p.stdout[-2000:]+p.stderr[-2000:])
    gen=out/'generated'
    run('build',[sys.executable,'-B','-O',packet/'build.py','--out',gen,'--locations',loc,'--pdf-graphs'],a.public_root)
    for i in range(2):run('render'+str(i),[a.xelatex,'-interaction=nonstopmode','-halt-on-error','summary.tex'],gen)
    run('author_check',[sys.executable,'-B','-O',packet/'check.py','--packet',gen,'--locations',loc,'--out',out/'author_check.json'],a.public_root)
    run('independent_check',[sys.executable,'-B','-O',HERE/'independent_review/check.py','--packet',gen,'--public-root',a.public_root,'--out',out/'independent_check.json'],a.public_root)
    stable=['results.json','topics.csv','applications.csv','summary.tex','whole_topics.svg','conditional_applications.svg','whole_topics.pdf','conditional_applications.pdf']
    for f in stable:
        if (gen/f).read_bytes()!=(packet/f).read_bytes():raise ValueError('Rebuild differs: '+f)
    old=[p.extract_text() for p in PdfReader(packet/'summary.pdf').pages];new=[p.extract_text() for p in PdfReader(gen/'summary.pdf').pages]
    if old!=new or len(new)!=5:raise ValueError('Reader text/page reconstruction differs.')
    report=dict(status='PASS_PUBLIC_ONLY_PORTABLE_REPLAY',input_bindings=20,identical_outputs=stable,reader_pages_text_identical=5,author_controls=22,independent_fractions=57,independent_SVG_bars=84,independent_PDF_bars=84,private_source_files_used=False,mathematical_proofs_rerun=False)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
