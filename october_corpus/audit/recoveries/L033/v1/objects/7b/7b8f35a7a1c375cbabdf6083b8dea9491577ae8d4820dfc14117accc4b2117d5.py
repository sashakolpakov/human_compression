import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,hashlib,json
P=Path(__file__).resolve().parent
STATUS='ACCEPTED_L033_CUBIC_EXAMPLE_COMPONENT_V1'
def read(p):return json.loads(Path(p).read_text())
def need(v,m):
    if not v:raise ValueError(m)
def exact(r,p=None):
    b=Path(p or r['path']).read_bytes();need(len(b)==r['bytes']and hashlib.sha256(b).hexdigest()==r['sha256'],'exact input')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(a.out.is_absolute()and not a.out.exists(),'fresh output')
    m=read(P/'manifest.json');d=read(P/'dependencies.json');r=read(P/'review.json');need(m['status']==r['status']==STATUS,'decision')
    for row in m['exports']:
        q=Path(row['path']);need(not q.is_absolute()and '..'not in q.parts,'safe export');exact(row,P/q)
    for row in d:exact(row)
    need(len({x['path']for x in d})==len(d),'unique bindings');exact(r['author_manifest']);need(r['author_manifest']['sha256']=='c9faad77d2093ee331b3d400ceaea5974af579bf52b6aadc6397f9aac626ce46','author')
    c=read(P/'fresh_receipt.json');need(c['status']=='CLEAN_FINITE_RETURN'and c['returncode']==0 and c['inputs_unchanged']and c['stderr_empty']and not c['deadline']and not c['target_census'],'clean replay')
    for row in c['outputs']:exact(row)
    f=read(P/'fresh_report.json');need(f['status']=='PASS'and f['signed_chambers']==48 and f['adjacent_chamber_checks']==16 and f['native_pages']==2,'fresh finite/native')
    z=read(P/'independent_report.json');need(z['status']=='PASS_INDEPENDENT_CUBIC_DUAL_AND_RESIDUES'and z['cross_type_incidence_pairs']==5285 and z['rank3_residue_sizes']==[26,26,6,14]and not z['author_helpers_imported'],'independent source-cell check')
    for row in z['inputs']:exact(row)
    need([x['vertices']for x in z['rank2_residues']]==[4,6,4,6,4,8],'all rank2 residues')
    a.out.mkdir();v=dict(status='PASS_DISTINCT_L033_CUBIC_EXAMPLE_REVIEW_BINDINGS',exports=len(m['exports']),dependencies=len(d),target_censuses=0,whole_original_credit=0);(a.out/'report.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps(v))
if __name__=='__main__':main()
