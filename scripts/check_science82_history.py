"""Run the complete science81 gate and prior history on exact preserved bytes."""
import sys
if sys.flags.optimize:raise RuntimeError('Optimized Python is not supported')
from pathlib import Path
import hashlib,importlib.util,json,os,shutil,tempfile
AUD='audit/science82/v1'
def verify(root):
 root=Path(root).resolve();routes=json.loads((root/AUD/'history_routes.json').read_text())['routes']
 for row in routes.values():
  p=root/row['path'];raw=p.read_bytes()
  if len(raw)!=row['bytes']or hashlib.sha256(raw).hexdigest()!=row['sha256']:raise ValueError('Historical science81 bytes changed')
 with tempfile.TemporaryDirectory(prefix='science82-history-')as tmp:
  historical=Path(tmp)/'repo';shutil.copytree(root,historical,copy_function=os.link,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc'))
  if(root/'.git').exists():(historical/'.git').symlink_to((root/'.git').resolve(),target_is_directory=(root/'.git').is_dir())
  for name,row in routes.items():
   target=historical/name;target.unlink();shutil.copyfile(root/row['path'],target)
  spec=importlib.util.spec_from_file_location('immutable_science81',historical/'scripts/verify_snapshot.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.ROOT=historical
  previous=m.check_previous_science81();current=m.check_science81()
  if current['counts']['corrected_recoveries']!=81 or current['counts']['handled']!=82:raise ValueError('Historical science81 counts')
  return dict(status='PASS_EXACT_SCIENCE81_HISTORY',previous=previous,science81=current)
