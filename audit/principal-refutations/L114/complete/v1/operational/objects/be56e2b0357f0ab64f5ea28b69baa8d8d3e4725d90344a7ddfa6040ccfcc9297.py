from pathlib import Path
import importlib.util,json,hashlib,sys
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans');R=Path('/Users/sasha/medusa/math_compression');P=S/'geometry/suzuki_incidence/higher_split_family'
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
assert not(P/'manifest.json').exists()
c=m.Closure()
for name in ['geometry/suzuki_subgroups/preliminaries_review_adoption','geometry/suzuki_subgroups/rank_two_families_root_review','geometry/suzuki_incidence/normalizer_restrictions_root_review']:c.packet(name)
for p in ['sources/catalogue_L110.pdf','sources/catalogue_L110.txt','sources/phase6_L110_page16.png','sources/phase6_L110_page17.png']:c.add(S/p)
for p in ['research/case_study/phase5_suzuki_realization.md','research/case_study/phase7_suzuki_torus_families.md']:c.add(R/p)
c.add(__file__)
(P/'dependencies.json').write_text(json.dumps(list(c.files.values()),indent=2)+'\n')
(P/'scope.json').write_text(json.dumps(dict(author='root',distinct_review='PENDING',
 source='L110 fixed2000/2001 edition,Constructions5and7',native_pages=3,
 scope='Uniform standard-position family with explicit literal index/order corrections; no all-positions or all-families classification.',
 whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None),indent=2)+'\n')
exports=[]
for p in sorted(P.iterdir()):
 if p.is_file():
  b=p.read_bytes();exports.append(dict(path=p.name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
(P/'manifest.json').write_text(json.dumps(dict(status='AUTHOR_L110_CANONICAL_SPLIT_FAMILY_PENDING_DISTINCT_REVIEW',exports=exports),indent=2)+'\n')
print(json.dumps(m.records.pin(P/'manifest.json')))
