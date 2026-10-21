#!/usr/bin/env python3
"""Replay the complete finite census; written proof requires distinct review."""
import argparse,hashlib,json,subprocess,shutil,re
from pathlib import Path
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise ValueError(msg)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((ROOT/n).read_text())
def bound(base,row):
    p=base/row['path'];need(p.stat().st_size==row['bytes'] and digest(p)==row['sha256'],'binding '+str(p))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);ap.add_argument('--study-root',type=Path);ap.add_argument('--render',action='store_true');ap.add_argument('--gap',default='/opt/homebrew/bin/gap');ap.add_argument('--pdflatex',default='/opt/homebrew/bin/pdflatex');a=ap.parse_args()
    out=a.out.resolve();need(not out.exists(),'fresh output required');out.mkdir(parents=True)
    manifest=read('manifest.json')
    for row in manifest['exports']:bound(ROOT,row)
    deps=read('dependencies.json');pins=0
    if a.study_root:
        for key in ['source','source_text','independent_prior_proof']:bound(a.study_root,deps[key]);pins+=1
    scope=read('scope.json');need(scope['new_original_credit']==scope['new_question_credit']==scope['new_Lean_declarations']==0,'scope');need(scope['required_mathematical_programs']==['polynomial_table.g'],'whole required code')
    shutil.copyfile(ROOT/'polynomial_table.g',out/'polynomial_table.g')
    p=subprocess.run([a.gap,'-q','-b','polynomial_table.g'],cwd=out,text=True,capture_output=True,timeout=120)
    (out/'gap.stdout').write_text(p.stdout);(out/'gap.stderr').write_text(p.stderr)
    need(p.returncode==0 and not re.search(r'Error|Syntax warning',p.stdout+p.stderr),'GAP census execution')
    rows=json.loads((out/'polynomial_table_rows.json').read_text());need(rows==read('polynomial_table_rows.json'),'exact complete12-row census');need(len(rows)==12,'all source rows')
    pages=0
    if a.render:
        doc=read('native.json');build=out/'native';build.mkdir();shutil.copyfile(ROOT/doc['tex'],build/doc['tex'])
        for i in range(2):
            c=subprocess.run([a.pdflatex,'-interaction=nonstopmode','-halt-on-error',doc['tex']],cwd=build,capture_output=True,text=True,timeout=60);(build/f'pass{i}.stdout').write_text(c.stdout);need(c.returncode==0,'native compilation')
        log=(build/Path(doc['tex']).with_suffix('.log')).read_text();need(not re.search('Overfull|Underfull|LaTeX Warning',log),'native diagnostics')
        hashes=[hashlib.sha256((p.extract_text() or '').encode()).hexdigest() for p in PdfReader(build/doc['pdf']).pages];need(hashes==doc['page_text_sha256'],'native page texts');pages=len(hashes)
    report={'status':'PASS_BOUNDED_CENSUS_AND_BINDINGS','manifest_sha256':digest(ROOT/'manifest.json'),'exports':len(manifest['exports']),'source_and_prior_pins':pins,'complete_rows':len(rows),'nonscalar_matrices_checked':sum(r['nonscalar_total'] for r in rows),'native_pages':pages,'written_proof_checked_by_program':False,'whole_L023_recovered':False}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
