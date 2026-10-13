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
D:=P177Graph("144_037",144,[1, 3, 4, 6, 9, 11, 12, 13, 15, 17, 18, 19, 23, 27, 29, 30, 32, 34, 38, 40, 42, 44, 46, 47, 48, 49, 51, 54, 57, 59, 61, 64, 67, 68, 69, 71, 77, 79, 80, 81, 82, 84, 85, 86, 87, 89, 91, 93, 95, 96, 97, 102, 103, 105, 107, 109, 115, 119, 122, 123, 124, 125, 127, 129, 132, 133, 134, 135, 136, 137, 138, 139],[[1, 2], [1, 5], [1, 117], [1, 130], [2, 6], [2, 12], [2, 13], [3, 7], [3, 14], [3, 104], [3, 106], [4, 7], [4, 8], [4, 113], [4, 128], [5, 11], [5, 15], [5, 27], [6, 16], [6, 26], [6, 28], [7, 17], [7, 19], [8, 9], [8, 18], [8, 29], [9, 14], [9, 94], [9, 118], [10, 19], [10, 30], [10, 127], [10, 129], [11, 20], [11, 100], [11, 120], [12, 20], [12, 111], [12, 112], [13, 24], [13, 31], [13, 52], [14, 32], [14, 42], [15, 25], [15, 33], [15, 53], [16, 34], [16, 51], [16, 54], [17, 21], [17, 35], [17, 55], [18, 22], [18, 36], [18, 56], [19, 37], [19, 39], [20, 38], [20, 49], [21, 30], [21, 119], [21, 136], [22, 57], [22, 109], [22, 129], [23, 39], [23, 58], [23, 141], [23, 142], [24, 40], [24, 125], [24, 139], [25, 59], [25, 122], [25, 133], [26, 40], [26, 132], [26, 133], [27, 43], [27, 52], [27, 60], [28, 49], [28, 61], [28, 80], [29, 41], [29, 55], [29, 62], [30, 63], [30, 75], [31, 47], [31, 64], [31, 81], [32, 50], [32, 56], [32, 65], [33, 34], [33, 48], [33, 82], [34, 66], [34, 83], [35, 44], [35, 67], [35, 84], [36, 46], [36, 68], [36, 85], [37, 42], [37, 69], [37, 86], [38, 45], [38, 53], [38, 70], [39, 68], [39, 71], [40, 72], [40, 78], [41, 57], [41, 134], [41, 137], [42, 58], [42, 76], [43, 59], [43, 135], [43, 138], [44, 62], [44, 131], [44, 142], [45, 77], [45, 124], [45, 125], [46, 65], [46, 131], [46, 141], [47, 60], [47, 140], [47, 144], [48, 70], [48, 140], [48, 143], [49, 73], [49, 74], [50, 79], [50, 97], [50, 119], [51, 73], [51, 143], [51, 144], [52, 80], [52, 87], [53, 61], [53, 87], [54, 78], [54, 88], [54, 104], [55, 86], [55, 89], [56, 69], [56, 89], [57, 75], [57, 90], [58, 91], [58, 95], [59, 78], [59, 92], [60, 93], [60, 105], [61, 94], [61, 106], [62, 95], [62, 107], [63, 79], [63, 84], [63, 96], [64, 66], [64, 70], [64, 108], [65, 67], [65, 96], [66, 97], [66, 109], [67, 98], [67, 110], [68, 98], [68, 99], [69, 100], [69, 111], [70, 102], [71, 75], [71, 101], [71, 112], [72, 77], [72, 81], [72, 102], [73, 93], [73, 103], [74, 77], [74, 123], [74, 138], [75, 85], [76, 79], [76, 115], [76, 137], [77, 92], [78, 82], [79, 90], [80, 104], [80, 113], [81, 88], [81, 113], [82, 114], [82, 118], [83, 93], [83, 115], [83, 127], [84, 101], [84, 117], [85, 116], [85, 120], [86, 112], [86, 117], [87, 118], [87, 128], [88, 119], [88, 129], [89, 120], [89, 130], [90, 91], [90, 107], [91, 111], [91, 121], [92, 103], [92, 105], [93, 108], [94, 97], [94, 102], [95, 99], [95, 110], [96, 100], [96, 121], [97, 131], [98, 122], [98, 124], [99, 123], [99, 132], [100, 124], [101, 125], [101, 133], [102, 126], [103, 106], [103, 126], [104, 127], [105, 114], [105, 128], [106, 115], [107, 116], [107, 130], [108, 134], [108, 136], [109, 118], [109, 141], [110, 135], [110, 139], [111, 123], [112, 132], [113, 136], [114, 129], [114, 137], [115, 142], [116, 133], [116, 138], [117, 139], [119, 126], [120, 122], [121, 125], [121, 138], [122, 143], [123, 144], [124, 140], [126, 137], [127, 141], [128, 134], [130, 135], [131, 136], [132, 143], [134, 142], [135, 144], [139, 140]]);;
R:=P177Census(D);;Need(Size(R.F)=576);;
PrintTo("current_c4_descent/144_037.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_037 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
