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
D:=P177Graph("064_013",64,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 34, 36, 38, 40, 42, 44, 46, 48, 49, 51, 53, 55, 57, 59, 61, 63],[[1, 2], [1, 16], [1, 26], [1, 33], [2, 3], [2, 27], [2, 34], [3, 4], [3, 28], [3, 35], [4, 5], [4, 29], [4, 36], [5, 6], [5, 30], [5, 37], [6, 7], [6, 31], [6, 38], [7, 8], [7, 32], [7, 39], [8, 9], [8, 17], [8, 40], [9, 10], [9, 18], [9, 41], [10, 11], [10, 19], [10, 42], [11, 12], [11, 20], [11, 43], [12, 13], [12, 21], [12, 44], [13, 14], [13, 22], [13, 45], [14, 15], [14, 23], [14, 46], [15, 16], [15, 24], [15, 47], [16, 25], [16, 48], [17, 33], [17, 35], [17, 60], [18, 34], [18, 36], [18, 61], [19, 35], [19, 37], [19, 62], [20, 36], [20, 38], [20, 63], [21, 37], [21, 39], [21, 64], [22, 38], [22, 40], [22, 49], [23, 39], [23, 41], [23, 50], [24, 40], [24, 42], [24, 51], [25, 41], [25, 43], [25, 52], [26, 42], [26, 44], [26, 53], [27, 43], [27, 45], [27, 54], [28, 44], [28, 46], [28, 55], [29, 45], [29, 47], [29, 56], [30, 46], [30, 48], [30, 57], [31, 33], [31, 47], [31, 58], [32, 34], [32, 48], [32, 59], [33, 49], [34, 50], [35, 51], [36, 52], [37, 53], [38, 54], [39, 55], [40, 56], [41, 57], [42, 58], [43, 59], [44, 60], [45, 61], [46, 62], [47, 63], [48, 64], [49, 50], [49, 64], [50, 51], [51, 52], [52, 53], [53, 54], [54, 55], [55, 56], [56, 57], [57, 58], [58, 59], [59, 60], [60, 61], [61, 62], [62, 63], [63, 64]]);;
R:=P177Census(D);;Need(Size(R.F)=512);;
PrintTo("current_c4_descent/064_013.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 064_013 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
