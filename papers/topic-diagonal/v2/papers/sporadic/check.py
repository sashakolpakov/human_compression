#!/usr/bin/env python3
"""Replay explicit sporadic witnesses; no random search is a proof premise."""
from pathlib import Path
import argparse, hashlib, json, shutil, subprocess, sys, time
ROOT=Path(__file__).resolve().parent
PARTS={'eight':('programs/verify_witnesses.g','COMPLETE 8 sporadic full outer extensions'),
       'on':('programs/verify_on.g','COMPLETE ON direct8-11 marking'),
       'outer-orders':('programs/on_outer_orders.g','NO_OUTER_ORDER4 PASS')}
EXTERNAL={'ONd2G1-p245520B0.g1':'6f6c19692a8916ea66890461ce3fc12427b01baa23b0eaaf6a77da99cd2eb3a7',
          'ONd2G1-p245520B0.g2':'0c50acddb7cd7dd0e78b36bf0317e2d71074a715d3699108b18704d987867d22'}
def need(x,msg):
    if not x: raise RuntimeError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run_gap(gap,stage,script,log,marker,timeout):
    p=subprocess.run([gap,'-q','-T','-m','128m','-o','4g',str(script)],cwd=stage,
        stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
    log.write_bytes(p.stdout);text=p.stdout.decode('utf-8',errors='replace').replace('\\\n','')
    need(p.returncode==0 and 'Error,' not in text and 'Syntax error:' not in text and marker in text,
         f'GAP did not prove expected assertion: {log.name}')
    return {'log':log.name,'sha256':sha(log),'exit':p.returncode,'marker':marker}
def controls(gap,stage,out):
    cases={
      'coincident_marks':'CheckTriple("bad",[(1,2),(1,2),(2,3)],6);;',
      'wrong_order':'CheckTriple("bad",[(1,2),(2,3),(3,4)],25);;',
      'ip_failure':'IPCheck([(1,2)(3,4),(1,3)(2,5),(1,5)(2,4)]);;',
      'ip_without_flags':'r:=[(2,3)(4,5),(1,2)(4,5),(1,3)(2,4)];;Need(IPCheck(r)=64,"IP fixture");;Print("IP_FIXTURE_PASS\\n");;FT3Check(r);;',
      'false_outer_reversal':'r:=[(1,2),(2,3),(3,4),(4,5)];;t:=();;Need(ForAll([1..4],i->r[i]^t=r[5-i]),"false duality");;',
    }
    result=[]
    for name,body in cases.items():
        f=stage/(name+'.g');f.write_text('Read("programs/finite_tools.g");;\n'+body+'\nPrint("BAD_ACCEPT\\n");;QUIT;\n')
        p=subprocess.run([gap,'-q','-T',str(f)],cwd=stage,capture_output=True,timeout=90)
        text=(p.stdout+p.stderr).decode(errors='replace');(out/(name+'.log')).write_text(text)
        need('Error,' in text and 'BAD_ACCEPT' not in text,f'negative control accepted: {name}')
        if name=='ip_without_flags':need('IP_FIXTURE_PASS' in text,'flag control did not first pass IP')
        result.append({'name':name,'rejected':True})
    # The success parser must reject even a process that exits zero with GAP Error.
    try:run_gap(gap,stage,stage/'coincident_marks.g',out/'parser_control.log','BAD_ACCEPT',90)
    except RuntimeError:result.append({'name':'zero_exit_is_not_success','rejected':True})
    else:raise RuntimeError('fail-closed parser control failed')
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--gap',default='/opt/homebrew/bin/gap');ap.add_argument('--atlas-root',type=Path);ap.add_argument('--part',action='append',choices=list(PARTS));ap.add_argument('--timeout',type=int,default=3600);ap.add_argument('--skip-controls',action='store_true');args=ap.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(),'output path must not exist')
    if (ROOT/'manifest.json').exists():
        frozen=json.loads((ROOT/'manifest.json').read_text())
        for row in frozen['exports']:
            need(sha(ROOT/row['path'])==row['sha256'],'frozen export mismatch: '+row['path'])
    out=args.out.resolve();out.mkdir(parents=True);stage=out/'stage';stage.mkdir()
    required=['programs/finite_tools.g','programs/verify_witnesses.g','programs/verify_on.g','programs/on_outer_orders.g']
    required += ['witnesses/'+n+'_rank4_witness.g' for n in ['M12','J2','HS','He','Suz','J3']]
    required += ['witnesses/m22_witness.g','witnesses/mcl_witness.g','witnesses/ON_compact.g']
    for rel in required:
        dest=stage/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/rel,dest)
    parts=args.part or list(PARTS);bind={};start=time.time()
    for p in sorted(stage.rglob('*.g')):bind[str(p.relative_to(stage))]=sha(p)
    if 'on' in parts:
        need(args.atlas_root is not None,'--atlas-root is required for ON')
        ext=args.atlas_root.resolve()
        for f,h in EXTERNAL.items():need(sha(ext/f)==h,'external Atlas input hash mismatch: '+f)
    logs={}
    for part in parts:
        f,marker=PARTS[part];driver=stage/(part+'_driver.g');prefix=''
        if part=='on':prefix='ExternalRoot:='+json.dumps(str(ext))+';;\n'
        driver.write_text(prefix+'Read('+json.dumps(f)+');;\n')
        logs[part]=run_gap(args.gap,stage,driver,out/(part+'.log'),marker,args.timeout)
    ctrl=[] if args.skip_controls else controls(args.gap,stage,out)
    report={'status':'PASS','parts':parts,'complete_nine_existence_cases':set(['eight','on'])<=set(parts),'outer_route_obstruction_checked':'outer-orders' in parts,'lean_verified':False,'conditional_named_group_inputs':True,'logs':logs,'controls':ctrl,'source_hashes':bind,'checker_sha256':sha(ROOT/'check.py'),'external_hashes':EXTERNAL if 'on' in parts else {},'seconds':time.time()-start}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['status','parts','complete_nine_existence_cases','seconds']}))
if __name__=='__main__':
    try:main()
    except Exception as e: print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
