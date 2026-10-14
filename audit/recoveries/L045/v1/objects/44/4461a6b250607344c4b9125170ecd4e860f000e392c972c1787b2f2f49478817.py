"""Complete bounded replay of the exceptional-family arithmetic certificate."""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
import argparse, hashlib, json, os, shutil, subprocess
from pathlib import Path


def need(b, why):
    if not b:
        raise ValueError(why)


def main():
    a=argparse.ArgumentParser();a.add_argument('--study',type=Path,required=True);a.add_argument('--out',type=Path,required=True);a.add_argument('--render',action='store_true');p=a.parse_args()
    P=Path(__file__).resolve().parent;S=p.study.resolve();O=p.out.resolve()
    need(not O.exists(),'fresh output required')
    dependencies=json.loads((P/'dependencies.json').read_text())
    for row in dependencies:
        f=Path(row['path']);f=f if f.is_absolute() else S/f
        b=f.read_bytes();need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'dependency '+str(f))
    exports=[]
    if (P/'manifest.json').exists():
        exports=json.loads((P/'manifest.json').read_text())['exports']
        for row in exports:
            b=(P/row['path']).read_bytes();need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'frozen export '+row['path'])
    O.mkdir(parents=True);env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
    def run(name,argv,timeout=120,cwd=None):
        cp=subprocess.run(argv,capture_output=True,env=env,timeout=timeout,cwd=cwd)
        (O/(name+'.stdout')).write_bytes(cp.stdout);(O/(name+'.stderr')).write_bytes(cp.stderr)
        need(cp.returncode==0 and not cp.stderr,'clean terminal '+name)
        return cp.stdout
    for n in ['exceptional_lower_bounds.py','exceptional_coset_inequalities.py','exceptional_controls.py','exceptional_lattice.py']:
        shutil.copy2(P/n,O/n)
    for n in ['exceptional_lower_bounds.py','exceptional_coset_inequalities.py']:
        run(n,[sys.executable,str(O/n)],30)
        if (P/n.replace('.py','.json')).exists():
            need(json.loads((O/n.replace('.py','.json')).read_text())==json.loads((P/n.replace('.py','.json')).read_text()),'exact polynomial report')
    run('lattice',[sys.executable,str(O/'exceptional_lattice.py'),'--out',str(O/'lattice')],260)
    run('independent',[sys.executable,str(O/'exceptional_controls.py'),'--input',str(O),'--out',str(O/'independent.json')])
    damaged=0
    cases=['lower_difference','lower_order','missing_lower_case','final_margin','root_coordinates','missing_root']
    for name in cases:
        D=O/('damaged_'+name);D.mkdir();(D/'lattice').mkdir()
        for f in ['exceptional_lower_bounds.json','exceptional_coset_inequalities.json']:
            shutil.copy2(O/f,D/f)
        shutil.copy2(O/'lattice/report.json',D/'lattice/report.json')
        f=D/('exceptional_lower_bounds.json' if name.startswith('lower') or name=='missing_lower_case' else 'exceptional_coset_inequalities.json' if name=='final_margin' else 'lattice/report.json')
        d=json.loads(f.read_text())
        if name=='lower_difference':d['rows'][0]['difference'][0]+=1
        elif name=='lower_order':d['rows'][0]['group_order'][0]+=1
        elif name=='missing_lower_case':d['rows'].pop()
        elif name=='final_margin':d['fixed'][0]['margin']='0'
        elif name=='root_coordinates':d['cases'][0]['root_lattice_coordinates'][0][0][0]+=1
        else:d['cases'][0]['roots'].pop();d['cases'][0]['root_lattice_coordinates'].pop()
        f.write_text(json.dumps(d)+'\n');dest=D/'forbidden.json'
        cp=subprocess.run([sys.executable,str(O/'exceptional_controls.py'),'--input',str(D),'--out',str(dest)],env=env,capture_output=True,timeout=120)
        (D/'stderr').write_bytes(cp.stderr);need(cp.returncode!=0 and not dest.exists(),'damaged report rejected '+name);damaged+=1
    guards=0
    for n in ['check.py','exceptional_lower_bounds.py','exceptional_coset_inequalities.py','exceptional_controls.py','exceptional_lattice.py']:
        for kind in ['argument','environment']:
            e=env.copy();cmd=[sys.executable]
            if kind=='argument':cmd+=['-O']
            else:e['PYTHONOPTIMIZE']='1'
            cp=subprocess.run(cmd+[str(P/n)],env=e,capture_output=True,timeout=10)
            (O/(n+'_'+kind+'.stderr')).write_bytes(cp.stderr)
            need(cp.returncode!=0 and b'unoptimized execution required' in cp.stderr,'optimization rejected');guards+=1
    pages=None
    if p.render:
        N=O/'native';N.mkdir();shutil.copy2(P/'exceptional.tex',N/'exceptional.tex')
        for i in range(2):run('native'+str(i),['/opt/homebrew/bin/pdflatex','-halt-on-error','-interaction=nonstopmode','exceptional.tex'],45,N)
        log=(N/'exceptional.log').read_text();need(not any(x in log for x in ['Overfull','Underfull','LaTeX Warning']),'clean native typesetting')
        from pypdf import PdfReader
        r=PdfReader(N/'exceptional.pdf');pages=len(r.pages);text='\n'.join(x.extract_text() or '' for x in r.pages);(N/'text.txt').write_text(text)
        if (P/'native_expected.txt').exists():need(text==(P/'native_expected.txt').read_text(),'exact native text')
        run('render',['/opt/homebrew/bin/gs','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png','exceptional.pdf'],45,N)
    report=dict(status='PASS_EXCEPTIONAL_ARITHMETIC_AND_LATTICES',exports=len(exports),dependencies=len(dependencies),lower_cases=18,final_families=9,fixed_cases=3,auxiliary_inequalities=15,root_equations=372,damaged_reports=damaged,optimization_guards=guards,native_pages=pages,whole_original_credit=0,new_open_question_credit=0)
    (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))


if __name__=='__main__':main()
