SizeScreen([1000000,24]);;
LoadPackage("LINS");;
Read("/Users/sasha/medusa/research/leemans/corpus106_L033_coxeter_lins_methods_v1/coxeter_seeds.g");;
Read("/Users/sasha/medusa/research/leemans/corpus106_L033_coxeter_lins_methods_v1/composed_pmodules.g");;
Read("/Users/sasha/medusa/research/leemans/algebra/coxeter_quotients/divisor_v1/divisor_options.g");;
F:=FreeGroup(3);;x:=GeneratorsOfGroup(F);;W:=F/Concatenation(List(x,g->g^2),[(x[1]*x[2])^2,(x[1]*x[3])^2,(x[2]*x[3])^2]);;LowIndexNormalSubgroupsSearch(W,1,CoxeterDivisorOptions([[1,2,2],[2,1,2],[2,2,1]],2));;
Print("INVALID_ACCEPTED\n");;
QUIT_GAP(0);
