"""Independent small coordinate diagnostics; no premise of the uniform written proof."""
from collections import deque

def need(v,m):
 if not v:raise ValueError(m)
def edge(k,u,v):return(k,min(u,v),max(u,v))
def square(base,a,b):return {edge(a,base,base^(1<<a)),edge(b,base,base^(1<<b)),edge(a,base^(1<<b),base^(1<<a)^(1<<b)),edge(b,base^(1<<a),base^(1<<a)^(1<<b))}
def cube(r):return [tuple(x^(1<<i)for x in range(1<<r))for i in range(r)]
def orbit(gens,start):
 seen={start};q=[start]
 for u in q:
  for g in gens:
   v=g[u]
   if v not in seen:seen.add(v);q.append(v)
 return seen
def valid(g,Q):
 n=len(g[0]);r=len(g)
 need(len(orbit(g,0))==n,'transitive')
 need(all(g[i][g[j][x]]==g[j][g[i][x]]for i in range(r)for j in range(r)if abs(i-j)>1 for x in range(n)),'string')
 need(all(sum(k==i for k,u,v in Q)==2 for i in range(r)),'paired selection')
 for k,u,v in Q:
  need(g[k][u]==v,'actual coloured edge');need(v not in orbit(g[:k]+g[k+1:],u),'eligible actual orbit cut')
 return True
def cycles(Q):
 adj={};out=set()
 for k,u,v in Q:adj.setdefault(u,[]).append((v,k));adj.setdefault(v,[]).append((u,k))
 for first in adj:
  def walk(u,vs,es):
   for v,k in adj[u]:
    e=edge(k,u,v)
    if v==first and len(vs)>=3:out.add(frozenset(es+[e]))
    elif v>first and v not in vs:walk(v,vs+[v],es+[e])
  walk(first,[first],[])
 return out
def distance(Q,A,B):
 q=deque((a,0)for a in A);seen=set(A);adj={}
 for k,u,v in Q:adj.setdefault(u,[]).append(v);adj.setdefault(v,[]).append(u)
 while q:
  u,d=q.popleft()
  if u in B:return d
  for v in adj.get(u,[]):
   if v not in seen:seen.add(v);q.append((v,d+1))
 return None
def vertices(Q):return {u for k,u,v in Q}|{v for k,u,v in Q}
def run():
 records=[]
 Q=square(0,0,1);valid(cube(2),Q);need(len(cycles(Q))==1 and len(Q)==4,'sharp equality square')
 records.append(dict(case='sharp equality C2^2',n=4,r=2,edges=4,squares=1,strict_even_bound_false=True))
 g=cube(3);path=[0,1,3,7,6,4,0];Q={edge((u^v).bit_length()-1,u,v)for u,v in zip(path,path[1:])};valid(g,Q);need([len(c)for c in cycles(Q)]==[6],'actual long cycle')
 S=square(0,0,2);Q1=(Q-{edge(0,6,7),edge(2,3,7)})|{edge(0,4,5),edge(2,1,5)};valid(g,Q1);need(S<=Q1 and all(len(c)==4 for c in cycles(Q1)),'two missing-edge completion')
 records.append(dict(case='cube long-cycle completion',n=8,eligible_edges_per_colour=4,selected_edges_per_colour=2,missing_completion_edges=len(S-Q),old_cycle_lengths=[6],new_cycle_lengths=sorted(map(len,cycles(Q1)))))
 g=cube(5);S=square(0,0,2);T=square(2,3,4);Q=S|T|{edge(1,0,2),edge(1,8,10)};valid(g,Q)
 Q1=S|{edge(k,g[1][u],g[1][v])for k,u,v in Q-S};T1={edge(k,g[1][u],g[1][v])for k,u,v in T};valid(g,Q1)
 need(distance(Q,vertices(S),vertices(T))==1 and distance(Q1,vertices(S),vertices(T1))==0,'global transport with real collision')
 need(len(cycles(Q))==len(cycles(Q1))==2 and all(len(c)==4 for c in cycles(Q1)),'global cycles preserved')
 records.append(dict(case='global middle transport with intersecting target',n=32,old_distance=1,new_distance=0,old_squares=2,new_squares=2))
 g=cube(6);S=square(0,0,1);T=square(8,4,5);Q=S|T|{edge(2,0,4),edge(3,4,12),edge(2,12,8),edge(3,16,24)};valid(g,Q)
 need(distance(Q,vertices(S),vertices(T))==3,'repeated connector shortest distance')
 Q1=(Q-{edge(0,2,3),edge(2,0,4)})|{edge(0,4,5),edge(2,1,5)};valid(g,Q1)
 need(len(cycles(Q))==2 and len(cycles(Q1))==1 and all(len(c)==4 for c in cycles(Q1)),'repeated connector reduces squares')
 records.append(dict(case='ordinary repeated-colour connector',n=64,connector_colours=[2,3,2],old_squares=2,new_squares=1))
 g=[]
 for i in range(3):p=list(range(4));p[i],p[i+1]=p[i+1],p[i];g.append(tuple(p))
 checks=0
 for i in range(3):
  eligible=[(u,g[i][u])for u in range(4)if u<g[i][u]and g[i][u]not in orbit(g[:i]+g[i+1:],u)];need(len(eligible)==1,'single actual crossing')
  a,b=eligible[0]
  for j in range(3):
   if abs(j-i)>1:need(g[j][a]==a and g[j][b]==b,'distant endpoints fixed')
  for ell in range(3):
   for k in range(min(i,ell)+1,max(i,ell)):
    for x in (a,b):need(all(g[ell][y]==y for y in orbit(g[:k]+g[k+1:],x)),'no gap');checks+=1
 records.append(dict(case='S4 single crossings',n=4,colours=3,no_gap_checks=checks))
 return dict(status='PASS_BOUNDED_COORDINATE_DIAGNOSTICS',cases=records,uniform_proof_premise=False,author_code_imported=False,large_census=False)
if __name__=='__main__':
 import json
 print(json.dumps(run(),indent=2))
