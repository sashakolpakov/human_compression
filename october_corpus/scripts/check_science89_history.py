"""Evaluate science88 and its entire preceding chain using exact historical pointers."""
import sys
if sys.flags.optimize:raise RuntimeError('Ordinary Python required')
from pathlib import Path
import hashlib,importlib.util,json,os,shutil,tempfile
AUD='audit/science89/v1'
def verify(root):
 root=Path(root).resolve();data=json.loads((root/AUD/'history_routes.json').read_text())
 for r in data['routes'].values():
  raw=(root/r['path']).read_bytes()
  if len(raw)!=r['bytes']or hashlib.sha256(raw).hexdigest()!=r['sha256']:raise ValueError('Changed historical bytes')
 with tempfile.TemporaryDirectory(prefix='science89-history-')as tmp:
  view=Path(tmp)/'repo';shutil.copytree(root,view,copy_function=os.link,symlinks=True,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc'))
  if(root/'.git').exists():(view/'.git').symlink_to((root/'.git').resolve(),target_is_directory=(root/'.git').is_dir())
  for name,r in data['routes'].items():
   p=view/name;p.unlink();shutil.copyfile(root/r['path'],p)
  spec=importlib.util.spec_from_file_location('science89_exact_predecessor',view/'scripts/verify_snapshot.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);m.ROOT=view
  previous=m.check_previous_science88();current=m.check_science88()
  if[current['counts'][k]for k in ['corrected_recoveries','refuted','handled','mathematical_pending']]!=[88,9,97,8]:raise ValueError('Predecessor counts')
  return dict(status='PASS_EXACT_SCIENCE88_HISTORY',previous=previous,current=current)
