"""Exact acquisition only; report any historical locator conflict without repair."""
from pathlib import Path
import json,hashlib,argparse
W=Path(__file__).resolve().parent;S=W.parents[2];R=S.parents[1]/'math_compression'
def read(p):return json.loads(p.read_text())
def need(v,m):
    if not v:raise ValueError(m)
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def collect(join,out):
    need(not out.exists(),'fresh closure');out.mkdir();deps={};errors=[];packets={}
    def add(p,r=None):
        p=Path(p).absolute()
        try:z=pin(p)
        except Exception as e:errors.append(dict(path=str(p),reason=str(e),expected=r));return
        if r and any(z[k]!=r[k]for k in ['sha256','bytes']):errors.append(dict(path=str(p),reason='literal binding mismatch',expected=r,actual=z));return
        if str(p)in deps:need(deps[str(p)]==z,'inconsistent actual path')
        deps[str(p)]=z
    def resolve(r,base):
        p=Path(r['path'])
        if p.is_absolute():return p
        ns=r.get('namespace')
        if ns=='absolute':return Path('/')/p
        if ns in ['repo','repository','public']:return R/p
        return base/p
    for k,c in read(join/'components.json').items():
        for field in ['author_manifest','gate_manifest']:
            m=Path(c[field]['path']);add(m,c[field]);d=read(m);packets[str(m)]=dict(status=d['status'],sha256=c[field]['sha256'])
            for r in d['exports']:add(resolve(r,m.parent),r)
            q=m.parent/'dependencies.json';need(q.exists(),'explicit dependencies '+str(m));add(q)
            data=read(q)
            if isinstance(data,dict):data=data.get('dependencies',data.get('bindings',data.get('inputs',None)))
            need(isinstance(data,list),'flat dependency interface '+str(q))
            for r in data:add(resolve(r,S),r)
        add(Path(c['proof']['path']),c['proof']);add(Path(c['proof_pdf']['path']),c['proof_pdf'])
    for p in [S/'sources/catalogue_L033.pdf',S/'sources/catalogue_L033.txt',W/'prepare.py',W/'joins.py',W/'principal.tex',W/'collect.py',S/'reboot_20261013/L033_work/principal_work/source_contract_work/synthesis_outline.rst']:
        add(p)
    aud=S/'reboot_20261013/L033_work/principal_work/source_contract_work/audit01'
    for p in aud.iterdir():
        if p.is_file():add(p)
    for p in join.iterdir():
        if p.is_file():add(p)
    for name,data in [('dependencies.json',[deps[k]for k in sorted(deps)]),('errors.json',errors),('packets.json',packets)]:
        (out/name).write_text(json.dumps(data,indent=2)+'\n')
    report=dict(status='PASS_EXACT_ACQUISITION'if not errors else'UNRESOLVED_EXACT_LOCATORS',dependencies=len(deps),packets=len(packets),errors=len(errors),target_censuses=0)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report));return report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--join',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();collect(a.join,a.out)
