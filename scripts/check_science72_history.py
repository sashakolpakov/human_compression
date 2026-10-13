"""Run science71 and its nested programme53 guards on saved read-only pointers."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,tempfile
def verify(root):
 root=Path(root).resolve();routes=json.loads((root/'audit/science72/v1/history_routes.json').read_text())['routes']
 for e in routes.values():
  data=(root/e['path']).read_bytes()
  if len(data)!=e['bytes']or hashlib.sha256(data).hexdigest()!=e['sha256']:raise ValueError('Historical71 binding '+e['path'])
 with tempfile.TemporaryDirectory(prefix='science72-history-')as tmp:
  historical=Path(tmp)
  def populate(src,dst,prefix=''):
   dst.mkdir(exist_ok=True)
   for child in src.iterdir():
    key=prefix+child.name;t=dst/child.name
    if key in routes:t.symlink_to(root/routes[key]['path'])
    elif child.is_dir()and any(x.startswith(key+'/')for x in routes):populate(child,t,key+'/')
    else:t.symlink_to(child,target_is_directory=child.is_dir())
  populate(root,historical)
  spec=importlib.util.spec_from_file_location('immutable_science71',historical/'scripts/verify_snapshot.py')
  module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);module.ROOT=historical
  nested=module.check_previous_science71();science71=module.check_science71()
  if science71['counts']['corrected_recoveries']!=71 or science71['counts']['measured']!=53:raise ValueError('Historical71 partition')
  return dict(status='PASS_EXACT_HISTORICAL_SCIENCE71_AND_PROGRAMME53',science71=science71,legacy=nested['legacy'],current=nested['current'])
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1]);a=p.parse_args();print(json.dumps(verify(a.repo),indent=2))
