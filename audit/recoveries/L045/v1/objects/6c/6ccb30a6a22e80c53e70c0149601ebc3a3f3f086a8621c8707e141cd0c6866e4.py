from pathlib import Path
import json,hashlib,shutil
S=Path('/Users/sasha/medusa/research/leemans');W=S/'reboot_20261013/L045_linear_unitary_distinct';A=S/'corpus106_L045_linear_unitary_v1';D=S/'corpus106_L045_linear_unitary_independent_review'
def pin(p,path=None):
 b=p.read_bytes();return dict(path=path if path is not None else str(p.relative_to(S)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
if D.exists():raise RuntimeError('immutable review exists')
review=json.loads((W/'review.json').read_text())
bindings=[dict(namespace='study',**pin(A/'manifest.json'))]+[dict(namespace='study',**pin(A/x['path']))for x in json.loads((A/'manifest.json').read_text())['exports']]+json.loads((A/'dependencies.json').read_text())['files']
for p in [S/'reboot_20261013/L045_work/lawther_liebeck_seitz_2002.pdf',S/'reboot_20261013/L045_work/classical_work/bubboloni_spiga_weigel_2022.pdf',S/'reboot_20261013/L045_work/classical_work/source_native/ll-03.png',S/'reboot_20261013/L045_work/classical_work/source_native/lls-02.png']:
 bindings.append(dict(namespace='study',**pin(p),role='documentary source read or viewed; full upstream bytes not redistributed by review'))
roots=dict(study=S,public=S.parents[1]/'math_compression',gap=Path('/opt/homebrew/bin/gap').resolve().parent.parent)
for x in bindings:
 actual=pin(roots[x['namespace']]/x['path'],x['path'])
 if any(actual[k]!=x[k]for k in ['bytes','sha256']):raise RuntimeError('review binding mismatch '+x['path'])
save(W/'bindings.json',dict(files=bindings))
save(W/'independent_receipt.json',dict(status='PASS_INDEPENDENT_PGO4',command=['/opt/homebrew/bin/gap','-q','-T',str(W/'independent_orthogonal.g')],terminal_session=28352,stdout=pin(W/'independent_orthogonal.stdout'),stderr=pin(W/'independent_orthogonal.stderr'),row_fields=['q','PGL2q2_order','extension_order','minus_involutions','outer_involutions','wreath_order','plus_involutions'],rows=[[3,720,1440,111,30,1152,123],[5,15600,31200,755,130,28800,795]],no_author_imports=True))
save(W/'review_preparation.json',dict(initial_failure='Initial review binding helper tried to render a public-namespace path relative to the private study. It failed before creating the frozen review; corrected helper retains each explicit namespace/path.',author_bytes_unchanged=True,mathematics_unchanged=True))
shutil.copytree(W,D,ignore=shutil.ignore_patterns('__pycache__','*.aux','*.out'))
exports=[pin(p,str(p.relative_to(D)))for p in sorted(D.rglob('*'))if p.is_file()]
save(D/'manifest.json',dict(schema='frozen-distinct-review-v1',status=review['status'],exports=exports))
print(D/'manifest.json',hashlib.sha256((D/'manifest.json').read_bytes()).hexdigest(),len(exports),len(bindings))
