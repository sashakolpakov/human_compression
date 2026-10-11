#!/usr/bin/env python3
"""Replay the exact N007 written boundary, finite validations and scoped Lean."""
import argparse, hashlib, json, os, pathlib, re, subprocess, sys, time
ROOT=pathlib.Path(__file__).resolve().parent
def need(ok,msg):
    if not ok: raise RuntimeError('DIAGONAL_REJECT '+msg)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser()
    for key in ['out','gap','lean','packages']: ap.add_argument('--'+key,type=pathlib.Path,required=True)
    ap.add_argument('--study-root',type=pathlib.Path)
    ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='xelatex')
    a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh raw output')
    out=a.out.resolve();need(not out.exists(),'fresh resolved output');out.mkdir(parents=True)
    started=time.monotonic();runs=[]
    manifest=ROOT/'manifest.json';exports=json.loads(manifest.read_text())['exports'] if manifest.exists() else []
    def verify():
        for row in exports:
            p=pathlib.PurePosixPath(row['path']);need(not p.is_absolute() and '..' not in p.parts,'safe path')
            q=ROOT/p;need(q.is_file() and q.stat().st_size==row['bytes'] and sha(q)==row['sha256'],'binding '+str(p))
    verify()
    contract=json.loads((ROOT/'contract.json').read_text());ledger=json.loads((ROOT/'source_clause_map.json').read_text())
    need(contract['source_id']=='N007' and contract['source_credit']==0 and contract['question_credit']==0,'candidate scope')
    need(contract['N006_whole_principal_recovered'] is False,'no N006 whole-source claim')
    need(contract['required_finite_programs']==0 and contract['validation_programs']==1,'finite evidence boundary')
    need(len(ledger['rows'])==32 and len({r['id'] for r in ledger['rows']})==32,'32 distinct source clauses')
    for name,row in ledger['proof_spans'].items():
        raw=b''.join((ROOT/row['path']).read_bytes().splitlines(keepends=True)[row['start_line']-1:row['end_line']])
        need(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'complete span '+name)
    if a.study_root:
        for row in contract['primary_bindings']:
            q=a.study_root/row['path'];need(q.stat().st_size==row['bytes'] and sha(q)==row['sha256'],'primary '+row['id'])
    def run(label,cmd,env=None):
        t=time.monotonic();r=subprocess.run([str(x) for x in cmd],cwd=out,env=env,text=True,capture_output=True,timeout=180)
        (out/(label+'.stdout')).write_text(r.stdout);(out/(label+'.stderr')).write_text(r.stderr)
        runs.append({'label':label,'returncode':r.returncode,'seconds':round(time.monotonic()-t,4),'stdout_sha256':sha(out/(label+'.stdout')),'stderr_sha256':sha(out/(label+'.stderr'))})
        return r
    r=run('gap_version',[a.gap,'-q','-T','-c','Print(GAPInfo.Version,"\\n");QUIT;'])
    need(r.returncode==0 and r.stdout.strip()=='4.15.1','GAP pin')
    r=run('finite',[a.gap,'-q','-T',ROOT/'programs/diagonal_models.g'])
    need(r.returncode==0 and not re.search('Error|warning',r.stdout+r.stderr,re.I),'clean finite replay')
    for token in ['order=48 IP=64 FT=512 PASS','order=1152 IP=256 FT=4096 PASS','DIAGONAL_MODELS_COMPLETE']:need(token in r.stdout,'finite completion '+token)
    text=(ROOT/'programs/diagonal_models.g').read_text();controls=[]
    for label,old,new in [('wrong_group_order',',1152,ord)',',576,ord)'),('wrong_doubled_label','ord[2][3]:=4','ord[2][3]:=2')]:
        need(text.count(old)==1,'unique finite control');bad=out/(label+'.g');bad.write_text(text.replace(old,new))
        r=run(label,[a.gap,'-q','-T',bad]);need('Error' in r.stdout+r.stderr and 'DIAGONAL_MODELS_COMPLETE' not in r.stdout,'finite rejection '+label);controls.append(label)
    deps=json.loads((ROOT/'formal/dependency_manifest.json').read_text());pins=[]
    for row in deps['packages']:
        folder=a.packages/row['name'];rev=subprocess.check_output(['git','-C',folder,'rev-parse','HEAD'],text=True).strip()
        need(rev==row['rev'],'dependency pin');need(subprocess.run(['git','-C',folder,'diff','--quiet','HEAD','--']).returncode==0,'clean dependency');pins.append(row)
    need('version 4.32.2,' in subprocess.check_output([a.lean,'--version'],text=True),'Lean pin')
    env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join(str(p/'.lake/build/lib/lean') for p in a.packages.iterdir() if (p/'.lake/build/lib/lean').is_dir())
    text=(ROOT/'formal/OrbitTwisting.lean').read_text();need(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s',text,re.M),'proof holes')
    target=out/'OrbitTwisting.lean';target.write_text(text)
    r=run('formal',[a.lean,'-o',out/'OrbitTwisting.olean',target],env)
    need(r.returncode==0 and not re.search('error:|warning:|sorryAx',r.stdout+r.stderr),'clean Lean')
    reports=re.findall(r"'OrbitTwisting\.([^']+)' depends on axioms: \[([^\]]*)\]",r.stdout)
    scope=json.loads((ROOT/'formal/scope.json').read_text());need([n for n,_ in reports]==scope['names'],'eight exact declarations')
    for _,axioms in reports:need(set(x.strip() for x in axioms.split(',') if x.strip())<={'propext','Classical.choice','Quot.sound'},'standard axioms')
    for label,old,new in [('wrong_complement','(I \\ M) ∪ (I \\ N) = I \\ (M ∩ N)','(I \\ M) ∩ (I \\ N) = I \\ (M ∩ N)'),('false_double','orderOf g = 2 * orderOf (g ^ 2)','orderOf g = 3 * orderOf (g ^ 2)'),('wrong_support_union','support f (R ∪ S) k =','support f (R ∩ S) k =')]:
        need(text.count(old)==1,'unique Lean control '+label);bad=out/(label+'.lean');bad.write_text(text.replace(old,new));r=run(label,[a.lean,bad],env)
        need(r.returncode!=0 and 'error:' in r.stdout+r.stderr,'Lean rejection '+label);controls.append(label)
    rendered=None
    if a.render:
        r=run('render',[sys.executable,ROOT/'build.py','--out',out/'render','--xelatex',a.xelatex]);need(r.returncode==0,'render replay');rendered=json.loads((out/'render/report.json').read_text())
    verify();report={'status':'PASS','seconds':round(time.monotonic()-started,4),'exports_checked':len(exports),'clauses':32,'proof_spans':len(ledger['proof_spans']),'formal_declarations':len(reports),'axiom_reports':reports,'controls_rejected':controls,'executions':runs,'dependencies':pins,'render':rendered,'primary_checked':bool(a.study_root),'validation_models':[{'order':48,'IP':64,'FT':512},{'order':1152,'IP':256,'FT':4096}],'required_finite_programs':0,'validation_programs':1,'source_credit':0,'question_credit':0,'ratio':None}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','seconds':report['seconds'],'report':str(out/'report.json')}))
if __name__=='__main__':main()
