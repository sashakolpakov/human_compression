"""Root-gated science68 publication entry."""
from pathlib import Path
import importlib.util
def verify(root):
 root=Path(root).resolve()
 spec=importlib.util.spec_from_file_location('science68_plan',root/'audit/science68/v1/publication_plan/check.py')
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 return module.verify(root,require_root=True)
