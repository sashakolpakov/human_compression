MethodControls:=function(root)
 local make,brute,targets,matrices,M,Q,F,rows,got,wanted,cases,oldfun,old,new,typ,tests,records,oldrows,newrows,pairs,checks;
 make:=function(M)
  local f,x,r,i,j;
  f:=FreeGroup(Length(M));x:=GeneratorsOfGroup(f);r:=List(x,g->g^2);
  for i in [1..Length(M)] do for j in [i+1..Length(M)] do Add(r,(x[i]*x[j])^M[i][j]);od;od;
  return f/r;
 end;
 brute:=function(Q,M)
  local all,res,t,i,j,okay;
  all:=Filtered(Elements(Q),x->x^2=One(Q));res:=[];
  for t in Tuples(all,Length(M)) do
   okay:=true;
   for i in [1..Length(M)] do for j in [i+1..Length(M)] do
    if (t[i]*t[j])^M[i][j]<>One(Q) then okay:=false;fi;
   od;od;
   if okay and Size(Group(t))=Size(Q) then AddSet(res,Minimum(Orbit(Q,t,OnTuples)));fi;
  od;
  return res;
 end;
 targets:=[Group(()),SymmetricGroup(3),DihedralGroup(IsPermGroup,8),AlternatingGroup(4),SymmetricGroup(4),AlternatingGroup(5)];
 matrices:=[[[1,2,2,2],[2,1,2,2],[2,2,1,2],[2,2,2,1]],[[1,3,2,4],[3,1,4,2],[2,4,1,3],[4,2,3,1]],[[1,3,2,5],[3,1,5,2],[2,5,1,3],[5,2,3,1]]];
 cases:=0;pairs:=0;
 for M in matrices do
  F:=make(M);
  for Q in targets do
   rows:=CoxeterTargetEpis(F,Q,M);
   got:=List(rows,h->Minimum(Orbit(Q,List(GeneratorsOfGroup(F),x->Image(h,x)),OnTuples)));
   if Length(Set(got))<>Length(got) then Error("duplicate inner orbit");fi;
   wanted:=brute(Q,M);if Set(got)<>wanted then Error("seed literal mismatch");fi;
   cases:=cases+1;pairs:=pairs+Length(got);
  od;
 od;
 records:=function(G,graph)
  local rows,n,a,s,d;
  rows:=[];
  for n in List(graph) do
   a:=FactorCosetAction(G,Grp(n));s:=List(GeneratorsOfGroup(G),g->Image(a,g));d:=Maximum(1,LargestMovedPoint(Image(a)));
   Add(rows,rec(order:=Index(n),permutations:=List(s,g->ListPerm(g,d))));
  od;
  return rows;
 end;
 oldfun:=LINS_FindPModules;
 tests:=[[matrices[1],16],[matrices[2],336],[matrices[3],120]];checks:=0;
 for typ in tests do
  M:=typ[1];F:=make(M);Reset(GlobalMersenneTwister,193314);Reset(GlobalRandomSource,193314);
  MakeReadWriteGlobal("LINS_FindPModules");LINS_FindPModules:=oldfun;MakeReadOnlyGlobal("LINS_FindPModules");
  old:=LowIndexNormalSubgroupsSearchForAll(F,typ[2]);oldrows:=records(F,old);
  Read(Concatenation(root,"/composed_control.g"));
  Reset(GlobalMersenneTwister,193314);Reset(GlobalRandomSource,193314);
  new:=LowIndexNormalSubgroupsSearch(F,typ[2],CoxeterSeedOptions(M));newrows:=records(F,new);
  if OrderedMarkingBijection(oldrows,newrows)=fail then Error("complete normal kernel mismatch");fi;
  Print("NORMAL_KERNEL_CONTROL ",typ[2]," ",Length(oldrows)," ",ComposedImageChecks,"\n");
  checks:=checks+ComposedImageChecks;
 od;
 Print("COMPLETE_METHOD_CONTROLS ",cases," SEED_CASES ",pairs," INNER_ORBITS 3 KERNEL_CONTROLS ",checks," IMAGE_CHECKS\n");
end;;
