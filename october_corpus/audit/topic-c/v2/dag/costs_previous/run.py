#!/usr/bin/env python3
"""Fresh author replay; original primary PDFs remain external inputs."""
import argparse, hashlib, json, os, subprocess, sys, time
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
def need(ok,msg):
    if not ok:raise ValueError(msg)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--node',default='node');ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='xelatex');a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'output must be genuinely fresh');a.out.mkdir(parents=True)
    root=a.study_root.resolve();out=a.out.resolve();start=time.monotonic();commands=[]
    manifest=HERE/'manifest.json'
    if manifest.exists():
        for b in json.loads(manifest.read_text())['exports']:
            path=Path(b['path']);need(not path.is_absolute() and '..' not in path.parts,'safe export path')
            need((HERE/path).stat().st_size==b['bytes'] and digest(HERE/path)==b['sha256'],'frozen author export '+str(path))
    def command(name,args):
        t=time.monotonic();r=subprocess.run(args,cwd=HERE,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
        (out/(name+'.log')).write_text(r.stdout);need(r.returncode==0,name+' failed; see log')
        commands.append({'name':name,'argv':list(map(str,args)),'seconds':round(time.monotonic()-t,3),'log_sha256':digest(out/(name+'.log'))})
    py=[sys.executable,'-B','-O']
    command('cost_check',py+[str(HERE/'check.py'),'--study-root',str(root),'--out',str(out/'cost_check.json')])
    command('reader_check',py+[str(HERE/'check_reader.py'),'--study-root',str(root),'--out',str(out/'reader_check.json')])
    command('regenerate_costs',py+[str(HERE/'author.py'),'--study-root',str(root),'--out',str(out/'costs')])
    for n in ['partition.json','weights.json','owner_costs.csv','input_bindings.json']:need((out/'costs'/n).read_bytes()==(HERE/n).read_bytes(),'exact regeneration '+n)
    command('regenerate_reader',py+[str(HERE/'reader_data.py'),'--study-root',str(root),'--packet',str(HERE),'--out',str(out/'reader')])
    for n in ['view_data.json','acquisition.json','explorer.html']:need((out/'reader'/n).read_bytes()==(HERE/n).read_bytes(),'exact regeneration '+n)
    command('javascript',[a.node,str(HERE/'test_explorer.js'),str(HERE/'explorer.html'),str(out/'default.svg')])
    need((out/'default.svg').read_bytes()==(HERE/'default.svg').read_bytes(),'DOM static SVG regenerated exactly')
    if a.render:
        command('render',py+[str(HERE/'build_reader.py'),'--packet',str(HERE),'--out',str(out/'render'),'--xelatex',a.xelatex])
        old=json.loads((HERE/'render_report.json').read_text());fresh=json.loads((out/'render/render_report.json').read_text())
        need(fresh['pages']==old['pages']==2 and fresh['page_text_sha256']==old['page_text_sha256'],'complete reader PDF page text equality')
        command('static_graph',py+[str(HERE/'static_graph.py'),'--packet',str(HERE),'--out',str(out/'static')])
        need((out/'static/static_graph.json').read_bytes()==(HERE/'static_graph.json').read_bytes(),'actual static graph edges and ids')
    report={'status':'PASS_FRESH_AUTHOR_COST_READER_REPLAY','seconds':round(time.monotonic()-start,3),'commands':commands,'frozen_manifest_sha256':digest(manifest) if manifest.exists() else None,'render_requested':a.render,'real_browser_test':False,'independent_ownership_acceptance':False,'runner_sha256':digest(Path(__file__)),'new_source_credit':0,'new_question_credit':0}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'seconds':report['seconds'],'commands':len(commands)}))
if __name__=='__main__':main()
