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
D:=P177Graph("084_002",84,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83],[[1, 2], [1, 14], [1, 72], [1, 84], [2, 3], [2, 15], [2, 73], [3, 4], [3, 16], [3, 74], [4, 5], [4, 17], [4, 75], [5, 6], [5, 18], [5, 76], [6, 7], [6, 19], [6, 77], [7, 8], [7, 20], [7, 78], [8, 9], [8, 21], [8, 79], [9, 10], [9, 22], [9, 80], [10, 11], [10, 23], [10, 81], [11, 12], [11, 24], [11, 82], [12, 13], [12, 25], [12, 83], [13, 14], [13, 26], [13, 84], [14, 15], [14, 27], [15, 16], [15, 28], [16, 17], [16, 29], [17, 18], [17, 30], [18, 19], [18, 31], [19, 20], [19, 32], [20, 21], [20, 33], [21, 22], [21, 34], [22, 23], [22, 35], [23, 24], [23, 36], [24, 25], [24, 37], [25, 26], [25, 38], [26, 27], [26, 39], [27, 28], [27, 40], [28, 29], [28, 41], [29, 30], [29, 42], [30, 31], [30, 43], [31, 32], [31, 44], [32, 33], [32, 45], [33, 34], [33, 46], [34, 35], [34, 47], [35, 36], [35, 48], [36, 37], [36, 49], [37, 38], [37, 50], [38, 39], [38, 51], [39, 40], [39, 52], [40, 41], [40, 53], [41, 42], [41, 54], [42, 43], [42, 55], [43, 44], [43, 56], [44, 45], [44, 57], [45, 46], [45, 58], [46, 47], [46, 59], [47, 48], [47, 60], [48, 49], [48, 61], [49, 50], [49, 62], [50, 51], [50, 63], [51, 52], [51, 64], [52, 53], [52, 65], [53, 54], [53, 66], [54, 55], [54, 67], [55, 56], [55, 68], [56, 57], [56, 69], [57, 58], [57, 70], [58, 59], [58, 71], [59, 60], [59, 72], [60, 61], [60, 73], [61, 62], [61, 74], [62, 63], [62, 75], [63, 64], [63, 76], [64, 65], [64, 77], [65, 66], [65, 78], [66, 67], [66, 79], [67, 68], [67, 80], [68, 69], [68, 81], [69, 70], [69, 82], [70, 71], [70, 83], [71, 72], [71, 84], [72, 73], [73, 74], [74, 75], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80], [80, 81], [81, 82], [82, 83], [83, 84]]);;
R:=P177Census(D);;Need(Size(R.F)=336);;
PrintTo("current_c4_descent/084_002.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 084_002 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
