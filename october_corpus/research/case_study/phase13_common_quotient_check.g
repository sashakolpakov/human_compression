# Exact diagnostics for the all-rank class<=3 common-quotient proof.
# Dependencies: GAP and NQ. No group catalogue or earlier computation imported.
if LoadPackage("nq")=fail then Error("NQ package required");fi;
SizeScreen([240,24]);;

UniversalPathThree:=function(d)
 local F,r,rels,i,j,P;
 F:=FreeGroup(d);r:=GeneratorsOfGroup(F);rels:=List(r,x->x^2);
 for i in [1..d] do
  for j in [i+1..d] do
   if j>i+1 then Add(rels,Comm(r[i],r[j]));fi;
  od;
 od;
 P:=NilpotentQuotient(F/rels,3);
 return rec(group:=P,r:=GeneratorsOfGroup(P){[1..d]});
end;

CheckIP:=function(G,r)
 local subsets,groups,i,j,k,valid;
 subsets:=Combinations([1..Length(r)]);
 groups:=List(subsets,I->Subgroup(G,r{I}));
 valid:=true;
 for i in [1..Length(groups)] do
  for j in [1..Length(groups)] do
   k:=Position(subsets,Intersection(subsets[i],subsets[j]));
   if Intersection(groups[i],groups[j])<>groups[k] then valid:=false;fi;
  od;
 od;
 return valid;
end;

CheckCollection:=function(d)
 local u,G,r,c,z,t,D,K,i,j,expected,count;
 u:=UniversalPathThree(d);G:=u.group;r:=u.r;
 c:=List([1..d-1],i->Comm(r[i],r[i+1]));
 z:=List(c,x->x^2);
 t:=List([1..d-2],i->Comm(c[i],r[i+2]));
 D:=DerivedSubgroup(G);K:=CommutatorSubgroup(D,G);
 if NilpotencyClassOfGroup(G)<>3 then Error("Class");fi;
 if not IsAbelian(D) or not IsElementaryAbelian(K) then Error("Derived layers");fi;
 if Group(Concatenation(z,t))<>K then Error("Gamma3 generators");fi;
 if not ForAll(Concatenation(z,t),x->Order(x)<=2) then Error("Exponent");fi;
 if not ForAll(Concatenation(z,t),x->ForAll(r,y->Comm(x,y)=One(G))) then Error("Centrality");fi;
 count:=0;
 for i in [1..d-1] do
  if c[i]<>(r[i]*r[i+1])^2 then Error("Commutator convention");fi;
  for j in [1..d] do
   expected:=One(G);
   if j=i-1 then expected:=t[i-1];fi;
   if j=i or j=i+1 then expected:=z[i];fi;
   if j=i+2 then expected:=t[i];fi;
   if Comm(c[i],r[j])<>expected then Error("Collection formula");fi;
   count:=count+1;
  od;
 od;
 if Size(G)/Size(K)<>2^(2*d-1) then Error("Universal class2 order");fi;
 Print("collection rank=",d," order=",Size(G)," gamma3=",Size(K)," comparisons=",count," PASS\n");
 return count;
end;

CheckAllRankThreeQuotients:=function()
 local u,iso,G,r,D,K,normals,N,hom,H,s,tested,nondeg,bad,good,validBad,type;
 u:=UniversalPathThree(3);iso:=IsomorphismPermGroup(u.group);G:=Image(iso);
 r:=List(u.r,x->Image(iso,x));D:=DerivedSubgroup(G);K:=CommutatorSubgroup(D,G);
 normals:=NormalSubgroups(G);
 tested:=0;nondeg:=0;bad:=0;good:=0;validBad:=0;
 for N in normals do
  if not IsSubgroup(D,N) then continue;fi;
  tested:=tested+1;
  hom:=NaturalHomomorphismByNormalSubgroup(G,N);H:=Image(hom);
  s:=List(r,x->Image(hom,x));type:=List([1..2],i->Order(s[i]*s[i+1]));
  if Minimum(type)<4 then continue;fi;
  nondeg:=nondeg+1;
  if not IsSubgroup(K,N) then bad:=bad+1;fi;
  if CheckIP(H,s) then
   good:=good+1;
   if not IsSubgroup(K,N) then validBad:=validBad+1;fi;
   if Size(H)/Size(CommutatorSubgroup(DerivedSubgroup(H),H))<>32 then Error("Counterexample found");fi;
  fi;
 od;
 if Length(normals)<>53 or tested<>26 or nondeg<>21 or bad<>5 or validBad<>0 then Error("Probe counts changed");fi;
 Print("quotient census universal_order=",Size(G)," all_normal_subgroups=",Length(normals)," derived_kernels=",tested," nondegenerate=",nondeg," smaller_class2=",bad," IP_valid=",good," smaller_class2_and_IP=",validBad," PASS\n");
 return good;
end;

Print("GAP=",GAPInfo.Version," NQ=",PackageInfo("nq")[1].Version,"\n");
comparisons:=Sum(List([2..6],CheckCollection));;
good:=CheckAllRankThreeQuotients();;
Print("total_collection_comparisons=",comparisons,"; valid_rank3_quotient_markings=",good,"\n");
Print("PASS: focused universal collection and complete rank3/class<=3 quotient diagnostic; all-rank proof is separate.\n");
QUIT;
