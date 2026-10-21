#!/usr/bin/env python3
"""Check that altered proof, program, formal and clause bindings are rejected."""
import argparse,json,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def need(c,m):
    if not c: raise RuntimeError(m)

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    need(not a.out.exists(),'fresh output required');a.out.mkdir(parents=True)
    cases=[('changed_proof','sections/steiner.tex','text'),('changed_program','programs/phase265_exceptional.g','text'),('changed_formal','formal/DeletedLineFourResidue.lean','text'),('changed_clause_count','scope.json','json')]
    rows=[]
    for name,file,kind in cases:
        work=a.out/name;shutil.copytree(ROOT,work,ignore=shutil.ignore_patterns('author_replay','binding_replay','__pycache__'))
        target=work/file
        if kind=='text':
            s=target.read_text();target.write_text(s.replace('a','b',1))
        else:
            j=json.loads(target.read_text());j['counts']['L092']=34;target.write_text(json.dumps(j))
        r=subprocess.run([sys.executable,'-B','-O',str(work/'check.py'),'--out',str(a.out/(name+'_result')),'--bindings-only'],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        need(r.returncode!=0 and ('changed' in r.stdout or 'scope size' in r.stdout),'mutation accepted or unrelated failure: '+name)
        log=a.out/(name+'.log');log.write_text(r.stdout);rows.append({'control':name,'status':'REJECTED','reason':r.stdout.strip().splitlines()[-1]})
        shutil.rmtree(work);shutil.rmtree(a.out/(name+'_result'))
    report={'status':'PASS','controls':rows,'scope':'Integrity checks only; mathematical controls are in the separate full replay.'}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
