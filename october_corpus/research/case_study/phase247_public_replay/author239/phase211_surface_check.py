#!/usr/bin/env python3
"""Exact cellular witnesses for phase211; uniform topology remains a written proof."""
import argparse
from collections import deque
import copy
import hashlib
import json
from pathlib import Path
import time

ROOT=Path(__file__).resolve().parent
D_FILE='phase109_cover_families_generalization_model.json'
D_SHA='3299bad80e6880a7e45000662dc981bc54c623bf581676a9829912b7bea06715'

def require(ok,label):
 if not ok:raise ValueError(label)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def mul(g,h):return tuple(h[x] for x in g)

def generated(gens,degree,limit):
 one=tuple(range(degree));group=[one];index={one:0};words=[[]]
 for g in group:
  for i,s in enumerate(gens):
   h=mul(g,s)
   if h not in index:
    require(len(group)<limit,'group enumeration limit')
    index[h]=len(group);group.append(h);words.append(words[index[g]]+[i])
 return group,index,words

def tomotope_model():
 def perm(cycles):
  p=list(range(12))
  for cyc in cycles:
   for a,b in zip(cyc,cyc[1:]+cyc[:1]):p[a-1]=b-1
  return tuple(p)
 gens=[perm(x) for x in [[(5,10),(6,9),(7,12),(8,11)],[(1,6),(2,5),(3,8),(4,7)],[(5,9),(6,10),(7,11),(8,12)],[(5,8),(6,7),(9,12),(10,11)]]]
 group,index,words=generated(gens,12,97);require(len(group)==96,'Tomotope automorphism order')
 labels=[];counts=[];one=tuple(range(12))
 for ids in [(1,2,3),(0,2,3),(0,1),(0,1,2),(0,1,3)]:
  H,_,_=generated([gens[i] for i in ids],12,97)
  label={};num=0
  for g in group:
   if g not in label:
    for h in H:label[mul(h,g)]=num
    num+=1
  require(len(label)==96,'Wythoff cosets do not partition')
  labels.append(label);counts.append(num)
 require(counts==[4,12,16,4,4],'Tomotope face counts')
 flags=[tuple(labels[i][g] for i in range(3))+(4*ty+labels[3+ty][g],) for ty in [0,1] for g in group]
 require(len(flags)==len(set(flags))==192,'literal Wythoff flags')
 adjacency=[]
 for i in range(4):
  classes={}
  for k,f in enumerate(flags):classes.setdefault(f[:i]+f[i+1:],[]).append(k)
  require(all(len(c)==2 for c in classes.values()),'unique flag adjacency')
  a=[0]*192
  for u,v in classes.values():a[u]=v+1;a[v]=u+1
  adjacency.append(a)
 return {'name':'Tomotope','degree':192,'generators':adjacency}, {'automorphism_order':96,'face_counts':counts,'flags':192}

