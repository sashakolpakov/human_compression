from pathlib import Path
from itertools import combinations
import json,hashlib,argparse

def need(t,m):
 if not t:raise ValueError(m)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--packet',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);a=ap.parse_args();need(not a.out.exists(),'fresh output');p=a.packet;m=json.loads((p/'manifest.json').read_text())
 for e in m['exports']:
  b=(p/e['path']).read_bytes();need(len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'],'export '+e['path'])
 data=json.loads((p/'results.json').read_text())['rows'];need(len(data)==3,'all three J1 inputs')
 full=0;high=0;decisions=0;counts={};failed=[]
 for row in data:
  n=row['rank'];types=set(range(1,n+1));res=row['residues'];expected={c for k in range(n) for c in combinations(range(1,n+1),k)}
  need({tuple(x['fixed_types']) for x in res}==expected and len(res)==len(expected),'all base flags')
  for x in res:
   rank=n-len(x['fixed_types']);need(x['residue_rank']==rank and set(x['types'])==types-set(x['fixed_types']),'all remaining types');full+=1
   need(row['order']==x['order']*x['flag_orbit_size'],'actual residue multiplicities')
   need(x['flag_transitive'] and x['connected'] and any(x['primitive_types']),'FT/RC/RWPRI')
   if rank>=2:
    high+=1;decisions+=rank;need(len(x['type_results'])==rank and x['IP']==all(x['type_results']) and x['WIP']==any(x['type_results']),'type quantification')
   else:need(x['firm'] and x['panel_size']>=2,'firm panels')
  rr={x['rank']:x for x in row['by_rank']};need(set(rr)==set(range(2,n+1)),'all ranks')
  for k,x in rr.items():
   these=[z for z in res if z['residue_rank']==k];need(x['base_residues']==len(these) and x['actual_residues']==sum(z['flag_orbit_size'] for z in these),'per-rank residue counts')
   need(x['IPk']==all(z['IP'] for z in these) and x['WIPk']==all(z['WIP'] for z in these),'forall residues, separate exists type')
  need(row['IP']==all(x['IPk'] for x in rr.values()) and row['WIP']==all(x['WIPk'] for x in rr.values()),'full residual quantification')
  panel2t=all(x['two_transitive'] for x in res if x['residue_rank']==1);need(row['filters']['twoT1']==panel2t,'panel2T')
  need(row['source_filter_pass']==all(row['filters'].values()),'all source filters')
  if not row['source_filter_pass']:failed.append([row['member'],row['active_row']])
  else:
   counts.setdefault(row['member'],[0,0,0])[0 if row['IP'] else 1 if row['WIP'] else 2]+=1
 need((full,high,decisions)==(37,26,65),'full residue counts')
 expected={'j1.rk3':[0,0,1],'j1.rk4':[1,0,1]};need(counts==expected,'aggregates')
 need(failed==[],'qualified exact rows')
 report=dict(status='PASS_DISTINCT_RESIDUE_QUANTIFIER_RECONSTRUCTION',author_manifest_sha256=hashlib.sha256((p/'manifest.json').read_bytes()).hexdigest(),rows=3,all_nonempty_base_residues=full,base_residues_rank_at_least_two=high,type_decisions_rank_at_least_two=decisions,full_filtered_IP_weak_only_neither=counts,excluded_action_rows=failed,method='Independent enumeration of every flag-type subset and reconstruction of all rank quantifiers from retained exact finite results; no author engine imports. The accepted generic shadow engine is unchanged; its bounded J1 execution is retained, not re-executed by this reconstruction.')
 a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
