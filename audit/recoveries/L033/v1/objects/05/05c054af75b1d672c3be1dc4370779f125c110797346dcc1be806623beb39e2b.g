LoadPackage("LINS");;
ExportNegatives:=function(root,output)
  local typ,M,bound,F,x,rels,i,j,G,gr,node,idx,act,H,sm,mark,d,stream,first;
  stream:=OutputTextFile(output,false);SetPrintFormattingStatus(stream,false);PrintTo(stream,"[\n");first:=true;
  for typ in ["3434","3534"] do
    if typ="3434" then M:=[[1,3,2,4],[3,1,4,2],[2,4,1,3],[4,2,3,1]];bound:=336;
    else M:=[[1,3,2,4],[3,1,5,2],[2,5,1,3],[4,2,3,1]];bound:=2160;fi;
    F:=FreeGroup(4);x:=GeneratorsOfGroup(F);rels:=List(x,g->g^2);
    for i in [1..4] do for j in [i+1..4] do Add(rels,(x[i]*x[j])^M[i][j]);od;od;
    G:=F/rels;gr:=LowIndexNormalSubgroupsSearchForAll(G,bound);
    for node in List(gr) do
      idx:=Index(node);
      if (typ="3434" and idx=336) or (typ="3534" and idx in [360,2160]) then
        act:=FactorCosetAction(G,Grp(node));H:=Image(act);sm:=SmallerDegreePermutationRepresentation(H);
        mark:=List(GeneratorsOfGroup(G),g->Image(sm,Image(act,g)));d:=LargestMovedPoint(Group(mark));
        if Size(Group(mark))<>idx then Error("nonfaithful compact negative");fi;
        if not first then PrintTo(stream,",\n");fi;first:=false;
        PrintTo(stream,"{\"type\":\"",typ,"\",\"node\":",Position(List(gr),node),",\"order\":",idx,",\"expected_reject\":true,\"matrix\":",M,",\"permutations\":",List(mark,g->ListPerm(g,d)),"}");
      fi;
    od;
  od;
  PrintTo(stream,"\n]\n");CloseStream(stream);Print("COMPLETE_NEGATIVES\n");
end;;
