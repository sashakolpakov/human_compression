import sys
if sys.flags.optimize:raise RuntimeError("ordinary Python required")
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent
def check(p,r):
 b=p.read_bytes()
 if len(b)!=r["bytes"]or hashlib.sha256(b).hexdigest()!=r["sha256"]:raise ValueError(str(p))
m=json.loads((P/"manifest.json").read_text())
for r in m["exports"]:check(P/r["path"],r)
d=json.loads((P/"dependencies.json").read_text())
for r in d["bindings"]:check(Path(r["path"]),r)
print(json.dumps(dict(status="PASS_SCIENCE89_REGISTRATION_REVIEW_INTEGRITY",exports=len(m["exports"]),bindings=len(d["bindings"]))))
