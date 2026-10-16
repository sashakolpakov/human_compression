from pathlib import Path
import json,hashlib
C=Path(__file__).resolve().parent;S=C.parents[2]
rows=[]
def add(label,pages,status,proof,qualification='Literal fixed-source scope; no additional principal count.'):
 rows.append(dict(label=label,physical_pages=pages,status=status,proof=proof,qualification=qualification,attribution='Source statement credited to its author; project and classical inputs identified in the cited proof.'))
add('Abstract, Introduction and Theorem5 exhaustive list',[1,2,3,15,18],'PRINCIPAL_STATEMENT_ALREADY_REFUTED','principal_boundary.tex, pure_mixed.tex: n3465 and four simple parabolics','Literal list excludes the repeated-prime pure-field boundary. No corrected exhaustive classification claimed.')
add('Definitions: left cosets, algebraic residues, RWPRI and local2T',[3,4,5],'SOURCE_CONVENTIONS_RETAINED','completion.tex section1','Algebraic local2T and actual thinness remain distinct; FT proofs establish common representatives for every flag.')
add('Elementary coset action and rank2 geometry',[3,4],'ELEMENTARY_REPROVED','completion.tex and common coset framework: translate a nonempty coset meet to the standard edge')
add('Lemma1',[4],'IMPORTED_PROVED','preliminary.tex: extend every edge using a common representative')
add('RWPRI strict intersections and ordered maximal chain',[5],'IMPORTED_PROVED','prime_degree.tex, prime_extensions.tex: strict subset intersections and induction choosing a maximal step')
add('Table1 maximal Suzuki subgroups and order',[6],'EXPLICIT_CLASSICAL_PREMISE','Classical Suzuki maximal-subgroup classification credited by source to Lueneburg; common_preliminaries.tex','No new proof or original credit for the classical classification.')
add('Lemma2',[6],'IMPORTED_PROVED','preliminary.tex: odd-power gcd identity')
add('Lemma3',[6],'CORRECTED_SCOPE_PROVED','restrictions.tex, prime_extensions.tex: proper overgroups of the embedded full split dihedral','The literal word subgroups must exclude the ambient group; statement retains the same embedded subfield.')
add('Lemma4',[6],'IMPORTED_PROVED','restrictions.tex: only simple-subfield maximal parabolics remain at rank at least4')
add('Theorem1 necessary patterns',[7],'IMPORTED_PROVED','patterns.tex: exactly three necessary prime-degree residue patterns')
add('Theorem1 existence of displayed patterns',[7],'IMPORTED_PROVED','realizations.tex: all allowed prime half-order parameters, including equal odd primes')
add('Theorem2',[7],'IMPORTED_PROVED_FULL_RANK_RANGE','prime_degree.tex: prime field degree, composite q-1, no rank at least3')
add('Theorem3 exhaustive rank3 list',[7,8,9],'ALREADY_REFUTED_IMPORTED','principal.tex: Sz8/Sz32/C533:4 with meet20 instead of8','Same already acquired L114 counterexample; no second principal credit.')
for i,shape in [(4,1),(5,2),(6,3),(7,4),(8,5),(9,6),(10,7),(11,8),(12,9),(13,10)]:
 status='INTERSECTIONS_IMPOSSIBLE' if i in [4,5,6,8] else 'INTERSECTIONS_EXIST_RWPRI_IMPOSSIBLE' if i==12 else 'CANONICAL_UNIFORM_EXISTENCE'
 add(f'Theorem3 pattern R{i}',[7 if i==4 else 8 if i<=9 else 9],status,f'realizations.tex: rank-three Theorem5.5 pattern{shape}; higher_families proofs where applicable','No exhaustion of arbitrary relative positions is inferred from a sufficient construction.')
add('Theorem4 dihedral enumeration and diagrams',[9,10],'EXPLICIT_CITED_PREMISE','Source reference[20], L109, separately attributed outside105; elementary odd-dihedral maximality used in prime_extensions.tex','No recovery credit for the cited original; no new enumeration assumed.')
for i in [1,2,3]:
 add(f'Section3.1 extension of R{i}',[10,11,12],'NONEXTENSION_PROVED',f'prime_extensions.tex caseR{i}', 'Source R1/R3 conclusions recovered; its positive R2 candidate is impossible. Equal sizes alone do not identify embedded subgroups.')
