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
D:=P177Graph("144_072",144,[1, 6, 7, 8, 9, 10, 11, 12, 13, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144],[[1, 2], [1, 3], [1, 4], [1, 5], [2, 133], [2, 137], [2, 138], [3, 134], [3, 139], [3, 140], [4, 136], [4, 142], [4, 143], [5, 135], [5, 141], [5, 144], [6, 14], [6, 16], [6, 17], [6, 18], [7, 15], [7, 21], [7, 22], [7, 23], [8, 19], [8, 27], [8, 28], [8, 29], [9, 20], [9, 24], [9, 25], [9, 26], [10, 32], [10, 36], [10, 38], [10, 40], [11, 33], [11, 37], [11, 39], [11, 41], [12, 31], [12, 34], [12, 42], [12, 45], [13, 30], [13, 35], [13, 43], [13, 44], [14, 46], [14, 62], [14, 70], [15, 47], [15, 63], [15, 70], [16, 59], [16, 67], [16, 73], [17, 61], [17, 68], [17, 77], [18, 60], [18, 69], [18, 76], [19, 48], [19, 63], [19, 72], [20, 49], [20, 62], [20, 72], [21, 50], [21, 64], [21, 73], [22, 56], [22, 65], [22, 77], [23, 55], [23, 66], [23, 76], [24, 52], [24, 67], [24, 71], [25, 54], [25, 69], [25, 75], [26, 53], [26, 68], [26, 74], [27, 51], [27, 64], [27, 71], [28, 57], [28, 66], [28, 75], [29, 58], [29, 65], [29, 74], [30, 49], [30, 58], [30, 81], [31, 49], [31, 57], [31, 80], [32, 52], [32, 58], [32, 82], [33, 52], [33, 57], [33, 83], [34, 46], [34, 55], [34, 85], [35, 46], [35, 56], [35, 84], [36, 47], [36, 60], [36, 85], [37, 47], [37, 61], [37, 84], [38, 48], [38, 54], [38, 80], [39, 48], [39, 53], [39, 81], [40, 56], [40, 59], [40, 79], [41, 55], [41, 59], [41, 78], [42, 50], [42, 61], [42, 79], [43, 50], [43, 60], [43, 78], [44, 51], [44, 54], [44, 83], [45, 51], [45, 53], [45, 82], [46, 125], [47, 121], [48, 128], [49, 119], [50, 120], [51, 124], [52, 118], [53, 129], [54, 130], [55, 123], [56, 122], [57, 132], [58, 131], [59, 117], [60, 127], [61, 126], [62, 120], [62, 124], [63, 117], [63, 118], [64, 119], [64, 125], [65, 127], [65, 130], [66, 126], [66, 129], [67, 121], [67, 128], [68, 123], [68, 132], [69, 122], [69, 131], [70, 105], [70, 113], [71, 107], [71, 113], [72, 106], [72, 114], [73, 108], [73, 114], [74, 109], [74, 116], [75, 110], [75, 115], [76, 112], [76, 116], [77, 111], [77, 115], [78, 100], [78, 102], [79, 99], [79, 101], [80, 100], [80, 103], [81, 99], [81, 104], [82, 98], [82, 102], [83, 97], [83, 101], [84, 98], [84, 103], [85, 97], [85, 104], [86, 118], [86, 119], [86, 129], [86, 130], [87, 120], [87, 121], [87, 122], [87, 123], [88, 124], [88, 128], [88, 131], [88, 132], [89, 117], [89, 125], [89, 126], [89, 127], [90, 113], [90, 114], [90, 115], [90, 116], [91, 103], [91, 104], [91, 105], [91, 106], [92, 101], [92, 102], [92, 107], [92, 108], [93, 97], [93, 100], [93, 110], [93, 112], [94, 98], [94, 99], [94, 109], [94, 111], [95, 105], [95, 108], [95, 111], [95, 112], [96, 106], [96, 107], [96, 109], [96, 110], [97, 133], [98, 133], [99, 134], [100, 134], [101, 136], [102, 135], [103, 136], [104, 135], [105, 139], [106, 137], [107, 140], [108, 138], [109, 142], [110, 141], [111, 144], [112, 143], [113, 133], [114, 134], [115, 136], [116, 135], [117, 140], [118, 138], [119, 139], [120, 140], [121, 137], [122, 142], [123, 141], [124, 138], [125, 137], [126, 142], [127, 141], [128, 139], [129, 144], [130, 143], [131, 144], [132, 143]]);;
R:=P177Census(D);;Need(Size(R.F)=2304);;
PrintTo("current_c4_descent/144_072.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_072 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
