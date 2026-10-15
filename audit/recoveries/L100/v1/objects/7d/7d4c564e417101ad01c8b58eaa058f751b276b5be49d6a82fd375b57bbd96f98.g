PSL34RankTwo:=rec();;PSL34Witnesses:=[];;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/result.g");;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/pair_witnesses.g");;
ExportLiteral:=function()
 local R,W,L,B,p,n,g;
 R:=PSL34RankTwo;W:=PSL34Witnesses;n:=21;
 if Group(R.group_generators)<>PSL(3,4) then Error("literal named model");fi;
 L:=gs->List(gs,g->ListPerm(g,n));
 B:=function(x)if x then return 1;else return 0;fi;end;
 p:=List(R.pairs,r->[L(r.A),L(r.B),L(r.H),r.orders,r.degrees,r.common_counts,B(r.digon),B(r.IP2),List(r.local_two_transitive,B)]);
 Print("LITERAL_DATA ",[L(R.group_generators),p,R.classes,List(W,w->[w.source_pair,w.target_pair,ListPerm(w.type_permutation,2),L(w.generator_images)])],"\n");
 Print("PASS_LITERAL_EXPORT\n");
end;;
ExportLiteral();
QUIT;
