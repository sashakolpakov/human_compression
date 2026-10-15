SizeScreen([1000000,24]);;
LoadPackage("LINS");;
Read("/Users/sasha/medusa/research/leemans/corpus106_L033_coxeter_lins_methods_v1/coxeter_seeds.g");;
Read("/Users/sasha/medusa/research/leemans/corpus106_L033_coxeter_lins_methods_v1/composed_pmodules.g");;
Read("/Users/sasha/medusa/research/leemans/algebra/coxeter_quotients/divisor_v1/divisor_options.g");;
CoxeterDivisorOptions([[1,2,2],[2,1,2],[2,2,1]],LINS_MaxIndex+1);;
Print("INVALID_ACCEPTED\n");;
QUIT_GAP(0);
