"""Record the fixed N012 principal contract; this grants no admission."""
from pathlib import Path
import hashlib
import json
import re
import sys

if sys.flags.optimize:
    raise RuntimeError('Run without Python optimization')

S = Path(__file__).resolve().parent.parent
P = Path(__file__).resolve().parent

def pin(path):
    p = S / path
    b = p.read_bytes()
    return {'path': path, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def write(name, value):
    (P / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

components = {
 'I': {'proof': 'corpus106_N012_integral_v1/integral_groups.tex',
       'author': 'corpus106_N012_integral_v1/manifest.json',
       'review': 'corpus106_N012_integral_independent_review/manifest.json',
       'adoption': 'corpus106_N012_integral_root_adoption/manifest.json',
       'status': 'accepted component'},
 'U': {'proof': 'corpus106_N011_recovery/root_parameters.tex',
       'author': 'corpus106_N011_recovery/manifest.json',
       'review': 'corpus106_N011_root_review/manifest.json',
       'status': 'accepted common proof'},
 'L': {'proof': 'corpus106_N011_recovery/linear_classification.tex',
       'author': 'corpus106_N011_recovery/manifest.json',
       'review': 'corpus106_N011_root_review/manifest.json',
       'status': 'accepted application; substitute I for its retained integral premise'},
 'Z': {'proof': 'corpus106_N012_central_quotients_v1/central_quotients.tex',
       'author': 'corpus106_N012_central_quotients_v1/manifest.json',
       'review': 'corpus106_N012_central_quotients_independent_review/manifest.json',
       'adoption': 'corpus106_N012_central_quotients_root_adoption/manifest.json',
       'status': 'accepted component'},
 'H': {'proof': 'corpus106_N012_finite_H_v2/finite_H.tex',
       'author': 'corpus106_N012_finite_H_v2/manifest.json',
       'review': 'corpus106_N012_finite_H_independent_review/manifest.json',
       'adoption': 'corpus106_N012_finite_H_root_adoption/manifest.json',
       'status': 'accepted component, final v2'},
 'Q': {'proof': 'corpus106_N012_quotient_completion_v1/quotients_and_classification.tex',
       'author': 'corpus106_N012_quotient_completion_v1/manifest.json',
       'status': 'frozen candidate pending separate distinct review; not an acquired premise of this audit'}
}

rows = []
def claim(label, pages, hypotheses, conclusion, route, qualification='', status='ROUTE_AVAILABLE_FROM_ACCEPTED_COMPONENTS'):
    rows.append(dict(source_label=label, printed_pages=pages,
                     hypotheses=hypotheses, principal_conclusion=conclusion,
                     route=route, qualification=qualification, status=status))

claim('Theorem 2.2.1', [20,23,29], 'Integer matrices; intended n>=2.',
      'GL_n(Z) admissible iff n>=5; PGL_n(Z) admissible iff n=2 or n>=5.',
      ['I: final theorem and Sections 1–4, including both n=2 cases and all n>=5 words.'],
      'PSL_3(2) and PSL_4(2) nonadmissibility are explicitly retained external inputs. No rank-three polytope conclusion over Z is asserted by this theorem.')
claim('Theorem 3.2.1', [30,35,36,37,38], 'Finite field q; intended n>=2.',
      'GL_n(q) admissible iff [q=2 and (n=2 or n>=5)] or [q=3 and n>=5].',
      ['L: Theorem labelled gl, Section 2.',
       'I supplies L\'s previously retained integral existence premise for reduction modulo 3.',
       'U supplies the complete symmetric-square obstruction for GL_4(3).'],
      'All q>=4 excluded by determinants; all n=3,4 excluded; GL_2(3) excluded directly. Source Table 1 is exactly these six cases.')
claim('Theorem 3.2.2', [30,38,39], 'Finite field q; intended n>=2.',
      'GL_n(q) is a rank-three regular-polytope group iff q in {2,3} and n>=5.',
      ['L gives the complete admissibility exclusion list.',
       'For q=3, GL_n(3)=H_n(3); H Theorem 1 gives generation and the actual intersection property.',
       'For q=2, GL_n(2)=PSL_n(2) is simple for n>=5; retained simple admissibility and Conder–Oliveros give a marking.',
       'GL_2(2)=S3 has no distinct commuting involutions and hence no rank-three C-marking.',
       'Q Section 3 writes this complete assembly; its distinct review is pending.'],
      'This is not a consequence of reducing integral generators alone. The replacement does not claim the precise source GL_6(3) marking or its pair orders 24 and 12.',
      'ROUTE_MAPPED_NEW_ASSEMBLY_REVIEW_PENDING')
claim('Theorem 3.3.1', [30,39,40,41,51], 'Finite field q; intended n>=2; d=gcd(n,q−1).',
      'PGL_n(q) admissible iff n=2, or n>=4 and d=2, or n>=5 and d=1.',
      ['L: Theorem labelled pgl, Section 5, acquiring Sections 2–4 and U.',
       'I replaces the old integral input in the q=3,n=6 reuse branch.'],
      'For n=2 all q are positive, including q=2 by repeated marks. For n>=3, d>2 is excluded by the cyclic determinant quotient; n=3 is always negative; n=4,d=1 is negative. Source Table 2 is exactly these six cases.')
claim('Corollary 3.3.1', [30,52], 'Finite field q; intended n>=2; d=gcd(n,q−1).',
      'PGL_n(q) is a rank-three regular-polytope group iff n=2 and q!=2, or n>=4 and d=2, or n>=5 and d=1.',
      ['L: Section 5, paragraph following its two classification tables.',
       'Q Section 3 repeats the exact parameter route and explicitly supplies the S3 exclusion.'],
      'PGL_2(3)=S4 is not almost simple and is treated separately. For the other positive cases the simple-socle centralizer argument rules out cyclic normal subgroups. No blanket almost-simple assertion is retained.')
claim('Theorem 4.2.1', [53,56,57,67], 'Odd prime power q; intended n>=2; H_n(q)={g:det(g)=±1}.',
      'H_n(q) admissible iff n>=5.',
      ['H: Theorem 1, all constructions in Sections 1–4.',
       'Z: Theorem labelled small gives the complete n=2,3,4 exclusions using U.'],
      'The characteristic-two sentence before the source theorem is background attributed to previous work, not an additional principal classification in this thesis.')
claim('Theorem 4.2.2', [53,68,69], 'Odd q=p^m; intended n>=2.',
      'H_n(q) is a rank-three regular-polytope group iff n>=5; for every n>=5 a type [4p,n] or [4p,2n] occurs.',
      ['H: Theorem 1 and Section 5, complete monomial-intersection calculation and exact product orders.',
       'Z: n=2,3,4 nonadmissibility also excludes polytopes.'],
      'The disjunction of types means at least one displayed construction of one of those types; it is not a classification of all possible types, nor a claim both types occur for every parameter.')
claim('Corollary 4.2.1', [69,70], 'Odd q=p^m; even n>=6; Z1=Z(H_n(q)); d=gcd(n,q−1), e=(q−1)/d.',
      'The full-centre quotient has a rank-three regular polytope of type [4p,n]. The printed universal isomorphism to PSL_n(q) semidirect C2 requires correction.',
      ['Z: Theorem labelled centres: H/Z1=PSL_n(q) for e even; H/Z1 embeds as PSL_n(q) semidirect C2 for e odd.',
       'H: Theorem 2 with S=Z1 gives the type [4p,n] in both cases.',
       'Q: final section records precisely this corrected principal disposition.'],
      'Source p69 falsely states Z1=Z2 for every even n. At n=6,q=5, 2I has determinant −1, |Z1|=4 and |Z2|=2. This is a correction to a numbered corollary, not just a harmless intermediate typo.',
      'CORRECTED_PRINCIPAL_ROUTE_AVAILABLE')
claim('Corollary 4.2.2', [70], 'Odd q=p^m; odd n>=5; Z1=Z(H_n(q)).',
      'H_n(q)/Z1 is PSL_n(q), with a rank-three regular polytope of type [4p,n].',
      ['Z: Theorem centres; odd n makes e even.', 'H: Theorem 2 with S=Z1.'],
      'The source corollary uses the full centre Z1. It must not be swapped with Corollary 4.2.3, which uses Z2.')
claim('Corollary 4.2.3', [70], 'Odd q=p^m; odd n>=5; Z2=Z(SL_n(q)).',
      'H_n(q)/Z2 is PSL_n(q) × C2, with a rank-three regular polytope of type [4p,n] or [4p,2n].',
      ['Z: Theorem centres; the central factor is represented by −I.', 'H: Theorem 2 with S=Z2.'],
      'No almost-simple criterion is applied to this direct product. Its cyclic normal factor makes that criterion inapplicable; the actual quotient intersection proof supplies the asserted types.')
claim('Theorem 4.3.1', [53,70,71,72,73,74,75], 'Odd q; intended n>=2; Q_n(q)=H_n(q)/Z(SL_n(q)).',
      'Q_n(q) admissible iff n=2 and q!=9, or n>=4.',
      ['Q: Lemma 1 and Theorem 2 close n=2,3; distinct review pending.',
       'Z: Theorem qfour supplies every odd field in n=4.',
       'H: Theorem 2 with S=Z2 supplies all n>=5.'],
      'For n=2, q=7 is positive through PGL_2(7), despite PSL_2(7) being excluded. q=9 is negative via its PSL_2(9) quotient. All n=3 are negative. The defective source beta on p72 is replaced by the reviewed N011 construction.',
      'SMALL_QUOTIENT_COMPONENT_REVIEW_PENDING')
claim('Corollary 4.3.1', [53,75], 'Odd q; intended n>=2; Q_n(q)=H_n(q)/Z(SL_n(q)).',
      'Q_n(q) is a rank-three regular-polytope group iff n=2 and q!=9, or n>=4.',
      ['Q: Lemma 1 and Theorem 2, with the actual central-lift proof from Z; distinct review pending.',
       'Z: qfour covers n=4 without asserting every displayed triple has IP in the direct-product case.',
       'H: actual scalar-quotient marking covers n>=5.'],
      'The source blanket invocation of Lemma 1.3.2 cannot cover Q when it has a central C2. Use the perfect-group central lift or H\'s direct quotient intersection proof.',
      'SMALL_QUOTIENT_COMPONENT_REVIEW_PENDING')

tables = [
 {'source_table': 1, 'printed_page': 35, 'principal_label': 'Theorem 3.2.1',
  'rows': [['n=2,q=2',True],['n=2,q!=2',False],['n=3,any q',False],['n=4,any q',False],['n>=5,q=2 or 3',True],['n>=5,q!=2,3',False]],
  'route': 'L Section 5 first table, deduced from Theorem gl'},
 {'source_table': 2, 'printed_page': 40, 'principal_label': 'Theorem 3.3.1',
  'rows': [['n=2,any q',True],['n=3,any q',False],['n>=4,gcd(n,q−1)>2',False],['n>=4,gcd(n,q−1)=2',True],['n=4,gcd(n,q−1)=1',False],['n>=5,gcd(n,q−1)=1',True]],
  'route': 'L Section 5 second table, deduced from Theorem pgl'}
]

support = [
 {'source': 'Lemmas 1.1.1–1.1.2', 'role': 'Quotient closure and primitive-square field generation.', 'route': 'L Section 1; U primitive-square lemma.'},
 {'source': 'Lemmas 1.2.1–1.2.2', 'role': 'Symmetric-square representation and Scott obstruction.', 'route': 'Complete U proofs; reused by L and Z.'},
 {'source': 'Lemmas 1.3.1–1.3.6', 'role': 'Previously published polytope criteria/correspondence, with source hypotheses.', 'route': 'Retain Conder–Oliveros and group–polytope correspondence explicitly. S3 is excluded directly. No new proof of every cited criterion is claimed.'},
 {'source': 'Lemmas 2.1.1–2.1.5', 'role': 'Integral elementary generation, matrix words and finite quotient reductions.', 'route': 'I gives the actual elementary/root argument and reductions needed by its theorem; external PSL3(2)/PSL4(2) exclusions remain explicit.'},
 {'source': 'Lemmas 3.1.1–3.1.4', 'role': 'Lifting a quotient generating set, determinant section, scalar splitting and reduction modulo p.', 'route': 'L Sections 1–2.'},
 {'source': 'Lemmas 3.1.5–3.1.6', 'role': 'Root propagation and finite root-parameter recognition.', 'route': 'U complete proofs; then L Sections 3–4.'},
 {'source': 'Lemma 3.1.7', 'role': 'Borrowed rank-two Dickson/Levchuk statements.', 'route': 'Not a premise of the replacement root proof or the Q small-quotient route. Do not claim a fresh proof of these background statements.'},
 {'source': 'Lemma 3.1.8', 'role': 'No involution generation when gcd(n,q−1)>2.', 'route': 'L cyclic determinant quotient argument proves the needed statement directly.'},
 {'source': 'Lemmas 4.1.1–4.1.2', 'role': 'Finite root recognition/propagation used by the source.', 'route': 'Actual constructive hypotheses are supplied by U and H; no claim all literal intermediate formulations are recovered verbatim.'},
 {'source': 'Lemmas 4.1.3–4.1.4', 'role': 'Signed cycle product orders and the two-dimensional centre split.', 'route': 'H explicit monomial product orders; Z complete centre theorem and Q small-quotient argument.'}
]

contract = {
 'status': 'COMPLETE_PRINCIPAL_SOURCE_CONTRACT_MAP_NOT_ADMISSION',
 'original': 'N012',
 'source': {'author': 'Irina Alexandrovna Markovskaya', 'supervisor': 'Yakov Nifantievich Nuzhin', 'year': 2025,
            'title': 'Linear groups over finite fields and over the ring of integers as automorphism groups of regular polytopes of rank 3',
            'edition_pages': 80, 'pdf': pin('sources/phase22_markovskaya_thesis.pdf'), 'text': pin('sources/phase22_markovskaya_thesis.txt')},
 'domain': 'n>=2, the intended domain fixed by both source tables and all case analyses; finite q is a prime power, odd q throughout the new Chapter 4 classifications.',
 'definitions': {'admissible': 'Three involutions with a commuting pair, allowing repetitions and the trivial group as in source p11; equivalent operationally to order-at-most-two marks.',
                 'H': 'determinant in {1,−1}', 'Q': 'H/Z(SL), source PGL^{±1}', 'Z1': 'full centre of H', 'Z2': 'centre of SL',
                 'polytope': 'Rank-three abstract regular polytope, hence three distinct nonidentity string C-generators and the intersection property.'},
 'components': components, 'principal_claims': rows, 'classification_tables': tables, 'supporting_material': support,
 'pending_before_whole_admission': ['Distinct review and root adoption of Q.', 'Whole-source assembly/review binding all 12 routes, exact correction and complete acquired proofs.', 'Portable evidence assembly and public registration.'],
 'credit': {'whole_original': 0, 'new_question': 0, 'Lean': 0, 'compression_factor': None},
 'boundary': 'This is a source-to-proof audit. It does not replace a distinct mathematical review or grant acceptance to the pending Q component.'
}

edges = [
 ['external finite PSL3(2)/PSL4(2) exclusions','I'],
 ['I','L: GL(q=3) reduction and its n6(q=3) projective branch'],
 ['U','L'], ['U','Z'], ['L: degree4 matrix-generation proof only','Z'],
 ['U','H'], ['L: degree6 Laurent identities only','H'], ['Z: small H obstruction','H'],
 ['L','Q'], ['Z','Q'], ['H','Q'],
 ['I','whole N012'], ['L','whole N012'], ['Z','whole N012'], ['H','whole N012'], ['Q after acceptance','whole N012']
]
write('principal_ledger.json', contract)
write('dependency_routes.json', {'edges': edges, 'acyclic_order': ['external inputs','I and U','L','Z','H','Q after acceptance','whole N012'],
      'integral_substitution': 'The frozen N011 prose is preserved. The new wrapper explicitly substitutes complete I for its external integral premise, with no dependency of I on the GL finite classification.',
      'external_inputs': ['Explicit finite simple-linear admissibility classification, including the required n2 cases in Q.', 'Sjerve–Cherkassoff PGL2(q) admissibility.', 'Conder–Oliveros criterion and the string C-group/polytope correspondence.'],
      'external_costs': 'Full external proof/software costs remain unknown, not zero.'})

text = (S / 'sources/phase22_markovskaya_thesis.txt').read_text()
observed = set()
for kind, label in re.findall(r'(Теорема|Следствие)\s+(\d+\.\d+\.\d+)', text):
    observed.add(('Theorem' if kind=='Теорема' else 'Corollary')+' '+label)
expected = {x['source_label'] for x in rows}
if observed != expected or len(rows)!=12:
    raise RuntimeError(f'Principal label mismatch: {observed ^ expected}')
for c in components.values():
    for k in ('proof','author','review','adoption'):
        if k in c and not (S/c[k]).is_file():
            raise RuntimeError(c[k])
if len(tables)!=2 or any(len(t['rows'])!=6 for t in tables):
    raise RuntimeError('Table coverage mismatch')

bindings = {'sources/phase22_markovskaya_thesis.pdf','sources/phase22_markovskaya_thesis.txt',
            'corpus106_N011_recovery/retained_inputs.json','corpus106_N011_root_review/review.rst',
            'phase22_linear_priority_supplement.json'}
for c in components.values():
    for k in ('proof','author','review','adoption'):
        if k in c: bindings.add(c[k])
for folder in ('corpus106_N012_integral_v1','corpus106_N012_finite_H_v2','corpus106_N012_central_quotients_v1','corpus106_N012_quotient_completion_v1'):
    for name in ('scope.json','dependencies.json'):
        if (S/folder/name).is_file(): bindings.add(f'{folder}/{name}')
for folder in ('corpus106_N012_integral_root_adoption','corpus106_N012_finite_H_root_adoption'):
    bindings.add(f'{folder}/adoption.json')
write('evidence.json', {'bindings': [pin(p) for p in sorted(bindings)],
                       'page_extractions': [pin(str(p.relative_to(S))) for p in sorted(P.glob('source_page_*.txt'))],
                       'reading_boundary': 'This audit read all principal source statements, introduction/conclusion and relevant actual theorem/support pages. It does not claim a new reading of all 80 pages. Complete component reviews remain separately acquired.'})
write('check_report.json', {'status':'PASS_SOURCE_CONTRACT_COMPLETENESS', 'distinct_principal_labels':len(observed),
      'principal_labels':sorted(observed), 'classification_tables':2, 'table_rows':12,
      'all_component_locators_exist':True, 'source_bindings_verified':True,
      'component_acceptance_checked_from_bound_records':True,
      'closing_component_distinct_acceptance':'PENDING_AT_AUDIT',
      'no_public_mutation':True, 'no_new_admission':True})
print(json.dumps({'principal_labels': len(observed), 'tables':len(tables), 'bindings':len(bindings), 'status':'PASS_SOURCE_CONTRACT_COMPLETENESS'}))
