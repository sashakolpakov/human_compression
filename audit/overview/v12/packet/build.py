"""Current overview from reviewed whole-document observations; no extraction."""
from pathlib import Path
from copy import deepcopy
from fractions import Fraction
from decimal import Decimal,localcontext
import csv,io,json,hashlib
HERE=Path(__file__).resolve().parent
CHANGED={'Chamber':'L008','ChiralEnumeration':'L028','Operations':'N006'}
def need(ok,msg):
 if not ok:raise ValueError('V12_REJECT: '+msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(n):return json.loads((HERE/n).read_text())
def fraction(a,b):
 f=Fraction(a,b)
 with localcontext()as c:c.prec=50;d=format(Decimal(a)/Decimal(b),'.12f')
 return dict(numerator=a,denominator=b,exact_fraction=str(f.numerator)+'/'+str(f.denominator),decimal=d)
def restore(old,numbers):
 need(old['topic_count']==19 and old['original_manuscript_count']==43 and old['accessible_pending_originals']==63,'exact v11 partition')
 need(list(numbers['topics'])==list(CHANGED),'exact three corrected topics')
 out=deepcopy(old)
 out.update(status='PRIVATE_V12_RESTORATION_CANDIDATE_PENDING_ROOT_PUBLICATION_REVIEW',historical_overview='audit/overview/v11/packet/results.json',historical_observations_unchanged=True,manuscripts_remeasured=False,factors_recomputed=False,restored_factors_carried_from_distinctly_reviewed_packet=True,available_whole_topic_comparisons=19,held_whole_topic_comparisons=0,available_conditional_comparisons=43,held_conditional_comparisons=0,available_written_and_conditional_comparisons=62,held_written_and_conditional_comparisons=0,written_and_conditional_comparisons=62,comparison_rows=62,software_inclusive_comparisons_available=False,policy='Executable listings are excluded on both sides by exact reviewed block masks. Scientific prose, algorithms in mathematical prose, tables and required proof dependencies are retained. Software-inclusive comparisons remain unknown.',restoration_scope='Three whole-topic and three conditional factors only. Sixteen whole-topic records and forty other conditional records remain unchanged.',no_new_mathematical_acceptance=True)
 for t in out['topics']:
  if t['topic']not in CHANGED:continue
  n=numbers['topics'][t['topic']];p=n['primary'];need(n['primary_coordinate']=='calibrated_selected_without_listings/NFC/characters_without_whitespace','fixed primary')
  need(t['common_theory']==p['common_sum']and t['applications_sum']==sum(p['application_bundle_costs'].values())and t['written_denominator']==p['whole_written'],'complete unchanged common/app cost')
  new=fraction(p['source_sum'],p['whole_written']);need(new['decimal']==p['written']['decimal']and new['numerator']==p['written']['source_cost'],'bound arithmetic')
  t['historical_source_sum']=t['source_sum'];t['source_sum']=p['source_sum'];t['written']=new;t['held_sources']=[]
  t['representation_before_listing_exclusion']=t['representation'];t['representation']=t['representation']+'; exact executable-listing exclusions on both sides'
  t['current_written_status']='AVAILABLE_AFTER_REVIEWED_SYMMETRIC_LISTING_EXCLUSION';t['current_written_reason']='Exact source executable blocks removed while surrounding mathematics remains; all replacement scientific PDFs and all full program roles unchanged.'
  t['written_comparison_scope']='Complete source and replacement manuscript text after matched concrete-listing exclusion. Full common theory and every complete application charged; all source/software/graphic limitations remain explicit.'
  t['listing_exclusion_evidence']='audit/overview/v12/matched_inputs/manifest.json';t['numerical_restoration_evidence']='audit/overview/v12/matched_numbers/manifest.json'
  for a in t['pairs']:
   q=p['conditional'][a['source']];cost=p['document_costs'][a['source']]
   need(a['application_cost']==p['application_bundle_costs'][a['source']],'whole application bundle')
   if a['source']!=CHANGED[t['topic']]:
    need(a['source_cost']==cost and a['conditional']==fraction(cost,a['application_cost']),'unaffected local boundary unchanged');continue
   a['historical_source_cost']=a['source_cost'];a['source_cost']=cost;a['conditional']=fraction(cost,a['application_cost'])
   need(a['conditional']['decimal']==q['decimal'],'conditional arithmetic pin')
   a['current_conditional_status']='AVAILABLE_AFTER_REVIEWED_SYMMETRIC_LISTING_EXCLUSION';a['current_conditional_reason']='Exact source listing excluded; complete local application unchanged. Whole common theory and required proof/program/data premises remain acquired in advance.'
   a['listing_exclusion_evidence']=t['listing_exclusion_evidence']
 return out

def csvs(r):
 out={};s=io.StringIO(newline='');w=csv.writer(s,lineterminator='\n');w.writerow(['topic','title','originals','current_source_cost','whole_common_cost','whole_application_cost','written_denominator','current_written_exact','current_written_factor','status','historical_source_cost','historical_written_exact','historical_written_factor'])
 for t in r['topics']:
  f=t['written'];h=t['historical_written'];w.writerow([t['topic'],t['title'],t['source_count'],t['source_sum'],t['common_theory'],t['applications_sum'],t['written_denominator'],f['exact_fraction'],f['decimal'],t['current_written_status'],t.get('historical_source_sum',t['source_sum']),h['exact_fraction'],h['decimal']])
 out['topics.csv']=s.getvalue();s=io.StringIO(newline='');w=csv.writer(s,lineterminator='\n');w.writerow(['topic','source','application','current_source_cost','whole_application_cost','whole_common_prepaid','current_conditional_exact','current_conditional_factor','status','historical_source_cost','historical_conditional_exact','historical_conditional_factor','acquisition_condition'])
 for t in r['topics']:
  for a in t['pairs']:
   f=a['conditional'];h=a['historical_conditional'];w.writerow([t['topic'],a['source'],a['application'],a['source_cost'],a['application_cost'],t['common_theory'],f['exact_fraction'],f['decimal'],a['current_conditional_status'],a.get('historical_source_cost',a['source_cost']),h['exact_fraction'],h['decimal'],t['conditional_assumption']])
 out['applications.csv']=s.getvalue();return out

def plot_data(r):
 whole=[dict(id=t['topic'],held=False,values=dict(source=t['source_sum'],common=t['common_theory'],applications=t['applications_sum']),status=t['current_written_status'])for t in r['topics']]
 pairs=[dict(id=a['source'],topic=t['topic'],held=False,values=dict(source=a['source_cost'],application=a['application_cost']),status=a['current_conditional_status'])for t in r['topics']for a in t['pairs']]
 return dict(scope='Current complete manuscript costs with exact listing exclusions. Whole common theory paid once per topic. No software-inclusive or pooled factor.',whole_topics=whole,conditional_1=pairs[:22],conditional_2=pairs[22:],graph_bars=143)
def main():
 r=restore(read('inputs/v11_results.json'),read('inputs/matched_numbers/results.json'))
 for n,x in [('results.json',r),('plot_data.json',plot_data(r))]:(HERE/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
 for n,x in csvs(r).items():(HERE/n).write_text(x)
if __name__=='__main__':main()
