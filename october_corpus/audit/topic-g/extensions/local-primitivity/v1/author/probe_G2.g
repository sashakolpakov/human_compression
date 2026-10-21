G:=PSU(3,3);;
Print("G order ",Size(G)," degree ",LargestMovedPoint(G),"\n");
ms:=ConjugacyClassesMaximalSubgroups(G);;
Print("maximal orders ",List(ms,c->Size(Representative(c))),"\n");
for c in ms do
 H:=Representative(c);
 if Index(G,H)=63 then
  A:=Action(G,RightTransversal(G,H),OnRight);;
  Print("63 action ",Size(A)," primitive ",IsPrimitive(A,[1..63])," subdegrees ",List(Orbits(Stabilizer(A,1),[1..63]),Length),"\n");
 fi;
od;
QUIT;
