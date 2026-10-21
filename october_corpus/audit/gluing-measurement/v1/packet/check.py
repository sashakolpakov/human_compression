#!/usr/bin/env python3
"""Replay frozen Gluing arithmetic/reader; this is an author check, not acceptance."""
from pathlib import Path
import argparse,json,subprocess,sys
import calculate as C
import build,presentation
H=Path(__file__).resolve().parent
def main():
    p=argparse.ArgumentParser();p.add_argument('--inputs',type=Path,required=True);p.add_argument('--input-review',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='xelatex');a=p.parse_args()
    C.need(not a.out.exists(),'fresh output directory');a.out.mkdir(parents=True)
    m=H/'manifest.json'
    if m.exists():
        for r in C.read(m)['exports']:
            f=H/r['path'];C.need(f.stat().st_size==r['bytes'] and C.sha(f)==r['sha256'],'frozen numerical export '+r['path'])
    result=C.calculate(a.inputs,a.input_review);C.need(result==C.read(H/'results.json'),'all thirty coordinates and120 exact fractions')
    C.need(build.controls(result,a.inputs,a.input_review)==C.read(H/'controls.json'),'all20 rejection controls')
    C.need(presentation.reader(result)==(H/'reader.tex').read_text(),'literal complete reader formulas and scope')
    C.need(presentation.graph(result)==C.read(H/'document_graph.json'),'exact complete-document graph')
    C.need(build.acquisition(result)==C.read(H/'acquisition.json'),'whole acquisition union')
    build.csvs(result,a.out)
    for n in ('costs.csv','fractions.csv'):C.need((a.out/n).read_bytes()==(H/n).read_bytes(),'exact CSV '+n)
    cmd=[sys.executable,'-B','-O',str(H/'build.py'),'--inputs',str(a.inputs.resolve()),'--input-review',str(a.input_review.resolve()),'--out',str((a.out/'rebuild').resolve())]
    if a.render:cmd+=['--render','--xelatex',a.xelatex]
    run=subprocess.run(cmd,capture_output=True,text=True);(a.out/'build.log').write_text(run.stdout+run.stderr);C.need(run.returncode==0,'fresh author build')
    for n in ('costs.svg','document_graph.svg'):
        C.need((a.out/'rebuild'/n).read_bytes()==(H/n).read_bytes(),'exact vector figure '+n)
    report=C.read(a.out/'rebuild/report.json');expected=C.read(H/'author_replay.json')
    if not a.render:expected['reader_pages']=None;expected.pop('reader_page_text_sha256',None)
    C.need(report==expected,'exact fresh report and page text')
    (a.out/'report.json').write_text(json.dumps(dict(status='PASS_AUTHOR_CHECK_PENDING_DISTINCT_REVIEW',coordinates=30,fractions=120,controls=20,actual_bars=9,document_graph_edges=8,reader_rendered=a.render),indent=2)+'\n')
    print('PASS30 coordinates/120 fractions/20 controls; full figures and acquisition')
if __name__=='__main__':main()
