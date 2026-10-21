"""Required exact finite checks; no SAT or nauty import, no graph database trust."""
from pathlib import Path
from itertools import combinations
import argparse,hashlib,json,time
from direct_graphs import need,check_simple,profile,distances,isomorphisms,valid_map,generated_order,middle_profiles
HERE=Path(__file__).resolve().parent
EXPECTED={3:[4,12],4:[1,2,4,8],5:[4,4,10,10,48,64,1920]}

def load(path):return json.loads(path.read_text())
def edge_universe(k):
 V=[(i,j) for i in range(k) for j in range(k) if i!=j]
 E=[(u,v) for u,v in combinations(range(len(V)),2) if V[u][0]!=V[v][0] and V[u][1]!=V[v][1]]
 return V,E

def middle(k,edges):
 V,E=edge_universe(k);N=len(V);A=[set() for _ in V];allowed=set(E)
 need(len(edges)==len(set(map(tuple,edges))) and all(tuple(e) in allowed for e in edges),'unique allowed edges')
 for u,v in edges:A[u].add(v);A[v].add(u)
 need(all(len(x)==k-2 for x in A),'middle degree')
 for u,v in combinations(range(N),2):
  common=A[u]&A[v]
  need(len(common)<=1,'middle four-cycle')
  need(not(v in A[u] and common),'middle triangle')
  if V[u][0]==V[v][0] or V[u][1]==V[v][1]:need(v not in A[u] and not common,'row/column separation')
 G=[set(x) for x in A]+[set() for _ in range(2*k+2)]
 def add(u,v):G[u].add(v);G[v].add(u)
 for u,(i,j) in enumerate(V):add(u,N+i);add(u,N+k+j)
 for i in range(k):add(N+i,N+2*k);add(N+k+i,N+2*k+1)
 return G

