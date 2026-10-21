#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,time

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,message):
    if not ok:raise RuntimeError(message)
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--source');args=p.parse_args()
    out=Path(args.out).expanduser();need(not out.exists() and not out.is_symlink(),'output must be fresh');out=out.resolve();out.mkdir(parents=True)
    root=Path(__file__).resolve().parent;start=time.monotonic()
    manifest=json.loads((root/'manifest.json').read_text())
    for row in manifest['exports']:
        path=root/row['path'];need(path.is_file() and not path.is_symlink(),'file '+row['path']);need(sha(path)==row['sha256'] and path.stat().st_size==row['bytes'],'binding '+row['path'])
    scope=json.loads((root/'scope.json').read_text())
    need(scope['required_finite_premises']==[] and scope['lean_declarations']==0,'scope')
    source_verified=False
    if args.source:
        need(sha(Path(args.source))==scope['source']['sha256'],'primary binding');source_verified=True
    reports={}
    for key,script in [('literal','programs/literal_twist.py'),('controls','controls.py')]:
        proc=subprocess.run([sys.executable,'-B','-O',str(root/script)],capture_output=True,text=True)
        (out/(key+'.stdout')).write_text(proc.stdout);(out/(key+'.stderr')).write_text(proc.stderr)
        need(proc.returncode==0,'failed '+key);value=json.loads(proc.stdout);need(value['status']=='PASS','status '+key)
        reference=json.loads((root/('validation.json' if key=='literal' else 'control_report.json')).read_text());need(value==reference,'replay '+key)
        reports[key]=value
    result={'status':'PASS','manifest_sha256':sha(root/'manifest.json'),'exports':len(manifest['exports']),'source_verified':source_verified,'reports':reports,'elapsed_seconds':time.monotonic()-start,'formal_scope':'No Lean; finite computations validate the uniform written proof.'}
    (out/'report.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
