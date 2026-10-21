from pathlib import Path
import importlib.util,json,hashlib,sys
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans');Y=S/'geometry/suzuki_incidence';C=Y/'higher_families';O=Y/'higher_families_root01'
assert hashlib.sha256((C/'manifest.json').read_bytes()).hexdigest()=='728df83d4ee5746a9dd4ecce98a8681221e63ad59e2c3c41711f7b5d060939bb'
r=json.loads((O/'report.json').read_text());assert r['status']=='PASS' and sum(x['pages'] for x in r['native'])==18
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.Closure();c.packet('geometry/suzuki_incidence/higher_families');c.add(__file__)
for p in O.rglob('*'):
 if p.is_file():c.add(p)
status='ACCEPTED_L110_SURVIVING_FAMILIES_AND_CONDITIONAL_DIAGRAMS'
c.finish('geometry/suzuki_incidence/higher_families_root_review',status,dict(status=status,author='j3_recovery',reviewer='root',source_id='L110',whole_original_credit=False,review=[
 'Reviewed the reassembly program and editorial ledger for the three previously independently accepted proof notes. Their exact original hashes are acquired. The16 pages retain the existing descent, compatible-torus, torus-family, pure-subfield and scalar-obstruction arguments; these are reused results, not newly counted proofs.',
 'Fresh assembly check passed719 dependency and69 export bindings, rebuilt all four native manuscripts with the same18 pages and text, and rejected both damaged bindings and both optimized Python invocations. No finite group search was repeated.',
 'Read the complete new two-page diagram proof and viewed both freshly rendered native pages. Checked that the subgroup-product criterion uses standard rank-two residues only after flag transitivity identifies them with actual residues.',
 'For Constructions8 and9, the acquired cyclic intersection orders make all field-field residues digons. The two-parts t^2 and t^(2a_i) distinguish the torus-field residue product from the full Suzuki subgroup, giving exactly the star diagram.',
 'For corrected Constructions5 and7, checked all four residue types and product orders. The conclusion is explicitly conditional on flag transitivity; the maximality theorem is not misrepresented as proving that extra property.',
 'For pure subfields, checked the inequalities x^5/2<f(x)<x^5 for f(x)=x^2(x^2+1)(x-1), x>=2, and the resulting strict product inequality for distinct odd relative primes. The diagram is complete, including bottom field2 when relevant to the order computation.',
 'Impossible prescribed lattices and the scalar maximality failure are not restored by conditional diagram calculations. The source comment about almost all geometries lacks a counting measure and is not promoted to a theorem. Arbitrary embeddings and flag transitivity of corrected5/7 remain unresolved extensions. This component alone grants no whole-original, new refutation, Lean or compression credit.'
]))
