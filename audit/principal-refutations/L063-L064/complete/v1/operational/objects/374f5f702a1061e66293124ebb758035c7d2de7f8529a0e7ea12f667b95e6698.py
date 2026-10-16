"""Individual source ledgers; no source registration is performed."""
from pathlib import Path
import json

A = Path(__file__).resolve().parent


def row(label, pages, status, proof, qualification, attribution='Source claim; the indicated proof retains its classical premises and original construction attribution.'):
    return dict(label=label, physical_pages=pages, status=status, proof=proof, qualification=qualification, attribution=attribution)


def ledger(sid, pages, rows):
    return dict(source_id=sid, source_pages=pages, principal_disposition='principal_statement_refuted',
                treatment='COMPLETE_FIXED_SOURCE_TREATMENT_AWAITING_DISTINCT_REVIEW', claims=rows,
                ordinary_recovery_credit=0, new_principal_refutation_credit=0, new_original_credit=0,
                new_named_open_questions_solved=0, new_Lean_declarations=0, new_measurements=0,
                new_scientific_acquisitions_in_assembly=0, public_registration_performed=False,
                principal_acquisition_repeated=False, remaining_fixed_paper_asserted_mathematical_claims=[],
                source_scope_conventions={'unordered_parabolics':True, 'conjugacy':'G-orbits',
                                          'source_isomorphism':'Aut(G)-orbits on the unordered subgroup pair',
                                          'full_graph_automorphism_groups':'separate claims, not inferred from the source-isomorphism counts'},
                borrowed_premises=['Dickson, Moore and Suzuki subgroup types, maximality, normalizers and subfield embedding data',
                                  'Classical PSL/PGL orders, projective-line actions and specified outer fusion',
                                  'Elementary subgroup lattices of A4, S4 and A5',
                                  'Tutte cubic arc-transitive vertex-stabilizer bound48, under the hypotheses proved in the graph components',
                                  'Accepted PartI treatment only for the previous Borel/dihedral maximal-parabolic scope'],
                uncertified_extensions=['No new compression measurement', 'No new Lean verification',
                                        'No independent repetition of historical MAGMA runs',
                                        'No claim that missing pages occur in the retained appendix edition',
                                        'No new principal refutation or named open-question count'])


rows = [
 row('Abstract, Theorem1.1 and final complete-classification assertion',[1,4,5,20],'PRINCIPAL_STATEMENT_ALREADY_REFUTED',['omitted_affine','subfields','completion'],'The missing even-characteristic affine family refutes the printed exhaustive list. The new component completes all surviving branches and gives the corrected classification.'),
 row('Section2 unordered conjugacy and isomorphism conventions',[4],'DEFINITION_RETAINED',['completion','cyclic_three','scalar'],'The two parabolics form a set; exchanging equal types must be included. Source isomorphism means Aut(G), not unrestricted graph isomorphism.'),
 row('Section3 reduction to maximal parabolic and local two-transitive actions',[5],'RECOVERED',['completion','partI'],'The rank-two local-action lemma proves the reduction, firmness and connectedness. The previous PartI branch is separately attributed.'),
]
for i in range(1,15):
    pages=[5] if i<=4 else [5,6] if i==5 else [6] if i<=11 else [6,7] if i==12 else [7]
    if i==5:
        status='BORROWED_FORMULA_WITH_RANGE_CORRECTION'; qual='Odd single-class clauses require d>2; d=2 is the separate four-group case. At q5 the printed formula gives15 but there are5 four-groups.'; proof=['completion','exceptional']
    elif i in (7,8):
        status='BORROWED_FORMULA_WITH_FIELD_PARAMETER_MADE_EXPLICIT'; qual='k is the degree of the largest multiplier field of V. The literal normalizers prove the displayed orbit lengths; no number of conjugacy classes is inferred.'; proof=['completion']
    else:
        status='EXPLICIT_CLASSICAL_PREMISE'; qual='Retained classical subgroup type, conjugacy and normalizer statement in its actual parameter range; not a premise asserting the target geometry classification.'; proof=['completion','overgroups']
    rows.append(row(f'Lemma4.1 item{i}',pages,status,proof,qual,'Source explicitly attributes the subgroup classification to Dickson, Moore, Huppert, Suzuki and King.'))