def decoded_graph6(raw):
 values=[c-63 for c in raw.strip()];n=values[0];need(0<=n<=62,'small graph6 order')
 bits=[(x>>j)&1 for x in values[1:] for j in range(5,-1,-1)];need(len(bits)>=n*(n-1)//2,'graph6 extent');A=[set() for _ in range(n)];pos=0
 for j in range(1,n):
  for i in range(j):
   if bits[pos]:A[i].add(j);A[j].add(i)
   pos+=1
 need(not any(bits[pos:]),'graph6 zero padding');return A

def verify(root=HERE):
 report=dict(status='PASS_EXACT_FINITE_L013_COMPONENT',censuses=[],witnesses=[],historical_identifiers=[],figure1=[],no_k6_completeness_claim=True);reps={}
 for k in [3,4,5]:
  data=load(root/f'k{k}_complete.json');need(data['status']=='OPTIMAL' and data['complete'],'completed exact SAT enumeration')
  sols=data['labelled_graphs'];need(len(sols)==data['labelled_solutions']=={3:4,4:102,5:240}[k],'exact labelled count')
  need(len({tuple(r['edge_indices']) for r in sols})==len(sols),'no duplicate assignments')
  graphs=data['graphs'];need(len(graphs)=={3:2,4:4,5:7}[k],'full class count')
  certificates={r['certificate']:r for r in graphs};need(len(certificates)==len(graphs),'distinct class keys')
  V,E=edge_universe(k);out=[];reps[k]=[]
  for index,r in enumerate(graphs):
   A=check_simple(r['adjacency']);B=middle(k,r['middle_edges']);need(A==B,'actual extension')
   p=profile(A);need(p==dict(order=k*k+k+2,degrees=[k],girth=5,diameter=4,connected=True),'exact full graph parameters')
   aut=isomorphisms(A,A);lower=generated_order(A,r['automorphism_generators']);need(aut['count']==lower==r['automorphism_order'],'full automorphism equality')
   ms=middle_profiles(A)
   if k==3:target=(None,None)
   elif k==4:target=(12,6)
   elif r['automorphism_order']==4:target=(6,4)
   elif r['automorphism_order']==10:target=(5,4)
   else:target=(5,5)
   choices=[m for m in ms if (m['profile']['girth'],m['profile']['diameter'])==target];need(choices,'source chosen middle profile')
   chosen=choices[0];need(chosen['profile']['order']==k*(k-1) and chosen['profile']['degrees']==[k-2],'chosen middle size/degree')
   if k==3:need(all(len(A[v]&set(chosen['middle_vertices']))==1 for v in chosen['middle_vertices']),'three disjoint edges')
   z=dict(id=f'k{k}_{index+1}',parameters=p,automorphism_order=aut['count'],automorphism_search_nodes=aut['nodes'],generator_group_order=lower,chosen_diametral_pair=chosen['pair'],chosen_middle_profile=chosen['profile'],all_diametral_middle_profiles=ms)
   out.append(z);reps[k].append((z['id'],A))
  for i,j in combinations(range(len(graphs)),2):need(isomorphisms(graphs[i]['adjacency'],graphs[j]['adjacency'],first=True)['count']==0,'distinct unrooted classes')
  need(sorted(r['automorphism_order'] for r in out)==EXPECTED[k],'source automorphism orders')
  labelled=[]
  for i,r in enumerate(sols):
   ids=r['edge_indices'];need(ids==sorted(set(ids)) and all(0<=j<len(E) for j in ids),'literal Boolean assignment')
   G=middle(k,[E[j] for j in ids]);target=certificates[r['full_graph_certificate']]
   iso=isomorphisms(G,target['adjacency'],first=True);need(iso['count']==1,'every SAT output covered by actual representative')
   labelled.append(dict(assignment=i,representative=next(j for j,x in enumerate(graphs) if x['certificate']==r['full_graph_certificate']),permutation=iso['witness']))
  report['censuses'].append(dict(k=k,labelled_graphs=len(sols),classes=len(out),graphs=out,literal_assignment_maps=labelled))
 g6=(root/'inputs/n44_k6_g5_d4.g6').read_bytes();witnessdata=load(root/'k6_witnesses.json');need(witnessdata['status']=='WITNESS_INPUTS_NO_CENSUS_CLAIM','witness-only scope')
 need(hashlib.sha256(g6).hexdigest()==witnessdata['provenance']['sha256'],'graph6 input pin')
 rows=g6.splitlines();need(len(rows)==2,'two inputs')
 for i,(line,r) in enumerate(zip(rows,witnessdata['graphs'])):
  A=decoded_graph6(line);need(A==check_simple(r['adjacency']),'independent graph6 decoding');p=profile(A)
  need(p==dict(order=44,degrees=[6],girth=5,diameter=4,connected=True),'degree-six witness parameters')
  upper=isomorphisms(A,A);lower=generated_order(A,r['automorphism_generators']);need(upper['count']==lower==r['automorphism_order'],'degree-six full automorphisms')
  report['witnesses'].append(dict(id=f'k6_{i+1}',parameters=p,automorphism_order=lower,automorphism_search_nodes=upper['nodes'],all_diametral_middle_profiles=middle_profiles(A)))
 need(sorted(x['automorphism_order'] for x in report['witnesses'])==[40,240],'source two witness orders')
 need(isomorphisms(witnessdata['graphs'][0]['adjacency'],witnessdata['graphs'][1]['adjacency'],first=True)['count']==0,'two nonisomorphic examples')
 historical=load(root/'historical_graphs.json')
 for r in historical['graphs']:
  A=check_simple(r['adjacency']);matches=[]
  for identity,B in reps[r['degree']]:
   m=isomorphisms(A,B,first=True)
   if m['count']:matches.append(dict(class_id=identity,permutation=m['witness']))
  need(len(matches)==1,'exact historical identifier match');need(isomorphisms(A,A)['count']==r['source_automorphism_order'],'literal HoG order')
  report['historical_identifiers'].append(dict(HoG_id=r['HoG_id'],**matches[0]))
 figure=load(root/'figure1_edges.json');need(len(figure['black_edges'])==19,'source black edges')
 for color,hog,order in [('red',1000,12),('green',50487,4)]:
  A=[set() for _ in range(14)]
  for u,v in figure['black_edges']+figure[color+'_edges']:A[u].add(v);A[v].add(u)
  B=next(r['adjacency'] for r in historical['graphs'] if r['HoG_id']==hog);m=isomorphisms(A,B,first=True)
  need(m['count']==1 and isomorphisms(A,A)['count']==order,'literal colored Figure1 graph')
  report['figure1'].append(dict(color=color,HoG_id=hog,permutation=m['witness'],automorphism_order=order))
 return report

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();start=time.monotonic();r=verify();a.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(dict(status=r['status'],censuses=[(x['k'],x['labelled_graphs'],x['classes']) for x in r['censuses']],k6=[x['automorphism_order'] for x in r['witnesses']],seconds=time.monotonic()-start)))
