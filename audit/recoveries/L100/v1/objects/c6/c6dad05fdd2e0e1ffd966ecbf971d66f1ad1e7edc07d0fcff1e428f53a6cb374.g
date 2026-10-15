PSL34RankTwo:=rec();;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/result.g");;
ExportConstructionInput:=function()
 local R,G,p,A,B,lines,blocks;
 R:=PSL34RankTwo;G:=Group(R.group_generators);
 if G<>PSL(3,4) or Size(G)<>20160 then Error("named model mismatch");fi;
 p:=R.pairs[R.classes[1][1]];
 A:=Group(p.A);B:=Group(p.B);
 blocks:=Filtered(Concatenation(Orbits(A,[1..21]),Orbits(B,[1..21])),x->Length(x)=5);
 if Length(blocks)<>1 then Error("line seed not unique");fi;
 lines:=Set(Orbit(G,Set(blocks[1]),OnSets));
 if Length(lines)<>21 then Error("line orbit");fi;
 Print("CONSTRUCTION_INPUT ",[List(R.group_generators,g->ListPerm(g,21)),lines],"\n");
 Print("PASS_CONSTRUCTION_INPUT\n");
end;;
ExportConstructionInput();
QUIT;
