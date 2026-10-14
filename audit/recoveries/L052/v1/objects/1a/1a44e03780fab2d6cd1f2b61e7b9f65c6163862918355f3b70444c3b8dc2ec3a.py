from pathlib import Path
import subprocess,time,json,sys
if sys.flags.optimize:raise RuntimeError('optimization unsupported')
w=Path(__file__).resolve().parent
rows=sorted(w.glob('T2.*'),key=lambda p:int(p.name.split('.')[1]))
for d in rows:
 if (d/'receipt.json').exists():continue
 t=time.monotonic()
 with (d/'stdout.log').open('w')as out,(d/'stderr.log').open('w')as err:
  try:
   p=subprocess.run(['/opt/homebrew/bin/gap','-q','-T',str(d/'run.g')],stdout=out,stderr=err,timeout=60)
   status='PASS'if p.returncode==0 and ('PASS_L052_ROW '+d.name)in(d/'stdout.log').read_text()and not(d/'stderr.log').read_text().strip()else'FAIL'
   result={'row':d.name,'status':status,'exit':p.returncode,'elapsed':time.monotonic()-t,'timeout':60}
  except subprocess.TimeoutExpired:
   result={'row':d.name,'status':'TIMEOUT','elapsed':time.monotonic()-t,'timeout':60}
 (d/'receipt.json').write_text(json.dumps(result,indent=2)+'\n');print(result,flush=True)
