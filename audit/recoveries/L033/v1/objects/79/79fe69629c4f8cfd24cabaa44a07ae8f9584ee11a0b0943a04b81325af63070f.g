LoadPackage("LINS");;
Read("/Users/sasha/medusa/research/leemans/corpus106_L033_coxeter_lins_methods_v1/coxeter_seeds.g");;
Read("/Users/sasha/medusa/research/leemans/corpus106_L033_coxeter_lins_methods_v1/composed_pmodules.g");;
Read("/Users/sasha/medusa/research/leemans/corpus106_L033_coxeter_lins_methods_v1/enumerate_changed.g");;
Read("/Users/sasha/medusa/research/leemans/algebra/coxeter_quotients/divisor_work/divisor_options.g");;
RunDivisorTarget:=function()
 local M,target,F,x,rels,i,j,W,start,gr,nodes,node,N,index,action,H,marking,result,small,sm,degree,records,r,f,n;
 M:=[[1,3,2,5],[3,1,5,2],[2,5,1,3],[5,2,3,1]];target:=9720;
 Reset(GlobalMersenneTwister,193314);Reset(GlobalRandomSource,193314);
 F:=FreeGroup("a","b","c","d");x:=GeneratorsOfGroup(F);rels:=List(x,g->g^2);
 for i in [1..4]do for j in [i+1..4]do Add(rels,(x[i]*x[j])^M[i][j]);od;od;W:=F/rels;start:=Runtime();
 gr:=LowIndexNormalSubgroupsSearch(W,target,CoxeterDivisorOptions(M,target));nodes:=List(gr);
 if not ForAll(nodes,r->target mod Index(r)=0)then Error("exact divisibility roster");fi;
 Print("DIVISOR_INDEX_MULTIPLICITIES ",Collected(List(nodes,Index)),"\n");records:=[];
 for n in [1..Length(nodes)]do
  node:=nodes[n];index:=Index(node);if index<>target then continue;fi;
  N:=Grp(node);action:=FactorCosetAction(W,N);H:=Image(action);marking:=List(GeneratorsOfGroup(W),g->Image(action,g));
  if Size(H)<>index or Group(marking)<>H then Error("faithful exact quotient");fi;
  result:=HyperbolicCheck(marking,M,[120,120,120,120]);
  Print("DIVISOR_TARGET_CHECK ",n," ",result,"\n");
  small:=SmallerDegreePermutationRepresentation(H);sm:=List(marking,g->Image(small,g));degree:=LargestMovedPoint(Group(sm));
  if Size(Group(sm))<>target or HyperbolicCheck(sm,M,[120,120,120,120])<>result then Error("faithful marked compact bridge");fi;
  r:=rec(node:=n,order:=target,permutations:=List(sm,g->ListPerm(g,degree)),checks:=result);Add(records,r);
 od;
 PrintTo(Concatenation(OUTPUT_DIR,"/records.g"),"divisor_records:=",records,";;\n");
 Print("COMPLETE_DIVISOR_TARGET ",target," NODES ",Length(nodes)," EXACT ",Length(records)," MS ",Runtime()-start,"\n");
end;;
RunDivisorTarget();;QUIT_GAP(0);
