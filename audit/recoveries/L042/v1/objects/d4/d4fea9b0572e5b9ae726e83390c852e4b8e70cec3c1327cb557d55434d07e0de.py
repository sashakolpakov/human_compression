"""Replay for the complete L042 principal classification.

The finite completeness premise is the accepted L019 wing census.
This checker verifies actual maps; the uniform growth argument is written.
"""
import argparse,copy,hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):
    raise RuntimeError('normal Python required')
from diagrams import need, graph, validate, pure_cut
from verify_diagrams import verify, conjugacy
HERE=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser();p.add_argument('--study',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true')
    p.add_argument('--source-tex',type=Path)
    a=p.parse_args();out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
    exports=json.loads((HERE/'manifest.json').read_text())['exports']
    deps=json.loads((HERE/'dependencies.json').read_text())
    for base,rows in ((HERE,exports),(a.study,deps)):
        for row in rows:
            q=base/row['path'];b=q.read_bytes()
            need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'binding '+str(q))
    env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
    for name,command,childenv in (
        ('argument',[sys.executable,'-O',str(HERE/'check.py')],env),
        ('environment',[sys.executable,str(HERE/'check.py')],dict(env,PYTHONOPTIMIZE='1'))):
        r=subprocess.run(command,capture_output=True,env=childenv,timeout=10)
        (out/f'guard_{name}.stdout').write_bytes(r.stdout);(out/f'guard_{name}.stderr').write_bytes(r.stderr)
        need(r.returncode!=0 and b'normal Python required' in r.stderr,'optimization guard')
    bases=json.loads((a.study/'topic_B_L019_balanced_pairs_v1/arrays_report.json').read_text())['boundary_literal_classes']
    source=json.loads((HERE/'source_figure_records.json').read_text())
    result=verify(bases,source)
    need(json.dumps(result,sort_keys=True)==json.dumps(json.loads((HERE/'diagram_report01.json').read_text()),sort_keys=True),'exact retained maps')
    (out/'diagram_report.json').write_text(json.dumps(result,indent=2)+'\n')
    bad=copy.deepcopy(source);bad['records'][0]['marks'][0][0]=999
    t,_=graph(3,'A',9);identity={'reverse_target':False,'point_map':list(range(9))}
    wrong=copy.deepcopy(identity);wrong['point_map'][0],wrong['point_map'][1]=1,0
    rejected=[]
    for name,action in [('invalid_source_permutation',lambda:verify(bases,bad)),
                        ('wrong_point_map',lambda:conjugacy(t,t,wrong)),
                        ('nonpure_cut',lambda:pure_cut(t,0)),
                        ('below_family_threshold',lambda:graph(4,'B',10))]:
        try:action()
        except (ValueError,IndexError):rejected.append(name)
        else:raise ValueError('damaged input accepted: '+name)
    (out/'malformed_controls.json').write_text(json.dumps(rejected,indent=2)+'\n')
    source_replayed=False
    if a.source_tex:
        raw=a.source_tex.read_bytes();need(hashlib.sha256(raw).hexdigest()==source['primary_tex_sha256'],'primary source hash')
        r=subprocess.run([sys.executable,str(HERE/'read_figure.py'),str(a.source_tex.resolve()),str(out/'source_figure_records.json')],capture_output=True,env=env,timeout=20)
        (out/'source.stdout').write_bytes(r.stdout);(out/'source.stderr').write_bytes(r.stderr)
        need(r.returncode==0 and not r.stderr,'source extraction')
        need(json.loads((out/'source_figure_records.json').read_text())==source,'exact primary extraction')
        source_replayed=True
    if a.render:
        shutil.copy2(HERE/'classification.tex',out/'classification.tex')
        for i in (1,2):
            r=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','classification.tex'],cwd=out,env=env,capture_output=True,timeout=30)
            (out/f'native{i}.stdout').write_bytes(r.stdout);(out/f'native{i}.stderr').write_bytes(r.stderr)
            need(r.returncode==0 and not r.stderr,'native build')
        log=(out/'classification.log').read_text()
        need('Overfull' not in log and 'LaTeX Warning:' not in log,'native content')
    report={'status':'PASS_L042_PRINCIPAL','exports':len(exports),'dependencies':len(deps),
            'source_diagrams':18,'complete_base_matches':18,'subdivision_controls':108,
            'malformed_controls':len(rejected),'optimization_guards':2,'primary_source_replayed':source_replayed,
            'complete_census_premise':'Accepted L019 balanced-pair/wing census; no unchanged census rerun',
            'all_degree_growth':'Written uniform proof, not inference from finite controls',
            'whole_original_credit':0,'new_open_conjecture_credit':0}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':main()
