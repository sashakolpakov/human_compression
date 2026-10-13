Need:=function(ok) if not ok then Error("L059 descent invalid"); fi; end;;
Read("maximal_descent.g");;

# Exact rank-two marked-geometry census for explicitly constructed graphs.
# This is a new bounded census, not a replay of the unrecovered historical lists.
LoadPackage("grape");;
SetAssertionLevel(1);;

P177Graph := function(label, n, black, edges)
  local E, graph, white;
  E := Set(List(edges, Set));
  white := Difference([1..n], black);
  Need( ForAll(E,e->Length(e)=2 and Length(Intersection(e,black))=1));
  graph := Graph(Group(()), [1..n], OnPoints, function(a,b) return Set([a,b]) in E; end, true);
  Need( IsConnectedGraph(graph));
  return rec(label:=label,n:=n,black:=Set(black),white:=white,edges:=E,graph:=graph);
end;;

P177Max := function(upper,lower)
  local degree, action;
  degree := Index(upper,lower);
  Need(degree>1);
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
  Need(IsTransitive(A,data.edges,OnSets));
  edge := data.edges[1];
  b := Intersection(edge,data.black)[1]; w := Intersection(edge,data.white)[1];
  classes := L059Descent(A,data.edges);
  witnesses := [];
  for cls in classes do
    H := Representative(cls);
    if IsTransitive(H,data.edges,OnSets) then
      H0 := Stabilizer(H,b); H1 := Stabilizer(H,w); B := Intersection(H0,H1);
      Need(Size(ClosureGroup(H0,H1))=Size(H));
      Need(Size(Core(H,B))=1);
      Need(Index(H,B)=Length(data.edges));
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
             A:=A,F:=F,base_edge:=edge,b:=b,w:=w,retained_edge_transitive_classes:=Length(classes),search:=L059Search,witnesses:=witnesses);
end;;


t:=Runtime();;
D:=P177Graph("064_008",64,[1, 2, 3, 4, 5, 6, 7, 8, 17, 18, 19, 20, 21, 22, 23, 24, 33, 34, 35, 36, 37, 38, 39, 40, 49, 50, 51, 52, 53, 54, 55, 56],[[1, 9], [1, 10], [1, 57], [1, 61], [2, 11], [2, 12], [2, 57], [2, 61], [3, 13], [3, 14], [3, 58], [3, 62], [4, 15], [4, 16], [4, 58], [4, 62], [5, 9], [5, 10], [5, 59], [5, 63], [6, 11], [6, 12], [6, 59], [6, 63], [7, 13], [7, 14], [7, 60], [7, 64], [8, 15], [8, 16], [8, 60], [8, 64], [9, 17], [9, 18], [10, 19], [10, 20], [11, 21], [11, 22], [12, 23], [12, 24], [13, 17], [13, 18], [14, 19], [14, 20], [15, 21], [15, 22], [16, 23], [16, 24], [17, 25], [17, 26], [18, 27], [18, 28], [19, 29], [19, 30], [20, 31], [20, 32], [21, 25], [21, 26], [22, 27], [22, 28], [23, 29], [23, 30], [24, 31], [24, 32], [25, 33], [25, 34], [26, 35], [26, 36], [27, 37], [27, 38], [28, 39], [28, 40], [29, 33], [29, 34], [30, 35], [30, 36], [31, 37], [31, 38], [32, 39], [32, 40], [33, 41], [33, 42], [34, 43], [34, 44], [35, 45], [35, 46], [36, 47], [36, 48], [37, 41], [37, 42], [38, 43], [38, 44], [39, 45], [39, 46], [40, 47], [40, 48], [41, 49], [41, 50], [42, 51], [42, 52], [43, 53], [43, 54], [44, 55], [44, 56], [45, 49], [45, 50], [46, 51], [46, 52], [47, 53], [47, 54], [48, 55], [48, 56], [49, 57], [49, 58], [50, 59], [50, 60], [51, 61], [51, 62], [52, 63], [52, 64], [53, 57], [53, 58], [54, 59], [54, 60], [55, 61], [55, 62], [56, 63], [56, 64]]);;
R:=P177Census(D);;Need(Size(R.F)=4096);;
PrintTo("current_c4_descent/064_008.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 064_008 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
