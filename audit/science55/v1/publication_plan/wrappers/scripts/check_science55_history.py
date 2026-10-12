"""Run immutable programme53 guards through an exact read-only path overlay."""
from pathlib import Path
import argparse, hashlib, importlib.util, json, tempfile
def verify(root):
 root=Path(root).resolve();routes=json.loads((root/'audit/science55/v1/history_routes.json').read_text())['routes']
 for e in routes.values():
  data=(root/e['path']).read_bytes()
  if len(data)!=e['bytes']or hashlib.sha256(data).hexdigest()!=e['sha256']:raise ValueError('Historical route changed: '+e['path'])
 with tempfile.TemporaryDirectory(prefix='science55-history-')as tmp:
  historical=Path(tmp)
  def populate(src,dst,prefix=''):
   dst.mkdir(exist_ok=True)
   for child in src.iterdir():
    key=prefix+child.name;t=dst/child.name
    if key in routes:t.symlink_to(root/routes[key]['path'])
    elif child.is_dir()and any(x.startswith(key+'/')for x in routes):populate(child,t,key+'/')
    else:t.symlink_to(child,target_is_directory=child.is_dir())
  populate(root,historical)
  spec=importlib.util.spec_from_file_location('immutable_programme53',historical/'scripts/verify_snapshot.py')
  module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  # __file__.resolve() follows the saved script, so set only the imported
  # module's root; all135 original function bodies remain byte-identical.
  module.ROOT=historical
  legacy=module.check_previous_programme53();current=module.check_programme53()
  if current['measured']!=53 or current['mathematical_pending']!=52:raise ValueError('Historical programme53 partition')
  return dict(status='PASS_EXACT_HISTORICAL_PROGRAMME53',legacy=legacy,current=current)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1]);a=p.parse_args();print(json.dumps(verify(a.repo),indent=2))
