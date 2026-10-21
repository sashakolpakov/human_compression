from pathlib import Path
import sys,json,importlib.util
sys.dont_write_bytecode=True
S=Path('/Users/sasha/medusa/research/leemans');Q=S/'geometry/suzuki_subgroups'
spec=importlib.util.spec_from_file_location('flat',S/'reboot_20261013/component_adoption_flat_v2.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
c=m.Closure()
for p in ['subfield_families','subfield_families_distinct_review','subfield_families_corrected','subfield_families_corrected_distinct_review']:
 c.packet('geometry/suzuki_subgroups/'+p)
for row in json.loads((Q/'subfield_families_corrected_distinct_review/bindings.json').read_text()):c.binding(row)
old=(Q/'subfield_families/subfields.tex').read_text();new=(Q/'subfield_families_corrected/subfields.tex').read_text()
before=r'\Sz(2^e)&\Sz(2^{ep})&';after=r'\Sz(2^e)&\Sz(2^{er})&'
if old.count(before)!=1 or old.replace(before,after)!=new:raise ValueError('exact exponent correction')
r=json.loads((Q/'subfield_families_corrected_distinct_review/review.json').read_text())
if r['status']!='ACCEPTED_L115_CORRECTED_SUBFIELD_CLASSIFICATION_DISTINCT_REVIEW':raise ValueError('distinct gate')
c.add(Path(__file__))
c.finish('geometry/suzuki_subgroups/subfield_families_root_adoption','ACCEPTED_L115_SUBFIELD_EXHAUSTION_AND_CLASSIFICATION',dict(
 reviewer='root',author='l070_publication',distinct_reviewer='finite_recoveries',review=[
 'Root read the complete general proof before the distinct review, including the normalizer condition forcing each point-stabilizer cover into the central overgroup, other maximal-intersection cases, both fixed-line cases and the complete total formulas. Classical subgroup classification, partition, ovoid and automorphism inputs remain explicit.',
 'The distinct reviewer identified a displayed exponent error missed on the first root reading: the second simple subfield group must have exponent er rather than ep, which is the first group. The proof already derived er. The original author edition and changes-requested review are retained unchanged.',
 'The corrected edition changes exactly that one TeX occurrence. Root independently checked the exact delta, read the complete distinct proof review and correction review, and directly viewed the corrected native page3. The distinct reviewer compared all six PDF pages and acquired the original four literal orbit controls.',
 'The fixed-line formula treats both gcd cases without imposing coprimality of absolute and relative field degrees. The central covers are exhaustive, not merely examples. Prime torus extensions and unordered distinct subfield indices give the remaining families; the global formulas remove their duplicate descriptions.',
 'All252 declared correction-review bindings were freshly rebound. Source Table12 numerical rows and the29 small-group diagrams still require their separate joins; no whole-original, new-conjecture, Lean or compression credit is inferred.'
 ],source_lemma='6.9 corrected',global_classification=True,source_numerical_rows_pending=60,source_diagrams_pending=29,root_initial_review_missed_displayed_exponent=True,target_runs=0,source_credit=0))
