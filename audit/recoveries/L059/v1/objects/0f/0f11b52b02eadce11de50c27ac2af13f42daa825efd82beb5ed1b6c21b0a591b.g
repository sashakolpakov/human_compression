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
D:=P177Graph("084_004",84,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84],[[1, 2], [1, 42], [1, 43], [1, 59], [2, 3], [2, 44], [2, 60], [3, 4], [3, 45], [3, 61], [4, 5], [4, 46], [4, 62], [5, 6], [5, 47], [5, 63], [6, 7], [6, 48], [6, 64], [7, 8], [7, 49], [7, 65], [8, 9], [8, 50], [8, 66], [9, 10], [9, 51], [9, 67], [10, 11], [10, 52], [10, 68], [11, 12], [11, 53], [11, 69], [12, 13], [12, 54], [12, 70], [13, 14], [13, 55], [13, 71], [14, 15], [14, 56], [14, 72], [15, 16], [15, 57], [15, 73], [16, 17], [16, 58], [16, 74], [17, 18], [17, 59], [17, 75], [18, 19], [18, 60], [18, 76], [19, 20], [19, 61], [19, 77], [20, 21], [20, 62], [20, 78], [21, 22], [21, 63], [21, 79], [22, 23], [22, 64], [22, 80], [23, 24], [23, 65], [23, 81], [24, 25], [24, 66], [24, 82], [25, 26], [25, 67], [25, 83], [26, 27], [26, 68], [26, 84], [27, 28], [27, 43], [27, 69], [28, 29], [28, 44], [28, 70], [29, 30], [29, 45], [29, 71], [30, 31], [30, 46], [30, 72], [31, 32], [31, 47], [31, 73], [32, 33], [32, 48], [32, 74], [33, 34], [33, 49], [33, 75], [34, 35], [34, 50], [34, 76], [35, 36], [35, 51], [35, 77], [36, 37], [36, 52], [36, 78], [37, 38], [37, 53], [37, 79], [38, 39], [38, 54], [38, 80], [39, 40], [39, 55], [39, 81], [40, 41], [40, 56], [40, 82], [41, 42], [41, 57], [41, 83], [42, 58], [42, 84], [43, 44], [43, 84], [44, 45], [45, 46], [46, 47], [47, 48], [48, 49], [49, 50], [50, 51], [51, 52], [52, 53], [53, 54], [54, 55], [55, 56], [56, 57], [57, 58], [58, 59], [59, 60], [60, 61], [61, 62], [62, 63], [63, 64], [64, 65], [65, 66], [66, 67], [67, 68], [68, 69], [69, 70], [70, 71], [71, 72], [72, 73], [73, 74], [74, 75], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80], [80, 81], [81, 82], [82, 83], [83, 84]]);;
R:=P177Census(D);;Need(Size(R.F)=336);;
PrintTo("current_c4_descent/084_004.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 084_004 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
