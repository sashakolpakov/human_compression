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
D:=P177Graph("144_016",144,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132, 134, 136, 138, 140, 142, 144],[[1, 2], [1, 72], [1, 73], [1, 125], [2, 3], [2, 74], [2, 126], [3, 4], [3, 75], [3, 127], [4, 5], [4, 76], [4, 128], [5, 6], [5, 77], [5, 129], [6, 7], [6, 78], [6, 130], [7, 8], [7, 79], [7, 131], [8, 9], [8, 80], [8, 132], [9, 10], [9, 81], [9, 133], [10, 11], [10, 82], [10, 134], [11, 12], [11, 83], [11, 135], [12, 13], [12, 84], [12, 136], [13, 14], [13, 85], [13, 137], [14, 15], [14, 86], [14, 138], [15, 16], [15, 87], [15, 139], [16, 17], [16, 88], [16, 140], [17, 18], [17, 89], [17, 141], [18, 19], [18, 90], [18, 142], [19, 20], [19, 91], [19, 143], [20, 21], [20, 92], [20, 144], [21, 22], [21, 73], [21, 93], [22, 23], [22, 74], [22, 94], [23, 24], [23, 75], [23, 95], [24, 25], [24, 76], [24, 96], [25, 26], [25, 77], [25, 97], [26, 27], [26, 78], [26, 98], [27, 28], [27, 79], [27, 99], [28, 29], [28, 80], [28, 100], [29, 30], [29, 81], [29, 101], [30, 31], [30, 82], [30, 102], [31, 32], [31, 83], [31, 103], [32, 33], [32, 84], [32, 104], [33, 34], [33, 85], [33, 105], [34, 35], [34, 86], [34, 106], [35, 36], [35, 87], [35, 107], [36, 37], [36, 88], [36, 108], [37, 38], [37, 89], [37, 109], [38, 39], [38, 90], [38, 110], [39, 40], [39, 91], [39, 111], [40, 41], [40, 92], [40, 112], [41, 42], [41, 93], [41, 113], [42, 43], [42, 94], [42, 114], [43, 44], [43, 95], [43, 115], [44, 45], [44, 96], [44, 116], [45, 46], [45, 97], [45, 117], [46, 47], [46, 98], [46, 118], [47, 48], [47, 99], [47, 119], [48, 49], [48, 100], [48, 120], [49, 50], [49, 101], [49, 121], [50, 51], [50, 102], [50, 122], [51, 52], [51, 103], [51, 123], [52, 53], [52, 104], [52, 124], [53, 54], [53, 105], [53, 125], [54, 55], [54, 106], [54, 126], [55, 56], [55, 107], [55, 127], [56, 57], [56, 108], [56, 128], [57, 58], [57, 109], [57, 129], [58, 59], [58, 110], [58, 130], [59, 60], [59, 111], [59, 131], [60, 61], [60, 112], [60, 132], [61, 62], [61, 113], [61, 133], [62, 63], [62, 114], [62, 134], [63, 64], [63, 115], [63, 135], [64, 65], [64, 116], [64, 136], [65, 66], [65, 117], [65, 137], [66, 67], [66, 118], [66, 138], [67, 68], [67, 119], [67, 139], [68, 69], [68, 120], [68, 140], [69, 70], [69, 121], [69, 141], [70, 71], [70, 122], [70, 142], [71, 72], [71, 123], [71, 143], [72, 124], [72, 144], [73, 90], [73, 128], [74, 91], [74, 129], [75, 92], [75, 130], [76, 93], [76, 131], [77, 94], [77, 132], [78, 95], [78, 133], [79, 96], [79, 134], [80, 97], [80, 135], [81, 98], [81, 136], [82, 99], [82, 137], [83, 100], [83, 138], [84, 101], [84, 139], [85, 102], [85, 140], [86, 103], [86, 141], [87, 104], [87, 142], [88, 105], [88, 143], [89, 106], [89, 144], [90, 107], [91, 108], [92, 109], [93, 110], [94, 111], [95, 112], [96, 113], [97, 114], [98, 115], [99, 116], [100, 117], [101, 118], [102, 119], [103, 120], [104, 121], [105, 122], [106, 123], [107, 124], [108, 125], [109, 126], [110, 127], [111, 128], [112, 129], [113, 130], [114, 131], [115, 132], [116, 133], [117, 134], [118, 135], [119, 136], [120, 137], [121, 138], [122, 139], [123, 140], [124, 141], [125, 142], [126, 143], [127, 144]]);;
R:=P177Census(D);;Need(Size(R.F)=1152);;
PrintTo("current_c4_descent/144_016.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_016 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
