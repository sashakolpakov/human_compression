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
D:=P177Graph("084_003",84,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83],[[1, 2], [1, 30], [1, 56], [1, 84], [2, 3], [2, 31], [2, 57], [3, 4], [3, 32], [3, 58], [4, 5], [4, 33], [4, 59], [5, 6], [5, 34], [5, 60], [6, 7], [6, 35], [6, 61], [7, 8], [7, 36], [7, 62], [8, 9], [8, 37], [8, 63], [9, 10], [9, 38], [9, 64], [10, 11], [10, 39], [10, 65], [11, 12], [11, 40], [11, 66], [12, 13], [12, 41], [12, 67], [13, 14], [13, 42], [13, 68], [14, 15], [14, 43], [14, 69], [15, 16], [15, 44], [15, 70], [16, 17], [16, 45], [16, 71], [17, 18], [17, 46], [17, 72], [18, 19], [18, 47], [18, 73], [19, 20], [19, 48], [19, 74], [20, 21], [20, 49], [20, 75], [21, 22], [21, 50], [21, 76], [22, 23], [22, 51], [22, 77], [23, 24], [23, 52], [23, 78], [24, 25], [24, 53], [24, 79], [25, 26], [25, 54], [25, 80], [26, 27], [26, 55], [26, 81], [27, 28], [27, 56], [27, 82], [28, 29], [28, 57], [28, 83], [29, 30], [29, 58], [29, 84], [30, 31], [30, 59], [31, 32], [31, 60], [32, 33], [32, 61], [33, 34], [33, 62], [34, 35], [34, 63], [35, 36], [35, 64], [36, 37], [36, 65], [37, 38], [37, 66], [38, 39], [38, 67], [39, 40], [39, 68], [40, 41], [40, 69], [41, 42], [41, 70], [42, 43], [42, 71], [43, 44], [43, 72], [44, 45], [44, 73], [45, 46], [45, 74], [46, 47], [46, 75], [47, 48], [47, 76], [48, 49], [48, 77], [49, 50], [49, 78], [50, 51], [50, 79], [51, 52], [51, 80], [52, 53], [52, 81], [53, 54], [53, 82], [54, 55], [54, 83], [55, 56], [55, 84], [56, 57], [57, 58], [58, 59], [59, 60], [60, 61], [61, 62], [62, 63], [63, 64], [64, 65], [65, 66], [66, 67], [67, 68], [68, 69], [69, 70], [70, 71], [71, 72], [72, 73], [73, 74], [74, 75], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80], [80, 81], [81, 82], [82, 83], [83, 84]]);;
R:=P177Census(D);;Need(Size(R.F)=336);;
PrintTo("current_c4_descent/084_003.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 084_003 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
