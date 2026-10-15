import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,hashlib,json,subprocess,time
from pathlib import Path
P=Path(__file__).resolve().parent;G=P.parent
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def need(v,s):
    if not v:raise ValueError(s)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--mode',choices=['doubling','truncation'],required=True);ap.add_argument('--cap',type=int,choices=[60],default=60);a=ap.parse_args();O=a.out.resolve();need(not O.exists(),'fresh output');O.mkdir()
    files=[P/'literal_joins_v3.py',P/'run_bound_v3.py',P/'small_controls.py',P/'small01/report.json',P/'approach01.rst',Path(sys.executable).resolve(),G/'palette_serialization_v1/derived/group_elements.json',G/'palette_serialization_frozen01/fresh/source_projection.json',P/'truncation01/receipt.json',P/'truncation01/result/partial.json',G/'source_join_component_v2/native/high-03.png',G/'source_join_component_v2/native/high-07.png',G/'source_join_component_v2/diagram_inventory02.json',G/'source_join_component_v2/construction_join03/joins.json',G/'source_join_component_v2/diagram_comparison01.json',G/'source_join_component_v2/construction_join.py',G/'constructions_component_v1/constructions.py',G/'constructions_component_v1/expected/model.json']+[G/f'palette_serialization_v1/derived/model{i}.json'for i in range(1,30)]
    before=[pin(p)for p in files];cmd=[sys.executable,str(P/'literal_joins_v3.py'),'--mode',a.mode,'--out',str(O/'result')]
    receipt=dict(status='RUNNING',inputs=before,command=cmd,cap_seconds=a.cap,target_census=False,literal_positive_map_search=True)
    (O/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');start=time.monotonic()
    with (O/'stdout').open('wb')as out,(O/'stderr').open('wb')as err:
        try:q=subprocess.run(cmd,stdout=out,stderr=err,timeout=a.cap);code=q.returncode;deadline=False
        except subprocess.TimeoutExpired:code=None;deadline=True
    unchanged=[pin(p)for p in files]==before
    complete=code==0 and not (O/'stderr').stat().st_size and unchanged
    receipt.update(status='COMPLETE_LITERAL_JOINS'if complete else('DEADLINE_PRESERVED'if deadline else'FAILED_PRESERVED'),exit_code=code,seconds=time.monotonic()-start,inputs_unchanged=unchanged,stdout=pin(O/'stdout'),stderr=pin(O/'stderr'))
    if (O/'result/report.json').exists():receipt['report']=pin(O/'result/report.json')
    (O/'receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt));raise SystemExit(0 if complete else 1)
if __name__=='__main__':main()
