#!/usr/bin/env python3
"""Portable fresh controls for a uniform, written class-count proof."""
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
from fractions import Fraction
from lower_bounds import need,linear_bound,symplectic_bound,odd_orthogonal_bound,even_orthogonal_bound

BASE=Path(__file__).resolve().parent

def pin(path):
    b=path.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def save(path,value):
    path.write_text(json.dumps(value,indent=2)+'\n')

def check_pin(path,item):
    need(pin(path)=={k:item[k] for k in ('bytes','sha256')},'changed input '+str(path))

def run(command,path,limit=60):
    path.mkdir();env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
    start=time.monotonic()
    with (path/'stdout').open('wb') as so,(path/'stderr').open('wb') as se:
        try:
            p=subprocess.run(list(map(str,command)),cwd=path,stdout=so,stderr=se,timeout=limit,env=env)
        except subprocess.TimeoutExpired:
            save(path/'receipt.json',{'status':'TIMEOUT_NO_CERTIFICATE','command':list(map(str,command)),'seconds':time.monotonic()-start});raise
    r={'status':'TERMINAL_PASS' if p.returncode==0 else 'FAILED','command':list(map(str,command)),'returncode':p.returncode,'seconds':time.monotonic()-start,'stdout':pin(path/'stdout'),'stderr':pin(path/'stderr')}
    save(path/'receipt.json',r)
    need(p.returncode==0 and not (path/'stderr').read_text().strip(),'clean execution '+str(path))
    return (path/'stdout').read_text()

def table_check(text):
    rows={}
    for line in text.strip().splitlines():
        if line.startswith('TABLE '):
            m=re.fullmatch(r'TABLE (\S+) (\d+) (\d+)',line)
            need(m is not None,'malformed table row')
            name,order,count=m.groups();need(name not in rows,'duplicate table row')
            rows[name]=[int(order),int(count)]
    expected=json.loads((BASE/'table_expected.json').read_text())
    need(rows==expected,'exact ordinary-table identities and counts')
    need(text.strip().endswith('PASS_CLASSICAL_LOWER_ORDINARY_TABLE_CONTROLS'),'table completion')
    need('Error' not in text and 'warning' not in text.lower(),'clean table stdout')
    actual_lowers={
      'L4(2)':linear_bound(4,2,False)[0], 'L4(3)':linear_bound(4,3,False)[0],
      'U4(2)':linear_bound(4,2,True)[0], 'U4(3)':linear_bound(4,3,True)[0],
      'S4(3)':symplectic_bound(2,3),'S6(2)':symplectic_bound(3,2),
      'O7(3)':odd_orthogonal_bound(3,3),
      'O8+(2)':even_orthogonal_bound(4,2,1),'O8-(2)':even_orthogonal_bound(4,2,-1)}
    for name,lower in actual_lowers.items():
        need(lower<=rows[name][1],'explicit class count exceeds actual group count')
    need(rows['U4(3)'][1]<Fraction(3**8,2),'source correction not detected')
    return rows

def validate_reports(arithmetic,literal):
    need(arithmetic==json.loads((BASE/'arithmetic_expected.json').read_text()),'complete rational arithmetic report')
    need(literal==json.loads((BASE/'literal_expected.json').read_text()),'complete independent literal report')

