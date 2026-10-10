#!/usr/bin/env python3
"""Replay the exact bounded cyclic-index checks into a new directory.

Requires Python and GAP, but no private sources, catalogue or prior manuscript.
The full uniform proof has a separate written/retained-theorem trust boundary.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

BOUND={
 'phase169_cyclic_index_check.py':'a4400f0cf7df676c57439b37149771990c87c1671d5859cd2e4eb219f0e576e6',
 'phase169_cyclic_index_check.g':'0d3dd8bd7acee4330b2da8b27e7db4c554a2a60751a34f31424b0f1798f2ba13',
}


def require(test,message):
    if not test:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--inputs',type=Path,default=Path(__file__).resolve().parent)
    ap.add_argument('--gap',default=shutil.which('gap'))
    ap.add_argument('--output-dir',type=Path,required=True)
    args=ap.parse_args()
    require(not os.path.lexists(args.output_dir),'Refusing existing output path')
    for name,expected in BOUND.items():
        require(sha(args.inputs/name)==expected,'Changed bound checker: '+name)
    require(args.gap,'GAP not found')
    out=args.output_dir;out.mkdir(parents=True)
    copies=out/'inputs';copies.mkdir()
    for name in BOUND:shutil.copyfile(args.inputs/name,copies/name)
    records=[]
    def run(label,argv,stdin=None):
        started=time.monotonic()
        p=subprocess.run(argv,input=stdin,capture_output=True,text=True,cwd=out,timeout=180)
        (out/(label+'.log')).write_text(p.stdout)
        (out/(label+'.stderr')).write_text(p.stderr)
        require(p.returncode==0 and 'Error,' not in p.stdout+p.stderr,label+' failed')
        records.append({'label':label,'argv':argv,'seconds':time.monotonic()-started,
                        'exit_code':p.returncode,'log_sha256':sha(out/(label+'.log')),
                        'stderr_sha256':sha(out/(label+'.stderr'))})
        return p.stdout
    version=run('gap-version',[args.gap,'-q','-T'], 'Print(GAPInfo.Version,"\\n");QUIT;\n').strip()
    normal=run('normal-forms',[sys.executable,'-B','-O',str(copies/'phase169_cyclic_index_check.py'),
                              '--output',str(out/'normal-forms.json')])
    require('PHASE169_NORMAL_FORMS_PASS 11' in normal,'Incomplete normal-form run')
    nf=json.loads((out/'normal-forms.json').read_text())
    require(len(nf['cases'])==11 and nf['total_IP_pairs']==704,'Wrong finite normal-form scope')
    gap=run('literal-presentations',[args.gap,'-q','-T',str(copies/'phase169_cyclic_index_check.g')])
    require(gap.rstrip().endswith('PHASE169_LITERAL_PRESENTATIONS_PASS'),'Incomplete GAP run')
    rows=[list(map(int,r)) for r in re.findall(r'^CASE (\d+) EPS (\d+) ORDER (\d+) EXP (\d+) CENTER (\d+) BOTH_PRESENTATIONS_AND_INVERSES PASS$',gap,re.M)]
    expected=[[M,e,8*M,M,4 if e==0 else 2] for M in [4,8,16,32] for e in ([0] if M==4 else [0,1])]
    require(rows==expected,'Wrong literal presentation cases')
    require('NEGATIVE M 4 EPS 1 ORDER 16 RIGHT_ORDER 2 PASS' in gap,'Missing degenerate boundary control')
    for name,expected_sha in BOUND.items():
        require(sha(args.inputs/name)==expected_sha and sha(copies/name)==expected_sha,'Checker changed during replay')
    result={'status':'PASS_EXACT_BOUNDED_CHECKS','inputs':BOUND,'GAP':version,
            'normal_form_cases':nf['cases'],'normal_form_IP_pairs':704,
            'literal_presentation_cases':rows,'negative_boundary':{'M':4,'epsilon':1,'order':16,'right_order':2},
            'runs':records,'private_source_inputs':False,'source_catalogue_used':False,
            'whole_family_proved_by_finite_sample':False,'Lean_certificate':False,
            'runner_sha256':sha(Path(__file__))}
    with (out/'report.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print('PHASE169_EXACT_CHECKS_PASS')


if __name__=='__main__':main()