rows += [
 row('Remark4.2 overlapping A5 and PSL/PGL subgroup names',[7],'RECOVERED',['subfields','completion'],'PSL2(4)=PSL2(5)=A5 and PSL=PGL in characteristic two; overlapping names do not count as distinct families.'),
 row('Remark4.3 orbit lengths do not give class counts',[7],'RECOVERED_WITH_CLASSICAL_ATTRIBUTION',['completion','scalar'],'The multiplier-field proof explains the distinction. Historical discussion of Dickson is attributed, and the needed actual scalar counts are proved.'),
 row('Table7 maximal subgroups in even characteristic',[8],'EXPLICIT_CLASSICAL_PREMISE',['overgroups','completion'],'Classical maximal subgroup types, orders and indices; only proper maximal subgroups are used.'),
 row('Table8 maximal subgroups in odd characteristic',[8],'CLASSICAL_PREMISE_WITH_INDEX_CORRECTION',['overgroups','completion'],'PGL2(s) has order s(s²−1); its index in PSL2(q), q=s², is q(q²−1)/(2s(s²−1)). The printed denominator lacks2.'),
 row('Lemma4.4 two-transitive degree divisibility',[7],'RECOVERED',['overgroups','completion'],'The point stabilizer is transitive on d−1 other points, hence d(d−1) divides the acting group order.'),
 row('Lemma4.5 abelian transitive permutation groups',[7],'RECOVERED',['completion'],'Faithfulness and commutativity force regularity; a two-transitive regular action has degree2.'),
 row('Proposition4.6 complete representation list',[9,10],'CORRECTED_AND_REPROVED',['overgroups','completion'],'All actual local actions are proved without assuming the in-preparation source. Printed prime-field S4 cases omit degrees2 and4; S4<PSL2(7) supplies both, with stabilizers A4 and S3.'),
 row('Proposition4.6 representation uniqueness wording',[9,10],'SCOPE_DISTINGUISHED',['overgroups','completion'],'Conjugacy within a fixed subgroup is distinguished from ambient embedding classes. Configuration counts are separately proved by normalizer orbits.'),
 row('Section4.4 PGL embedding and characteristic PSL subgroup',[10],'EXPLICIT_CLASSICAL_PREMISE',['overgroups','subfields'],'PGL2(s) embeds in PSL2(s²); its index-two PSL subgroup is characteristic. Used with the normalizer and Galois proofs, not to identify equal-order overgroups.'),
 row('Lemma4.7 four class-fusion statements',[10],'EXPLICIT_CLASSICAL_PREMISE_WITH_EXPLICIT_DIHEADRAL_PROOF',['exceptional','subfields','s4_pairs'],'Fusion applies when the two named classes actually exist. The torus parity proof establishes the dihedral clause directly; classical exceptional and subfield fusion remains attributed.'),
]
lemmas={
 '5.1':([11],'overgroups','Small D10 overgroups; appendix page pointer is an edition mismatch in the retained L064.'),
 '5.2':([11],'overgroups','All A4 overgroups under the stated ambient maximal-A5 hypotheses; defining-characteristic cases included.'),
 '5.3':([12],'scalar','Main subgroup count (4^(r−1)−1)/15 recovered. Intermediate Steps4/5 mix A4 and E16:3 labels; the coordinate proof supplies the actual incidences and normalizers.'),
 '5.4':([13],'scalar','All Frobenius-orbit counts recovered, including r=3 and r>3; no finite table fitting.'),
 '5.7':([17],'overgroups','D6 overgroups D12,D18,S4 in the actual prime characteristic.'),
 '5.8':([17],'overgroups','D8 overgroups D16,D24,S4 in the actual prime characteristic.'),
 '5.9':([18],'overgroups','A4 overgroups S4,A5 with their ambient divisibility conditions.'),
 '5.11':([18],'subfields','Published restriction to extension degree2 is false; all two-dimensional affine covers are proved.'),
 '5.13':([18,19],'subfields','Read in its surrounding odd-prime extension context; no affine cover for the half-scalar group.'),
 '5.14':([19],'subfields','A5 stabilizers at subfield sizes9,11 have a unique projective overgroup, by pointwise Frobenius descent.'),
 '5.15':([19],'subfields','S4 stabilizer at subfield size7 has a unique projective overgroup.'),
 '5.17':([19],'q9','The q9 D8 case has only S4 as a local overgroup, and exactly one unordered configuration.'),
 '5.18':([19],'subfields','Quadratic PGL Borel has the unique projective and affine overgroups described in the proof.'),
 '5.19':([19,20],'subfields','The simple index-two subgroup has unique PGL overgroup; only s3 gives the additional A5 possibility.'),
 '5.20':([20],'subfields','At q25, S4 lies in a unique PGL2(5) overgroup, so no configuration with a second such group.'),
}
for label,(pages,proof,qual) in lemmas.items():
    status='SOURCE_ASSERTION_CORRECTED' if label=='5.11' else 'RECOVERED'
    rows.append(row('Lemma'+label,pages,status,[proof,'overgroups'],qual))
