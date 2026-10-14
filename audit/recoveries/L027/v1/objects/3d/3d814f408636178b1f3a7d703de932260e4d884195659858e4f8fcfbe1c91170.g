Need:=function(ok,msg)if not ok then Error(msg);fi;end;
for p in [3,5,7] do
 F:=GF(p);o:=One(F);z:=Zero(F);D:=[DiagonalMat([o,-o,-o]),DiagonalMat([-o,o,-o]),DiagonalMat([-o,-o,o])];
 cases:=[ ["one",[[o,z,z],[o,-o,z],[z,z,-o]]], ["product",[[o,z,z],[o,-o,z],[o,z,-o]]], ["heis",[[o,-2*o,z],[z,-o,z],[o,-o,-o]]]];
 lines:=[];for x in F do for y in F do Add(lines,[o,x,y]);od;od;for x in F do Add(lines,[z,o,x]);od;Add(lines,[z,z,o]);
 for case in cases do
  ps:=List(Concatenation(D,[case[2]]),m->Permutation(m,lines,OnLines));
  for es in Combinations([1,2,3],2) do
   gs:=[ps[es[1]],ps[4],ps[es[2]]];G:=Group(gs);A:=Group(gs{[1,2]});B:=Group(gs{[2,3]});
   Print(p," ",case[1]," ",es," order=",Size(G)," type=",Order(gs[1]*gs[2]),",",Order(gs[2]*gs[3])," intersection=",Size(Intersection(A,B)),"\n");
  od;
 od;
od;QUIT;
