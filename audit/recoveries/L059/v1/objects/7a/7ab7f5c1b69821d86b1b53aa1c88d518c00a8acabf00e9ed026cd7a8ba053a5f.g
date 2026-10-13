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
D:=P177Graph("140_004",140,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132, 134, 136, 138, 140],[[1, 2], [1, 70], [1, 71], [1, 129], [2, 3], [2, 72], [2, 130], [3, 4], [3, 73], [3, 131], [4, 5], [4, 74], [4, 132], [5, 6], [5, 75], [5, 133], [6, 7], [6, 76], [6, 134], [7, 8], [7, 77], [7, 135], [8, 9], [8, 78], [8, 136], [9, 10], [9, 79], [9, 137], [10, 11], [10, 80], [10, 138], [11, 12], [11, 81], [11, 139], [12, 13], [12, 82], [12, 140], [13, 14], [13, 71], [13, 83], [14, 15], [14, 72], [14, 84], [15, 16], [15, 73], [15, 85], [16, 17], [16, 74], [16, 86], [17, 18], [17, 75], [17, 87], [18, 19], [18, 76], [18, 88], [19, 20], [19, 77], [19, 89], [20, 21], [20, 78], [20, 90], [21, 22], [21, 79], [21, 91], [22, 23], [22, 80], [22, 92], [23, 24], [23, 81], [23, 93], [24, 25], [24, 82], [24, 94], [25, 26], [25, 83], [25, 95], [26, 27], [26, 84], [26, 96], [27, 28], [27, 85], [27, 97], [28, 29], [28, 86], [28, 98], [29, 30], [29, 87], [29, 99], [30, 31], [30, 88], [30, 100], [31, 32], [31, 89], [31, 101], [32, 33], [32, 90], [32, 102], [33, 34], [33, 91], [33, 103], [34, 35], [34, 92], [34, 104], [35, 36], [35, 93], [35, 105], [36, 37], [36, 94], [36, 106], [37, 38], [37, 95], [37, 107], [38, 39], [38, 96], [38, 108], [39, 40], [39, 97], [39, 109], [40, 41], [40, 98], [40, 110], [41, 42], [41, 99], [41, 111], [42, 43], [42, 100], [42, 112], [43, 44], [43, 101], [43, 113], [44, 45], [44, 102], [44, 114], [45, 46], [45, 103], [45, 115], [46, 47], [46, 104], [46, 116], [47, 48], [47, 105], [47, 117], [48, 49], [48, 106], [48, 118], [49, 50], [49, 107], [49, 119], [50, 51], [50, 108], [50, 120], [51, 52], [51, 109], [51, 121], [52, 53], [52, 110], [52, 122], [53, 54], [53, 111], [53, 123], [54, 55], [54, 112], [54, 124], [55, 56], [55, 113], [55, 125], [56, 57], [56, 114], [56, 126], [57, 58], [57, 115], [57, 127], [58, 59], [58, 116], [58, 128], [59, 60], [59, 117], [59, 129], [60, 61], [60, 118], [60, 130], [61, 62], [61, 119], [61, 131], [62, 63], [62, 120], [62, 132], [63, 64], [63, 121], [63, 133], [64, 65], [64, 122], [64, 134], [65, 66], [65, 123], [65, 135], [66, 67], [66, 124], [66, 136], [67, 68], [67, 125], [67, 137], [68, 69], [68, 126], [68, 138], [69, 70], [69, 127], [69, 139], [70, 128], [70, 140], [71, 72], [71, 140], [72, 73], [73, 74], [74, 75], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80], [80, 81], [81, 82], [82, 83], [83, 84], [84, 85], [85, 86], [86, 87], [87, 88], [88, 89], [89, 90], [90, 91], [91, 92], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108], [108, 109], [109, 110], [110, 111], [111, 112], [112, 113], [113, 114], [114, 115], [115, 116], [116, 117], [117, 118], [118, 119], [119, 120], [120, 121], [121, 122], [122, 123], [123, 124], [124, 125], [125, 126], [126, 127], [127, 128], [128, 129], [129, 130], [130, 131], [131, 132], [132, 133], [133, 134], [134, 135], [135, 136], [136, 137], [137, 138], [138, 139], [139, 140]]);;
R:=P177Census(D);;Need(Size(R.F)=560);;
PrintTo("current_c4_descent/140_004.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 140_004 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
