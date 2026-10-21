import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,hashlib,json,subprocess,time
from pathlib import Path
P=Path(__file__).resolve().parent;G=P.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();O=a.out.resolve()
    if O.exists():raise ValueError('fresh output')
    O.mkdir();files=[P/'objects_v2.py',P/'run_bound_v2.py',Path(sys.executable).resolve(),G/'constructions_component_v1/expected/model.json',G/'baer_component_v1/inputs/baer_orbits.json',G/'palette_serialization_v1/derived/group_elements.json']
    before=[pin(p)for p in files];cmd=[sys.executable,str(P/'objects_v2.py'),'--out',str(O/'result')];r=dict(status='RUNNING',inputs=before,command=cmd,cap_seconds=60,target_census=False,finite_object_construction=True)
    (O/'receipt.json').write_text(json.dumps(r,indent=2)+'\n');start=time.monotonic()
    with (O/'stdout').open('wb')as out,(O/'stderr').open('wb')as err:
        try:q=subprocess.run(cmd,stdout=out,stderr=err,timeout=60);code=q.returncode;deadline=False
        except subprocess.TimeoutExpired:code=None;deadline=True
    same=[pin(p)for p in files]==before;ok=code==0 and not (O/'stderr').stat().st_size and same
    r.update(status='COMPLETE_LITERAL_OBJECTS'if ok else('DEADLINE_PRESERVED'if deadline else'FAILED_PRESERVED'),exit_code=code,seconds=time.monotonic()-start,inputs_unchanged=same,stdout=pin(O/'stdout'),stderr=pin(O/'stderr'))
    if (O/'result/objects.json').exists():r['result']=pin(O/'result/objects.json')
    (O/'receipt.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r));raise SystemExit(0 if ok else 1)
if __name__=='__main__':main()