add('Figure1 and Construction1 pentagon diagram',[12,18,19],'IMPOSSIBLE_HYPOTHESIS','prime_extensions.tex, higher_obstructions.tex; diagrams.tex','The conditional diagram is not an existing geometry because its prescribed intersection lattice is impossible.')
add('Section3.2 no higher-rank extension',[12],'IMPORTED_PROVED','prime_degree.tex: rank3 residue already impossible')
for i in range(4,14):
 status='IMPOSSIBLE_SOURCE_RESIDUE' if i in [4,5,6,8] else 'RWPRI_IMPOSSIBLE' if i==12 else 'CANONICAL_CONCLUSION_PROVED_EXHAUSTIVENESS_REFUTED'
 proof='higher_obstructions.tex' if i in [4,5,6,8] else 'pure_mixed.tex' if i in [12,13] else 'split_families.tex' if i in [7,9] else 'torus_families.tex'
 add(f'Section3.3 extension branch R{i}',[12 if i==4 else 13 if i<=8 else 14 if i<=12 else 15],status,proof,'Conditional canonical positive family is proved; source inference that its branches exhaust arbitrary embeddings relies on the refuted Theorem3 and is not retained.')
add('Section3.3.2 same R7/R8 branches',[13],'EXHAUSTIVE_PREMISE_REFUTED','principal.tex and realizations.tex','R7 realized; R8 impossible; they do not exhaust the stated parameters.')
add('Construction1',[15],'PRESCRIBED_LATTICE_IMPOSSIBLE','higher_obstructions.tex; prime_extensions.tex','Full intended lattice from sourcep15 includes the forbidden common-reflection subfield meet.')
for i in [2,3,4]:
 add(f'Construction{i}',[15,16] if i==2 else [16],'LITERAL_AND_INTENDED_LATTICE_IMPOSSIBLE','higher_obstructions.tex','Literal full meet cannot lie in the printed odd dihedral; repairing its final index leaves the independent intended-lattice obstruction.')
add('Construction2 truncation remark',[16],'IMPOSSIBLE_HYPOTHESIS','higher_obstructions.tex','Both stated full lattices are impossible; deleting a type formally does not establish either realization.')
add('Constructions2–4 intersection remark',[16],'CORRECTED_SCOPE','higher_obstructions.tex','Their intended residue types differ at the subfield meet; literal full-intersection indexing is independently inconsistent.')
for i in [5,7]:
 add(f'Construction{i}',[16,17] if i==5 else [17],'CORRECTED_UNIFORM_RWPRI_EXISTENCE','split_families.tex','Correct conflicting labels; Construction5 also needs its missing t-1 factor and corrected affine product. Every intended allowed parameter is realized; FT not asserted.')
add('Construction5 distinguished-index distinction',[16],'CONDITIONAL_DISTINCTION_PROVED','completion.tex: different omitted maximal-subfield orders distinguish stated-action families','Requires admissible parameters for each chosen distinguished prime; no enumeration of unlabelled geometries.')
add('Construction6 intended lattice',[17],'PRESCRIBED_LATTICE_IMPOSSIBLE','higher_obstructions.tex: inherited R8 meet','Different lower lattices with the same bare parabolic types are not excluded.')
add('Construction6 bare parabolic types',[17],'EXPLICIT_GEOMETRY_WITH_DIFFERENT_MEETS','descent.tex and retained finite certificate: relative3,5,7; torus13,41,113','Not claimed to satisfy the impossible full intended source lattice.')
for i in [8,9]:
 add(f'Construction{i}',[17] if i==8 else [17,18],'UNIFORM_CANONICAL_GEOMETRY_EXISTENCE','descent.tex, torus_families.tex','Correct repeated final index; all source parameter tuples including selected primes dividing base torus order. FT, thickness, RC and RWPRI proved; not an embedding census.')
