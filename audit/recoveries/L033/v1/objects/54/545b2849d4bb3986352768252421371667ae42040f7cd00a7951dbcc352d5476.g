LoadPackage("LINS");;
FindExplicit3535 := function(root,output)
  local M,F,x,rels,i,j,V,basis,gens,g,b,a,H,A,rows,h,marking,result,
        target,stream,first,small,sm,d;
  Read(Concatenation(root,"/coxeter_seeds.g"));
  Read(Concatenation(root,"/enumerate_broad.g"));
  M:=[[1,3,2,5],[3,1,5,2],[2,5,1,3],[5,2,3,1]];
  F:=FreeGroup(4);x:=GeneratorsOfGroup(F);rels:=List(x,g->g^2);
  for i in [1..4] do for j in [i+1..4] do Add(rels,(x[i]*x[j])^M[i][j]);od;od;
  F:=F/rels;
  stream:=OutputTextFile(output,false);SetPrintFormattingStatus(stream,false);PrintTo(stream,"[\n");first:=true;
  for target in [3840,9720] do
    if target=3840 then
      A:=Group((1,2)(3,4)(5,6)(7,8)(9,10), (1,3,5,7,9)(2,4,6,8,10), (1,3,5)(2,4,6), (1,2));
    else
      V:=Filtered(Tuples([0,1,2],5),v->Sum(v) mod 3=0);
      gens:=[];
      for i in [1..4] do
        b:=[0,0,0,0,2];b[i]:=1;
        Add(gens,PermList(List(V,v->Position(V,List([1..5],j->(v[j]+b[j]) mod 3)))));
      od;
      for g in [(1,2,3,4,5),(1,2,3)] do
        Add(gens,PermList(List(V,v->Position(V,Permuted(v,g)))));
      od;
      A:=Group(gens);
    fi;
    H:=DirectProduct(A,Group((1,2)));
    if Size(H)<>target then Error("named affine construction order mismatch");fi;
    Print("EXPLICIT_TARGET_BEGIN ",target,"\n");
    rows:=CoxeterTargetEpis(F,H,M);
    for h in rows do
      marking:=List(GeneratorsOfGroup(F),g->Image(h,g));
      result:=HyperbolicCheck(marking,M,[120,120,120,120]);
      if result.ok then
        small:=SmallerDegreePermutationRepresentation(H);sm:=List(marking,g->Image(small,g));d:=LargestMovedPoint(Group(sm));
        if Size(Group(sm))<>target then Error("compact map failure");fi;
        if not first then PrintTo(stream,",\n");fi;first:=false;
        PrintTo(stream,"{\"type\":\"3535\",\"node\":",Position(rows,h),",\"order\":",target,",\"local_orders\":",result.local_orders,",\"permutations\":",List(sm,g->ListPerm(g,d)),"}");
        Print("EXPLICIT_POSITIVE ",target," ",result,"\n");
      fi;
    od;
  od;
  PrintTo(stream,"\n]\n");CloseStream(stream);Print("COMPLETE_EXPLICIT_3535\n");
end;;
