# Exact bounded checks of every proposed noncentral excess-two family.
# Not an exhaustive search outside the proved candidate lists.
if LoadPackage("nq")=fail then Error("NQ required");fi;
SizeScreen([100000,24]);;
K2FamilyCheck19:=function(d,kind,edge,triple,betaBits)
 local F,f,r,u,z,rel,i,j,c,alpha,beta,Q,epi,iso,G,kg,K,Z,L,
 sets,pars,S,want,meets;
 F:=FreeGroup(d+2);f:=GeneratorsOfGroup(F);r:=f{[1..d]};u:=f[d+1];z:=f[d+2];
 rel:=List(r,x->x^2);Add(rel,z^2);
 for i in [1..d] do for j in [i+1..d] do
  if j-i>1 then Add(rel,Comm(r[i],r[j]));fi;
 od;od;
 for c in f do Add(rel,Comm(z,c));od;
 alpha:=List([1..d-1],i->One(F));beta:=List([1..d-2],i->One(F));
 if kind="C4" then
  Add(rel,u^2*z);alpha[edge]:=u;
  for i in [1..d] do
   if i=edge or i=edge+1 then Add(rel,u^r[i]*u);else Add(rel,Comm(u,r[i]));fi;
  od;
 else
  Add(rel,u^2);beta[triple]:=u;
  if edge<>0 then alpha[edge]:=z;fi;
  for i in [1..d] do
   if i=triple+1 then Add(rel,Comm(u,r[i])*z);else Add(rel,Comm(u,r[i]));fi;
  od;
 fi;
 for i in betaBits do beta[i]:=z;od;
 for i in [1..d-1] do
  c:=Comm(r[i],r[i+1]);Add(rel,c^2*alpha[i]^-1);
  if i<=d-2 then Add(rel,Comm(c,r[i+2])*beta[i]^-1);fi;
 od;
 Q:=F/rel;epi:=NqEpimorphismNilpotentQuotient(Q,4);G:=Image(epi);
 kg:=List(GeneratorsOfGroup(Q){[d+1,d+2]},x->Image(epi,x));
 r:=List(GeneratorsOfGroup(Q){[1..d]},x->Image(epi,x));
 iso:=IsomorphismPcGroup(G);r:=List(r,x->Image(iso,x));kg:=List(kg,x->Image(iso,x));G:=Image(iso);
 if Size(G)<>2^(2*d+1) or Subgroup(G,r)<>G then Error("Order/generation");fi;
 K:=CommutatorSubgroup(DerivedSubgroup(G),G);Z:=Subgroup(G,[kg[2]]);
 L:=CommutatorSubgroup(K,G);
 if K<>Subgroup(G,kg) or Size(K)<>4 or L<>Z or Size(Z)<>2 then Error("Lower central series");fi;
 if not IsSubgroup(Centre(G),Z) then Error("gamma4 central");fi;
 if (kind="C4")<>IsCyclic(K) then Error("Kernel type");fi;
 sets:=Combinations([1..d]);pars:=List(sets,S->Subgroup(G,r{S}));
 for i in [1..Length(sets)] do
  S:=sets[i];want:=TrivialSubgroup(G);
  if kind="C4" then
   if IsSubset(S,[edge,edge+1]) then want:=K;fi;
  else
   if IsSubset(S,[triple..triple+2]) then want:=K;
   elif edge<>0 and IsSubset(S,[edge,edge+1]) then want:=Z;fi;
  fi;
  if Intersection(K,pars[i])<>want then Error("Exact parabolic kernel");fi;
  if Size(pars[i])<>Size(want)*2^(Length(S)+Number([1..d-1],j->j in S and j+1 in S)) then Error("Parabolic order");fi;
 od;
 meets:=0;
 for i in [1..Length(sets)] do for j in [1..Length(sets)] do
  if Intersection(pars[i],pars[j])<>pars[Position(sets,Intersection(sets[i],sets[j]))] then Error("Actual IP");fi;
  meets:=meets+1;
 od;od;
 return [Length(sets),meets];
end;;
Print("GAP=",GAPInfo.Version," NQ=",PackageInfo("nq")[1].Version,"\n");;
tot19:=[0,0,0];;
for d19 in [3..5] do
 cntC19:=0;cntV19:=0;checks19:=[0,0];;
 for e19 in [1..d19-1] do
  candidates19:=Filtered([e19-1,e19],i->i>=1 and i<=d19-2);
  for bits19 in Combinations(candidates19) do
   checks19:=checks19+K2FamilyCheck19(d19,"C4",e19,0,bits19);cntC19:=cntC19+1;
  od;
 od;
 for t19 in [1..d19-2] do
  checks19:=checks19+K2FamilyCheck19(d19,"V4",0,t19,[]);cntV19:=cntV19+1;
  for e19 in [t19,t19+1] do
   candidates19:=Filtered([e19-1,e19],i->i>=1 and i<=d19-2 and i<>t19);
   for bits19 in Combinations(candidates19) do
    checks19:=checks19+K2FamilyCheck19(d19,"V4",e19,t19,bits19);cntV19:=cntV19+1;
   od;
  od;
 od;
 if cntC19<>4*d19-8 or cntV19<>5*d19-12 then Error("Family count");fi;
 Print("PASS rank=",d19," C4=",cntC19," V4=",cntV19," kernels_and_orders=",checks19[1]," actual_IP_meets=",checks19[2],"\n");
 tot19:=tot19+[cntC19+cntV19,checks19[1],checks19[2]];
od;
Print("PASS totals_groups_parabolics_meets=",tot19,"; candidate diagnostics, not an independent exhaustion.\n");
QUIT;
