from pathlib import Path
import json,hashlib,shutil
S=Path('/Users/sasha/medusa/research/leemans');W=S/'reboot_20261013/L045_symplectic_upper_distinct';A=S/'corpus106_L045_symplectic_upper_v2';D=S/'corpus106_L045_symplectic_upper_independent_review'
def pin(p,path=None):
 b=p.read_bytes();return dict(path=path if path is not None else str(p.relative_to(S)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
if D.exists():raise RuntimeError('immutable review exists')
review=dict(status='ACCEPTED_SYMPLECTIC_UPPER_COMPONENT',author_manifest=pin(A/'manifest.json'),reviewer='/root/l044_resume',mathematics='Complete written uniform proof read and accepted under its explicit retained cover and acquired finite exceptions.',author='publication_recovery',root_contribution='Projective coset organization and identification of missing odd unitary overgroup disclosed by author.',reviewer_contribution='Requested explicit final two A1(q^2) bounds; exact one-paragraph v2 clarification only, no new proof or code.',replay='replay01/report.json',final_native='final_edition_report.json',independent='independent_receipt.json',scope={'whole_original_credit':0,'open_question_credit':0,'orthogonal_credit':0,'classification_reproved':False,'compression_or_Lean':False},live_handles=[])
save(W/'review.json',review)
bindings=[dict(namespace='study',**pin(A/'manifest.json'))]+[dict(namespace='study',**pin(A/x['path'])) for x in json.loads((A/'manifest.json').read_text())['exports']]+json.loads((A/'dependencies.json').read_text())['files']
for name in ['aschbacher_seitz_1976.pdf','aschbacher_seitz_corrections_1978.pdf','burness_thomas_2017.pdf','classical_work/bubboloni_spiga_weigel_2022.pdf','classical_work/source_native/as-02.png']:
 bindings.append(dict(namespace='study',**pin(S/'reboot_20261013/L045_work'/name),role='Documentary source read or viewed; upstream text is not redistributed in this review.'))
roots=dict(study=S,public=S.parents[1]/'math_compression',gap=Path('/opt/homebrew/bin/gap').resolve().parent.parent)
for x in bindings:
 a=pin(roots[x['namespace']]/x['path'],x['path'])
 if any(a[k]!=x[k] for k in ('bytes','sha256')):raise RuntimeError('binding '+x['path'])
save(W/'bindings.json',{'files':bindings})
shutil.copytree(W,D,ignore=shutil.ignore_patterns('__pycache__','*.aux','*.out'))
exports=[pin(p,str(p.relative_to(D))) for p in sorted(D.rglob('*')) if p.is_file()]
save(D/'manifest.json',dict(schema='frozen-distinct-review-v1',status=review['status'],exports=exports))
print(D/'manifest.json',hashlib.sha256((D/'manifest.json').read_bytes()).hexdigest(),len(exports),len(bindings))
