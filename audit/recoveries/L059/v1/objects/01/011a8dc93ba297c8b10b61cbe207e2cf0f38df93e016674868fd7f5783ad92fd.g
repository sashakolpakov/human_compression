Need:=function(ok) if not ok then Error("L059 cutoff probe invalid"); fi; end;;
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


D:=P177Graph("140_011",140,[1, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 18, 21, 42, 45, 47, 50, 53, 54, 55, 56, 59, 60, 61, 62, 64, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 95, 96, 97, 99, 101, 102, 106, 107, 130, 131, 132, 133, 134, 135, 136, 137, 138],[[1, 2], [1, 3], [1, 4], [1, 5], [2, 6], [2, 7], [2, 8], [3, 9], [3, 11], [3, 13], [4, 10], [4, 12], [4, 14], [5, 15], [5, 18], [5, 21], [6, 16], [6, 19], [6, 22], [7, 17], [7, 20], [7, 23], [8, 24], [8, 29], [8, 34], [9, 25], [9, 30], [9, 35], [10, 26], [10, 31], [10, 36], [11, 27], [11, 32], [11, 37], [12, 28], [12, 33], [12, 38], [13, 39], [13, 51], [13, 57], [14, 40], [14, 52], [14, 58], [15, 41], [15, 43], [15, 44], [16, 42], [16, 53], [16, 59], [17, 45], [17, 54], [17, 60], [18, 46], [18, 48], [18, 49], [19, 47], [19, 55], [19, 61], [20, 50], [20, 56], [20, 62], [21, 63], [21, 65], [21, 66], [22, 64], [22, 77], [22, 82], [23, 67], [23, 78], [23, 83], [24, 68], [24, 70], [24, 71], [25, 60], [25, 69], [25, 71], [26, 64], [26, 79], [26, 84], [27, 59], [27, 68], [27, 80], [28, 72], [28, 78], [28, 85], [29, 73], [29, 74], [29, 75], [30, 64], [30, 81], [30, 86], [31, 62], [31, 69], [31, 75], [32, 76], [32, 78], [32, 87], [33, 61], [33, 73], [33, 80], [34, 88], [34, 89], [34, 90], [35, 47], [35, 101], [35, 106], [36, 42], [36, 102], [36, 107], [37, 56], [37, 91], [37, 107], [38, 54], [38, 92], [38, 106], [39, 45], [39, 53], [39, 95], [40, 89], [40, 93], [40, 96], [41, 47], [41, 85], [41, 96], [42, 44], [42, 94], [43, 69], [43, 83], [43, 90], [44, 87], [44, 99], [45, 103], [45, 108], [46, 56], [46, 84], [46, 93], [47, 104], [48, 80], [48, 82], [48, 88], [49, 54], [49, 86], [49, 97], [50, 52], [50, 98], [50, 109], [51, 89], [51, 97], [51, 99], [52, 55], [52, 95], [53, 105], [53, 110], [54, 94], [55, 100], [55, 111], [56, 104], [57, 74], [57, 92], [57, 102], [58, 70], [58, 91], [58, 101], [59, 122], [59, 126], [60, 123], [60, 127], [61, 112], [61, 127], [62, 113], [62, 126], [63, 72], [63, 74], [63, 79], [64, 116], [65, 67], [65, 77], [65, 95], [66, 70], [66, 76], [66, 81], [67, 114], [67, 117], [68, 109], [68, 117], [69, 115], [70, 94], [71, 111], [71, 120], [72, 98], [72, 124], [73, 108], [73, 114], [74, 104], [75, 110], [75, 118], [76, 103], [76, 119], [77, 118], [77, 120], [78, 116], [79, 100], [79, 125], [80, 115], [81, 105], [81, 121], [82, 113], [82, 123], [83, 112], [83, 122], [84, 112], [84, 129], [85, 113], [85, 128], [86, 122], [86, 128], [87, 123], [87, 129], [88, 98], [88, 103], [89, 116], [90, 100], [90, 105], [91, 108], [91, 124], [92, 109], [92, 119], [93, 114], [93, 119], [94, 130], [95, 115], [96, 118], [96, 121], [97, 117], [97, 124], [98, 133], [99, 120], [99, 125], [100, 131], [101, 110], [101, 125], [102, 111], [102, 121], [103, 134], [104, 130], [105, 132], [106, 126], [106, 129], [107, 127], [107, 128], [108, 136], [109, 135], [110, 135], [111, 136], [112, 133], [113, 131], [114, 131], [115, 130], [116, 130], [117, 132], [118, 133], [119, 138], [120, 134], [121, 137], [122, 134], [123, 132], [124, 137], [125, 138], [126, 136], [127, 135], [128, 138], [129, 137], [131, 140], [132, 139], [133, 139], [134, 140], [135, 140], [136, 139], [137, 140], [138, 139]]);;
R:=P177Census(D);;
Need(Size(R.F)=20160);;
PrintTo("quartic_cutoff_probe/140_011.g","L059Result := ",R,";\n");
Print("L059_CUTOFF_COMPLETE 140_011 ",Length(R.witnesses),"\n");
QUIT;
