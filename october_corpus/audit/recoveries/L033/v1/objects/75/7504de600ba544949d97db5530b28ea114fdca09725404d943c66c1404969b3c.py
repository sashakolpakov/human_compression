import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,hashlib,json
P=Path(__file__).resolve().parent
STATUS='ACCEPTED_L033_COMPLETE_SQUARE3535_THROUGH3840'
AUTHOR='d6d218b2ac2297fd0c53f4976c64e5e2e361e503d44e12baa253635bb39369f0'
def read(p):return json.loads(Path(p).read_text())
def need(v,m):
    if not v:raise ValueError(m)
def exact(r,p=None):
    b=Path(p or r['path']).read_bytes();need(len(b)==r['bytes']and hashlib.sha256(b).hexdigest()==r['sha256'],'exact '+str(p or r['path']))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(a.out.is_absolute()and not a.out.exists(),'fresh output')
    m=read(P/'manifest.json');d=read(P/'dependencies.json');r=read(P/'review.json');need(m['status']==r['status']==STATUS,'decision')
    for row in m['exports']:
        q=Path(row['path']);need(not q.is_absolute()and '..'not in q.parts,'safe export');exact(row,P/q)
    for row in d:exact(row)
    need(len({x['path']for x in d})==len(d),'unique deps');exact(r['author_manifest']);need(r['author_manifest']['sha256']==AUTHOR,'author')
    c=read(P/'fresh_receipt.json');need(c['status']=='CLEAN_FINITE_RETURN'and c['returncode']==0 and not c['deadline']and c['inputs_unchanged']and c['stderr_empty']and c['target_census'],'clean exact finite target')
    for row in c['outputs']:exact(row)
    f=read(P/'fresh_report.json')
    for k,v in dict(status='PASS_COMPLETE_SQUARE3535_THROUGH3840',all_indices_through=3840,normal_kernels=25,marked_quotients=23,positive=1,intersection_rejections=21,incidence_rejections=1,broad_minimum=1920,excluded_exact_order3840=11,native_pages=2).items():need(f[k]==v,k)
    z=read(P/'independent_report.json');need(z['status']=='PASS_INDEPENDENT_COMPLETE_SQUARE_MARKINGS'and len(z['rows'])==23 and not z['author_helpers_imported']and z['normal_quotient_searches']==0,'independent finite check')
    for row in z['inputs']:exact(row)
    p=z['positive'];need(p['order']==1920 and p['local_orders']==[60]*4 and p['actual_flags']['actual_chambers']==p['actual_flags']['chamber_orbit']==1920 and p['actual_flags']['first_nonorbit_flag']is None,'positive flag complex')
    need(z['incidence_only_failure']['order']==960 and z['incidence_only_failure']['actual_flags']['first_nonorbit_flag']is not None,'incidence obstruction')
    w=read(P/'printed_witness.json');need(w['status']=='PASS_PRINTED_WITNESS_ORDERED_ISOMORPHISM'and w['order']==1920 and w['generator_edges']==7680,'printed marking')
    for row in w['inputs']:exact(row)
    a.out.mkdir();v=dict(status='PASS_DISTINCT_L033_SMALL_SQUARE_REVIEW_BINDINGS',exports=len(m['exports']),dependencies=len(d),additional_scientific_replay=False,whole_original_credit=0);(a.out/'report.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps(v))
if __name__=='__main__':main()
