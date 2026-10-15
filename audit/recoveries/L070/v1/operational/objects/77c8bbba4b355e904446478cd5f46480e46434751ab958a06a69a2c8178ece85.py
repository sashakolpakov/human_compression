"""Exact synthesis of accepted applications; no group/census execution."""
import sys
if sys.flags.optimize:
 raise RuntimeError('ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,json,collections,copy
P=Path(__file__).resolve().parent;C=P.parent

def need(x,s):
 if not x:raise ValueError(s)
def load(p):return json.loads(p.read_text())
def ranks(rows):
 z=collections.Counter()
 for r in rows:
  need(r['total']==sum(r['by_rank'].values()),'complete row total')
  z.update(r['by_rank'])
 return dict(sorted(z.items()))
def assemble(regular,chiral,aut,domain):
 rr={r['group_key']:r for r in regular['rows']};cc={r['group_key']:r for r in chiral['rows']}
 need(len(rr)==len(regular['rows'])==79 and set(rr)==set(cc)and len(cc)==len(chiral['rows']),'same79unique groups')
 rj={r['occurrence']:r for r in regular['joins']};cj={r['occurrence']:r for r in chiral['joins']};aj={r['occurrence']:r for r in aut['occurrence_joins']}
 need(len(rj)==len(regular['joins'])==88 and set(rj)==set(cj)==set(aj)and len(cj)==len(chiral['joins'])and len(aj)==len(aut['occurrence_joins']),'all88unique occurrences')
 joined=[];tables={};regraw=chiraw=0
 for label in sorted(rj):
  r,c,a=rj[label],cj[label],aj[label];key=r['group_key'];need(key==c['group_key']==a['group_key'],'literal common model join');need(r['computed_by_rank']==rr[key]['by_rank']and c['computed_by_rank']==cc[key]['by_rank'],'rank lists match acquired model')
  t=label.split('R')[0][1:];tab=tables.setdefault(t,dict(occurrences=0,regular=0,chiral=0,regular_rank_at_least4=0,chiral_rank_at_least4=0));tab['occurrences']+=1
  for kind,z in [('regular',r),('chiral',c)]:
   tab[kind]+=sum(z['computed_by_rank'].values());tab[kind+'_rank_at_least4']+=sum(v for n,v in z['computed_by_rank'].items()if int(n)>=4)
  joined.append(dict(occurrence=label,group_key=key,regular=r,chiral=c,automorphism_name=a))
 rt=ranks(list(rr.values()));ct=ranks(list(cc.values()));need(rt==regular['totals_by_rank']and ct==chiral['totals_by_rank'],'independent global rank sum')
 need(all(n%2==0 for n in ct.values()),'all chiral rank counts mirror pair')
 for t,tab in tables.items():
  for k,v in tab.items():need(chiral['table_totals'][t][k]==v,'accepted and independently joined family total')
 duplicates=dict(regular=sum(x['regular']for x in tables.values())-sum(rt.values()),chiral=sum(x['chiral']for x in tables.values())-sum(ct.values()))
 need(duplicates==dict(regular=95,chiral=50),'exact source duplicated occurrences')
 need(domain['classes_below_one_million']==80 and domain['classes_below_900000']==79 and domain['missing_section4_table']=='sp44'and domain['missing_group_order']==979200,'explicit historical domain correction')
 need([x['occurrence']for x in regular['mismatches']]==['T4R30']and[x['occurrence']for x in chiral['mismatches']]==['T6R03'],'exact exceptional source rows')
 return dict(status='COMPLETE_L070_PRINTED_SOURCE_SYNTHESIS_PENDING_DISTINCT_REVIEW',groups=79,occurrences=88,regular=sum(rt.values()),oriented_chiral=sum(ct.values()),mirror_pairs=sum(ct.values())//2,regular_by_rank=rt,chiral_by_rank=ct,tables=tables,duplicate_contributions=duplicates,joined_source_rows=joined,source_order_corrections=aut['order_corrections'],source_Aut_correction=aut['aut_label_correction'],larger_domain=dict(printed_groups=79,section4_socle_condition_classes=80,missing='Sp4(4)',order=979200,omitted_polytope_count=None,historical_program_execution_claim=False),new_censuses=0,whole_original_credit=0)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output')
 r=load(C/'regular_application_v1/application.json');c=load(C/'chiral_application_v2/application.json');aut=load(C/'chiral_application_v2/aut_columns.json');dom=load(C/'chiral_application_v2/domain.json');z=assemble(r,c,aut,dom)
 damaged=[]
 x=copy.deepcopy(c);x['rows'].pop();damaged.append((r,x,aut,dom))
 x=copy.deepcopy(c);x['joins'][0]['group_key']='WRONG';damaged.append((r,x,aut,dom))
 x=copy.deepcopy(r);x['rows'][0]['total']+=1;damaged.append((x,c,aut,dom))
 x=copy.deepcopy(aut);x['occurrence_joins'][0]['group_key']='WRONG';damaged.append((r,c,x,dom))
 x=copy.deepcopy(dom);x['classes_below_one_million']=79;damaged.append((r,c,aut,x))
 x=copy.deepcopy(c);x['totals_by_rank']['3']+=2;damaged.append((r,x,aut,dom))
 for args in damaged:
  try:assemble(*args)
  except ValueError:pass
  else:raise ValueError('damaged synthesis accepted')
 z['synthesis_damage_controls']=len(damaged);a.out.write_text(json.dumps(z,indent=2)+'\n');print(json.dumps({k:z[k]for k in ['status','groups','occurrences','regular','oriented_chiral','mirror_pairs','synthesis_damage_controls','new_censuses']}))
if __name__=='__main__':main()
