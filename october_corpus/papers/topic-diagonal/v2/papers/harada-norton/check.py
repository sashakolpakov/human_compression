#!/usr/bin/env python3
"""Deterministic HN certificate; Atlas inputs are external and hash-bound."""
from pathlib import Path
import argparse, array, hashlib, json, shutil, struct, subprocess, sys, time
ROOT=Path(__file__).resolve().parent
EXTERNAL={
 'HNd2G1-p1140000B0.b1':'de2503113c6082192c71a2f71c678b13f2c913a489659764c45a98271de39f88',
 'HNd2G1-p1140000B0.b2':'d6585c3591a7168ff7cc9126efcf423b5cf0209b81b66fe2d48fbd1db905e7b2'}
MARKER='HN_COMPLETE_EXACT_WITNESS PASS 98properIP 6flag_equalities retained_named_group_and_maximal_classification'
def need(b,s):
    if not b: raise RuntimeError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def decode(raw,n):
    need(len(raw)==12+8*n,'binary length')
    need(struct.unpack('<iii',raw[:12])==(-1,n,1),'binary header')
    a=array.array('Q');a.frombytes(raw[12:])
    if sys.byteorder!='little':a.byteswap()
    need(len(a)==n and min(a)==1 and max(a)==n and len(set(a))==n,'complete permutation bijection')
    return a
def invoke(gap,stage,script,log,marker,timeout):
    p=subprocess.run([gap,'-q','-T','-m','256m','-o','4g',str(script)],cwd=stage,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
    log.write_bytes(p.stdout);s=p.stdout.decode(errors='replace').replace('\\\n','')
    need(p.returncode==0 and 'Error,' not in s and 'Syntax error:' not in s and marker in s,'GAP rejected or omitted certificate: '+log.name)
    return {'log':log.name,'sha256':sha(log),'marker':marker,'returncode':p.returncode}
def controls(gap,stage,out):
    result=[]
    for name,raw in [('bad_header',struct.pack('<iii',0,2,1)+struct.pack('<QQ',1,2)),('duplicate_image',struct.pack('<iii',-1,2,1)+struct.pack('<QQ',1,1)),('truncated_image',struct.pack('<iii',-1,2,1)+struct.pack('<Q',1))]:
        try:decode(raw,2)
        except RuntimeError:result.append({'name':name,'rejected':True})
        else:raise RuntimeError('bad binary accepted: '+name)
    # This elementary arithmetic is only the exclusion step after a retained
    # complete maximal list and an identified outer generator have been supplied.
    def gen_condition(outer,eleven,nineteen,orders):
        return outer and eleven and nineteen and all(m%209 for m in orders)
    orders=[479001600,354816000,33094656,7372800,5040000,4000000,3317760,2073600,2064384,1500000,186624,116640]
    need(gen_condition(True,True,True,orders),'generation arithmetic positive control')
    for name,flags,os in [('no_outer',(False,True,True),orders),('no_eleven',(True,False,True),orders),('no_nineteen',(True,True,False),orders),('unexcluded_maximal',(True,True,True),orders+[209])]:
        need(not gen_condition(*flags,os),'bad generation interface accepted');result.append({'name':name,'rejected':True})
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
    for f,h in EXTERNAL.items():
        p=a.atlas_root/f;need(sha(p)==h,'external Atlas hash mismatch: '+f);inputs[f]={'sha256':h,'bytes':p.stat().st_size}
    for i,f in enumerate(EXTERNAL,1):
        vals=decode((a.atlas_root/f).read_bytes(),1140000)
        q=stage/f'HN_standard_{i}.g';q.write_text(f'HNStandard{i}:=PermList(['+','.join(map(str,vals))+']);;\n')
        inputs[f]['decoded_sha256']=sha(q)
    for rel in ['programs/local_geometry.g','programs/verify_hn.g','witnesses/HN_compact.g']:
        p=stage/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/rel,p)
    report={'status':'PASS','complete_HN_case':True,'named_group_and_maximal_classification_retained':True,'full_group_order_enumerated':False,'lean_verified':False,'external_inputs':inputs,'retained_catalogue_bindings':catalogues,'checker_sha256':sha(ROOT/'check.py')}
    report['finite_replay']=invoke(a.gap,stage,stage/'programs/verify_hn.g',out/'hn.log',MARKER,a.timeout)
    report['controls']=controls(a.gap,stage,out)
    report['actual_software_query']=subprocess.check_output([a.gap,'-q','-c','Print(GAPInfo.Version,"\\n");QUIT;'],text=True).strip()
    report['seconds']=time.time()-start
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','complete_HN_case':True,'seconds':report['seconds']}))
if __name__=='__main__':
    try:main()
    except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
