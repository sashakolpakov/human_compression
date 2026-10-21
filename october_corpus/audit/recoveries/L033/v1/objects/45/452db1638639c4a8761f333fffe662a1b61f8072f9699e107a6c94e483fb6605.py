import sys
if sys.flags.optimize: raise SystemExit('optimized execution unsupported')
from pathlib import Path
import json,subprocess,time
here=Path(__file__).resolve().parent
results=[]
for typ in ['3334','3335','3534','3535','353','435','535','5333']:
    out=here/(typ+'_full01')
    r=subprocess.run([sys.executable,str(here/'run.py'),'--type',typ,'--out',str(out),'--seconds','120'])
    results.append({'type':typ,'returncode':r.returncode,'report':str(out/'report.json')})
    (here/'batch01.json').write_text(json.dumps({'results':results,'complete':len(results)==8},indent=2)+'\n')
print('ALL_EIGHT_CHILDREN_TERMINAL',flush=True)
