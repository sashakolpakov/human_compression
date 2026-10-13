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
D:=P177Graph("144_025",144,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129, 131, 133, 135, 137, 139, 141, 143],[[1, 2], [1, 36], [1, 54], [1, 73], [2, 3], [2, 55], [2, 74], [3, 4], [3, 56], [3, 75], [4, 5], [4, 57], [4, 76], [5, 6], [5, 58], [5, 77], [6, 7], [6, 59], [6, 78], [7, 8], [7, 60], [7, 79], [8, 9], [8, 61], [8, 80], [9, 10], [9, 62], [9, 81], [10, 11], [10, 63], [10, 82], [11, 12], [11, 64], [11, 83], [12, 13], [12, 65], [12, 84], [13, 14], [13, 66], [13, 85], [14, 15], [14, 67], [14, 86], [15, 16], [15, 68], [15, 87], [16, 17], [16, 69], [16, 88], [17, 18], [17, 70], [17, 89], [18, 19], [18, 71], [18, 90], [19, 20], [19, 72], [19, 91], [20, 21], [20, 37], [20, 92], [21, 22], [21, 38], [21, 93], [22, 23], [22, 39], [22, 94], [23, 24], [23, 40], [23, 95], [24, 25], [24, 41], [24, 96], [25, 26], [25, 42], [25, 97], [26, 27], [26, 43], [26, 98], [27, 28], [27, 44], [27, 99], [28, 29], [28, 45], [28, 100], [29, 30], [29, 46], [29, 101], [30, 31], [30, 47], [30, 102], [31, 32], [31, 48], [31, 103], [32, 33], [32, 49], [32, 104], [33, 34], [33, 50], [33, 105], [34, 35], [34, 51], [34, 106], [35, 36], [35, 52], [35, 107], [36, 53], [36, 108], [37, 73], [37, 89], [37, 142], [38, 74], [38, 90], [38, 143], [39, 75], [39, 91], [39, 144], [40, 76], [40, 92], [40, 109], [41, 77], [41, 93], [41, 110], [42, 78], [42, 94], [42, 111], [43, 79], [43, 95], [43, 112], [44, 80], [44, 96], [44, 113], [45, 81], [45, 97], [45, 114], [46, 82], [46, 98], [46, 115], [47, 83], [47, 99], [47, 116], [48, 84], [48, 100], [48, 117], [49, 85], [49, 101], [49, 118], [50, 86], [50, 102], [50, 119], [51, 87], [51, 103], [51, 120], [52, 88], [52, 104], [52, 121], [53, 89], [53, 105], [53, 122], [54, 90], [54, 106], [54, 123], [55, 91], [55, 107], [55, 124], [56, 92], [56, 108], [56, 125], [57, 73], [57, 93], [57, 126], [58, 74], [58, 94], [58, 127], [59, 75], [59, 95], [59, 128], [60, 76], [60, 96], [60, 129], [61, 77], [61, 97], [61, 130], [62, 78], [62, 98], [62, 131], [63, 79], [63, 99], [63, 132], [64, 80], [64, 100], [64, 133], [65, 81], [65, 101], [65, 134], [66, 82], [66, 102], [66, 135], [67, 83], [67, 103], [67, 136], [68, 84], [68, 104], [68, 137], [69, 85], [69, 105], [69, 138], [70, 86], [70, 106], [70, 139], [71, 87], [71, 107], [71, 140], [72, 88], [72, 108], [72, 141], [73, 109], [74, 110], [75, 111], [76, 112], [77, 113], [78, 114], [79, 115], [80, 116], [81, 117], [82, 118], [83, 119], [84, 120], [85, 121], [86, 122], [87, 123], [88, 124], [89, 125], [90, 126], [91, 127], [92, 128], [93, 129], [94, 130], [95, 131], [96, 132], [97, 133], [98, 134], [99, 135], [100, 136], [101, 137], [102, 138], [103, 139], [104, 140], [105, 141], [106, 142], [107, 143], [108, 144], [109, 110], [109, 144], [110, 111], [111, 112], [112, 113], [113, 114], [114, 115], [115, 116], [116, 117], [117, 118], [118, 119], [119, 120], [120, 121], [121, 122], [122, 123], [123, 124], [124, 125], [125, 126], [126, 127], [127, 128], [128, 129], [129, 130], [130, 131], [131, 132], [132, 133], [133, 134], [134, 135], [135, 136], [136, 137], [137, 138], [138, 139], [139, 140], [140, 141], [141, 142], [142, 143], [143, 144]]);;
R:=P177Census(D);;Need(Size(R.F)=576);;
PrintTo("current_c4_descent/144_025.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_025 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
