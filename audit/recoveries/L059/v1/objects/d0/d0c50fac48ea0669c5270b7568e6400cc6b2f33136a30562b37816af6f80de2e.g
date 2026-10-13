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
D:=P177Graph("132_004",132,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132],[[1, 2], [1, 66], [1, 67], [1, 113], [2, 3], [2, 68], [2, 114], [3, 4], [3, 69], [3, 115], [4, 5], [4, 70], [4, 116], [5, 6], [5, 71], [5, 117], [6, 7], [6, 72], [6, 118], [7, 8], [7, 73], [7, 119], [8, 9], [8, 74], [8, 120], [9, 10], [9, 75], [9, 121], [10, 11], [10, 76], [10, 122], [11, 12], [11, 77], [11, 123], [12, 13], [12, 78], [12, 124], [13, 14], [13, 79], [13, 125], [14, 15], [14, 80], [14, 126], [15, 16], [15, 81], [15, 127], [16, 17], [16, 82], [16, 128], [17, 18], [17, 83], [17, 129], [18, 19], [18, 84], [18, 130], [19, 20], [19, 85], [19, 131], [20, 21], [20, 86], [20, 132], [21, 22], [21, 67], [21, 87], [22, 23], [22, 68], [22, 88], [23, 24], [23, 69], [23, 89], [24, 25], [24, 70], [24, 90], [25, 26], [25, 71], [25, 91], [26, 27], [26, 72], [26, 92], [27, 28], [27, 73], [27, 93], [28, 29], [28, 74], [28, 94], [29, 30], [29, 75], [29, 95], [30, 31], [30, 76], [30, 96], [31, 32], [31, 77], [31, 97], [32, 33], [32, 78], [32, 98], [33, 34], [33, 79], [33, 99], [34, 35], [34, 80], [34, 100], [35, 36], [35, 81], [35, 101], [36, 37], [36, 82], [36, 102], [37, 38], [37, 83], [37, 103], [38, 39], [38, 84], [38, 104], [39, 40], [39, 85], [39, 105], [40, 41], [40, 86], [40, 106], [41, 42], [41, 87], [41, 107], [42, 43], [42, 88], [42, 108], [43, 44], [43, 89], [43, 109], [44, 45], [44, 90], [44, 110], [45, 46], [45, 91], [45, 111], [46, 47], [46, 92], [46, 112], [47, 48], [47, 93], [47, 113], [48, 49], [48, 94], [48, 114], [49, 50], [49, 95], [49, 115], [50, 51], [50, 96], [50, 116], [51, 52], [51, 97], [51, 117], [52, 53], [52, 98], [52, 118], [53, 54], [53, 99], [53, 119], [54, 55], [54, 100], [54, 120], [55, 56], [55, 101], [55, 121], [56, 57], [56, 102], [56, 122], [57, 58], [57, 103], [57, 123], [58, 59], [58, 104], [58, 124], [59, 60], [59, 105], [59, 125], [60, 61], [60, 106], [60, 126], [61, 62], [61, 107], [61, 127], [62, 63], [62, 108], [62, 128], [63, 64], [63, 109], [63, 129], [64, 65], [64, 110], [64, 130], [65, 66], [65, 111], [65, 131], [66, 112], [66, 132], [67, 68], [67, 132], [68, 69], [69, 70], [70, 71], [71, 72], [72, 73], [73, 74], [74, 75], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80], [80, 81], [81, 82], [82, 83], [83, 84], [84, 85], [85, 86], [86, 87], [87, 88], [88, 89], [89, 90], [90, 91], [91, 92], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108], [108, 109], [109, 110], [110, 111], [111, 112], [112, 113], [113, 114], [114, 115], [115, 116], [116, 117], [117, 118], [118, 119], [119, 120], [120, 121], [121, 122], [122, 123], [123, 124], [124, 125], [125, 126], [126, 127], [127, 128], [128, 129], [129, 130], [130, 131], [131, 132]]);;
R:=P177Census(D);;Need(Size(R.F)=528);;
PrintTo("current_c4_descent/132_004.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 132_004 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
