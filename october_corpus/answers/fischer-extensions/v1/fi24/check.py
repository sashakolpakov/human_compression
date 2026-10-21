#!/usr/bin/env python3
"""Deterministic Fi24prime:2 certificate; external Atlas inputs are hash-bound."""
from pathlib import Path
import argparse, hashlib, json, re, shutil, subprocess, sys, time
ROOT=Path(__file__).resolve().parent
EXTERNAL={
 'F24d2G1-p306936B0.g1':('f218e592111b9ae5e5f2547bb3884de8adbb098924d7b395339c279b093ba1e9','b11'),
 'F24d2G1-p306936B0.g2':('0a8bfb3c98b82d19454d05db0d595131629f1dffadfe574cde20d17e25509e9e','b21')}
MARKER='F24_COMPLETE_EXACT_WITNESS PASS 98properIP 6flag_equalities retained_named_group_and_maximal_classification'
def need(b,s):
    if not b: raise RuntimeError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def literal_permutation(raw,assignment,n):
    s=raw.decode('ascii')
    m=re.fullmatch(r'\s*'+re.escape(assignment)+r'\s*:=\s*((?:\(\s*[0-9]+(?:\s*,\s*[0-9]+)+\s*\)\s*)+);\s*',s)
    need(m is not None,'input is not exactly one literal permutation assignment')
    images=[int(v) for v in re.findall(r'[0-9]+',m.group(1))]
    need(images and min(images)>=1 and max(images)<=n and len(images)==len(set(images)),
         'cycle labels must be distinct and in degree range')
    return {'assignment':assignment,'moved_points':len(images),'largest_label':max(images),'literal_assignment_only':True,'all_cycles_disjoint':True}
