Read("/Users/sasha/medusa/research/leemans/topic_D_L096_HS_extension/archive_data/inputs.g");;
Read("/Users/sasha/medusa/research/leemans/topic_D_L096_HS_extension/profile_match_v2.g");;
Read("/Users/sasha/medusa/research/leemans/reboot_20261013/L091_work/rank_two_catalogue.g");;
G:=Group(Concatenation(L096Inputs[1].parabolic_generators));;
r:=RankTwoCatalogue(G);;
PrintTo("/Users/sasha/medusa/research/leemans/reboot_20261013/L091_work/clean_run01/result.g","HSRankTwoResult:=",r,";;\n");
Print("PASS_COMPLETE_RANK_TWO\n");
QUIT;
