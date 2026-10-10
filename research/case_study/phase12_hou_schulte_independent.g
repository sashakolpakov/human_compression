# Independent exact witness for arXiv:2605.20691v1, Theorem 4.2(c-e).
# Build the class-two nilpotent quotient of a presentation, independently
# of any explicit vector/cocycle implementation. Dependencies: GAP, NQ.
# Run: gap -q phase12_hou_schulte_independent.g

if LoadPackage("nq")=fail then Error("NQ package required"); fi;
F:=FreeGroup("r0","r1","r2","r3");;
ff:=GeneratorsOfGroup(F);;
rels:=List(ff,x->x^2);;
for i in [1..4] do
 for j in [i+1..4] do
  if j>i+1 then Add(rels,Comm(ff[i],ff[j]));fi;
 od;
od;
pcG:=NilpotentQuotient(F/rels,2);;
toPerm:=IsomorphismPermGroup(pcG);;
G:=Image(toPerm);;
rho:=List(GeneratorsOfGroup(pcG){[1..4]},r->Image(toPerm,r));;
if Size(G)<>128 or NilpotencyClassOfGroup(G)<>2 then
 Error("Unexpected presentation quotient");
fi;
if not ForAll(rho,r->Order(r)=2) then Error("Involution failure");fi;
if Size(Group(rho))<>128 then Error("Generation failure");fi;
for i in [1..4] do
 for j in [i+1..4] do
  if j>i+1 and Order(rho[i]*rho[j])<>2 then Error("String failure");fi;
 od;
od;
adj:=List([1..3],i->Order(rho[i]*rho[i+1]));;
if adj<>[4,4,4] then Error("Type failure");fi;
subsets:=Combinations([1..4]);;
groups:=List(subsets,I->Subgroup(G,rho{I}));;
count:=0;;
for i in [1..Length(subsets)] do
 for j in [1..Length(subsets)] do
  k:=Position(subsets,Intersection(subsets[i],subsets[j]));;
  if Intersection(groups[i],groups[j])<>groups[k] then Error("IP failure");fi;
  count:=count+1;;
 od;
od;
sigma:=List([1..3],i->rho[i]*rho[i+1]);;
A:=Subgroup(G,sigma);;
Ai:=[];;
for i in [1..3] do
 gs:=ShallowCopy(sigma);;gs[i]:=gs[i]^2;;
 Add(Ai,Subgroup(G,gs));;
od;
phis:=List(Ai,FrattiniSubgroup);;
C:=Intersection(phis);;
gamma3:=CommutatorSubgroup(DerivedSubgroup(G),G);;
cs:=List(sigma,s->s^2);;
expected:=[Subgroup(G,cs{[2,3]}),Subgroup(G,cs),Subgroup(G,cs{[1,2]})];;
if phis<>expected then Error("Unexpected Frattini subgroups");fi;
if Comm(sigma[1],sigma[3])<>sigma[2]^2 then Error("Redundancy identity failure");fi;
if Ai[2]<>Subgroup(G,sigma{[1,3]}) then Error("Redundancy generation failure");fi;
if C<>Subgroup(G,[cs[2]]) then Error("C identification failure");fi;
if List(Ai,Size)<>[32,32,32] then Error("A_i orders");fi;
if List(phis,Size)<>[4,8,4] then Error("Phi orders");fi;
if List([1..3],i->LogInt(Size(Ai[i])/Size(phis[i]),2))<>[3,2,3] then Error("Ranks");fi;
if Size(C)<>2 or Size(gamma3)<>1 then Error("Contradiction values");fi;
q:=NaturalHomomorphismByNormalSubgroup(G,C);;
qrho:=List(rho,r->Image(q,r));;
qgroups:=List(subsets,I->Subgroup(Image(q),qrho{I}));;
qfail:=[];;
for i in [1..Length(subsets)] do
 for j in [1..Length(subsets)] do
  k:=Position(subsets,Intersection(subsets[i],subsets[j]));;
  if Intersection(qgroups[i],qgroups[j])<>qgroups[k] then
   Add(qfail,[subsets[i],subsets[j],Size(Intersection(qgroups[i],qgroups[j])),Size(qgroups[k])]);
  fi;
 od;
od;
Print("GAP=",GAPInfo.Version,"; NQ=",PackageInfo("nq")[1].Version,"\n");
Print("group_order=",Size(G),"; class=",NilpotencyClassOfGroup(G),"; rank=4; type=",adj,"\n");
Print("full_IP_comparisons=",count,"; status=PASS\n");
Print("rotation_order=",Size(A),"; A_i_orders=",List(Ai,Size),"\n");
Print("A_i_Frattini_orders=",List(phis,Size),"; A_i_minimal_generator_numbers=",List([1..3],i->LogInt(Size(Ai[i])/Size(phis[i]),2)),"\n");
Print("sigma2_squared_equals_comm_sigma1_sigma3=true\n");
Print("actual_C_order=",Size(C),"; theorem_4_2_c_prediction=1\n");
Print("actual_quotient_order=",Size(Image(q)),"; theorem_4_2_d_prediction=128\n");
Print("gamma3_order=",Size(gamma3),"; C_equals_gamma3=",C=gamma3,"\n");
Print("induced_quotient_IP_failures=",Length(qfail),"; quotient_type=",List([1..3],i->Order(qrho[i]*qrho[i+1])),"\n");
Print("PASS: source hypotheses hold; Theorem 4.2(c),(d),(e) fail for C as defined.\n");
QUIT;
