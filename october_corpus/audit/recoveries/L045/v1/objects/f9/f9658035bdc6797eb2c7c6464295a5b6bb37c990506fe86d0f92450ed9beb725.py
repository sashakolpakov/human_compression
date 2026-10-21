#!/usr/bin/env python3
"""Fresh bounded controls for the written linear/unitary existence proof."""
import sys
if sys.flags.optimize:
    raise RuntimeError('optimized execution is not accepted')
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time

BASE=Path(__file__).resolve().parent

def need(test,message):
    if not test:raise ValueError(message)

def pin(path):
    data=path.read_bytes()
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

def check_pin(path,item):
    need(pin(path)=={k:item[k] for k in ('bytes','sha256')},'changed exact input '+str(path))

def save(path,obj):path.write_text(json.dumps(obj,indent=2)+'\n')

def run(command,directory,limit=90):
    directory.mkdir()
    env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
    command=list(map(str,command));start=time.monotonic()
    with (directory/'stdout').open('wb') as so,(directory/'stderr').open('wb') as se:
        try:p=subprocess.run(command,cwd=directory,stdout=so,stderr=se,timeout=limit,env=env)
        except subprocess.TimeoutExpired:
            save(directory/'receipt.json',{'status':'TIMEOUT_NO_CERTIFICATE','command':command,'seconds':time.monotonic()-start,'stdout':pin(directory/'stdout'),'stderr':pin(directory/'stderr')})
            raise
    receipt={'status':'TERMINAL_PASS' if p.returncode==0 else 'FAILED','returncode':p.returncode,'command':command,'seconds':time.monotonic()-start,'stdout':pin(directory/'stdout'),'stderr':pin(directory/'stderr')}
    save(directory/'receipt.json',receipt)
    need(p.returncode==0 and not (directory/'stderr').read_text().strip(),'clean terminal execution '+str(directory))
    return (directory/'stdout').read_text()

def validate(arithmetic,literal):
    need(arithmetic==json.loads((BASE/'arithmetic_expected.json').read_text()),'complete exact arithmetic report')
    expected=(BASE/'literal_expected.stdout').read_text()
    # GAP's formatting can change line breaks, but no mathematical token.
    need(re.sub(r'\s+','',literal)==re.sub(r'\s+','',expected),'complete exact literal transcript')
    need('Error' not in literal and 'warning' not in literal.lower(),'clean GAP mathematical execution')
    need(literal.strip().endswith('] ]'),'complete final literal record')
    need('PASS_TRACE_FORMS 7 813' in literal,'trace controls completion')
    need('PASS_J_ISOMETRIES' in literal,'isometry controls completion')

def main():
    p=argparse.ArgumentParser();p.add_argument('--study',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true')
    p.add_argument('--gap',type=Path,default=Path(shutil.which('gap') or '/missing/gap'))
    p.add_argument('--gap-root',type=Path)
    p.add_argument('--repo',type=Path)
    a=p.parse_args();need(a.out.is_absolute() and not a.out.exists(),'fresh absolute output required')
    manifest=json.loads((BASE/'manifest.json').read_text())
    for item in manifest['exports']:check_pin(BASE/item['path'],item)
    deps=json.loads((BASE/'dependencies.json').read_text())['files']
    roots={'study':a.study.resolve(),'gap':(a.gap_root or a.gap.resolve().parent.parent).resolve(),'public':(a.repo or a.study.resolve().parent.parent/'math_compression').resolve()}
    for item in deps:check_pin(roots[item['namespace']]/item['path'],item)
    a.out.mkdir(parents=True)
    run([sys.executable,BASE/'linear_bounds.py','--out',a.out/'arithmetic.json'],a.out/'arithmetic_execution')
    arithmetic=json.loads((a.out/'arithmetic.json').read_text())
    literal=run([a.gap,'-q','-b',BASE/'linear_upper_controls.g'],a.out/'literal_execution')
    validate(arithmetic,literal)
    negatives=[]
    for kind in ('changed_count','missing_rank','changed_family','missing_finite_route','changed_trace_count','changed_isometry_count','missing_completion','gap_error'):
        ar=copy.deepcopy(arithmetic);li=literal
        if kind=='changed_count':ar['rows'][0]['upper']='0'
        elif kind=='missing_rank':ar['rows'].pop()
        elif kind=='changed_family':ar['rows'][0]['family']='Sp'
        elif kind=='missing_finite_route':ar['separately_acquired_finite_routes'].pop()
        elif kind=='changed_trace_count':li=li.replace('7 813','7 812')
        elif kind=='changed_isometry_count':li=li.replace('23040','23041')
        elif kind=='missing_completion':li=li.replace('PASS_J_ISOMETRIES','')
        else:li+='\nError, test failure despite process exit zero\n'
        try:validate(ar,li)
        except ValueError as e:negatives.append({'case':kind,'rejected':True,'message':str(e)})
        else:raise ValueError('damaged mathematical record passed '+kind)
    save(a.out/'negative_controls.json',negatives)
    guards=[]
    for script in ('check.py','linear_bounds.py','lower_bounds.py'):
        for mode in ('argument','environment'):
            dest=a.out/(script+'_'+mode);env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
            cmd=[sys.executable]
            if mode=='argument':cmd.append('-O')
            else:env['PYTHONOPTIMIZE']='1'
            cmd += [str(BASE/script),'--out',str(dest)]
            z=subprocess.run(cmd,capture_output=True,env=env,timeout=15)
            need(z.returncode!=0 and b'optimized execution is not accepted' in z.stderr and not dest.exists(),'pre-output optimization rejection')
            guards.append({'script':script,'mode':mode,'rejected':True,'no_output':True})
    save(a.out/'optimization_controls.json',guards)
    native=None
    if a.render:
        n=a.out/'native';n.mkdir();shutil.copy2(BASE/'linear_upper.tex',n/'linear_upper.tex')
        for i in range(2):run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(n),n/'linear_upper.tex'],n/('build'+str(i)))
        log=(n/'linear_upper.log').read_text()
        need('Overfull' not in log and 'LaTeX Warning' not in log,'native reference/layout check')
        from pypdf import PdfReader
        pages=PdfReader(n/'linear_upper.pdf').pages
        text='\n'.join(page.extract_text() or '' for page in pages)
        need(text==(BASE/'native_text.txt').read_text(),'exact rebuilt native text')
        run(['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile='+str(n/'page-%02d.png'),n/'linear_upper.pdf'],n/'render')
        native={'pages':len(pages),'exact_text':True,'underfull':'Underfull' in log}
    report={'status':'PASS_LINEAR_UNITARY_UPPER_COMPONENT','exports':len(manifest['exports']),'bindings':len(deps),'arithmetic_rows':arithmetic['number_of_rows'],'acquired_finite_routes':len(arithmetic['separately_acquired_finite_routes']),'trace_models':7,'trace_forms':813,'literal_isometry_models':3,'damaged_controls':len(negatives),'optimization_guards':len(guards),'native':native,'new_census':False,'whole_original_credit':0,'symplectic_or_orthogonal_credit':0}
    save(a.out/'report.json',report);print(json.dumps(report))

if __name__=='__main__':main()
