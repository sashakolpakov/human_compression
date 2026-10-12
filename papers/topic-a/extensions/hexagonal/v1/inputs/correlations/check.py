#!/usr/bin/env python3
"""Bindings, limited scope controls, optional word diagnostics and clean render."""
from pathlib import Path
import argparse, copy, hashlib, json, shutil, subprocess, time
from word_checks import run

HERE = Path(__file__).resolve().parent
def need(v, m):
    if not v:
        raise ValueError(m)
def load(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def validate(s):
    need(s['diagrams'] == [4,5], 'two exact source diagrams')
    need(s['group_maps_all_positive_integer_s'] is True, 'uniform group scope')
    need(s['diagram4_geometry'] == 'from each existing regular universal fork hypertope with actual prescribed residues', 'forward geometry hypothesis')
    need(s['diagram5_flag_transitivity'] == 'experimental, not proved here', 'experimental geometry boundary')
    need(s['rank_four_generating_list'] == ['t','a','b','d'], 'four generators')
    need(s['new_original_credit'] == s['new_question_credit'] == s['new_Lean_credit'] == 0, 'zero credits')

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    p.add_argument('--render',action='store_true');p.add_argument('--study-root',type=Path)
    a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False);started=time.monotonic()
    if (HERE/'manifest.json').exists():
        for r in load(HERE/'manifest.json')['exports']:
            q=HERE/r['path'];need(q.stat().st_size==r['bytes'] and sha(q)==r['sha256'],r['path'])
    if a.study_root:
        for r in load(HERE/'bindings.json')['external_bindings']:
            q=a.study_root/r['path'];need(q.stat().st_size==r['bytes'] and sha(q)==r['sha256'],r['path'])
    scope=load(HERE/'scope.json');validate(scope);controls=[]
    for field,value in [('diagram4_geometry','every presentation is a hypertope'),('diagram5_flag_transitivity','proved'),('rank_four_generating_list',['t','a','b']),('new_original_credit',1)]:
        bad=copy.deepcopy(scope);bad[field]=value
        try:validate(bad)
        except ValueError:controls.append(field)
        else:raise ValueError('scope mutation accepted '+field)
    diagnostic=run();pages=[]
    if a.render:
        from pypdf import PdfReader
        d=a.out/'render';d.mkdir();shutil.copyfile(HERE/'correlation_reduction.tex',d/'correlation_reduction.tex')
        for i in (1,2):
            with (d/f'pass{i}.stdout').open('w') as f:
                r=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','correlation_reduction.tex'],cwd=d,stdout=f,stderr=subprocess.STDOUT,timeout=30)
            need(r.returncode==0,'clean TeX execution')
        log=(d/'correlation_reduction.log').read_text()
        need(not any(x in log for x in ['Overfull','Underfull','LaTeX Warning','Missing character']),'clean final render')
        texts=lambda p:[x.extract_text() for x in PdfReader(p).pages]
        need(texts(d/'correlation_reduction.pdf')==texts(HERE/'correlation_reduction.pdf'),'exact rendered page text')
        pages=[len(texts(d/'correlation_reduction.pdf'))]
    report={'status':'PASS_AUTHOR_CORRELATION_REDUCTION','scope_controls':controls,'diagnostics':diagnostic,'rendered_pages':pages,'previous_finite_or_Lean_repeated':False,'new_original_credit':0,'seconds':round(time.monotonic()-started,6)}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