def invoke(gap,stage,script,log,marker,timeout):
    p=subprocess.run([gap,'-q','-T','-m','256m','-o','4g',str(script)],cwd=stage,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
    log.write_bytes(p.stdout);s=p.stdout.decode(errors='replace').replace('\\\n','')
    need(p.returncode==0 and 'Error,' not in s and 'Syntax error:' not in s and marker in s,'GAP rejected or omitted certificate: '+log.name)
    return {'log':log.name,'sha256':sha(log),'marker':marker,'returncode':p.returncode}
def controls(gap,stage,out):
    result=[]
    literal_permutation(b'b11:=(1,2)(3,4);','b11',4)
    for name,raw in [
      ('wrong_assignment',b'b21:=(1,2);'),
      ('duplicate_cycle_label',b'b11:=(1,2)(2,3);'),
      ('out_of_range_label',b'b11:=(1,5);'),
      ('extra_executable_statement',b'b11:=(1,2);QUIT;'),
      ('nonliteral_expression',b'b11:=Random(SymmetricGroup(4));')]:
        try:literal_permutation(raw,'b11',4)
        except RuntimeError:result.append({'name':name,'rejected':True})
        else:raise RuntimeError('invalid input accepted: '+name)
    # This elementary arithmetic is only the exclusion step after a retained
    # complete maximal list and an identified outer generator have been supplied.
    def gen_condition(outer,prime23,prime29,orders):
        return outer and prime23 and prime29 and all(m%667 for m in orders)
    orders=[r['order'] for r in json.loads((ROOT/'retained_inputs.json').read_text())['complete_maximal_subgroups'][1:]]
    need(gen_condition(True,True,True,orders),'generation arithmetic positive control')
    for name,flags,os in [('no_outer',(False,True,True),orders),('no_order23',(True,False,True),orders),('no_order29',(True,True,False),orders),('unexcluded_maximal',(True,True,True),orders+[667])]:
        need(not gen_condition(*flags,os),'bad generation interface accepted');result.append({'name':name,'rejected':True})
    # Change actual saved witness data, then replay the fixed verifier until
    # its first violated mathematical equality; do not substitute a mock test.
    witness=stage/'witnesses/F24_compact.g'; original=witness.read_bytes()
    for name,change in [('wrong_prime23_exponent','F24Prime23[2]:=1;'),('identity_endpoint','F24bPower:=0;')]:
        try:
            witness.write_bytes(original+b'\n'+change.encode()+b'\n')
            try:invoke(gap,stage,stage/'programs/verify.g',out/(name+'.log'),MARKER,120)
            except RuntimeError:
                text=(out/(name+'.log')).read_text()
                expected='exact order23 witness' if name=='wrong_prime23_exponent' else 'string product orders'
                need('Error, '+expected in text,'mutation did not reach expected mathematical guard')
                result.append({'name':name,'rejected':True,'expected_failure':expected})
            else:raise RuntimeError('altered actual witness accepted: '+name)
        finally:witness.write_bytes(original)
    cases={
     'coincident_marks':'ProperIP([(1,2),(1,2),(2,3)]);;',
     'ip_failure':'ProperIP([(1,2)(3,4),(1,3)(2,5),(1,5)(2,4)]);;',
     'ip_without_flags':'r:=[(2,3)(4,5),(1,2)(4,5),(1,3)(2,4)];;Need(ProperIP(r)=49,"positive IP");;Print("IP_POSITIVE\\n");;FlagStreaming(r);;',
     'incorrect_halving_power':'a:=(2,5)(3,4);;b:=(1,2)(3,5);;Need(Order(a*b)=5,"D10 fixture");;Need(b=(a*a^b)*a,"wrong halving exponent");;'
    }
    for name,body in cases.items():
        pth=stage/(name+'.g');pth.write_text('Read("programs/local_geometry.g");;\n'+body+'\nPrint("BAD_ACCEPT\\n");;QUIT;\n')
        p=subprocess.run([gap,'-q','-T',str(pth)],cwd=stage,capture_output=True,timeout=90)
        s=(p.stdout+p.stderr).decode(errors='replace');(out/(name+'.log')).write_text(s)
        need('Error,' in s and 'BAD_ACCEPT' not in s,'bad finite model accepted: '+name)
        if name=='ip_without_flags':need('IP_POSITIVE' in s,'FT countermodel did not first pass IP')
        result.append({'name':name,'rejected':True})
    try:invoke(gap,stage,stage/'coincident_marks.g',out/'parser_control.log','BAD_ACCEPT',90)
    except RuntimeError:result.append({'name':'zero_exit_is_not_success','rejected':True})
    else:raise RuntimeError('zero exit parser accepted GAP Error')
    return result
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--atlas-root',type=Path,required=True);ap.add_argument('--gap',default='/opt/homebrew/bin/gap');ap.add_argument('--timeout',type=int,default=1800);a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'output already exists or is a symlink')
    if (ROOT/'manifest.json').exists():
        for row in json.loads((ROOT/'manifest.json').read_text())['exports']:
            need(sha(ROOT/row['path'])==row['sha256'],'frozen export mismatch: '+row['path'])
    out=a.out.resolve();out.mkdir(parents=True);stage=out/'stage';stage.mkdir();start=time.time()
    inputs={}
    query='LoadPackage("ctbllib");Print(Filename(DirectoriesPackageLibrary("ctbllib","")[1],""),"\\n");QUIT;'
    package=Path(subprocess.check_output([a.gap,'-q','-c',query],text=True).strip())
    catalogues=[]
    for row in json.loads((ROOT/'retained_inputs.json').read_text())['installed_catalogue_inputs']:
        p=package/row['relative_package_path']
        need(sha(p)==row['sha256'],'retained CTblLib data mismatch: '+row['relative_package_path'])
        catalogues.append({'path':row['relative_package_path'],'sha256':row['sha256'],'bytes':p.stat().st_size})
    for f,(h,var) in EXTERNAL.items():
        p=a.atlas_root/f;need(sha(p)==h,'external Atlas hash mismatch: '+f)
        inputs[f]={'sha256':h,'bytes':p.stat().st_size,**literal_permutation(p.read_bytes(),var,306936)}
        shutil.copyfile(p,stage/f)
    for rel in ['programs/local_geometry.g','programs/verify.g','witnesses/F24_compact.g']:
        p=stage/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/rel,p)
    report={'status':'PASS','complete_Fi24prime_extension_case':True,'named_group_and_maximal_classification_retained':True,'full_group_order_enumerated':False,'lean_verified':False,'external_inputs':inputs,'retained_catalogue_bindings':catalogues,'checker_sha256':sha(ROOT/'check.py')}
    report['finite_replay']=invoke(a.gap,stage,stage/'programs/verify.g',out/'fi24.log',MARKER,a.timeout)
    report['controls']=controls(a.gap,stage,out)
    report['actual_software_query']=subprocess.check_output([a.gap,'-q','-c','Print(GAPInfo.Version,"\\n");QUIT;'],text=True).strip()
    report['seconds']=time.time()-start
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','complete_Fi24prime_extension_case':True,'seconds':report['seconds']}))
if __name__=='__main__':
    try:main()
    except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
