LoadPackage("grape");;
SetAssertionLevel(1);;

P177Hexagon := function(tips, expected)
  local n, edges, j, i, gr, colors, A, C, gen, cls, reflection;
  n:=6+Length(tips);
  edges:=List([0..5],i->Set([i+1,((i+1) mod 6)+1]));
  for j in [1..Length(tips)] do
    i:=tips[j];
    Add(edges,Set([i+1,6+j]));
    Add(edges,Set([((i+1) mod 6)+1,6+j]));
  od;
  gr:=Graph(Group(()),[1..n],OnPoints,
    function(a,b) return Set([a,b]) in edges; end,true);
  colors:=[[1,3,5],[2,4,6],[7..n]];
  A:=AutGroupGraph(gr,colors);
  C:=AutGroupGraph(gr);
  for gen in GeneratorsOfGroup(C) do
    for cls in colors do Assert(1,OnSets(cls,gen) in colors); od;
  od;
  Assert(1,[Size(C),Size(A)]=expected);
  Print("HEXAGON tips=",tips," correlation_order=",Size(C),
    " type_preserving_order=",Size(A)," groups=",
    StructureDescription(C),"/",StructureDescription(A),"\n");
  if Length(tips)=6 then
    reflection:=PermList(Concatenation(
      List([0..5],i->(-i mod 6)+1),
      List([0..5],i->((-i-1) mod 6)+7)));
    Assert(1,reflection in A and Order(reflection)=2);
    Print("TYPE_PRESERVING_REFLECTION ",reflection,"\n");
  fi;
end;;

P177Hexagon([0,2,4],[6,3]);;
P177Hexagon([0..5],[12,6]);;
Print("PHASE177_HEXAGON_CHECK_COMPLETE\n");
QUIT;
