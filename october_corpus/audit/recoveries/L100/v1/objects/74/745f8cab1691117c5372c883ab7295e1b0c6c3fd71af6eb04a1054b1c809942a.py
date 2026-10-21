import sys
if sys.flags.optimize:raise RuntimeError("ordinary Python required")
import json,hashlib
from pathlib import Path
p=Path(__file__).resolve().parent
def verify(f,r):
 b=f.read_bytes()
 if len(b)!=r["bytes"] or hashlib.sha256(b).hexdigest()!=r["sha256"]:raise ValueError(str(f))
for r in json.loads((p/"manifest.json").read_text())["exports"]:verify(p/r["path"],r)
for r in json.loads((p/"dependencies.json").read_text()):verify(Path(r["path"]),r)
print("PASS_FROZEN_REVIEW_BINDINGS_NO_TARGET")
