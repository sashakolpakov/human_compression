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
D:=P177Graph("144_002",144,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129, 131, 133, 135, 137, 139, 141, 143],[[1, 2], [1, 18], [1, 128], [1, 144], [2, 3], [2, 19], [2, 129], [3, 4], [3, 20], [3, 130], [4, 5], [4, 21], [4, 131], [5, 6], [5, 22], [5, 132], [6, 7], [6, 23], [6, 133], [7, 8], [7, 24], [7, 134], [8, 9], [8, 25], [8, 135], [9, 10], [9, 26], [9, 136], [10, 11], [10, 27], [10, 137], [11, 12], [11, 28], [11, 138], [12, 13], [12, 29], [12, 139], [13, 14], [13, 30], [13, 140], [14, 15], [14, 31], [14, 141], [15, 16], [15, 32], [15, 142], [16, 17], [16, 33], [16, 143], [17, 18], [17, 34], [17, 144], [18, 19], [18, 35], [19, 20], [19, 36], [20, 21], [20, 37], [21, 22], [21, 38], [22, 23], [22, 39], [23, 24], [23, 40], [24, 25], [24, 41], [25, 26], [25, 42], [26, 27], [26, 43], [27, 28], [27, 44], [28, 29], [28, 45], [29, 30], [29, 46], [30, 31], [30, 47], [31, 32], [31, 48], [32, 33], [32, 49], [33, 34], [33, 50], [34, 35], [34, 51], [35, 36], [35, 52], [36, 37], [36, 53], [37, 38], [37, 54], [38, 39], [38, 55], [39, 40], [39, 56], [40, 41], [40, 57], [41, 42], [41, 58], [42, 43], [42, 59], [43, 44], [43, 60], [44, 45], [44, 61], [45, 46], [45, 62], [46, 47], [46, 63], [47, 48], [47, 64], [48, 49], [48, 65], [49, 50], [49, 66], [50, 51], [50, 67], [51, 52], [51, 68], [52, 53], [52, 69], [53, 54], [53, 70], [54, 55], [54, 71], [55, 56], [55, 72], [56, 57], [56, 73], [57, 58], [57, 74], [58, 59], [58, 75], [59, 60], [59, 76], [60, 61], [60, 77], [61, 62], [61, 78], [62, 63], [62, 79], [63, 64], [63, 80], [64, 65], [64, 81], [65, 66], [65, 82], [66, 67], [66, 83], [67, 68], [67, 84], [68, 69], [68, 85], [69, 70], [69, 86], [70, 71], [70, 87], [71, 72], [71, 88], [72, 73], [72, 89], [73, 74], [73, 90], [74, 75], [74, 91], [75, 76], [75, 92], [76, 77], [76, 93], [77, 78], [77, 94], [78, 79], [78, 95], [79, 80], [79, 96], [80, 81], [80, 97], [81, 82], [81, 98], [82, 83], [82, 99], [83, 84], [83, 100], [84, 85], [84, 101], [85, 86], [85, 102], [86, 87], [86, 103], [87, 88], [87, 104], [88, 89], [88, 105], [89, 90], [89, 106], [90, 91], [90, 107], [91, 92], [91, 108], [92, 93], [92, 109], [93, 94], [93, 110], [94, 95], [94, 111], [95, 96], [95, 112], [96, 97], [96, 113], [97, 98], [97, 114], [98, 99], [98, 115], [99, 100], [99, 116], [100, 101], [100, 117], [101, 102], [101, 118], [102, 103], [102, 119], [103, 104], [103, 120], [104, 105], [104, 121], [105, 106], [105, 122], [106, 107], [106, 123], [107, 108], [107, 124], [108, 109], [108, 125], [109, 110], [109, 126], [110, 111], [110, 127], [111, 112], [111, 128], [112, 113], [112, 129], [113, 114], [113, 130], [114, 115], [114, 131], [115, 116], [115, 132], [116, 117], [116, 133], [117, 118], [117, 134], [118, 119], [118, 135], [119, 120], [119, 136], [120, 121], [120, 137], [121, 122], [121, 138], [122, 123], [122, 139], [123, 124], [123, 140], [124, 125], [124, 141], [125, 126], [125, 142], [126, 127], [126, 143], [127, 128], [127, 144], [128, 129], [129, 130], [130, 131], [131, 132], [132, 133], [133, 134], [134, 135], [135, 136], [136, 137], [137, 138], [138, 139], [139, 140], [140, 141], [141, 142], [142, 143], [143, 144]]);;
R:=P177Census(D);;Need(Size(R.F)=576);;
PrintTo("current_c4_descent/144_002.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_002 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
