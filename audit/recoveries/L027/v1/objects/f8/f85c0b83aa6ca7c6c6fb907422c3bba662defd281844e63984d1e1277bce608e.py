"""Prepare the L027 synthesis interfaces; no mathematical search is run."""
import hashlib,json
from pathlib import Path
S=Path('/Users/sasha/medusa/research/leemans');R=S.parents[1]/'math_compression';W=S/'reboot_20261013';P=Path(__file__).resolve().parent

def save(n,x): (P/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def ns(p):
 x=pin(p)
 for name,root in [('study',S),('public',R)]:
  if p.is_relative_to(root):x.update(namespace=name,path=str(p.relative_to(root)));return x
 raise ValueError(str(p))

spec=[
 ('rank_four','v1','rank_four.tex','root_adoption','independent_review'),
 ('rank_five','v1','rank_five.tex','root_adoption','independent_review'),
 ('even_subgroups','v1','even_subgroups.tex','root_adoption','independent_review'),
 ('odd_four','v2','odd_four.tex','root_adoption','independent_review'),
 ('rank_obstruction','v1','rank_obstruction.tex','root_adoption','independent_review'),
 ('odd_three','v2','odd_three.tex','root_adoption','independent_review'),
 ('table_one','v1','table_one.tex','root_review',None),
 ('unitary_examples','v1','unitary_examples.tex','root_review',None)]
components=[];deps={}
def add(p):
 x=ns(p);deps[(x['namespace'],x['path'])]=x;return x
for name,edition,tex,acceptance,distinct in spec:
 base='corpus106_L027_'+name;folder=S/(base+'_'+edition)
 a=add(folder/'manifest.json');v=json.loads((folder/'manifest.json').read_text())
 for x in v['exports']:add(folder/x['path'])
 roots=[S/(base+'_'+acceptance)]
 if distinct:roots.append(S/(base+'_'+distinct))
 records=[]
 for root in roots:
  m=add(root/'manifest.json');mv=json.loads((root/'manifest.json').read_text())
  for x in mv['exports']:add(root/x['path'])
  records.append(dict(role='root_acceptance' if root==roots[0] else 'distinct_review',manifest=m,status=mv.get('status')))
 title=next(l for l in (folder/tex).read_text().splitlines() if l.startswith('\\title{'))[7:-1]
 components.append(dict(id=name,title=title,author_manifest=a,accepted_by=records,manuscript=add(folder/tex),pdf=add(folder/tex.replace('.tex','.pdf')),status='ACCEPTED_BOUNDED_COMPONENT'))
source=add(S/'sources/psl3_chiral2022.pdf')
for p in [W/'L027_work/source_contract01.json',W/'L027_work/source_text.txt',W/'L027_section7_routes_audit/report.json',W/'L027_section7_routes_audit/audit.rst',S/'sources/phase282_L028_revised.pdf']:
 add(p)
E=R/'papers/topic-e/v3';EA=R/'audit/topic-e/v3/admission.json'
for p in [EA,E/'manifest.json',E/'chiral-projective-groups.tex',E/'chiral-projective-groups.pdf',E/'umbrella.tex',E/'source_map.json',E/'retained_inputs.json',E/'retained_source_maps.json']+sorted((E/'sections').glob('*.tex')):
 add(p)
for name in ['corpus106_L045_principal_v1','corpus106_L045_principal_independent_review','corpus106_L045_principal_root_adoption']:
 m=S/name/'manifest.json';add(m)
 for x in json.loads(m.read_text())['exports']:add(m.parent/x['path'])
reused=[dict(id='topic_e',manifest=ns(E/'manifest.json'),acceptance=ns(EA),scope='Actual string and rotation criteria, rank-four projective-line classification, complete chiral classification and previously accepted odd composite-degree construction; inherited qualifications unchanged.'),dict(id='L045',manifest=ns(S/'corpus106_L045_principal_v1/manifest.json'),acceptance=ns(S/'corpus106_L045_principal_root_adoption/manifest.json'),scope='Positive simple-group chiral-polyhedron theorem outside A7/L2/L3/U3; does not prove the negative exceptions.')]
save('components.json',dict(components=components,reused=reused))

ret=[]
def retained(i,claim,source,status,scope,routes=[]):ret.append(dict(id=i,claim=claim,source_attribution=source,evidence_status=status,scope=scope,routes=routes))
retained('R1','Regular and chiral rotation correspondences; actual string end and rotation end intersection criteria','Source Section2, McMullen–Schulte[15] and Schulte–Weiss[21]','EXPLICIT_CLASSICAL_INPUT_AND_ACQUIRED_COMMON_STATEMENT','Actual subgroups and the complete indexed intersection property; no quotient-IP or arbitrary hypermap transfer.',['topic_e'])
retained('R2','Dickson natural-subfield subgroup classification and SO3(F) ≅ PGL2(F) for odd F','Source[25] and classical Dickson theorem, as declared in odd/even components','EXPLICIT_RETAINED_CLASSICAL_CLASSIFICATIONS','Actual natural embeddings and exact trace fields; full classical proofs not rederived.',['topic_e'])
retained('R3','PSL3/PSU3 orders, simplicity, projective actions, and full automorphism descriptions','Standard classical facts explicitly stated in each construction and the unitary component','EXPLICIT_RETAINED_CLASSICAL_INPUTS','All semilinear and graph cosets must be accounted for; PSU3(2) handled separately by the acquired written proof.')
retained('R4','Rank-three projective-line marking families in Tables2–3','Source[4] Conder–Potočnik–Širáň and[11] Leemans–Schulte','SOURCE_ATTRIBUTED_PRIOR_CLASSIFICATION','The source table uses only string C-markings. No assertion that an arbitrary reflexible hypermap is a string C-group; this synthesis gives group alternatives but does not regenerate the prior all-type rank-three census.')
retained('R5','No chiral polyhedron has automorphism group PSL3(q) or PSU3(q)','Introduction/Section7 and source[1], Breda d’Azevedo–Catalano2021','SOURCE_ATTRIBUTED_PRIOR_THEOREM','Retained as the exact lower-rank theorem; its original complete proof has not been reacquired in this L027 assembly.')
retained('R6','Earlier classification of simple groups with regular polytopes and the stated corrected exceptional list','Introduction: Nuzhin[17–20], Mazurov[14], Vandenschrick[24], Macaj/Jones personal communication','SOURCE_ATTRIBUTED_HISTORICAL_CONTEXT','No new principal claim and not used to prove the three L027 theorems. Historical personal-communication attribution is not promoted to a new independent certificate.')
retained('R7','PSL3(q), q=2,3,4, has no chiral polytope','Introduction[8] and Section7[3]','SOURCE_ATTRIBUTED_PRIOR_COMPUTATION','The available L028 method is not a replacement for these missing group-specific complete executions. This source-attributed list is not our new census.')
retained('R8','PSU3(q), q∈{2,3,4,5,7,9,13,16}, has no chiral polytope','Section7[3], Buekenhout–Leemans–Tranchida','SOURCE_ATTRIBUTED_PRIOR_COMPUTATION','Exact group-specific executions not acquired; the available earlier edition has no matching complete output roster. The elementary PSU3(2) rank-bound argument pays only the ranks it states.')
retained('R9','Three PSU3(11) enantiomorphic pairs: [5,4,5] twice and [4,5,4] once','Section7 explicitly based on data collected for[3]','SOURCE_ATTRIBUTED_PRIOR_DATA','Literal tuples and census receipts not present in the acquired earlier paper. Retained attribution only, not independently certified here.')
retained('R10','Alt7 has no chiral polytope','Introduction and Section7[8]','SOURCE_ATTRIBUTED_HISTORICAL_CONTEXT','No new Alt7 census is claimed.')
retained('R11','Positive chiral-polyhedron theorem for the remaining nonabelian simple groups','Introduction[9], Leemans–Liebeck; separately accepted L045 principal theorem','ACQUIRED_PROJECT_PRINCIPAL_THEOREM','Only its proved positive range; negative exceptions retain their separate sources.',['L045'])
retained('R12','PSL2/PGL2 chiral classifications, small negatives and odd composite-degree construction','Source[10]; exact previously accepted Topic E v3 proof and source dispositions','ACQUIRED_PROJECT_PRINCIPAL_THEOREM','Use actual theorem, not the source atlas table. q=81 in L027’s negative list is corrected by the explicit k=40 pointed construction.',['topic_e'])
save('retained_inputs.json',dict(records=ret,policy='Source-attributed earlier results retain their original authorship and evidence limits. No new L027 claim is used as its own premise.'))

rows=[]
def row(i,kind,pages,claim,route,disposition='PROVED_WITH_ACQUIRED_COMPONENTS',qualification=''):
 rows.append(dict(id=i,kind=kind,source_physical_pages=pages,claim=claim,route=route,disposition=disposition,qualification=qualification))
row('T1.1','numbered',[2,5,6,7],'All q≥5 rank-four PSL3 construction, exact type, self-duality and both full end stabilizers',['rank_four'])
row('T1.2','numbered',[2,8,9,10],'Both signs and both primitive cube roots give rank-five chiral PSL3(p), p=1 mod6',['rank_five'])
row('T1.3','numbered',[2,22,23],'No chiral rank>5 for PSL3(q) or PSU3(q), q≥2',['rank_obstruction'])
row('L2.1','numbered',[4],'String end-intersection criterion',['R1'],'RETAINED_PRIOR_THEOREM','Actual end groups; no projection shortcut.')
row('L2.2','numbered',[4],'Rotation end-intersection criterion',['R1'],'RETAINED_PRIOR_THEOREM','Full actual indexed criterion.')
row('L2.3','numbered',[4,5],'Two directly regular ends, exact index2 and types',['rank_obstruction'])
row('T5.1','numbered',[12,13,14,15],'Complete reducible odd rank-three alternatives',['odd_three'])
row('T5.2','numbered',[15,16],'Irreducible odd rank-three conic alternatives and small types',['odd_three','R2'])
row('T5.3','numbered',[16,17],'Odd rank-four alternatives and rank bound',['odd_four','topic_e'],'PROVED_WITH_CORRECTIONS','D2p squared, dual point/line convention, and characteristic-five embeddings.')
row('T5.4','numbered',[17,18],'Even triangular/fixed-flag classification',['even_subgroups'])
row('T5.5','numbered',[18,19],'Even rank-three classification with exact trace field',['even_subgroups','R2'])
row('T5.6','numbered',[19,20],'Even rank-four modules, iff IP and rank bound',['even_subgroups'])
row('L6.1','numbered',[22],'Order-two rotation forces a nontrivial proper normal subgroup',['rank_obstruction'])
row('T6.1','numbered',[22],'Preliminary rank≤6, including small nonsimple unitary boundary',['rank_obstruction'],'PROVED_WITH_ACQUIRED_COMPONENTS','No all-rank PSU3(2) census inferred from the bounded elementary argument.')
row('L6.2','numbered',[22],'Rotations at distance>2 commute',['rank_obstruction'],'PROVED_WITH_ACQUIRED_COMPONENTS','Source attributes the lemma to Schulte–Weiss; attribution retained.')
row('Table1','table',[17],'All nine signed parameter cells and all three characteristic polynomials',['table_one'],'PROVED_WITH_CORRECTIONS','Necessary parameter restrictions with actual square-root and field qualification; not an IP certificate; b corrected to a-prime.')
for j,claim,routes,disp,qual in [
(1,'[4], D8',['odd_three'],'PROVED_WITH_ACQUIRED_COMPONENTS',''),
(2,'[k], k|(q−1), split dihedral',['odd_three'],'PROVED_WITH_ACQUIRED_COMPONENTS','Rotation order at least2; q2 trivial split torus supplies no rank2 marking.'),
(3,'[k], k|(q+1), nonsplit dihedral',['odd_three'],'PROVED_WITH_ACQUIRED_COMPONENTS',''),
(4,'[k,4] and[k,k], exact trace-field module',['even_subgroups'],'PROVED_WITH_ACQUIRED_COMPONENTS',''),
(5,'All rank3 types of PSL2(q-prime)',['even_subgroups','R4'],'GROUPS_PROVED_PRIOR_TYPE_CLASSIFICATION_RETAINED','No new complete projective-line rank3 census.'),
(6,'[4,k,4], exact four-dimensional module',['even_subgroups'],'PROVED_WITH_ACQUIRED_COMPONENTS','')]:row(f'Table2.{j}','table',[21],claim,routes,disp,qual)
for j,claim,routes,disp,qual in [
(1,'[k], k|2p, dihedral',['odd_three'],'PROVED_WITH_CORRECTIONS','Unipotent order p, not2(2,p); rank2 marking requires k≥2.'),
(2,'[k], k|(q−1), split dihedral',['odd_three'],'PROVED_WITH_ACQUIRED_COMPONENTS',''),
(3,'[k], k|(q+1), nonsplit dihedral',['odd_three'],'PROVED_WITH_ACQUIRED_COMPONENTS',''),
(4,'[2p,p], D2p squared',['odd_three'],'PROVED_WITH_ACQUIRED_COMPONENTS',''),
(5,'[2p,4] and[4,4], D2p wreath C2',['odd_three'],'PROVED_WITH_ACQUIRED_COMPONENTS',''),
(6,'[2p,p] and[2p,2p], Heisenberg semidirect Klein4',['odd_three'],'PROVED_WITH_ACQUIRED_COMPONENTS',''),
(7,'Generic affine group and its types',['odd_three'],'PROVED_WITH_CORRECTIONS','Actual types[h,h-prime],[h,2p],[h-prime,2p], where h=order(lambda),h-prime=order(-lambda); printed types are false.'),
(8,'S4, types[3,3] and[3,4]',['odd_three'],'PROVED_WITH_ACQUIRED_COMPONENTS','Up to reversal as in the source table.'),
(9,'A5, types[5,3] and[5,5]',['odd_three'],'PROVED_WITH_ACQUIRED_COMPONENTS','Up to reversal as in the source table.'),
(10,'All rank3 projective-line types',['odd_three','R4'],'GROUPS_PROVED_PRIOR_TYPE_CLASSIFICATION_RETAINED','Actual string C-markings only; no arbitrary hypermap transfer.'),
(11,'[p,2p,p], Heisenberg semidirect Klein4',['odd_four'],'PROVED_WITH_ACQUIRED_COMPONENTS',''),
(12,'[3,3,3], PGL2(5)',['odd_four','topic_e'],'PROVED_WITH_ACQUIRED_COMPONENTS','Characteristic5, not merely ambient q5.'),
(13,'[3,5,3], PSL2(11)',['odd_four','topic_e'],'PROVED_WITH_ACQUIRED_COMPONENTS',''),
(14,'[5,3,5], PSL2(19)',['odd_four','topic_e'],'PROVED_WITH_ACQUIRED_COMPONENTS','')]:row(f'Table3.{j}','table',[21],claim,routes,disp,qual)
row('S3.words','auxiliary',[6,7],'Elementary-matrix word and end labels',['rank_four'],'PROVED_WITH_CORRECTIONS','Missing x^-1 factor and swapped subgroup names corrected.')
row('S4.ends','auxiliary',[8,9],'Adjacent translation module, restricted parabolic and negative-sign conic intersection',['rank_five'],'PROVED_WITH_CORRECTIONS','The parabolic is not generally the full point stabilizer; both sign-specific intersections are paid.')
row('S4.six','auxiliary',[10],'Six constructed classes including duals',['rank_five'],'PROVED_WITH_QUALIFICATION','Six ordered oriented marking classes, three unbased polytope classes; no classification of every PSL3(p) rank5 marking.')
row('S4.quadratic','auxiliary',[10],'Quadratic-field directly regular analogue',['rank_five'],'PROVED_WITH_CORRECTIONS','Translation kernel p²=q, not q²; full regular group is PSL3(q) extended by Frobenius.')
row('S5.rank2','auxiliary',[11],'All rank-two isomorphism/order possibilities',['odd_three'],'PROVED_WITH_CORRECTIONS','Not a conjugacy classification; regular unipotent bound repaired.')
row('S5.simplex','auxiliary',[17,22],'Conic simplex and characteristic-five extension fields',['odd_four','rank_obstruction'],'PROVED_WITH_CORRECTIONS','All characteristic5 ambient embeddings included.')
row('S5.direct','auxiliary',[21],'Simple A5/PSL2 ends cannot be directly regular',['odd_four','even_subgroups','rank_obstruction'],'PROVED_WITH_ACQUIRED_COMPONENTS','Actual index2 condition is used.')
row('S7.psu17','new_source_computation',[24],'Three positive PSU3(17) enantiomorphic pairs: types[3,7,3],[3,8,3],[3,9,3]',['unitary_examples'],'PROVED_WITH_ACQUIRED_COMPONENTS','No type-exhaustion claim or all-rank census.')
row('S7.psu_ranks','principal_consequence',[24],'Any unitary chiral polytope has rank4 or5',['rank_obstruction','R5'],'PROVED_WITH_RETAINED_PRIOR_THEOREM','The rank3 exclusion retains its earlier authorship.')
row('S7.psl2_list','historical_context',[24],'The printed small PSL2 negative list',['topic_e'],'CORRECTED_BY_PREVIOUSLY_ACQUIRED_RESULT','q81 is positive of type[40,40,40]; the other eleven values obey the acquired negative criteria.')
for i,claim,routes,pages in [
('C.regular_simple','Prior finite simple regular classification',['R6'],[1,23]),
('C.simple_positive','Prior positive chiral-polyhedron classification',['R11'],[1,24]),
('C.psl2','Prior PSL2 chiral classification/rank bound',['R12'],[1,2,24]),
('C.no_polyhedra','Prior PSL3/PSU3 no chiral-polyhedron theorem',['R5'],[2,24]),
('C.psl3_negative','Prior PSL3 q≤4 negative searches',['R7'],[2,24]),
('C.psu_negative','Prior listed PSU3 negative searches',['R8'],[24]),
('C.psu11','Prior three PSU3(11) pairs',['R9'],[24]),
('C.alt7','Prior Alt7 negative',['R10'],[1,24])]:row(i,'historical_context',pages,claim,routes,'RETAINED_WITH_EXPLICIT_ATTRIBUTION')
row('Q.unitary','historical_question',[24],'Existence for PSU3(q), q>17',[],'RECORDED_WITHOUT_CURRENT_STATUS_CLAIM','No new literature search or resolution.')
row('Q.psl2','historical_question',[24],'PSL2(p^d), p^d=3 mod4,d>1 not a prime power',['topic_e'],'ALREADY_RESOLVED_BY_ACQUIRED_PROJECT_RESULT','Previously accepted coprime-subfield proof, no new question credit.')
save('source_map.json',dict(original='L027',edition='Fixed25-page2022author edition',source=source,clauses=rows,numbered_statements=15,table_rows=21,policy='Complete corrected principal synthesis with every numbered statement, all table rows, all own Section7 positive claims and exact retained historical boundaries; not a new reproduction of cited earlier census data.'))
save('source_ledger.json',dict(primary=[dict(**source,role='fixed source; documentary hash-only at publication'),dict(**ns(S/'sources/phase282_L028_revised.pdf'),role='independently inspected earlier edition for evidence scope, not a substitute for missing census outputs')],source_contract_predecessor=ns(W/'L027_work/source_contract01.json'),text=ns(W/'L027_work/source_text.txt'),section7_audit=ns(W/'L027_section7_routes_audit/report.json'),full_source_pages_read=list(range(1,26))))
save('attribution.json',dict(synthesis_author='l044_resume',root_author='rank_four only; separate mathematical contributions to rank_five disclosed in its accepted packet',other_component_authorship='Exact roles remain in acquired component/review manifests. This synthesis changes none of them.',source_authors=['Dimitri Leemans','Adrien Vandenschrick'],new_synthesis='Complete source joins and inherited-theorem correction for q81; no new finite enumeration.',contract_assistance='publication_recovery read full principal draft for principal/Section7 scope; not a distinct mathematical acceptance.',independent_acceptance_required=True))
save('scope.json',dict(original='L027',status='AUTHOR_PRINCIPAL_ASSEMBLY_AWAITING_DISTINCT_REVIEW',principal_obligations=['T1.1','T1.2','T1.3'],components=8,section7_own_positive='Three PSU3(17) pairs; no exhaustive count inferred.',retained_prior_census=['R7','R8','R9'],literal_corrections_included=True,new_originals_taken_in=0,whole_original_credit=0,new_question_credit=0,new_Lean_credit=0,new_measurements=0))
save('publication_interface.json',dict(principal='principal.tex',complete_written_proof='Principal synthesis followed by the eight exact acquired component manuscripts in components.json; complete_proof.pdf is a concatenation, not a replacement for their TeX.',acquired_roots='components.json',retained_inputs='retained_inputs.json',source_map='source_map.json',source_policy='Full source PDFs, article text and source renders remain documentary hash-only; mathematical data/code/receipts and all predecessor proof/review closures remain acquired.',historical_status_policy='Old bounded packets preserve their original pending/whole-credit wording. Current synthesis joins only their exact accepted bounded claims.',public_writer='root only',measurements='none; no existing measurement record changed'))
save('dependencies.json',dict(files=sorted(deps.values(),key=lambda x:(x['namespace'],x['path'])),closure_boundary='All direct author, distinct-review and root-acceptance exports for eight components, together with exact accepted Topic E and L045 joins. Nested dependencies retain their existing manifests and accepted proof boundaries; they are not re-enumerated by this synthesis.'))
print(json.dumps(dict(components=len(components),clauses=len(rows),retained=len(ret),dependencies=len(deps))))
