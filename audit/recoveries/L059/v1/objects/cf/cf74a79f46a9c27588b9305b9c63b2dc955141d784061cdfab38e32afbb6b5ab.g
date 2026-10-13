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
D:=P177Graph("132_002",132,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129, 131],[[1, 2], [1, 24], [1, 110], [1, 132], [2, 3], [2, 25], [2, 111], [3, 4], [3, 26], [3, 112], [4, 5], [4, 27], [4, 113], [5, 6], [5, 28], [5, 114], [6, 7], [6, 29], [6, 115], [7, 8], [7, 30], [7, 116], [8, 9], [8, 31], [8, 117], [9, 10], [9, 32], [9, 118], [10, 11], [10, 33], [10, 119], [11, 12], [11, 34], [11, 120], [12, 13], [12, 35], [12, 121], [13, 14], [13, 36], [13, 122], [14, 15], [14, 37], [14, 123], [15, 16], [15, 38], [15, 124], [16, 17], [16, 39], [16, 125], [17, 18], [17, 40], [17, 126], [18, 19], [18, 41], [18, 127], [19, 20], [19, 42], [19, 128], [20, 21], [20, 43], [20, 129], [21, 22], [21, 44], [21, 130], [22, 23], [22, 45], [22, 131], [23, 24], [23, 46], [23, 132], [24, 25], [24, 47], [25, 26], [25, 48], [26, 27], [26, 49], [27, 28], [27, 50], [28, 29], [28, 51], [29, 30], [29, 52], [30, 31], [30, 53], [31, 32], [31, 54], [32, 33], [32, 55], [33, 34], [33, 56], [34, 35], [34, 57], [35, 36], [35, 58], [36, 37], [36, 59], [37, 38], [37, 60], [38, 39], [38, 61], [39, 40], [39, 62], [40, 41], [40, 63], [41, 42], [41, 64], [42, 43], [42, 65], [43, 44], [43, 66], [44, 45], [44, 67], [45, 46], [45, 68], [46, 47], [46, 69], [47, 48], [47, 70], [48, 49], [48, 71], [49, 50], [49, 72], [50, 51], [50, 73], [51, 52], [51, 74], [52, 53], [52, 75], [53, 54], [53, 76], [54, 55], [54, 77], [55, 56], [55, 78], [56, 57], [56, 79], [57, 58], [57, 80], [58, 59], [58, 81], [59, 60], [59, 82], [60, 61], [60, 83], [61, 62], [61, 84], [62, 63], [62, 85], [63, 64], [63, 86], [64, 65], [64, 87], [65, 66], [65, 88], [66, 67], [66, 89], [67, 68], [67, 90], [68, 69], [68, 91], [69, 70], [69, 92], [70, 71], [70, 93], [71, 72], [71, 94], [72, 73], [72, 95], [73, 74], [73, 96], [74, 75], [74, 97], [75, 76], [75, 98], [76, 77], [76, 99], [77, 78], [77, 100], [78, 79], [78, 101], [79, 80], [79, 102], [80, 81], [80, 103], [81, 82], [81, 104], [82, 83], [82, 105], [83, 84], [83, 106], [84, 85], [84, 107], [85, 86], [85, 108], [86, 87], [86, 109], [87, 88], [87, 110], [88, 89], [88, 111], [89, 90], [89, 112], [90, 91], [90, 113], [91, 92], [91, 114], [92, 93], [92, 115], [93, 94], [93, 116], [94, 95], [94, 117], [95, 96], [95, 118], [96, 97], [96, 119], [97, 98], [97, 120], [98, 99], [98, 121], [99, 100], [99, 122], [100, 101], [100, 123], [101, 102], [101, 124], [102, 103], [102, 125], [103, 104], [103, 126], [104, 105], [104, 127], [105, 106], [105, 128], [106, 107], [106, 129], [107, 108], [107, 130], [108, 109], [108, 131], [109, 110], [109, 132], [110, 111], [111, 112], [112, 113], [113, 114], [114, 115], [115, 116], [116, 117], [117, 118], [118, 119], [119, 120], [120, 121], [121, 122], [122, 123], [123, 124], [124, 125], [125, 126], [126, 127], [127, 128], [128, 129], [129, 130], [130, 131], [131, 132]]);;
R:=P177Census(D);;Need(Size(R.F)=528);;
PrintTo("current_c4_descent/132_002.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 132_002 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
