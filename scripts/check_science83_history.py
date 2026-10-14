"""Run the complete science82 gate and prior history on exact preserved bytes."""
import sys
if sys.flags.optimize:raise RuntimeError('Optimized Python is not supported')
from pathlib import Path
import hashlib,importlib.util,json,os,shutil,tempfile
AUD='audit/science83/v1'
def verify(root):
 root=Path(root).resolve();routes=json.loads((root/AUD/'history_routes.json').read_text())['routes']
 for row in routes.values():
  p=root/row['path'];raw=p.read_bytes()
  if len(raw)!=row['bytes']or hashlib.sha256(raw).hexdigest()!=row['sha256']:raise ValueError('Historical science82 bytes changed')
 with tempfile.TemporaryDirectory(prefix='science83-history-')as tmp:
  historical=Path(tmp)/'repo';shutil.copytree(root,historical,copy_function=os.link,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc'))
  if(root/'.git').exists():(historical/'.git').symlink_to((root/'.git').resolve(),target_is_directory=(root/'.git').is_dir())
  for name,row in routes.items():
   target=historical/name;target.unlink();shutil.copyfile(root/row['path'],target)
  spec=importlib.util.spec_from_file_location('immutable_science82',historical/'scripts/verify_snapshot.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.ROOT=historical
  previous=m.check_previous_science82();current=m.check_science82()
  if current['counts']['corrected_recoveries']!=82 or current['counts']['handled']!=83:raise ValueError('Historical science82 counts')
  return dict(status='PASS_EXACT_SCIENCE82_HISTORY',previous=previous,science82=current)
