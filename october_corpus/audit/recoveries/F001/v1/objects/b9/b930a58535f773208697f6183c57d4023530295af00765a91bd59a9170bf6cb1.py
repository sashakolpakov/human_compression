#!/usr/bin/env python3
"""Bindings, exact arithmetic, and scope controls; not a proof assistant."""
import argparse,copy,hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import mixed_arithmetic

def need(ok,msg):
    if not ok:raise ValueError(msg)
def load(name):return json.loads((HERE/name).read_text())
def binding(root,row):
    b=(root/row['path']).read_bytes()
    need(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'binding '+row['path'])
def scope(s):
    need(s['original']=='F001','original')
    need(s['source_edition']=='arXiv:1912.05512v1, 11 December 2019','edition')
    need(s['fields']=='all odd prime powers q>=5','fields')
    need(s['group']=='Omega(5,q)','group')
    need(s['involution_scope']=='both nontrivial involution types','types')
    need(s['rank_bound']==5,'bound')
    for k in ['mixed_involutions_covered','whole_odd_upper_bound_claimed']:
        need(s[k] is True,k)
    for k in ['whole_original_accepted','independent_review_complete','uniform_proof_formalized','new_original_credit','new_conjecture_credit','new_Lean','new_measurement']:
        need(s[k] is False,k)
    need(s['remaining']=='Distinct review of this mixed bound; full F001 principal assembly and admission','remaining')

def main():
    need(sys.flags.optimize==0,'optimized Python unsupported')
    p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);p.add_argument('--study-root',type=Path);p.add_argument('--render',action='store_true');a=p.parse_args()
    a.out=a.out.resolve();a.out.mkdir(parents=True,exist_ok=False)
    man=load('manifest.json')
    for row in man['exports']:binding(HERE,row)
    count=0
    if a.study_root:
        for row in load('dependencies.json')['bindings']:binding(a.study_root,row);count+=1
    sc=load('scope.json');scope(sc);controls=[]
    for k in ['mixed_involutions_covered','whole_odd_upper_bound_claimed','whole_original_accepted','independent_review_complete','uniform_proof_formalized','new_original_credit','new_conjecture_credit','new_Lean','new_measurement']:
        bad=copy.deepcopy(sc);bad[k]=not bad[k]
        try:scope(bad)
        except ValueError:controls.append(k)
        else:raise ValueError('damaged scope passed '+k)
    actual=mixed_arithmetic.run();expected=load('expected.json');need(actual==expected,'exact arithmetic differs')
    damaged=[]
    bad=copy.deepcopy(expected);bad['symbolic_identities']=bad['symbolic_identities'][:-1];damaged.append(('lost_identity',bad))
    bad=copy.deepcopy(expected);bad['deleted_S7']['coverage']=bad['deleted_S7']['coverage'][:-1];damaged.append(('lost_orbit',bad))
    bad=copy.deepcopy(expected);bad['deleted_S7']['four_cases'][0]['spaces'][2]['dimension']=0;damaged.append(('lost_root',bad))
    bad=copy.deepcopy(expected);bad['deleted_S7']['four_cases'][0]['spaces'][2]['basis']=[[1,0,0,0,0]];damaged.append(('wrong_root',bad))
    for label,bad in damaged:need(bad!=actual,'damaged certificate passed '+label)
    pages=None
    if a.render:
        from pypdf import PdfReader
        d=a.out/'native';d.mkdir();shutil.copyfile(HERE/'mixed_bound.tex',d/'mixed_bound.tex');env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
        for k in [1,2]:
            r=subprocess.run(['pdflatex','-halt-on-error','-interaction=nonstopmode','mixed_bound.tex'],cwd=d,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60);(d/f'pass{k}.log').write_text(r.stdout);need(r.returncode==0,'native build')
        log=(d/'mixed_bound.log').read_text()
        for t in ['Overfull','LaTeX Warning:','undefined references']:need(t not in log,'native warning '+t)
        ts=[p.extract_text()or'' for p in PdfReader(d/'mixed_bound.pdf').pages];ref=load('native.json')
        need(len(ts)==ref['pages'] and [hashlib.sha256(t.encode()).hexdigest() for t in ts]==ref['page_text_sha256'],'native changed');pages=len(ts)
    report={'status':'PASS','exports':len(man['exports']),'bindings':count,'symbolic_identities':len(actual['symbolic_identities']),'deleted_involutions':actual['deleted_S7']['involutions'],'transitive_pairs':actual['deleted_S7']['transitive_pairs'],'normal_forms':len(actual['deleted_S7']['four_cases']),'scope_controls':controls,'damaged_certificate_controls':[x[0]for x in damaged],'native_pages':pages,'uniform_proof':'written; not formally verified by this program','whole_original_accepted':False}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
