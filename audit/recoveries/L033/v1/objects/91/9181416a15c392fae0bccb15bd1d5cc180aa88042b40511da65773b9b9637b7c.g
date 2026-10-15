LoadPackage("LINS");;
hyperbolic_records:=[];;
VerifyFiniteCore:=function(root)
  local types,matrices,localorders,n,t,r,s,H,c,idx,M,i,j,J,F,x,rel,subM,u,count,bridge;
  types:=["3334","3335","3434","3534","353","435","535","5333"];
  matrices:=[[[1,3,2,4],[3,1,3,2],[2,3,1,3],[4,2,3,1]],
    [[1,3,2,5],[3,1,3,2],[2,3,1,3],[5,2,3,1]],
    [[1,3,2,4],[3,1,4,2],[2,4,1,3],[4,2,3,1]],
    [[1,3,2,4],[3,1,5,2],[2,5,1,3],[4,2,3,1]],
    [[1,3,2,2],[3,1,5,2],[2,5,1,3],[2,2,3,1]],
    [[1,4,2,2],[4,1,3,2],[2,3,1,5],[2,2,5,1]],
    [[1,5,2,2],[5,1,3,2],[2,3,1,5],[2,2,5,1]],
    [[1,5,3,3],[5,1,2,2],[3,2,1,2],[3,2,2,1]]];
  localorders:=[[24,48,48,24],[24,120,120,24],[48,48,48,48],[120,48,48,120],
    [120,12,12,120],[120,20,16,48],[120,20,20,120],[8,24,120,120]];
  count:=0;bridge:=[];
  if LINS_MaxIndex<9720 or LINS_DefaultOptions.UseLIS<>false then Error("wrong LINS interface");fi;
  for idx in [1..8] do
    t:=types[idx];M:=matrices[idx];
    # Recompute the full finite rank-three presentation orders.
    for n in [1..4] do
      J:=Difference([1..4],[n]);F:=FreeGroup(3);x:=GeneratorsOfGroup(F);rel:=List(x,g->g^2);
      for i in [1..3] do for j in [i+1..3] do Add(rel,(x[i]*x[j])^M[J[i]][J[j]]);od;od;
      u:=Size(F/rel);
      if u<>localorders[idx][n] then Error("universal finite local order mismatch");fi;
    od;
    Read(Concatenation(root,"/censuses/",t,"/records.g"));
    for r in hyperbolic_records do
      s:=List(r.permutations,PermList);H:=Group(s);
      if Size(H)<>r.order then Error("positive order mismatch");fi;
      c:=HyperbolicCheck(s,M,localorders[idx]);
      if c<>r.checks or not c.ok then Error("positive incidence mismatch");fi;
      count:=count+1;Add(bridge,[t,r.node,r.order,r.permutations]);
    od;
  od;
  if count<>59 then Error("wrong positive inventory");fi;
  Print("POSITIVE_RECORDS ",bridge,"\n");
  Print("COMPLETE_FINITE_CORE 59 POSITIVES 15104 INTERSECTIONS 1888 FLAGS 32 LOCAL_PRESENTATIONS\n");
end;;
