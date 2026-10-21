#!/usr/bin/env python3
"""Fail-closed inventory structural/evidence checks; not mathematical proof review."""
from pathlib import Path
import argparse,copy,csv,hashlib,json
P=Path(__file__).resolve().parent
EXPECTED={f'L{i:03}'for i in range(1,129)}|{f'F{i:03}'for i in range(1,18)}|{f'N{i:03}'for i in range(1,17)}
NONPDF={'L022','L108','N001','N005'}
def require(p,m):
 if not p:raise ValueError(m)
def validate(j):
 rows=j['entries'];by={r['original_id']:r for r in rows};require(len(rows)==161 and set(by)==EXPECTED,'exact161 original IDs')
 require(all(r['unique_original_count']==1 and r['target_remains_active'] is True for r in rows),'every original remains active exactly once')
 require(sum(r['source_access']['accessible']for r in rows)==104,'104 accessible originals')
 require(sum(not r['source_access']['accessible']for r in rows)==57,'57 complete-body retrieval targets')
 principal={r['original_id']for r in rows if r['proof']['principal_contract_admitted']};require(len(principal)==27,'27 admitted principal contracts, no candidate inflation')
 require(j['new_source_credit']==0 and j['new_question_credit']==0 and j['new_ratios']is None,'no inventory credits or factors')
 got_nonpdf=set()
 for r in rows:
  a=r['source_access'];ss=a['usable_representations'];require(a['accessible']==bool(ss),'usable representations decide access')
  require(a['pending_retrieval']==(not a['accessible']),'retrieval independence')
  require(r['authors'] and r['title'] and r['citation'] and r['edition'],'identity metadata')
  require(r['next_obligation'] and r['formalization_status'],'recovery/formal obligation')
  require(r['proof']['all_original_assertions_claimed'] is False,'no blanket assertion equivalence')
  require(r['measurement']['node_count_factor_forbidden'] is True,'no node-count compression')
  require(all(e.get('available_local') is not False for e in r['proof']['evidence']),'all proof evidence resolved')
  if a['accessible']:
   require(r['principal_results_to_recover']['summary'],'accessible source actual target summary')
   require('pending' in r['programme_status'] or r['proof']['principal_contract_admitted'],'accessible original cannot be excluded')
   require(all(s['usable'] and len(s['sha256'])==64 for s in ss),'bound usable source')
   if not any(s['representation']=='primary_pdf'for s in ss):got_nonpdf.add(r['original_id'])
  else:
   require(a['availability_evidence_category']!='complete_original_available','unavailable is complete-body limitation')
   require('retrieval' in r['programme_status'],'unlocated original still targeted')
  if r['proof']['status']=='full_admitted_principal_contract':require(r['original_id']in principal,'principal status must have admission')
 require(got_nonpdf==NONPDF,'four complete nonPDF sources count as available')
 require(by['N001']['source_access']['usable_representations'][0]['authored_body_lines']==[181,220],'N001 source body excludes widget')
 require(by['L108']['source_access']['usable_representations'][0]['authored_body_lines']==[1,36],'L108 entire authored rendering')
 require(by['L028']['proof']['principal_contract_admitted']is False and by['F015']['proof']['principal_contract_admitted']is False,'author candidates not admitted by this inventory')
 require(by['N006']['source_access']['accessible']and by['N007']['source_access']['accessible'],'late existing PDFs restored')
 require(all(by[i]['source_access']['accessible'] is False for i in ['L097','L098','L101','L123']),'mislabelled duplicate files do not confer access')
 require(by['L007']['genuine_duplicate_original_id']is None and by['L127']['genuine_duplicate_original_id']is None,'unproved duplicate titles not merged')
 require(by['L073']['proof']['status']=='partial_census_with_source_table_gap','counts do not discharge table labels')
 return by

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--inventory',type=Path,default=P/'inventory.json');ap.add_argument('--study',type=Path,required=True);ap.add_argument('--public',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 if a.out.exists()or a.out.is_symlink():raise SystemExit('fresh output required')
 a.out.mkdir(parents=True);j=json.loads(a.inventory.read_text());by=validate(j);n=0
 for b in j['immutable_inputs']:
  p=(a.study if b['namespace']=='study'else a.public)/b['path'];raw=p.read_bytes();require(len(raw)==b['bytes']and hashlib.sha256(raw).hexdigest()==b['sha256'],'input binding '+str(p));n+=1
 for r in j['entries']:
  for s in r['source_access']['usable_representations']:
   if s['representation']=='primary_pdf':require((a.study/s['path']).read_bytes().startswith(b'%PDF-'),'PDF magic')
 csvpath=a.inventory.with_suffix('.csv');csvrows=list(csv.DictReader(csvpath.open()));require({x['id']for x in csvrows}==EXPECTED and len(csvrows)==161,'CSV original rows')
 for r in csvrows:
  x=by[r['id']];require(r['title']==x['title']and r['proof_status']==x['proof']['status']and r['accessible']==str(x['source_access']['accessible']),'CSV exact field agreement')
 batches=json.loads((a.inventory.parent/'prioritized_batches.json').read_text())['batches'];ids=[i for b in batches for i in b['original_ids']];require(len(ids)==len(set(ids)),'batch originals not duplicated');require(set(ids)==EXPECTED-{x['original_id']for x in j['entries']if x['proof']['principal_contract_admitted']},'every unfinished original remains in a batch')
 mutations=[]
 def reject(label,fn):
  c=copy.deepcopy(j);fn(c)
  try:validate(c)
  except (ValueError,KeyError,TypeError):mutations.append({'control':label,'rejected':True});return
  raise RuntimeError('mutation accepted: '+label)
 def row(c,i):return next(x for x in c['entries']if x['original_id']==i)
 reject('remove_original',lambda c:c['entries'].pop())
 reject('duplicate_original',lambda c:c['entries'].__setitem__(0,c['entries'][1]))
 reject('exclude_accessible_source',lambda c:row(c,'L036').__setitem__('target_remains_active',False))
 reject('drop_nonPDF_source',lambda c:row(c,'N001')['source_access'].__setitem__('accessible',False))
 reject('drop_late_source',lambda c:row(c,'N006')['source_access'].__setitem__('accessible',False))
 reject('inflate_author_candidate',lambda c:row(c,'L028')['proof'].__setitem__('principal_contract_admitted',True))
 reject('erase_table_gap',lambda c:row(c,'L073')['proof'].__setitem__('status','full_admitted_principal_contract'))
 reject('merge_distinct_titles',lambda c:row(c,'L127').__setitem__('genuine_duplicate_original_id','L007'))
 reject('include_N001_site_widget',lambda c:row(c,'N001')['source_access']['usable_representations'][0].__setitem__('authored_body_lines',[181,240]))
 reject('claim_all_assertions',lambda c:row(c,'L104')['proof'].__setitem__('all_original_assertions_claimed',True))
 reject('erase_target_statement',lambda c:row(c,'F001')['principal_results_to_recover'].__setitem__('summary',None))
 reject('missing_proof_binding',lambda c:row(c,'L028')['proof']['evidence'][0].__setitem__('available_local',False))
 reject('factor_from_inventory',lambda c:c.__setitem__('new_ratios',12))
 report={'status':'PASS_AUTHOR_INVENTORY_AUDIT_NOT_INDEPENDENT_MATH_REVIEW','originals':161,'available':104,'retrieval_targets':57,'principal_contracts':27,'all_unfinished_originals_in_batches':len(ids),'exact_input_bindings':n,'mutation_controls':mutations,'primary_files_redistributed':False,'fresh_full_proof_reviews':0,'new_credits':0,'ratios':None}
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
