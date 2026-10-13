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
D:=P177Graph("144_007",144,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129, 131, 133, 135, 137, 139, 141, 143],[[1, 2], [1, 48], [1, 49], [1, 124], [2, 3], [2, 50], [2, 125], [3, 4], [3, 51], [3, 126], [4, 5], [4, 52], [4, 127], [5, 6], [5, 53], [5, 128], [6, 7], [6, 54], [6, 129], [7, 8], [7, 55], [7, 130], [8, 9], [8, 56], [8, 131], [9, 10], [9, 57], [9, 132], [10, 11], [10, 58], [10, 133], [11, 12], [11, 59], [11, 134], [12, 13], [12, 60], [12, 135], [13, 14], [13, 61], [13, 136], [14, 15], [14, 62], [14, 137], [15, 16], [15, 63], [15, 138], [16, 17], [16, 64], [16, 139], [17, 18], [17, 65], [17, 140], [18, 19], [18, 66], [18, 141], [19, 20], [19, 67], [19, 142], [20, 21], [20, 68], [20, 143], [21, 22], [21, 69], [21, 144], [22, 23], [22, 70], [22, 97], [23, 24], [23, 71], [23, 98], [24, 25], [24, 72], [24, 99], [25, 26], [25, 73], [25, 100], [26, 27], [26, 74], [26, 101], [27, 28], [27, 75], [27, 102], [28, 29], [28, 76], [28, 103], [29, 30], [29, 77], [29, 104], [30, 31], [30, 78], [30, 105], [31, 32], [31, 79], [31, 106], [32, 33], [32, 80], [32, 107], [33, 34], [33, 81], [33, 108], [34, 35], [34, 82], [34, 109], [35, 36], [35, 83], [35, 110], [36, 37], [36, 84], [36, 111], [37, 38], [37, 85], [37, 112], [38, 39], [38, 86], [38, 113], [39, 40], [39, 87], [39, 114], [40, 41], [40, 88], [40, 115], [41, 42], [41, 89], [41, 116], [42, 43], [42, 90], [42, 117], [43, 44], [43, 91], [43, 118], [44, 45], [44, 92], [44, 119], [45, 46], [45, 93], [45, 120], [46, 47], [46, 94], [46, 121], [47, 48], [47, 95], [47, 122], [48, 96], [48, 123], [49, 50], [49, 96], [49, 97], [50, 51], [50, 98], [51, 52], [51, 99], [52, 53], [52, 100], [53, 54], [53, 101], [54, 55], [54, 102], [55, 56], [55, 103], [56, 57], [56, 104], [57, 58], [57, 105], [58, 59], [58, 106], [59, 60], [59, 107], [60, 61], [60, 108], [61, 62], [61, 109], [62, 63], [62, 110], [63, 64], [63, 111], [64, 65], [64, 112], [65, 66], [65, 113], [66, 67], [66, 114], [67, 68], [67, 115], [68, 69], [68, 116], [69, 70], [69, 117], [70, 71], [70, 118], [71, 72], [71, 119], [72, 73], [72, 120], [73, 74], [73, 121], [74, 75], [74, 122], [75, 76], [75, 123], [76, 77], [76, 124], [77, 78], [77, 125], [78, 79], [78, 126], [79, 80], [79, 127], [80, 81], [80, 128], [81, 82], [81, 129], [82, 83], [82, 130], [83, 84], [83, 131], [84, 85], [84, 132], [85, 86], [85, 133], [86, 87], [86, 134], [87, 88], [87, 135], [88, 89], [88, 136], [89, 90], [89, 137], [90, 91], [90, 138], [91, 92], [91, 139], [92, 93], [92, 140], [93, 94], [93, 141], [94, 95], [94, 142], [95, 96], [95, 143], [96, 144], [97, 98], [97, 144], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108], [108, 109], [109, 110], [110, 111], [111, 112], [112, 113], [113, 114], [114, 115], [115, 116], [116, 117], [117, 118], [118, 119], [119, 120], [120, 121], [121, 122], [122, 123], [123, 124], [124, 125], [125, 126], [126, 127], [127, 128], [128, 129], [129, 130], [130, 131], [131, 132], [132, 133], [133, 134], [134, 135], [135, 136], [136, 137], [137, 138], [138, 139], [139, 140], [140, 141], [141, 142], [142, 143], [143, 144]]);;
R:=P177Census(D);;Need(Size(R.F)=576);;
PrintTo("current_c4_descent/144_007.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_007 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
