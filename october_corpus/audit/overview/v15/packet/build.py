"""Overview48: replace only Representation with the accepted two-source edition."""
from pathlib import Path
from copy import deepcopy
from fractions import Fraction
from decimal import Decimal,localcontext
import csv,io,json,hashlib
HERE=Path(__file__).resolve().parent
CHANGED=['Representation'];NEW=['L126']
def need(x,m):
 if not x:raise ValueError('V15_REJECT: '+m)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(n):return json.loads((HERE/n).read_text())
def fraction(n,d):
 f=Fraction(n,d)
 with localcontext()as c:c.prec=50;s=format(Decimal(n)/Decimal(d),'.12f')
 return dict(numerator=n,denominator=d,exact_fraction=f'{f.numerator}/{f.denominator}',decimal=s)
def derive(old,n):
 need(old['topic_count']==18 and old['original_manuscript_count']==47,'exact previous47');r=deepcopy(old);p=n['primary'];d=p['costs'];q=p['raw_costs'];prior=next(x for x in old['topics']if x['topic']=='Representation');t=deepcopy(prior)
 t.update(title=n['title'],source_count=2,source_ids=['F010','L126'],source_sum=p['totals']['source'],common_theory=d['U_R'],applications_sum=d['R1']+d['R2'],written_denominator=p['totals']['written'],written=fraction(p['totals']['source'],p['totals']['written']),printed_program_cost=d['CODE'],raw_program_alternative=q['required_finite_certificate']+q['optional_validation'],mandatory_data_cost=q['required_graph_data'],required_certificate_raw_cost=q['required_finite_certificate'],optional_validation_raw_cost=q['optional_validation'],whole_file_inventory=deepcopy(n['raw_file_inventory']['files']),whole_file_group_costs=deepcopy(q),common_components={'U_R':d['U_R']},application_components={'R1':{'R1':d['R1']},'R2':{'R2':d['R2']}},source_admission='audit/topic-representation/v3/admission.json',admitted_numeric_origin='audit/topic-representation/v3/measurement/packet/results.json',primary_coordinate='calibrated_selected/NFC/characters_without_whitespace',current_written_status='AVAILABLE_FROM_ACCEPTED_COMPLETE_MANUSCRIPT_BOUNDARY',current_written_reason='Whole shared theory and both complete applications; executable listings excluded symmetrically; primary result is written expansion.',written_comparison_scope='Complete manuscript length, not minimum proof complexity or total research effort.',conditional_assumption='Whole13-page U and actual retained mathematical inputs acquired. L126 additionally requires full graph certificate and19326-byte JSON; no sibling application premise. Nine optional validations are not prerequisites.',program_roles='Ten complete programs: one required elementary graph certificate and nine optional validations. Whole19326-byte graphJSON is additional mandatory data. Two helpers and four partialLean modules/22declarations remain separate. CODE16 and raw programs are alternatives, not summed.',historical_written=deepcopy(prior['written']),previous_topic_record=deepcopy(prior),listing_screening_evidence='Exact adopted inputs4c61d955 and distinct review3c103ab2; no executable listings in either measured scientific side.',entire_source_pages={'F010':13,'L126':13},entire_common_pages=[13],entire_application_pages={'F010':4,'L126':12},entire_program_pages={'CODE':16},scientific_boundary='Six F010 blocks and31 L126 dispositions, with exact finite-field/small-case corrections and connected-chamber splitting qualification. Broader Section6.2/Section8 programmes unresolved; classical inputs retained.',unknown_costs=deepcopy(n['unknown_costs']),scoped_Lean_declarations=22,full_source_formalized=False,whole_topic_interpretation='Expansion: no achieved whole-topic compression in the fixed primary coordinate.',no_sibling_application_dependency=True)
 t['pairs']=[]
 for s,a in [('F010','R1'),('L126','R2')]:
  before=next((x for x in prior['pairs']if x['source']==s),None)
  t['pairs'].append(dict(source=s,application=a,original_application_id=a,source_cost=d[s],application_cost=d[a],conditional=fraction(d[s],d[a]),source_representation='complete_PDF_calibrated_selected',historical_conditional=deepcopy(before['conditional'])if before else None,current_conditional_status='AVAILABLE_FROM_ACCEPTED_COMPLETE_MANUSCRIPT_BOUNDARY',current_conditional_reason=t['conditional_assumption']))
 r['topics']=[t if x['topic']=='Representation'else deepcopy(x)for x in old['topics']];ids=[s for x in r['topics']for s in x['source_ids']]
 need(len(ids)==len(set(ids))==48 and set(ids)-set(old['original_ids'])=={'L126'},'only L126 added')
 r.update(status='AUTHOR_V15_OVERVIEW_PENDING_DISTINCT_ROOT_REVIEW',original_manuscript_count=48,original_ids=ids,accessible_pending_originals=58,available_conditional_comparisons=48,available_whole_topic_comparisons=18,available_written_and_conditional_comparisons=66,written_and_conditional_comparisons=66,comparison_rows=66,historical_written_and_conditional_comparisons=65,historical_overview='audit/overview/v14/packet/results.json',programme_snapshot_status='48_RECOVERED_OF_106_ACTIVE_ORIGINALS_58_PENDING',restoration_scope='Only Representation changes;17 other topic records and46 other individual records are exactly preserved.',new_originals_reflected_from_scientific_admissions=['L126'],whole_programme_binding={'active':106,'recovered':48,'pending':58,'archived':55,'registration':'audit/programme48/v1/new_original_registration.json','source_admission':'audit/topic-representation/v3/admission.json'},new_source_credit=0,new_question_credit=0,new_formal_credit=0,factors_recomputed=True,recomputed_from_accepted_costs_only=True)
 return r

