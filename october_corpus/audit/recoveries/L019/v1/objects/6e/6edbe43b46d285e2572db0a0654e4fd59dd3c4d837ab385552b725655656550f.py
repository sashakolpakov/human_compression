import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import time
if sys.flags.optimize:
    raise SystemExit('optimized Python is unsupported')
def need(p,message):
    if not p:raise ValueError(message)
w=Path(__file__).resolve().parent
env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);receipts=[]
def run(tag,args,success=True,extra=None):
    e=env.copy()
    if extra:e.update(extra)
    start=time.monotonic();p=subprocess.run(args,cwd=w,env=e,capture_output=True,timeout=60)
    (w/(tag+'.stdout')).write_bytes(p.stdout);(w/(tag+'.stderr')).write_bytes(p.stderr)
    need((p.returncode==0)==success,'unexpected exit: '+tag)
    receipts.append({'tag':tag,'args':args,'returncode':p.returncode,'seconds':time.monotonic()-start,'deadline_seconds':60})
    (w/'check_receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
    return p
run('extraction',[sys.executable,'extract_inputs.py'])
run('direct',[sys.executable,'check_boundaries.py','--output','direct_report.json'])
p=run('gap',['/opt/homebrew/bin/gap','-q','-b','gap_boundaries.g'])
need(not p.stderr and p.stdout.decode().strip().endswith('PASS_INITIAL_FRACTURE_BOUNDARIES'),'unclean GAP result')
lines=p.stdout.decode().replace('\r','').splitlines();data=json.loads((w/'direct_report.json').read_text())
expected=[]
for row in data['a11']:
    expected.append('A11|%d|%s|1'%(row['source_index'],str(row['reverse']).lower()))
for row in data['s8']:
    expected.append('S8|%d|%d|%s'%(row['source_index'],row['omitted'],str(sorted(map(len,row['orbits'])))))
for row in data['small']:
    expected.append('SMALL|%d|%s'%(row['source_index'],str([sorted(map(len,o)) for o in row['omission_orbits']])))
need([line.replace(' ','') for line in lines[:-1]]==[line.replace(' ','') for line in expected],'literal/GAP disagreement')
roster=json.loads((w/'inputs.json').read_text())
for name,mutate in [('missing_case',lambda d:d['a11_rank_six'].pop()),('bad_permutation',lambda d:d['s8_rank_six'][0]['permutations'][0].__setitem__(0,99)),('wrong_index',lambda d:d['a11_rank_six'][0].__setitem__('source_index',1))]:
    bad=copy.deepcopy(roster);mutate(bad);(w/(name+'.json')).write_text(json.dumps(bad))
    run(name,[sys.executable,'check_boundaries.py','--input',name+'.json','--output',name+'.report.json'],False)
run('optimization_argument',[sys.executable,'-O','check_boundaries.py','--output','optimization.report.json'],False)
run('optimization_environment',[sys.executable,'check_boundaries.py','--output','optimization_env.report.json'],False,{'PYTHONOPTIMIZE':'1'})
for i in range(2):run('build'+str(i),['pdflatex','-interaction=nonstopmode','-halt-on-error','initial_fracture.tex'])
run('raster',['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile=native-%02d.png','initial_fracture.pdf'])
(w/'check_receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
print('PASS: literal/GAP agreement, five negative controls and native build')
