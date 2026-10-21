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
D:=P177Graph("148_002",148,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132, 134, 136, 138, 140, 142, 144, 146, 148],[[1, 2], [1, 74], [1, 75], [1, 87], [2, 3], [2, 76], [2, 88], [3, 4], [3, 77], [3, 89], [4, 5], [4, 78], [4, 90], [5, 6], [5, 79], [5, 91], [6, 7], [6, 80], [6, 92], [7, 8], [7, 81], [7, 93], [8, 9], [8, 82], [8, 94], [9, 10], [9, 83], [9, 95], [10, 11], [10, 84], [10, 96], [11, 12], [11, 85], [11, 97], [12, 13], [12, 86], [12, 98], [13, 14], [13, 87], [13, 99], [14, 15], [14, 88], [14, 100], [15, 16], [15, 89], [15, 101], [16, 17], [16, 90], [16, 102], [17, 18], [17, 91], [17, 103], [18, 19], [18, 92], [18, 104], [19, 20], [19, 93], [19, 105], [20, 21], [20, 94], [20, 106], [21, 22], [21, 95], [21, 107], [22, 23], [22, 96], [22, 108], [23, 24], [23, 97], [23, 109], [24, 25], [24, 98], [24, 110], [25, 26], [25, 99], [25, 111], [26, 27], [26, 100], [26, 112], [27, 28], [27, 101], [27, 113], [28, 29], [28, 102], [28, 114], [29, 30], [29, 103], [29, 115], [30, 31], [30, 104], [30, 116], [31, 32], [31, 105], [31, 117], [32, 33], [32, 106], [32, 118], [33, 34], [33, 107], [33, 119], [34, 35], [34, 108], [34, 120], [35, 36], [35, 109], [35, 121], [36, 37], [36, 110], [36, 122], [37, 38], [37, 111], [37, 123], [38, 39], [38, 112], [38, 124], [39, 40], [39, 113], [39, 125], [40, 41], [40, 114], [40, 126], [41, 42], [41, 115], [41, 127], [42, 43], [42, 116], [42, 128], [43, 44], [43, 117], [43, 129], [44, 45], [44, 118], [44, 130], [45, 46], [45, 119], [45, 131], [46, 47], [46, 120], [46, 132], [47, 48], [47, 121], [47, 133], [48, 49], [48, 122], [48, 134], [49, 50], [49, 123], [49, 135], [50, 51], [50, 124], [50, 136], [51, 52], [51, 125], [51, 137], [52, 53], [52, 126], [52, 138], [53, 54], [53, 127], [53, 139], [54, 55], [54, 128], [54, 140], [55, 56], [55, 129], [55, 141], [56, 57], [56, 130], [56, 142], [57, 58], [57, 131], [57, 143], [58, 59], [58, 132], [58, 144], [59, 60], [59, 133], [59, 145], [60, 61], [60, 134], [60, 146], [61, 62], [61, 135], [61, 147], [62, 63], [62, 136], [62, 148], [63, 64], [63, 75], [63, 137], [64, 65], [64, 76], [64, 138], [65, 66], [65, 77], [65, 139], [66, 67], [66, 78], [66, 140], [67, 68], [67, 79], [67, 141], [68, 69], [68, 80], [68, 142], [69, 70], [69, 81], [69, 143], [70, 71], [70, 82], [70, 144], [71, 72], [71, 83], [71, 145], [72, 73], [72, 84], [72, 146], [73, 74], [73, 85], [73, 147], [74, 86], [74, 148], [75, 76], [75, 148], [76, 77], [77, 78], [78, 79], [79, 80], [80, 81], [81, 82], [82, 83], [83, 84], [84, 85], [85, 86], [86, 87], [87, 88], [88, 89], [89, 90], [90, 91], [91, 92], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108], [108, 109], [109, 110], [110, 111], [111, 112], [112, 113], [113, 114], [114, 115], [115, 116], [116, 117], [117, 118], [118, 119], [119, 120], [120, 121], [121, 122], [122, 123], [123, 124], [124, 125], [125, 126], [126, 127], [127, 128], [128, 129], [129, 130], [130, 131], [131, 132], [132, 133], [133, 134], [134, 135], [135, 136], [136, 137], [137, 138], [138, 139], [139, 140], [140, 141], [141, 142], [142, 143], [143, 144], [144, 145], [145, 146], [146, 147], [147, 148]]);;
R:=P177Census(D);;Need(Size(R.F)=592);;
PrintTo("current_c4_descent/148_002.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 148_002 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
