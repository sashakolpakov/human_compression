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
D:=P177Graph("144_003",144,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129, 131, 133, 135, 137, 139, 141, 143],[[1, 2], [1, 56], [1, 90], [1, 144], [2, 3], [2, 57], [2, 91], [3, 4], [3, 58], [3, 92], [4, 5], [4, 59], [4, 93], [5, 6], [5, 60], [5, 94], [6, 7], [6, 61], [6, 95], [7, 8], [7, 62], [7, 96], [8, 9], [8, 63], [8, 97], [9, 10], [9, 64], [9, 98], [10, 11], [10, 65], [10, 99], [11, 12], [11, 66], [11, 100], [12, 13], [12, 67], [12, 101], [13, 14], [13, 68], [13, 102], [14, 15], [14, 69], [14, 103], [15, 16], [15, 70], [15, 104], [16, 17], [16, 71], [16, 105], [17, 18], [17, 72], [17, 106], [18, 19], [18, 73], [18, 107], [19, 20], [19, 74], [19, 108], [20, 21], [20, 75], [20, 109], [21, 22], [21, 76], [21, 110], [22, 23], [22, 77], [22, 111], [23, 24], [23, 78], [23, 112], [24, 25], [24, 79], [24, 113], [25, 26], [25, 80], [25, 114], [26, 27], [26, 81], [26, 115], [27, 28], [27, 82], [27, 116], [28, 29], [28, 83], [28, 117], [29, 30], [29, 84], [29, 118], [30, 31], [30, 85], [30, 119], [31, 32], [31, 86], [31, 120], [32, 33], [32, 87], [32, 121], [33, 34], [33, 88], [33, 122], [34, 35], [34, 89], [34, 123], [35, 36], [35, 90], [35, 124], [36, 37], [36, 91], [36, 125], [37, 38], [37, 92], [37, 126], [38, 39], [38, 93], [38, 127], [39, 40], [39, 94], [39, 128], [40, 41], [40, 95], [40, 129], [41, 42], [41, 96], [41, 130], [42, 43], [42, 97], [42, 131], [43, 44], [43, 98], [43, 132], [44, 45], [44, 99], [44, 133], [45, 46], [45, 100], [45, 134], [46, 47], [46, 101], [46, 135], [47, 48], [47, 102], [47, 136], [48, 49], [48, 103], [48, 137], [49, 50], [49, 104], [49, 138], [50, 51], [50, 105], [50, 139], [51, 52], [51, 106], [51, 140], [52, 53], [52, 107], [52, 141], [53, 54], [53, 108], [53, 142], [54, 55], [54, 109], [54, 143], [55, 56], [55, 110], [55, 144], [56, 57], [56, 111], [57, 58], [57, 112], [58, 59], [58, 113], [59, 60], [59, 114], [60, 61], [60, 115], [61, 62], [61, 116], [62, 63], [62, 117], [63, 64], [63, 118], [64, 65], [64, 119], [65, 66], [65, 120], [66, 67], [66, 121], [67, 68], [67, 122], [68, 69], [68, 123], [69, 70], [69, 124], [70, 71], [70, 125], [71, 72], [71, 126], [72, 73], [72, 127], [73, 74], [73, 128], [74, 75], [74, 129], [75, 76], [75, 130], [76, 77], [76, 131], [77, 78], [77, 132], [78, 79], [78, 133], [79, 80], [79, 134], [80, 81], [80, 135], [81, 82], [81, 136], [82, 83], [82, 137], [83, 84], [83, 138], [84, 85], [84, 139], [85, 86], [85, 140], [86, 87], [86, 141], [87, 88], [87, 142], [88, 89], [88, 143], [89, 90], [89, 144], [90, 91], [91, 92], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108], [108, 109], [109, 110], [110, 111], [111, 112], [112, 113], [113, 114], [114, 115], [115, 116], [116, 117], [117, 118], [118, 119], [119, 120], [120, 121], [121, 122], [122, 123], [123, 124], [124, 125], [125, 126], [126, 127], [127, 128], [128, 129], [129, 130], [130, 131], [131, 132], [132, 133], [133, 134], [134, 135], [135, 136], [136, 137], [137, 138], [138, 139], [139, 140], [140, 141], [141, 142], [142, 143], [143, 144]]);;
R:=P177Census(D);;Need(Size(R.F)=576);;
PrintTo("current_c4_descent/144_003.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_003 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
