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
D:=P177Graph("146_002",146,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129, 131, 133, 135, 137, 139, 141, 143, 145],[[1, 2], [1, 28], [1, 120], [1, 146], [2, 3], [2, 29], [2, 121], [3, 4], [3, 30], [3, 122], [4, 5], [4, 31], [4, 123], [5, 6], [5, 32], [5, 124], [6, 7], [6, 33], [6, 125], [7, 8], [7, 34], [7, 126], [8, 9], [8, 35], [8, 127], [9, 10], [9, 36], [9, 128], [10, 11], [10, 37], [10, 129], [11, 12], [11, 38], [11, 130], [12, 13], [12, 39], [12, 131], [13, 14], [13, 40], [13, 132], [14, 15], [14, 41], [14, 133], [15, 16], [15, 42], [15, 134], [16, 17], [16, 43], [16, 135], [17, 18], [17, 44], [17, 136], [18, 19], [18, 45], [18, 137], [19, 20], [19, 46], [19, 138], [20, 21], [20, 47], [20, 139], [21, 22], [21, 48], [21, 140], [22, 23], [22, 49], [22, 141], [23, 24], [23, 50], [23, 142], [24, 25], [24, 51], [24, 143], [25, 26], [25, 52], [25, 144], [26, 27], [26, 53], [26, 145], [27, 28], [27, 54], [27, 146], [28, 29], [28, 55], [29, 30], [29, 56], [30, 31], [30, 57], [31, 32], [31, 58], [32, 33], [32, 59], [33, 34], [33, 60], [34, 35], [34, 61], [35, 36], [35, 62], [36, 37], [36, 63], [37, 38], [37, 64], [38, 39], [38, 65], [39, 40], [39, 66], [40, 41], [40, 67], [41, 42], [41, 68], [42, 43], [42, 69], [43, 44], [43, 70], [44, 45], [44, 71], [45, 46], [45, 72], [46, 47], [46, 73], [47, 48], [47, 74], [48, 49], [48, 75], [49, 50], [49, 76], [50, 51], [50, 77], [51, 52], [51, 78], [52, 53], [52, 79], [53, 54], [53, 80], [54, 55], [54, 81], [55, 56], [55, 82], [56, 57], [56, 83], [57, 58], [57, 84], [58, 59], [58, 85], [59, 60], [59, 86], [60, 61], [60, 87], [61, 62], [61, 88], [62, 63], [62, 89], [63, 64], [63, 90], [64, 65], [64, 91], [65, 66], [65, 92], [66, 67], [66, 93], [67, 68], [67, 94], [68, 69], [68, 95], [69, 70], [69, 96], [70, 71], [70, 97], [71, 72], [71, 98], [72, 73], [72, 99], [73, 74], [73, 100], [74, 75], [74, 101], [75, 76], [75, 102], [76, 77], [76, 103], [77, 78], [77, 104], [78, 79], [78, 105], [79, 80], [79, 106], [80, 81], [80, 107], [81, 82], [81, 108], [82, 83], [82, 109], [83, 84], [83, 110], [84, 85], [84, 111], [85, 86], [85, 112], [86, 87], [86, 113], [87, 88], [87, 114], [88, 89], [88, 115], [89, 90], [89, 116], [90, 91], [90, 117], [91, 92], [91, 118], [92, 93], [92, 119], [93, 94], [93, 120], [94, 95], [94, 121], [95, 96], [95, 122], [96, 97], [96, 123], [97, 98], [97, 124], [98, 99], [98, 125], [99, 100], [99, 126], [100, 101], [100, 127], [101, 102], [101, 128], [102, 103], [102, 129], [103, 104], [103, 130], [104, 105], [104, 131], [105, 106], [105, 132], [106, 107], [106, 133], [107, 108], [107, 134], [108, 109], [108, 135], [109, 110], [109, 136], [110, 111], [110, 137], [111, 112], [111, 138], [112, 113], [112, 139], [113, 114], [113, 140], [114, 115], [114, 141], [115, 116], [115, 142], [116, 117], [116, 143], [117, 118], [117, 144], [118, 119], [118, 145], [119, 120], [119, 146], [120, 121], [121, 122], [122, 123], [123, 124], [124, 125], [125, 126], [126, 127], [127, 128], [128, 129], [129, 130], [130, 131], [131, 132], [132, 133], [133, 134], [134, 135], [135, 136], [136, 137], [137, 138], [138, 139], [139, 140], [140, 141], [141, 142], [142, 143], [143, 144], [144, 145], [145, 146]]);;
R:=P177Census(D);;Need(Size(R.F)=584);;
PrintTo("current_c4_descent/146_002.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 146_002 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
