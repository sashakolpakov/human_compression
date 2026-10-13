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
D:=P177Graph("144_006",144,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 122, 124, 126, 128, 130, 132, 134, 136, 138, 140, 142, 144],[[1, 2], [1, 24], [1, 25], [1, 127], [2, 3], [2, 26], [2, 128], [3, 4], [3, 27], [3, 129], [4, 5], [4, 28], [4, 130], [5, 6], [5, 29], [5, 131], [6, 7], [6, 30], [6, 132], [7, 8], [7, 31], [7, 133], [8, 9], [8, 32], [8, 134], [9, 10], [9, 33], [9, 135], [10, 11], [10, 34], [10, 136], [11, 12], [11, 35], [11, 137], [12, 13], [12, 36], [12, 138], [13, 14], [13, 37], [13, 139], [14, 15], [14, 38], [14, 140], [15, 16], [15, 39], [15, 141], [16, 17], [16, 40], [16, 142], [17, 18], [17, 41], [17, 143], [18, 19], [18, 42], [18, 144], [19, 20], [19, 43], [19, 121], [20, 21], [20, 44], [20, 122], [21, 22], [21, 45], [21, 123], [22, 23], [22, 46], [22, 124], [23, 24], [23, 47], [23, 125], [24, 48], [24, 126], [25, 26], [25, 48], [25, 49], [26, 27], [26, 50], [27, 28], [27, 51], [28, 29], [28, 52], [29, 30], [29, 53], [30, 31], [30, 54], [31, 32], [31, 55], [32, 33], [32, 56], [33, 34], [33, 57], [34, 35], [34, 58], [35, 36], [35, 59], [36, 37], [36, 60], [37, 38], [37, 61], [38, 39], [38, 62], [39, 40], [39, 63], [40, 41], [40, 64], [41, 42], [41, 65], [42, 43], [42, 66], [43, 44], [43, 67], [44, 45], [44, 68], [45, 46], [45, 69], [46, 47], [46, 70], [47, 48], [47, 71], [48, 72], [49, 50], [49, 72], [49, 73], [50, 51], [50, 74], [51, 52], [51, 75], [52, 53], [52, 76], [53, 54], [53, 77], [54, 55], [54, 78], [55, 56], [55, 79], [56, 57], [56, 80], [57, 58], [57, 81], [58, 59], [58, 82], [59, 60], [59, 83], [60, 61], [60, 84], [61, 62], [61, 85], [62, 63], [62, 86], [63, 64], [63, 87], [64, 65], [64, 88], [65, 66], [65, 89], [66, 67], [66, 90], [67, 68], [67, 91], [68, 69], [68, 92], [69, 70], [69, 93], [70, 71], [70, 94], [71, 72], [71, 95], [72, 96], [73, 74], [73, 96], [73, 97], [74, 75], [74, 98], [75, 76], [75, 99], [76, 77], [76, 100], [77, 78], [77, 101], [78, 79], [78, 102], [79, 80], [79, 103], [80, 81], [80, 104], [81, 82], [81, 105], [82, 83], [82, 106], [83, 84], [83, 107], [84, 85], [84, 108], [85, 86], [85, 109], [86, 87], [86, 110], [87, 88], [87, 111], [88, 89], [88, 112], [89, 90], [89, 113], [90, 91], [90, 114], [91, 92], [91, 115], [92, 93], [92, 116], [93, 94], [93, 117], [94, 95], [94, 118], [95, 96], [95, 119], [96, 120], [97, 98], [97, 120], [97, 121], [98, 99], [98, 122], [99, 100], [99, 123], [100, 101], [100, 124], [101, 102], [101, 125], [102, 103], [102, 126], [103, 104], [103, 127], [104, 105], [104, 128], [105, 106], [105, 129], [106, 107], [106, 130], [107, 108], [107, 131], [108, 109], [108, 132], [109, 110], [109, 133], [110, 111], [110, 134], [111, 112], [111, 135], [112, 113], [112, 136], [113, 114], [113, 137], [114, 115], [114, 138], [115, 116], [115, 139], [116, 117], [116, 140], [117, 118], [117, 141], [118, 119], [118, 142], [119, 120], [119, 143], [120, 144], [121, 122], [121, 144], [122, 123], [123, 124], [124, 125], [125, 126], [126, 127], [127, 128], [128, 129], [129, 130], [130, 131], [131, 132], [132, 133], [133, 134], [134, 135], [135, 136], [136, 137], [137, 138], [138, 139], [139, 140], [140, 141], [141, 142], [142, 143], [143, 144]]);;
R:=P177Census(D);;Need(Size(R.F)=576);;
PrintTo("current_c4_descent/144_006.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_006 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
