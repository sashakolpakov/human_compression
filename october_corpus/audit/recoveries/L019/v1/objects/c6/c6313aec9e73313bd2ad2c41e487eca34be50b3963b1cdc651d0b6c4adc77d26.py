import json,os,subprocess,sys,time
from pathlib import Path
if sys.flags.optimize:raise SystemExit('optimized Python is unsupported')
w=Path(__file__).resolve().parent;env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None);receipts=[]
commands=[['pdflatex','-interaction=nonstopmode','-halt-on-error','inheritance.tex']]*2+[['gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile=native-%02d.png','inheritance.pdf']]
for i,args in enumerate(commands):
 start=time.monotonic();p=subprocess.run(args,cwd=w,env=env,capture_output=True,timeout=60)
 (w/f'build{i}.stdout').write_bytes(p.stdout);(w/f'build{i}.stderr').write_bytes(p.stderr)
 receipts.append({'args':args,'returncode':p.returncode,'seconds':time.monotonic()-start,'deadline_seconds':60});(w/'build_receipts.json').write_text(json.dumps(receipts,indent=2)+'\n')
 if p.returncode:raise ValueError('Native build failed')
print('PASS_NATIVE_INHERITANCE')
