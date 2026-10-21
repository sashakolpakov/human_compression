#!/usr/bin/env python3
"""Bind the complete six-source U+A edition and its actual shared proof cost."""
import argparse,copy,difflib,hashlib,json,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def sha(b):return hashlib.sha256(b).hexdigest()
def binding(name):
 p=ROOT/name;b=p.read_bytes();return {'path':name,'sha256':sha(b),'utf8_bytes':len(b)}
def span(s,a,b):
 t=s[a:b];return {'start_codepoint':a,'end_codepoint_exclusive':b,'sha256_utf8':sha(t.encode()),'utf8_bytes':len(t.encode()),'codepoints':len(t),'plain_NFC_whitespace_tokens':len(unicodedata.normalize('NFC',t).split())}
def sections(s):
 ms=list(re.finditer(r'^## ([1-9])\. .*$',s,re.M));out={}
 for i,m in enumerate(ms):
  end=ms[i+1].start() if i+1<len(ms) else s.index('## Appendix C.')
  out[m.group(1)]={'section':m.group(1),**span(s,m.start(),end)}
 return out

def diff(old,new):
 a=old.splitlines(keepends=True);b=new.splitlines(keepends=True);ops=[];adds=removes=0
 for tag,i,j,k,l in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
  if tag=='equal':continue
  rb=len(''.join(a[i:j]).encode());ab=len(''.join(b[k:l]).encode());adds+=ab;removes+=rb
  ops.append({'operation':tag,'old_line_start_zero':i,'old_line_end_exclusive':j,'new_line_start_zero':k,'new_line_end_exclusive':l,'removed_utf8_bytes':rb,'added_utf8_bytes':ab})
 if adds-removes != len(new.encode())-len(old.encode()):raise RuntimeError('Diff accounting mismatch')
 return {'gross_added_bytes':adds,'gross_removed_bytes':removes,'signed_net_bytes':adds-removes,'operations':ops}
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--output-dir',type=Path,required=True);z=ap.parse_args()
 if z.output_dir.exists() or z.output_dir.is_symlink():raise SystemExit('Refusing existing output directory')
 old_u=(ROOT/'phase123_umbrella_manuscript_v2.md').read_text();u=(ROOT/'phase138_umbrella_v3.md').read_text()
 old_a=(ROOT/'phase117_two_group_application.md').read_text();a=(ROOT/'phase138_module_A_v2.md').read_text()
 extension=(ROOT/'phase130_typed_helly_L034.md').read_text();erratum=(ROOT/'phase130_geometry_erratum.md').read_text();n009_erratum=(ROOT/'phase138_N009_decomposition_erratum.md').read_text()
 old_c=json.loads((ROOT/'phase123_umbrella_v2_contracts.json').read_text());old_l=json.loads((ROOT/'phase117_two_group_application_ledger_checkpoint04.json').read_text());h=json.loads((ROOT/'phase130_intake.json').read_text())
 uc=copy.deepcopy(old_c);uc['schema']='phase138_umbrella_v3_contracts';uc['status']='integrated_author_candidate_pending_independent_review';uc['manuscript']=binding('phase138_umbrella_v3.md');uc['input_bindings']=[binding('phase123_umbrella_v2_contracts.json'),binding('phase130_intake.json'),binding('phase130_geometry_erratum.md')]
 for c in uc['contracts']:
  for key in ['statement_binding','complete_proof_binding']:
   b=c[key];t=old_u[b['start_codepoint']:b['end_codepoint_exclusive']]
   if u.count(t)!=1:raise RuntimeError('Old U proof not preserved: '+c['id']+' '+key)
   start=u.index(t);c[key]={'id':b['id'],**span(u,start,start+len(t))}
  c['formal_coverage_record_is_inherited_historical_U_v2_scope']=True
  if c['id']=='U.SK':
   c['previous_formal_coverage']=c['formal_coverage']
   c['formal_coverage']={'status':'reviewed complete support-induction, generation, exact-profile and IP core; written theorem hypotheses still explicitly bound in applications','file':'formal/SupportedKernelGeneration.lean','declaration':'MathCompression.SupportedKernelGeneration.supported_kernel_construction','complete_application_Lean':False}
   c['formal_coverage_record_is_inherited_historical_U_v2_scope']=False
  c['previous_statement_and_proof_bytes_preserved']=True
  c['consumer_status']='existing admitted five-source usage retained; integrated six-source binding pending independent review'
 for name,starttoken,endtoken,deps in [
  ('U.SK.Helly','**Theorem U.SK.Helly','**Corollary U.SK.Geometry',[]),
  ('U.SK.Geometry','**Corollary U.SK.Geometry','A sufficient alternative',['U.SK','U.SK.Helly','U.Geometry'])]:
  start=u.index(starttoken);proof=u.index('*Proof.*',start);end=u.index(endtoken,proof)
  uc['contracts'].append({'id':name,'statement_exact_markdown':u[start:proof],'statement_binding':{'id':'statement:'+name,**span(u,start,proof)},'complete_proof_binding':{'id':'proof:'+name,**span(u,proof,end)},'dependencies':deps,'retained_inputs':[],'provenance_kind':'integrated_reviewed_coordinate_kernel_proof_with_mandatory_involutivity_correction','historical_novelty_claim':False,'open_conjecture_claim':False,'intended_application_A_consumers':['A4.1','A.H'],'consumer_status':'six-source integrated candidate pending independent review','formal_coverage':{'status':'written_complete; phase137 author-frozen marked transfer and SK specialization pending independent admission' if name.endswith('Helly') else 'written_complete; geometry and involutivity not Lean-certified','complete_source_application_Lean':False}})
 uc['theorem_count']=len(uc['contracts']);uc['historical_provenance_fields_reference_unchanged_U_v2_proofs']=True
 uc['formal_scope_addendum']='phase138_scope.md';uc['fresh_lean_compilation_in_this_phase']=False;uc['complete_formalization_claim']=False
 sl=sections(a);os=sections(old_a);preserved={}
 for key in ['2','5','6','8']:
  x=os[key];y=sl[key]
  if old_a[x['start_codepoint']:x['end_codepoint_exclusive']]!=a[y['start_codepoint']:y['end_codepoint_exclusive']]:raise RuntimeError('Unchanged A branch modified '+key)
  preserved[key]=y
 for start,end in [('## 7. Exhaustive bounded classification','The retained decompositions are'),('Only the finite scope is used;','## 8. Free extensions')]:
  p0=old_a.index(start);p1=old_a.index(end,p0);t=old_a[p0:p1]
  if a.count(t)!=1:raise RuntimeError('Unchanged classification proof modified')
  preserved[start]={'sha256_utf8':sha(t.encode()),'utf8_bytes':len(t.encode())}
 # Full old affine proof remains a literal prefix before the new decomposition subsection.
 x=os['3'];old_affine=old_a[x['start_codepoint']:x['end_codepoint_exclusive']]
 if a.count(old_affine)!=1:raise RuntimeError('Old affine proof changed')
 rows=copy.deepcopy(old_l['contract_rows'])
 for row in rows:
  row['proof_locations']=[sl[v['section']] for v in row['proof_locations']]
  row['use_map_status']='actual_derivation_bound_to_integrated_U_v3_author_candidate'
  row['full_Lean_verification']=False
  row['previous_contract_statement_preserved']=True
 for row in rows:
  if row['id']=='A.N009.23':
   row['structural_background_correction']='Printed diagonal pairing corrected to <b,b^(ac)> x <b^a,b^c>, proved by A3.2 and §7.4 for every positive parameter; classification/presentations/orders remain retained.'
   row['application_derivation']='retained finite smooth-quotient classification; structural decomposition now proved by A3.2 and its explicit §7.4 marking check'
   row['mandatory_predecessor_erratum']=binding('phase138_N009_decomposition_erratum.md')
 # All previously accepted target text and import boundaries remain exact.
 if any(x['exact_normalized_target']!=y['exact_normalized_target'] or x['source_imports']!=y['source_imports'] for x,y in zip(rows,old_l['contract_rows'])):raise RuntimeError('Old target mutation')
 for clause in h['source_principal_contract']['clauses']:
  rows.append({'id':clause['id'],'source_id':'L034','source_reference':'Theorem 3.2','parameter_range':h['source_principal_contract']['parameter_range'],'exact_normalized_target':clause['statement'],'source_status':'corrected complete principal construction; parity rows and repeated pair word corrected explicitly','principal_result_or_inventory_record':'principal_result','proof_locations':[sl['3'],sl['4'],sl['9']],'application_derivation':'A.H, via A4.1 geometric clause and A3.2 affine decompositions','umbrella_calls':['U.SK','U.SK.Local','U.SK.Geometry','U.SK.Helly','U.Geometry','U.Order'],'source_imports':['regular-polytope/string-C-group correspondence for the square seed; complete retained interface in A §1'],'scope_corrections_section':'9','use_map_status':'actual_derivation_bound_to_integrated_U_v3_author_candidate','section_spans_are_not_dependency_closures':True,'semantic_necessity_claim':False,'full_Lean_verification':False})
 l=copy.deepcopy(old_l);l.update(schema='phase138_six_source_ledger',status='complete_author_candidate_pending_integrated_review',source_bundle=old_l['source_bundle']+['L034'],contract_rows=rows,contract_row_count=len(rows),application=binding('phase138_module_A_v2.md'),section_bindings=sl)
 l['detailed_multiclauses']+=copy.deepcopy(h['source_principal_contract']['clauses']);l['auxiliary_records']=[{'source_id':'L034','source_reference':'Lemma 3.1','attribution':'McMullen–Schulte, as credited by the source','target':'Both complete square and diagonal quotient decompositions for every integer q>=2, including actual complement actions','application_derivation':'Proposition A3.2','proof_locations':[sl['3']],'additional_source_count':0}]
 l['umbrella']={'proof':binding('phase138_umbrella_v3.md'),'contract_path':'phase138_umbrella_v3_contracts.json','full_shared_proof_charged_once':True,'exclusion_as_zero_cost_forbidden':True}
 l['source_versions_and_measurement_boundaries']['L034']={'source_id':'L034','source_version':h['source'],'private_primary_bindings':h['private_primary_bindings'],'reading':h['reading'],'newly_normalized_house_format_measurement':False,'source_ratio_computed':False}
 for item in l['certificate_artifacts']:
  actual=binding(item['path'])
  if actual['sha256']!=item['sha256'] or actual['utf8_bytes']!=item['utf8_bytes']:raise RuntimeError('Changed certificate '+item['path'])
 l['certificate_replay']='python3 -B -O research/case_study/phase78_n009_integration_run.py --output-dir /private/tmp/NEW-two-group-certificate';l['unchanged_computations_reexecuted']=False
 l['formalization_map']=[x for x in l['formalization_map'] if x['theorem']!='U.SK used in A4.1/A4.2']
 l['formalization_map'] += [
 {'theorem':'U.SK used in A4.1/A4.2','scope':'actual support induction, pure kernel isolation, full fiber generation, exact parabolic profiles and full IP','artifact':'formal/SupportedKernelGeneration.lean','declaration':'MathCompression.SupportedKernelGeneration.supported_kernel_construction','status':'published reviewed phase129 core; unchanged compilation inherited','source_application_full_Lean':False,'missing':['A-specific affine local maps and proper-parabolic premises','coset geometry recognition','complete six source corollaries']},
 {'theorem':'U.SK.Helly','scope':'full generic marked transfer and actual SK specialization, all image/profile/coordinate premises discharged','artifact':'formal/SupportedKernelHelly.lean','declarations':['MathCompression.SupportedKernelHelly.marked_typed_helly','MathCompression.SupportedKernelHelly.supported_kernel_typed_helly'],'status':'phase137 author-frozen compilation; independent root admission pending at this checkpoint','source_application_full_Lean':False},
 {'theorem':'U.SK.Geometry / A.H','scope':'written proof only for involutivity, recognition, affine identifications, complete presentation and parameter binding','full_theorem_Lean':False}]
 l['formal_status_bindings']=[binding(x) for x in ['phase129_supported_kernel_scope.md','formal/SupportedKernelGeneration.lean','phase137_supported_kernel_helly_scope.md','phase137_supported_kernel_helly_manifest.json']]
 l['claims']={'new_conjecture_solution':False,'historical_priority':False,'ratio':None,'source_papers_fully_Lean_verified':False,'integrated_six_source_mathematical_admission':False,'previous_five_source_and_corrected_L034_admission_preserved':True}
 code=sum(x['utf8_bytes'] for x in l['certificate_artifacts']);body=u+a
 checkpoints={'five_source':{'whole_package_bytes':len((old_u+old_a).encode())+code,'diff':diff(old_u+old_a,body)},'corrected_six_source_additive':{'whole_package_bytes':len((old_u+old_a+extension+erratum).encode())+code,'diff':diff(old_u+old_a+extension+erratum,body)}}
 if checkpoints['five_source']['whole_package_bytes']!=190995 or checkpoints['corrected_six_source_additive']['whole_package_bytes']!=208750:raise RuntimeError('Baseline changed')
 for name,prior in [('five_source_with_N009_correction',old_u+old_a),('six_source_additive_with_both_corrections',old_u+old_a+extension+erratum)]:
  checkpoints[name]={'whole_package_bytes':len((prior+n009_erratum).encode())+code,'diff':diff(prior+n009_erratum,body),'mandatory_N009_erratum':binding('phase138_N009_decomposition_erratum.md')}
 for name in ['five_source','corrected_six_source_additive']:
  checkpoints[name]['historical_inventory_only_missing_newly_identified_N009_correction']=True
  checkpoints[name]['valid_complete_proof_comparator_without_correction']=False
 costs={'schema':'phase138_cost_checkpoint','metric':'raw UTF-8 bytes; raw NFC whitespace tokens supplied separately, not mixed with PDF/source extraction','umbrella':binding('phase138_umbrella_v3.md'),'application':binding('phase138_module_A_v2.md'),'umbrella_raw_NFC_whitespace_tokens':len(unicodedata.normalize('NFC',u).split()),'application_raw_NFC_whitespace_tokens':len(unicodedata.normalize('NFC',a).split()),'required_complete_code_and_data':l['certificate_artifacts'],'unchanged_required_code_bytes':code,'whole_U_A_four_artifact_bytes':len(body.encode())+code,'baselines':checkpoints,'diff_protocol':'Python difflib.SequenceMatcher on exact UTF-8-decoded lines with keepends=True and autojunk=False; baseline mathematical texts concatenated without extra separators, with the full mandatory N009 erratum appended in both corrected baselines; new U then A. Moved text may be counted in both gross additions and removals. Four unchanged code files have zero diff but their full cost remains in every total.','gross_diff_is_not_new_mathematical_idea_acquisition':True,'model_acquisition_cost_quantified':False,'relocation_as_zero_cost':False,'primary_source_normalized_house_format_comparison':None,'source_ratio':None,'claim_of_12x_or_other_desired_factor':False,'legacy_5_source_metrics':'Exact source PDF hashes remain in ledger; earlier extraction metrics are marked inherited and not a new comparable denominator.'}
 preserved['old_affine_prefix']={'sha256_utf8':sha(old_affine.encode()),'utf8_bytes':len(old_affine.encode())}
 costs['preserved_old_complete_branches']=preserved;costs['old_U_statement_and_proof_pairs_preserved']=28;costs['module_B_U_interfaces_unchanged']=['U.Coset','U.RelativeBound','U.Relative','U.Maximal','U.FrattiniTransport','U.FrattiniLadder']
 costs['first_actual_reuse_map']=[{'shared_leg':'U.SK.Helly + corrected U.SK.Geometry','applications':['A4.1 geometric clause','A.H via A4.1'],'per_use_cost':'base square geometry and literal dihedral reflection check are stated in A.H/A4.1; no duplicated Helly proof'},{'shared_leg':'A4.1','applications':['L032 prescribed orders','L035 existence','L034 exact hypertope construction'],'per_use_cost':'L034 pays all three target/base dihedral maps, exact order arithmetic, source relator evaluation, normal-kernel bound and pure-coordinate identification'},{'shared_leg':'A §3 affine square model','applications':['L035 square-map recognition','F016 local square sections','N009 lattice centers','L034 corrected square/diagonal decompositions'],'per_use_cost':'all-integer quotient decomposition and exact source parity words are added; previous affine normal forms retained; N009 diagonal factor pairing is corrected and derived in §7.4'}]
 costs['ablation_semantics']='Removing a named dependency removes this recorded derivation, not every possible proof.'
 z.output_dir.mkdir(parents=True)
 for name,d in [('phase138_umbrella_v3_contracts.json',uc),('phase138_module_A_v2_ledger.json',l),('phase138_cost_checkpoint.json',costs)]:
  (z.output_dir/name).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
 print(json.dumps({'contract_rows':len(rows),'U_theorems':len(uc['contracts']),'whole_bytes':costs['whole_U_A_four_artifact_bytes'],'baselines':{k:{'bytes':v['whole_package_bytes'],**{x:y for x,y in v['diff'].items() if x!='operations'}} for k,v in checkpoints.items()}}))
if __name__=='__main__':main()
