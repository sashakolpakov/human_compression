"""Verify retained inputs and native assembly; the general proof needs human review."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,hashlib,json,subprocess,importlib.util
from pypdf import PdfReader
HERE=Path(__file__).resolve().parent

def need(ok,message):
    if not ok: raise ValueError(message)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p):return dict(path=str(p),bytes=p.stat().st_size,sha256=sha(p))
def bind(p,row):
    need(p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'Exact retained file: '+str(p))
def main(a):
    need(sha(HERE/'manifest.json')==a.expected_manifest,'Exact reviewed component')
    m=load(HERE/'manifest.json')
    for row in m['exports']:
        p=Path(row['path']);need(not p.is_absolute() and '..' not in p.parts,'Relative export')
        bind(HERE/p,row)
    deps=load(HERE/'dependencies.json')
    for row in deps:bind(Path(row['path']),row)
    scope=load(HERE/'scope.json')
    need(scope['source_claims']==['L114 Theorem 6.1 eight retained Sz8 markings only'],'Exact claim scope')
    need(scope['whole_original_credit']==scope['new_conjecture_credit']==scope['new_Lean_credit']==0,'No extra credit')
    out=a.out.resolve();need(not out.exists(),'Fresh output');out.mkdir(parents=True)
    commands=[]
    for k in (1,2):
        command=['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory',str(out),str(HERE/'panels.tex')]
        r=subprocess.run(command,cwd=HERE,capture_output=True)
        (out/f'latex{k}.stdout').write_bytes(r.stdout);(out/f'latex{k}.stderr').write_bytes(r.stderr);r.check_returncode();commands.append(command)
    need('Overfull' not in (out/'panels.log').read_text(),'Clean native layout')
    old=PdfReader(HERE/'panels.pdf');new=PdfReader(out/'panels.pdf')
    need(len(old.pages)==len(new.pages)==m['native_pages'],'Exact proof page count')
    need([p.extract_text() for p in old.pages]==[p.extract_text() for p in new.pages],'Identical proof text')
    command=['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile='+str(out/'page-%02d.png'),str(out/'panels.pdf')]
    subprocess.run(command,check=True,capture_output=True);commands.append(command)
    for j in range(1,m['native_pages']+1):need(sha(out/f'page-{j:02d}.png')==sha(HERE/f'page-{j:02d}.png'),'Identical native page')
    raw=HERE.parent/'remaining_markings_actual01/stdout'
    receipt=load(HERE.parent/'remaining_markings_actual01/receipt.json')
    need(receipt['reason']=='completed' and receipt['returncode']==0 and receipt['child_reaped'],'Clean actual acquisition')
    need(not receipt['final_binding_failures'] and not receipt['final_boundary_failures'] and receipt['final_request_unchanged'],'Final acquisition guards')
    for row in receipt['outputs']:bind(raw.parent/row['path'],row)
    spec=importlib.util.spec_from_file_location('independent_panel_reader',HERE/'literal.py')
    reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
    data=load(raw);finite=reader.verify(data);finite['rejected_damages']=reader.controls(data)
    need(all(r['actual_panel_sizes']==[2,2,2] and r['standard_chambers']==[2,2,2] for r in finite['markings']),'Actual observed result')
    (out/'finite_report.json').write_text(json.dumps(finite,indent=2)+'\n')
    guards=[]
    for flag in ['-O','-OO']:
        r=subprocess.run([sys.executable,flag,str(HERE/'literal.py'),str(raw)],capture_output=True)
        need(r.returncode!=0 and b'Ordinary Python required' in r.stderr,'Optimization guard')
        guards.append(dict(flag=flag,returncode=r.returncode))
    (out/'optimization_guards.json').write_text(json.dumps(guards,indent=2)+'\n')
    for row in deps:bind(Path(row['path']),row)
    report=dict(status='PASS_L114_EIGHT_RETAINED_MARKING_PANELS',dependencies=len(deps),exports=len(m['exports']),native_pages=m['native_pages'],finite_targets=1,proof_status='General proof requires distinct mathematical review; this checker verifies its exact inputs and native assembly.',whole_original_credit=0,new_conjecture_credit=0,new_Lean_credit=0,commands=commands,finite_report=finite,optimization_guards=guards)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,sort_keys=True))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);p.add_argument('--expected-manifest',required=True);main(p.parse_args())
