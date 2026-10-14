"""Integrity, finite controls and native edition checks; general proof needs review."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Normal Python is required')
sys.dont_write_bytecode = True
from pathlib import Path
import argparse, hashlib, json, os, shutil, subprocess, time


def need(ok, why):
    if not ok: raise ValueError(why)


def digest(p):
    b=p.read_bytes()
    return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args()
    root=Path(__file__).resolve().parent
    out=args.out.resolve()
    need(not out.exists() and not out.is_relative_to(root),'fresh external output')
    manifest=json.loads((root/'manifest.json').read_text())
    dependencies=json.loads((root/'dependencies.json').read_text())
    for row in manifest['exports']:
        need(digest(root/row['path'])=={k:row[k] for k in ['bytes','sha256']},'changed export')
    for row in dependencies:
        need(digest(Path(row['path']))=={k:row[k] for k in ['bytes','sha256']},'changed dependency')
    out.mkdir(parents=True)
    start=time.monotonic()
    result=subprocess.run([sys.executable,'-B',str(root/'check_decorations.py')],capture_output=True,timeout=180)
    (out/'finite.stdout').write_bytes(result.stdout)
    (out/'finite.stderr').write_bytes(result.stderr)
    need(result.returncode==0 and not result.stderr,'finite controls completed')
    finite=json.loads(result.stdout.splitlines()[-1])
    need(finite==json.loads((root/'finite_expected.json').read_text()),'exact finite result')
    guards=[]
    for file in ['check.py','check_decorations.py']:
        for mode in ['argument','environment']:
            env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
            if mode=='environment':env['PYTHONOPTIMIZE']='1'
            result=subprocess.run([sys.executable]+(['-O'] if mode=='argument' else [])+[str(root/file)],env=env,capture_output=True,timeout=10)
            need(result.returncode!=0 and (b'Normal Python' in result.stderr or b'ordinary Python' in result.stderr),'optimization guard')
            (out/(file+'.'+mode+'.stderr')).write_bytes(result.stderr)
            guards.append([file,mode])
    from pypdf import PdfReader
    native=out/'native';native.mkdir()
    for file in ['decorated_points.tex','tetrahedra_section.tex']:
        shutil.copyfile(root/file,native/file)
    for i in range(2):
        result=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','decorated_points.tex'],cwd=native,capture_output=True,timeout=60)
        (native/f'build{i}.stdout').write_bytes(result.stdout)
        (native/f'build{i}.stderr').write_bytes(result.stderr)
        need(result.returncode==0 and not result.stderr,'native build')
    log=(native/'decorated_points.log').read_text()
    need(not any(s in log for s in ['Warning','Overfull','Underfull']),'clean native output')
    old=[p.extract_text() for p in PdfReader(root/'decorated_points.pdf').pages]
    new=[p.extract_text() for p in PdfReader(native/'decorated_points.pdf').pages]
    need(old==new and len(new)==8,'all native page text')
    result=subprocess.run(['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile=page-%02d.png','decorated_points.pdf'],cwd=native,capture_output=True,timeout=60)
    (native/'render.stdout').write_bytes(result.stdout)
    (native/'render.stderr').write_bytes(result.stderr)
    need(result.returncode==0 and not result.stderr,'native render')
    report=dict(status='PASS_L041_EDITION_AND_FINITE_CONTROLS',exports=len(manifest['exports']),
                dependencies=len(dependencies),finite_fields=[r['q'] for r in finite['cases']],
                optimization_guards=guards,native_pages=8,seconds=time.monotonic()-start,
                general_proof_is_computational=False,whole_original_credit=0,
                new_question_credit=0,new_Lean=0,measurement=None)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__=='__main__':main()
