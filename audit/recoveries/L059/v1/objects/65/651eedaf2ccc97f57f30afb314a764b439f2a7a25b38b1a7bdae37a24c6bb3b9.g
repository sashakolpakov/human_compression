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
D:=P177Graph("084_019",84,[1, 4, 6, 7, 10, 11, 12, 15, 17, 18, 19, 23, 27, 28, 30, 34, 39, 40, 41, 43, 44, 45, 47, 48, 50, 52, 56, 57, 59, 60, 61, 63, 64, 66, 67, 70, 73, 76, 77, 78, 81, 84],[[1, 2], [1, 3], [1, 5], [1, 8], [2, 4], [2, 7], [2, 12], [3, 6], [3, 11], [3, 18], [4, 9], [4, 16], [4, 26], [5, 10], [5, 17], [5, 27], [6, 13], [6, 24], [6, 37], [7, 14], [7, 25], [7, 38], [8, 15], [8, 23], [8, 39], [9, 19], [9, 34], [9, 52], [10, 20], [10, 32], [10, 35], [11, 21], [11, 36], [11, 53], [12, 22], [12, 33], [12, 54], [13, 19], [13, 47], [13, 66], [14, 28], [14, 45], [14, 48], [15, 22], [15, 29], [15, 49], [16, 30], [16, 50], [16, 67], [17, 31], [17, 46], [17, 51], [18, 32], [18, 46], [18, 54], [19, 62], [19, 74], [20, 28], [20, 47], [20, 70], [21, 40], [21, 60], [21, 63], [22, 41], [22, 64], [23, 33], [23, 42], [23, 65], [24, 41], [24, 43], [24, 78], [25, 44], [25, 60], [25, 61], [26, 39], [26, 45], [26, 61], [27, 37], [27, 53], [27, 54], [28, 62], [28, 80], [29, 34], [29, 40], [29, 57], [30, 51], [30, 55], [30, 75], [31, 50], [31, 56], [31, 63], [32, 50], [32, 76], [33, 57], [33, 77], [34, 58], [34, 82], [35, 57], [35, 59], [35, 81], [36, 44], [36, 45], [36, 73], [37, 60], [37, 73], [38, 39], [38, 52], [38, 67], [39, 54], [40, 74], [40, 83], [41, 42], [41, 55], [42, 48], [42, 56], [43, 65], [43, 68], [43, 75], [44, 69], [44, 75], [45, 79], [46, 70], [46, 81], [47, 71], [47, 82], [48, 71], [48, 72], [49, 59], [49, 70], [49, 77], [50, 68], [51, 52], [51, 76], [52, 68], [53, 66], [53, 78], [55, 66], [55, 84], [56, 80], [56, 83], [57, 69], [58, 63], [58, 73], [58, 77], [59, 75], [59, 79], [60, 79], [61, 71], [61, 80], [62, 78], [62, 81], [63, 72], [64, 65], [64, 72], [64, 80], [65, 66], [67, 74], [67, 82], [68, 84], [69, 70], [69, 84], [71, 81], [72, 76], [73, 83], [74, 77], [76, 83], [78, 82], [79, 84]]);;
R:=P177Census(D);;Need(Size(R.F)=672);;
PrintTo("current_c4_descent/084_019.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 084_019 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
