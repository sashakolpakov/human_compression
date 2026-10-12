#!/usr/bin/env python3
import argparse,json,subprocess,time,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--seconds',type=float,default=5);p.add_argument('--key',default='square_candidates');p.add_argument('--out',type=Path,required=True);p.add_argument('--resume',action='store_true');a=p.parse_args()
rows=json.loads(Path('arithmetic_candidates.json').read_text())[a.key];results=json.loads(a.out.read_text())['results'] if a.resume else []
for row in rows[len(results):]:
 cmd=['/private/tmp/L018_exact_packing',str(row['width']),str(row['height']),str(row['pieces']),str(a.seconds)]
 r=subprocess.run(cmd,check=True,text=True,capture_output=True,timeout=a.seconds+15);d=json.loads(r.stdout);d['command']=cmd;results.append(d)
 out={'status':'BOUNDED_BATCH_COMPLETE' if len(results)==len(rows) else 'BOUNDED_BATCH_RUNNING','cpp_sha256':hashlib.sha256(Path('exact_packing.cpp').read_bytes()).hexdigest(),'cpp_binary_sha256':hashlib.sha256(Path(cmd[0]).read_bytes()).hexdigest(),'candidate_key':a.key,'total_candidates':len(rows),'results':results}
 a.out.write_text(json.dumps(out,indent=2)+'\n');print(d['width'],d['height'],d['pieces'],d['status'],d['nodes'],d['seconds'],flush=True)
