#!/usr/bin/env python3
"""Replay the explicit Fi22:2 incidence certificate, without a search."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys,time
ROOT=Path(__file__).resolve().parent
MARKER='EXACT_FI22_PERMUTATION_CERTIFICATE PASS order129123503308800 socle64561751654400 properIP=[ 49, 49 ] flags=[ 464, 768 ]'
def need(b,s):
    if not b:raise RuntimeError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(gap,stage,f,log,marker):
    p=subprocess.run([gap,'-q','-T','-m','128m','-o','4g',str(f)],cwd=stage,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600)
    log.write_bytes(p.stdout);s=p.stdout.decode(errors='replace').replace('\\\n','')
    need(p.returncode==0 and 'Error,' not in s and 'Syntax error:' not in s and marker in s,'certificate rejected or marker omitted: '+log.name)
    return {'path':log.name,'sha256':sha(log),'returncode':p.returncode,'marker':marker}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--gap',default='/opt/homebrew/bin/gap');a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'output exists or is a dangling symlink')
    if (ROOT/'manifest.json').exists():
        for x in json.loads((ROOT/'manifest.json').read_text())['exports']:need(sha(ROOT/x['path'])==x['sha256'],'frozen export mismatch: '+x['path'])
    out=a.out.resolve();out.mkdir(parents=True);stage=out/'stage';stage.mkdir();start=time.time()
    bound=[];pkgs={}
    for x in json.loads((ROOT/'retained_inputs.json').read_text())['installed_inputs']:
        pkg=x['package']
        if pkg not in pkgs:
            query=f'LoadPackage("{pkg}");Print(Filename(DirectoriesPackageLibrary("{pkg}","")[1],""),"\\n");QUIT;'
            pkgs[pkg]=Path(subprocess.check_output([a.gap,'-q','-c',query],text=True).strip())
        p=pkgs[pkg]/x['relative_package_path'];need(sha(p)==x['sha256'],'retained input mismatch: '+str(p));bound.append(x)
    for f in ['programs/local_geometry.g','programs/verify.g','witnesses/Fi22.g']:
        d=stage/f;d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/f,d)
    cert=run(a.gap,stage,stage/'programs/verify.g',out/'finite.log',MARKER)
    cases={
     'coincident_marks':'ProperIP([(1,2),(1,2),(2,3)]);;',
     'ip_failure':'ProperIP([(1,2)(3,4),(1,3)(2,5),(1,5)(2,4)]);;',
     'ip_without_flags':'r:=[(2,3)(4,5),(1,2)(4,5),(1,3)(2,4)];;Need(ProperIP(r)=49,"positive IP");;Print("IP_POSITIVE\\n");;FlagStreaming(r);;',
     'wrong_generated_order':'Need(Size(Group((1,2),(2,3),(3,4)))=25,"wrong full order");;',
     'incorrect_halving_power':'a:=(2,5)(3,4);;b:=(1,2)(3,5);;Need(Order(a*b)=5,"D10 fixture");;Need(b=(a*a^b)*a,"wrong halving exponent");;'
    };controls=[]
    for name,body in cases.items():
        f=stage/(name+'.g');f.write_text('Read("programs/local_geometry.g");;\n'+body+'\nPrint("BAD_ACCEPT\\n");;QUIT;\n')
        p=subprocess.run([a.gap,'-q','-T',str(f)],cwd=stage,capture_output=True,timeout=90)
        s=(p.stdout+p.stderr).decode(errors='replace');(out/(name+'.log')).write_text(s)
        need('Error,' in s and 'BAD_ACCEPT' not in s,'negative control accepted: '+name)
        if name=='ip_without_flags':need('IP_POSITIVE' in s,'flag countermodel lacks positive IP')
        controls.append({'name':name,'rejected':True})
    try:run(a.gap,stage,stage/'coincident_marks.g',out/'parser_control.log','BAD_ACCEPT')
    except RuntimeError:controls.append({'name':'zero_exit_is_not_success','rejected':True})
    else:raise RuntimeError('fail-closed parser failed')
    report={'status':'PASS','exact_generated_group_equality':True,'named_group_identity_retained':True,'maximal_subgroup_list_only_additional_validation':True,'Lean_declarations':0,'priority_claim':False,'finite_replay':cert,'controls':controls,'installed_inputs':bound,'source_bindings':{f:sha(ROOT/f) for f in ['programs/local_geometry.g','programs/verify.g','witnesses/Fi22.g','check.py']},'seconds':time.time()-start}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','seconds':report['seconds']}))
if __name__=='__main__':
    try:main()
    except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
