"""One fixed sixty-second certificate probe; preserves every terminal outcome."""
import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,datetime,hashlib,json,os,subprocess,time
from pathlib import Path
def need(ok,text):
    if not ok:raise ValueError(text)
def pin(p):
    b=Path(p).read_bytes();return dict(path=str(Path(p)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def main():
    a=argparse.ArgumentParser();a.add_argument('--request',type=Path,required=True);a.add_argument('--check-only',action='store_true');args=a.parse_args()
    request=args.request.resolve();raw=request.read_bytes();r=json.loads(raw)
    need(r['scope']=='FIXED_L100_GEOMETRY_33_BAER_PROBE'and r['external_cap_seconds']==60,'exact narrow request')
    need(r['new_group_or_subgroup_or_aut_or_graph_searches']==0,'fixed computational scope')
    need(r['command']==[r['python'],r['certificate'],'--out',r['certificate_output']],'literal actual command')
    need(len({v['path']for v in r['inputs']})==len(r['inputs']),'unique input paths')
    for v in r['inputs']:need(pin(v['path'])==v,'exact input '+v['path'])
    need(pin(Path(__file__).resolve())in r['inputs'],'executed runner pinned')
    if args.check_only:print('PASS_GEOMETRY33_PROBE_PREFLIGHT',len(r['inputs']));return
    out=Path(r['receipt_folder']);need(out.is_absolute()and not out.exists()and out.parent.is_dir(),'fresh receipt folder')
    need(not Path(r['certificate_output']).exists(),'fresh certificate output')
    out.mkdir();start=time.monotonic();receipt=dict(status='ACTIVE',request=pin(request),inputs=r['inputs'],command=r['command'],external_cap_seconds=60,
        started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),target_census=False,new_literal_construction_probe=True,source_credit=0)
    def save():
        tmp=out/'receipt.tmp';tmp.write_text(json.dumps(receipt,indent=2)+'\n');tmp.replace(out/'receipt.json')
    save();env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');env.pop('PYTHONOPTIMIZE',None)
    try:
        q=subprocess.run(r['command'],capture_output=True,timeout=60,env=env);stdout,stderr,code=q.stdout,q.stderr,q.returncode
        receipt['status']='RETURNED'
    except subprocess.TimeoutExpired as e:stdout,stderr,code=e.stdout or b'',e.stderr or b'',None;receipt['status']='DEADLINE_NO_COMPLETE_CERTIFICATE'
    except Exception as e:stdout,stderr,code=b'',repr(e).encode(),None;receipt['status']='LAUNCH_FAILURE'
    (out/'stdout').write_bytes(stdout);(out/'stderr').write_bytes(stderr)
    receipt.update(returncode=code,seconds=time.monotonic()-start,stdout=pin(out/'stdout'),stderr=pin(out/'stderr'),finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    try:
        for v in r['inputs']:need(pin(v['path'])==v,'input changed '+v['path'])
        need(request.read_bytes()==raw,'request changed');receipt['inputs_unchanged']=True
    except Exception as e:receipt.update(status='INPUT_CHANGED_NO_CERTIFICATE',inputs_unchanged=False,input_error=repr(e))
    if receipt['status']=='RETURNED':
        if code==0 and not stderr:
            try:
                f=Path(r['certificate_output'])/'certificate.json';value=json.loads(f.read_text())
                need(value['status']=='PASS_LITERAL_BAER_GEOMETRY_33_CONSTRUCTIONS','complete certificate marker')
                receipt.update(status='COMPLETE_LITERAL_CONSTRUCTION_PROBE',certificate=pin(f))
            except Exception as e:
                receipt.update(status='FAILED_COMPLETION_CHECK_NO_CERTIFICATE',completion_error=repr(e))
        else:receipt['status']='FAILED_NO_COMPLETE_CERTIFICATE'
    save();print(json.dumps(receipt))
if __name__=='__main__':main()