for label,pages,proof,status,qual in [
 ('5.5',[14,15,16,17],'exceptional','RECOVERED_WITH_EMPTY_PARAMETER_BRANCHES','The A5 classification and nonempty class counts are recovered; scalar cases and q16 are reused. Four square-field rows are empty.'),
 ('5.6',[17],'cyclic_three','UNORDERED_INNER_COUNTS_CORRECTED','Rows1--5 recovered; rows6--7 have m+floor(m/2) inner classes, Aut count m retained.'),
 ('5.10',[18],'exceptional','RECOVERED','All S4 configurations and both class columns; full graph groups are separate Section6 assertions.'),
 ('5.12',[18],'subfields','EXHAUSTIVITY_CORRECTED','The m2 row and all small even cases recovered; all prime-degree affine covers included.'),
 ('5.16',[19],'subfields','UNORDERED_INNER_COUNTS_CORRECTED','Only s3 survives. Table5 inner counts are halved; full automorphism counts retained.'),
 ('5.21',[20],'subfields','RECOVERED','All three quadratic PGL rows, including q9 and the q25 exclusion.')]:
    rows.append(row('Proposition'+label,pages,status,[proof,'scalar' if label in ('5.5','5.12','5.16') else 'overgroups'],qual))

arc_rows=json.loads((A.parent/'arc_actions/source_rows.json').read_text())['rows']
for ar in arc_rows:
    t,r=ar['table'],ar['row']; proof=[];status='RECOVERED'; qual='Existence and both class columns are recovered; the local arc length is proved independently from the actual stabilizers.'
    if t==1:
        proof=['subfields'] if r==1 else ['scalar'] if r in (2,3,4) else ['exceptional']
        if r in (12,13,14,18): status='EMPTY_PARAMETER_BRANCH';qual='No q satisfies the complete printed hypotheses. The local arc statement is a conditional stabilizer theorem, not an existence assertion.'
        elif r in (16,17):qual='Counts recovered; the q=-1 mod40 alternative is empty and q=9 mod40 is the actual square-field branch.'
    elif t==2:
        proof=['cyclic_three']
        if r>=6: status='INNER_COUNT_CORRECTED';qual='With m=(p−epsilon)/6, inner count m+floor(m/2) replaces2m−1; Aut count m and local arc length2 are retained.'
    elif t==3: proof=['exceptional','s4_pairs'] if r in (7,8) else ['exceptional']
    elif t==4:
        proof=['subfields']
        if r==1:status='PRINTED_ROW_RECOVERED_EXHAUSTIVITY_CORRECTED';qual='At m2 the printed one/one counts hold; additional prime-degree affine covers were omitted. Their counts are supplied by scalar_orbits.'
        if r==5:qual='Exact repeat of Table1 row1, not an additional family; its prime-exponent condition reduces to q16.'
    elif t==5:proof=['scalar','subfields'];status='INNER_COUNT_CORRECTED';qual='Inner count (3^(m−1)−1)/2; at q27 this is4 instead of8. Printed Aut counts and local arc length2 retained.'
    elif t==6:proof=['q9'] if r==3 else ['subfields']
    proof+=['arcs']
    x=row(f'Table{t} row{r}',[2 if t<=2 else 3],status,proof,qual)
    x.update(table=t,row=r,local_arc_length=ar['local_arc_length'])
    rows.append(x)

exceptions=[[(1,1)],[(1,6),(1,13)],[(3,2)],[(3,5)],[(3,6)],[(3,7),(3,8)],[(4,1)],[(4,5)],[(6,1)]]
for i,refs in enumerate(exceptions,1):
    x=row(f'Table9 exception row{i}',[21],'RECOVERED_AS_EXACT_CROSSREFERENCE',['arcs'],'The same source configurations already occur in Tables1--6; this adds no family. Empty Table1 row13 remains conditional only.')
    x['source_table_rows']=[{'table':t,'row':r} for t,r in refs];rows.append(x)
