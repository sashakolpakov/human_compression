"""Author-side scope assembly from the fixed accepted F010 contract."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parent;study=R.parent;public=study.parent.parent/'math_compression'
def bind(p,base=R):
 b=(base/p).read_bytes();return dict(path=p,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def span(path,start=None,end=None):
 text=(R/path).read_text();a=0 if start is None else text.index(start);b=len(text) if end is None else text.index(end,a+len(start or ''))
 return dict(path=path,start_codepoint=a,end_codepoint_exclusive=b,sha256_utf8=hashlib.sha256(text[a:b].encode()).hexdigest(),scope='Complete named statement/proof or declared context; overlapping locators are not cost partitions')
p='sections/01-recognition.tex'
spans={'UR.Conventions':span(p,end='The following elementary fact'),
'UR.Restriction':span(p,'The following elementary fact','For colored graphs'),
'UR.Components':span(p,'Here is a local criterion'),
'UR.Chambers':span('sections/02-chambers.tex'),
'UR.Cleaning':span('sections/03-cleaning.tex',end='\\begin{corollary}'),
'UR.Conversion':span('sections/03-cleaning.tex','\\begin{corollary}'),
'UR.Attribution':span('sections/04-umbrella-scope.tex'),
'R.MainStatement':span('sections/05-pair-encoding.tex',end='\\begin{theorem}[Ordered-pair'),
'R.PairEncoding':span('sections/05-pair-encoding.tex','\\begin{theorem}[Ordered-pair','\\begin{proof}[Proof of Theorem'),
'R.MainDeduction':span('sections/05-pair-encoding.tex','\\begin{proof}[Proof of Theorem'),
'R.SymmetricFamily':span('sections/06-symmetric-family.tex'),
'R.Hexagon':span('sections/07-hexagon.tex'),
'R.SourceScope':span('sections/08-application-scope.tex')}
old=json.loads((study/'phase177_F010_contract.json').read_text())
mapping={'Theorem3.1':['UR.Conventions','UR.Restriction','R.PairEncoding'],
'Theorem4.1':['UR.Conventions','UR.Restriction','UR.Chambers'],
'Theorem4.2':['UR.Conventions','UR.Restriction','UR.Components','UR.Cleaning'],
'TheoremA':['UR.Conventions','UR.Restriction','R.MainStatement','R.PairEncoding','UR.Chambers','R.MainDeduction'],
'Example5.1':['R.Hexagon','R.SourceScope'],
'Example5.2':['UR.Conventions','UR.Components','UR.Restriction','R.SymmetricFamily','UR.Cleaning','UR.Chambers','R.SourceScope']}
pages={'Theorem3.1':[4,5,6],'Theorem4.1':[6,7,8],'Theorem4.2':[8,9,10],'TheoremA':[2],'Example5.1':[10],'Example5.2':[10,11,12]}
contracts=[dict(id='F010.'+row['source'],inherited_record=row,current_spans=mapping[row['source']],physical_source_pages=pages[row['source']],
 status='corrected_example' if row['source']=='Example5.1' else 'qualified_base_case' if row['source']=='Example5.2' else 'proved_principal_result',
 attribution='Original construction and principal theorem: Díaz Ramos–Molinier–Viruel; common elementary proof organization and explicit local corrections retained from accepted project proof bank.') for row in old['principal_blocks']]
programs=['phase177_hexagon_check.g','phase188_gadget_check.g'];drivers=['phase188_verify.py','phase193_public_check.py'];inventory=[]
for n in programs+drivers:
 p=('programs/' if n in programs else 'drivers/')+n;inventory.append(dict(original=n,copy=p,**{k:v for k,v in bind(p).items() if k!='path'},role='bounded_validation' if n in programs else 'historical_operational_driver',universal_proof_premise=False))
formal=json.loads((R/'formal/scope.json').read_text());maps=[]
for mod in formal['modules']:
 for name in mod['declarations']:
  maps.append(dict(declaration=name,module=mod['file'],written_span='UR.Restriction' if 'RecognizableRestriction' in name else 'R.Hexagon',
   scope='Generic abstract permutation-subgroup interface; no application hypothesis instantiated' if 'RecognizableRestriction' in name else 'Explicit completed-hexagon reflection or C3 obstruction; no full group count'))
pre=[]
for p in ['phase177_F010_contract.json','phase177_export.json','phase177_finite_pair_representation.md','phase188_export.json','phase188_review.json','phase188_F010_independent_review.md']:
 pre.append(dict(namespace='study',**bind(p,study)))
for p in ['research/case_study/phase193_F010_overlay.json','research/case_study/phase193_export.json']:
 pre.append(dict(namespace='public',**bind(p,public)))
docs=[bind(str(p.relative_to(R))) for p in sorted(R.glob('*.tex'))]+[bind(str(p.relative_to(R))) for p in sorted((R/'sections').glob('*.tex'))]+[bind(str(p.relative_to(R))) for p in sorted(R.glob('*.pdf'))]
scope=dict(schema='finite_representation_canonical_contract_v1',status='AUTHOR_COMPLETE_PENDING_INDEPENDENT_REVIEW',source_ids=['F010'],intake_closed=True,
 source=dict(title=old['title'],authors=old['authors'],edition=old['version'],pages=13,primary=bind(old['source'],study)),
 predecessors=pre,inherited_source_block_order=[r['source'] for r in old['principal_blocks']],contracts=contracts,proof_spans=spans,documents=docs,
 complete_scientific_documents=['umbrella','finite-normal-pairs'],full_validation_appendix='program-appendix',
 precise_hypotheses=dict(normal_subgroup_required=True,finite=True,main_nontrivial_rank='[G:H]+3',trivial_rank=1,connected_main_construction=True,
 arbitrary_input_cleaning_need_not_be_connected=True,rank_two_universal_claim=False),
 source_qualifications=['Actual chamber degrees are r-1 and d(v)(r-1).','Completed hexagon pair is (D12,S3), not the printed (D12,C3).','Symmetric-family minimum degree two begins at n=3; the n=2 path has leaves.'],
 exclusions=['No universal fixed-rank-two representation','No optimality of every chamber-completion hypothesis or graph size','No blanket identification of (Sn,An) with (Aut(An),Inn(An))','No unrelated L059 result or computation','No new answer to the source Question 2.4, already settled in its Theorem A'],
 program_inventory=inventory,validation_boundary=dict(full_mathematical_programs=2,complete_archival_drivers=2,
 uniform_written_proof_depends_on_finite_results=False,all_program_bytes_preserved=True,
 explanation='Every universal construction and the complete exceptional groups have written proofs. Existing exact finite checks remain full bounded validation.'),
 formal_scope=bind('formal/scope.json'),formal_statement_map=maps,
 retained_inputs=['Elementary finite group/permutation and connected-component facts; no external graph-representation theorem is an unproved premise','GAP 4.15.1 and GRAPE 4.9.3 exact finite graph/group algorithms for bounded validation','Lean 4.32.2 kernel, pinned mathlib and declared cached dependency objects'],
 original_attribution='The normal-pair theorem, three explicit constructions and symmetric family belong to Antonio Díaz Ramos, Rémi Molinier and Antonio Viruel. Frucht and König are historical antecedents, not additional claimed rederivations.',
 cost_boundary=dict(full_common_paper_charged_once=True,cross_topic_discount=False,full_application_charged=True,full_validation_appendix_alternative_raw_programs=True,
 two_full_operational_drivers_separate=True,prior_own_proof_bank_as_unpriced_logical_premise=False,ratio=None,external_proof_cost=None,source_graphics_cost=None),
 no_whole_assertion_equivalence_claim=True,new_source_credit=0,new_question_credit=0,new_formal_declarations=8,reused_formal_reports=4)
(R/'scope.json').write_text(json.dumps(scope,indent=2,ensure_ascii=False)+'\n')
print('scope: six inherited blocks,',len(spans),'complete spans,',len(maps),'formal reports')
