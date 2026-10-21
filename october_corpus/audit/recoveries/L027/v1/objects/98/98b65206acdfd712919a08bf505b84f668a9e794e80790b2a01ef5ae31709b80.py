from pathlib import Path
import hashlib,json,shutil
S=Path('/Users/sasha/medusa/research/leemans');W=S/'reboot_20261013/L027_table_one_work';O=S/'corpus106_L027_table_one_v1'
def pin(p):b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
if O.exists():raise RuntimeError('immutable packet exists')
O.mkdir()
for n in ['table_one.tex','table_one.pdf','table_one.py','check.py','prepare.py']:shutil.copy2(W/n,O/n)
shutil.copy2(W/'table02.json',O/'expected.json')
write(O/'scope.json',dict(original='L027',claim='Every necessary parameter cell of sourceTable1, plus correction b to aprime in last characteristic polynomial',status='AUTHOR_COMPLETE_AWAITING_DISTINCT_REVIEW',not_claimed=['IP from table arithmetic','Whole original recovery','New conjecture or Lean','Measurement'],native_pages=2,attribution='Source parameter choices and table are Leemans--Vandenschrick; exact elimination and field/root qualification here are l044_resume'))
(O/'development.rst').write_text('The initial arithmetic helper used sympy.ilcm with one argument in constant\nrows. It stopped before producing a report; retained table_one_initial.py.\nAdding initial argument1 repairs this API issue. All nine rows then passed.\nThe final control also computes all three literal characteristic polynomials.\nThe first native build had wide displays; final displays are split/shortened\nand both pages directly viewed. Source physical17 directly viewed. No new\ngroup census and no changes to accepted conic classification.\n')
paths=[S/'sources/psl3_chiral2022.pdf',W/'source-17.png',W/'table_one_initial.py',W/'table01.json',S/'corpus106_L027_odd_four_v2/manifest.json',S/'corpus106_L027_odd_four_v2/odd_four.tex',S/'corpus106_L027_odd_four_root_adoption/manifest.json']
write(O/'dependencies.json',[pin(p) for p in paths]);exports=[]
for p in sorted(O.iterdir()):x=pin(p);x['path']=p.name;exports.append(x)
write(O/'manifest.json',dict(status='AUTHOR_COMPLETE_AWAITING_DISTINCT_REVIEW',exports=exports));print(pin(O/'manifest.json'))
