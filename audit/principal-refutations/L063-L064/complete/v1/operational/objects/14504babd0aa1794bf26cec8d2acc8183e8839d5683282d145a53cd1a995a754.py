from pathlib import Path
import hashlib, importlib.util, json, sys
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans')
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def require(condition,message):
    if not condition: raise ValueError(message)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

for name,author,review,digest,status,notes in [
 ('q9_geometry_root_adoption','q9_geometry','q9_geometry_independent_review','f8f9260b66df75f615008e8e8ef22dd48f2819e2b4bc53fd00c619f95a55b62a','ROOT_ADOPTED_L063_Q9_GEOMETRY_AND_FULL_AUTOMORPHISMS',[
  'Root authored the three-page proof; j3_recovery independently read the complete proof, literal reader and witness, rebuilt all three native pages, and inspected the two joined source pages. Root read the complete distinct review and replay report.',
  'The duad/syntheme model proves the generalized quadrangle axioms, girth eight and diameter four. The forty-five incidences and explicit type-reversing involution are verified literally. Sylow counting establishes the unique embedded configuration, conditional on the attributed classical subgroup theorem.',
  'The displayed S6 action and duality attain the Tutte upper bound 1440. The core and centralizer arguments identify the full group with the explicitly attributed Aut(A6), and its exact arc length is five. No whole-source, new refutation, conjecture, Lean or measurement credit.'
 ]),
 ('s4_automorphisms_root_adoption','s4_automorphisms','s4_automorphisms_distinct_review','3b6bdb4cee1994d163fd47a3e8a2e321baab673e71faf696d72756a41aec0970','ROOT_ADOPTED_L063_S4_FULL_AUTOMORPHISMS',[
  'Root and j3_recovery contributed to the proof. finite_recoveries supplied a distinct full mathematical review, fresh four-page native rebuild, direct proof/source inspection and exact source-page joins. Root read the whole proof and distinct review.',
  'The literal torus normalizer distinguishes the same-class and different-class S4 pairs. The same-class pair admits a central type reversal; the different-class pair has trivial centralizer. Tutte and the simple-group core argument bound and identify the full automorphism group.',
  'Four prime-field assertions, for p=17,31,47,79, are corrected to PSL2(p) times C2; the other five specified prime-field groups remain PGL2(p). Both configuration counts and exact arc length four are covered. The order-nine case is separate. No additional original or principal-refutation credit.'
 ])]:
    base='geometry/psl2_rank_two/'
    require(sha(S/base/review/'manifest.json')==digest,'Exact distinct review')
    c=m.Closure();c.packet(base+author);c.packet(base+review);c.add(__file__)
    c.finish(base+name,status,dict(status=status,author='root and j3_recovery' if name.startswith('s4') else 'root',distinct_reviewer='finite_recoveries' if name.startswith('s4') else 'j3_recovery',review=notes))

P=S/'geometry/suzuki_subgroups/publication_work'
require(sha(P/'integration02/manifest.json')=='e9e64e53b1bbfcf5c408842462337ccae9e6d602708f60ced1c6cdf255fcb6a6','Exact installer')
require(sha(P/'registration_candidate02/manifest.json')=='63c4ec8b8ba2b429451fbbec09f8149475c4ab52006f26e37d4bc52c4022dce7','Exact candidate')
for path,status in [('/private/tmp/l115_registration_candidate_root01.json','PASS_L115_REGISTRATION_CANDIDATE'),('/private/tmp/l115_install_inputs_root01.json','PASS_L115_INSTALLATION_INPUTS')]:
    require(json.loads(Path(path).read_text())['status']==status,'Fresh root check')
c=m.Closure()
for name in ['registration_handoff','registration_candidate02','integration02']:
    c.packet('geometry/suzuki_subgroups/publication_work/'+name)
c.packet('geometry/suzuki_subgroups/publication_operational_root_review')
for path in ['/private/tmp/l115_registration_candidate_root01.json','/private/tmp/l115_install_inputs_root01.json','/private/tmp/l115_protocol-01.png','/private/tmp/l115_protocol-02.png',__file__]:c.add(path)
status='ACCEPTED_L115_SOURCE_COMPLETION_REGISTRATION'
c.finish('geometry/suzuki_subgroups/publication_registration_root_review',status,dict(status=status,author='l070_publication',reviewer='root',review=[
 'Read the complete candidate checker, installer, finalizer and installed checker, and the README/completion/protocol deltas. Viewed both changed native protocol pages. Fresh root candidate and input checks pass.',
 'All 37,123 operational bindings are preserved, with 21,105 exact decoded scientific objects. The additional content-addressed route is bound to the already accepted transport and codec. Source and environment premises remain explicit and cannot supply missing scientific bytes. All four count and seven boundary damage controls reject.',
 'The only source completion is L115: 97 becomes 98, eight remaining becomes seven. The 92 ordinary treatments, nine principal refutations, 101 principal dispositions and 53 measured originals are unchanged. All 70 fixed-source claims have dispositions; eight complete manuscripts retain 36 proof pages, including the existing four-page correction once.',
 'The installer preserves replaced files before mutation. The finalizer follows exact predecessor history only for the explicitly declared old mutable paths and previous tracked manifest; all other review inputs retain their exact original bindings. This is a declared historical route, not a missing-input fallback.',
 'The installed preflight, final root gate, tracked manifest and snapshot verification remain required before commit. No new conjecture, Lean or compression factor is claimed.'
]))
