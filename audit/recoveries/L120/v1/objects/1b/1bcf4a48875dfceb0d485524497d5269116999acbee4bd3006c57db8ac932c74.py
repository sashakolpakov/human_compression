"""Bounded, receipt-preserving execution of fixed involution-class branches."""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
import argparse, hashlib, json, math, os, re, signal, subprocess, time
from pathlib import Path
W=Path(__file__).resolve().parent
def need(b,s):
    if not b: raise ValueError(s)
def pin(p):
    b=p.read_bytes()
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,x):
    t=p.with_suffix('.writing');t.write_text(json.dumps(x,indent=2)+'\n');t.replace(p)
def parse(path,n,kind,limit):
    text=path.read_text()
    need(text.count('COMPLETE_EXHAUSTION')==1,'exact terminal marker')
    order=math.factorial(n)//(2 if kind=='even' else 1)
    need(re.search(rf'DEGREE\s+{n}\s+RANK_LIMIT\s+{limit}\s+GROUP_ORDER\s+{order}\b',text),'header')
    pat=r'MARK\s+(\[.*?\])\s+ORDER\s+(\d+)\s+TYPE\s+(\[.*?\])\s+SELF_DUAL_PERMUTATION\s+(true|false)'
    marks=[];counts={str(r):{'ordered':0,'self_dual':0}for r in range(3,limit+1)}
    for ids,o,typ,selfdual in re.findall(pat,text,re.S):
        ids=json.loads(ids);typ=json.loads(typ);r=len(ids)
        need(3<=r<=limit and len(typ)==r-1,'mark format')
        marks.append({'ids':ids,'order':int(o),'type':typ,'self_dual':selfdual=='true'})
        if int(o)==order:
            counts[str(r)]['ordered']+=1
            counts[str(r)]['self_dual']+=selfdual=='true'
    printed={int(r):int(c)for r,c in re.findall(r'RANK\s+(\d+)\s+MARKS\s+(\d+)',text)}
    need(set(printed)==set(range(3,limit+1)),'all rank headings')
    for r,c in printed.items():need(sum(len(m['ids'])==r for m in marks)==c,'all literal records parsed')
    return {'counts':counts,'transitive_records':len(marks),'marks':marks}
def execute(spec,out,cap):
    kind,n,limit,branch=spec['kind'],spec['degree'],spec['rank_limit'],spec.get('branch')
    out.mkdir(parents=True,exist_ok=False)
    engine=W/f'enumerate_{kind}{"_pool" if spec.get("engine_entry")=="pool" else ("_connected" if spec.get("engine_entry")=="connected" else ("_domain" if spec.get("engine_entry")=="domain" else ("_direct" if spec.get("engine_entry")=="direct" else ("_parts" if branch is not None else ""))))}.g'
    driver=out/'driver.g'
    driver.write_text(f'degree:={n};;rankLimit:={limit};;\n'+(f'rootTranspositions:={branch};;\n'if branch is not None else '')+f'Read({json.dumps(str(engine))});\n')
    base={'spec':spec,'cap_seconds':cap,'engine':pin(engine),'driver':pin(driver),'runner':pin(Path(__file__)),'start_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
    env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
    start=time.monotonic()
    with (out/'stdout.log').open('wb') as so,(out/'stderr.log').open('wb') as se:
        p=subprocess.Popen(['/opt/homebrew/bin/gap','-q','-T',str(driver)],stdout=so,stderr=se,env=env,start_new_session=True)
        save(out/'running.json',dict(base,pid=p.pid,deadline_unix=time.time()+cap,status='RUNNING'))
        try:p.wait(timeout=cap);status='TERMINAL'
        except subprocess.TimeoutExpired:
            os.killpg(p.pid,signal.SIGTERM)
            try:p.wait(timeout=5)
            except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);p.wait()
            status='CAPPED_INCOMPLETE'
    report=dict(base,status=status,returncode=p.returncode,elapsed_seconds=time.monotonic()-start,stdout=pin(out/'stdout.log'),stderr=pin(out/'stderr.log'))
    if status=='TERMINAL':
        try:
            need(p.returncode==0,'GAP return code');need((out/'stderr.log').read_text().strip()=='','GAP stderr')
            result=parse(out/'stdout.log',n,kind,limit);save(out/'result.json',result)
            report.update(status='COMPLETE_FIXED_BRANCH' if branch is not None else 'COMPLETE_CONTROL',result=pin(out/'result.json'))
        except Exception as e:report.update(status='FAILED_CHECK',error=repr(e))
    save(out/'report.json',report)
    print(json.dumps({'out':str(out),'status':report['status'],'elapsed_seconds':report['elapsed_seconds']}),flush=True)
    return report
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--plan',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    plan=json.loads(a.plan.read_text());a.out.mkdir(parents=True,exist_ok=True)
    reports=[]
    for item in plan['runs']:
        dest=a.out/item['name']
        if (dest/'report.json').exists():
            prior=json.loads((dest/'report.json').read_text())
            need(prior['spec']==item['spec'],'resume specification')
            need(prior['status']in('COMPLETE_CONTROL','COMPLETE_FIXED_BRANCH'),'noncomplete prior attempt requires a new explicit plan and destination')
            need(prior['engine']==pin(Path(prior['engine']['path'])),'resumed engine changed')
            need(prior['result']==pin(dest/'result.json'),'resumed result changed')
            reports.append(prior);continue
        need(not dest.exists(),'interrupted directory requires separate reviewed restart')
        reports.append(execute(item['spec'],dest,item['cap_seconds']))
        save(a.out/'queue_receipt.json',{'plan':pin(a.plan),'reports':reports})
        if reports[-1]['status']=='FAILED_CHECK':raise RuntimeError('stop queue after failed check')
        if (a.out/'STOP_AFTER_CURRENT').exists():
            save(a.out/'stopped.json',{'status':'STOPPED_AFTER_CURRENT','completed_attempts':len(reports)});sys.exit(0)
    save(a.out/'queue_receipt.json',{'plan':pin(a.plan),'reports':reports,'terminal':True})
