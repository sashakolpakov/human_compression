SizeScreen([1000000,1000000]);;
P:="/Users/sasha/medusa/research/leemans/corpus106_L045_sporadic_twelve_v1";;
W:="/Users/sasha/medusa/math_compression/papers/topic-diagonal/v2/papers/sporadic/witnesses";;
Emit:=function(name,gs,word,orders)
 local n;
 n:=Maximum(List(gs,LargestMovedPoint));
 Print("{\"name\":\"",name,"\",\"generators\":",List(gs,g->ListPerm(g,n)),",\"word\":",word,",\"orders\":",orders,"}\n");
end;;
Read(Concatenation(P,"/mathieu_pairs.g"));;
for z in MathieuPairs do
 Emit(Concatenation("M",String(z.n)),[z.x,z.y],[],[]);
od;
Read(Concatenation(P,"/rank4_pairs.g"));;
for z in SporadicPairs do
 Read(Concatenation(W,"/",z.name,"_rank4_witness.g"));;
 Emit(z.name,Rank4Witness,z.word,z.orders);
od;
Read(Concatenation(P,"/small_pairs.g"));;
for z in SmallSporadicPairs do Emit(z.name,[z.x,z.t],[],z.orders);od;
QUIT;
