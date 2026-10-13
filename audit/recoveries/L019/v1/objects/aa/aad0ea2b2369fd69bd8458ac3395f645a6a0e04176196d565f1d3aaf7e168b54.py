import json
import os
from pathlib import Path
import subprocess
import sys
import time
if sys.flags.optimize:raise SystemExit('optimized Python is unsupported')
w=Path(__file__).resolve().parent
env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);receipts=[]
commands=[['pdflatex','-interaction=nonstopmode','-halt-on-error','orbit_budgets.tex']]*2
commands.append(['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile=native-%02d.png','orbit_budgets.pdf'])
for index,args in enumerate(commands):
    start=time.monotonic();p=subprocess.run(args,cwd=w,env=env,capture_output=True,timeout=60)
    (w/('build%d.stdout'%index)).write_bytes(p.stdout);(w/('build%d.stderr'%index)).write_bytes(p.stderr)
    receipts.append({'args':args,'returncode':p.returncode,'seconds':time.monotonic()-start,'deadline_seconds':60})
    (w/'build_receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
    if p.returncode:raise ValueError('Native build failed')
print('PASS_NATIVE_ORBIT_BUDGETS')