def csvs(r):
 out={};f=io.StringIO(newline='');w=csv.writer(f,lineterminator='\n');w.writerow(['topic','title','originals','source_cost','whole_common','all_applications','written_denominator','written_exact','written_factor','coordinate','required_data_inventory'])
 for t in r['topics']:w.writerow([t['topic'],t['title'],t['source_count'],t['source_sum'],t['common_theory'],t['applications_sum'],t['written_denominator'],t['written']['exact_fraction'],t['written']['decimal'],t['representation'],t.get('mandatory_data_cost','not_established_separately')])
 out['topics.csv']=f.getvalue();f=io.StringIO(newline='');w=csv.writer(f,lineterminator='\n');w.writerow(['topic','source','application','actual_documents','source_cost','application_cost','whole_common_prepaid','conditional_exact','conditional_factor','acquisition_condition'])
 for t in r['topics']:
  for a in t['pairs']:w.writerow([t['topic'],a['source'],a['application'],a.get('original_application_id',a['application']),a['source_cost'],a['application_cost'],t['common_theory'],a['conditional']['exact_fraction'],a['conditional']['decimal'],t['conditional_assumption']])
 out['applications.csv']=f.getvalue();return out

def plot_data(r):
 whole=[dict(id=t['topic'],held=False,values=dict(source=t['source_sum'],common=t['common_theory'],applications=t['applications_sum']),status=t['current_written_status'])for t in r['topics']]
 pairs=[dict(id=a['source'],topic=t['topic'],held=False,values=dict(source=a['source_cost'],application=a['application_cost']),status=a['current_conditional_status'])for t in r['topics']for a in t['pairs']]
 return dict(scope='18topics48originals; whole common paid, no pooled/software scalar.',whole_topics=whole,conditional_1=pairs[:24],conditional_2=pairs[24:],graph_bars=150)
if __name__=='__main__':
 r=derive(read('inputs/previous_results.json'),read('inputs/numbers_results.json'))
 for name,x in [('results.json',r),('plot_data.json',plot_data(r))]:(HERE/name).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
 for name,x in csvs(r).items():(HERE/name).write_text(x)
