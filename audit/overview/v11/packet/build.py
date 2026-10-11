"""Additive status correction only: no extraction and no factor calculation."""
from pathlib import Path
from copy import deepcopy
import csv,io,json,hashlib
HERE=Path(__file__).resolve().parent
HELD={'Chamber':'L008','ChiralEnumeration':'L028','Operations':'N006'}
REASONS={
 'L008':'Executable Magma functions occur in the counted source, section5, physical pages8–10; replacement programs are separate and excluded. A matched code boundary is not yet available.',
 'L028':'Executable ChiralPolytopes, OrderedSubsetsGroups and DiagramPlus listings occur in the counted source, section4.2, physical pages9–12; replacement programs are separate and excluded. A matched code boundary is not yet available.',
 'N006':'The counted source contains the concrete McL search pseudocode in the proof of Theorem5.3, physical page20; replacement programs are separate and excluded. A matched code boundary is not yet available.'}
UNKNOWN='AWAITING_MATCHED_CODE_BOUNDARY'
AVAILABLE='AVAILABLE_FROM_UNCHANGED_MATCHED_MANUSCRIPT_BOUNDARY'
def need(ok,msg):
 if not ok:raise ValueError('LISTING_CORRECTION_REJECT: '+msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(name):return json.loads((HERE/name).read_text())
def derive(old,screen):
 need(old['topic_count']==19 and old['original_manuscript_count']==43 and old['active_originals']==106 and old['accessible_pending_originals']==63,'exact published programme')
 need(screen['held_topics']==list(HELD) and screen['held_sources']==list(HELD.values()),'exact final listing findings')
 topicids=[t['topic']for t in old['topics']]
 need(screen['unaffected_topics_screened']==[k for k in topicids if k not in HELD],'complete named positive screen, not inferred from silence')
 need(screen['held_listing_roles']=={s:'proof_or_algorithm_implementation_not_optional_validation'for s in HELD.values()},'no mandatory-as-optional relabeling')
 cur=deepcopy(old);cur.update(status='ADDITIVE_CURRENT_COMPARISON_CORRECTION_PENDING_ROOT_ADOPTION',historical_overview='audit/overview/v10/packet/results.json',historical_observations_unchanged=True,manuscripts_remeasured=False,factors_recomputed=False,available_whole_topic_comparisons=16,held_whole_topic_comparisons=3,available_conditional_comparisons=40,held_conditional_comparisons=3,available_written_and_conditional_comparisons=56,held_written_and_conditional_comparisons=6,policy='Executable listings must be counted on both sides or excluded on both sides. Concrete proof/algorithm listings cannot remain only in a source numerator merely because their role is required. Held factors are null until a matched boundary is reviewed. Mathematical algorithm prose and tables are not automatically code listings.',programme_snapshot_status='43_RECOVERED_OF_106_ACTIVE_ORIGINALS_63_PENDING_UNCHANGED',current_comparison_status_is_not_scientific_admission=True)
 cur['software_inclusive_comparisons_available']=False
 cur['historical_written_and_conditional_comparisons']=62;cur['comparison_rows']=62;cur['written_and_conditional_comparisons']=56
 for t in cur['topics']:
  key=t['topic'];t['historical_written']=deepcopy(t['written']);t['historical_embedded_validation_listings_screened']=t.get('embedded_validation_listings_screened',False)
  t['embedded_validation_listings_screened']=True;t['listing_screening_evidence']=screen['evidence_by_topic'][key]
  held=key in HELD;t['current_written_status']=UNKNOWN if held else AVAILABLE
  t['current_written_reason']=REASONS[HELD[key]] if held else 'Final listing audit found no unmatched concrete executable listing in this complete manuscript boundary; exact v10 costs and fraction retained.'
  t['held_sources']=[HELD[key]]if held else []
  if held:t['written']=None
  t['written_comparison_scope']='Complete manuscript observations remain historical and unchanged; current availability is controlled by the exact listing screen.'
  for k in ['including_printed_programs','including_raw_programs','including_optional_validation']:
   need(t.get(k)is None,'prior software-inclusive factor already null');t[k]=None
  need(t.get('historical_software_cost')is None,'historical software unknown')
  t['software_comparison_status']='UNAVAILABLE_UNTIL_BOTH_SIDES_HAVE_MATCHED_SOFTWARE_BOUNDARIES'
  for a in t['pairs']:
   a['historical_conditional']=deepcopy(a['conditional']);helda=a['source']in HELD.values();a['current_conditional_status']=UNKNOWN if helda else AVAILABLE
   a['current_conditional_reason']=REASONS[a['source']]if helda else 'Source and local application manuscript boundary passed the final listing screen. The whole common theory and required premises remain prepaid, with no cross-topic discount.'
   if helda:a['conditional']=None
 return cur

def csvs(cur):
 out={};b=io.StringIO(newline='');w=csv.writer(b,lineterminator='\n');w.writerow(['topic','title','originals','source_cost_observed','whole_common_cost_observed','application_cost_observed','written_denominator_observed','current_written_exact','current_written_factor','current_status','held_sources','historical_written_exact','historical_written_factor'])
 for t in cur['topics']:
  c=t['written'];h=t['historical_written'];w.writerow([t['topic'],t['title'],t['source_count'],t['source_sum'],t['common_theory'],t['applications_sum'],t['written_denominator'],c['exact_fraction']if c else 'null',c['decimal']if c else 'null',t['current_written_status'],';'.join(t['held_sources']),h['exact_fraction'],h['decimal']])
 out['topics.csv']=b.getvalue();b=io.StringIO(newline='');w=csv.writer(b,lineterminator='\n');w.writerow(['topic','source','application','source_cost_observed','application_cost_observed','whole_common_cost_observed','current_conditional_exact','current_conditional_factor','current_status','historical_conditional_exact','historical_conditional_factor','assumption'])
 for t in cur['topics']:
  for a in t['pairs']:
   c=a['conditional'];h=a['historical_conditional'];w.writerow([t['topic'],a['source'],a['application'],a['source_cost'],a['application_cost'],t['common_theory'],c['exact_fraction']if c else 'null',c['decimal']if c else 'null',a['current_conditional_status'],h['exact_fraction'],h['decimal'],t['conditional_assumption']])
 out['applications.csv']=b.getvalue();return out

def plot_data(cur):
 rows=[]
 for t in cur['topics']:
  rows.append(dict(id=t['topic'],held=t['written']is None,values=None if t['written']is None else dict(source=t['source_sum'],common=t['common_theory'],applications=t['applications_sum']),status=t['current_written_status']))
 app=[]
 for t in cur['topics']:
  for a in t['pairs']:app.append(dict(id=a['source'],topic=t['topic'],held=a['conditional']is None,values=None if a['conditional']is None else dict(source=a['source_cost'],application=a['application_cost']),status=a['current_conditional_status']))
 return dict(scope='Current graphs; held rows intentionally have no numeric bars. Historical observations remain only in explicitly labeled data columns.',whole_topics=rows,conditional_1=app[:22],conditional_2=app[22:],graph_bars=128,held_row_label='awaiting matched code boundary')

def main():
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 c=derive(read('inputs/historical_results.json'),read('screening.json'))
 (a.out/'results.json').write_text(json.dumps(c,ensure_ascii=False,indent=2)+'\n');(a.out/'plot_data.json').write_text(json.dumps(plot_data(c),indent=2)+'\n')
 for n,t in csvs(c).items():(a.out/n).write_text(t)
 print('Status correction only:16+40 available,3+3 held;43 recoveries unchanged; no new fractions.')
if __name__=='__main__':main()
