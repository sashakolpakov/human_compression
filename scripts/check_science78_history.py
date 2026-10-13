"""Run the existing L046 correction and science77 gates on preserved editions."""
from pathlib import Path
import hashlib,importlib.util,json,os,shutil,tempfile
AUD='audit/science78/v1'
def verify(root):
 root=Path(root).resolve();routes=json.loads((root/AUD/'history_routes.json').read_text())['routes']
 for row in routes.values():
  raw=(root/row['path']).read_bytes()
  if len(raw)!=row['bytes']or hashlib.sha256(raw).hexdigest()!=row['sha256']:raise ValueError('Historical L046/science77 bytes changed')
 with tempfile.TemporaryDirectory(prefix='science78-history-')as tmp:
  historical=Path(tmp)/'repo';shutil.copytree(root,historical,copy_function=os.link,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc'))
  if(root/'.git').exists():(historical/'.git').symlink_to((root/'.git').resolve(),target_is_directory=(root/'.git').is_dir())
  for name,row in routes.items():
   target=historical/name;target.unlink();shutil.copyfile(root/row['path'],target)
  spec=importlib.util.spec_from_file_location('immutable_L046_edition',historical/'scripts/verify_snapshot.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);module.ROOT=historical
  previous=module.check_L046_previous();correction=module.check_L046_current()
  if previous['science77']['counts']['corrected_recoveries']!=77:raise ValueError('Historical recovery count changed')
  return dict(status='PASS_EXACT_L046_AND_SCIENCE77_HISTORY',previous=previous,correction=correction)
