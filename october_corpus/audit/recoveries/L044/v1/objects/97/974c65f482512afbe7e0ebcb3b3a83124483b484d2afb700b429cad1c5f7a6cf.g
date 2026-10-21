# Bounded diagnostic: orbit cuts plus string commutation do not give
# the one-or-two selected-edge rigidity. This is NOT a string C-group.
SizeScreen([10000,10000]);;
r:=[(1,2)(3,4)(5,7),(2,6)(7,8),(1,3)(2,4),(1,5)(2,7)(6,8)];;
G:=Group(r);;
Q:=[[[1,2],[3,4]],[[2,6],[7,8]],[[1,3],[2,4]],[[1,5],[6,8]]];;
if Size(G)<>40320 or not IsTransitive(G,[1..8]) then Error("ambient group");fi;
for i in [1..4] do for j in [i+2..4] do
 if Comm(r[i],r[j])<>() then Error("string commutation");fi;
od;od;
orbits:=[];;
for i in [1..4] do
 H:=Subgroup(G,r{Difference([1..4],[i])});;
 Add(orbits,Orbits(H,[1..8]));;
 for e in Q[i] do
  if e[1]^r[i]<>e[2] or e[2] in Orbit(H,e[1]) then Error("eligible edge");fi;
 od;
od;
edges:=Concatenation(Q);; seen:=[1];;
repeat
 old:=ShallowCopy(seen);;
 for e in edges do if Intersection(seen,e)<>[] then seen:=Union(seen,e);fi;od;
until seen=old;
if Length(edges)<>8 or seen<>[1..8] then Error("connected unicyclic selection");fi;
# Selected alternating square has labels0,2 and vertices1,2,4,3.
# The actual square1,2,7,5 has labels0,3 and shares edge1--2.
actual:=[[1,2,1],[2,7,4],[7,5,1],[5,1,4]];;
if not ForAll(actual,e->e[1]^r[e[3]]=e[2]) then Error("actual commuting square");fi;
if not [1,5] in Q[4] or [2,7] in Q[4] then Error("exactly one selected label3 edge");fi;
subs:=Combinations([1..4]);;Hs:=List(subs,s->Subgroup(G,r{s}));;fails:=[];;
for i in [1..16] do for j in [1..16] do
 if Intersection(Hs[i],Hs[j])<>Hs[Position(subs,Intersection(subs[i],subs[j]))] then Add(fails,[subs[i],subs[j]]);fi;
od;od;
if fails<>[[[1,2,3],[2,3,4]],[[2,3,4],[1,2,3]]] then Error("precise IP obstruction");fi;
P:=Subgroup(G,r{[1,2,3]});;T:=Subgroup(G,r{[2,3,4]});;M:=Subgroup(G,r{[2,3]});;
Print("PASS_BOUNDED_ORBIT_CUT_OBSTRUCTION\n");
Print("group_order=",Size(G)," selected_edges=",Length(edges)," vertices=",Length(seen),"\n");
Print("omission_orbits=",orbits,"\n");
Print("end_parabolic_orders=",[Size(P),Size(T)]," intersection_order=",Size(Intersection(P,T))," prescribed_middle_order=",Size(M),"\n");
Print("IP_failing_pairs_one_based=",fails,"\n");
QUIT;
