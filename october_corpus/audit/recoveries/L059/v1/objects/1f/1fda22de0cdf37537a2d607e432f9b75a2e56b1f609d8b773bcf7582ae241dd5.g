# Exact rank-two marked-geometry census for explicitly constructed graphs.
# This is a new bounded census, not a replay of the unrecovered historical lists.
LoadPackage("grape");;
SetAssertionLevel(1);;

P177Graph := function(label, n, black, edges)
  local E, graph, white;
  E := Set(List(edges, Set));
  white := Difference([1..n], black);
  Assert(1, ForAll(E,e->Length(e)=2 and Length(Intersection(e,black))=1));
  graph := Graph(Group(()), [1..n], OnPoints, function(a,b) return Set([a,b]) in E; end, true);
  Assert(1, IsConnectedGraph(graph));
  return rec(label:=label,n:=n,black:=Set(black),white:=white,edges:=E,graph:=graph);
end;;

P177Max := function(upper,lower)
  local degree, action;
  degree := Index(upper,lower);
  Assert(1,degree>1);
  action := Action(upper,RightCosets(upper,lower),OnRight);
  if Transitivity(action,[1..degree])>=2 then return "2T"; fi;
  if IsPrimitive(action,[1..degree]) then return "M"; fi;
  return "X";
end;;

P177Census := function(data)
  local A, F, classes, edge, b, w, witnesses, H, H0, H1, B, D, duals,
        row, cls, maxcode, normcode, maxorder, dualorder, suborders;
  A := AutGroupGraph(data.graph,[data.black,data.white]);
  F := AutGroupGraph(data.graph);
  Assert(1,IsTransitive(A,data.edges,OnSets));
  edge := data.edges[1];
  b := Intersection(edge,data.black)[1]; w := Intersection(edge,data.white)[1];
  classes := ConjugacyClassesSubgroups(A);
  witnesses := [];
  for cls in classes do
    H := Representative(cls);
    if IsTransitive(H,data.edges,OnSets) then
      H0 := Stabilizer(H,b); H1 := Stabilizer(H,w); B := Intersection(H0,H1);
      Assert(1,Size(ClosureGroup(H0,H1))=Size(H));
      Assert(1,Size(Core(H,B))=1);
      Assert(1,Index(H,B)=Length(data.edges));
      maxcode := List([[H0,B],[H1,B],[H,H0],[H,H1]],p->P177Max(p[1],p[2]));
      normcode := List([H,H0,H1,B],K->IsNormal(A,K));
      D := Stabilizer(Normalizer(F,H),edge,OnSets);
      duals := Filtered(Elements(D),g->b^g=w);
      if IsEmpty(duals) then dualorder:=0; else dualorder:=Minimum(List(duals,Order)); fi;
      maxorder := Maximum(List(ConjugacyClasses(H),c->Order(Representative(c))));
      row := rec(H:=H,H0:=H0,H1:=H1,B:=B,maxcode:=maxcode,normcode:=normcode,
                 dualorder:=dualorder,maxorder:=maxorder,
                 group_order:=Size(H),subgroup_orders:=List([H0,H1,B],Size),
                 structure:=List([H,H0,H1,B],StructureDescription));
      Add(witnesses,row);
    fi;
  od;
  Print(data.label," vertices=",data.n," edges=",Length(data.edges)," Aut+=",Size(A),
        " Aut=",Size(F)," subgroup_classes=",Length(classes)," geometries=",Length(witnesses),"\n");
  Print("MAX ",Collected(List(witnesses,r->r.maxcode)),"\n");
  Print("NORM ",Collected(List(witnesses,r->r.normcode)),"\n");
  return rec(label:=data.label,n:=data.n,black:=data.black,white:=data.white,edges:=data.edges,
             A:=A,F:=F,base_edge:=edge,b:=b,w:=w,subgroup_classes:=Length(classes),witnesses:=witnesses);
end;;

P177Inputs := [];;
Add(P177Inputs,P177Graph("K3_3",6,[1..3],Cartesian([1..3],[4..6])));;
Add(P177Inputs,P177Graph("K4_4",8,[1..4],Cartesian([1..4],[5..8])));;
P177Cube := Cartesian([0,1],[0,1],[0,1]);;
P177Edges := Filtered(Combinations([1..8],2),e->Number([1..3],i->P177Cube[e[1]][i]<>P177Cube[e[2]][i])=1);;
Add(P177Inputs,P177Graph("cube",8,Filtered([1..8],i->Sum(P177Cube[i]) mod 2=0),P177Edges));;
P177Edges := Filtered(Cartesian([1..7],[8..14]),e->((e[1]-1)-(e[2]-8)) mod 7 in [0,1,3]);;
Add(P177Inputs,P177Graph("Heawood",14,[1..7],P177Edges));;
P177Pairs := Combinations([1..5],2);;
P177Original := Filtered(Combinations([1..10],2),e->IsEmpty(Intersection(P177Pairs[e[1]],P177Pairs[e[2]])));;
P177Edges := Concatenation(List([1..15],i->List(P177Original[i],v->[v,10+i])));;
Add(P177Inputs,P177Graph("Petersen_subdivision",25,[1..10],P177Edges));;
P177Results := List(P177Inputs,P177Census);;
PrintTo("phase177_graph_witnesses.g","P177Results := ",P177Results,";\n");
Print("PHASE177_BOUNDED_CENSUS_COMPLETE\n");
QUIT;