rows += [
 row('Lemma5.3 Step4 total subgroup count',[12],'INTERMEDIATE_COUNT_CORRECTED',['completion','scalar'],'For q=4^r, the number of A4 subgroups is q(q²−1)/12. The printed q(q−1)/12 misses the q+1 fixed-point choices; the final Lemma5.3 formula is recovered.'),
 row('Lemma5.3 Steps4--5 subgroup labels',[12],'LITERAL_SUBGROUP_LABELS_CORRECTED',['completion','scalar'],'H is A4=U4:C3, of order12; E16:C3 has order48 and is not A5. The coordinate proof consistently distinguishes these groups.'),
 row('Section6 second A5/D30 path orientation',[20],'LITERAL_PATH_TYPE_CORRECTED',['arcs'],'The second path starts at type1, not type0; the proof handles both orientations.'),
 row('Section6 S4/D24 local kernel notation',[22],'LITERAL_GROUP_NAME_CORRECTED',['arcs'],'The group acting on cosets of D8 is D24, not the printed D18. The full fourth-arc obstruction is reproduced with attribution to the source referee argument.'),
 row('Section6 q9 generalized quadrangle, full group and five arcs',[22],'RECOVERED',['q9','arcs'],'The literal duad/syntheme model and symplectic quotient give the quadrangle; a checked duality and Tutte bound prove full group PGammaL2(9), order1440 and five arcs.'),
]
for p in [17,23,31,41,47,71,73,79,89]:
    corrected=p in [17,31,47,79]
    rows.append(row(f'Section6 S4/S4 full graph group q={p}',[22],'FULL_GRAPH_GROUP_CORRECTED' if corrected else 'RECOVERED',['s4_pairs'],'Full group PSL2(p)×C2, not the printed PGL2(p); full arc length4.' if corrected else 'Full group PGL2(p) and full arc length4.'))
for p in [17,31,79,97]:
    rows.append(row(f'Section6 S4/D16 full graph group q={p}',[22],'RECOVERED',['subdivision'],'Suppressing degree2 vertices, the cubic stabilizer bound and the outer-class action prove full group PSL2(p); two inner configurations remain distinct.'))
rows += [
 row('Section6 appendix arc-proof pointer',[20],'FIXED_EDITION_DISCREPANCY',['completion','arcs'],'The retained appendix pages19--20 concern Proposition30 and contain no arc proofs. The required source assertions are proved in the shared arc manuscript.'),
 row('Section7 and earlier appendix pointers',[11,17,18,19,20,23],'FIXED_EDITION_BOUNDARY',['completion'],'The retained appendix begins at Lemma12, omits the advertised entire A5 count proof and the standalone q25/S4 lemma. No missing content is invented or counted.'),
 row('Historical checks and named constructions',[4,14,15,16,17,22,23,24],'ATTRIBUTION_RETAINED',['completion'],'Historical MAGMA checks are not repeated or used as proof. Original constructions, cited classifications and the classical graph names retain attribution.')
]

appendix=[]
for label,pages,proof,status,qual in [
 ('Lemma12',[1,2],'overgroups','RECOVERED','A4 overgroup list in the original A5 ambient scope; defining-characteristic cases are handled by the common proof.'),
 ('Proposition16',[2,3,4],'cyclic_three','UNORDERED_INNER_COUNTS_CORRECTED','Its C6/S3 families retain both counts; A4/A4 inner count is m+floor(m/2), Aut count m retained under the published unordered convention.'),
 ('Lemma17',[5],'overgroups','RECOVERED','D6 local overgroups D12,D18,S4 in prime fields.'),
 ('Lemma18',[5],'overgroups','RECOVERED','D8 local overgroups D16,D24,S4 in prime fields.'),
 ('Lemma19',[5,6],'overgroups','RECOVERED','A4 local overgroups S4,A5 in its specified prime-field scope.'),
 ('Proposition20',[6,7,8,9,10,11],'exceptional','RECOVERED','Every S4 family and both class counts follow from the common normalizer proofs; full graph groups are not assertions of this appendix.'),
 ('Lemma21',[11],'subfields','RECOVERED_WITH_COMPLETE_AFFINE_INTERPRETATION','Its proof lists the affine type without the published lemma’s m2 restriction; the complete coordinate proof identifies every two-dimensional affine cover.'),
 ('Proposition22',[11,12,13],'subfields','EXHAUSTIVITY_CORRECTED','All q4 and q16 branches recovered. The affine case is not restricted to extension degree2; general prime-degree covers are supplied.'),
 ('Lemma23',[13,14],'subfields','RECOVERED','Odd-prime extension context; half-scalar Borel has no affine two-transitive cover.'),
 ('Lemma24',[14],'subfields','MAIN_OVERGROUP_CONCLUSION_RECOVERED_AUXILIARY_CLAIM_CORRECTED','The actual A5 local-overgroup conclusion is proved. Its separate assertion excluding every PGL2(3^w) in PSL2(3^(2m)) is false and not used.'),
 ('Lemma25',[14],'subfields','RECOVERED','Only the projective7 overgroup remains for S4 in the stated odd-degree characteristic7 scope.'),
 ('Proposition26',[14,15,16,17],'subfields','UNORDERED_INNER_COUNTS_CORRECTED','All nonexistence branches proved by unique projective overgroups and affine covers. At s3, inner counts are halved; scalar-orbit Aut counts retained.'),
 ('Lemma27',[17],'q9','RECOVERED','Only S4 local overgroups of D8 in q9; the full q9 component supplies the actual unordered configuration.'),
 ('Lemma28',[17,18],'subfields','RECOVERED','Quadratic PGL Borel has exactly the affine and projective local-overgroup types.'),
 ('Lemma29',[18],'subfields','RECOVERED','Unique same-type PGL overgroup over PSL; only s3 permits A5 as another type.'),
 ('Proposition30',[18,19,20,21],'subfields','RECOVERED','All three actual quadratic PGL families and both class counts, using q9 where needed; this edition has no separate q25/S4 subcase.')]:
    appendix.append(row(label,pages,status,[proof,'scalar' if label in ('Proposition22','Proposition26') else 'overgroups'],qual))