def analyze(model,details=False):
 degree=model['degree'];gens=[tuple(x-1 for x in s) for s in model['generators']];one=tuple(range(degree))
 require(len(gens)==4 and all(sorted(s)==list(one) for s in gens),'permutations')
 require(all(mul(s,s)==one and s!=one for s in gens),'nontrivial involutions')
 require(all(mul(gens[i],gens[j])==mul(gens[j],gens[i]) and gens[i]!=gens[j] for i,j in [(0,2),(0,3),(1,3)]),'proper string pairs')
 require(len(set(gens))==4,'distinct marks')
 group,index,words=generated(gens,degree,20000);n=len(group)
 adjacency=[[index[mul(g,s)] for s in gens] for g in group]
 edges=[];edge_index={}
 for v in range(n):
  for i in range(4):
   w=adjacency[v][i]
   require(w!=v and adjacency[w][i]==v,'Cayley involution edges')
   if v<w:edge_index[v,i]=edge_index[w,i]=len(edges);edges.append((v,w,i))
 require(len(edges)==2*n,'Cayley edge count')
 def component(ids,start=0):
  seen={start};todo=[start]
  for a in todo:
   for i in ids:
    b=adjacency[a][i]
    if b not in seen:seen.add(b);todo.append(b)
  return seen
 faces=[];edgefaces=[[] for _ in edges];edge_signs=[{} for _ in edges]
 for ids in [(0,2),(0,3),(1,3),(1,2)]:
  todo=set(range(n))
  while todo:
   start=min(todo);verts=component(ids,start);todo-=verts
   ee={edge_index[v,i] for v in verts for i in ids}
   require(len(ee)==len(verts),'two-color cycle cardinality')
   if ids!=(1,2):require(len(verts)==4,'nonadjacent square cardinality')
   f=len(faces);faces.append((ids,verts,ee))
   for e in ee:edgefaces[e].append(f)
   v=start;step=0;visited=set()
   while True:
    require(v not in visited,'repeated vertex within polygon')
    visited.add(v);i=ids[step%2];w=adjacency[v][i];e=edge_index[v,i]
    edge_signs[e][f]=1 if v<w else -1
    v=w;step+=1
    if v==start:break
   require(step==len(ee) and visited==verts,'complete polygon boundary')
 require(all(len(fs)==2 for fs in edgefaces),'surface edge incidence')
 # Each vertex has exactly the four prescribed corners, and a cyclic link.
 for v in range(n):
  corners=[ids for ids,vs,ee in faces if v in vs]
  require(sorted(corners)==[(0,2),(0,3),(1,2),(1,3)],'surface vertex link')
 orientable=all((len(words[v])-len(words[w]))%2==1 for v,w,_ in edges)
 def dual_components(selected_edges,selected_faces):
  out=set(range(len(faces)))-selected_faces;links={f:[] for f in out}
  for e,fs in enumerate(edgefaces):
   if e not in selected_edges:
    f,h=fs;require(f in out and h in out,'complement dual edge')
    sign=-edge_signs[e][f]*edge_signs[e][h]
    links[f].append((h,sign));links[h].append((f,sign))
  components=[]
  while out:
   root=min(out);q=[root];out.remove(root);ori={root:1};parent={root:root};ok=True;bad=[]
   for f in q:
    for h,sign in sorted(links[f]):
     if h in ori:
      if ori[h]!=ori[f]*sign:ok=False;bad.append([f,h,sign])
     else:ori[h]=ori[f]*sign;parent[h]=f
     if h in out:out.remove(h);q.append(h)
   require(set(q)==set(ori)==set(parent),'component spanning tree')
   row={'size':len(q),'orientable':ok,'root':root}
   if details:row.update({'vertices':sorted(q),'parent':[[x,parent[x]] for x in sorted(q)],'orientation_conflict':bad[:1]})
   components.append(row)
  return components
 whole=dual_components(set(),set())
 require(len(whole)==1 and whole[0]['orientable']==orientable,'two independent orientability calculations')
 def check(ii,jj):
  aa,bb=component(ii),component(jj);kk=tuple(sorted(set(ii)&set(jj)));cc=component(kk)
  selected_edges={e for e,(v,w,i) in enumerate(edges) if (v in aa and i in ii) or (v in bb and i in jj)}
  selected_faces={f for f,(ids,vs,ee) in enumerate(faces) if (set(ids)<=set(ii) and vs<=aa) or(set(ids)<=set(jj) and vs<=bb)}
  comps=dual_components(selected_edges,selected_faces)
  forbidden=sorted((aa&bb)-cc)
  row={'pair':[list(ii),list(jj)],'base_orders':[len(aa),len(bb),len(cc)],'base_intersection_order':len(aa&bb),
       'selected_disks':len(selected_faces),'complement_components':comps,
       'homology_injective_odd':(len(comps)==1 if orientable else not any(c['orientable'] for c in comps)),
       'homology_injective_two':len(comps)==1,'base_defect_count':len(forbidden)}
  if forbidden:row['base_defect_word']=words[forbidden[0]]
  if details:row.update({'selected_edges':sorted(selected_edges),'selected_faces':sorted(selected_faces)})
  return row
 q=len(component((1,2)))//2
 chi=n-len(edges)+len(faces)
 require(chi==n//(2*q)-n//4,'surface Euler formula')
 tests=[check((0,1,2),(1,2,3)),check((0,1),(1,2)),check((1,2),(2,3))]
 result={'name':model.get('name'),'order':n,'cells':[n,len(edges),len(faces)],'middle_order':q,'orientable':orientable,
       'Euler_characteristic':chi,'H1_dimension_odd':(2 if orientable else 1)-chi,'H1_dimension_two':2-chi,
       'pairs':tests,'all_odd_prime_criterion':all(t['homology_injective_odd'] for t in tests),'prime_two_criterion':all(t['homology_injective_two'] for t in tests)}
 if details:result.update({'edges':edges,'faces':[{'colors':ids,'vertices':sorted(vs),'edges':sorted(ee)} for ids,vs,ee in faces],
                         'Cayley_generator_edges':adjacency,'generated_words':words})
 return result

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
 require(not args.out.exists() and not args.out.is_symlink(),'fresh output directory required')
 start=time.monotonic();require(sha(ROOT/D_FILE)==D_SHA,'frozen D input hash')
 D=json.loads((ROOT/D_FILE).read_text());D['name']='D256'
 T,bridge=tomotope_model()
 d=analyze(D,True);t=analyze(T,False)
 require(d['cells']==[256,512,224] and d['orientable'] and d['H1_dimension_odd']==34,'D surface parameters')
 require([x['complement_components'][0]['size'] for x in d['pairs']]==[178,223,223] and all(len(x['complement_components'])==1 for x in d['pairs']),'D literal complement components')
 require(d['all_odd_prime_criterion'] and d['prime_two_criterion'],'D uniform criterion')
 require(t['cells']==[18432,36864,14592] and not t['orientable'] and t['H1_dimension_odd']==3841,'Tomotope surface parameters')
 require([x['complement_components'][0]['size'] for x in t['pairs']]==[14090,14591,14591] and all(len(x['complement_components'])==1 for x in t['pairs']),'Tomotope literal complement components')
 require(t['all_odd_prime_criterion'] and t['prime_two_criterion'],'Tomotope uniform criterion')
 require(d['pairs'][0]['base_defect_count']>0 and t['pairs'][0]['base_defect_count']>0,'nonpolytopal targets')
 negative={'name':'independent_marks_do_not_suffice','degree':8,'generators':[[4,6,7,1,8,2,3,5],[2,1,6,5,4,3,8,7],[3,6,1,7,8,2,4,5],[2,1,5,6,3,4,8,7]]}
 bad=analyze(negative)
 require(not bad['all_odd_prime_criterion'] and [c['size'] for c in bad['pairs'][0]['complement_components']]==[9,9],'negative complement control')
 broken=copy.deepcopy(D);broken['generators'][0]=list(range(1,17))
 try:analyze(broken)
 except ValueError as e:control=str(e)
 else:raise ValueError('identity-generator mutation accepted')
 args.out.mkdir(parents=True)
 (args.out/'D256_cell_certificate.json').write_text(json.dumps(d,indent=2)+'\n')
 (args.out/'Tomotope_cell_report.json').write_text(json.dumps({'construction':bridge,'surface':t},indent=2)+'\n')
 (args.out/'Tomotope_model.json').write_text(json.dumps(T,indent=2)+'\n')
 (args.out/'negative_control.json').write_text(json.dumps(bad,indent=2)+'\n')
 report={'status':'PASS','seconds':round(time.monotonic()-start,3),'program_sha256':sha(Path(__file__)),
         'input':{D_FILE:D_SHA},'D256_kernel_dimension_all_primes':34,'Tomotope_kernel_dimension_odd_primes':3841,
         'positive_models':2,'negative_controls':{'wrong_sggi':control,'disconnected_complement':'detected'},
         'artifacts':{p.name:sha(p) for p in sorted(args.out.iterdir())},
         'scope':'Exact literal surface construction, components and orientation. Uniform homology and polytope theorem is written separately; no general conjecture or minimal-descendant enumeration is certified by this program.'}
 (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))

if __name__=='__main__':main()
