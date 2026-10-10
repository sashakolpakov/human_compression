# Standalone counterexample to "cyclic TPP + numerical equality implies
# injectivity of the global multiplication map". No census is required.
LoadPackage("smallgrp");;
G := SmallGroup(32,5);;
pc := GeneratorsOfGroup(G);;
a := pc[2];; b := pc[1];; c := pc[2]*pc[3];;
A := Subgroup(G,[a]);; B := Subgroup(G,[b]);; C := Subgroup(G,[c]);;
ab := Set(Concatenation(List(Elements(A),x->List(Elements(B),y->x*y))));;
abc := Set(Concatenation(List(ab,x->List(Elements(C),y->x*y))));;
Assert(0,IdGroup(G)=[32,5]);
Assert(0,List([A,B,C],Size)=[2,8,2]);
Assert(0,Size(Intersection(A,B))=1);
Assert(0,Length(Intersection(ab,Elements(C)))=1);
Assert(0,Product(List([A,B,C],Size))=Size(G));
Assert(0,Length(abc)=24);
Print("PASS\n");
Print("GAP ",GAPInfo.Version," SmallGrp ",PackageInfo("smallgrp")[1].Version,"\n");
Print("Group SmallGroup(32,5), standard pc generators f1,...,f5\n");
Print("Cyclic generators (f2,f1,f2*f3); orders [2,8,2]\n");
Print("|A intersect B|=1; |AB intersect C|=1; |A||B||C|=32; |ABC|=24\n");
Print("Structure ",StructureDescription(G),"; nilpotency class ",NilpotencyClassOfGroup(G),"\n");
QUIT;
