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
D:=P177Graph("144_008",144,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132, 134, 136, 138, 140, 142, 144],[[1, 2], [1, 72], [1, 73], [1, 111], [2, 3], [2, 74], [2, 112], [3, 4], [3, 75], [3, 113], [4, 5], [4, 76], [4, 114], [5, 6], [5, 77], [5, 115], [6, 7], [6, 78], [6, 116], [7, 8], [7, 79], [7, 117], [8, 9], [8, 80], [8, 118], [9, 10], [9, 81], [9, 119], [10, 11], [10, 82], [10, 120], [11, 12], [11, 83], [11, 121], [12, 13], [12, 84], [12, 122], [13, 14], [13, 85], [13, 123], [14, 15], [14, 86], [14, 124], [15, 16], [15, 87], [15, 125], [16, 17], [16, 88], [16, 126], [17, 18], [17, 89], [17, 127], [18, 19], [18, 90], [18, 128], [19, 20], [19, 91], [19, 129], [20, 21], [20, 92], [20, 130], [21, 22], [21, 93], [21, 131], [22, 23], [22, 94], [22, 132], [23, 24], [23, 95], [23, 133], [24, 25], [24, 96], [24, 134], [25, 26], [25, 97], [25, 135], [26, 27], [26, 98], [26, 136], [27, 28], [27, 99], [27, 137], [28, 29], [28, 100], [28, 138], [29, 30], [29, 101], [29, 139], [30, 31], [30, 102], [30, 140], [31, 32], [31, 103], [31, 141], [32, 33], [32, 104], [32, 142], [33, 34], [33, 105], [33, 143], [34, 35], [34, 106], [34, 144], [35, 36], [35, 73], [35, 107], [36, 37], [36, 74], [36, 108], [37, 38], [37, 75], [37, 109], [38, 39], [38, 76], [38, 110], [39, 40], [39, 77], [39, 111], [40, 41], [40, 78], [40, 112], [41, 42], [41, 79], [41, 113], [42, 43], [42, 80], [42, 114], [43, 44], [43, 81], [43, 115], [44, 45], [44, 82], [44, 116], [45, 46], [45, 83], [45, 117], [46, 47], [46, 84], [46, 118], [47, 48], [47, 85], [47, 119], [48, 49], [48, 86], [48, 120], [49, 50], [49, 87], [49, 121], [50, 51], [50, 88], [50, 122], [51, 52], [51, 89], [51, 123], [52, 53], [52, 90], [52, 124], [53, 54], [53, 91], [53, 125], [54, 55], [54, 92], [54, 126], [55, 56], [55, 93], [55, 127], [56, 57], [56, 94], [56, 128], [57, 58], [57, 95], [57, 129], [58, 59], [58, 96], [58, 130], [59, 60], [59, 97], [59, 131], [60, 61], [60, 98], [60, 132], [61, 62], [61, 99], [61, 133], [62, 63], [62, 100], [62, 134], [63, 64], [63, 101], [63, 135], [64, 65], [64, 102], [64, 136], [65, 66], [65, 103], [65, 137], [66, 67], [66, 104], [66, 138], [67, 68], [67, 105], [67, 139], [68, 69], [68, 106], [68, 140], [69, 70], [69, 107], [69, 141], [70, 71], [70, 108], [70, 142], [71, 72], [71, 109], [71, 143], [72, 110], [72, 144], [73, 74], [73, 144], [74, 75], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80], [80, 81], [81, 82], [82, 83], [83, 84], [84, 85], [85, 86], [86, 87], [87, 88], [88, 89], [89, 90], [90, 91], [91, 92], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108], [108, 109], [109, 110], [110, 111], [111, 112], [112, 113], [113, 114], [114, 115], [115, 116], [116, 117], [117, 118], [118, 119], [119, 120], [120, 121], [121, 122], [122, 123], [123, 124], [124, 125], [125, 126], [126, 127], [127, 128], [128, 129], [129, 130], [130, 131], [131, 132], [132, 133], [133, 134], [134, 135], [135, 136], [136, 137], [137, 138], [138, 139], [139, 140], [140, 141], [141, 142], [142, 143], [143, 144]]);;
R:=P177Census(D);;Need(Size(R.F)=576);;
PrintTo("current_c4_descent/144_008.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_008 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
