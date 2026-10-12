"""Portable bounded source/proof/certificate replay; no map census."""
from pathlib import Path
import argparse, copy, hashlib, json, shutil, subprocess, sys
from pypdf import PdfReader
R=Path(__file__).resolve().parent
def need(x,m):
    if not x: raise ValueError(m)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n): return json.loads((R/n).read_text())
def run(cmd,cwd=None):
    z=subprocess.run(cmd,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    need(z.returncode==0,z.stdout[-4000:]);return z.stdout
def validate(scope,result):
    need(scope['whole_original_acceptance'] is False,'whole original boundary')
    need(scope['classIII_flag_completion_universal'] is False,'flag completion boundary')
    need(scope['classIII_pregeometry_symmetry_proved'] is True,'symmetry boundary')
    need(scope['elementary_companion_refutes_classIII'] is False,'companion scope')
    need(scope['required_programs']==['certificate.py'],'whole finite certificate required')
    need(result['seed']['order']==504 and result['seed']['swapped_value']!=[1,0,0,1],'seed and relation')
    need(result['torus']['order']==32 and result['torus']['edge_completions']==0,'full torus group')
    need(result['parallel_product']['order_by_written_theorem']==16128,'product order')
    need(len(result['negative_controls'])==4 and all(x['rejected'] for x in result['negative_controls']),'mathematical controls')
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    p.add_argument('--study-root',type=Path);p.add_argument('--render',action='store_true');a=p.parse_args()
    need(not a.out.exists(),'fresh output required');a.out.mkdir(parents=True)
    m=read('manifest.json')
    for x in m['exports']:
        f=R/x['path'];need(f.stat().st_size==x['bytes'] and sha(f)==x['sha256'],'export '+x['path'])
    external=read('dependencies.json')['bindings']
    if a.study_root:
        for x in external:
            f=a.study_root/x['path'];need(f.stat().st_size==x['bytes'] and sha(f)==x['sha256'],'external '+x['path'])
    log=run([sys.executable,'-B','-O',str(R/'certificate.py'),'--out',str(a.out/'certificate_result.json')])
    (a.out/'certificate.log').write_text(log)
    result=json.loads((a.out/'certificate_result.json').read_text());need(result==read('certificate_result.json'),'fresh exact bounded certificate')
    scope=read('scope.json');validate(scope,result)
    mutations=[('whole-original claim','whole_original_acceptance',True),
               ('universal flag completion','classIII_flag_completion_universal',True),
               ('misread no-duality refutation','classIII_pregeometry_symmetry_proved',False),
               ('Class IV scope drift','elementary_companion_refutes_classIII',True),
               ('omit required finite code','required_programs',[])]
    controls=[]
    for name,k,v in mutations:
        bad=copy.deepcopy(scope);bad[k]=v
        try:validate(bad,result)
        except ValueError:controls.append({'control':name,'rejected':True})
        else:raise ValueError('negative control passed '+name)
    bad=copy.deepcopy(result);bad['torus']['order']=8
    try:validate(scope,bad)
    except ValueError:controls.append({'control':'vertex action mistaken for flag group','rejected':True})
    else:raise ValueError('vertex-image mutation passed')
    pages=0
    if a.render:
        b=a.out/'native';b.mkdir();shutil.copyfile(R/'rank_four_completion.tex',b/'rank_four_completion.tex')
        for i in range(2):(b/f'run{i}.log').write_text(run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','rank_four_completion.tex'],b))
        log=(b/'rank_four_completion.log').read_text();need(not any(s in log for s in ['Overfull','Underfull','LaTeX Warning']),'native diagnostics')
        texts=[hashlib.sha256((x.extract_text() or '').encode()).hexdigest() for x in PdfReader(b/'rank_four_completion.pdf').pages]
        need(texts==read('native.json')['page_text_sha256'],'native exact page texts');pages=len(texts)
    report={'status':'PASS_BOUNDED_AUTHOR_REPLAY','exports':len(m['exports']),
            'external_bindings':len(external) if a.study_root else 0,
            'required_certificate':'exact fixed SL2(8) instance, not a map census',
            'mathematical_controls':4,'scope_controls':controls,'native_pages':pages,
            'source_routes':len(read('source_map.json')['rows']),'whole_L023_acceptance':False}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
