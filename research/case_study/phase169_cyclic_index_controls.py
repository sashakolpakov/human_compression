#!/usr/bin/env python3
"""Portable replay and rejection controls for the frozen finite bridge checks."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def require(test,message):
    if not test:
        raise RuntimeError(message)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output-dir',type=Path,required=True)
    ap.add_argument('--gap',default=shutil.which('gap'))
    args=ap.parse_args()
    require(not os.path.lexists(args.output_dir),'Refusing existing output path')
    root=Path(__file__).resolve().parent
    out=args.output_dir;out.mkdir(parents=True)
    portable=out/'portable';portable.mkdir()
    names=['phase169_cyclic_index_check.py','phase169_cyclic_index_check.g','phase169_cyclic_index_verify.py']
    hashes={n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in names}
    for n in names:shutil.copyfile(root/n,portable/n)
    cases=[]
    def run(label,argv,success,needle):
        p=subprocess.run([sys.executable,'-B','-O',*map(str,argv)],capture_output=True,text=True,timeout=180,cwd=portable)
        require((p.returncode==0)==success and needle in p.stdout+p.stderr,'Wrong outcome: '+label)
        cases.append({'case':label,'expected_success':success,'returncode':p.returncode,
                      'stdout':p.stdout,'stderr':p.stderr})
    runner=portable/names[2];checker=portable/names[0]
    for kind in ['file','directory','dangling_symlink']:
        p=out/('existing-'+kind)
        if kind=='file':p.write_bytes(b'keep me')
        elif kind=='directory':p.mkdir();(p/'sentinel').write_bytes(b'keep me')
        else:p.symlink_to(out/'absent-target')
        for program,flag in [(runner,'--output-dir'),(checker,'--output')]:
            run(program.name+' rejects '+kind,[program,flag,p],False,'Refusing existing output path')
        require(p.is_symlink() if kind=='dangling_symlink' else
                (p.read_bytes()==b'keep me' if kind=='file' else (p/'sentinel').read_bytes()==b'keep me'),
                'Clobbered output')
    for n in names[:2]:
        p=portable/n;old=p.read_bytes();p.write_bytes(old+b'\n')
        dest=out/('mutated-'+p.suffix[1:])
        run('changed checker '+n,[runner,'--gap','/GAP-MUST-NOT-RUN','--output-dir',dest],False,'Changed bound checker')
        require(not os.path.lexists(dest),'Rejected mutation wrote output')
        p.write_bytes(old)
    run('only three public arithmetic files',[runner,'--gap',args.gap,'--output-dir',out/'fresh-replay'],True,'PHASE169_EXACT_CHECKS_PASS')
    for n in names:
        require(hashlib.sha256((root/n).read_bytes()).hexdigest()==hashes[n] and
                hashlib.sha256((portable/n).read_bytes()).hexdigest()==hashes[n],'Inputs changed')
    result={'status':'PASS','cases':cases,'case_count':len(cases),'input_hashes':hashes,
            'portable_copy_files':names,'private_source_files_copied':False,
            'portable_replay':json.loads((out/'fresh-replay/report.json').read_text())}
    (out/'controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PHASE169_CONTROLS_PASS',len(cases))


if __name__=='__main__':main()
