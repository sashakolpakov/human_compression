import sys
if not __debug__:
    raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,hashlib,json,subprocess,time
from pathlib import Path
P=Path(__file__).resolve().parent; G=P.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--models',required=True);ap.add_argument('--seconds',type=int,default=60);a=ap.parse_args()
    if a.out.exists() or not 1<=a.seconds<=180:raise ValueError('fresh output and bounded cap')
    ids=[int(x)for x in a.models.split(',')];a.out.mkdir()
    files=[P/'automorphism_names.py',Path(__file__).resolve(),G/'doubling_component_v1/literal_joins_v3.py',G/'source_join_component_v2/construction_join.py',G/'constructions_component_v1/expected/model.json',G/'palette_serialization_v1/derived/group_elements.json',G/'source_join_component_v2/diagram_comparison01.json',G/'postprocess_target01/automorphisms.g',Path(sys.executable).resolve()]
    for i in ids:files.extend(G/f'palette_serialization_v1/derived/{s}{i}.json'for s in ['model','groups'])
    before=[pin(p)for p in files];cmd=[sys.executable,str(P/'automorphism_names.py'),'--out',str(a.out/'result'),'--models',a.models]
    (a.out/'request.json').write_text(json.dumps(dict(command=cmd,cap_seconds=a.seconds,inputs=before,target_census=False),indent=2)+'\n')
    start=time.monotonic();timed=False
    with (a.out/'stdout').open('wb')as o,(a.out/'stderr').open('wb')as e:
        try:r=subprocess.run(cmd,stdout=o,stderr=e,timeout=a.seconds);code=r.returncode
        except subprocess.TimeoutExpired:timed=True;code=None
    unchanged=before==[pin(p)for p in files]
    clean=not (a.out/'stderr').read_bytes()
    complete=code==0 and not timed and unchanged and clean and (a.out/'result/report.json').exists()
    receipt=dict(status='COMPLETE'if complete else'TIMEOUT_PRESERVED'if timed else'FAILED_PRESERVED',exit_code=code,deadline=timed,seconds=time.monotonic()-start,inputs_unchanged=unchanged,command=cmd,inputs=before,outputs=[pin(p)for p in sorted(a.out.rglob('*'))if p.is_file()],target_census=False,source_credit=0)
    (a.out/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt['status'],receipt['seconds'],flush=True)
    if not complete:raise SystemExit(1)
if __name__=='__main__':main()
