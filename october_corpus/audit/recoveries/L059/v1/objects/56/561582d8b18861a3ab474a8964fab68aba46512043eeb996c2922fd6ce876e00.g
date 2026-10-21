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
D:=P177Graph("136_003",136,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129, 131, 133, 135],[[1, 2], [1, 36], [1, 102], [1, 136], [2, 3], [2, 37], [2, 103], [3, 4], [3, 38], [3, 104], [4, 5], [4, 39], [4, 105], [5, 6], [5, 40], [5, 106], [6, 7], [6, 41], [6, 107], [7, 8], [7, 42], [7, 108], [8, 9], [8, 43], [8, 109], [9, 10], [9, 44], [9, 110], [10, 11], [10, 45], [10, 111], [11, 12], [11, 46], [11, 112], [12, 13], [12, 47], [12, 113], [13, 14], [13, 48], [13, 114], [14, 15], [14, 49], [14, 115], [15, 16], [15, 50], [15, 116], [16, 17], [16, 51], [16, 117], [17, 18], [17, 52], [17, 118], [18, 19], [18, 53], [18, 119], [19, 20], [19, 54], [19, 120], [20, 21], [20, 55], [20, 121], [21, 22], [21, 56], [21, 122], [22, 23], [22, 57], [22, 123], [23, 24], [23, 58], [23, 124], [24, 25], [24, 59], [24, 125], [25, 26], [25, 60], [25, 126], [26, 27], [26, 61], [26, 127], [27, 28], [27, 62], [27, 128], [28, 29], [28, 63], [28, 129], [29, 30], [29, 64], [29, 130], [30, 31], [30, 65], [30, 131], [31, 32], [31, 66], [31, 132], [32, 33], [32, 67], [32, 133], [33, 34], [33, 68], [33, 134], [34, 35], [34, 69], [34, 135], [35, 36], [35, 70], [35, 136], [36, 37], [36, 71], [37, 38], [37, 72], [38, 39], [38, 73], [39, 40], [39, 74], [40, 41], [40, 75], [41, 42], [41, 76], [42, 43], [42, 77], [43, 44], [43, 78], [44, 45], [44, 79], [45, 46], [45, 80], [46, 47], [46, 81], [47, 48], [47, 82], [48, 49], [48, 83], [49, 50], [49, 84], [50, 51], [50, 85], [51, 52], [51, 86], [52, 53], [52, 87], [53, 54], [53, 88], [54, 55], [54, 89], [55, 56], [55, 90], [56, 57], [56, 91], [57, 58], [57, 92], [58, 59], [58, 93], [59, 60], [59, 94], [60, 61], [60, 95], [61, 62], [61, 96], [62, 63], [62, 97], [63, 64], [63, 98], [64, 65], [64, 99], [65, 66], [65, 100], [66, 67], [66, 101], [67, 68], [67, 102], [68, 69], [68, 103], [69, 70], [69, 104], [70, 71], [70, 105], [71, 72], [71, 106], [72, 73], [72, 107], [73, 74], [73, 108], [74, 75], [74, 109], [75, 76], [75, 110], [76, 77], [76, 111], [77, 78], [77, 112], [78, 79], [78, 113], [79, 80], [79, 114], [80, 81], [80, 115], [81, 82], [81, 116], [82, 83], [82, 117], [83, 84], [83, 118], [84, 85], [84, 119], [85, 86], [85, 120], [86, 87], [86, 121], [87, 88], [87, 122], [88, 89], [88, 123], [89, 90], [89, 124], [90, 91], [90, 125], [91, 92], [91, 126], [92, 93], [92, 127], [93, 94], [93, 128], [94, 95], [94, 129], [95, 96], [95, 130], [96, 97], [96, 131], [97, 98], [97, 132], [98, 99], [98, 133], [99, 100], [99, 134], [100, 101], [100, 135], [101, 102], [101, 136], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108], [108, 109], [109, 110], [110, 111], [111, 112], [112, 113], [113, 114], [114, 115], [115, 116], [116, 117], [117, 118], [118, 119], [119, 120], [120, 121], [121, 122], [122, 123], [123, 124], [124, 125], [125, 126], [126, 127], [127, 128], [128, 129], [129, 130], [130, 131], [131, 132], [132, 133], [133, 134], [134, 135], [135, 136]]);;
R:=P177Census(D);;Need(Size(R.F)=544);;
PrintTo("current_c4_descent/136_003.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 136_003 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
