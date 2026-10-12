# Identify the exceptional panel as the action of A5 on its ten duads.
Read("prior_representatives.g");;
SizeScreen([100000,100000]);;
P:=SporadicRepresentatives[18].parabolics;;B:=Intersection(P);;
K:=Intersection(P[2],P[3]);;A:=AlternatingGroup(5);;
iso:=IsomorphismGroups(K,A);;
if iso=fail or not IsBijective(iso) then Error("panel identification");fi;
D:=Image(iso,B);;small:=Filtered(Orbits(D,[1..5]),o->Length(o)=2);;
if Length(small)<>1 then Error("unique stabilized duad");fi;
d:=small[1];;
if D<>Stabilizer(A,d,OnSets) then Error("exact duad stabilizer");fi;
all:=Combinations([1..5],2);;
if SortedList(List(OrbitsDomain(D,all,OnSets),Length))<>[1,3,6] then Error("duad suborbits");fi;
Print("PANEL_GENERATORS ",GeneratorsOfGroup(K),"\n");;
Print("PANEL_IMAGES ",List(GeneratorsOfGroup(K),x->Image(iso,x)),"\n");;
Print("BOREL_IMAGES ",GeneratorsOfGroup(D)," DUAD ",d,"\n");;
Print("PASS_EXACT_A5_DUAD_PANEL\n");;QUIT;
