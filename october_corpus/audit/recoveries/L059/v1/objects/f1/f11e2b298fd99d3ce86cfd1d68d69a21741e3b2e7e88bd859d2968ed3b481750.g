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
D:=P177Graph("136_004",136,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132, 134, 136],[[1, 2], [1, 68], [1, 69], [1, 95], [2, 3], [2, 70], [2, 96], [3, 4], [3, 71], [3, 97], [4, 5], [4, 72], [4, 98], [5, 6], [5, 73], [5, 99], [6, 7], [6, 74], [6, 100], [7, 8], [7, 75], [7, 101], [8, 9], [8, 76], [8, 102], [9, 10], [9, 77], [9, 103], [10, 11], [10, 78], [10, 104], [11, 12], [11, 79], [11, 105], [12, 13], [12, 80], [12, 106], [13, 14], [13, 81], [13, 107], [14, 15], [14, 82], [14, 108], [15, 16], [15, 83], [15, 109], [16, 17], [16, 84], [16, 110], [17, 18], [17, 85], [17, 111], [18, 19], [18, 86], [18, 112], [19, 20], [19, 87], [19, 113], [20, 21], [20, 88], [20, 114], [21, 22], [21, 89], [21, 115], [22, 23], [22, 90], [22, 116], [23, 24], [23, 91], [23, 117], [24, 25], [24, 92], [24, 118], [25, 26], [25, 93], [25, 119], [26, 27], [26, 94], [26, 120], [27, 28], [27, 95], [27, 121], [28, 29], [28, 96], [28, 122], [29, 30], [29, 97], [29, 123], [30, 31], [30, 98], [30, 124], [31, 32], [31, 99], [31, 125], [32, 33], [32, 100], [32, 126], [33, 34], [33, 101], [33, 127], [34, 35], [34, 102], [34, 128], [35, 36], [35, 103], [35, 129], [36, 37], [36, 104], [36, 130], [37, 38], [37, 105], [37, 131], [38, 39], [38, 106], [38, 132], [39, 40], [39, 107], [39, 133], [40, 41], [40, 108], [40, 134], [41, 42], [41, 109], [41, 135], [42, 43], [42, 110], [42, 136], [43, 44], [43, 69], [43, 111], [44, 45], [44, 70], [44, 112], [45, 46], [45, 71], [45, 113], [46, 47], [46, 72], [46, 114], [47, 48], [47, 73], [47, 115], [48, 49], [48, 74], [48, 116], [49, 50], [49, 75], [49, 117], [50, 51], [50, 76], [50, 118], [51, 52], [51, 77], [51, 119], [52, 53], [52, 78], [52, 120], [53, 54], [53, 79], [53, 121], [54, 55], [54, 80], [54, 122], [55, 56], [55, 81], [55, 123], [56, 57], [56, 82], [56, 124], [57, 58], [57, 83], [57, 125], [58, 59], [58, 84], [58, 126], [59, 60], [59, 85], [59, 127], [60, 61], [60, 86], [60, 128], [61, 62], [61, 87], [61, 129], [62, 63], [62, 88], [62, 130], [63, 64], [63, 89], [63, 131], [64, 65], [64, 90], [64, 132], [65, 66], [65, 91], [65, 133], [66, 67], [66, 92], [66, 134], [67, 68], [67, 93], [67, 135], [68, 94], [68, 136], [69, 70], [69, 136], [70, 71], [71, 72], [72, 73], [73, 74], [74, 75], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80], [80, 81], [81, 82], [82, 83], [83, 84], [84, 85], [85, 86], [86, 87], [87, 88], [88, 89], [89, 90], [90, 91], [91, 92], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108], [108, 109], [109, 110], [110, 111], [111, 112], [112, 113], [113, 114], [114, 115], [115, 116], [116, 117], [117, 118], [118, 119], [119, 120], [120, 121], [121, 122], [122, 123], [123, 124], [124, 125], [125, 126], [126, 127], [127, 128], [128, 129], [129, 130], [130, 131], [131, 132], [132, 133], [133, 134], [134, 135], [135, 136]]);;
R:=P177Census(D);;Need(Size(R.F)=544);;
PrintTo("current_c4_descent/136_004.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 136_004 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
