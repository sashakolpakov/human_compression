"""Run only the seven fixed survey rows after exact method acceptance."""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
import argparse, hashlib, json, os, subprocess
from pathlib import Path

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def check_hash(path, expected):
    need(hashlib.sha256(path.read_bytes()).hexdigest()==expected, 'accepted bytes '+str(path))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--study',type=Path,required=True)
    parser.add_argument('--plan',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args=parser.parse_args()
    S=args.study.resolve();plan=json.loads(args.plan.read_text())
    need(plan.get('acceptance')=='ACCEPTED_FOR_FIXED_ROWS', 'explicit accepted plan required')
    check_hash(S/plan['method_manifest'],plan['method_manifest_sha256'])
    check_hash(S/plan['root_adoption_manifest'],plan['root_adoption_sha256'])
    P=(S/plan['method_manifest']).parent
    for row in json.loads((P/'manifest.json').read_text())['exports']:
        data=(P/row['path']).read_bytes()
        need(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'frozen method export')
    need(type(plan['runs']) is list and plan['runs'],'nonempty fixed plan')
    expected={('symmetric',8):(7,range(1,5),120),('symmetric',10):(9,range(1,6),120),('symmetric',11):(10,range(1,6),120),('symmetric',12):(7,range(1,7),120),('symmetric',13):(7,range(1,7),300),('symmetric',14):(8,range(1,8),900),('even',15):(7,[2,4,6],900)}
    for row in plan['runs']:
        spec=row['spec'];key=(spec['kind'],spec['degree'])
        need(all(type(spec[k]) is int for k in ['degree','rank_limit','branch']), 'literal integer target parameters')
        need(key in expected,'only fixed survey targets')
        rank,branches,cap=expected[key]
        need(spec['rank_limit']==rank and spec['branch'] in branches and spec['engine_entry']=='pool','exact fixed target branch')
        need(type(row['cap_seconds']) is int and 1<=row['cap_seconds']<=cap,'bounded cap')
    env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
    cp=subprocess.run([sys.executable,str(P/'run_pool.py'),'--plan',str(args.plan.resolve()),'--out',str(args.out.resolve())],env=env)
    raise SystemExit(cp.returncode)

if __name__=='__main__':main()
