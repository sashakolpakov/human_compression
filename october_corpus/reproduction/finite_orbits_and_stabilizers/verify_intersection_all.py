"""Serial public replay:24 new word controls,10 admission tests,one case."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parent
def need(v,s):
    if not v:raise ValueError(s)
def read(name,cap):
    p=ROOT/name;need(not p.is_symlink()and p.resolve(strict=True).is_relative_to(ROOT)and p.stat().st_size<=cap,'bounded relative metadata');return p.read_bytes()
def main():
    ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--output',required=True);ap.add_argument('--python',default=sys.executable);ap.add_argument('--volume',default=str(ROOT));ap.add_argument('--role');a=ap.parse_args()
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode and not sys.flags.optimize,'EBS metadata replay')
    index=json.loads(read('INTERSECTION_CASES.json',65536));rows=index['cases']
    need(index['schema']=='F004_ONE_TWO_END_WORD_CERTIFICATE_INDEX_V1'and index['positions']==[1099]and len(rows)==1 and rows[0]['position']==1099 and type(rows[0]['position'])is int,'exact one-case index')
    out=Path(a.output);need(out.is_absolute()and not os.path.lexists(out)and out.parent.resolve(strict=True)==out.parent,'fresh output root');out.mkdir();(out/'guards').mkdir();(out/'results').mkdir()
    roles=[('arithmetic','INTERSECTION_CONTROL_SOURCE_MANIFEST.json','intersection_controls.py',None),('admission','INTERSECTION_ADMISSION_SOURCE_MANIFEST.json','intersection_admission.py',None),('1099','INTERSECTION_SOURCE_MANIFEST.json','verify_intersection.py',rows[0])]
    if a.role:roles=[r for r in roles if r[0]==a.role];need(len(roles)==1,'one known role')
    reports=[];env={k:v for k,v in os.environ.items()if k not in('COVERAGE_PROCESS_CONFIG','COVERAGE_CONFIG','COVERAGE_PROCESS_START','OPENSSL_CONF','OPENSSL_MODULES')}
    for name,mf,entry,case in roles:
        manifest=read(mf,65536);cmd=[a.python,'-E','-B','-S',str(ROOT/entry),'--manifest',str(ROOT/mf),hashlib.sha256(manifest).hexdigest(),'--output',str(out/'results'/name)]
        if case:
            rel=Path(case['file']['path']);need(not rel.is_absolute()and '..'not in rel.parts,'relative indexed case');cmd+=['--case',str(ROOT/rel),case['file']['sha256']]
        supervisor=ROOT.parent/'fixed_line_orbits/runtime/supervise_validation.py';argv=[a.python,'-E','-B',str(supervisor),'--volume',a.volume,'--output',str(out/'guards'/name),'--rss-cap-mib','128','--timeout','100','--']+cmd
        done=subprocess.run(argv,env=env,capture_output=True);(out/(name+'.stdout')).write_bytes(done.stdout);(out/(name+'.stderr')).write_bytes(done.stderr)
        need(done.returncode==0,'guard failed; preserve earlier roles and use a fresh output for retry')
        p=out/'results'/name/'result.json';need(p.stat().st_size<=131072,'bounded result');r=json.loads(p.read_bytes())
        if case:need(r['position']==case['position']and r['original_row_id']==case['original_row_id']and r['original_job']==[20,4]and r['status']=='VERIFIED_MATRIX_INTERSECTION_PROPERTY_FAILURE_BY_TWO_END_WORDS'and r['Original_identity_transfer_verified']is False,'same indexed subject and qualified matrix verdict')
        else:need(r['status']=='PASS'and r['arithmetic_count'if name=='arithmetic'else'admission_count']==(24 if name=='arithmetic'else 10)and r['Original_inputs_loaded']is False,'complete new controls')
        reports.append(dict(role=name,guard='guards/'+name,result='results/'+name,returncode=0))
    body=json.dumps(dict(schema='F004_TWO_END_WORDS_SERIAL_REPLAY_V1',all_requested_roles_passed=True,roles=reports,separate_guarded_workers=len(reports),Original_identity_transfer_verified=False,new_case_or_census_credit=0),sort_keys=True,separators=(',',':'))+'\n'
    (out/'intersection_replay.json').write_text(body);print(body,end='')
if __name__=='__main__':main()
