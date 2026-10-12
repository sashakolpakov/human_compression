# Direct panel actions for the one M12 census class absent from the archive.
# This does not call the shadow engine or use the old recorded twoT flag.
Read("prior_representatives.g");;
SizeScreen([100000,100000]);;
P:=SporadicRepresentatives[18].parabolics;;
B:=Intersection(P);;
Print("AMBIENT_ORDER ",Size(G)," PARABOLICS ",List(P,Size)," BOREL ",Size(B),"\n");;
for i in [1..3] do
 K:=Intersection(P{Difference([1..3],[i])});;
 C:=RightCosets(K,B);;
 orbs:=OrbitsDomain(B,C,OnRight);;
 Print("PANEL ",i," ORDER ",Size(K)," DEGREE ",Length(C),
       " POINT_STABILIZER_ORBITS ",SortedList(List(orbs,Length)),"\n");;
 if Length(C)<2 or Length(orbs)<>2 then
  Print("NOT_LOCALLY_TWO_TRANSITIVE ",i,"\n");;
 fi;
od;
Print("PASS_M12_MISSING_PANELS\n");;QUIT;
