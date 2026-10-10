# Exact bounded presentation diagnostics. Uniform classification is a separate
# written proof. No group catalogue is used. Requires GAP and NQ.
if LoadPackage("nq")=fail then Error("NQ required");fi;
SizeScreen([100000,24]);;
CheckK1Rank:=function(d)
 local masks,bits,mask,alpha,beta,F,f,z,rel,i,j,c,exp,G,r,zz,iso,
 sets,groups,K,seeds,pred,actual,least,A,B,meets,good,bad,
 supports,suborder,failmeet,firstbad,classes,Q,epi,qgens;
 masks:=2^(2*d-3)-1;good:=0;bad:=0;meets:=0;firstbad:=fail;
 for mask in [1..masks] do
  bits:=List([0..2*d-4],i->QuoInt(mask,2^i) mod 2);
  alpha:=bits{[1..d-1]};beta:=bits{[d..2*d-3]};
  F:=FreeGroup(d+1);f:=GeneratorsOfGroup(F);z:=f[d+1];
  rel:=List(f,x->x^2);
  for i in [1..d] do Add(rel,Comm(z,f[i]));
   for j in [i+1..d] do if j-i>1 then Add(rel,Comm(f[i],f[j]));fi;od;
  od;
  for i in [1..d-1] do
   c:=Comm(f[i],f[i+1]);Add(rel,c^2*z^alpha[i]);
   for j in [1..d] do
    exp:=0;
    if j=i or j=i+1 then exp:=alpha[i];
    elif j=i-1 then exp:=beta[i-1];
    elif j=i+2 then exp:=beta[i];fi;
    Add(rel,Comm(c,f[j])*z^exp);
   od;
  od;
  Q:=F/rel;epi:=NqEpimorphismNilpotentQuotient(Q,3);G:=Image(epi);
  qgens:=GeneratorsOfGroup(Q);r:=List(qgens{[1..d]},x->Image(epi,x));
  zz:=Image(epi,qgens[d+1]);
  iso:=IsomorphismPcGroup(G);r:=List(r,x->Image(iso,x));zz:=Image(iso,zz);G:=Image(iso);
  if Size(G)<>2^(2*d) or Subgroup(G,r)<>G then Error("Order/generation");fi;
  K:=CommutatorSubgroup(DerivedSubgroup(G),G);
  if K<>Subgroup(G,[zz]) or Size(K)<>2 then Error("Central gamma3");fi;
  if not IsSubgroup(Centre(G),K) then Error("Centrality");fi;
  seeds:=Concatenation(List(Filtered([1..d-1],i->alpha[i]=1),i->[i,i+1]),
    List(Filtered([1..d-2],i->beta[i]=1),i->[i,i+1,i+2]));
  least:=Filtered(seeds,A->ForAll(seeds,B->IsSubset(B,A)));
  pred:=Length(least)=1;
  sets:=Combinations([1..d]);groups:=List(sets,A->Subgroup(G,r{A}));
  for i in [1..Length(sets)] do
   A:=sets[i];exp:=Length(A)+Number([1..d-1],j->j in A and j+1 in A);
   if ForAny(seeds,B->IsSubset(A,B)) then exp:=exp+1;fi;
   if Size(groups[i])<>2^exp then Error("Parabolic order formula");fi;
   if IsSubgroup(groups[i],K)<>ForAny(seeds,B->IsSubset(A,B)) then Error("Kernel support criterion");fi;
  od;
  actual:=true;failmeet:=fail;
  for i in [1..Length(sets)] do for j in [1..Length(sets)] do
   if Intersection(groups[i],groups[j])<>groups[Position(sets,Intersection(sets[i],sets[j]))] then
    actual:=false;
    if failmeet=fail then failmeet:=[sets[i],sets[j],Size(Intersection(groups[i],groups[j])),
      Size(groups[Position(sets,Intersection(sets[i],sets[j]))])];fi;
   fi;
   meets:=meets+1;
  od;od;
  if actual<>pred then Error("IP classification");fi;
  if actual then good:=good+1;else bad:=bad+1;
   if firstbad=fail then firstbad:=[alpha,beta,failmeet];fi;
  fi;
 od;
 if good<>5*d-10 then Error("Census formula");fi;
 Print("PASS rank=",d," parameter_vectors=",masks," IP=",good," non_IP=",bad,
  " exact_parabolic_orders=",masks*2^d," exact_IP_meets=",meets,
  " first_non_IP_alpha_beta_supports_meetorders=",firstbad,"\n");
 return [masks,good,bad,meets];
end;;
Print("GAP=",GAPInfo.Version," NQ=",PackageInfo("nq")[1].Version,"\n");;
totals:=[0,0,0,0];;
for d17 in [3..5] do totals:=totals+CheckK1Rank(d17);od;
Print("PASS totals_vectors_IP_nonIP_meets=",totals,"; bounded diagnostics only.\n");
QUIT;
