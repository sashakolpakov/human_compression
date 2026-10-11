#!/usr/bin/env python3
"""Replay the bounded gluing packet. Finite diagnostics are not proof premises."""
import argparse,hashlib,json,os,re,shutil,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok: raise RuntimeError(msg)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x): Path(p).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def run(cmd,*,cwd=None,env=None,timeout=120):
    r=subprocess.run(list(map(str,cmd)),cwd=cwd,env=env,capture_output=True,text=True,timeout=timeout)
    return r,r.stdout+r.stderr

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--study-root',type=Path,default=ROOT.parent)
    ap.add_argument('--lean',type=Path,default=Path('/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean'))
    ap.add_argument('--packages',type=Path,default=Path('/Users/sasha/bogachev/formal/.lake/packages'))
    ap.add_argument('--gap',type=Path,default=Path('/opt/homebrew/bin/gap'))
    ap.add_argument('--xelatex',type=Path,default=Path('/opt/homebrew/bin/xelatex'))
    ap.add_argument('--render',action='store_true');a=ap.parse_args()
    need(not a.out.exists(),'Use a fresh output directory');a.out.mkdir(parents=True)
    scope=json.loads((ROOT/'scope.json').read_text());bound=[]
    for x in scope['bound_files']:
        p=(a.study_root if x.get('external') else ROOT)/x['path']
        need(sha(p)==x['sha256'],'Changed bound file: '+str(p));bound.append(x['path'])
    if (ROOT/'manifest.json').exists():
        for x in json.loads((ROOT/'manifest.json').read_text())['exports']:
            need(sha(ROOT/x['path'])==x['sha256'],'Changed frozen export: '+x['path'])
    r,s=run([a.gap,'-q',ROOT/'check_gluing.g']);(a.out/'gap.log').write_text(s)
    need(r.returncode==0 and 'Error,' not in s and 'Syntax warning' not in s,'GAP did not finish cleanly')
    need('4 weakening controls' in s and 'PASS 6 inputs' in s,'Missing GAP completion')
    need(s.count('PAIR ')==12 and s.count('ITERATED_')==2,'Missing finite cases')
    pins=json.loads((ROOT/'formal/dependency_manifest.json').read_text());libs=[];revs=[]
    for x in pins['packages']:
        p=a.packages/x['name'];r,v=run(['git','-C',p,'rev-parse','HEAD']);need(r.returncode==0 and v.strip()==x['rev'],'Package revision')
        r,v=run(['git','-C',p,'diff','--quiet','HEAD','--']);need(r.returncode==0,'Modified dependency source')
        lib=p/'.lake/build/lib/lean'
        if lib.is_dir():libs.append(str(lib))
        revs.append({'name':x['name'],'revision':x['rev']})
    r,v=run([a.lean,'--version']);need(r.returncode==0 and 'version 4.32.2,' in v,'Lean version')
    env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join(libs);env.pop('LEAN_SRC_PATH',None)
    src=ROOT/'formal/RootOrbitIntersection.lean';raw=src.read_text()
    need(not re.search(r'\b(sorry|admit|axiom|native_decide)\b',raw),'Forbidden source placeholder or unchecked tactic')
    r,s=run([a.lean,'-o',a.out/'RootOrbitIntersection.olean',src],env=env);(a.out/'lean.log').write_text(s)
    need(r.returncode==0 and 'warning:' not in s,'Lean compilation failed or warned')
    reports=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",s,re.S)
    need([x[0] for x in reports]==scope['formal']['declarations'],'Wrong declaration report')
    for name,ax in reports:need(set(re.findall(r'[A-Za-z][\w.]*',ax))<={'propext','Classical.choice','Quot.sound'},'Unexpected axioms')
    controls=[]
    edits=[('root_swap_hypothesis','(hH : hasRootSwaps H a)','(hH : True)'),
           ('fixed_point_hypothesis','(hfix : ∀ g ∈ M, g a = a)','(hfix : True)'),
           ('subgroup_intersection_hypothesis','(hIP : ∀ J K, H J ⊓ H K = H (J ∩ K))','(hIP : True)')]
    for name,old,new in edits:
        need(old in raw,'Control anchor missing');p=a.out/(name+'.lean');p.write_text(raw.replace(old,new))
        rr,ss=run([a.lean,p],env=env);(a.out/(name+'.log')).write_text(ss)
        need(rr.returncode!=0 and 'error' in ss,'Weakened hypothesis accepted: '+name);controls.append(name)
    render=None
    if a.render:
        from pypdf import PdfReader
        rd=a.out/'render';rd.mkdir();shutil.copy2(ROOT/'common_point_gluing.tex',rd/'common_point_gluing.tex')
        for i in range(2):
            rr,ss=run([a.xelatex,'-halt-on-error','-interaction=nonstopmode','common_point_gluing.tex'],cwd=rd)
            (a.out/f'render{i}.log').write_text(ss);need(rr.returncode==0,'Render failed')
        need(not re.search(r'Overfull|Missing character|LaTeX Warning|Font Warning',ss),'Render diagnostics')
        old=[p.extract_text() for p in PdfReader(ROOT/'common_point_gluing.pdf').pages]
        new=[p.extract_text() for p in PdfReader(rd/'common_point_gluing.pdf').pages]
        need(old==new,'Rendered PDF text differs');render={'pages':len(old),'per_page_text_equal':True}
    result={'status':'PASS','scope':'Author replay of bounded gluing theorem packet; no independent mathematical acceptance.',
      'source_credit':0,'question_credit':0,'ratio':None,'bindings':bound,
      'finite_diagnostics':{'paired':12,'iterated':2,'weakening_countermodels':4,'proof_premise':False},
      'lean':{'declarations':len(reports),'axioms':'standard only','scope':scope['formal']['scope'],'trusted_cached_dependencies':True,'packages':revs},
      'lean_hypothesis_controls':controls,'render':render}
    dump(a.out/'report.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
