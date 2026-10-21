from pathlib import Path
import argparse,csv,json,hashlib,math
from decimal import Decimal,localcontext

def need(x,m):
 if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fraction(x,n,d):
 need(x['numerator']==n and x['denominator']==d,'unreduced costs')
 g=math.gcd(n,d);need(x['exact_fraction']==str(n//g)+'/'+str(d//g),'reduced fraction')
 with localcontext() as ctx:
  ctx.prec=60;z=Decimal(n)/Decimal(d);want=format(z,'.12f')
 need(x['decimal']==want,'decimal division')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);a=ap.parse_args();p=a.packet;need(not a.out.exists(),'fresh output')
 m=load(p/'manifest.json')
 for e in m['exports']:
  q=p/e['path'];need(q.stat().st_size==e['bytes'] and sha(q)==e['sha256'],'export '+e['path'])
 r=load(p/'results.json');old=load(p/'inputs/previous_results.json');nums=load(p/'inputs/numbers_results.json')['primary'];scope=load(p/'programme_scope.json')
 t={x['topic']:x for x in r['topics']};prev={x['topic']:x for x in old['topics']};need(len(t)==19 and t.keys()==prev.keys(),'topic partition')
 oldpairs={z['source']:z for x in prev.values() for z in x['pairs']};pairs={z['source']:z for x in t.values() for z in x['pairs']};need(len(pairs)==52 and set(pairs)==set(oldpairs)|{'L047'},'only new L047')
 for k,x in t.items():
  if k!='B':need(x==prev[k],'whole non-B unchanged')
 for k,x in oldpairs.items():need(pairs[k]==x,'earlier individual unchanged')
 counted=0
 for k,x in t.items():
  ss=sum(z['source_cost'] for z in x['pairs']);aa=sum(z['application_cost'] for z in x['pairs']);uu=x['common_theory']
  need(x['source_count']==len(x['pairs']) and x['source_ids']==[z['source'] for z in x['pairs']],'matched whole source roster')
  need(x['source_sum']==ss and x['applications_sum']==aa and x['written_denominator']==uu+aa,'paid common and local totals')
  fraction(x['written'],ss,uu+aa);counted+=1
  for z in x['pairs']:fraction(z['conditional'],z['source_cost'],z['application_cost']);counted+=1
  for field in ['including_printed_programs','including_raw_programs','including_optional_validation','historical_software_cost','full_formalization_cost']:need(x[field] is None,'no unmatched software or invented unknown cost')
 b=t['B'];need(b['source_sum']==nums['source_sum'] and b['common_components']==nums['common_components'] and b['applications_sum']==nums['application_sum'],'root-adopted B costs')
 for i,z in pairs.items():
  if i in nums['conditional']:
   need(z['source_cost']==nums['source_costs'][i] and z['application_cost']==nums['applications'][i],'accepted B individual costs')
 need(b['whole_file_inventory']==load(p/'inputs/numbers_results.json')['whole_file_inventory'],'entire accepted inventory')
 need('v10' not in b['current_written_reason'],'stale current v10 reason removed')
 need(b['current_written_status']!='AVAILABLE_FROM_UNCHANGED_MATCHED_MANUSCRIPT_BOUNDARY','new edition status')
 groups=[set(scope[k]) for k in ['measured_original_ids','mathematical_pending_original_ids','editorial_original_ids','archived_original_ids']]
 need([len(x) for x in groups]==[52,53,1,55],'corpus counts')
 need(len(set.union(*groups))==161 and all(not groups[i]&groups[j] for i in range(4) for j in range(i)),'disjoint historical partition')
 need(groups[0]==set(pairs) and groups[0]|groups[1]|groups[2]==set(scope['active_original_ids']),'active106exact')
 need(scope['actual_root_registration_binding'] is None and r['whole_programme_binding']['registration_sha256'] is None,'publication still separate')
 need(r['pooled_factor'] is None and r['cross_topic_deduplication'] is False,'no pooled or overlap discount')
 need(counted==r['written_and_conditional_comparisons']==71,'all71')
 result=dict(status='PASS_DISTINCT_OVERVIEW_ARITHMETIC',reviewer='root',author_manifest_sha256=sha(p/'manifest.json'),exact_fractions=71,whole_topics=19,originals=52,unchanged_non_B_topic_objects=18,unchanged_earlier_individual_objects=51,partition=[52,53,1,55],all_inputs_previously_adopted=True,new_scientific_credit=0,publication_registration_pending=True,method='Direct reconstruction with integer sums, gcd reductions and decimal division; no author build or arithmetic imports. All admitted B input vectors and whole-file inventory retained.')
 a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
