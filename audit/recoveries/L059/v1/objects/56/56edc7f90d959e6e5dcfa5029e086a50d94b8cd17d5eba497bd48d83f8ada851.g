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
D:=P177Graph("144_033",144,[1, 4, 5, 6, 8, 12, 15, 17, 18, 19, 22, 23, 24, 26, 28, 32, 33, 35, 39, 42, 44, 46, 47, 51, 53, 55, 56, 58, 59, 61, 63, 66, 67, 68, 70, 72, 75, 78, 80, 82, 83, 87, 89, 91, 92, 94, 95, 97, 99, 102, 103, 104, 106, 110, 113, 115, 116, 119, 121, 122, 123, 124, 126, 128, 129, 131, 136, 140, 141, 142, 143, 144],[[1, 2], [1, 3], [1, 79], [1, 90], [2, 4], [2, 5], [2, 97], [3, 6], [3, 8], [3, 97], [4, 7], [4, 9], [4, 114], [5, 10], [5, 13], [5, 114], [6, 11], [6, 14], [6, 100], [7, 12], [7, 15], [7, 126], [8, 16], [8, 21], [8, 100], [9, 17], [9, 22], [9, 126], [10, 18], [10, 23], [10, 116], [11, 19], [11, 24], [11, 115], [12, 20], [12, 25], [12, 135], [13, 26], [13, 33], [13, 116], [14, 17], [14, 22], [14, 115], [15, 27], [15, 34], [15, 135], [16, 28], [16, 35], [16, 102], [17, 29], [17, 36], [18, 30], [18, 37], [18, 127], [19, 31], [19, 38], [19, 139], [20, 32], [20, 39], [20, 142], [21, 26], [21, 33], [21, 102], [22, 40], [22, 49], [23, 27], [23, 34], [23, 127], [24, 41], [24, 50], [24, 139], [25, 42], [25, 51], [25, 142], [26, 43], [26, 52], [27, 44], [27, 53], [28, 45], [28, 54], [28, 132], [29, 46], [29, 55], [29, 136], [30, 47], [30, 56], [30, 144], [31, 32], [31, 39], [31, 141], [32, 48], [32, 57], [33, 40], [33, 49], [34, 58], [34, 67], [35, 41], [35, 50], [35, 132], [36, 42], [36, 51], [36, 136], [37, 59], [37, 68], [37, 144], [38, 46], [38, 55], [38, 141], [39, 60], [39, 69], [40, 61], [40, 70], [41, 44], [41, 53], [42, 62], [42, 71], [43, 63], [43, 72], [43, 140], [44, 64], [44, 73], [45, 47], [45, 56], [45, 143], [46, 65], [46, 74], [47, 48], [47, 57], [48, 66], [48, 75], [49, 58], [49, 67], [50, 61], [50, 70], [51, 76], [51, 85], [52, 59], [52, 68], [52, 140], [53, 60], [53, 69], [54, 63], [54, 72], [54, 143], [55, 77], [55, 86], [56, 64], [56, 73], [57, 78], [57, 87], [58, 79], [58, 88], [59, 62], [59, 71], [60, 80], [60, 89], [61, 81], [61, 90], [62, 82], [62, 91], [63, 65], [63, 74], [64, 83], [64, 92], [65, 66], [65, 75], [66, 84], [66, 93], [67, 76], [67, 85], [68, 79], [68, 88], [69, 94], [69, 103], [70, 77], [70, 86], [71, 78], [71, 87], [72, 81], [72, 90], [73, 95], [73, 104], [74, 82], [74, 91], [75, 96], [75, 105], [76, 97], [76, 106], [77, 80], [77, 89], [78, 98], [78, 107], [79, 99], [80, 100], [80, 108], [81, 83], [81, 92], [82, 101], [82, 109], [83, 84], [83, 93], [84, 102], [84, 110], [85, 94], [85, 103], [86, 97], [86, 106], [87, 111], [87, 117], [88, 95], [88, 104], [89, 96], [89, 105], [90, 99], [91, 112], [91, 118], [92, 100], [92, 108], [93, 113], [93, 119], [94, 114], [94, 120], [95, 98], [95, 107], [96, 115], [96, 121], [98, 116], [98, 122], [99, 101], [99, 109], [101, 102], [101, 110], [103, 111], [103, 117], [104, 114], [104, 120], [105, 123], [105, 128], [106, 112], [106, 118], [107, 113], [107, 119], [108, 124], [108, 129], [109, 116], [109, 122], [110, 125], [110, 130], [111, 126], [111, 131], [112, 115], [112, 121], [113, 127], [113, 132], [117, 123], [117, 128], [118, 126], [118, 131], [119, 133], [119, 137], [120, 124], [120, 129], [121, 125], [121, 130], [122, 134], [122, 138], [123, 135], [123, 139], [124, 127], [124, 132], [125, 136], [125, 140], [128, 133], [128, 137], [129, 135], [129, 139], [130, 141], [130, 143], [131, 134], [131, 138], [133, 142], [133, 144], [134, 136], [134, 140], [137, 141], [137, 143], [138, 142], [138, 144]]);;
R:=P177Census(D);;Need(Size(R.F)=576);;
PrintTo("current_c4_descent/144_033.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_033 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
