"""Retain a deadline-bound GAP execution; no partial result earns completeness."""
import sys
if sys.flags.optimize:
    raise SystemExit("optimized execution is unsupported")
import argparse, hashlib, json, os, pathlib, subprocess, time

HERE = pathlib.Path(__file__).resolve().parent
TYPES = {
    '3434': ('square',[3,4,3,4],[48,48,48,48],9216),
    '3334': ('square',[3,3,3,4],[24,48,48,24],7680),
    '3335': ('square',[3,3,3,5],[24,120,120,24],7200),
    '3534': ('square',[3,5,3,4],[120,48,48,120],2160),
    '3535': ('square',[3,5,3,5],[120,120,120,120],9720),
    '353': ('string',[3,5,3],[120,12,12,120],8160),
    '435': ('string',[4,3,5],[120,20,16,48],7680),
    '535': ('string',[5,3,5],[120,20,20,120],8160),
    '5333': ('star',[5,3,3],[8,24,120,120],7680),
}
def pin(path):
    b=path.read_bytes(); return {'path':str(path),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
def main():
    p=argparse.ArgumentParser(); p.add_argument('--type',choices=TYPES,required=True)
    p.add_argument('--bound',type=int); p.add_argument('--seconds',type=int,default=120)
    p.add_argument('--out',type=pathlib.Path,required=True); a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=False); a.out=a.out.resolve()
    shape,labels,local,default=TYPES[a.type]; bound=a.bound or default
    M=[[1 if i==j else 2 for j in range(4)] for i in range(4)]
    edges={'square':[(0,1),(1,2),(2,3),(3,0)],'string':[(0,1),(1,2),(2,3)],'star':[(0,1),(0,2),(0,3)]}[shape]
    for (i,j),v in zip(edges,labels): M[i][j]=M[j][i]=v
    driver=a.out/'driver.g'; records=a.out/'records.g'
    driver.write_text(f'Read({json.dumps(str(HERE/"enumerate.g"))});;\nRunHyperbolic({M},{local},{bound},{json.dumps(str(records))});;\nQUIT;\n')
    cmd=['/opt/homebrew/bin/gap','-q','-b','--quitonbreak',str(driver)]
    start=time.monotonic(); report={'status':'RUNNING','type':a.type,'bound':bound,'seconds_cap':a.seconds,'matrix':M,'local_orders':local,'command':cmd,'inputs':[pin(pathlib.Path(__file__)),pin(HERE/'enumerate.g'),pin(driver)],'whole_original_credit':0}
    (a.out/'active.json').write_text(json.dumps(report,indent=2)+'\n')
    env=os.environ.copy(); env.pop('PYTHONOPTIMIZE',None)
    with (a.out/'stdout').open('wb') as so,(a.out/'stderr').open('wb') as se:
        try:
            r=subprocess.run(cmd,stdout=so,stderr=se,timeout=a.seconds,env=env)
            report['returncode']=r.returncode
            text=(a.out/'stdout').read_text(); err=(a.out/'stderr').read_text()
            report['status']='PASS' if r.returncode==0 and f'COMPLETE_HYPERBOLIC_BOUND {bound} ' in text and not err.strip() and not any(x in text for x in ['Syntax warning','Error,','Error:']) else 'FAIL'
        except subprocess.TimeoutExpired:
            report['status']='TIMEOUT_NO_CERTIFICATE'
    report['seconds']=time.monotonic()-start
    report['outputs']=[pin(q) for q in (a.out/'stdout',a.out/'stderr',records) if q.exists()]
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n'); (a.out/'active.json').write_text(json.dumps({'status':'TERMINAL','report':pin(a.out/'report.json')},indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','type','bound','seconds']}),flush=True)
    if report['status']!='PASS': raise SystemExit(1)
if __name__=='__main__': main()
