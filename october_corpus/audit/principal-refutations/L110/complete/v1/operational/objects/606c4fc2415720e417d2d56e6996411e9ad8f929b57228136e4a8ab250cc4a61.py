from pathlib import Path
import sys,json,hashlib,shutil,importlib.util
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans');W=S/'geometry/suzuki_subgroups/preliminaries'
if(W/'manifest.json').exists():raise ValueError('fresh freeze')
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.Closure();c.packet('corpus106_L115_scalar_subspaces_root_adoption')
for p in [S/'sources/older_L115_emis.pdf',S/'sources/older_L115_emis.txt',S/'corpus106_L115_scalar_subspaces_v1/central_covers.tex',Path(__file__)]:c.add(p)
for i in range(1,5):c.add(Path(f'/private/tmp/l115-source-{i:02}.png'))
c.add(Path('/private/tmp/l115_cyclic_diagnostic01.g'))
r=json.loads((W/'author02/receipt.json').read_text())
if not all(q['passed']for q in r):raise ValueError('small controls')
if b'PASS_L115_PRELIMINARY_CONTROLS CYCLIC_ACTIONS 34' not in(W/'author02/groups.stdout').read_bytes()or(W/'author02/groups.stderr').read_bytes():raise ValueError('exact group marker')
if 'Overfull' in(W/'native03/preliminaries.log').read_text():raise ValueError('layout')
if(W/'preliminaries.tex').read_bytes()!=(W/'native03/preliminaries.tex').read_bytes():raise ValueError('final text')
(W/'dependencies.json').write_text(json.dumps(list(c.files.values()),indent=2)+'\n')
(W/'scope.json').write_text(json.dumps(dict(author='root',status='AUTHOR_COMPLETE_AWAITING_DISTINCT_REVIEW',original='L115',source_statements=['Lemma3.'+str(i)for i in range(1,8)]+['Lemma5.'+str(i)for i in range(1,4)]+['Lemma6.1'],source_statement_count=11,pages=5,scope='Surviving preliminary results only; all remaining source claims stay unpaid.',literal_domain_correction='Lemma3.2 needs a proper subfield: q=s^r with s>2 and r>1.',borrowed=['Classical Suzuki root-group and faithful matrix realization','Classical ovoid action','Suzuki maximal-subgroup classification'],new_question_credit=0,whole_original_credit=0,new_Lean=0,measurement=None,priority_claim=False),indent=2)+'\n')
exports=[]
for p in sorted(W.rglob('*')):
 if p.is_file():
  b=p.read_bytes();exports.append(dict(path=str(p.relative_to(W)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
(W/'manifest.json').write_text(json.dumps(dict(status='AUTHOR_COMPLETE_L115_PRELIMINARY_RESULTS_AWAITING_DISTINCT_REVIEW',exports=exports,author='root',whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None),indent=2)+'\n')
b=(W/'manifest.json').read_bytes();print(json.dumps(dict(path=str(W/'manifest.json'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest(),exports=len(exports),dependencies=len(c.files))))
