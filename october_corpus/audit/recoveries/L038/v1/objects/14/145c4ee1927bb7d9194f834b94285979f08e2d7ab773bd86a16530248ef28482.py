#!/usr/bin/env python3
"""Replay the bounded diagnostics, actual generic Lean lemmas, and exact edition."""
import argparse,hashlib,json,os,re,shutil,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n')
def run(cmd,cwd=None,env=None):
    r=subprocess.run(list(map(str,cmd)),cwd=cwd,env=env,capture_output=True,text=True,timeout=120)
    return r.returncode,r.stdout+r.stderr

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--study-root',type=Path,default=ROOT.parent)
    p.add_argument('--public-root',type=Path);p.add_argument('--gap',default='/opt/homebrew/bin/gap');p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex')
    p.add_argument('--lean',type=Path,default=Path('/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean'));p.add_argument('--packages',type=Path,default=Path('/Users/sasha/bogachev/formal/.lake/packages'));a=p.parse_args()
    need(not a.out.exists(),'Use a fresh output directory');a.out.mkdir(parents=True)
    scope=json.loads((ROOT/'scope.json').read_text());pins=json.loads((ROOT/'dependency_manifest.json').read_text())
    for x in scope['bound_files']:need(sha(ROOT/x['path'])==x['sha256'],'Changed local binding '+x['path'])
    for x in scope['external_bindings']:need(sha(a.study_root/x['path'])==x['sha256'],'Changed source/previous packet '+x['path'])
    audit=json.loads((ROOT/'dependency_audit.json').read_text())
    if a.public_root:
        for x in audit['bound_read_files']:need(sha(a.public_root/x['path'])==x['sha256'],'Changed audited public proof '+x['path'])
    frozen=(ROOT/'manifest.json').exists()
    if frozen:
        for x in json.loads((ROOT/'manifest.json').read_text())['exports']:need(sha(ROOT/x['path'])==x['sha256'],'Changed frozen export '+x['path'])
    raw=(ROOT/'check_kernels.g').read_text();marker='PASS kernel_cases=600 leaf_cases=180 leaf_positive=144 leaf_negative=36 split_cases=312 split_positive=276 split_negative=36 rectangle_cases=225 parity_parameters=5 assumption_controls=4'
    rc,txt=run([a.gap,'-q','-b','-x','240',ROOT/'check_kernels.g']);(a.out/'gap.log').write_text(txt)
    need(rc==0 and 'Error,' not in txt and 'Syntax warning' not in txt and marker in txt,'Bounded diagnostic failed')
    gapcontrols=[]
    mutations=[
        ('kernel_test_discarded','return ForAll(KernelRows(xs,a,domain),r->r[4]);','return true;'),
        ('wrong_prefix_orbit','rootOrbit:=Orbit(prev,a);','rootOrbit:=Orbit(next,a);'),
        ('split_twist_discarded','beta:=Swap(a,b)*xs[i];','beta:=();')]
    for name,old,new in mutations:
        need(raw.count(old)==1,'Mutation anchor '+name);f=a.out/(name+'.g');f.write_text(raw.replace(old,new));cr,ct=run([a.gap,'-q','-b','-x','240',f]);(a.out/(name+'.log')).write_text(ct)
        need((cr!=0 or 'Error,' in ct) and marker not in ct,'Incorrect GAP mutation accepted '+name);gapcontrols.append(name)
    libs=[]
    for x in pins['packages']:
        d=a.packages/x['name'];rc,txt=run(['git','-C',d,'rev-parse','HEAD']);need(rc==0 and txt.strip()==x['rev'],'Package pin '+x['name'])
        rc,txt=run(['git','-C',d,'diff','--quiet','HEAD','--']);need(rc==0,'Modified package source '+x['name'])
        if (d/'.lake/build/lib/lean').is_dir():libs.append(str(d/'.lake/build/lib/lean'))
    rc,txt=run([a.lean,'--version']);need(rc==0 and 'version 4.32.2,' in txt,'Lean version')
    env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join(libs);env.pop('LEAN_SRC_PATH',None)
    src=ROOT/'RestrictionKernelCriterion.lean';raw=src.read_text();need(not re.search(r'\b(sorry|admit|axiom|native_decide)\b',raw),'Unpermitted placeholder/evaluator')
    rc,txt=run([a.lean,'-o',a.out/'RestrictionKernelCriterion.olean',src],env=env);(a.out/'lean.log').write_text(txt)
    need(rc==0 and 'warning:' not in txt,'Lean compile failed or warned')
    reports=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",txt,re.S)
    need([x[0] for x in reports]==scope['declarations'],'Wrong declaration inventory')
    for name,ax in reports:need(set(re.findall(r'[A-Za-z][\w.]*',ax))<={'propext','Classical.choice','Quot.sound'},'Nonstandard axiom')
    leancontrols=[]
    mutations=[('subgroup_containment_reversed','(hPQ : P ≤ Q)','(hPQ : Q ≤ P)'),('kernel_containment_weakened','Q ⊓ f.ker ≤ P','Q ⊓ f.ker ≤ Q')]
    for name,old,new in mutations:
        need(old in raw,'Lean mutation anchor');f=a.out/(name+'.lean');f.write_text(raw.replace(old,new));cr,ct=run([a.lean,f],env=env);(a.out/(name+'.log')).write_text(ct)
        need(cr!=0 and 'error' in ct,'Incorrect Lean weakening compiled');leancontrols.append(name)
    render=None
    if a.render:
        from pypdf import PdfReader
        rd=a.out/'render';rd.mkdir();shutil.copy2(ROOT/'restriction_kernels.tex',rd/'restriction_kernels.tex')
        for k in range(2):
            rc,txt=run([a.xelatex,'-halt-on-error','-interaction=nonstopmode','restriction_kernels.tex'],rd);(a.out/f'render{k}.log').write_text(txt);need(rc==0,'Render failed')
        need(not re.search('Overfull|Missing character|LaTeX Warning|Font Warning',txt),'Render diagnostics')
        old=[x.extract_text() for x in PdfReader(ROOT/'restriction_kernels.pdf').pages];new=[x.extract_text() for x in PdfReader(rd/'restriction_kernels.pdf').pages]
        need(len(old)==scope['expected_pages'] and old==new,'PDF page text changed');render={'pages':len(old),'per_page_text_equal':True}
    result={'status':'PASS','frozen_exports_checked':frozen,'source_and_previous_packets_checked':len(scope['external_bindings']),'audited_public_proof_bindings_checked':len(audit['bound_read_files']) if a.public_root else None,'bounded_cases':scope['programs'][0]['cases'],'rejected_gap_mutations':gapcontrols,'lean_declarations':len(reports),'axioms':'standard only','rejected_lean_weakenings':leancontrols,'render':render,'formal_scope':scope['formal_scope'],'full_uniform_theorems_formalized':False,'finite_tests_are_uniform_premises':False,'trusted_cached_dependencies':True,'source_credit':0,'question_credit':0}
    dump(a.out/'report.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
