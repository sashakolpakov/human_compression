Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/result.g");;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/pair_witnesses.g");;
RunOracle:=function()
 local G,cache,i,r,A,B,H,k,rt,f,base,N,sets,counts,actual,a,j,c,total,w,phi,p,q,target,cls,expected,maps,loc,hom,P,alltwo;
 G:=Group(PSL34RankTwo.group_generators);cache:=[];total:=0;
 for i in [1..Length(PSL34RankTwo.pairs)] do
  r:=PSL34RankTwo.pairs[i];A:=Subgroup(G,r.A);B:=Subgroup(G,r.B);H:=Subgroup(G,r.H);
  if Intersection(A,B)<>H or [Size(A),Size(B),Size(H)]<>r.orders then Error("Actual groups mismatch");fi;
  for j in [1,2] do
   loc:=[A,B][j];rt:=RightTransversal(loc,H);hom:=ActionHomomorphism(loc,rt,OnRight);P:=Image(hom);
   base:=Position(rt,One(G));
   if not IsPrimitive(P,[1..Length(rt)]) then Error("Local not primitive");fi;
   if IsTransitive(Image(hom,H),Difference([1..Length(rt)],[base]))<>r.local_two_transitive[j] then Error("Local 2T flag");fi;
  od;
  k:=PositionProperty(cache,x->x.A=A);
  if k=fail then
   rt:=RightTransversal(G,A);f:=ActionHomomorphism(G,rt,OnRight);base:=Position(rt,One(G));
   Add(cache,rec(A:=A,f:=f,base:=base));k:=Length(cache);
  fi;
  f:=cache[k].f;base:=cache[k].base;N:=Set(Orbit(Image(f,B),base));
  if Length(N)<>r.degrees[2] then Error("Neighbour orbit degree");fi;
  rt:=RightTransversal(A,H);sets:=List(rt,a->OnSets(N,Image(f,a)));
  actual:=List(Filtered([1..Length(rt)],j->not rt[j]in H),j->Length(Intersection(N,sets[j])));
  if SortedList(actual)<>SortedList(r.common_counts) then Print("MISMATCH ",i," ",actual," ",r.common_counts,"\n");Error("Common neighbour multiset");fi;
  counts:=[];
  for j in [1..Length(sets)] do for k in [j+1..Length(sets)] do Add(counts,Length(Intersection(sets[j],sets[k])));od;od;
  total:=total+Length(counts);
  if (ForAll(counts,x->x=1)or Length(N)=Index(G,A))<>r.IP2 then Error("All pairs incidence");fi;
 od;
 cls:=PSL34RankTwo.classes;
 if SortedList(Concatenation(cls))<>Filtered([1..Length(PSL34RankTwo.pairs)],i->PSL34RankTwo.pairs[i].IP2) then Error("Survivor partition");fi;
 if Length(Set(List(cls,c->SortedList(PSL34RankTwo.pairs[c[1]].orders{[1,2]}))))<>7 then Error("Distinct typesizes");fi;
 expected:=SortedList(Concatenation(List(cls,c->c{[2..Length(c)]})));
 if SortedList(List(PSL34Witnesses,w->w.source_pair))<>expected then Error("Witness coverage");fi;
 for w in PSL34Witnesses do
  phi:=GroupHomomorphismByImages(G,G,GeneratorsOfGroup(G),w.generator_images);
  if phi=fail or not IsBijective(phi) then Error("Not an automorphism");fi;
  r:=PSL34RankTwo.pairs[w.source_pair];p:=List([r.A,r.B],x->Subgroup(G,x));
  r:=PSL34RankTwo.pairs[w.target_pair];q:=List([r.A,r.B],x->Subgroup(G,x));target:=Permuted(q,w.type_permutation);
  if List(p,H->Image(phi,H))<>target then Error("Simultaneous images");fi;
 od;
 Print("PASS_COSET_ORACLE ",Length(PSL34RankTwo.pairs)," PAIRS ",total," NEIGHBOUR_PAIRS ",Length(PSL34Witnesses)," WITNESSES\n");
end;;
PSL34RankTwo.pairs[1].orders[1]:=1;
RunOracle();
QUIT;
