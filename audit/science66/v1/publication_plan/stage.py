"""Isolated science66 overlay; public baseline is read only."""
from pathlib import Path
import argparse,hashlib,json,shutil
HERE=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text())
def need(x,m):
    if not x:raise ValueError(m)
def binding(p,r):need(p.stat().st_size==r['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],'binding '+str(p))
def overlay(repo,out,changes):
    def rec(src,dst,prefix=''):
        dst.mkdir(exist_ok=True)
        for p in src.iterdir():
            n=prefix+p.name;q=dst/p.name
            if n in changes:continue
            if p.is_dir() and any(x.startswith(n+'/') for x in changes):rec(p,q,n+'/')
            else:q.symlink_to(p,target_is_directory=p.is_dir())
    rec(repo,out)
def main(a):
    repo=a.repo.resolve();out=a.out.resolve();need(not out.exists() and not out.is_relative_to(repo),'fresh private stage')
    plan=load(HERE/'copy_plan.json');rows={r['public_path']:r for r in plan['files']}
    wr=[p for p in (HERE/'wrappers').rglob('*') if p.is_file()]
    changes={n for n,r in rows.items() if r['transport']=='COPY_FROZEN'}|{str(p.relative_to(HERE/'wrappers')) for p in wr}|{'audit/science66/v1/publication_plan'}
    overlay(repo,out,changes)
    for n,r in rows.items():
        if r['transport']=='EXISTING_PUBLIC':binding(repo/n,r);continue
        src=a.study/r['study_path'];binding(src,r);dst=out/n;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
    for src in wr:
        dst=out/src.relative_to(HERE/'wrappers');dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
    if (HERE/'manifest.json').exists():own=[HERE/r['path'] for r in load(HERE/'manifest.json')['exports']]+[HERE/'manifest.json']
    else:own=[p for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc']
    for src in own:
        dst=out/'audit/science66/v1/publication_plan'/src.relative_to(HERE);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
    report=dict(status='PASS_PRIVATE_STAGE_ROOT_PUBLICATION_REQUIRED',logical_routes=len(plan['files']),complete_packets=len(plan['packets']),new_files=plan['new_public_files'],reused_public_files=plan['reused_existing_public_files'],wrapper_files=len(wr),public_repo_written=False,source_assets_copied=False,new_measurements=0)
    (out/'science66_stage_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--study',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);main(p.parse_args())
