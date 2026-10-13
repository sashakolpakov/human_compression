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
D:=P177Graph("128_002",128,[1, 3, 5, 7, 9, 11, 13, 15, 18, 20, 22, 24, 26, 28, 30, 32, 33, 35, 37, 39, 41, 43, 45, 47, 50, 52, 54, 56, 58, 60, 62, 64, 65, 67, 69, 71, 73, 75, 77, 79, 82, 84, 86, 88, 90, 92, 94, 96, 97, 99, 101, 103, 105, 107, 109, 111, 114, 116, 118, 120, 122, 124, 126, 128],[[1, 2], [1, 16], [1, 17], [1, 121], [2, 3], [2, 18], [2, 122], [3, 4], [3, 19], [3, 123], [4, 5], [4, 20], [4, 124], [5, 6], [5, 21], [5, 125], [6, 7], [6, 22], [6, 126], [7, 8], [7, 23], [7, 127], [8, 9], [8, 24], [8, 128], [9, 10], [9, 25], [9, 113], [10, 11], [10, 26], [10, 114], [11, 12], [11, 27], [11, 115], [12, 13], [12, 28], [12, 116], [13, 14], [13, 29], [13, 117], [14, 15], [14, 30], [14, 118], [15, 16], [15, 31], [15, 119], [16, 32], [16, 120], [17, 18], [17, 32], [17, 33], [18, 19], [18, 34], [19, 20], [19, 35], [20, 21], [20, 36], [21, 22], [21, 37], [22, 23], [22, 38], [23, 24], [23, 39], [24, 25], [24, 40], [25, 26], [25, 41], [26, 27], [26, 42], [27, 28], [27, 43], [28, 29], [28, 44], [29, 30], [29, 45], [30, 31], [30, 46], [31, 32], [31, 47], [32, 48], [33, 34], [33, 48], [33, 49], [34, 35], [34, 50], [35, 36], [35, 51], [36, 37], [36, 52], [37, 38], [37, 53], [38, 39], [38, 54], [39, 40], [39, 55], [40, 41], [40, 56], [41, 42], [41, 57], [42, 43], [42, 58], [43, 44], [43, 59], [44, 45], [44, 60], [45, 46], [45, 61], [46, 47], [46, 62], [47, 48], [47, 63], [48, 64], [49, 50], [49, 64], [49, 65], [50, 51], [50, 66], [51, 52], [51, 67], [52, 53], [52, 68], [53, 54], [53, 69], [54, 55], [54, 70], [55, 56], [55, 71], [56, 57], [56, 72], [57, 58], [57, 73], [58, 59], [58, 74], [59, 60], [59, 75], [60, 61], [60, 76], [61, 62], [61, 77], [62, 63], [62, 78], [63, 64], [63, 79], [64, 80], [65, 66], [65, 80], [65, 81], [66, 67], [66, 82], [67, 68], [67, 83], [68, 69], [68, 84], [69, 70], [69, 85], [70, 71], [70, 86], [71, 72], [71, 87], [72, 73], [72, 88], [73, 74], [73, 89], [74, 75], [74, 90], [75, 76], [75, 91], [76, 77], [76, 92], [77, 78], [77, 93], [78, 79], [78, 94], [79, 80], [79, 95], [80, 96], [81, 82], [81, 96], [81, 97], [82, 83], [82, 98], [83, 84], [83, 99], [84, 85], [84, 100], [85, 86], [85, 101], [86, 87], [86, 102], [87, 88], [87, 103], [88, 89], [88, 104], [89, 90], [89, 105], [90, 91], [90, 106], [91, 92], [91, 107], [92, 93], [92, 108], [93, 94], [93, 109], [94, 95], [94, 110], [95, 96], [95, 111], [96, 112], [97, 98], [97, 112], [97, 113], [98, 99], [98, 114], [99, 100], [99, 115], [100, 101], [100, 116], [101, 102], [101, 117], [102, 103], [102, 118], [103, 104], [103, 119], [104, 105], [104, 120], [105, 106], [105, 121], [106, 107], [106, 122], [107, 108], [107, 123], [108, 109], [108, 124], [109, 110], [109, 125], [110, 111], [110, 126], [111, 112], [111, 127], [112, 128], [113, 114], [113, 128], [114, 115], [115, 116], [116, 117], [117, 118], [118, 119], [119, 120], [120, 121], [121, 122], [122, 123], [123, 124], [124, 125], [125, 126], [126, 127], [127, 128]]);;
R:=P177Census(D);;Need(Size(R.F)=1024);;
PrintTo("current_c4_descent/128_002.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_002 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
