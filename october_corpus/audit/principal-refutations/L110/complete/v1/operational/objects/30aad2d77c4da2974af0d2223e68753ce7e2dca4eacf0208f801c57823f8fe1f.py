from pathlib import Path
import importlib.util,json,sys
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans');Y=S/'geometry/suzuki_incidence'
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
items=[('preliminary_scope','preliminary_scope_root01','preliminary_scope_root_review','ACCEPTED_L114_PRELIMINARY_STATEMENTS_AND_CORRECTIONS',[
 'Read the full three-page proof, exact arithmetic checker and source claim table. Viewed all three newly assembled native pages after fresh exact dependency/export and raster checks passed.',
 'The maximal-subfield count and prime quotient implications follow from the already accepted classical subgroup list and repunit argument. The gcd identity for odd exponents follows from the ordinary power gcd and coprimality with the minus factor.',
 'The four literal ancillary errors are distinguished from intended statements: maximal proper divisor rather than prime divisor, divisibility of field degrees rather than merely powers of two, residue variable e rather than2e+1, and extension within the compatible torus. The stated small exact witnesses and four rejected damages were freshly checked.',
 'For the extension lemma an involution has a unique cyclic order-four subgroup in its torus normalizer. The odd subgroup fixes the unique torus, and adjoining its unique larger cyclic subgroup gives the compatible extension. Proper-overgroup restrictions explicitly exclude the ambient group.',
 'The linear-diagram flag-transitivity theorem remains attributed to the cited prior work with its required geometric hypotheses. No general thinness, new principal refutation or whole-source credit follows.'
 ]),('remaining_markings_application','remaining_markings_root01','remaining_markings_root_review','ACCEPTED_L114_EIGHT_RETAINED_MARKINGS_AS_GEOMETRIES',[
 'Read the entire independent polynomial field reader, complete two-page application proof and fresh audit. Directly viewed both newly assembled native pages; exact dependency/export, native raster, eleven damaged-record and two optimization-guard checks passed.',
 'All eight prescribed recipes have the stated dihedral orders, exact pair/triple intersections and complete literal coset sets. The twenty-four actual panels each have two members, each with a common representative in the base pair intersection.',
 'Every edge translates to a base edge. The complete panel calculation therefore proves thinness and flag transitivity for these markings. Intersections generate each dihedral parabolic, and the full split normalizer is maximal, proving connectedness of residues and the ambient incidence graph.',
 'Prime indices verify every RWPRI subset. Algebraic local rank-one residues are regular two-point actions. These positive examples do not classify all relative positions or prove the source universal thinness assertion.',
 'The one permitted original acquisition is terminal. This independent result review uses only its saved bytes; it launches no new marking search.'
 ])]
for component,outname,acceptance,status,review in items:
 c=m.Closure();c.packet('geometry/suzuki_incidence/'+component)
 out=Y/outname;r=json.loads((out/'report.json').read_text());assert r['status'].startswith('PASS_L114_')
 for p in out.iterdir():
  if p.is_file():c.add(p)
 c.add(__file__)
 c.finish('geometry/suzuki_incidence/'+acceptance,status,dict(reviewer='root',author='j3_recovery',review=review,native_pages=r['native_pages'],source_credit=0))
