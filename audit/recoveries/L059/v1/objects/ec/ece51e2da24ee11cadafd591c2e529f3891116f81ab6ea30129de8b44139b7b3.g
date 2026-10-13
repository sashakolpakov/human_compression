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
D:=P177Graph("084_007",84,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70],[[1, 15], [1, 28], [1, 76], [1, 79], [2, 15], [2, 16], [2, 77], [2, 80], [3, 16], [3, 17], [3, 78], [3, 81], [4, 17], [4, 18], [4, 79], [4, 82], [5, 18], [5, 19], [5, 80], [5, 83], [6, 19], [6, 20], [6, 81], [6, 84], [7, 20], [7, 21], [7, 71], [7, 82], [8, 21], [8, 22], [8, 72], [8, 83], [9, 22], [9, 23], [9, 73], [9, 84], [10, 23], [10, 24], [10, 71], [10, 74], [11, 24], [11, 25], [11, 72], [11, 75], [12, 25], [12, 26], [12, 73], [12, 76], [13, 26], [13, 27], [13, 74], [13, 77], [14, 27], [14, 28], [14, 75], [14, 78], [15, 32], [15, 41], [16, 33], [16, 42], [17, 29], [17, 34], [18, 30], [18, 35], [19, 31], [19, 36], [20, 32], [20, 37], [21, 33], [21, 38], [22, 34], [22, 39], [23, 35], [23, 40], [24, 36], [24, 41], [25, 37], [25, 42], [26, 29], [26, 38], [27, 30], [27, 39], [28, 31], [28, 40], [29, 44], [29, 55], [30, 45], [30, 56], [31, 43], [31, 46], [32, 44], [32, 47], [33, 45], [33, 48], [34, 46], [34, 49], [35, 47], [35, 50], [36, 48], [36, 51], [37, 49], [37, 52], [38, 50], [38, 53], [39, 51], [39, 54], [40, 52], [40, 55], [41, 53], [41, 56], [42, 43], [42, 54], [43, 64], [43, 65], [44, 65], [44, 66], [45, 66], [45, 67], [46, 67], [46, 68], [47, 68], [47, 69], [48, 69], [48, 70], [49, 57], [49, 70], [50, 57], [50, 58], [51, 58], [51, 59], [52, 59], [52, 60], [53, 60], [53, 61], [54, 61], [54, 62], [55, 62], [55, 63], [56, 63], [56, 64], [57, 75], [57, 80], [58, 76], [58, 81], [59, 77], [59, 82], [60, 78], [60, 83], [61, 79], [61, 84], [62, 71], [62, 80], [63, 72], [63, 81], [64, 73], [64, 82], [65, 74], [65, 83], [66, 75], [66, 84], [67, 71], [67, 76], [68, 72], [68, 77], [69, 73], [69, 78], [70, 74], [70, 79]]);;
R:=P177Census(D);;Need(Size(R.F)=1344);;
PrintTo("current_c4_descent/084_007.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 084_007 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
