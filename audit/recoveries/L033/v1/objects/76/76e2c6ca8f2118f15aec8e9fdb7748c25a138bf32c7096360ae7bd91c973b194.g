LoadPackage("LINS");;
Read("/Users/sasha/medusa/research/leemans/corpus106_L033_coxeter_lins_methods_v1/coxeter_seeds.g");;
Read("/Users/sasha/medusa/research/leemans/corpus106_L033_coxeter_lins_methods_v1/composed_pmodules.g");;
Read("/Users/sasha/medusa/research/leemans/algebra/coxeter_quotients/divisor_work/divisor_options.g");;
DivisorControls:=function()
 local examples,e,F,x,rels,i,j,W,all,m,got,wanted,H,matches,total,cases;
 examples:=[rec(name:="A3",M:=[[1,3,2],[3,1,3],[2,3,1]],bound:=24,targets:=[1,2,3,4,6,8,12,24]),
 rec(name:="B3",M:=[[1,4,2],[4,1,3],[2,3,1]],bound:=48,targets:=[2,6,12,16,24,48]),
 rec(name:="C2cubed",M:=[[1,2,2],[2,1,2],[2,2,1]],bound:=8,targets:=[1,2,4,8]),
 rec(name:="affineA2",M:=[[1,3,3],[3,1,3],[3,3,1]],bound:=24,targets:=[6,9,12,18,24]),
 rec(name:="H3",M:=[[1,5,2],[5,1,3],[2,3,1]],bound:=120,targets:=[30,60,120])];
 total:=0;cases:=0;
 for e in examples do
  F:=FreeGroup(Length(e.M));x:=GeneratorsOfGroup(F);rels:=List(x,g->g^2);
  for i in [1..Length(x)]do for j in [i+1..Length(x)]do Add(rels,(x[i]*x[j])^e.M[i][j]);od;od;
  W:=F/rels;all:=List(LowIndexNormalSubgroupsSearch(W,e.bound));
  for m in e.targets do
   got:=List(LowIndexNormalSubgroupsSearch(W,m,CoxeterDivisorOptions(e.M,m)));
   wanted:=Filtered(all,H->m mod Index(H)=0);
   if Length(got)<>Length(wanted)then Error("complete divisor inventory cardinality");fi;
   for H in got do
    if m mod Index(H)<>0 then Error("retained index divides target");fi;
    matches:=Filtered(wanted,K->Index(K)=Index(H)and LINS_IsSubgroupFp(Grp(H),Grp(K))and LINS_IsSubgroupFp(Grp(K),Grp(H)));
    if Length(matches)<>1 then Error("actual normal kernel equality");fi;
    total:=total+1;
   od;
   cases:=cases+1;Print("DIVISOR_CONTROL ",e.name," ",m," ",Length(got),"\n");
  od;
 od;
 Print("COMPLETE_DIVISOR_CONTROLS ",cases," ",total,"\n");
end;;
DivisorControls();;QUIT_GAP(0);
