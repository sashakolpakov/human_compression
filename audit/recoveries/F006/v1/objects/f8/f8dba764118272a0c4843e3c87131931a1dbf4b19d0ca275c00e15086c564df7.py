#!/usr/bin/env python3
"""Distinct binding/scope/finite diagnostic replay. No author modules imported."""
import argparse,copy,hashlib,json,re,sys
from pathlib import Path
from finite_checks import audit as finite_audit
ROOT=Path(__file__).resolve().parent

def load(p):return json.loads(p.read_text())
def need(x,m):
 if not x:raise ValueError(m)
def record(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def bound(p,r):need(record(p)=={k:r[k] for k in ['bytes','sha256']},'changed binding '+str(p))
def semantics(s,m,d):
 need(s['source_ids']==['L047'] and s['principal_source_contracts']==1,'one exact original')
 need(len(m['rows'])==58 and len({r['id'] for r in m['rows']})==58 and len(m['proof_contexts'])==12,'all source/context rows')
 need(s['full_IP_required'] and s['new_sharp_rank_induction_decreases_degree'] and s['quotient_images_not_assumed_IP'],'actual induction/IP boundary')
 need(s['ordered_vs_unordered_distinction'],'ordered distinction')
 need(sum(r['status']=='attributed_ancillary_report_not_a_premise' for r in m['rows'])==23,'finer maxima not recovered')
 need(s['new_Lean_declarations']==0 and s['reused_partial_Lean_declarations']==14 and not s['full_source_formalization'],'partial formal')
 need(s['new_question_credit']==s['new_source_credit']==0 and not s['ratios_computed'],'no credit/rate')
 need('L044' in s['Conjecture1.1_status'],'historical resolution')
 need(all(s[k] is None for k in ['full_external_costs','full_graphics_cost','complete_software_inclusive_factor']),'unknown costs')
 need(s['scientific_pages']=={'inherited_common':16,'new_common':10,'new_application':3},'whole common/app')
 need(s['complete_program_appendix_pages']=={'inherited':7,'new':7},'whole programs')
 expected=['small_extremal.g','small_transitive.g','primitive_bounds.g','primitive_markings.g','retained/finite_boundary/search.g','retained/finite_boundary/run.g']
 need([r['path'] for r in s['new_mathematical_programs'][:6]]==expected and all(r['role'].startswith('required ') for r in s['new_mathematical_programs'][:6]),'complete six required inputs')
 need(len(s['new_mathematical_programs'])==10 and s['new_required_program_count']==6,'retained programs')
 need('old universal imprimitive irredundant-length theorem' in d['logical_interfaces']['common_not_invoked'],'no circular sharp-bound premise')
 need(d['payment_boundary']['root_finite_proof_fully_included_in_new_common'],'full finite proof paid')
 need(d['roles']['new_author']!='/root/rewrite_termination' and d['roles']['common_author']=='/root/rewrite_termination','prior authorship disclosure')
 rows={r['id']:r for r in m['rows']}
 need(rows['Tab1.1']['status']=='corrected' and '[3,2,3]' in rows['Tab1.1']['claim'],'literal order36 correction')
 need(rows['P2.2']['status']=='recovered_with_standing_hypothesis','standing string hypothesis')
 need(all(rows[x]['status']=='recovered_with_rank_convention' for x in ['C4.1','C4.2','C4.3']),'parent/parabolic convention')

def controls(s,m,d):
 changes=[('drop_IP',lambda a,b,c:a.update(full_IP_required=False)),('quotient_IP_assumed',lambda a,b,c:a.update(quotient_images_not_assumed_IP=False)),('same_degree_induction',lambda a,b,c:a.update(new_sharp_rank_induction_decreases_degree=False)),('forget_ordered_types',lambda a,b,c:a.update(ordered_vs_unordered_distinction=False)),('new_conjecture_credit',lambda a,b,c:a.update(new_question_credit=1)),('formal_scope_inflated',lambda a,b,c:a.update(full_source_formalization=True)),('external_cost_zero',lambda a,b,c:a.update(full_external_costs=0)),('old_common_free',lambda a,b,c:a['scientific_pages'].update(inherited_common=0)),('old_programs_omitted',lambda a,b,c:a['new_mathematical_programs'].pop()),('required_became_optional',lambda a,b,c:a['new_mathematical_programs'][0].update(role='optional')),('principal_row_omitted',lambda a,b,c:b['rows'].pop()),('ancillary_maximum_promoted',lambda a,b,c:next(r for r in b['rows'] if r['id']=='Tab3.1').update(status='recovered')),('finite_body_unpaid',lambda a,b,c:c['payment_boundary'].update(root_finite_proof_fully_included_in_new_common=False)),('source_type_uncorrected',lambda a,b,c:next(r for r in b['rows'] if r['id']=='Tab1.1').update(status='recovered'))]
 rejected=[]
 for label,fn in changes:
  a,b,c=copy.deepcopy((s,m,d));fn(a,b,c)
  try:semantics(a,b,c)
  except (ValueError,KeyError,IndexError):rejected.append(label)
  else:raise ValueError('control accepted '+label)
 return rejected

def run(a):
 p=a.packet.resolve();a.out.mkdir(parents=True,exist_ok=False);bind=load(ROOT/'bindings.json');bound(p/'manifest.json',bind['current_manifest'])
 for r in load(p/'manifest.json')['exports']:bound(p/r['path'],r)
 s,m,d=load(p/'scope.json'),load(p/'source_map.json'),load(p/'dependencies.json');semantics(s,m,d)
 old_manifest=load(p/'previous_manifest.json');bound(p/'previous_manifest.json',bind['previous_manifest'])
 changed=[r['path'] for r in old_manifest['exports'] if record(p/r['path'])!={k:r[k] for k in ['bytes','sha256']}]
 need(set(changed)=={'README.rst','primitive_branch.tex','source_map.json','string_rank_theory.pdf'},'only precision exports changed')
 old_files={r['path']:r for r in old_manifest['exports']}
 for n in ['primitive_branch.tex','source_map.json']:bound(p/'previous'/n,old_files[n])
 before=(p/'previous/primitive_branch.tex').read_text();after=(p/'primitive_branch.tex').read_text()
 old_fragment=r'alternative, with $m\geq5$ and degree $n=\binom m k^\ell$.'
 new_fragment='alternative, with $m\\geq5$ and, after replacing subsets by complements,\n$1\\leq k\\leq m/2$. The degree is $n=\\binom m k^\\ell$.'
 need(before.count(old_fragment)==1 and after==before.replace(old_fragment,new_fragment),'exact one proof clarification')
 old_map=load(p/'previous/source_map.json');need(old_map['rows']==m['rows'],'all dispositions exact across editions')
 for dep in d['packets']:
  mf=p/dep['manifest'];bound(mf,dep);files={x['path']:x for x in load(mf)['exports']}
  for n in dep['copied_exports']:bound(mf.parent/n,files[n])
 for x in s['new_mathematical_programs']:bound(p/x['path'],x)
 for x in m['proof_contexts']:
  t=(p/x['file']).read_text();snippet=t[x['start_codepoint']:x['end_codepoint_exclusive']]
  need(hashlib.sha256(snippet.encode()).hexdigest()==x['sha256_utf8'],'complete context')
 if a.study_root:
  source=m['source'];bound(a.study_root/source['pdf']['path'],source['pdf']);bound(a.study_root/source['text']['path'],source['text']);t=(a.study_root/source['text']['path']).read_text()
  for x in m['rows']:
   q=x['source_span'];need(hashlib.sha256(t[q['start_codepoint']:q['end_codepoint_exclusive']].encode()).hexdigest()==q['sha256_utf8'],'source span')
 migration=load(p/'finite_migration.json');t=(p/migration['source']).read_text();need(t[migration['start_codepoint']:migration['end_codepoint_exclusive']]==(p/migration['target']).read_text(),'entire finite body')
 prog=(p/'program-appendix.tex').read_text();listed=re.findall(r'\\VerbatimInput\[[^\]]*\]\{([^}]+)\}',prog)
 need(listed==[x['path'] for x in s['new_mathematical_programs'][:6]],'full six-file print')
 old=load(ROOT/'contract_review.json')['source_rows'];need([(r['id'],r['status'],r['claim'],r['proof_contexts']) for r in old]==[(r['id'],r['status'],r['claim'],r['proof_contexts']) for r in m['rows']],'source dispositions unchanged')
 # The precision successor must explicitly contain the reviewed complement convention.
 primitive=(p/'primitive_branch.tex').read_text();need('complement' in primitive and re.search(r'1\s*\\leq\s*k\s*\\leq\s*m/2',primitive),'subset complement convention')
 controls_list=controls(s,m,d);finite=finite_audit(p);(a.out/'finite_result.json').write_text(json.dumps(finite,indent=2)+'\n')
 report={'status':'PASS_DISTINCT_L047_REVIEW_REPLAY','author_manifest':record(p/'manifest.json'),'source_rows':58,'proof_contexts':12,'all_export_bindings':len(load(p/'manifest.json')['exports']),'source_bound':a.study_root is not None,'scope_controls_rejected':controls_list,'bounded_diagnostic_controls':finite['negative_controls'],'positive_tuples':finite['literal_positive_count'],'positive_IP_pairs':finite['positive_IP_pairs'],'inherited_authorship_disclosed':True,'large_GAP_census_repeated':False,'author_code_imported':False,'source_credit':0,'new_question_credit':0}
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');return report
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--packet',type=Path,required=True);ap.add_argument('--study-root',type=Path);ap.add_argument('--out',type=Path,required=True);print(json.dumps(run(ap.parse_args())))