appendix += [
 row('Proposition30 page19 transporter denominator',[19],'TRANSCRIPTION_CORRECTED',['subfields','completion'],'The ambient denominator is |PSL2(p^(2n))|, not |PSL2(2^(2n))|. The unique PGL overgroup over the fixed Borel is proved directly.'),
 row('Proposition30 page20 transporter denominator',[20],'TRANSCRIPTION_CORRECTED',['subfields','completion'],'The repeated equal-type Borel formula has the same corrected ambient denominator; the unique-overgroup conclusion is recovered.'),
 row('Proposition30 page21 transporter denominator',[21],'TRANSCRIPTION_CORRECTED',['subfields','completion'],'The simple-intersection transporter denominator is the actual ambient order |PSL2(p^(2n))|; the normalizer proof gives exactly one PGL overgroup.'),
 row('Lemma24 item2 PGL exclusion',[14],'AUXILIARY_ASSERTION_REFUTED',['subfields','completion'],'PGL2(3) and PGL2(3^m) embed in PSL2(3^(2m)); the false assertion is replaced by the valid action/order argument.'),
 row('Proposition22 small-field and q16 subcases',[11,12],'RECOVERED',['subfields'],'Three q4 configurations and the q16 A5/D30 configuration each have one inner and one Aut class.'),
 row('Proposition22 general even affine subcase',[12,13],'PRINCIPAL_STATEMENT_ALREADY_REFUTED',['omitted_affine','subfields','scalar'],'The claimed m2 necessity is false. All actual affine covers and the projective-overgroup uniqueness are now proved.'),
 row('Proposition26 odd subfield uniqueness branches',[15,16,17],'RECOVERED',['subfields'],'Pointwise Frobenius descent supplies literal unique-overgroup arguments; equality of subgroup orders is never used as identification.'),
 row('Proposition30 q9 D8 subcase',[19],'RECOVERED',['q9'],'Two S4 classes give one unordered configuration; the graph group proof is supplied for L063 without pretending it is stated here.'),
 row('Proposition30 quadratic affine subcase',[19,20],'RECOVERED',['subfields'],'Two inner configurations and one Aut class; the fixed Borel has exactly one projective overgroup, so the equal-type possibility is excluded.'),
 row('Proposition30 simple-intersection subcase',[20,21],'RECOVERED',['subfields'],'At q9 the S4/A5 configuration gives two inner and one Aut class; another PGL overgroup above the simple subgroup is excluded.'),
 row('Retained edition coverage and numbering',[1,21],'FIXED_EDITION_BOUNDARY',['completion'],'This 21-page edition begins with Lemma12 and ends with Proposition30; absent Lemmas13/14, Proposition15, standalone q25 lemma and arc pages are not assigned invented claims.'),
 row('Historical confirmations and earlier citations',[2,3,4,6,7,8,9,10,11,12,13,15,16,17,19,20,21],'ATTRIBUTION_RETAINED',['completion'],'Historical checks are not rerun; explicit elementary subgroup/normalizer proofs replace their use as validation.')
]

for sid,pages,claims in [('L063',24,rows),('L064',21,appendix)]:
    if len({r['label'] for r in claims})!=len(claims): raise ValueError('duplicate label')
    data=ledger(sid,pages,claims)
    (A/(sid+'_claims.json')).write_text(json.dumps(data,indent=2)+'\n')
    print(sid,len(claims))
