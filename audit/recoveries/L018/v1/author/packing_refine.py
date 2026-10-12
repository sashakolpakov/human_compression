#!/usr/bin/env python3
import argparse,json,subprocess,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--seconds',type=float,required=True);p.add_argument('--binary',default='/private/tmp/L018_exact_packing_sides');p.add_argument('--cpp',type=Path,default=Path('exact_packing_sides.cpp'));p.add_argument('--out',type=Path,required=True);a=p.parse_args()
old=json.loads(a.input.read_text());rows=[z for z in old['results']if z['status']=='UNKNOWN'];out=[]
for row in rows:
 cmd=[a.binary,str(row['width']),str(row['height']),str(row['pieces']),str(a.seconds)];r=subprocess.run(cmd,check=True,text=True,capture_output=True,timeout=a.seconds+15);d=json.loads(r.stdout);d['command']=cmd;out.append(d)
 a.out.write_text(json.dumps({'status':'BOUNDED_REFINEMENT_COMPLETE'if len(out)==len(rows)else'BOUNDED_REFINEMENT_RUNNING','input_sha256':hashlib.sha256(a.input.read_bytes()).hexdigest(),'cpp_sha256':hashlib.sha256(a.cpp.read_bytes()).hexdigest(),'binary_sha256':hashlib.sha256(Path(a.binary).read_bytes()).hexdigest(),'total_unresolved_inputs':len(rows),'results':out},indent=2)+'\n');print(d['width'],d['height'],d['pieces'],d['status'],d['nodes'],d['seconds'],flush=True)
