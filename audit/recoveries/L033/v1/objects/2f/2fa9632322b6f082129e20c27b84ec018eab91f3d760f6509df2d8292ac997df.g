SizeScreen([1000000,24]);;
LoadPackage("LINS");;
Read("/Users/sasha/medusa/research/leemans/corpus106_L033_coxeter_lins_methods_v1/coxeter_seeds.g");;
Read("/Users/sasha/medusa/research/leemans/corpus106_L033_coxeter_lins_methods_v1/composed_pmodules.g");;
Read("/Users/sasha/medusa/research/leemans/algebra/coxeter_quotients/divisor_v1/divisor_options.g");;

F:=FreeGroup(3);;x:=GeneratorsOfGroup(F);;
W:=F/Concatenation(List(x,g->g^2),[(x[1]*x[2])^2,(x[1]*x[3])^2,(x[2]*x[3])^2]);;
good:=List(LowIndexNormalSubgroupsSearch(W,8,CoxeterDivisorOptions([[1,2,2],[2,1,2],[2,2,1]],8)));;
opt:=CoxeterDivisorOptions([[1,2,2],[2,1,2],[2,2,1]],8);;opt.DoCut:=function(gr,H)return Index(H)<>8;end;;
bad:=List(LowIndexNormalSubgroupsSearch(W,8,opt));;
if Number(good,H->Index(H)=8)<>1 or Number(bad,H->Index(H)=8)<>0 then Error("incorrect equality cut must lose target kernel");fi;
Print("ANCESTOR_CONTROL 1 0\n");;

QUIT_GAP(0);
