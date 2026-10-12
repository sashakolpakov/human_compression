"""Public science-only gate, independent of the unchanged measurement overview."""
from pathlib import Path
import argparse, importlib.util, json
def verify(root):
 root=Path(root).resolve();p=root/'audit/science55/v1/publication_plan/check.py'
 spec=importlib.util.spec_from_file_location('science55_publication',p)
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 return module.verify(root,require_root=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[1]);a=p.parse_args();print(json.dumps(verify(a.repo),indent=2))
