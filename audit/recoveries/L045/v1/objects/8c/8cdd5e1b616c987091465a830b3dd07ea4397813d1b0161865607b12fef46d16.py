"""Fresh bounded D4 cover controls and complete immutable-input integrity."""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
from arithmetic import need, calculate, validate

def pin(p):
    b=p.read_bytes()
    return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())

def validate_routes(r):
    rows=r['rows']
    need([x['id'] for x in rows] == list(range(1,43)), '42 distinct source table rows')
    need([x['id'] for x in rows if x['route'].startswith('retain_')] == [8,10,15,16], 'exact surviving rows')
    need(rows[6]['route'] == rows[8]['route'] == 'natural_B3_no_line', 'natural B3 exclusion')
    need(rows[35]['route'] == 'unitary_singer_order', 'unitary three-space interface')
    need(rows[10]['route'] == 'novelty' and rows[39]['route'] == 'outside_q_ge4', 'novelty and small parameter')
    need(r['notes_page']==420 and all(x['physical_page']==(418 if x['id']<=14 else 419) for x in rows), 'source page coverage')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--study',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--render',action='store_true')
    a=ap.parse_args()
    P=Path(__file__).resolve().parent
    S=a.study.resolve(); O=a.out.resolve()
    need(not O.exists(), 'fresh output required')
    deps=json.loads((P/'dependencies.json').read_text())
    exports=[]
    for row in deps:
        actual=pin(S/row['path'])
        need(all(actual[k]==row[k] for k in ('bytes','sha256')), 'exact acquired dependency: '+row['path'])
    if (P/'manifest.json').exists():
        exports=json.loads((P/'manifest.json').read_text())['exports']
        for row in exports:
            actual=pin(P/row['path'])
            need(all(actual[k]==row[k] for k in ('bytes','sha256')), 'exact packet export: '+row['path'])
    historic=0
    if (P/'execution_aliases.json').exists():
        aliases=json.loads((P/'execution_aliases.json').read_text())
        for p in sorted((P/'author_replay').glob('*.receipt.json')):
            r=json.loads(p.read_text())
            need(r['exit_code']==0, 'clean retained execution')
            for row in r['inputs']+[r['stdout'],r['stderr']]:
                need(row['path'] in aliases, 'complete retained execution alias')
                actual=pin(P/aliases[row['path']])
                need(all(actual[k]==row[k] for k in ('bytes','sha256')), 'retained literal execution bytes')
                historic+=1
    routes=json.loads((P/'table_routes.json').read_text());validate_routes(routes)
    O.mkdir(parents=True)
    env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1'
    receipts=[]
    def run(name,command,inputs,cwd=None,cap=60):
        before=[pin(p) for p in inputs];start=time.monotonic()
        try:
            r=subprocess.run(command,env=env,cwd=cwd,capture_output=True,timeout=cap)
        except subprocess.TimeoutExpired as e:
            (O/(name+'.stdout')).write_bytes(e.stdout or b'')
            (O/(name+'.stderr')).write_bytes(e.stderr or b'')
            (O/(name+'.timeout.json')).write_text(json.dumps(dict(status='TIMEOUT_NO_CERTIFICATE',inputs=before,command=command,cap=cap),indent=2)+'\n')
            raise
        so=O/(name+'.stdout');se=O/(name+'.stderr')
        so.write_bytes(r.stdout);se.write_bytes(r.stderr)
        record=dict(command=command,cwd=str(cwd) if cwd else None,inputs=before,
                    exit_code=r.returncode,elapsed=time.monotonic()-start,cap=cap,stdout=pin(so),stderr=pin(se))
        (O/(name+'.receipt.json')).write_text(json.dumps(record,indent=2)+'\n')
        need(before==[pin(p) for p in inputs], 'unchanged executed input')
        need(r.returncode==0 and not r.stderr, 'clean execution: '+name)
        receipts.append(name)
        return r.stdout
    arithmetic=json.loads(run('arithmetic',[sys.executable,str(P/'arithmetic.py')],[P/'arithmetic.py']))
    row_count=validate(arithmetic)
    need(arithmetic==json.loads((P/'expected_arithmetic.json').read_text()),'exact complete arithmetic output')
    gap=run('fields',['/opt/homebrew/bin/gap','-q','-T',str(P/'field_controls.g')],[P/'field_controls.g'])
    need(gap==(P/'expected_gap.txt').read_bytes(), 'exact actual finite-field controls')
    need(len([s for s in gap.decode().splitlines() if s.strip()])==7 and b'COMPLETE_D4_FIELD_CONTROLS 1620' in gap,'complete finite-field roster')
    damaged=[]
    for name in ['missing_prime_power','wrong_primitive_power','wrong_projective_order','missing_source_row','extra_surviving_row','missing_U3_exclusion']:
        if name in ['missing_prime_power','wrong_primitive_power','wrong_projective_order']:
            bad=copy.deepcopy(arithmetic)
            if name=='missing_prime_power':bad['prime_power_rows'].pop()
            elif name=='wrong_primitive_power':bad['prime_power_rows'][1]['primitive_part']=1
            else:bad['prime_power_rows'][1]['projective_order']*=2
            f=validate
        else:
            bad=copy.deepcopy(routes)
            if name=='missing_source_row':bad['rows'].pop()
            elif name=='extra_surviving_row':bad['rows'][34]['route']='retain_B3'
            else:bad['rows'][35]['route']='small_exponents'
            f=validate_routes
        try:f(bad)
        except ValueError:damaged.append(name)
        else:raise ValueError('damaged certificate accepted: '+name)
    (O/'damaged_controls.json').write_text(json.dumps(damaged,indent=2)+'\n')
    guards=[]
    for script in ['check.py','arithmetic.py']:
        for mode in ['argument','environment']:
            forbidden=O/('forbidden_'+script+'_'+mode)
            command=[sys.executable];e=env.copy()
            if mode=='argument':command+=['-O']
            else:e['PYTHONOPTIMIZE']='1'
            r=subprocess.run(command+[str(P/script),'--out',str(forbidden)],env=e,capture_output=True,timeout=10)
            need(r.returncode!=0 and b'unoptimized execution required' in r.stderr and not forbidden.exists(),'pre-output optimization rejection')
            guards.append(dict(script=script,mode=mode,exit_code=r.returncode,stderr=r.stderr.decode()))
    (O/'optimization_controls.json').write_text(json.dumps(guards,indent=2)+'\n')
    native=O/'native';native.mkdir();shutil.copy2(P/'cover.tex',native/'cover.tex')
    for i in range(2):
        run('native'+str(i),['/opt/homebrew/bin/pdflatex','-halt-on-error','-interaction=nonstopmode','cover.tex'],[native/'cover.tex'],cwd=native)
    log=(native/'cover.log').read_text()
    need(not any(x in log for x in ['Overfull','LaTeX Warning']), 'native references and page widths')
    from pypdf import PdfReader
    reader=PdfReader(native/'cover.pdf')
    text='\n'.join(p.extract_text() or '' for p in reader.pages)
    (native/'text.txt').write_text(text)
    need(len(reader.pages)==3, 'complete three-page proof')
    if (P/'expected_text.txt').exists():need(text==(P/'expected_text.txt').read_text(),'exact native text')
    if a.render:
        run('render',['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile=page-%02d.png','cover.pdf'],[native/'cover.pdf'],cwd=native)
    report=dict(status='PASS_D4_COVER_COMPONENT',exports=len(exports),dependencies=len(deps),source_rows=42,
                prime_power_controls=row_count,exclusion_checks=arithmetic['exclusion_checks'],finite_fields=6,
                normalizer_degree_cases=1620,damaged_controls=len(damaged),optimization_guards=len(guards),
                native_pages=3,underfull_messages=log.count('Underfull'),historical_execution_pins=historic,
                receipts=receipts,whole_original_credit=0)
    (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':main()
