# Optional direct check of the source's full-group line-primitivity claim.
A:=PGammaL(2,8);;G:=DerivedSubgroup(A);;
if Size(A)<>1512 or Size(G)<>504 then Error("wrong projective groups");fi;
D:=Normalizer(G,SylowSubgroup(G,3));;
U0:=SylowSubgroup(G,2);;
U:=First(AsList(ConjugacyClassSubgroups(G,U0)),x->Size(Intersection(D,x))=2);;
P:=Normalizer(A,D);;B:=Intersection(P,Normalizer(A,U));;L:=ClosureGroup(U,B);;
if [Size(D),Size(U),Size(P),Size(L),Size(B)]<>[18,8,54,24,6] then Error("WBS stabilizers");fi;
pl:=Action(P,RightTransversal(P,B),OnRight);;
ln:=Action(L,RightTransversal(L,B),OnRight);;
if IsPrimitive(pl,[1..9]) or not IsPrimitive(ln,[1..4]) then Error("wrong local conclusions");fi;
point_action:=Action(A,RightTransversal(A,P),OnRight);;
if not IsTransitive(Stabilizer(point_action,1),[2..28]) then Error("not two-point transitive");fi;
Print("WBS8|",Size(A),"|",Size(P),"|",Size(L),"|",Size(B),"|",Size(pl),"|",Size(ln),"|pencil_imprimitive|line_primitive\n");
Print("PASS\n");QUIT;
