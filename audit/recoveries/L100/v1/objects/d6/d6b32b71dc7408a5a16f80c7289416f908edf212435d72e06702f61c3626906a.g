Read("/Users/sasha/medusa/research/leemans/topic_D_L096_HS_extension/archive_data/inputs.g");;
Read("/Users/sasha/medusa/research/leemans/reboot_20261013/L091_work/clean_run01/result.g");;
Read("/Users/sasha/medusa/research/leemans/reboot_20261013/L091_work/pair_witnesses.g");;
IndependentLocal:=function(K,H)
 local t,f,kernel,base,rest;
 t:=RightTransversal(K,H);f:=ActionHomomorphism(K,t,OnRight);base:=Position(t,One(K));
 if base=fail or Length(t)<2 then return false;fi;
 rest:=Difference([1..Length(t)],[base]);
 return Set(Orbit(Image(f,H),rest[1]))=rest;
end;;
IndependentIncidence:=function(G,A,B,H)
 local t,f,base,N,sets,a,i,j,counts,c;
 t:=RightTransversal(G,A);f:=ActionHomomorphism(G,t,OnRight);base:=Position(t,One(G));
 N:=Set(Orbit(Image(f,B),base));
 if Length(N)<>Index(B,H) then Error("Wrong B orbit degree");fi;
 sets:=List(RightTransversal(A,H),a->OnSets(N,Image(f,a)));
 # B-cosets may have identical neighbourhoods in the complete bipartite case.
 if Length(sets)<>Index(A,H) then Error("Wrong A degree");fi;
 counts:=[];
 for i in [1..Length(sets)] do
  for j in [i+1..Length(sets)] do
   c:=Length(Intersection(sets[i],sets[j]));Add(counts,c);
  od;
 od;
 if Length(Set(counts))<>1 then Error("Nonconstant common-neighbour count");fi;
 return rec(common:=counts[1],tested:=Length(counts),digon:=Length(N)=Length(t));
end;;
RunIndependent:=function()
 local G,r,A,B,H,x,i,total,classes,profiles,w,phi,p,q,target,damaged,all,front,elem,K,L,small,expected,actual;
 G:=Group(Concatenation(L096Inputs[1].parabolic_generators));
 if Size(G)<>44352000 or Length(HSRankTwoResult.pairs)<>13 then Error("Ambient/pair roster");fi;
 total:=0;
 for i in [1..Length(HSRankTwoResult.pairs)] do
  r:=HSRankTwoResult.pairs[i];A:=Subgroup(G,r.A);B:=Subgroup(G,r.B);H:=Intersection(A,B);
  if H<>Subgroup(G,r.H) or [Size(A),Size(B),Size(H)]<>r.orders then Error("Literal subgroups");fi;
  if not IndependentLocal(A,H) or not IndependentLocal(B,H) then Error("Literal H local orbits");fi;
  if Group(Concatenation(GeneratorsOfGroup(A),GeneratorsOfGroup(B)))<>G then Error("Connectivity");fi;
  x:=IndependentIncidence(G,A,B,H);total:=total+x.tested;
  if x.common<>r.common or x.digon<>r.digon or (x.common=1 or x.digon)<>r.IP2 then Error("Incidence record mismatch");fi;
  Print("PAIR_ALL_NEIGHBOURS ",i," ",x.tested," ",x.common,"\n");
 od;
 classes:=HSRankTwoResult.classes;
 if SortedList(Concatenation(classes))<>Filtered([1..13],i->HSRankTwoResult.pairs[i].IP2) then Error("Partition");fi;
 profiles:=List(classes,c->SortedList(HSRankTwoResult.pairs[c[1]].orders{[1,2]}));
 if Length(Set(profiles))<>6 then Error("Order separation");fi;
 for w in HSRankTwoWitnesses do
  phi:=GroupHomomorphismByImages(G,G,GeneratorsOfGroup(G),w.generator_images);
  if phi=fail or not IsBijective(phi) then Error("Witness not automorphism");fi;
  r:=HSRankTwoResult.pairs[w.source_pair];p:=[Subgroup(G,r.A),Subgroup(G,r.B)];
  r:=HSRankTwoResult.pairs[w.target_pair];q:=[Subgroup(G,r.A),Subgroup(G,r.B)];target:=Permuted(q,w.type_permutation);
  if List(p,K->Image(phi,K))<>target then Error("Two simultaneous images");fi;
 od;
 if Length(HSRankTwoWitnesses)<>4 then Error("Missing witness");fi;
 damaged:=GroupHomomorphismByImages(G,G,GeneratorsOfGroup(G),List(GeneratorsOfGroup(G),g->One(G)));
 if damaged<>fail and IsBijective(damaged) then Error("Trivial map accepted");fi;
 w:=HSRankTwoWitnesses[1];phi:=GroupHomomorphismByImages(G,G,GeneratorsOfGroup(G),w.generator_images);
 r:=HSRankTwoResult.pairs[w.source_pair];p:=[Subgroup(G,r.A),Subgroup(G,r.B)];r:=HSRankTwoResult.pairs[w.target_pair];q:=[Subgroup(G,r.A),Subgroup(G,r.B)];
 target:=Permuted(q,w.type_permutation*(1,2));
 if List(p,K->Image(phi,K))=target then Error("Wrong type permutation accepted");fi;
 # Complete small group subgroup family by closure under every element, no lattice routine.
 small:=SymmetricGroup(4);all:=[TrivialSubgroup(small)];front:=1;
 while front<=Length(all) do
  K:=all[front];
  for elem in Elements(small) do
   L:=ClosureGroup(K,elem);if not L in all then Add(all,L);fi;
  od;front:=front+1;
 od;
 if Length(all)<>30 then Error("Exhaustive S4 closure control");fi;
 total:=rec(neighbour_pairs:=total,subgroups:=Length(all));
 for H in all do
  expected:=Filtered(all,K->H<>K and K<>small and IsSubset(K,H));actual:=IntermediateSubgroups(small,H).subgroups;
  if Set(expected)<>Set(actual) or Length(actual)<>Length(Set(actual)) then Error("Actual-overgroup completeness");fi;
 od;
 G:=Group((1,2,3),(1,2),(4,5));A:=Group((1,2,3),(1,2));B:=Group((1,2),(4,5));H:=Intersection(A,B);
 if not IndependentLocal(A,H) or not IndependentLocal(B,H) then Error("Digon locals");fi;
 x:=IndependentIncidence(G,A,B,H);if x.common<>2 or not x.digon then Error("Complete-bipartite alternative");fi;
 G:=SymmetricGroup(3);A:=Group((1,2));B:=Group((2,3));H:=Intersection(A,B);x:=IndependentIncidence(G,A,B,H);
 if x.common<>1 or x.digon then Error("Partial linear control");fi;
 G:=SymmetricGroup(4);A:=Stabilizer(G,1);B:=Stabilizer(G,2);H:=Intersection(A,B);x:=IndependentIncidence(G,A,B,H);
 if x.common<>2 or x.digon then Error("Genuine quadrangle control");fi;
 if IndependentLocal(A,A) then Error("Degree-one local action accepted");fi;
 Print("PASS_INDEPENDENT_RANK_TWO ",total.neighbour_pairs," 13 4 ",total.subgroups," 3 3\n");
end;;
RunIndependent();
QUIT;
