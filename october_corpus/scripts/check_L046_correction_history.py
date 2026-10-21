"""Run the unchanged science77 checks on their exact preserved editions."""
from pathlib import Path
import hashlib,importlib.util,json,os,shutil,tempfile
AUD='audit/bounded-corrections/L046/v1'
def verify(root):
 root=Path(root).resolve();routes=json.loads((root/AUD/'history_routes.json').read_text())['routes']
 for row in routes.values():
  raw=(root/row['path']).read_bytes()
  if len(raw)!=row['bytes']or hashlib.sha256(raw).hexdigest()!=row['sha256']:raise ValueError('Historical science77 bytes changed')
 with tempfile.TemporaryDirectory(prefix='L046-history-')as tmp:
  historical=Path(tmp)/'repo'
  shutil.copytree(root,historical,copy_function=os.link,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc'))
  if(root/'.git').exists():(historical/'.git').symlink_to((root/'.git').resolve(),target_is_directory=(root/'.git').is_dir())
  for name,row in routes.items():
   target=historical/name;target.unlink();shutil.copyfile(root/row['path'],target)
  spec=importlib.util.spec_from_file_location('immutable_science77',historical/'scripts/verify_snapshot.py')
  module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);module.ROOT=historical
  nested=module.check_previous_science77();science77=module.check_science77()
  if science77['counts']['corrected_recoveries']!=77 or science77['counts']['mathematical_pending']!=27:raise ValueError('Historical partition changed')
  return dict(status='PASS_EXACT_HISTORICAL_SCIENCE77',previous_history=nested,science77=science77)
