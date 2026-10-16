"""Verify retained inputs and native assembly; the general proof needs human review."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,hashlib,json,subprocess
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
    need(scope['source_claims']==['L114 Lemma 4.2', 'L114 Lemma 4.3', 'L114 Lemma 4.4', 'L114 Lemma 4.5', 'L114 Lemma 4.6', 'L114 Lemma 5.1'],'Exact claim scope')
    need(scope['whole_original_credit']==scope['new_conjecture_credit']==scope['new_Lean_credit']==0,'No extra credit')
    out=a.out.resolve();need(not out.exists(),'Fresh output');out.mkdir(parents=True)
    commands=[]
    for k in (1,2):
        command=['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory',str(out),str(HERE/'restrictions.tex')]
        r=subprocess.run(command,cwd=HERE,capture_output=True)
        (out/f'latex{k}.stdout').write_bytes(r.stdout);(out/f'latex{k}.stderr').write_bytes(r.stderr);r.check_returncode();commands.append(command)
    need('Overfull' not in (out/'restrictions.log').read_text(),'Clean native layout')
    old=PdfReader(HERE/'restrictions.pdf');new=PdfReader(out/'restrictions.pdf')
    need(len(old.pages)==len(new.pages)==5,'Exact proof page count')
    need([p.extract_text() for p in old.pages]==[p.extract_text() for p in new.pages],'Identical proof text')
    command=['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile='+str(out/'page-%02d.png'),str(out/'restrictions.pdf')]
    subprocess.run(command,check=True,capture_output=True);commands.append(command)
    for j in range(1,6):need(sha(out/f'page-{j:02d}.png')==sha(HERE/f'page-{j:02d}.png'),'Identical native page')
    for row in deps:bind(Path(row['path']),row)
    report=dict(status='PASS_L114_NORMALIZER_RESTRICTIONS_INPUTS_AND_NATIVE_ASSEMBLY',dependencies=len(deps),exports=len(m['exports']),native_pages=5,finite_targets=0,proof_status='General proof requires distinct mathematical review; this checker verifies its exact inputs and native assembly.',whole_original_credit=0,new_conjecture_credit=0,new_Lean_credit=0,commands=commands)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,sort_keys=True))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);p.add_argument('--expected-manifest',required=True);main(p.parse_args())
