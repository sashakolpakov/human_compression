# Required finite premise: complete maximal-subgroup list and Aut order
# for the abstract group G2(2)' = PSU(3,3). No affine-module construction.
G:=PSU(3,3);;
if Size(G)<>6048 or not IsSimpleGroup(G) then Error("wrong G2(2)' group");fi;
maxs:=ConjugacyClassesMaximalSubgroups(G);;
orders:=SortedList(List(maxs,c->Size(Representative(c))));;
if orders<>[96,96,168,216] then Error("unexpected complete maximal orders");fi;
if ForAny(orders,m->m mod 96=0 and m<>96) then Error("index63 subgroup could be nonmaximal");fi;
A:=AutomorphismGroup(G);;
if Size(A)<>12096 then Error("unexpected full automorphism order");fi;
Print("G2_SMALL_PREMISE|",GAPInfo.Version,"|",Size(G),"|",orders,"|",Size(A),"\n");
for c in maxs do
 H:=Representative(c);;
 if Size(H)=96 then
  P:=Action(G,RightTransversal(G,H),OnRight);;
  if Size(P)<>6048 or not IsPrimitive(P,[1..63]) then Error("index63 action");fi;
  ds:=SortedList(List(Orbits(Stabilizer(P,1),[1..63]),Length));;
  Print("G2_SMALL_ACTION|",Size(P),"|",ds,"\n");
 fi;
od;
if 12096 mod (63*62)=0 then Error("two-transitivity exclusion broken");fi;
Print("PASS\n");
QUIT;
