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
D:=P177Graph("150_003",150,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 121, 123, 125, 127, 129, 131, 133, 135, 137, 139, 141, 143, 145, 147, 149],[[1, 2], [1, 30], [1, 31], [1, 126], [2, 3], [2, 32], [2, 127], [3, 4], [3, 33], [3, 128], [4, 5], [4, 34], [4, 129], [5, 6], [5, 35], [5, 130], [6, 7], [6, 36], [6, 131], [7, 8], [7, 37], [7, 132], [8, 9], [8, 38], [8, 133], [9, 10], [9, 39], [9, 134], [10, 11], [10, 40], [10, 135], [11, 12], [11, 41], [11, 136], [12, 13], [12, 42], [12, 137], [13, 14], [13, 43], [13, 138], [14, 15], [14, 44], [14, 139], [15, 16], [15, 45], [15, 140], [16, 17], [16, 46], [16, 141], [17, 18], [17, 47], [17, 142], [18, 19], [18, 48], [18, 143], [19, 20], [19, 49], [19, 144], [20, 21], [20, 50], [20, 145], [21, 22], [21, 51], [21, 146], [22, 23], [22, 52], [22, 147], [23, 24], [23, 53], [23, 148], [24, 25], [24, 54], [24, 149], [25, 26], [25, 55], [25, 150], [26, 27], [26, 56], [26, 121], [27, 28], [27, 57], [27, 122], [28, 29], [28, 58], [28, 123], [29, 30], [29, 59], [29, 124], [30, 60], [30, 125], [31, 32], [31, 60], [31, 61], [32, 33], [32, 62], [33, 34], [33, 63], [34, 35], [34, 64], [35, 36], [35, 65], [36, 37], [36, 66], [37, 38], [37, 67], [38, 39], [38, 68], [39, 40], [39, 69], [40, 41], [40, 70], [41, 42], [41, 71], [42, 43], [42, 72], [43, 44], [43, 73], [44, 45], [44, 74], [45, 46], [45, 75], [46, 47], [46, 76], [47, 48], [47, 77], [48, 49], [48, 78], [49, 50], [49, 79], [50, 51], [50, 80], [51, 52], [51, 81], [52, 53], [52, 82], [53, 54], [53, 83], [54, 55], [54, 84], [55, 56], [55, 85], [56, 57], [56, 86], [57, 58], [57, 87], [58, 59], [58, 88], [59, 60], [59, 89], [60, 90], [61, 62], [61, 90], [61, 91], [62, 63], [62, 92], [63, 64], [63, 93], [64, 65], [64, 94], [65, 66], [65, 95], [66, 67], [66, 96], [67, 68], [67, 97], [68, 69], [68, 98], [69, 70], [69, 99], [70, 71], [70, 100], [71, 72], [71, 101], [72, 73], [72, 102], [73, 74], [73, 103], [74, 75], [74, 104], [75, 76], [75, 105], [76, 77], [76, 106], [77, 78], [77, 107], [78, 79], [78, 108], [79, 80], [79, 109], [80, 81], [80, 110], [81, 82], [81, 111], [82, 83], [82, 112], [83, 84], [83, 113], [84, 85], [84, 114], [85, 86], [85, 115], [86, 87], [86, 116], [87, 88], [87, 117], [88, 89], [88, 118], [89, 90], [89, 119], [90, 120], [91, 92], [91, 120], [91, 121], [92, 93], [92, 122], [93, 94], [93, 123], [94, 95], [94, 124], [95, 96], [95, 125], [96, 97], [96, 126], [97, 98], [97, 127], [98, 99], [98, 128], [99, 100], [99, 129], [100, 101], [100, 130], [101, 102], [101, 131], [102, 103], [102, 132], [103, 104], [103, 133], [104, 105], [104, 134], [105, 106], [105, 135], [106, 107], [106, 136], [107, 108], [107, 137], [108, 109], [108, 138], [109, 110], [109, 139], [110, 111], [110, 140], [111, 112], [111, 141], [112, 113], [112, 142], [113, 114], [113, 143], [114, 115], [114, 144], [115, 116], [115, 145], [116, 117], [116, 146], [117, 118], [117, 147], [118, 119], [118, 148], [119, 120], [119, 149], [120, 150], [121, 122], [121, 150], [122, 123], [123, 124], [124, 125], [125, 126], [126, 127], [127, 128], [128, 129], [129, 130], [130, 131], [131, 132], [132, 133], [133, 134], [134, 135], [135, 136], [136, 137], [137, 138], [138, 139], [139, 140], [140, 141], [141, 142], [142, 143], [143, 144], [144, 145], [145, 146], [146, 147], [147, 148], [148, 149], [149, 150]]);;
R:=P177Census(D);;Need(Size(R.F)=600);;
PrintTo("current_c4_descent/150_003.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 150_003 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
