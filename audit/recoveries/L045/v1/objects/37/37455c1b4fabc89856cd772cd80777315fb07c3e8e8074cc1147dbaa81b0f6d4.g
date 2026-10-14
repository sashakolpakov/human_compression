cases:=0;;
for U in Filtered(Combinations([1..6]),x->Length(x)>=3) do
 for T in Combinations([1..6],3) do
  if Length(Intersection(U,T))>0 then
   gens:=Concatenation(GeneratorsOfGroup(AlternatingGroup(U)),GeneratorsOfGroup(AlternatingGroup(T)));
   H:=Group(gens);;
   if H<>AlternatingGroup(Union(U,T)) then Error("merge equality");fi;
   cases:=cases+1;
  fi;
 od;
od;
needless:=Group((1,2,3),(4,5,6));;
if Size(needless)<>9 or needless=AlternatingGroup(6) then Error("disjoint negative control");fi;
Print("PASS_INDEPENDENT_MERGE ",cases,"\n");
QUIT;
