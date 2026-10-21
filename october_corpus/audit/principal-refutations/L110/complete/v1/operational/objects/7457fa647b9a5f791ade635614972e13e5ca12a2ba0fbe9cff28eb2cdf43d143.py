from pathlib import Path
import importlib.util,json,hashlib,sys
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans');R=Path('/Users/sasha/medusa/math_compression');P=S/'geometry/suzuki_incidence/higher_obstructions'
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
assert not(P/'manifest.json').exists();c=m.Closure()
for part in ['geometry/suzuki_subgroups/preliminaries_review_adoption','geometry/suzuki_incidence/normalizer_restrictions_root_review']:c.packet(part)
for name in ['sources/catalogue_L110.pdf','sources/catalogue_L110.txt','sources/phase6_L110_page15.png','sources/phase6_L110_page16.png','sources/phase6_L110_page17.png']:c.add(S/name)
for name in ['research/case_study/phase5_suzuki_realization.md','research/case_study/phase5_suzuki_higher.md','research/case_study/phase5_suzuki_higher_audit.json']:c.add(R/name)
c.add(__file__)
(P/'dependencies.json').write_text(json.dumps(list(c.files.values()),indent=2)+'\n')
(P/'scope.json').write_text(json.dumps(dict(author='root',distinct_review='PENDING',native_pages=3,source_original='L110',claims=[
 dict(target='Constructions2,3,4 literal intersections including G_m',disposition='IMPOSSIBLE_BY_GROUP_ORDERS'),
 dict(target='Constructions2,3,4 intended full lattices',disposition='IMPOSSIBLE_R4_R5_R6_RESIDUES'),
 dict(target='Construction6 intended full lattice',disposition='IMPOSSIBLE_R8_RESIDUE'),
 dict(target='Construction1 intended full lattice and Section3.1 final R2 extension',disposition='IMPOSSIBLE_SPLIT_DIHEDRAL_ALIGNMENT')],qualification='Requires the full source-prescribed intersection pattern. No assertion about arbitrary tuples with only these abstract parabolic types; no independent all-rank completeness theorem.',whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None),indent=2)+'\n')
exports=[]
for p in sorted(P.rglob('*')):
 if p.is_file():
  b=p.read_bytes();exports.append(dict(path=str(p.relative_to(P)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
(P/'manifest.json').write_text(json.dumps(dict(status='AUTHOR_L110_FIVE_PRESCRIBED_CONSTRUCTION_OBSTRUCTIONS_PENDING_DISTINCT_REVIEW',exports=exports),indent=2)+'\n')
print(json.dumps(m.records.pin(P/'manifest.json')))
