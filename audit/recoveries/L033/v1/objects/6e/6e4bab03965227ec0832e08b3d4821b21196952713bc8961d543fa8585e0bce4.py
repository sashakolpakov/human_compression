import sys
if sys.flags.optimize:raise RuntimeError('Normal Python is required')
from pathlib import Path
import json,hashlib,shutil
S=Path('/Users/sasha/medusa/research/leemans');R=Path('/Users/sasha/medusa/math_compression');W=S/'reboot_20261013/L033_euclidean_work';O=S/'corpus106_L033_translation_kernel_v1'
def need(b,m):
 if not b:raise ValueError(m)
def h(p):
 b=p.read_bytes();return dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
need(not O.exists(),'fresh immutable author packet');O.mkdir()
for n in ['translation_kernel.tex','translation_kernel.pdf','commutators.py','commutators.json','check.py','source_map.json','reuse_inventory.json','scope.json','freeze.py']:
 shutil.copyfile(W/n,O/n)
deps={}
def add(p):
 r=dict(path=str(p),**h(p));old=deps.get(str(p));need(old is None or old==r,'unique bound edition');deps[str(p)]=r
for name in ['corpus106_L052_residue_theory_v1','corpus106_L052_residue_theory_independent_review','corpus106_L052_residue_theory_root_adoption','corpus106_L033_quotient_kernels_v1','corpus106_L033_quotient_kernels_independent_review','corpus106_L033_quotient_kernels_root_adoption']:
 P=S/name;add(P/'manifest.json')
 for r in json.loads((P/'manifest.json').read_text())['exports']:
  p=P/r['path'];need(h(p)=={k:r[k]for k in ['bytes','sha256']},'acquired manifest unchanged');add(p)
 if (P/'dependencies.json').exists():
  for r in json.loads((P/'dependencies.json').read_text()):
   p=Path(r['path']);p=p if p.is_absolute()else S/p
   need(h(p)=={k:r[k]for k in ['bytes','sha256']},'acquired dependency unchanged');add(p)
for n in ['sources/catalogue_L033.pdf','sources/catalogue_L033.txt']:add(S/n)
for n in ['papers/topic-affine/v2/sections/02-squares.tex','papers/topic-a/extensions/hexagonal/v1/inputs/base/shared_sections/01-local-kernels.tex','papers/topic-c/extensions/generalized-halving/v1/sections/20-affine-groups.tex','papers/topic-c/extensions/generalized-halving/v1/sections/30-iterated-geometry.tex','papers/topic-c/extensions/generalized-halving/v1/PUBLICATION.rst','audit/topic-c/extensions/generalized-halving/v1/admission.json','papers/topic-a/extensions/locally-toroidal/v1/sections/02-square.tex','papers/topic-a/extensions/locally-toroidal/v1/PUBLICATION.rst','audit/topic-a/extensions/locally-toroidal/v1/admission.json','papers/topic-a/extensions/hexagonal/v1/README.rst']:
 add(R/n)
(O/'dependencies.json').write_text(json.dumps(list(deps.values()),indent=2)+'\n')
exports=[dict(path=str(p.relative_to(O)),**h(p))for p in sorted(O.iterdir())if p.is_file()]
(O/'manifest.json').write_text(json.dumps(dict(schema='human-compression-author-v1',status='AUTHOR_TRANSLATION_KERNEL_REVIEW_PENDING',exports=exports),indent=2)+'\n')
print(json.dumps(dict(path=str(O/'manifest.json'),sha256=h(O/'manifest.json')['sha256'],exports=len(exports),dependencies=len(deps))))
