#!/usr/bin/env python3
"""Independent finite diagnostics for the written/Lean residual-generation map.

No author model or compiler code is imported. These checks are not uniform proofs.
"""
import argparse,itertools,json
from pathlib import Path
def need(x,m):
 if not x:raise ValueError(m)
def powerset(items):
 items=list(items)
 return [frozenset(c) for r in range(len(items)+1) for c in itertools.combinations(items,r)]
def closure(seed,mul,one):
 out={one};todo=[one];generators=set(seed)
 for x in todo:
  for y in generators:
   z=mul(x,y)
   if z not in out:out.add(z);todo.append(z)
 return frozenset(out)
def inspect_family(G,mul,one,subgroups,Ps,choices):
 I=frozenset(range(len(Ps)))
 def fixed(S):return frozenset(x for x in G if all(x in Ps[i] for i in I-S))
 def maximal(A,B):return A<B and not any(A<K<B for K in subgroups)
 subsets=powerset(I)
 hmem=all(choices[i] in Ps[j] for i in I for j in I if i!=j)
 hout=all(choices[i] not in Ps[i] for i in I)
 hmax=all(any(maximal(fixed(S-{i}),fixed(S)) for i in S) for S in subsets if S)
 if not(hmem and hout and hmax):return None
 borel=fixed(frozenset());generated={S:closure(borel|{choices[i] for i in S},mul,one) for S in subsets}
 need(all(generated[S]==fixed(S) for S in subsets),'actual complement-indexed generation')
 need(all(generated[S]&generated[T]==generated[S&T] for S in subsets for T in subsets),'actual generated intersections')
 need(all(choices[i] not in generated[I-{i}] for i in I),'relative irredundancy')
 need(generated[I]==G,'whole group generated')
 return {'rank':len(I),'borel_order':len(borel),'subsets_checked':len(subsets),'pairs_checked':len(subsets)**2}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh output')
 perms=list(itertools.permutations(range(3)));ix={p:i for i,p in enumerate(perms)};G=frozenset(range(6));one=ix[(0,1,2)]
 mul=lambda a,b:ix[tuple(perms[a][perms[b][i]] for i in range(3))]
 subgroups=[H for H in powerset(G) if one in H and all(mul(a,b) in H for a in H for b in H)]
 need(len(subgroups)==6,'six literal S3 subgroups')
 counts={};checks=0
 for rank in range(1,4):
  count=0
  for Ps in itertools.product(subgroups,repeat=rank):
   candidates=[list(set.intersection(set(G),*(set(Ps[j]) for j in range(rank) if j!=i))-set(Ps[i])) for i in range(rank)]
   for chosen in itertools.product(*candidates):
    result=inspect_family(G,mul,one,subgroups,Ps,chosen)
    if result:count+=1;checks+=result['pairs_checked']
  counts[str(rank)]=count
 # An odd-prime example with a nontrivial Borel; not an XOR model.
 triples=list(itertools.product(range(3),range(3),range(2)));lookup={x:i for i,x in enumerate(triples)};G18=frozenset(range(18));identity=lookup[(0,0,0)]
 plus=lambda a,b:lookup[((triples[a][0]+triples[b][0])%3,(triples[a][1]+triples[b][1])%3,(triples[a][2]+triples[b][2])%2)]
 # Generate the full subgroup lattice by adjoining each actual group element.
 lattice={frozenset({identity})};pending=list(lattice)
 for H in pending:
  for x in G18:
   K=closure(H|{x},plus,identity)
   if K not in lattice:lattice.add(K);pending.append(K)
 Ps=[frozenset(i for i,x in enumerate(triples) if x[j]==0) for j in range(2)]
 c=[lookup[(1,0,1)],lookup[(0,1,0)]]
 positive=inspect_family(G18,plus,identity,lattice,Ps,c)
 need(positive and positive['borel_order']==2,'nontrivial Borel and odd-prime coordinate model')
 # The same literal choices with the type labels swapped do not satisfy the
 # geometric membership interface. An arbitrary list of generators is not it.
 bad=list(reversed(c));rejected=inspect_family(G18,plus,identity,lattice,Ps,bad) is None
 need(rejected,'wrong type-to-choice bridge rejected')
 report={'status':'PASS_INDEPENDENT_FINITE_INTERFACES','S3_all_subgroup_families_ranks_1_2_3':counts,
  'S3_generated_intersection_pairs':checks,'odd_prime_nontrivial_Borel':positive,
  'C3_squared_times_C2_subgroups':len(lattice),'swapped_type_choice_control_rejected':rejected,
  'author_code_imported':False,'uniform_proof':False}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
