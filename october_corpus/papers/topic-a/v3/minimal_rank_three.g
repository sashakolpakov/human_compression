# All groups below the claimed minimum that survive the written order bound.
# SmallGroups classification and GAP exact group algorithms are retained inputs.
L128Check := function()
  local rows,n,id,G,inv,triple,total,pairs,gens;
  rows := [];
  for n in [40,48,56] do
    total:=0;pairs:=0;gens:=0;
    for id in [1..NumberSmallGroups(n)] do
      G:=SmallGroup(n,id);
      inv:=Filtered(Elements(G),g->Order(g)=2);
      for triple in Combinations(inv,3) do
        total:=total+1;
        if not ForAll(Combinations(triple,2),p->Order(p[1]*p[2])=4) then continue;fi;
        pairs:=pairs+1;
        if Size(Subgroup(G,triple))=n then gens:=gens+1;fi;
      od;
    od;
    if gens<>0 then Error("L128_REJECT smaller generating triple");fi;
    Add(rows,[n,NumberSmallGroups(n),total,pairs,gens]);
  od;
  if rows<>[[40,14,3764,0,0],[48,52,19498,88,0],[56,13,9366,0,0]] then
    Error("L128_REJECT exact enumeration totals");
  fi;
  Print("L128_COMPLETE_SMALL_ORDER_SEARCH ",rows,"\n");
end;
L128Check();
QUIT;
