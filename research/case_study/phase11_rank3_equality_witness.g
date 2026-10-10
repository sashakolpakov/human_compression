# One exact witness: three independent Frattini directions plus cyclic TPP
# and equality of cardinalities still do not give global product injection.
LoadPackage("smallgrp");;
G := SmallGroup(64,90);;
pc := GeneratorsOfGroup(G);;
a := pc[1];;
b := pc[1]*pc[2]*pc[4]*pc[5];;
c := pc[1]*pc[3]*pc[4]*pc[5]*pc[6];;
A := Subgroup(G,[a]);; B := Subgroup(G,[b]);; C := Subgroup(G,[c]);;
ab := Set(Concatenation(List(Elements(A),x->List(Elements(B),y->x*y))));;
abc := Set(Concatenation(List(ab,x->List(Elements(C),y->x*y))));;
Assert(0,IdGroup(G)=[64,90]);
Assert(0,List([A,B,C],Size)=[4,4,4]);
Assert(0,Size(Intersection(A,B))=1);
Assert(0,Length(Intersection(ab,Elements(C)))=1);
Assert(0,Subgroup(G,[a,b,c])=G);
Assert(0,Index(G,FrattiniSubgroup(G))=8);
Assert(0,NilpotencyClassOfGroup(G)=3);
Assert(0,Length(abc)=48);
Print("PASS\n");
Print("GAP ",GAPInfo.Version," SmallGrp ",PackageInfo("smallgrp")[1].Version,"\n");
Print("Group SmallGroup(64,90); standard pc generators f1,...,f6\n");
Print("a=f1, b=f1*f2*f4*f5, c=f1*f3*f4*f5*f6\n");
Print("Orders [4,4,4]; generates G; Frattini index 8; nilpotency class 3\n");
Print("TPP: |A intersect B|=1 and |AB intersect C|=1\n");
Print("|A||B||C|=|G|=64, but |ABC|=48\n");
QUIT;
