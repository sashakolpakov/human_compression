#!/usr/bin/env python3
"""Replay only the new small structural witnesses, never the old geometry census."""
from pathlib import Path
import argparse,json,subprocess,hashlib,sys,time
HERE=Path(__file__).resolve().parent

def gap(x):
 if isinstance(x,str):return json.dumps(x)
 if isinstance(x,list):return '['+','.join(map(gap,x))+']'
 if isinstance(x,dict):return 'rec('+','.join(k+':='+gap(v) for k,v in x.items())+')'
 return str(x)
def run(out,code,gap_exe):
 (out/'job.g').write_text(code)
 t=time.monotonic();r=subprocess.run([gap_exe,'-q','-T',str(out/'job.g')],capture_output=True,text=True,timeout=120)
 (out/'stdout.txt').write_text(r.stdout);(out/'stderr.txt').write_text(r.stderr)
 return r,time.monotonic()-t

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--controls',action='store_true');p.add_argument('--gap',default='/opt/homebrew/bin/gap');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 subprocess.run([sys.executable,'-B',str(HERE/'prepare_models.py'),'--out',str(a.out/'models.json')],check=True)
 obj=json.loads((a.out/'models.json').read_text())
 if (HERE/'models.json').is_file() and (HERE/'models.json').read_bytes()!=(a.out/'models.json').read_bytes():raise ValueError('model reconstruction changed')
 pre='CubicModels:='+gap(obj['cubic'])+';;\nSquareLinear:='+gap(obj['square_linear'])+';;\nFiniteModels:='+gap(obj['finite_models'])+';;\n'
 code=pre+(HERE/'verify.g').read_text();r,seconds=run(a.out,code,a.gap)
 if r.returncode or r.stderr.strip() or 'PASS_SEVEN_SHARED_STRUCTURES' not in r.stdout:raise ValueError((r.returncode,r.stdout[-2000:],r.stderr))
 rows=[l.split()[1] for l in r.stdout.splitlines() if l.startswith('PASS_SHARED_ROW ')]
 if rows!=['T6.2','T6.3','T6.4','T6.5','T8.1','T8.2','T8.3']:raise ValueError(rows)
 controls=[]
 if a.controls:
  changes=[('wrong cubic order','Size(G)=48*r.s^3','Size(G)=47*r.s^3'),('wrong extraspecial order','Extra(N,7,"T6_3_N")','Extra(N,5,"T6_3_N")'),('nontrivial complement intersection','Split(G,N,C,"T6_3")','Split(G,N,N,"T6_3")'),('wrong square quotient target','DirectProduct(SymmetricGroup(3),SymmetricGroup(3)),"T8_1_S3xS3"','CyclicGroup(IsPermGroup,36),"T8_1_S3xS3"'),('false finite normal factor','Size(G)=720 and Size(P)=60','Size(G)=720 and Size(P)=30'),('wrong final source stage','Split(G,K3,cs.S,"T8_3_FINAL_S3")','Split(G,K2,cs.S,"T8_3_FINAL_S3")')]
  for i,(name,old,new) in enumerate(changes):
   if old not in code:raise ValueError('unapplied control '+name)
   d=a.out/f'control_{i}';d.mkdir();q,tm=run(d,code.replace(old,new,1),a.gap)
   if not q.returncode and not q.stderr.strip() and 'PASS_SEVEN_SHARED_STRUCTURES' in q.stdout:raise ValueError('unrejected '+name)
   controls.append(name)
 inputs=[{'path':str(f.relative_to(HERE)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in [HERE/'prepare_models.py',HERE/'verify.g',HERE/'run.py',HERE/'inputs/model_data.json',HERE/'models.json']]
 report={'code_and_data_bindings':inputs,'generated_job_sha256':hashlib.sha256(code.encode()).hexdigest(),'status':'PASS','source_rows':rows,'finite_witness_seconds':seconds,'normal_and_complement_witnesses':sum(l.startswith('SPLIT ') for l in r.stdout.splitlines()),'direct_product_witnesses':sum(l.startswith('DIRECT ') for l in r.stdout.splitlines()),'named_bijective_maps':sum(l.startswith('NAMED ') for l in r.stdout.splitlines()),'controls':controls,'unchanged_presentation_and_geometry_reexecuted':False,'uniform_T8_1':'Written splitting of the accepted affine model plus the one fixed faithful1152-element linear group; no finite-parameter extrapolation.','full_original_admission':False}
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
