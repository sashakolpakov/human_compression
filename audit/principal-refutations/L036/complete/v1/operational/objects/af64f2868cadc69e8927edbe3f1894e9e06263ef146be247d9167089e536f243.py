"""Assemble exact accepted L036 components; no mathematical acquisition."""
from pathlib import Path
import hashlib
import json
import shutil

C=Path(__file__).resolve().parent
P=C.parent
S=P.parents[1]
R=Path('/Users/sasha/medusa/math_compression')

def pin(p,base=None):
 b=p.read_bytes(); return dict(path=str(p.relative_to(base) if base else p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def dump(name,data): (C/name).write_text(json.dumps(data,indent=2)+'\n')

proofs=[
 ('principal',R/'corrections/rudvalis-rank-two/v1/proof/orbit_bound'),
 ('theory',P/'character_application/theory'),
 ('characters',P/'character_application/totals'),
 ('marks',P/'table_application/applications'),
 ('algorithm',P/'algorithm_scope/scope'),
]
(C/'proofs').mkdir(exist_ok=True)
imports=[]
for name,stem in proofs:
 for ext in ['.tex','.pdf']:
  source=stem.with_suffix(ext); dst=C/'proofs'/(name+ext)
  shutil.copyfile(source,dst)
  imports.append(dict(source=pin(source),destination=pin(dst,C),mode='EXACT'))
shutil.copyfile(P/'m11_application/tables.tex',C/'proofs/tables.tex')
imports.append(dict(source=pin(P/'m11_application/tables.tex'),destination=pin(C/'proofs/tables.tex',C),mode='EXACT'))
deltas=[]
for old,new,changes in [
 ('method.tex','m11.tex',[
  ('\\section{The order-forty-eight name}','\\section{Identifying $\\mathrm{GL}_2(3)$}',1),
  ('Section 3 of the source defines','Section 2 (physical page 3) of the source defines',1)]),
 ('corrections.py','m11_corrections.py',[
  ('Section3 defines','Section2 (physical page3) defines',1)]),
 ('source_join_corrected.json','m11_source_join_corrected.json',[
  ('Section3 defines','Section2 (physical page3) defines',4)]),
]:
 source=P/'m11_application'/old; dst=C/'proofs'/new
 text=source.read_text()
 for before,after,count in changes:
  if text.count(before)!=count: raise ValueError('unexpected edition delta')
  text=text.replace(before,after)
 dst.write_text(text)
 deltas.append(dict(source=pin(source),destination=pin(dst,C),replacements=[dict(before=a,after=b,count=n) for a,b,n in changes],mathematics_changed=False))
dump('imports.json',imports)
dump('edition_deltas.json',dict(frozen_application_unchanged=True,changes=deltas,reason='Correct our Section3 citation to Section2, physical page3, and use a plain descriptive heading. No source value, proof argument, calculation, or accepted application is altered.'))

characters=json.loads((P/'character_application/arithmetic01.json').read_text())
marks=json.loads((P/'table_application/results.json').read_text())
m22=json.loads((P/'character_application/imports.json').read_text())
groups=[]
for g in characters['groups']:
 groups.append(dict(name=g['name'],automorphism_group=g['name'],route='complete Maxes list and compatible character fusions',maximal_classes=g['maximal_classes'],maximal_table_names=g['maximal_table_names'],indices=g['indices'],normalizer_is_maximal=True,count=g['unordered_pair_orbits'],input=pin(P/'character_application/arithmetic01.json'),premises=['Named nonabelian simple group','Trivial outer automorphism group','CTblLib Maxes completeness and compatible fusions']))
for g in marks['counts']:
 if not g['name'].endswith('.2'): continue
 groups.append(dict(name=g['name'][:-2],automorphism_group=g['name'],route='complete automorphism-group table of marks',socle_class=g['socle_class'],maximal_classes=g['maximal_classes'],maximal_orders=g['maximal_orders'],normalizer_classes=g['normalizer_classes'],normalizer_orders=g['normalizer_orders'],count=g['unordered_pair_orbits'],input=pin(P/'table_application/results.json'),premises=['Named nonabelian simple socle and full automorphism group','Complete TomLib subgroup table','Compatible cyclic and squared-element class data']))
groups.append(dict(name='M22',automorphism_group='Aut(M22)',route='accepted L073 census',count=81,input=m22['admission'],premises=m22['retained_premises'],source_import=m22))
order=['M11','M12','M22','M23','M24','J1','J2','J3','HS','McL','He','Ru']
groups.sort(key=lambda g:order.index(g['name']))
dump('group_inputs.json',dict(groups=groups,library_editions=dict(GAP='4.15.1',CTblLib='1.3.11',TomLib='1.2.11'),parameter_set='Theorem1 in completion.tex: off-diagonal normalizer double cosets, diagonal nontrivial double cosets modulo inversion',sum_of_counts=sum(g['count'] for g in groups),external_representative_files_verified=False,characters_identify_embeddings=False))

rows=[]
def add(label,pages,status,proof,qualification,attribution):
 rows.append(dict(label=label,physical_pages=pages,status=status,proof=proof,qualification=qualification,attribution=attribution))
add('Theorem 2.1: coset incidence and flags of size at most two',[2],'REPROVED_BORROWED_RESULT','completion.tex, first three paragraphs','Objects retain their types even when subgroups or coset sets agree; no higher-rank flag-transitivity claim.','Source attributes the construction to Tits [14].')
add('Rank-two firmness, connectedness, primitivity and equivalence',[2,3],'REPROVED','completion.tex, Theorem1 and preceding coset argument','Distinct maximal proper subgroups; automorphisms of the distinguished group, allowing duality.','Definitions and equivalence are those of the source; the proof is elementary coset theory.')
add('Section 3.1: previous algorithm',[3,4],'EXPLICIT_BORROWED_BACKGROUND','completion.tex scope; corrected algorithm note','The cited Dehon algorithm and its higher-rank tests are background, not a new higher-rank classification here.','Source explicitly attributes this sketch to Dehon and Dehon--Leemans [6,7].')
add('Section 3: unrestricted faithfulness of a maximal coset action',[4],'REFUTED_AND_HYPOTHESIS_IDENTIFIED','proofs/algorithm.tex, Proposition1 and order-four example','Faithfulness holds when the maximal subgroup has trivial core, including the twelve nonabelian simple groups.','Core identity is classical; the explicit diagnosis and witness belong to this treatment.')
add('Algorithm 3.1: unrestricted inverse-image output',[4,5],'REFUTED_AND_REPAIRED','proofs/algorithm.tex, Proposition1 and Theorem2','Retain the original second subgroup and lift only the point stabilizer; require complete maximal list and exact Aut equivalence.','Source supplies orbit method; kernel correction and counterexample are added here.')
add('Algorithm 3.1: undefined K variable',[5],'NOTATION_TYPO_IDENTIFIED','proofs/algorithm.tex, paragraph after Proposition1','Reading K as the image subgroup does not fix the distinct core problem.','Printed pseudocode is quoted by position, with this diagnosis attributed to this treatment.')
for g in groups:
 route=g['route']
 proof=('proofs/characters.tex' if g['name'] in ['M11','M23','M24','J1','Ru'] else ('accepted L073 import in group_inputs.json' if g['name']=='M22' else 'proofs/marks.tex'))
 add('Table 1: '+g['name'],[5],'CORRECTED_EXACT_COUNT' if g['name']=='Ru' else 'RECOVERED_EXACT_COUNT',proof+'; completion.tex Theorem1; group_inputs.json','Full Aut equivalence; complete named-group/library premises. Corrected count '+str(g['count'])+'.','Source count is prior work; '+route+'. Ru principal refutation was already accepted and gets no second credit.')
for label,page,cells in [('Table 2: M11 suborbits',6,25),('Table 5: M12 suborbits',9,121),('Table 6: M22 suborbits',10,64),('Table 7: M23 suborbits',10,49),('Table 8: J1 suborbits',11,49)]:
 add(label,[page],'RECOVERED_NUMERICAL_ARRAY','proofs/theory.tex product theorem; proofs/marks.tex; accepted source_join.json',str(cells)+' numerical cells unchanged. All permitted equal-degree joins retained; classical shape lists remain explicit premises.','Original numerical array attributed to source; product of marks is classical; exact arithmetic and joins are supplied here.')
add('Table 7: the two index-253 M23 subgroup labels',[10],'CORRECTED_TWO_LABELS','proofs/marks.tex normal-E16 proof','Class201 is 2^4:A7 and class202 is L3(4):2; numeric array unchanged; complete cyclic fusion and classical two-shape list required.','Printed labels belong to source; positive normal-subgroup test and correction belong to this treatment.')
add('Section 4.1 and 4.2: preliminary 38 and 268 counts',[6],'RECOVERED_WITH_DUALITY_EXPLAINED','proofs/marks.tex, suborbit section; completion.tex Theorem1','Upper-triangle totals38/268, inner totals37/255 and full M12 total166 are different quantities.','Source reports preliminary totals; inversion and full Aut distinctions are made explicit here.')
add('Table 3: all 37 M11 geometries and named intersections',[7],'RECOVERED_WITH_FOUR_ORIENTATION_CORRECTIONS','proofs/m11.tex and tables.tex; accepted M11 finite certificate','All47586 pairs covered. Source rows12/18 become[4,2,3],23/35 become[4,3,3]. Ambiguous profiles10/11 and16/17 retain both joins.','Source supplies rows; literal intersections import accepted L054 structures; finite enumeration and typed-diameter corrections are supplied here.')
add('Table 4: 70 M11 design parameter entries',[8],'RECOVERED_UNCHANGED','proofs/m11.tex and tables.tex; independent subset-count certificate','Actual point orientation recorded separately from Table3 subgroup order.','Source parameters are prior results; complete finite verification supplied here.')
add('Section 4.1: omitted rows 31/32 and Steiner row 28 star',[6,8],'QUALIFIED_DESIGN_CONVENTION_AND_RECOVERED_PARAMETERS','proofs/m11.tex; completion.tex correction ledger','Rows31/32 are complete incidence with repeated full blocks and satisfy literal counts; proper/simple-block convention explains exclusion. Row28star is a4-(11,5,1)design, the classical small Witt design description. No separate uniqueness theorem or automorphism classification asserted.','Source identifies Steiner system; our certificate proves its displayed design parameters.')
add('Comparison with earlier M11, M22 and M23 totals',[2,6],'RECOVERED_NUMERICAL_COMPARISON','completion.tex and accepted L073 import','Exact37,81,170 agree with the present source. Earlier papers receive no new completion credit here.','Earlier totals and historical comparison belong to the cited authors.')
add('Table 1 standard group orders and chosen action degrees',[5],'EXPLICIT_NAMED_GROUP_DATA','group_inputs.json and accepted named-group data','Classification and chosen representation degrees are documentary/group-library premises, not a new classification.','Classical sporadic group data and source chosen actions.')
add('Reported runtimes and claimed implementation speedup',[2,4,5],'ATTRIBUTED_EMPIRICAL_REPORT','completion.tex, final scope','No speedup, reproduction of historical hardware, or complexity factor claimed.','Original authors\' historical measurements only.')
add('Electronic geometry files linked on page 2',[2],'EXTERNAL_ARTIFACTS_UNVERIFIED','completion.tex, final scope; group_inputs.json','The fixed paper receives a complete mathematical parameter set and exact counts. Downloadable file contents, one-to-one file matching and their data-edition completeness are not certified.','Original authors\' linked external datasets; not used as proof premises.')
add('Introductory McLaughlin codes',[1],'EXPLICIT_CITED_BACKGROUND','completion.tex, final scope','The source refers to its separate code paper [13]; no independent code theorem or manuscript credit here.','Source reference[13], not a new result of the fixed twelve-page article.')
add('Higher-rank algorithm extension and conjectured cause of old M22 error',[12],'FUTURE_WORK_AND_HISTORICAL_SPECULATION','completion.tex, final scope','No solved-conjecture credit; the source labels these as future work and likely explanation.','Source concluding remarks.')
add('Table 1 caption says eleven while table has twelve groups',[5],'CAPTION_COUNT_TYPO_IDENTIFIED','group_inputs.json, twelve entries','Only caption word changes; no mathematical count altered.','Printed source caption; arithmetic count supplied here.')
ledger=dict(source_id='L036',source_edition='Art Discrete Appl Math 2 (2019), P1.08, fixed twelve-page journal PDF',source_pdf=pin(S/'sources/catalogue_L036.pdf'),source_text=pin(S/'reboot_20261013/L036_work/source.txt'),claims=rows,principal_disposition='principal_statement_refuted',proposed_complete_disposition='COMPLETE_CORRECTED_FIXED_SOURCE_TREATMENT',ordinary_recovery_credit=0,new_principal_refutation_credit=0,new_original_credit=0,new_named_open_questions_solved=0,new_Lean_declarations=0,new_measurements=0,public_registration_performed=False,principal_acquisition_repeated=False,remaining_fixed_paper_mathematical_claims=[],external_representative_files_verified=False,external_dataset_obligation_promoted=False,borrowed_premises=['Classical named sporadic groups, simplicity, automorphism groups and maximal subgroup shape lists','Complete pinned CTblLib/TomLib data and compatible fusions, centralizers and square maps','Previously accepted L073 census and L054 literal structural imports','Classical Tits coset construction, Burnside counting, mark products and cited Dehon background'],uncertified_extensions=['Contents and completeness of external downloadable representative files','Higher-rank extension proposed as future work','Historical timings and a claimed speedup, not independently benchmarked','General formal verification in Lean and compression measurement'])
dump('claims.json',ledger)

roots=[P/'character_application',P/'table_application',P/'algorithm_scope',P/'m11_application',P/'character_application_root_review',P/'table_application_root_review',P/'algorithm_scope_review_adoption',P/'m11_application_root_review']
deps={}
def addpin(row):
 path=Path(row['path']); actual=pin(path)
 if actual!=row: raise ValueError('changed source binding '+str(path))
 if str(path) in deps and deps[str(path)]!=row: raise ValueError('conflicting binding')
 deps[str(path)]=row
for root in roots:
 for filename in ['manifest.json','dependencies.json']:
  f=root/filename
  if f.exists():
   addpin(pin(f))
   obj=json.loads(f.read_text())
   if filename=='dependencies.json':
    for row in obj: addpin(row)
 for row in json.loads((root/'manifest.json').read_text())['exports']:
  addpin(dict(row,path=str(root/row['path'])))
for x in imports: addpin(x['source'])
for x in deltas: addpin(x['source'])
for f in [R/'audit/principal-refutations/L036/v1/admission.json',S/'sources/catalogue_L036.pdf',S/'reboot_20261013/L036_work/source.txt',R/'audit/topic-mathieu/v1/admission.json']:
 addpin(pin(f))
dump('dependencies.json',[deps[k] for k in sorted(deps)])
print(json.dumps(dict(claims=len(rows),dependencies=len(deps),counts=sum(g['count'] for g in groups))))
