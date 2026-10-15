# All RWPRI rank-two coset geometries; local double transitivity is an output.
# Complete maximal-subgroup and actual intermediate-subgroup interfaces are retained.
PrimitiveRankTwoCatalogue:=function(G)
 local maxima,locals,pairs,reps,classes,profiles,caches,A,H,B,hs,n,hom,P,
       i,j,r,t,u,commons,digon,ip,over,p,pp,keys,AutG,twoA,twoB;
 maxima:=MaximalSubgroupClassReps(G);locals:=[];pairs:=[];
 for i in [1..Length(maxima)] do
  A:=maxima[i];hs:=MaximalSubgroupClassReps(A);
  for j in [1..Length(hs)] do
   H:=hs[j];n:=Index(A,H);
   hom:=ActionHomomorphism(A,RightTransversal(A,H),OnRight);P:=Image(hom);
   if n<2 or not IsPrimitive(P,[1..n]) then Error("Incomplete maximal interface");fi;
   twoA:=IsTransitive(Stabilizer(P,1),[2..n]);
   Add(locals,rec(maximal_index:=i,local_index:=j,A:=GeneratorsOfGroup(A),
                 H:=GeneratorsOfGroup(H),degree:=n,twoA:=twoA));
  od;
 od;
 Print("MAXIMAL_CLASSES ",Length(maxima)," LOCAL_INPUTS ",Length(locals),"\n");
 for i in [1..Length(locals)] do
  r:=locals[i];A:=Subgroup(G,r.A);H:=Subgroup(G,r.H);over:=IntermediateSubgroups(G,H);
  for B in over.subgroups do
   if Intersection(A,B)=H then
    n:=Index(B,H);hom:=ActionHomomorphism(B,RightTransversal(B,H),OnRight);P:=Image(hom);
    if n>1 and IsPrimitive(P,[1..n]) then
     twoB:=IsTransitive(Stabilizer(P,1),[2..n]);
     t:=Filtered(RightTransversal(A,H),x->not x in H);u:=RightTransversal(B,H);
     commons:=List(t,a->Number(u,b->ForAny(u,c->b/(c*a) in A)));
     digon:=Index(G,A)=n;ip:=ForAll(commons,x->x=1)or digon;
     if Group(Concatenation(GeneratorsOfGroup(A),GeneratorsOfGroup(B)))<>G then Error("Disconnected pair");fi;
     Add(pairs,rec(local_input:=i,A:=r.A,B:=GeneratorsOfGroup(B),H:=r.H,
         orders:=[Size(A),Size(B),Size(H)],degrees:=[r.degree,n],
         common_counts:=commons,digon:=digon,IP2:=ip,local_two_transitive:=[r.twoA,twoB]));
     Print("PAIR ",Length(pairs)," ",Last(pairs).orders," ",Last(pairs).degrees,
           " COMMONS ",Set(commons)," IP2 ",ip," 2T ",[r.twoA,twoB],"\n");
    fi;
   fi;
  od;
 od;
 AutG:=AutomorphismGroup(G);reps:=[];classes:=[];profiles:=[];caches:=[];keys:=[[],[1],[2],[1,2]];
 for i in [1..Length(pairs)] do
  r:=pairs[i];
  if r.IP2 then
   p:=[Subgroup(G,r.A),Subgroup(G,r.B)];
   pp:=rec(keys:=keys,orders:=[Size(G),Size(p[1]),Size(p[2]),Size(Intersection(p))]);
   j:=PositionProperty([1..Length(reps)],j->L096ProfileEquivalent(AutG,p,pp,reps[j],profiles[j],caches[j]));
   if j=fail then Add(reps,p);Add(classes,[]);Add(profiles,pp);Add(caches,rec());j:=Length(reps);fi;
   Add(classes[j],i);
  fi;
 od;
 Print("CLASSES ",classes,"\n");
 return rec(group_order:=Size(G),group_generators:=GeneratorsOfGroup(G),maximal_classes:=Length(maxima),
            locals:=locals,pairs:=pairs,classes:=classes);
end;;
