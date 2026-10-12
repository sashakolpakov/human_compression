"""Finalize wrapper bindings only before the proposal is frozen."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
def binding(p,name):
 b=p.read_bytes();return dict(path=name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
if (HERE/'manifest.json').exists():raise ValueError('Immutable proposal already frozen')
files=[binding(p,str(p.relative_to(HERE/'wrappers')))for p in sorted((HERE/'wrappers').rglob('*'))if p.is_file()]
(HERE/'wrapper_routes.json').write_text(json.dumps(dict(files=files),indent=2)+'\n')
print(json.dumps(dict(wrapper_files=len(files))))
