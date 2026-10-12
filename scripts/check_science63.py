"""Root-gated entry into the immutable science63 publication proposal."""
from pathlib import Path
import importlib.util
def verify(root):
    root=Path(root).resolve()
    spec=importlib.util.spec_from_file_location('science63_plan',root/'audit/science63/v1/publication_plan/check.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.verify(root,require_root=True)
