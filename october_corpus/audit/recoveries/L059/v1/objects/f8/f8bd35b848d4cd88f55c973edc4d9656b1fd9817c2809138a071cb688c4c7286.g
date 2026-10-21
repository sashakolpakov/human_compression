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
D:=P177Graph("136_002",136,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129, 131, 133, 135],[[1, 2], [1, 34], [1, 104], [1, 136], [2, 3], [2, 35], [2, 105], [3, 4], [3, 36], [3, 106], [4, 5], [4, 37], [4, 107], [5, 6], [5, 38], [5, 108], [6, 7], [6, 39], [6, 109], [7, 8], [7, 40], [7, 110], [8, 9], [8, 41], [8, 111], [9, 10], [9, 42], [9, 112], [10, 11], [10, 43], [10, 113], [11, 12], [11, 44], [11, 114], [12, 13], [12, 45], [12, 115], [13, 14], [13, 46], [13, 116], [14, 15], [14, 47], [14, 117], [15, 16], [15, 48], [15, 118], [16, 17], [16, 49], [16, 119], [17, 18], [17, 50], [17, 120], [18, 19], [18, 51], [18, 121], [19, 20], [19, 52], [19, 122], [20, 21], [20, 53], [20, 123], [21, 22], [21, 54], [21, 124], [22, 23], [22, 55], [22, 125], [23, 24], [23, 56], [23, 126], [24, 25], [24, 57], [24, 127], [25, 26], [25, 58], [25, 128], [26, 27], [26, 59], [26, 129], [27, 28], [27, 60], [27, 130], [28, 29], [28, 61], [28, 131], [29, 30], [29, 62], [29, 132], [30, 31], [30, 63], [30, 133], [31, 32], [31, 64], [31, 134], [32, 33], [32, 65], [32, 135], [33, 34], [33, 66], [33, 136], [34, 35], [34, 67], [35, 36], [35, 68], [36, 37], [36, 69], [37, 38], [37, 70], [38, 39], [38, 71], [39, 40], [39, 72], [40, 41], [40, 73], [41, 42], [41, 74], [42, 43], [42, 75], [43, 44], [43, 76], [44, 45], [44, 77], [45, 46], [45, 78], [46, 47], [46, 79], [47, 48], [47, 80], [48, 49], [48, 81], [49, 50], [49, 82], [50, 51], [50, 83], [51, 52], [51, 84], [52, 53], [52, 85], [53, 54], [53, 86], [54, 55], [54, 87], [55, 56], [55, 88], [56, 57], [56, 89], [57, 58], [57, 90], [58, 59], [58, 91], [59, 60], [59, 92], [60, 61], [60, 93], [61, 62], [61, 94], [62, 63], [62, 95], [63, 64], [63, 96], [64, 65], [64, 97], [65, 66], [65, 98], [66, 67], [66, 99], [67, 68], [67, 100], [68, 69], [68, 101], [69, 70], [69, 102], [70, 71], [70, 103], [71, 72], [71, 104], [72, 73], [72, 105], [73, 74], [73, 106], [74, 75], [74, 107], [75, 76], [75, 108], [76, 77], [76, 109], [77, 78], [77, 110], [78, 79], [78, 111], [79, 80], [79, 112], [80, 81], [80, 113], [81, 82], [81, 114], [82, 83], [82, 115], [83, 84], [83, 116], [84, 85], [84, 117], [85, 86], [85, 118], [86, 87], [86, 119], [87, 88], [87, 120], [88, 89], [88, 121], [89, 90], [89, 122], [90, 91], [90, 123], [91, 92], [91, 124], [92, 93], [92, 125], [93, 94], [93, 126], [94, 95], [94, 127], [95, 96], [95, 128], [96, 97], [96, 129], [97, 98], [97, 130], [98, 99], [98, 131], [99, 100], [99, 132], [100, 101], [100, 133], [101, 102], [101, 134], [102, 103], [102, 135], [103, 104], [103, 136], [104, 105], [105, 106], [106, 107], [107, 108], [108, 109], [109, 110], [110, 111], [111, 112], [112, 113], [113, 114], [114, 115], [115, 116], [116, 117], [117, 118], [118, 119], [119, 120], [120, 121], [121, 122], [122, 123], [123, 124], [124, 125], [125, 126], [126, 127], [127, 128], [128, 129], [129, 130], [130, 131], [131, 132], [132, 133], [133, 134], [134, 135], [135, 136]]);;
R:=P177Census(D);;Need(Size(R.F)=544);;
PrintTo("current_c4_descent/136_002.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 136_002 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