def main():
    p=argparse.ArgumentParser();p.add_argument('--study',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--gap',type=Path,default=Path(shutil.which('gap') or '/missing/gap'));p.add_argument('--gap-root',type=Path);p.add_argument('--render',action='store_true')
    a=p.parse_args();need(a.out.is_absolute() and not a.out.exists(),'fresh absolute output')
    m=json.loads((BASE/'manifest.json').read_text())
    for item in m['exports']:check_pin(BASE/item['path'],item)
    deps=json.loads((BASE/'dependencies.json').read_text())['files'];roots={'study':a.study.resolve(),'gap':(a.gap_root or a.gap.resolve().parent.parent).resolve()}
    for item in deps:check_pin(roots[item['namespace']]/item['path'],item)
    a.out.mkdir(parents=True)
    run([sys.executable,BASE/'lower_bounds.py','--out',a.out/'arithmetic.json'],a.out/'arithmetic_execution')
    run([sys.executable,BASE/'small_controls.py','--out',a.out/'literal.json'],a.out/'literal_execution')
    arithmetic=json.loads((a.out/'arithmetic.json').read_text());literal=json.loads((a.out/'literal.json').read_text());validate_reports(arithmetic,literal)
    txt=run([a.gap,'-q','-b',BASE/'table_controls.g'],a.out/'table_execution');tables=table_check(txt)
    damaged=[]
    for kind in ('class_count','missing_class','quadratic_sign','source_half','missing_table','missing_terminal'):
        ar=copy.deepcopy(arithmetic);li=copy.deepcopy(literal);text=txt
        if kind=='class_count':ar['rows'][0]['lower_numerator']+=1
        elif kind=='missing_class':ar['rows'].pop()
        elif kind=='quadratic_sign':li['quadratic_rows'][0]['fixed_forms']['1']+=1
        elif kind=='source_half':text=text.replace('U4(3) 3265920 2835','U4(3) 3265920 3281')
        elif kind=='missing_table':text='\n'.join(line for line in text.splitlines() if not line.startswith('TABLE U4(3)'))
        else:text=text.replace('PASS_CLASSICAL_LOWER_ORDINARY_TABLE_CONTROLS','')
        try:validate_reports(ar,li);table_check(text)
        except ValueError as e:damaged.append({'control':kind,'rejected':True,'message':str(e)})
        else:raise ValueError('damaged certificate passed '+kind)
    save(a.out/'damaged_controls.json',damaged)
    guards=[]
    for script in ('check.py','lower_bounds.py','small_controls.py'):
        for mode in ('argument','environment'):
            dest=a.out/(script+'_'+mode);env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);cmd=[sys.executable]
            if mode=='argument':cmd.append('-O')
            else:env['PYTHONOPTIMIZE']='1'
            cmd += [str(BASE/script),'--out',str(dest)]
            p0=subprocess.run(cmd,capture_output=True,env=env,timeout=15)
            need(p0.returncode!=0 and b'optimized execution is not accepted' in p0.stderr and not dest.exists(),'pre-output optimization guard')
            guards.append({'script':script,'mode':mode,'rejected':True,'no_output':True})
    save(a.out/'optimization_controls.json',guards)
    native=None
    if a.render:
        n=a.out/'native';n.mkdir();shutil.copy2(BASE/'lower_bounds.tex',n/'lower_bounds.tex')
        for i in range(2):run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(n),n/'lower_bounds.tex'],n/('pass'+str(i)))
        log=(n/'lower_bounds.log').read_text();need('Overfull' not in log and 'LaTeX Warning' not in log,'native layout/reference guard')
        from pypdf import PdfReader
        pdf=PdfReader(n/'lower_bounds.pdf');text='\n'.join(page.extract_text() or '' for page in pdf.pages)
        need(text==(BASE/'native_text.txt').read_text(),'exact native mathematical text')
        run(['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile='+str(n/'page-%02d.png'),n/'lower_bounds.pdf'],n/'render')
        native={'pages':len(pdf.pages),'text_matches':True,'underfull':'Underfull' in log}
    report={'status':'PASS_CLASSICAL_LOWER_COMPONENT','exports':len(m['exports']),'bindings':len(deps),'arithmetic_cases':arithmetic['number_of_rows'],'literal_queries':literal['literal_queries'],'ordinary_tables':len(tables),'damaged_controls':len(damaged),'optimization_guards':len(guards),'native':native,'whole_original_credit':0,'existence_bound_still_pending':True}
    save(a.out/'report.json',report);print(json.dumps(report))

if __name__=='__main__':main()
