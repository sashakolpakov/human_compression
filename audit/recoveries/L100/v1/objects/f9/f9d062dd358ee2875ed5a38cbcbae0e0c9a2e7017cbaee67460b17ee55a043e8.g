Read("/Users/sasha/medusa/research/leemans/topic_D_L096_HS_extension/profile_match_v2.g");;
Read("/Users/sasha/medusa/research/leemans/geometry/psl3_4/rank_two.g");;
G:=PSL(3,4);;
Print("AMBIENT ",Size(G)," DEGREE ",LargestMovedPoint(G),"\n");
r:=PrimitiveRankTwoCatalogue(G);;
PrintTo("/Users/sasha/medusa/research/leemans/geometry/psl3_4/result.g","PSL34RankTwo:=",r,";;\n");
Print("PASS_PRIMITIVE_RANK_TWO\n");
QUIT;
