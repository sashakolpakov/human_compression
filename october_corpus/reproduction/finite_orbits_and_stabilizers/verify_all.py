"""Serial metadata orchestration: eight separately guarded arithmetic processes."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys
ROOT=Path(__file__).resolve().parent
def need(x,s):
    if not x:raise ValueError(s)
def read(name,cap):
    p=ROOT/name;need(not p.is_symlink()and p.resolve(strict=True).is_relative_to(ROOT)and p.stat().st_size<=cap,'bounded relative metadata');return p.read_bytes()
def main():
    ap=argparse.ArgumentParser(allow_abbrev=False);ap.add_argument('--output',required=True);ap.add_argument('--volume',default=str(ROOT));ap.add_argument('--python',default=sys.executable);ap.add_argument('--role');a=ap.parse_args()
    need(sys.flags.ignore_environment and sys.flags.no_site and sys.dont_write_bytecode,'EBS metadata orchestration')
    index=json.loads(read('CASES.json',65536));need(index['schema']=='F004_SEVEN_PORTABLE_FINITE_ORBITS_V1'and index['positions']==[109,349,400,502,877,1033,1099]and len(index['cases'])==7 and [r['position']for r in index['cases']]==index['positions']and all(type(r['position'])is int for r in index['cases']),'exact ordered seven exported cases')
    out=Path(a.output);need(out.is_absolute()and not os.path.lexists(out)and out.parent.resolve(strict=True)==out.parent,'fresh output root');out.mkdir();(out/'guards').mkdir();(out/'results').mkdir()
    roles=[('controls','CONTROL_SOURCE_MANIFEST.json',None)]+[(str(r['position']),'SOURCE_MANIFEST.json',r)for r in index['cases']]
    if a.role:roles=[r for r in roles if r[0]==a.role];need(len(roles)==1,'one known role')
    reports=[]
    for name,mf,case in roles:
        manifest=read(mf,65536);script=ROOT/('controls.py'if name=='controls'else'verify.py');cmd=[a.python,'-E','-B','-S',str(script),'--manifest',str(ROOT/mf),hashlib.sha256(manifest).hexdigest(),'--output',str(out/'results'/name)]
        if case:
            namepath=Path(case['file']['path']);need(not namepath.is_absolute()and '..'not in namepath.parts,'relative indexed case');cmd+=['--case',str(ROOT/namepath),case['file']['sha256']]
        supervisor=ROOT.parent/'fixed_line_orbits/runtime/supervise_validation.py';argv=[a.python,'-E','-B',str(supervisor),'--volume',a.volume,'--output',str(out/'guards'/name),'--rss-cap-mib','128','--timeout','100','--']+cmd
        r=subprocess.run(argv,capture_output=True);(out/(name+'.stdout')).write_bytes(r.stdout);(out/(name+'.stderr')).write_bytes(r.stderr)
        need(r.returncode==0,'guarded role failed; earlier roles remain in this output directory')
        result_path=out/'results'/name/'result.json';need(result_path.stat().st_size<=131072,'bounded scalar result');facts=json.loads(result_path.read_bytes())
        if case:need(facts['position']==case['position']and facts['original_job']==[20,4]and facts['status']=='VERIFIED_FINITE_ORBIT_AND_SMALL_STABILIZER_MATRIX_FACTS','returned case subject equals indexed role')
        else:need(facts['status']=='PASS'and facts['arithmetic_count']==33 and facts['portable_count']==8,'all control counts')
        reports.append(dict(role=name,returncode=r.returncode,guard='guards/'+name,result='results/'+name))
    body=json.dumps(dict(schema='F004_PORTABLE_FINITE_ORBITS_SERIAL_REPLAY_V1',all_requested_roles_passed=True,roles=reports,independent_arithmetic_processes=len(reports),canonical_or_case_credit=0),sort_keys=True,separators=(',',':'))+'\n';(out/'replay.json').write_text(body);print(body,end='')
if __name__=='__main__':main()
