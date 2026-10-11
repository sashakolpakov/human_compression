#!/usr/bin/env python3
"""Replay the complete finite examples and scoped algebra, without claiming formal C-induction."""
import argparse, hashlib, json, os, re, shutil, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x): Path(p).write_text(json.dumps(x,indent=2)+'\n')
def run(cmd,cwd=None,env=None):
    r=subprocess.run(list(map(str,cmd)),cwd=cwd,env=env,capture_output=True,text=True,timeout=180)
    return r.returncode,r.stdout+r.stderr

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    p.add_argument('--study-root',type=Path,default=ROOT.parent)
    p.add_argument('--gap',default='/opt/homebrew/bin/gap');p.add_argument('--render',action='store_true')
    p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex')
    p.add_argument('--lean',type=Path,default=Path('/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean'))
    p.add_argument('--packages',type=Path,default=Path('/Users/sasha/bogachev/formal/.lake/packages'));a=p.parse_args()
    need(not a.out.exists(),'Use a fresh output directory');a.out.mkdir(parents=True)
    a.out=a.out.resolve();scope=json.loads((ROOT/'scope.json').read_text())
    for b in scope['local_bindings']:need(sha(ROOT/b['path'])==b['sha256'],'Changed local binding '+b['path'])
    for b in scope['external_bindings']:need(sha(a.study_root/b['path'])==b['sha256'],'Changed retained source binding '+b['path'])
    for b in scope['proof_contexts']:
        s=(ROOT/b['path']).read_text();part=s[b['start']:b['end']]
        need(hashlib.sha256(part.encode()).hexdigest()==b['sha256'],'Changed proof context '+b['id'])
    frozen=(ROOT/'manifest.json').exists()
    if frozen:
        for b in json.loads((ROOT/'manifest.json').read_text())['exports']:
            need(sha(ROOT/b['path'])==b['sha256'],'Changed frozen export '+b['path'])
    marker='PASS matrix_unordered_IP=172 A11_unordered_IP=6240'
    src=ROOT/'check_examples.g';raw=src.read_text()
    rc,txt=run([a.gap,'-q','-b','-x','240',src]);(a.out/'examples.log').write_text(txt)
    need(rc==0 and 'Error,' not in txt and 'Syntax warning' not in txt and marker in txt,'Finite examples failed')
    controls=[]
    for name,old,new in [
      ('wrong_form','F:=z*[[1,1,0,0]','F:=z*[[2,1,0,0]'),
      ('wrong_contraction','ys:=[xs[2],xs[1]*xs[3],xs[4]]','ys:=[xs[2],xs[1]*xs[4],xs[4]]'),
      ('lost_double_edge','figures:=[[[0,2]','figures:=[[[0]'),
      ('false_recovery','Need(not xs[1] in Group(ys{[2,3]})','Need(xs[1] in Group(ys{[2,3]})')]:
        need(raw.count(old)==1,'Mutation anchor '+name)
        f=a.out/(name+'.g');f.write_text(raw.replace(old,new));cr,ct=run([a.gap,'-q','-b','-x','240',f]);(a.out/(name+'.log')).write_text(ct)
        need((cr!=0 or 'Error,' in ct) and marker not in ct,'GAP mutation accepted '+name);controls.append(name)
    pins=json.loads((ROOT/'dependency_manifest.json').read_text());libs=[]
    for x in pins['packages']:
        d=a.packages/x['name'];rc,txt=run(['git','-C',d,'rev-parse','HEAD']);need(rc==0 and txt.strip()==x['rev'],'Package pin '+x['name'])
        rc,txt=run(['git','-C',d,'diff','--quiet','HEAD','--']);need(rc==0,'Modified package source '+x['name'])
        if (d/'.lake/build/lib/lean').is_dir():libs.append(str(d/'.lake/build/lib/lean'))
    rc,txt=run([a.lean,'--version']);need(rc==0 and 'version 4.32.2,' in txt,'Lean version')
    env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join(libs);env.pop('LEAN_SRC_PATH',None)
    src=ROOT/'RankContraction.lean';raw=src.read_text()
    need(not re.search(r'\b(sorry|admit|axiom|native_decide)\b',raw),'Unpermitted placeholder/evaluator')
    rc,txt=run([a.lean,'--root='+str(ROOT),'-o',a.out/'RankContraction.olean',src],env=env);(a.out/'lean.log').write_text(txt)
    need(rc==0 and 'warning:' not in txt,'Lean compile failed or warned')
    reports=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",txt,re.S)
    need([x[0] for x in reports]==scope['declarations'],'Wrong declaration inventory')
    for name,ax in reports:need(set(re.findall(r'[A-Za-z][\w.]*',ax))<={'propext','Classical.choice','Quot.sound'},'Nonstandard axiom')
    lc=[]
    for name,old,new in [
      ('no_involution','(ha : a ^ 2 = 1)','(ha : a ^ 2 = a ^ 2)'),
      ('no_odd_order','(hbc : (b * c) ^ (2 * k + 1) = 1)','(hbc : (1 : G) = 1)'),
      ('wrong_excluded_element','(ha : χ a ≠ 1)','(ha : χ b ≠ 1)')]:
        need(old in raw,'Lean mutation anchor '+name);f=a.out/(name+'.lean');f.write_text(raw.replace(old,new))
        cr,ct=run([a.lean,'--root='+str(a.out),f],env=env);(a.out/(name+'.log')).write_text(ct)
        need(cr!=0 and 'error' in ct and 'outside of the root' not in ct,'Lean weakening accepted or not typechecked '+name);lc.append(name)
    renders=[]
    if a.render:
        from pypdf import PdfReader
        rd=a.out/'render';rd.mkdir();shutil.copy2(ROOT/'check_examples.g',rd/'check_examples.g')
        for name,pages in scope['pdf_pages'].items():
            shutil.copy2(ROOT/(name+'.tex'),rd/(name+'.tex'))
            for k in range(2):
                rc,txt=run([a.xelatex,'-halt-on-error','-interaction=nonstopmode',name+'.tex'],rd)
                (a.out/(name+f'_render{k}.log')).write_text(txt);need(rc==0,'Render failed '+name)
            need(not re.search('Overfull|Missing character|LaTeX Warning|Font Warning',txt),'Render diagnostic '+name)
            old=[x.extract_text() for x in PdfReader(ROOT/(name+'.pdf')).pages];new=[x.extract_text() for x in PdfReader(rd/(name+'.pdf')).pages]
            need(len(old)==pages and old==new,'Changed per-page PDF text '+name);renders.append({'document':name,'pages':pages,'per_page_text_equal':True})
        text=''.join(p.extract_text() for p in PdfReader(rd/'programs.pdf').pages)
        norm=lambda s:''.join(s.split())
        need(norm((ROOT/'check_examples.g').read_text()) in norm(text),'Whole GAP source is not included in appendix')
    report={'status':'PASS','frozen_exports_checked':frozen,'source_rows':len(scope['source_rows']),'proof_contexts':len(scope['proof_contexts']),
      'retained_external_bindings':len(scope['external_bindings']),'matrix_unordered_IP':172,'A11_unordered_IP':6240,
      'rejected_GAP_mutations':controls,'lean_declarations':len(reports),'axioms':'standard only','rejected_Lean_weakenings':lc,
      'render':renders,'full_program_text_included':bool(a.render),'formal_scope':scope['formal_scope'],'end_to_end_formalization':False,
      'uniform_proof_depends_on_samples':False,'required_finite_programs':1,'source_credit':0,'question_credit':0,
      'retained_construction_inputs_proved_here':False,'source_conjecture_5_1_solved':False,'compression_factor':None}
    dump(a.out/'report.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':main()