add('Construction10',[18],'INTERSECTIONS_EXIST_RWPRI_IMPOSSIBLE','pure_mixed.tex: all mixed overgroups correspond to scalar subspaces; codimension greater than1','Negative result applies to every embedding with the prescribed mixed parabolic and pair intersections.')
add('Construction11 literal parameters',[18],'UNIFORM_CANONICAL_GEOMETRY_EXISTENCE','pure_mixed.tex TheoremA and section3','All literal allowed tuples have e>1. FT, thickness, RC and RWPRI proved.')
add('Construction11 exact boundary',[18],'CORRECTED_CRITERION_PROVED','pure_mixed.tex: RWPRI iff e>1; principal_boundary.tex','Repeated primes allow all distinct relative primes to be selected; e1 fails at a final 5:4 inclusion.')
add('Section5 star diagrams of surviving prescribed families',[18,19],'CONDITIONAL_DIAGRAM_PROVED','diagrams.tex: subgroup-product criterion','8/9 centre torus; corrected5/7 centre dihedral; FT conditional for5/7. No global quantitative almost-all claim is inferred.')
add('Section5 nonstar pure-subfield diagrams',[18],'DIAGRAM_PROVED','diagrams.tex: product order strictly smaller for every pair','Complete diagram; source observation concerns rank greater than3.')
add('Section5 future flag-transitivity question',[3,19],'SOURCE_FUTURE_QUESTION_PARTLY_ANSWERED','descent.tex, torus_families.tex, pure_mixed.tex','Canonical8/9/11 and the bare-type6 example proved. Corrected5/7 and arbitrary embeddings remain unproved; these are not assertions of Theorem5.')
add('Introduction quoted rank2 local2T uniqueness',[2],'ALREADY_CORRECTED_IMPORTED','local_rank.tex: rank2 scalar families; scalar_subspaces.tex; subfield_families.tex','Quoted earlier classification corrected; no L115 whole-source credit from this import.')
add('Introduction quoted thinness',[2],'ALREADY_REFUTED_IMPORTED','nonthin8.tex and nonthin32.tex','Literal algebraic local2T satisfied, actual panels have three chambers. Exact source conventions retained.')
add('Introduction quoted universal local rank and prime restriction',[2],'REFUTED_BY_ACTUAL_GEOMETRIES','local_rank.tex and local_geometry.tex: arbitrary-rank thick RC FT locally2T geometries; rank3 composite-degree geometry','Stronger geometry join kept separate from the old conservative pregeometry proof; no additional principal count.')
add('Introduction historical literature and References',[1,2,19,20],'ATTRIBUTED_CONTEXT','Original citations retained in source and overview','No reproof or original credit for historical descriptions of other groups and papers.')
b=(S/'sources/catalogue_L110.pdf').read_bytes()
d=dict(source_id='L110',source_edition='Note di Matematica20(1)(2000/2001),1–20, fixed twenty-page edition',source_pdf=dict(path=str(S/'sources/catalogue_L110.pdf'),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()),claims=rows,principal_disposition='principal_statement_refuted',ordinary_recovery_credit=0,new_principal_refutation_credit=0,new_original_credit=0,new_named_open_questions_solved=0,new_Lean_declarations=0,new_measurements=0,new_scientific_acquisitions_in_assembly=0,public_registration_performed=False,principal_acquisition_repeated=False,remaining_fixed_paper_asserted_mathematical_claims=[],borrowed_premises=['Classical Suzuki structure, model, subfield maximality and centralizers','Lang–Steinberg surjectivity','Schur–Zassenhaus','Explicit quoted dihedral classification [20]/L109 outside105'],uncertified_extensions=['Corrected complete classification of arbitrary subgroup positions','Flag transitivity of corrected Constructions5/7','Flag transitivity of arbitrary embeddings with only listed abstract parabolic types','Full Lean formalization of the Suzuki arguments','Quantitative almost-all classification or compression ratio'],new_assembly_mathematics=['Uniform prime-residue nonextension proof with embedded-affine uniqueness','Subgroup-product calculation of conditional diagrams','Scalar-coordinate attachment proving actual locally2T geometries in arbitrary rank'],reused_math='Exact previously reviewed phase7/8 proofs, corrected rank3 theory, existing principal refutation and finite certificates')
(C/'claims.json').write_text(json.dumps(d,indent=2)+'\n');print(len(rows))
