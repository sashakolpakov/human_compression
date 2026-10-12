"""Make an isolated public-route stage; never write through baseline symlinks."""
from pathlib import Path
import argparse, hashlib, json, shutil
HERE=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(t,m):
 if not t:raise ValueError(m)
def overlay(repo,out,changes):
 def populate(src,dst,prefix=''):
  dst.mkdir(exist_ok=True)
  for c in src.iterdir():
   name=prefix+c.name;t=dst/c.name
   if name in changes:continue
   if c.is_dir()and any(x.startswith(name+'/')for x in changes):populate(c,t,name+'/')
   else:t.symlink_to(c,target_is_directory=c.is_dir())
 populate(repo,out)
def main():
 p=argparse.ArgumentParser();p.add_argument('--study',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 repo=a.repo.resolve();out=a.out.resolve();need(not out.exists()and not out.is_relative_to(repo),'fresh private output required')
 plan=load(HERE/'copy_plan.json');wr=[x for x in (HERE/'wrappers').rglob('*')if x.is_file()]
 changes={r['public_path']for r in plan['files']}|{str(x.relative_to(HERE/'wrappers'))for x in wr}|{'audit/science59/v1/publication_plan'}
 overlay(repo,out,changes)
 for r in plan['files']:
  src=a.study/r['study_path'];need(src.stat().st_size==r['bytes']and sha(src)==r['sha256'],'frozen input '+r['study_path'])
  dst=out/r['public_path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
 for src in wr:
  dst=out/src.relative_to(HERE/'wrappers');dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
 # The public guard is portable against an export-only proposal copy.
 if (HERE/'manifest.json').exists():
  proposal_files=[HERE/e['path']for e in load(HERE/'manifest.json')['exports']]+[HERE/'manifest.json']
 else:proposal_files=[p for p in HERE.rglob('*')if p.is_file()and '__pycache__'not in p.parts and p.suffix!='.pyc']
 for src in proposal_files:
  dst=out/'audit/science59/v1/publication_plan'/src.relative_to(HERE);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
 report=dict(status='PASS_PRIVATE_STAGE_ACCEPTED_SCIENCE_ROOT_PUBLICATION_REQUIRED',root_science_adoptions_bound=True,files=len(plan['files']),packets=len(plan['packets']),wrapper_files=len(wr),public_repo_written=False,source_assets_copied=False,measurement_added=False)
 (out/'science59_stage_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
