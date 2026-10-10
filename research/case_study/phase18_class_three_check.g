# Independent group-level bounded diagnostics for the class-three formula.
# Enumerates all rank-two parameter quotients at d=3,4, and every predicted
# IP rank-two quotient at d=5. No group catalogue is used.
if LoadPackage("nq")=fail then Error("NQ required");fi;
SizeScreen([100000,24]);;
Xor18:=function(a,b)return (a mod 2+b mod 2) mod 2 + 2*((QuoInt(a,2)+QuoInt(b,2)) mod 2);end;;
Span18:=function(labels)
 local vals,x;vals:=[0];
 for x in labels do vals:=Union(vals,List(vals,y->Xor18(x,y)));od;
 return vals;
end;;
CheckClassThree18:=function(d)
 local labels,all,alpha,beta,cost,F,f,z,word,rel,i,j,c,value,Q,epi,G,
 qgens,r,zz,iso,K,sets,groups,S,active,dim,actual,pred,meets,
 tested,good,bad,skipped,paraboliccount;
 tested:=0;good:=0;bad:=0;skipped:=0;meets:=0;paraboliccount:=0;
 all:=Filtered(Tuples([0..3],2*d-3),L->First(L,x->x<>0)=1 and First(L,x->x>1)=2);
 for labels in all do
  alpha:=labels{[1..d-1]};beta:=labels{[d..2*d-3]};
  cost:=Number(alpha,x->x<>0)+Number([1..d-2],i->not beta[i] in Span18(alpha{[i,i+1]}));
  pred:=cost=2;
  if d=5 and not pred then skipped:=skipped+1;continue;fi;
  tested:=tested+1;
  F:=FreeGroup(d+2);f:=GeneratorsOfGroup(F);z:=f{[d+1,d+2]};
  word:=v->z[1]^(v mod 2)*z[2]^QuoInt(v,2);
  rel:=List(f,x->x^2);
  for i in [1..d+2] do for j in [d+1,d+2] do Add(rel,Comm(f[i],f[j]));od;od;
  for i in [1..d] do for j in [i+1..d] do if j-i>1 then Add(rel,Comm(f[i],f[j]));fi;od;od;
  for i in [1..d-1] do
   c:=Comm(f[i],f[i+1]);Add(rel,c^2*word(alpha[i]));
   for j in [1..d] do
    value:=0;
    if j=i or j=i+1 then value:=alpha[i];
    elif j=i-1 then value:=beta[i-1];elif j=i+2 then value:=beta[i];fi;
    Add(rel,Comm(c,f[j])*word(value));
   od;
  od;
  Q:=F/rel;epi:=NqEpimorphismNilpotentQuotient(Q,3);G:=Image(epi);qgens:=GeneratorsOfGroup(Q);
  r:=List(qgens{[1..d]},x->Image(epi,x));zz:=List(qgens{[d+1,d+2]},x->Image(epi,x));
  iso:=IsomorphismPcGroup(G);r:=List(r,x->Image(iso,x));zz:=List(zz,x->Image(iso,x));G:=Image(iso);
  if Size(G)<>2^(2*d+1) or Subgroup(G,r)<>G then Error("Order/generation");fi;
  K:=CommutatorSubgroup(DerivedSubgroup(G),G);
  if K<>Subgroup(G,zz) or Size(K)<>4 or not IsSubgroup(Centre(G),K) then Error("Central elementary gamma3");fi;
  sets:=Combinations([1..d]);groups:=List(sets,S->Subgroup(G,r{S}));
  for i in [1..Length(sets)] do
   S:=sets[i];active:=[];
   for j in [1..d-1] do if j in S and j+1 in S then Add(active,alpha[j]);fi;od;
   for j in [1..d-2] do if IsSubset(S,[j..j+2]) then Add(active,beta[j]);fi;od;
   dim:=LogInt(Length(Span18(active)),2);
   if Size(groups[i])<>2^(Length(S)+Number([1..d-1],j->j in S and j+1 in S)+dim) then Error("Parabolic order");fi;
   if Size(Intersection(K,groups[i]))<>2^dim then Error("Parabolic kernel");fi;
   paraboliccount:=paraboliccount+1;
  od;
  actual:=true;
  for i in [1..Length(sets)] do for j in [1..Length(sets)] do
   if Intersection(groups[i],groups[j])<>groups[Position(sets,Intersection(sets[i],sets[j]))] then actual:=false;fi;
   meets:=meets+1;
  od;od;
  if actual<>pred then Error("Class-three IP criterion");fi;
  if actual then good:=good+1;else bad:=bad+1;fi;
 od;
 if good<>(25*d^2-125*d+162)/2 then Error("Count");fi;
 Print("PASS rank=",d," linear_quotients=",Length(all)," actual_groups_tested=",tested,
  " predicted_bad_skipped=",skipped," IP=",good," non_IP=",bad,
  " exact_parabolic_orders=",paraboliccount," exact_group_meets=",meets,"\n");
 return [tested,good,bad,paraboliccount,meets];
end;;
Print("GAP=",GAPInfo.Version," NQ=",PackageInfo("nq")[1].Version,"\n");;
totals18:=[0,0,0,0,0];;
for d18 in [3..5] do totals18:=totals18+CheckClassThree18(d18);od;
Print("PASS totals_groups_IP_nonIP_parabolics_meets=",totals18,"; bounded diagnostics only.\n");
QUIT;
