"""Run the complete previous L029 disposition and history on preserved bytes."""
import sys
if sys.flags.optimize:raise RuntimeError('Optimized Python is not supported')
from pathlib import Path
import hashlib,importlib.util,json,os,shutil,tempfile
AUD='audit/principal-refutations/suzuki-subfields/v1'
def verify(root):
 root=Path(root).resolve();routes=json.loads((root/AUD/'history_routes.json').read_text())['routes']
 for row in routes.values():
  p=root/row['path'];raw=p.read_bytes()
  if len(raw)!=row['bytes']or hashlib.sha256(raw).hexdigest()!=row['sha256']:raise ValueError('Historical L029 bytes changed')
 with tempfile.TemporaryDirectory(prefix='suzuki-dispositions-history-')as tmp:
  historical=Path(tmp)/'repo';shutil.copytree(root,historical,copy_function=os.link,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc'))
  if(root/'.git').exists():(historical/'.git').symlink_to((root/'.git').resolve(),target_is_directory=(root/'.git').is_dir())
  for name,row in routes.items():
   target=historical/name;target.unlink();shutil.copyfile(root/row['path'],target)
  spec=importlib.util.spec_from_file_location('immutable_L029_disposition',historical/'scripts/verify_snapshot.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.ROOT=historical
  previous=m.check_previous_L029_disposition();current=m.check_L029_disposition()
  if current['counts']['corrected_recoveries']!=85 or current['counts']['handled']!=87 or current['counts']['refuted']!=2:raise ValueError('Historical L029 counts')
  return dict(status='PASS_EXACT_L029_DISPOSITION_HISTORY',previous=previous,L029=current)
