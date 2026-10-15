SizeScreen([1000000,24]);;
LoadPackage("LINS");;
Read("/Users/sasha/medusa/research/leemans/corpus106_L033_coxeter_lins_methods_v1/coxeter_seeds.g");;
Read("/Users/sasha/medusa/research/leemans/corpus106_L033_coxeter_lins_methods_v1/composed_pmodules.g");;
Read("/Users/sasha/medusa/research/leemans/algebra/coxeter_quotients/small_square_v1/enumerate_all.g");;
RunHyperbolic([[1, 3, 2, 5], [3, 1, 5, 2], [2, 5, 1, 3], [5, 2, 3, 1]],[120,120,120,120],3840,"/Users/sasha/medusa/research/leemans/algebra/coxeter_quotients/small_square_author01/census/records.g");;
QUIT_GAP(0);
