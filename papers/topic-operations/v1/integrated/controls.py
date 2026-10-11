#!/usr/bin/env python3
"""Bounded false-input checks, separate from the actual proof certificate."""
from pathlib import Path
import importlib.util,json,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent
def need(ok,message):
 if not ok:raise RuntimeError(message)
def main():
 source=(ROOT/'programs/affine_example.py').read_text();rows=[]
 mutations=[('wrong_quotient_lattice','modulus=2*s','modulus=s'),('erase_translation','refl(0,3,(1,0,0,-1))','refl(0,3)'),('wrong_translation_word','word([2,3,0,1]*2)','word([2,3,1,0]*2)')]
 for name,old,new in mutations:
  need(source.count(old)==1,'mutation anchor '+name)
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'bad.py';p.write_text(source.replace(old,new))
   r=subprocess.run([sys.executable,'-B','-O',str(p)],capture_output=True,text=True)
   need(r.returncode!=0,'bad model accepted '+name)
   rows.append({'name':name,'rejected':True,'diagnostic':r.stderr.strip().splitlines()[-1]})
 spec=importlib.util.spec_from_file_location('affine_control',ROOT/'programs/affine_example.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 norm=max(sum(abs(x) for x in t) for H in m.proper() for _,t in H)
 need(norm==4,'independent l1 witness');rows.append({'name':'false_proper_translation_l1_bound_two','rejected':norm>2,'actual_maximum':norm})
 print(json.dumps({'status':'PASS','controls':rows},indent=2,sort_keys=True))
if __name__=='__main__':main()
