"""Recheck the exact completed distinct review; no scientific replay."""
import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,hashlib,json
P=Path(__file__).resolve().parent
STATUS='ACCEPTED_L033_DIVISOR_TARGET9720_COMPONENT_V1'
AUTHOR='d24447e9377bfd6d0aae82b9ef9b5b81631231226646ef8bbe308dd66353906b'
def read(p):return json.loads(Path(p).read_text())
def need(v,m):
    if not v:raise ValueError(m)
def exact(r,p=None):
    b=Path(p or r['path']).read_bytes()
    need(len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],str(p or r['path']))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(a.out.is_absolute() and not a.out.exists(),'fresh absolute output')
    m=read(P/'manifest.json');d=read(P/'dependencies.json');r=read(P/'review.json')
    need(m['status']==r['status']==STATUS,'decision')
    for row in m['exports']:
        q=Path(row['path']);need(not q.is_absolute() and '..'not in q.parts,'safe export');exact(row,P/q)
    for row in d:exact(row)
    need(len({x['path']for x in d})==len(d),'unique dependencies')
    exact(r['author_manifest']);need(r['author_manifest']['sha256']==AUTHOR,'author')
    c=read(P/'fresh_receipt.json')
    need(c['status']=='CLEAN_FINITE_RETURN' and c['returncode']==0 and not c['deadline'] and c['inputs_unchanged'] and c['stderr_empty'] and c['target_census'],'clean finite target receipt')
    for row in c['outputs']:exact(row)
    f=read(P/'fresh_report.json')
    expected=dict(status='PASS_DIVISOR_TARGET9720',control_targets=26,actual_kernel_comparisons=132,exact_target=9720,retained_normal_kernels=6,exact_target_kernels=1,intersection_failures=12,native_pages=3,marked_damages=2)
    for k,v in expected.items():need(f[k]==v,k)
    need(len(f['input_guards'])==len(f['literal_damages'])==4 and f['necessary_ancestor_control']==[1,0],'controls')
    z=read(P/'independent_report.json')
    need(z['status']=='PASS_INDEPENDENT_LITERAL_9720_OBSTRUCTION' and not z['author_helpers_imported'] and z['normal_quotient_searches']==0 and len(z['results'])==2,'independent scope')
    for row in z['inputs']:exact(row)
    for row in z['results']:
        need(row['order']==9720 and row['degree']==27 and row['local_orders']==[120]*4,'literal group')
        need(len(row['intersection_failures'])==12 and row['common_maximal_intersection_order']==2 and row['all_four_words_equal'],'literal obstruction')
    need(r['whole_original_credit']==0 and r['measurement'] is None,'scope')
    a.out.mkdir();report=dict(status='PASS_DISTINCT_L033_DIVISOR_REVIEW_BINDINGS',exports=len(m['exports']),dependencies=len(d),additional_scientific_replay=False,whole_original_credit=0)
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
