"""Bind existing private source bytes and the declared twelve-result intake.

No source files are modified. No manuscript-length numerator or ratio is computed.
This is a review-stage integrity/coverage artifact, not a mathematical checker.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'phase36_compress_forest_intake.json'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def binding(rel, kind, expected=None):
    data = (ROOT / rel).read_bytes()
    digest = sha(data)
    if expected is not None:
        assert digest == expected, (rel, digest)
    return {'path': rel, 'absolute_path': str(ROOT / rel), 'bytes': len(data),
            'sha256': digest, 'kind': kind}

def span(text, start, end, **extra):
    selected = text[start:end]
    return {'start_codepoint': start, 'end_codepoint_exclusive': end,
            'sha256_utf8': sha(selected.encode('utf-8')), **extra}

def located(text, first, after, **extra):
    start = text.index(first)
    end = text.index(after, start)
    return span(text, start, end, **extra)

n1_rel = 'sources/phase16_N001_browser_record.txt'
n3_rel = 'sources/phase10_N003_extracted.txt'
n1 = (ROOT / n1_rel).read_text()
n3 = (ROOT / n3_rel).read_text()
prior = json.loads((ROOT / 'phase12_N003_source_scope.json').read_text())
expected = {
 n1_rel: '222d5742392a4c40c0468d473bfba99b50f34a70eb0ac90200006314d3c5b207',
 n3_rel: '165ef2f20f7b5b3f04021205e002e0f22d2249b035bbc480de10f21986d14310',
 'sources/network_independent_generators.pdf': '43f3f2b1cbb7dacc55f12572ef78a5bb574bcfe745aba6cc0c10291256e611a2',
}
files = [binding(n1_rel, 'rendered_authored_primary_text_record', expected[n1_rel]),
 binding('sources/network_independent_generators.pdf', 'complete_author_manuscript_pdf', expected['sources/network_independent_generators.pdf']),
 binding(n3_rel, 'complete_page_marked_pdf_extraction', expected[n3_rel]),
 binding('sources/phase16_N001_academia.html', 'failed_direct_retrieval_challenge_not_primary_text'),
 binding('phase12_N003_source_scope.json', 'prior_private_source_scope_record'),
 binding('phase16_older_source_access.md', 'prior_private_access_report')]

n1_statement = located(n1, 'Theorem 1 If (Γ, G)', '2 Proof of the theorem',
 displayed_lines=[198,199], printed_pages=[216], role='complete_four_part_target_statement')
n1_main_candidate = located(n1, 'L181: Some properties', 'References [1]',
 displayed_lines=[181,216], role='candidate_authored_body_before_references_with_layout',
 approved_for_length_measurement=False,
 limits='Contains displayed line prefixes, printed page headers, footnote/address matter and corrupted diagram glyphs; a common body/word convention and independent review are still required.')
n1_authored = located(n1, 'L181: Some properties', 'L221: ## References',
 displayed_lines=[181,220], role='authored_text_including_bibliography_and_addresses')
n1_b97 = located(n1, 'We recall the main theorem of [3].', 'For example, we can start',
 displayed_lines=[193,194], role='retained_1997_classification_restatement')

formulations = [
 ('A1','N001','Theorem 1(1)', 'For every inductively minimal finite pair (Gamma,G), the pair is RWPRI and has properties (2T)_1 and (IP)_2.', ['B97','Coset','Elementary'], 'F, I, D', 'B97 plus D identifies the tree; I supplies all three residual/local properties.'),
 ('A2','N001','Theorem 1(2)', 'An inductively minimal pair of even rank is PRI.', ['B97','Coset','Elementary'], 'F, O, I, D', 'The tree has an odd number of vertices, so every cut is unbalanced.'),
 ('A3','N001','Theorem 1(3)', 'For an inductively minimal pair, failure of PRI implies QPRI; failure of PRI occurs exactly when the connected diagram has a middle (a nonend whose deletion components have equal cardinality).', ['B97','Coset','Elementary'], 'F, O, I, D', 'A diagram middle is exactly a balanced nonleaf cut; O identifies its unique subgroup chain.'),
 ('A4','N001','Theorem 1(4)', 'An inductively minimal pair is RPRI if and only if its diagram is a complete graph.', ['B97','Coset','Elementary'], 'F, O, I, D', 'Stars have only leaf cuts in their residues; every nonstar contains the obstructing three-edge path.'),
 ('B1','N003','Theorem 1.1', 'For a normal subgroup N of G, mu(G) <= mu(G/N)+mu_prime(N). If N is abelian, mu(G) <= mu(G/N)+mu_prime_G(N), with G acting on N by conjugation. The printed source says a group; this contract takes finite G.', ['Elementary'], 'R(a)', 'Choose a quotient-minimal subfamily and replace every remaining generator by an element of N; for abelian N conjugators can be taken in the chosen lift.'),
 ('B2','N003','Theorem 2.1', 'For n >= 7, every independent generating set S of S_n of size n-1 is S(T), the edge transpositions of a labelled tree T, or {s} union {(s t)^epsilon(t): t in S(T) except s}, where s in S(T) and epsilon(t) in {+1,-1}. Conversely every set of either form is an independent generating set of S_n.', ['W1','W2','Elementary'], 'F, P, R(a), M, E', 'M removes the imprimitive case; orbit-crossing edges yield a tree; F limits each generator support; P gives the converse.'),
 ('B3','N003','Corollary 2.2', 'For the two families of Theorem 2.1, the numbers of actual unordered generating sets are n^(n-2) and (n-1)n^(n-2), respectively; identifying each 3-cycle with its inverse changes the second count to binomial(n,2)(n-1)^(n-3). Degree n >= 7 is inherited from that theorem.', ['W1','W2','Cayley','Elementary'], 'F, P, M, E; B3 count adapter', 'Actual twisted sets recover a unique distinguished-edge tree by multiplication by the unique odd member; inverse identification contracts that edge.'),
 ('B4','N003','Corollary 2.3', 'For n >= 7 every independent generating set (s_i:i in I) of S_n of size n-1 is strongly independent: with G_J=<s_i:i not in J>, G_J intersect G_K = G_(J union K) for all J,K subsets of I.', ['W1','W2','Elementary'], 'F, P, M, E', 'Recognize the two markings and apply their exact subset formulas, including the empty subset.'),
 ('B5','N003','Corollary 2.4', 'For n >= 7 and B <= S_n, mu(S_n,B)=n-1 implies B=1.', ['W1','W2','Elementary'], 'F, P, O, M, E', 'Maximal omission subgroups contain B; a leaf cut forces a fixed point and excludes the half-swapping coset at a balanced cut.'),
 ('B6','N003','Theorem 3.1 and its immediately stated consequence', 'A source coset geometry for G with Borel B has rank <= mu_prime(G,B). An RWPRI source coset geometry has rank <= mu(G,B), and choices s_i in H_(I minus {i}) outside H_i form a strongly independent relative generating family. The printed source does not impose finite G; this contract takes finite G.', ['Coset','Elementary'], 'R(b)', 'Panel choices give relative independence; a residual maximal subgroup induction gives every parabolic and strong independence.'),
 ('B7','N003','Theorem 3.2', 'For n >= 7 there is a bijection between independent generating sets of S_n of size n-1, modulo simultaneous conjugation and inversion of individual generators, and RWPRI coset geometries for S_n of rank n-1. The specified group action is retained and set order/type labels may be renamed.', ['W1','W2','Coset','AutSn','Elementary'], 'F, P, O, R, M, E, G', 'F completes cut flags; parity is adjusted by the distinguished transposition; G proves every residue primitive in some type, and cyclic panels give uniqueness.'),
 ('B8','N003','Corollary 3.3', 'For n >= 7 every source coset geometry of S_n of rank n-1 is RWPRI, without an initial RWPRI hypothesis.', ['W1','W2','Coset','Elementary'], 'F, P, O, R, M, E, G', 'Only one balanced parabolic can enlarge; a second cut blocks half interchange in every panel; (G2) recovers all parabolics from those panels.')
]

targets=[]
for idx,(label,paper,ref,form,bg,common,adapter) in enumerate(formulations):
    item={'adapter':label,'paper':paper,'source_reference':ref,
          'full_source_formulation_normalized':form,
          'common_result':common,'adapter_argument':adapter,
          'imported_background_transitive_closure':bg,
          'mathematical_status':'written_corollary_pending_independent_review',
          'literal_or_scoped': 'finite_group_specialization' if label in ['B1','B6'] else 'literal_mathematical_content_with_notation_normalized',
          'source_statement_reproduced_verbatim':False}
    if paper=='N001':
        item['source_file']=n1_rel
        item['source_span']=n1_statement
    else:
        anchor=prior['targets'][idx-4]
        st,en=anchor['span_start_codepoint'],anchor['span_end_codepoint_exclusive']
        assert sha(n3[st:en].encode()) == anchor['span_sha256'], label
        item['source_file']=n3_rel
        item['source_span']=span(n3,st,en,physical_pdf_pages=anchor['source_pages'],role='prior_hash_bound_statement_and_proof_anchor_not_a_length_selection')
    if label=='A3':
        item['interpretive_note']='The printed phrase "this is the case" is read as failure of PRI, as its proof confirms. PRI pairs are also QPRI under the source definition. The manuscript states the stronger unambiguous profile.'
    targets.append(item)

background = [
 {'id':'B97','statement':'Inductively minimal rank-r pairs are thin and residually connected, with group S_(r+1); their connected diagrams have no induced cycles longer than three, every edge in exactly one maximal clique, and every vertex in one or two maximal cliques; conversely each permitted connected diagram determines one pair up to isomorphism.', 'reference':'Buekenhout-Cara-Dehon 1997, Mostly Finite Geometries, pp185-190, as restated in N001 Lemma1 and following paragraph', 'direct_original_read':False,'restatement_binding':n1_b97,'used_only_for':['A1','A2','A3','A4'],'not_targeted':'The 1997 classification itself is outside this intake.'},
 {'id':'W1','statement':'Every independent family in S_m has size <=m-1; every independent family of size m-1 generates S_m.', 'reference':'Whiston 2000, Journal of Algebra232,255-268; source recital N003 p3','direct_original_read':False,'read_limit':'N003 recital read; original Whiston proof not independently read in this assembly.','normalization':'N003 recital says equality iff generation; only the required extremal-size => generation direction is retained, not a false assertion that all minimal generating sets have maximal size.'},
 {'id':'W2','statement':'For n>=7 an omission subgroup of an independent (n-1)-element generating family in S_n is intransitive, transitive imprimitive with two-point blocks, or A_n.','reference':'N003 p4 consequence explicitly attributed to Whiston [8]','direct_original_read':False,'cfsg_dependency_retained':True,'not_inferred_from':'W1'},
 {'id':'Cayley','statement':'The number of trees on a specified labelled m-point set is m^(m-2).','reference':'Classical formula, also invoked in N003 Corollary2.2','unexpanded':True},
 {'id':'Coset','statement':'The source (G1)-(G3) criterion and residue/coset correspondence; RWPRI equivalence to (G4). All conditions are restated in manuscript section1.','reference':'N003 author manuscript pp7-8; Buekenhout1995, Buekenhout-Hermand1991, Tits1974 as cited there.','direct_original_read':False,'read_limit':'The exact criterion in N003 has been read; the earlier reference books/articles were not independently acquired for this assembly.'},
 {'id':'AutSn','statement':'Every automorphism of S_n is inner for n>=7.','reference':'Classical symmetric-group automorphism fact, used only if group-geometry isomorphisms allow automorphisms of the specified action.','unexpanded':True,'alternative':'The source conjugate-coset-data convention avoids this additional isomorphism convention.'},
 {'id':'Elementary','statement':'Elementary finite group and permutation theory, vector spaces over F2, sign, finite maxima, primitive action iff maximal point stabilizer; all nontrivial forest, parity, module and overgroup arguments are expanded in manuscript.','unexpanded':True}
]

contract={
 'schema':'compress_A_intake_review_v1','date':'2026-10-10','bundle':'Compress_A',
 'status':'complete_written_draft_not_frozen_not_independently_certified',
 'intake_ids':['N001','N003'],'target_count':12,
 'objective':'A single standalone manuscript deriving all twelve declared source results from a shared proved core and explicit retained background; first bundle in a larger multi-manuscript programme.',
 'source_files':files,
 'source_versions':{
 'N001':{'title':'Some properties of inductively minimal geometries','authors':['Francis Buekenhout','Philippe Cara'],'year':1998,'publication':'Bull. Belg. Math. Soc. Simon Stevin5,213-219','doi':'10.36045/bbms/1103409005','primary_locator':'https://www.academia.edu/54639280/Some_properties_of_inductively_minimal_geometries','version':'Complete rendered authored text corresponding to the1998 article; exact record bytes bound, original PDF absent and layout/version identity not independently established.','access_depth':'complete rendered authored text L181-L220 read, including proofs and bibliography','primary_pdf_available':False,'author_body_span':n1_authored,'candidate_mainbody_span':n1_main_candidate,'read_limits':['Original PDF not retrieved.','Diagram glyphs and formula layout are damaged by browser rendering.','Website wrapper and recommendations outside displayed L181-L220 are not article content.','The raw direct-request HTML is a challenge page and is not evidence of article access.']},
 'N003':{'title':'Independent generating sets and geometries for symmetric groups','authors':['Peter J. Cameron','Philippe Cara'],'year':2002,'publication':'Journal of Algebra258,641-651','doi':'10.1016/S0021-8693(02)00550-1','primary_locator':'https://maths.qmul.ac.uk/~pjc/preprints/igsgsn.pdf','version':'Complete12-page author manuscript with bound PDF and page-marked extraction; not silently identified with final journal layout.','access_depth':'all12pages read in prior source audit and target/definition/proof passages reviewed in this assembly','primary_pdf_available':True,'read_limits':['The prior extraction is used verbatim; PDF extraction was not regenerated by this binding script.','Whiston and1997originals are not part of this two-paper primary acquisition.']}
 },
 'scope_contract':{'N001':'All four parts of Theorem1, with source definitions and all ranks >=1.','N003':'All eight numbered results, restricting general group results to finite groups and keeping n>=7 for symmetric-group classifications; Theorem3.1 strong-independence consequence included.','excluded':['N003 unnumbered small-degree exceptional census and computational claims','N003 unnumbered general direct-product discussion and open questions','N008 and any Frattini extension','N002 counting/truncation papers and full-shadow-IP papers','Reproduction of every auxiliary statement, example, historical discussion or bibliography entry'],'corrections_or_clarifications':['N001 QPRI clause disambiguated as non-PRI iff middle; all PRI pairs are automatically QPRI.','W1 recital uses extremal-size implies generation; the misleading reverse phrasing is not repeated.','General group results are finite specializations, not certified arbitrary-infinite claims.'],'source_theorems_not_used_as_background':True},
 'targets':targets,'retained_background':background,
 'source_body_length_status':'No approved full-body word-length measurement for the two-version intake. Candidate N001 rendered-body span is recorded solely for later reviewed extraction.',
 'measurement':{'eligible_for_final_manuscript_ratio':False,'manuscript_ratio':None,'reason':'Independent mathematical and scope review pending; identical full-body length convention and source-span treatment not yet approved. N001 has no original PDF and its rendered body requires explicit layout handling.','primary_metric_proposed':'normalized main-body words with identical references/acknowledgments exclusions, including required proof appendices','denominator_policy':'Complete integrated manuscript body plus every necessary external adapter/dependency exposition, charged once; retained unexpanded background explicitly conditional.','prior_matched_proof_ratio':'Separate diagnostic, not imported or substituted.'},
 'draft_files':[binding('phase36_compress_forest_manuscript.md','integrated_complete_mathematical_draft')],
 'review_requirements':['Independent all-parameter mathematical review of the assembled proof, including the changed exposition.','Independent check of all12source formulations, finite restrictions and action/isomorphism conventions.','Review the retained B97,W1,W2 dependency boundary and inspect for circular target imports.','Freeze exact source/body/denominator spans and the common word normalization only after mathematical scope is accepted.'],
 'integrity_check':{'source_hashes_verified':True,'N003_target_anchor_hashes_verified':8,'N001_complete_theorem_span_bound':True,'counts_and_membership_asserted':True},
}
assert len(targets)==12
assert len({t['adapter'] for t in targets})==12
assert {t['paper'] for t in targets}=={'N001','N003'}
OUT.write_text(json.dumps(contract,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'output':str(OUT),'source_files_verified':len(expected),'targets':len(targets),'manuscript_ratio':None,'status':contract['status']},indent=2))
