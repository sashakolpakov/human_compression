#!/usr/bin/env python3
"""Fail-closed concrete-data controls; run only in fresh private directories."""
from pathlib import Path
import json,subprocess,sys,tempfile

def run():
    root=Path(__file__).resolve().parent
    changes=[
      ('wrong_diagram_involution','literal_twist.py','q=(0,2,1,3)','q=(1,0,2,3)'),
      ('erase_affine_translation','affine_example.py','refl(0,3,(1,0,0,-1))','refl(0,3,(0,0,0,0))'),
      ('wrong_literal_parabolic','literal_twist.py','for a in two_support]+[pp],op,unit)','for a in two_support]+[qq],op,unit)'),
      ('reverse_action_composition','literal_twist.py','action[compose(b,c)][a]','action[compose(c,b)][a]')]
    rows=[]
    for name,filename,old,new in changes:
        with tempfile.TemporaryDirectory(prefix='N005-twist-control-') as tmp:
            dst=Path(tmp)
            for f in (root/'programs').glob('*.py'):(dst/f.name).write_bytes(f.read_bytes())
            f=dst/filename;s=f.read_text()
            if s.count(old)!=1:raise RuntimeError('mutation anchor '+name)
            f.write_text(s.replace(old,new))
            p=subprocess.run([sys.executable,'-B','-O',str(dst/'literal_twist.py')],capture_output=True,text=True)
            if p.returncode==0:raise RuntimeError('control accepted '+name)
            rows.append({'name':name,'rejected':True,'error':p.stderr.strip().splitlines()[-1]})
    return {'status':'PASS','controls':rows}
if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
