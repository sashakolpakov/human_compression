#!/usr/bin/env python3
"""Replay the written-tree packet's bounded diagnostics and elementary Lean steps."""
import argparse,hashlib,json,os,re,shutil,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def run(cmd,**kw):
    r=subprocess.run(list(map(str,cmd)),capture_output=True,text=True,timeout=180,**kw)
    return r,r.stdout+r.stderr

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--study-root',type=Path,default=ROOT.parent);ap.add_argument('--render',action='store_true')
    ap.add_argument('--gap',type=Path,default=Path('/opt/homebrew/bin/gap'))
    ap.add_argument('--xelatex',type=Path,default=Path('/opt/homebrew/bin/xelatex'))
    ap.add_argument('--lean',type=Path,default=Path('/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean'))
    ap.add_argument('--packages',type=Path,default=Path('/Users/sasha/bogachev/formal/.lake/packages'))
    a=ap.parse_args();need(not a.out.exists(),'Use a fresh output directory');a.out.mkdir(parents=True)
    scope=json.loads((ROOT/'scope.json').read_text())
    for x in scope['bound_files']:
        p=(a.study_root if x.get('external') else ROOT)/x['path'];need(sha(p)==x['sha256'],'Changed bound file: '+str(p))
    if (ROOT/'manifest.json').exists():
        for x in json.loads((ROOT/'manifest.json').read_text())['exports']:
            need(sha(ROOT/x['path'])==x['sha256'],'Changed frozen export: '+x['path'])
    r,s=run([a.gap,'-q','-b','--quitonbreak',ROOT/'check_parallel.g']);(a.out/'diagnostics.log').write_text(s)
    need(r.returncode==0 and not re.search(r'Error,|Syntax warning',s),'Diagnostic execution failed')
    flat=' '.join(s.split())
    for token in ['PASS deleted cases 57 exact selected subgroups 687 wreath cases 21','PASS binary cases 21 exact binary fibers 229 exact tail fibers 31','branching-tail control']:
        need(token in flat,'Missing finite diagnostic completion: '+token)
    pins=json.loads((ROOT/'formal/dependency_manifest.json').read_text());libs=[]
    for x in pins['packages']:
        p=a.packages/x['name'];r,s=run(['git','-C',p,'rev-parse','HEAD']);need(r.returncode==0 and s.strip()==x['rev'],'Dependency revision')
        r,s=run(['git','-C',p,'diff','--quiet','HEAD','--']);need(r.returncode==0,'Changed dependency source')
        lib=p/'.lake/build/lib/lean'
        if lib.is_dir():libs.append(str(lib))
    r,s=run([a.lean,'--version']);need(r.returncode==0 and 'version 4.32.2,' in s,'Lean version')
    env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join(libs);env.pop('LEAN_SRC_PATH',None)
    src=ROOT/'formal/ParallelIntersections.lean';raw=src.read_text()
    need(not re.search(r'\b(sorry|admit|axiom|native_decide)\b',raw),'Forbidden placeholder or unchecked tactic')
    r,s=run([a.lean,'-o',a.out/'ParallelIntersections.olean',src],env=env);(a.out/'formal.log').write_text(s)
    need(r.returncode==0 and 'warning:' not in s,'Formal replay failed')
    reports=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",s,re.S)
    need([x[0] for x in reports]==scope['formal']['declarations'],'Exact formal inventory')
    for name,ax in reports:need(set(re.findall(r'[A-Za-z][\w.]*',ax))<={'propext','Classical.choice','Quot.sound'},'Unexpected axioms')
    controls=[]
    edits=[('agreement_union','(R ∩ R\') := by','(R ∪ R\') := by'),
           ('character_generators','(hS : ∀ s ∈ S, χ s = ψ s)','(hS : True)'),
           ('character_distinction','(ht : χ t ≠ ψ t)','(ht : True)'),
           ('partition_disjunction','preserves (fun x y => P x y ∧ P\' x y) σ ↔','preserves (fun x y => P x y ∨ P\' x y) σ ↔')]
    for name,old,new in edits:
        need(old in raw,'Mutation anchor absent');p=a.out/(name+'.lean');p.write_text(raw.replace(old,new))
        rr,ss=run([a.lean,p],env=env);(a.out/(name+'.log')).write_text(ss)
        need(rr.returncode!=0 and 'error' in ss,'Invalid weakening compiled: '+name);controls.append(name)
    rendering=None
    if a.render:
        from pypdf import PdfReader
        d=a.out/'render';d.mkdir();shutil.copy2(ROOT/'parallel_trees.tex',d/'parallel_trees.tex')
        for i in range(2):
            r,s=run([a.xelatex,'-halt-on-error','-interaction=nonstopmode','parallel_trees.tex'],cwd=d);(a.out/f'render{i}.log').write_text(s);need(r.returncode==0,'Render failure')
        need(not re.search('Overfull|Missing character|LaTeX Warning|Font Warning',s),'Render diagnostics')
        old=[p.extract_text() for p in PdfReader(ROOT/'parallel_trees.pdf').pages];new=[p.extract_text() for p in PdfReader(d/'parallel_trees.pdf').pages]
        need(old==new,'Rebuilt page text changed');rendering=dict(pages=len(old),per_page_text_equal=True)
    result=dict(status='PASS',independent_mathematical_acceptance=False,source_credit=0,question_credit=0,
        finite_diagnostics=scope['programs'][0],formal=dict(declarations=len(reports),axioms='standard only',scope=scope['formal']['scope']),hypothesis_controls=controls,render=rendering)
    dump(a.out/'report.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
