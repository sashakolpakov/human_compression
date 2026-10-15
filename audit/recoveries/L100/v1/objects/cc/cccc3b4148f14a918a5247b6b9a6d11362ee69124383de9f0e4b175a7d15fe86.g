# Complete rank-two search, conditional only on GAP's subgroup and action
# algorithms and its explicitly retained maximal-subgroup data.
# The caller supplies the ambient permutation group and the previously
# reviewed L096ProfileEquivalent function. No source geometry roster is read.
RankTwoCatalogue:=function(G)
 local maxima,locals,pairs,reps,classes,profiles,caches,A,H,B,hs,n,hom,P,
       i,j,r,t,a,u,common,digon,ip,over,p,pp,keys,AutG;
 maxima:=MaximalSubgroupClassReps(G);
 locals:=[];pairs:=[];
 for i in [1..Length(maxima)] do
  A:=maxima[i];hs:=MaximalSubgroupClassReps(A);
  for j in [1..Length(hs)] do
   H:=hs[j];n:=Index(A,H);
   hom:=ActionHomomorphism(A,RightTransversal(A,H),OnRight);P:=Image(hom);
   if n>1 and IsTransitive(Stabilizer(P,1),[2..n]) then
    Add(locals,rec(maximal_index:=i,local_index:=j,A:=GeneratorsOfGroup(A),
                  H:=GeneratorsOfGroup(H),degree:=n));
   fi;
  od;
 od;
 Print("MAXIMAL_CLASSES ",Length(maxima)," LOCAL_INPUTS ",Length(locals),"\n");
 for i in [1..Length(locals)] do
  r:=locals[i];A:=Subgroup(G,r.A);H:=Subgroup(G,r.H);
  over:=IntermediateSubgroups(G,H);
  for B in over.subgroups do
   if Intersection(A,B)=H then
    n:=Index(B,H);hom:=ActionHomomorphism(B,RightTransversal(B,H),OnRight);P:=Image(hom);
    if n>1 and IsTransitive(Stabilizer(P,1),[2..n]) then
     t:=RightTransversal(A,H);a:=First(t,x->not x in H);
     u:=RightTransversal(B,H);
     common:=Number(u,b->ForAny(u,c->b/(c*a) in A));
     digon:=Index(G,A)=n;ip:=common=1 or digon;
     if Group(Concatenation(GeneratorsOfGroup(A),GeneratorsOfGroup(B)))<>G then
      Error("Unexpected disconnected pair");
     fi;
     Add(pairs,rec(local_input:=i,A:=r.A,B:=GeneratorsOfGroup(B),H:=r.H,
                  orders:=[Size(A),Size(B),Size(H)],degrees:=[r.degree,n],
                  common:=common,digon:=digon,IP2:=ip));
     Print("PAIR ",Length(pairs)," ",i," ",Last(pairs).orders," ",Last(pairs).degrees,
           " COMMON ",common," IP2 ",ip,"\n");
    fi;
   fi;
  od;
 od;
 AutG:=AutomorphismGroup(G);reps:=[];classes:=[];profiles:=[];caches:=[];
 keys:=[[],[1],[2],[1,2]];
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
 Print("AUTOMORPHISM_ORDER ",Size(AutG)," CLASSES ",classes,"\n");
 return rec(group_order:=Size(G),automorphism_order:=Size(AutG),
            maximal_classes:=Length(maxima),locals:=locals,pairs:=pairs,classes:=classes);
end;;
