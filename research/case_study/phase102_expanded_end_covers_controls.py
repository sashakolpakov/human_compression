#!/usr/bin/env python3
"""Negative controls for the frozen expanded-end affine certificate."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
PROGRAM='phase102_expanded_end_covers_check.py'
CERT='phase102_expanded_end_covers_certificate.json'
MODEL='phase66_coprime_cover_permutation_model.json'


def require(ok,label):
    if not ok:raise ValueError(label)


def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(path):return {str(p.relative_to(path)):sha(p) for p in sorted(path.rglob('*')) if p.is_file()}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output-dir',type=Path,required=True)
    ap.add_argument('--successful-replay-dir',type=Path,required=True)
    args=ap.parse_args()
    require(not args.output_dir.exists() and not args.output_dir.is_symlink(),'new controls directory required')
    args.output_dir.mkdir(parents=True)
    frozen=json.loads((ROOT/CERT).read_text());rows=[]
    for kind in ['shift','medial_word','killed_basis','kernel_dimension','defect_remainder']:
        test=copy.deepcopy(frozen)
        if kind=='shift':test['shifts'][1]=[]
        if kind=='medial_word':test['killed_relation_word_0based']=[1,2]*2
        if kind=='killed_basis':test['killed_invariant_basis'][0]=[]
        if kind=='kernel_dimension':test['cover_kernel_dimension']=129
        if kind=='defect_remainder':test['recursive_intersection_tests'][0]['forbidden_base_cosets'][0]['nonzero_remainder']=[]
        path=args.output_dir/(kind+'.json');path.write_text(json.dumps(test,indent=2)+'\n')
        out=args.output_dir/(kind+'-out')
        proc=subprocess.run([sys.executable,'-O',str(ROOT/PROGRAM),'--expected-certificate',str(path),'--output-dir',str(out)],capture_output=True,text=True)
        require(proc.returncode!=0 and not out.exists() and 'expected certificate differs' in proc.stderr,'altered certificate accepted: '+kind)
        rows.append({'kind':kind,'rejected':True,'output_absent':True})
    folder=args.output_dir/'changed-model';folder.mkdir()
    for name in [PROGRAM,MODEL]:shutil.copyfile(ROOT/name,folder/name)
    with (folder/MODEL).open('ab') as out:out.write(b'\n')
    out=folder/'must-not-exist'
    proc=subprocess.run([sys.executable,'-O',str(folder/PROGRAM),'--output-dir',str(out)],capture_output=True,text=True)
    require(proc.returncode!=0 and not out.exists() and 'model hash mismatch' in proc.stderr,'changed model accepted')
    rows.append({'kind':'model_hash','rejected':True,'output_absent':True})
    before=inventory(args.successful_replay_dir)
    require(set(before)=={'certificate.json','report.json'},'unexpected successful output inventory')
    existing=args.output_dir/'existing-file';existing.write_text('preserve\n')
    dangling=args.output_dir/'dangling-link';dangling.symlink_to(args.output_dir/'absent')
    refusals=[]
    for name,path in [('directory',args.successful_replay_dir),('file',existing),('dangling_symlink',dangling)]:
        proc=subprocess.run([sys.executable,'-O',str(ROOT/PROGRAM),'--output-dir',str(path)],capture_output=True,text=True)
        require(proc.returncode!=0 and 'fresh output directory required' in proc.stderr,'occupied output accepted')
        refusals.append(name)
    require(inventory(args.successful_replay_dir)==before and existing.read_text()=='preserve\n' and dangling.is_symlink(),'output altered')
    report={'status':'PASS','date':'2026-10-10','negative_controls':rows,'no_clobber':refusals,
            'successful_outputs_unchanged':before,'optimized_python':True,
            'program_sha256':sha(ROOT/PROGRAM),'certificate_sha256':sha(ROOT/CERT),
            'controls_sha256':sha(Path(__file__)),'scope':'Author integrity controls, independent mathematical review still required.'}
    (args.output_dir/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
