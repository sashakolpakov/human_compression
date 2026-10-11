#!/usr/bin/env python3
"""Bind the private chamber edition; this script does not establish its proofs."""
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parent
STUDY=ROOT.parent
PUBLIC=STUDY.parents[1]/'math_compression'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def item(p,root):return dict(path=str(p.relative_to(root)),sha256=sha(p),bytes=p.stat().st_size)
def write(name,obj): (ROOT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')

def main():
    primary=[('L008','sources/chirality_test2026.pdf','Complete ten-page arXiv2511.14562v1; November2025'),
      ('N016','phase57_ten_source_measurement_sources/N016.pdf','Complete eight-page author edition dated25July2023; publisherPDFunacquired'),
      ('FLW','sources/hypertopes_accepted2016.pdf','Retained historical attribution and exact Theorem8.2; selected reading'),
      ('CPexcerpt','phase41_chiral_cover_tight_excerpts_web.txt','Retained Proposition4.2/Table4 excerpts only; not a full classification review')]
    sources=[dict(id=i,edition=e,**item(STUDY/p,STUDY)) for i,p,e in primary]
    prior=[('incidence_compression.md','Existing L008 written reduction §§1–3; archived source, not free hidden premise'),
      ('phase41_chiral_cover_manuscript.md','Complete prior N016 proof bank; reworked, not imported as a theorem'),
      ('phase41_chiral_cover_ledger.md','Earlier exact source clauses and attribution'),
      ('phase41_chiral_cover_manifest.json','Earlier author freeze'),
      ('phase43_chiral_cover_root_audit.json','Distinct earlier full mathematical/source/program acceptance'),
      ('phase43_chiral_cover_root_audit.md','Complete distinct earlier review narrative'),
      ('phase63_ten_source_measurement_recent_audit_report.json','Independent full eight-page acquired N016 PDF and edition review')]
    prior=[dict(role=r,**item(STUDY/p,STUDY)) for p,r in prior]
    spans={}
    def split(path,entries):
        text=(ROOT/path).read_text()
        for i,(key,start) in enumerate(entries):
            a=text.index(start);end=entries[i+1][1] if i+1<len(entries) else None
            b=text.index(end,a+len(start)) if end else len(text)
            data=text[a:b].encode();spans[key]=dict(path=path,start_anchor=start,end_anchor=end,bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
    split('sections/01-fibers.tex',[('U.Fiber','\\begin{theorem}[The extension fiber]'),('U.TwoFiber','\\begin{corollary}')])
    split('sections/02-chambers.tex',[('U.Propagation','\\begin{lemma}[Propagation'),('U.Reflection','\\begin{theorem}[Two regular orbits]')])
    split('sections/03-mirrors.tex',[('U.Transport','\\begin{theorem}[Intersection transport]'),('U.Mirror','\\begin{theorem}[The invariant relation kernel]'),('U.Correspondence','\\subsection{The geometric input'),('U.LocalMirror','\\subsection{Local mirrors'),('U.PrimeMinimal','\\begin{lemma}[Prime degree')])
    split('sections/hypertope.tex',[('H.Marking','\\section{The marking'),('H.Neighbors','\\section{Neighbors'),('H.Residues','\\section{Every residue'),('H.FullGroup','\\section{The full automorphism'),('H.Scope','\\section{Source scope')])
    split('sections/covers-01.tex',[('R.Local','\\section{Compatible'),('R.RegularEnd','\\begin{lemma}[A regular end]'),('R.Criterion',"\\begin{theorem}[Cunningham's criterion]"),('R.Corollaries','\\section{All general')])
    split('sections/covers-02.tex',[('R.Torus','\\subsection{Chiral square'),('R.Atomic','\\subsection{The five atomic')])
    split('sections/covers-03.tex',[('R.Finite','\\section{Two distinct')])
    split('sections/covers-04.tex',[('R.Scope','\\section{Attribution')])
    rows=[]
    def row(id,source,locator,claim,refs,status='recovered',retained=()):
        rows.append(dict(id=id,source_id=source,source_locator=locator,claim=claim,status=status,new_proof_spans=refs,retained_inputs=list(retained)))
    row('H01','L008','Theorem1.1, physicalpp2,7–8','Finite chirality criterion, with all listed tests and both directions',['H.Marking','H.Neighbors','H.Residues','H.FullGroup','U.Fiber','U.Reflection'])
    row('H02','L008','Theorem1.1 product cardinality clause','For infinite groups use exact two-coset fiber; numerical cardinal equality alone is insufficient',['U.TwoFiber','H.Marking'],'qualified_infinite_formulation')
    row('H03','L008','Theorem1.1(ii); §2.3 IC+','Panel stabilizers trivial from the stated C+ intersection condition',['H.Marking'])
    row('H04','L008','Theorem1.1(i), proofp7','One truncation plus two-coset fiber implies transitivity on every proper flag type',['U.Fiber','H.Neighbors'])
    row('H05','L008','Theorem1.1 proofp7 thinness','Exactly two completions per panel, including for infinite G',['H.Neighbors'])
    row('H06','L008','Theorem1.1 proofpp7–8 residualconnectedness','Connected residues, with actual second matching in ranktwo',['H.Residues'])
    row('H07','L008','Theorem1.1(iv); FLW2016 Theorem8.2','Actual marked inversion extends to chamber reflection and hence geometry; converse',['U.Propagation','U.Reflection','H.FullGroup'])
    row('H08','L008','Theorem1.1 necessity','Designated group has the required two free orbits without assuming it is full Aut beforehand',['H.FullGroup','U.Propagation'])
    row('H09','L008','Section5 three Magma functions, pp8–10','Printed source software and ancillary claims are outside the admitted principal replacement boundary',['H.Scope'],'excluded_ancillary_implementation')
    row('R01','N016','Proposition2.2,p4','Regular facet or vertexfigure forces polytopal smallest cover',['R.RegularEnd','U.Transport','U.LocalMirror'],retained=['string_Cplus_correspondence','direct_regular_sections'])
    row('R02','N016','Proposition2.3,p4','Ends of the mirror mix are polytopal; remaining test is the end intersection',['R.RegularEnd','R.Criterion'],retained=['depth_two_regular_sections','recursive_Cplus'])
    row('R03','N016','Proposition2.4,p5','Chirality is the first-coordinate second-projection kernel',['U.Mirror','U.LocalMirror'])
    row('R04','N016','Theorem3.1,p5','Embedded local chirality intersection criterion',['R.Criterion','R.RegularEnd','U.Transport','U.LocalMirror'],retained=['string_Cplus_correspondence','depth_two_regular_sections'])
    row('R05','N016','Remark3.2,p6','Regular-end specialization',['R.Corollaries'])
    row('R06','N016','Corollary3.3,p6','Regular medial section; exact embedded intersection statement',['R.Corollaries'])
    row('R07','N016','Corollary3.4,p6','Rankfour criterion excludes nonidentity powers, correcting literal no-power wording',['R.Corollaries'],'recovered_with_identity_wording_correction')
    row('R08','N016','Example3.5,p6','All five exact retained atomic-family parameter ranges have nonpolytopal smallest cover',['R.Atomic','R.Corollaries','U.LocalMirror'],retained=['CP_Table4_families','CP_prime_chirality'])
    row('R09','N016','Proposition3.6,p6','Totally chiral ends iff totally chiral medial for polytopal cover',['R.Corollaries'])
    row('R10','N016','Corollary3.7,p6','Every chiral extension with the stated facet-kernel intersection has polytopal smallest cover; no existence assertion',['R.Corollaries'])
    row('R11','N016','Example3.8,p6','All source squaretorus facets satisfy the extension condition',['R.Torus','R.Corollaries'],retained=['square_tessellation_model'])
    row('R12','N016','§4firstparagraph,p6','If smallest regular cover is polytopal it is unique minimal; infinite covers allowed',['U.Mirror','U.PrimeMinimal'])
    row('R13','N016','§4Ppresentation,p7','Literal chiral P has648flags',['R.Finite'],retained=['GAP_exact_algorithms','string_Cplus_correspondence'])
    row('R14','N016','§4R,p7','Mirror mix R is smallest regular cover with1944flags and fails polytopality',['R.Finite','U.Mirror','U.Transport'],retained=['GAP_exact_algorithms','string_Cplus_correspondence'])
    row('R15','N016','§4Tanddual,p7','Literal T is trivial facet extension, Td its exact dual',['R.Finite'],retained=['GAP_exact_algorithms','two_facet_interpretation'])
    row('R16','N016','§4QandQprime,p7','Two distinct5832flag threefoldcovers are minimal regular polytope covers',['R.Finite','U.PrimeMinimal','U.Mirror'],retained=['GAP_exact_algorithms','marked_cover_correspondence'])
    row('R17','N016','§4generalexpectation,pp6–7','Source question is not an application theorem; later unrestricted answer separatelybound',['R.Scope'],'separate_question_not_principal_credit')
    row('R18','N016','§4finalparagraph,p7','Five-family multiplicity question separate from source proved conclusions; later admitted work separatelybound',['R.Scope'],'separate_question_not_principal_credit')
    write('scope.json',dict(status='AUTHOR_COMPLETE_PENDING_INDEPENDENT_REVIEW',principal_contracts=['L008:Theorem1.1','N016:all proved July25 2023 author conclusions'],principal_count_unchanged=2,project_principal_count_unchanged=27,whole_manuscript_all_assertions_claim=False,counts=dict(L008=9,N016=18,proof_spans=len(spans)),source_bindings=sources,prior_bindings=prior,proof_spans=spans,rows=rows,retained_input_full_expansion_cost=None,new_question_credit=0,compression_factor=None))
    programs=[]
    for path,role,required,printed in [('programs/chiral_cover.g','mathematical premise: all six finite group rows and maps',True,True),('programs/reflection_models.py','bounded validation and assumption countermodels; no uniform theorem premise',False,True),('programs/archived_author_driver.py','historical operational runner, copied complete but not executed',False,False),('programs/archived_review_driver.py','historical independent operational runner, copied complete but not executed',False,False),('check.py','current operational replay, binding, rendering and mutation driver',False,False)]:
        if (ROOT/path).exists(): programs.append(dict(role=role,required_mathematical_premise=required,printed=printed,**item(ROOT/path,ROOT)))
    write('program_inventory.json',dict(programs=programs,required_mathematical_files=1,diagnostic_files=1,archival_drivers=2,current_drivers=1,programs_appendix='programs.pdf',complete_required_program_charged_once=True,diagnostic_program_printed_separately=True,historical_L008_software='Three visible Magma functions appear in the acquired full primary; no claim of zero historical code. Underlying software implementation cost unknown.',historical_N016_software='Source reports RAMP use, without the complete source computation script; unreported historical code length remains unknown.',historical_code_cost=None))
    reports={'LiftCertificate':4,'ChamberOrbit':3,'TwoOrbitReflection':7}
    scopes={'LiftCertificate':{'used_declarations':['LeemansLift.intersection_of_image_and_kernel'],'written_interface':'U.Transport','unused_declarations':'Other three retained declarations are compiled but not premises of these applications.'},'ChamberOrbit':{'used_declarations':['LeemansChamberOrbit.all_in_base_orbit_of_closed','LeemansChamberOrbit.orbit_closed_of_base_neighbors'],'written_interface':'H.FullGroup adjacency-closed union argument uses the same propagation principle; exact geometry instantiation remains written.','unused_declarations':'Transitive unique-panel-mate specialization is evidence only, not the chiral action.'},'TwoOrbitReflection':{'used_declarations':['MathCompression.TwoOrbitReflection.actual_reflection'],'written_interface':'U.Reflection explicit positive construction, actual G×Bool neighbor/translate/reflect formulas.','unformalized':'Residual connectivity, chamber reconstruction, necessity and full automorphism classification remain written.'}}
    modules=[dict(reports=n,scope=scopes[name],**item(ROOT/'formal'/(name+'.lean'),ROOT)) for name,n in reports.items()]
    write('formal/scope.json',dict(status='AUTHOR_SCOPED_FORMAL',modules=modules,total_axiom_reports=14,new_axiom_reports=7,end_to_end_application_formalized=False,excluded_available_components=['TorsorPartitions.lean','CoverCharacterSeparation.lean','QuotientIntersectionCriterion.lean'],exclusion_reason='Not required by these complete written proof routes; no declaration is silently treated as a source-specific certificate.'))
    questions=[dict(id='general_unrestricted',statement='Every abstract polytope of finite rank has a minimal regular polytopal cover, unique iff marked monodromy is a string C-group; covers may be infinite.',proof_premise_here=False,accepted_record=item(PUBLIC/'research/case_study/phase223_question_update.json',PUBLIC),review=item(PUBLIC/'research/case_study/phase222_manifest.json',PUBLIC)),dict(id='finite_rank_four',statement='For finite rankfour actual polytopes with non-C monodromy, infinitely many finite minimal regular covers; not allrankfinite theorem.',proof_premise_here=False,accepted_record=item(PUBLIC/'research/case_study/phase274_export.json',PUBLIC)),dict(id='interval_extension',statement='A local interval regular-cover family extends to global finite regular covers, with exact hypotheses in the separate interval theorem.',proof_premise_here=False,accepted_record=item(PUBLIC/'research/case_study/phase280_export.json',PUBLIC)),dict(id='allrankfinite',statement='General finite minimal-cover multiplicity in all ranks remains unresolved in this closed corpus.',proof_premise_here=False,accepted_record=None)]
    baselines=[]
    for stem in ['finite-rank-four-covers','interval-covers','coprime-obstruction']:
        baselines.append(dict(role='Separate accepted question or obstruction proof; not an imported common premise; any future use must charge its complete needed proof.',**item(PUBLIC/'papers/questions'/(stem+'.tex'),PUBLIC)))
    write('question_map.json',dict(status='RECORDED_EXISTING_ANSWERS_NOT_NEW_CREDIT',questions=questions,separate_prior_baselines=baselines,warning='Do not read stale phase41/registry unresolved labels as overriding later admissions. The rankfive arbitrary-marked-group obstruction is not actual polytope monodromy.'))
    print(json.dumps({'status':'BOUND','rows':len(rows),'spans':len(spans),'program_files':len(programs)}))
if __name__=='__main__':main()
