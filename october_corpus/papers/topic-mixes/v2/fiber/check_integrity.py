#!/usr/bin/env python3
"""Reject changed frozen inputs before any proof replay; operational control only."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def need(p,m):
    if not p:raise RuntimeError(m)
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--study-root',type=Path,default=ROOT.parent);a=p.parse_args()
    need(not a.out.exists(),'fresh output directory required');a.out.mkdir(parents=True)
    m=json.loads((ROOT/'manifest.json').read_text());cases=[]
    for label,path in [('changed_written_proof','fiber_intersections.tex'),('changed_required_program','check_coprime.g'),('changed_scope','scope.json')]:
        d=a.out/label;d.mkdir()
        for x in m['exports']:
            data=(ROOT/x['path']).read_bytes();need(hashlib.sha256(data).hexdigest()==x['sha256'],'Changed source export')
            q=d/x['path'];q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
        (d/'manifest.json').write_bytes((ROOT/'manifest.json').read_bytes())
        q=d/path;q.write_bytes(q.read_bytes()+b'\n ')
        result=subprocess.run([sys.executable,'-B','-O',d/'check.py','--study-root',a.study_root,'--out',d/'replay'],capture_output=True,text=True,timeout=30)
        log=result.stdout+result.stderr;(a.out/(label+'.log')).write_text(log)
        need(result.returncode!=0 and ('Changed local input '+path in log or 'Changed frozen export '+path in log),'Integrity corruption accepted or wrong failure: '+label)
        need(not (d/'replay/cop rime.log'.replace(' ','')).exists(),'Expensive proof ran before binding failure')
        cases.append({'name':label,'changed_path':path,'rejected_before_proof_replay':True})
    result={'status':'PASS','controls':cases,'original_manifest_sha256':hashlib.sha256((ROOT/'manifest.json').read_bytes()).hexdigest()}
    (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
