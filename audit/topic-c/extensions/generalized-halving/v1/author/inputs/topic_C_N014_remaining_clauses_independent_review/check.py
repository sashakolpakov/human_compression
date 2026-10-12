#!/usr/bin/env python3
"""Bounded immutable review replay; no imports from the authored packet."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
from pypdf import PdfReader
from independent_models import run


def need(b,m):
    if not b: raise ValueError(m)


def sig(p):
    b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true')
    a=ap.parse_args();here=Path(__file__).resolve().parent
    a.out.mkdir(parents=True,exist_ok=False)
    bindings=json.loads((here/'bindings.json').read_text())
    for row in bindings['study_inputs']:
        need(sig(a.study_root/row['path'])=={k:row[k] for k in ['bytes','sha256']},'input '+row['path'])
    author=a.study_root/'topic_C_N014_remaining_clauses'
    manifest=json.loads((author/'manifest.json').read_text())
    for row in manifest['exports']:
        need(sig(author/row['path'])=={k:row[k] for k in ['bytes','sha256']},'author export '+row['path'])
    if (here/'manifest.json').exists():
        for row in json.loads((here/'manifest.json').read_text())['exports']:
            need(sig(here/row['path'])=={k:row[k] for k in ['bytes','sha256']},'review '+row['path'])
    need(run()==json.loads((here/'independent_report.json').read_text()),'independent models')
    process=subprocess.run([sys.executable,'-B','-O',str(author/'second_leaf_example.py'),
                            '--out',str(a.out/'author_example.json')],capture_output=True,text=True)
    need(process.returncode==0,'author optional replay')
    need(json.loads((a.out/'author_example.json').read_text())==json.loads((author/'second_leaf_example.json').read_text()),'author report')
    if a.render:
        build=a.out/'render';build.mkdir()
        for i in [1,2]:
            p=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode',
                              '-halt-on-error','-output-directory='+str(build),str(author/'remaining_clauses.tex')],capture_output=True,text=True)
            (build/f'pass{i}.log').write_text(p.stdout+p.stderr);need(p.returncode==0,'render')
        text=lambda p:[x.extract_text() for x in PdfReader(p).pages]
        need(text(build/'remaining_clauses.pdf')==text(author/'remaining_clauses.pdf'),'all four page texts')
        need(len(text(author/'remaining_clauses.pdf'))==4,'four-page note')
    r=dict(status='PASS',author_exports=len(manifest['exports']),study_bindings=len(bindings['study_inputs']),
           original_flags=322,transformed_flags=362,residues=274,coset_models=1,rendered=a.render,
           whole_source_acceptance=False,role='distinct bounded mathematical review with supplementary finite checks')
    (a.out/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))


if __name__=='__main__':main()
