LoadPackage("LINS");;
F := FreeGroup("a","b","c","d");;
x := GeneratorsOfGroup(F);;
M := [[1,3,2,4],[3,1,4,2],[2,4,1,3],[4,2,3,1]];;
rels := List(x, g -> g^2);;
for i in [1..4] do
  for j in [i+1..4] do
    if j<=4 then Add(rels,(x[i]*x[j])^M[i][j]); fi;
  od;
od;
G := F/rels;;
start := Runtime();;
Print("START_SQUARE_3434_BOUND336\n");
normals := LowIndexNormalSubgroupsSearchForAll(G,336);;
nodes := List(normals);;
Print("COMPLETE_NORMALS ",Length(nodes)," TIME_MS ",Runtime()-start,"\n");
counts := [];;
for node in nodes do
  N := Grp(node);;
  index := Index(G,N);;
  Add(counts,index);
  if index mod 48 = 0 then
    action := FactorCosetAction(G,N);;
    H := Image(action);;
    marking := List(GeneratorsOfGroup(G),g->Image(action,g));;
    orders := List([1..4],i->List([1..4],j->Order(marking[i]*marking[j])));;
    parabolic := List([1..4],i->Subgroup(H,marking{Difference([1..4],[i])}));;
    localorders := List(parabolic,Size);;
    Print("CANDIDATE ",index," PAIRS ",orders," LOCAL ",localorders,"\n");
    if orders=M and localorders=[48,48,48,48] then
      Print("MARKING ",List(marking,p->List([1..index],i->i^p)),"\n");
    fi;
  fi;
od;
Print("INDEX_MULTIPLICITIES ",Collected(counts),"\n");
Print("COMPLETE_DIAGNOSTIC\n");
QUIT;
