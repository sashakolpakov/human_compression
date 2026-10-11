"""Consolidate accepted A and Mixes; no extraction or scientific computation."""
from pathlib import Path
from copy import deepcopy
from fractions import Fraction
from decimal import Decimal,localcontext
import csv,io,json,hashlib
HERE=Path(__file__).resolve().parent
CHANGED=['A','Mixes'];REMOVED=['Affine'];NEW=['F007']
def need(ok,msg):
 if not ok:raise ValueError('V14_REJECT: '+msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(n):return json.loads((HERE/n).read_text())
def fraction(a,b):
 f=Fraction(a,b)
 with localcontext()as c:c.prec=50;d=format(Decimal(a)/Decimal(b),'.12f')
 return dict(numerator=a,denominator=b,exact_fraction=f'{f.numerator}/{f.denominator}',decimal=d)
def basis(key,n,old):
 return dict(topic=key,title=n.get('title',n.get('topic')),source_count=len(n['source_ids']),source_ids=deepcopy(n['source_ids']),representation='calibrated_selected_pdf'if key=='A'else'raw_untrimmed_pdf',normalization='NFC',unit='characters_without_whitespace',including_printed_programs=None,including_raw_programs=None,including_optional_validation=None,external_proof_cost=None,historical_software_cost=None,complete_graphic_cost=None,full_formalization_cost=None,software_comparison_status='UNAVAILABLE_UNTIL_BOTH_SIDES_HAVE_MATCHED_SOFTWARE_BOUNDARIES',current_written_status='AVAILABLE_FROM_ACCEPTED_COMPLETE_MANUSCRIPT_BOUNDARY',current_written_reason='Whole common theory and all local applications charged under exact independently accepted coordinate; executable software excluded symmetrically.',written_comparison_scope='Complete manuscript extracted text with exact source-contract and unknown-cost qualifications.',embedded_validation_listings_screened=True,held_sources=[],historical_written=deepcopy(old['written']),historical_source_sum=old['source_sum'],previous_topic_record=deepcopy(old),numerical_status='ROOT_ACCEPTED_TOPIC_NUMBERS',no_cross_topic_discount=True,primary_coordinate=n['primary_coordinate'],source_admission='programme_binding.json',whole_file_inventory=deepcopy(n['whole_file_inventory']),whole_file_group_costs=deepcopy(n['whole_file_group_costs']),full_source_formalized=False)
def pair(s,app,docs,d,previous,coordinate):
 prior=next((a for t in previous for a in t['pairs']if a['source']==s),None);cost=sum(d[x]for x in docs)
 return dict(source=s,application=app,original_application_id='+'.join(docs),source_cost=d[s],application_cost=cost,conditional=fraction(d[s],cost),source_representation=coordinate,historical_conditional=deepcopy(prior['conditional'])if prior else None,historical_source_cost=prior['source_cost']if prior else None,current_conditional_status='AVAILABLE_FROM_ACCEPTED_COMPLETE_MANUSCRIPT_BOUNDARY',current_conditional_reason='After acquiring the entire common paper(s), all required complete computational/data premises and retained mathematics, charge the complete local application bundle.')
def unified_A(n,old,affine):
 p=n['primary'];d=p['document_costs'];t=basis('A',n,old);need(n['primary_coordinate']=='calibrated_selected/NFC/characters_without_whitespace','accepted A coordinate')
 t.update(source_sum=p['source_sum'],common_theory=p['whole_common'],applications_sum=p['application_sum'],written_denominator=p['whole_written'],written=fraction(p['source_sum'],p['whole_written']),common_components={'U':d['U']},application_components={app:{app:d[app]}for app in n['applications'].values()},pairs=[pair(s,app,[app],d,[old,affine],'complete_PDF_calibrated_selected')for s,app in n['applications'].items()],previous_affine_record=deepcopy(affine),printed_program_cost=p['separate_software']['printed_sum'],raw_program_alternative=p['separate_software']['raw_group_costs']['required_program_or_data'],optional_validation_printed=None,separate_software_inventory=deepcopy(p['separate_software']),program_roles='Eleven whole required mathematical programs/data files; three inherited auxiliary files, two current operational drivers and fourteen partial formal files remain separately inventoried. Exclusion from this manuscript metric does not make a required premise optional.',conditional_assumption='Whole23-page common theory, every complete required program/data file and all retained mathematical inputs acquired. No free old A or Affine theory; optional validation is separate.',entire_source_pages=n['source_pages'],entire_common_pages=[n['whole_common_pages']],entire_application_pages=deepcopy(n['application_pages']),entire_program_pages=deepcopy(n['printed_appendix_pages']),numeric_origin='inputs/A_results.json/primary',listing_screening_evidence='Accepted unified-A input review and symmetric policy: scientific manuscripts and code inventories are distinct; no historical software total assumed.',scientific_boundary='Eight accepted original contracts retain their corrections and retained classifications. The full common paper includes the translation-lattice addition. Graphical structure and unextracted source image labels remain unmeasured; the coordinate is extracted text, not all visible information.',unknown_costs=deepcopy(n['unknown_costs']),merged_previous_topics=['A','Affine'])
 need(t['written']['decimal']==p['written']['decimal'],'A accepted whole');return t

def expanded_Mix(n,old):
 p=n['primary'];d=p['document_costs'];t=basis('Mixes',n,old);need(n['primary_coordinate']=='raw_untrimmed/NFC/characters_without_whitespace','accepted Mix coordinate')
 t.update(source_sum=p['source_sum'],common_theory=p['whole_common'],applications_sum=p['application_sum'],written_denominator=p['whole_written'],written=fraction(p['source_sum'],p['whole_written']),common_components={x:d[x]for x in n['common_documents']},application_components={s:{x:d[x]for x in docs}for s,docs in n['application_documents'].items()},pairs=[pair(s,'MX'+str(i+1),docs,d,[old],'complete_PDF_raw_untrimmed')for i,(s,docs)in enumerate(n['application_documents'].items())],printed_program_cost=p['separate_inventory']['required_printed_alternative'],raw_program_alternative=p['separate_inventory']['required_finite_certificate'],optional_validation_printed=p['separate_inventory']['partial_optional_printed_inventory'],separate_software_inventory=deepcopy(p['separate_inventory']),required_files=deepcopy(n['required_files']),optional_files=deepcopy(n['optional_files']),required_printed_coverage=deepcopy(n['required_printed_coverage']),program_roles='Both whole finite certificates remain required; six complete validation programs remain optional. Six operational drivers and three partial formal files are separate. REQ contains both required programs; historical mixed appendices are alternative inventories, never added again.',conditional_assumption=n['conditional_prepaid'],entire_source_pages=n['source_pages'],entire_common_pages=[n['document_pages'][x]for x in n['common_documents']],entire_application_pages=deepcopy(n['application_pages']),entire_program_pages={x:n['document_pages'][x]for x in ['CODE1','CODE2','REQ','VAL']},numeric_origin='inputs/Mix_results.json/primary',listing_screening_evidence='Accepted three-source input review: no concrete executable listings in measured scientific PDFs; complete programs disclosed separately on both sides.',scientific_boundary=deepcopy(n['source_scope_limits']),source_dispositions=deepcopy(n['source_scope']),scoped_Lean_declarations=n['partial_formal_declarations'],unknown_costs=deepcopy(n['unknown_costs']))
 need(t['written']['decimal']==p['written']['decimal'],'Mix accepted whole');return t

def derive(old,a,m,programme):
 need(old['topic_count']==19 and old['original_manuscript_count']==46,'exact v13 baseline');r=deepcopy(old);by={t['topic']:t for t in old['topics']}
 r['topics']=[unified_A(a,t,by['Affine'])if t['topic']=='A'else expanded_Mix(m,t)if t['topic']=='Mixes'else deepcopy(t)for t in old['topics']if t['topic']!='Affine']
 ids=[s for t in r['topics']for s in t['source_ids']];need(len(ids)==len(set(ids))==47 and set(ids)-set(old['original_ids'])==set(NEW),'only new F007')
 r.update(factors_recomputed=True,recomputed_from_accepted_costs_only=True,historical_written_and_conditional_comparisons=65,status='AUTHOR_V14_CONSOLIDATION_PENDING_DISTINCT_OVERVIEW_REVIEW',topic_count=18,original_manuscript_count=47,original_ids=ids,accessible_pending_originals=59,available_whole_topic_comparisons=18,available_conditional_comparisons=47,available_written_and_conditional_comparisons=65,written_and_conditional_comparisons=65,comparison_rows=65,historical_overview='audit/overview/v13/packet/results.json',historical_observations_unchanged=True,programme_snapshot_status='47_RECOVERED_OF_106_ACTIVE_ORIGINALS_59_PENDING',restoration_scope='Unified A replaces separate A and Affine; Mixes adds F007. Sixteen other topic records and36 other individual records remain exact, including expanded E and all symmetric listing restorations.',no_new_mathematical_acceptance=True,new_source_credit=0,new_question_credit=0,new_formal_credit=0,new_originals_reflected_from_scientific_admissions=NEW,whole_programme_binding=deepcopy(programme),software_inclusive_comparisons_available=False,policy='Complete manuscripts in each topic adopted coordinate, whole common theory charged per topic and executable software excluded symmetrically. No pooled or software-inclusive scalar.')
 # Replace inherited tally fields, including any historic alias.
 for k in ['available_written_comparisons','whole_topic_comparisons']:
  if k in r:r[k]=18
 for t in r['topics']:
  if t['topic']in CHANGED:t['source_admission']=programme['source_admissions'][t['topic']]
 return r

def csvs(r):
 out={};s=io.StringIO(newline='');w=csv.writer(s,lineterminator='\n');w.writerow(['topic','title','originals','current_source_cost','whole_common_cost','all_applications_cost','written_denominator','current_written_exact','current_written_factor','coordinate','historical_written_exact','historical_written_factor'])
 for t in r['topics']:
  h=t['historical_written'];w.writerow([t['topic'],t['title'],t['source_count'],t['source_sum'],t['common_theory'],t['applications_sum'],t['written_denominator'],t['written']['exact_fraction'],t['written']['decimal'],t['representation'],h['exact_fraction'],h['decimal']])
 out['topics.csv']=s.getvalue();s=io.StringIO(newline='');w=csv.writer(s,lineterminator='\n');w.writerow(['topic','source','application','actual_documents','current_source_cost','application_cost','whole_common_prepaid','conditional_exact','conditional_factor','historical_conditional_exact','acquisition_condition'])
 for t in r['topics']:
  for a in t['pairs']:
   h=a['historical_conditional'];w.writerow([t['topic'],a['source'],a['application'],a.get('original_application_id',a['application']),a['source_cost'],a['application_cost'],t['common_theory'],a['conditional']['exact_fraction'],a['conditional']['decimal'],h['exact_fraction']if h else 'no_prior_comparison',t['conditional_assumption']])
 out['applications.csv']=s.getvalue();return out

def plot_data(r):
 whole=[dict(id=t['topic'],held=False,values=dict(source=t['source_sum'],common=t['common_theory'],applications=t['applications_sum']),status=t['current_written_status'])for t in r['topics']];pairs=[dict(id=a['source'],topic=t['topic'],held=False,values=dict(source=a['source_cost'],application=a['application_cost']),status=a['current_conditional_status'])for t in r['topics']for a in t['pairs']]
 return dict(scope='Complete18-topic47-original manuscripts; whole common theory paid, exact adopted coordinates, no pooled/software scalar.',whole_topics=whole,conditional_1=pairs[:24],conditional_2=pairs[24:],graph_bars=148)
if __name__=='__main__':
 r=derive(read('inputs/v13_results.json'),read('inputs/A_results.json'),read('inputs/Mix_results.json'),read('programme_binding.json'))
 for name,obj in [('results.json',r),('plot_data.json',plot_data(r))]:(HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
 for name,text in csvs(r).items():(HERE/name).write_text(text)
