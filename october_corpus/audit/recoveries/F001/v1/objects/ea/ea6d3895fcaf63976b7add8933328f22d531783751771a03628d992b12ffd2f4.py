from pathlib import Path
import json,hashlib,datetime,shutil
S=Path('/Users/sasha/medusa/research/leemans');A=S/'corpus106_F001_reflection_bound_v1';W=S/'reboot_20261013/F001_reflection_distinct';D=S/'corpus106_F001_reflection_bound_independent_review'
assert not D.exists();D.mkdir()
def pin(p):
 b=p.read_bytes();return dict(path=str(p.relative_to(S)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
assert pin(A/'manifest.json')['sha256']=='abf325a642a8f6dad4157edd6fc47fc8e0a439f93cf341960b3a5fcc44941061'
shutil.copyfile(W/'review.rst',D/'review.rst');shutil.copyfile(W/'replay01/report.json',D/'replay_report.json')
write(D/'review.json',dict(status='ACCEPTED_BOUNDED_NEGATIVE_REFLECTION_RANK_BOUND',reviewer='publication_recovery',author='f003_resume',author_manifest=pin(A/'manifest.json'),read_complete_uniform_proof=True,read_classification_specialization=True,primary_native_pages_directly_viewed=[15,16,17,18,19],new_native_pages_directly_viewed=[1,2,3,4],new_proof_authorship_by_reviewer=False,reviewer_mixed_involution_notes_are_not_premises=True,mixed_involutions_covered=False,whole_original_credit=0,new_conjecture_credit=0,new_Lean_credit=0,new_measurement_credit=0,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
paths=[S/x['path']for x in json.loads((A/'dependencies.json').read_text())['bindings']]+[p for p in A.iterdir()if p.is_file()]+[W/'freeze_review.py',W/'review.rst']+[p for p in (W/'replay01').rglob('*')if p.is_file()]+[p for p in (W/'source_pages').iterdir()if p.is_file()]
write(D/'dependencies.json',dict(bindings=[pin(p)for p in {str(p):p for p in paths}.values()]))
write(D/'manifest.json',dict(status='FROZEN_DISTINCT_BOUNDED_REVIEW',exports=[{**pin(p),'path':p.name}for p in sorted(D.iterdir())if p.is_file()]))
print(json.dumps(pin(D/'manifest.json')))
