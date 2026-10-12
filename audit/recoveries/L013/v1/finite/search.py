"""Exact middle-graph CP-SAT model; completion requires OPTIMAL enumeration status."""
from pathlib import Path
import argparse,base64,json,time
from collections import deque,Counter
from itertools import combinations
from ortools.sat.python import cp_model
import pynauty

def setup(k):
 V=[(i,j) for i in range(k) for j in range(k) if i!=j];N=len(V)
 E=[(a,b) for a,b in combinations(range(N),2) if V[a][0]!=V[b][0] and V[a][1]!=V[b][1]]
 idx={e:i for i,e in enumerate(E)};pos=[set() for _ in V]
 for a,b in E:pos[a].add(b);pos[b].add(a)
 def edge(a,b):return idx[tuple(sorted((a,b)))]
 forbidden=set()
 for v in range(N):
  for a,b in combinations(sorted(pos[v]),2):
   pair={edge(v,a),edge(v,b)}
   if V[a][0]==V[b][0] or V[a][1]==V[b][1]:forbidden.add(tuple(sorted(pair)))
   if b in pos[a]:forbidden.add(tuple(sorted(pair|{edge(a,b)})))
 for a,b in combinations(range(N),2):
  for v,w in combinations(sorted(pos[a]&pos[b]),2):forbidden.add(tuple(sorted({edge(a,v),edge(a,w),edge(b,v),edge(b,w)})))
 m=cp_model.CpModel();xs=[m.new_bool_var('e'+str(i)) for i in range(len(E))]
 for v in range(N):m.add(sum(xs[edge(v,u)] for u in pos[v])==k-2)
 for f in sorted(forbidden):m.add_bool_or([xs[i].Not() for i in f])
 return V,E,m,xs,dict(vertices=N,edge_variables=len(E),degree_equations=N,forbidden_constraints=len(forbidden))

def extend(k,edges):
 V=[(i,j) for i in range(k) for j in range(k) if i!=j];N=len(V);A=[set() for _ in range(N+2*k+2)]
 def add(a,b):A[a].add(b);A[b].add(a)
 for a,b in edges:add(a,b)
 for v,(i,j) in enumerate(V):add(v,N+i);add(v,N+k+j)
 for i in range(k):add(N+i,N+2*k);add(N+k+i,N+2*k+1)
 return A

def graph(A):return pynauty.Graph(len(A),adjacency_dict={i:list(sorted(row)) for i,row in enumerate(A)})
def classify(k,edges):
 A=extend(k,edges);g=graph(A);c=pynauty.certificate(g).hex();aut=pynauty.autgrp(g)
 order=int(aut[1])*10**int(aut[2]);return c,dict(middle_edges=edges,adjacency=[sorted(x) for x in A],automorphism_order=order,automorphism_generators=aut[0],vertex_orbits=aut[3])

class Collector(cp_model.CpSolverSolutionCallback):
 def __init__(self,k,E,xs,out,max_solutions=0):super().__init__();self.k=k;self.E=E;self.xs=xs;self.out=out;self.count=0;self.groups={};self.solutions=[];self.start=time.monotonic();self.max_solutions=max_solutions
 def on_solution_callback(self):
  self.count+=1;edges=[e for e,x in zip(self.E,self.xs) if self.value(x)];c,row=classify(self.k,edges);self.solutions.append(dict(edge_indices=[i for i,x in enumerate(self.xs) if self.value(x)],full_graph_certificate=c))
  if c not in self.groups:self.groups[c]=row;print(json.dumps(dict(k=self.k,solutions=self.count,new_class=len(self.groups),orders=sorted(r['automorphism_order'] for r in self.groups.values()),seconds=time.monotonic()-self.start)),flush=True);self.save('RUNNING')
  if self.max_solutions and self.count>=self.max_solutions:self.stop_search()
 def save(self,status,extra=None):
  data=dict(k=self.k,status=status,labelled_solutions=self.count,full_graph_classes=len(self.groups),labelled_graphs=self.solutions,automorphism_orders=sorted(r['automorphism_order'] for r in self.groups.values()),graphs=[dict(certificate=c,**v) for c,v in sorted(self.groups.items())],elapsed_seconds=time.monotonic()-self.start)
  if extra:data.update(extra)
  self.out.write_text(json.dumps(data,indent=2)+'\n')

def main(a):
 start=time.monotonic();V,E,m,xs,stats=setup(a.k);a.out.parent.mkdir(parents=True,exist_ok=True)
 print(json.dumps(dict(k=a.k,model=stats,build_seconds=time.monotonic()-start)),flush=True)
 sol=cp_model.CpSolver();sol.parameters.enumerate_all_solutions=True;sol.parameters.num_search_workers=1;sol.parameters.max_time_in_seconds=a.seconds
 sol.parameters.random_seed=a.seed
 cb=Collector(a.k,E,xs,a.out,a.max_solutions);status=sol.solve(m,cb)
 cb.save(sol.status_name(status),dict(complete=status==cp_model.OPTIMAL and not a.max_solutions,model=stats,solver_stats=sol.response_stats(),time_limit_seconds=a.seconds,seed=a.seed))
 print(json.dumps(dict(status=sol.status_name(status),solutions=cb.count,classes=len(cb.groups),seconds=time.monotonic()-start)),flush=True)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--k',type=int,required=True);p.add_argument('--seconds',type=float,default=60);p.add_argument('--seed',type=int,default=0);p.add_argument('--max-solutions',type=int,default=0);p.add_argument('--out',type=Path,required=True);main(p.parse_args())
