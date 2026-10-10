#!/usr/bin/env python3
"""Direct coset-geometry diagnostic for the endpoint-support S6 separator."""
import argparse,hashlib,itertools,json
from pathlib import Path


def mul(p,q): return tuple(p[q[i]] for i in range(len(p)))
def cyc(n,*cs):
 p=list(range(n))
 for c in cs:
  for x,y in zip(c,c[1:]+c[:1]):p[x]=y
 return tuple(p)
def group(gs,n=6):
 seen={tuple(range(n))};q=list(seen)
 for x in q:
  for g in gs:
   y=mul(x,g)
   if y not in seen:seen.add(y);q.append(y)
 return frozenset(seen)
def bitset(elements,index):
 s=0
 for x in elements:s|=1<<index[x]
 return s


def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
 if args.output.exists():p.error('Use a new report path.')
 gs=(cyc(6,(0,1)),cyc(6,(0,2),(1,3),(4,5)),cyc(6,(3,4)),cyc(6,(3,5)))
 G=group(gs);elements=sorted(G);index={g:i for i,g in enumerate(elements)}
 lattice=[group([g for i,g in enumerate(gs) if mask>>i&1]) for mask in range(16)]
 assert all(lattice[i]&lattice[j]==lattice[i&j] for i in range(16) for j in range(16))
 cosets=[]
 for i in range(4):
  H=lattice[15^(1<<i)]
  row={bitset((mul(g,h) for h in H),index) for g in G}
  cosets.append(sorted(row))
 flags={};helly_bad={};witness=None
 for mask in range(1,16):
  types=[i for i in range(4) if mask>>i&1];flags[mask]=[];helly_bad[mask]=0
  for choices in itertools.product(*(range(len(cosets[i])) for i in types)):
   blocks=[cosets[i][j] for i,j in zip(types,choices)]
   if not all(x&y for x,y in itertools.combinations(blocks,2)):continue
   flag=tuple(zip(types,choices));flags[mask].append(flag)
   common=(1<<len(G))-1
   for block in blocks:common &= block
   if not common:
    helly_bad[mask]+=1
    if witness is None:
     witness={'typed_coset_indices':flag,'left_coset_representatives':[elements[(block&-block).bit_length()-1] for block in blocks]}
 chambers=flags[15];panel_counts=[];bad_extensions=0
 for mask,fs in flags.items():
  for flag in fs:
   count=sum(all(pair in chamber for pair in flag) for chamber in chambers)
   if len(flag)==3:panel_counts.append(count)
   bad_extensions += count==0
 # Distinct endpoint shadows and B2, on the literal old coset incidence.
 endpoints=[]
 for edge in cosets[1]:endpoints.append(frozenset(v for v,V in enumerate(cosets[0]) if V&edge))
 B1=all(len(s)==2 for s in endpoints) and len(set(endpoints))==len(endpoints)
 B2_bad=[]
 for i in (2,3):
  for j,X in enumerate(cosets[i]):
   shadow=frozenset(v for v,V in enumerate(cosets[0]) if V&X)
   for e,E in enumerate(cosets[1]):
    if bool(E&X)!=(endpoints[e]<=shadow):B2_bad.append([i,j,e,sorted(endpoints[e]),sorted(shadow)])
 report={'status':'PASS','checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'group_order':len(G),'generators_zero_based':gs,'old_IP_meets':256,
 'maximal_parabolic_orders':[len(lattice[15^(1<<i)]) for i in range(4)],
 'type_sizes':list(map(len,cosets)), 'flags_by_type_mask':{str(k):len(v) for k,v in flags.items()},
 'pairwise_incident_families_without_common_group_element_by_mask':helly_bad,
 'first_Helly_failure':witness,'all_flags_extend_to_chambers':bad_extensions==0,
 'unextendible_flags':bad_extensions,'chambers':len(chambers),
 'corank_one_completion_counts':sorted(set(panel_counts)), 'B1':B1,'B2':not B2_bad,
 'B2_failure_count':len(B2_bad),'first_B2_failure':B2_bad[0] if B2_bad else None,
 'scope':'Single explicit C-group. Every typed coset flag checked; no catalogue or general theorem inferred.'}
 assert len(G)==720 and B1
 assert witness is not None and not B2_bad and bad_extensions==90
 assert helly_bad[13]==90 and sum(helly_bad.values())==90
 assert len(chambers)==720 and sorted(set(panel_counts))==[0,2]
 args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
 print(json.dumps({k:report[k] for k in ['type_sizes','chambers','all_flags_extend_to_chambers','corank_one_completion_counts','B1','B2','B2_failure_count']}))
 print('PASS')
if __name__=='__main__':main()
