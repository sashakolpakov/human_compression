#!/usr/bin/env python3
"""Check immutable assembly, acquired exports, scope and native build.

This is an integrity and publication check, not a formal proof verifier.
Accepted finite searches are acquired, not repeated here.
"""
import argparse, copy, hashlib, json, os, shutil, subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
def need(ok, message):
    if not ok: raise ValueError(message)
def load(name): return json.loads((HERE/name).read_text())
def bind(base, row):
    data = (base/row['path']).read_bytes()
    need(len(data) == row['bytes'] and hashlib.sha256(data).hexdigest() == row['sha256'], 'binding '+row['path'])
def scope(s):
    need(s['original'] == 'F001' and s['source_edition'] == 'arXiv:1912.05512v1, 11 December 2019', 'source')
    need(s['principal'] == 'rk(PSp4(q)) is empty for q=3 and {3,4,5} otherwise, for every prime power q', 'principal')
    need(s['principal_author_proof_complete'] is True and s['all_components_distinctly_accepted'] is True, 'complete components')
    need(s['whole_original_accepted'] is False, 'whole review boundary')
    need(s['all_source_auxiliary_assertions_recovered'] is False, 'auxiliary scope')
    need(s['auxiliary_Lemma4_1'] == 'refuted separately in O5(7) and SO5(7); not used', 'auxiliary correction')
    need(s['odd_upper_bound_involution_scope'] == 'both nontrivial types', 'mixed types')
    need(s['q3_exclusion_scope'] == 'all ranks by complete prefix exhaustion and simplicity', 'q3 completeness')
    need(s['higher_dimensional_question'] == 'outside principal contract; no new resolution claim', 'question scope')
    need(s['q2_simplicity_used'] is False and s['external_classification_reproved'] is False, 'retained boundaries')
    need(s['new_original_credit'] == s['new_question_credit'] == s['new_Lean_credit'] == 0 and s['new_factor'] is None, 'credit')
def main():
    need(sys.flags.optimize == 0, 'optimized Python is unsupported')
    ap=argparse.ArgumentParser(); ap.add_argument('--study-root',type=Path,required=True); ap.add_argument('--out',type=Path,required=True); ap.add_argument('--render',action='store_true'); a=ap.parse_args()
    a.out=a.out.resolve(); a.out.mkdir(parents=True,exist_ok=False)
    manifest=load('manifest.json'); dep=load('dependencies.json')
    for row in manifest['exports']: bind(HERE,row)
    for row in dep['bindings']: bind(a.study_root,row)
    inherited=[]
    for relative in dep['required_acquired_manifests']:
        path=a.study_root/relative; m=json.loads(path.read_text())
        need('exports' in m, 'acquired export manifest '+relative)
        for row in m['exports']: bind(path.parent,row); inherited.append(str(Path(relative).parent/row['path']))
    s=load('scope.json'); scope(s); controls=[]
    for key,value in [('principal_author_proof_complete',False),('all_components_distinctly_accepted',False),('whole_original_accepted',True),('all_source_auxiliary_assertions_recovered',True),('auxiliary_Lemma4_1','recovered'),('odd_upper_bound_involution_scope','negative reflections only'),('q3_exclusion_scope','no rank three found'),('higher_dimensional_question','solved'),('q2_simplicity_used',True),('external_classification_reproved',True),('new_original_credit',1),('new_question_credit',1),('new_Lean_credit',1),('new_factor',2)]:
        trial=copy.deepcopy(s); trial[key]=value
        try: scope(trial)
        except ValueError: controls.append(key)
        else: raise ValueError('scope mutation accepted '+key)
    routes=load('claim_routes.json'); ids=[row['id'] for row in routes['rows']]
    need(ids==['P1','P1.E5','P1.E34','P1.EU','P1.B235','P1.B2U','P1.O345','P1.OU','P1.Q3','P1.LOW','A1','R1','Q1','E1'],'source routes')
    need(routes['whole_original_credit']==routes['new_question_credit']==routes['new_Lean_credit']==0 and routes['new_factor'] is None,'route credit')
    pages=None
    if a.render:
        from pypdf import PdfReader
        native=a.out/'native'; native.mkdir(); shutil.copyfile(HERE/'principal.tex',native/'principal.tex'); env=os.environ.copy(); env.pop('PYTHONOPTIMIZE',None)
        for i in [1,2]:
            p=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','principal.tex'],cwd=native,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60)
            (native/f'pass{i}.log').write_text(p.stdout); need(p.returncode==0,'native build')
        log=(native/'principal.log').read_text()
        for bad in ['Overfull','LaTeX Warning:','undefined references']: need(bad not in log,'native '+bad)
        texts=[p.extract_text() or '' for p in PdfReader(native/'principal.pdf').pages]; ref=load('native.json')
        need(len(texts)==ref['pages'] and [hashlib.sha256(t.encode()).hexdigest() for t in texts]==ref['page_text_sha256'],'native page text'); pages=len(texts)
    report={'status':'PASS','exports':len(manifest['exports']),'direct_bindings':len(dep['bindings']),'acquired_manifests':len(dep['required_acquired_manifests']),'acquired_export_records':len(inherited),'acquired_unique_files':len(set(inherited)),'claim_routes':len(ids),'scope_controls':controls,'native_pages':pages,'finite_searches_repeated':False,'formal_verification':False,'whole_original_accepted':False}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report))
if __name__=='__main__': main()
