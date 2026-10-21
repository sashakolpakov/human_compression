#!/usr/bin/env python3
"""Compile the actual output-marking obstruction with pinned dependencies."""
import argparse,hashlib,json,os,re,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(cmd,env=None):
    r=subprocess.run(list(map(str,cmd)),env=env,capture_output=True,text=True,timeout=120)
    return r.returncode,r.stdout+r.stderr

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--study-root',type=Path,default=ROOT.parent)
    p.add_argument('--lean',type=Path,default=Path('/Users/sasha/.elan/toolchains/leanprover--lean4---v4.32.2/bin/lean'));p.add_argument('--packages',type=Path,default=Path('/Users/sasha/bogachev/formal/.lake/packages'));a=p.parse_args()
    need(not a.out.exists(),'Use a fresh output directory');a.out.mkdir(parents=True)
    scope=json.loads((ROOT/'scope.json').read_text());pins=json.loads((ROOT/'dependency_manifest.json').read_text())
    for x in scope['bindings']:
        r=a.study_root if x.get('external') else ROOT;need(sha(r/x['path'])==x['sha256'],'Changed binding '+x['path'])
    if (ROOT/'manifest.json').exists():
        for x in json.loads((ROOT/'manifest.json').read_text())['exports']:need(sha(ROOT/x['path'])==x['sha256'],'Changed frozen export '+x['path'])
    libs=[]
    for x in pins['packages']:
        d=a.packages/x['name'];rc,txt=run(['git','-C',d,'rev-parse','HEAD']);need(rc==0 and txt.strip()==x['rev'],'Package pin '+x['name'])
        rc,txt=run(['git','-C',d,'diff','--quiet','HEAD','--']);need(rc==0,'Modified package source '+x['name'])
        if (d/'.lake/build/lib/lean').is_dir():libs.append(str(d/'.lake/build/lib/lean'))
    rc,txt=run([a.lean,'--version']);need(rc==0 and 'version 4.32.2,' in txt,'Lean version')
    env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join(libs);env.pop('LEAN_SRC_PATH',None)
    src=ROOT/'RankExtensionObstruction.lean';raw=src.read_text()
    need(not re.search(r'\b(sorry|admit|axiom|native_decide)\b',raw),'Unpermitted proof placeholder or evaluator')
    rc,txt=run([a.lean,'-o',a.out/'RankExtensionObstruction.olean',src],env);(a.out/'lean.log').write_text(txt)
    need(rc==0 and 'warning:' not in txt,'Compilation failed or warned')
    reports=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",txt,re.S)
    need([x[0] for x in reports]==scope['declarations'],'Declaration inventory')
    for name,ax in reports:need(set(re.findall(r'[A-Za-z][\w.]*',ax))<={'propext','Classical.choice','Quot.sound'},'Nonstandard axiom')
    controls=[]
    for name,old,new in [('sigma_removed','def sigma : Equiv.Perm (Fin 10) := Equiv.swap 5 6','def sigma : Equiv.Perm (Fin 10) := 1'),('left_word_twist_removed','else if i = 2 then Equiv.swap 2 9 * sigma','else if i = 2 then Equiv.swap 2 9'),('label_sets_overlap','def rightLabels : Set (Fin 5) := {3, 4}','def rightLabels : Set (Fin 5) := {2, 4}')]:
        need(raw.count(old)==1,'Mutation anchor');f=a.out/(name+'.lean');f.write_text(raw.replace(old,new));cr,ct=run([a.lean,f],env);(a.out/(name+'.log')).write_text(ct)
        need(cr!=0 and 'error' in ct,'Incorrect mutation compiled');controls.append(name)
    report={'status':'PASS','declarations':len(reports),'axioms':'standard only','rejected_mutations':controls,'scope':scope['formal_scope'],'old_input_C_formalized':False,'source_hypotheses_formalized':False,'trusted_cached_dependencies':True,'source_credit':0,'question_credit':0}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
