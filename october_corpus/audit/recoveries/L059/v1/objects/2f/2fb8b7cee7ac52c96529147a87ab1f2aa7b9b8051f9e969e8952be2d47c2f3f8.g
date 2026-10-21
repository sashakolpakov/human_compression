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
D:=P177Graph("128_031",128,[1, 3, 5, 8, 9, 11, 12, 13, 14, 16, 19, 25, 27, 28, 30, 31, 32, 33, 35, 37, 39, 40, 43, 48, 50, 52, 55, 56, 58, 59, 60, 61, 64, 67, 69, 70, 77, 78, 80, 81, 83, 86, 87, 88, 89, 90, 93, 96, 97, 98, 103, 104, 106, 107, 111, 112, 117, 118, 119, 120, 121, 122, 127, 128],[[1, 2], [1, 4], [1, 73], [1, 76], [2, 5], [2, 8], [2, 88], [3, 6], [3, 7], [3, 57], [3, 72], [4, 9], [4, 14], [4, 98], [5, 10], [5, 15], [5, 101], [6, 11], [6, 16], [6, 93], [7, 12], [7, 13], [7, 87], [8, 17], [8, 24], [8, 110], [9, 17], [9, 18], [9, 102], [10, 19], [10, 25], [10, 112], [11, 20], [11, 21], [11, 99], [12, 21], [12, 26], [12, 105], [13, 22], [13, 23], [13, 100], [14, 15], [14, 34], [14, 115], [15, 27], [15, 35], [16, 22], [16, 36], [16, 114], [17, 27], [17, 28], [18, 19], [18, 37], [18, 118], [19, 29], [19, 38], [20, 30], [20, 39], [20, 117], [21, 31], [21, 32], [22, 32], [22, 40], [23, 30], [23, 33], [23, 111], [24, 25], [24, 48], [24, 121], [25, 41], [25, 49], [26, 33], [26, 50], [26, 120], [27, 41], [27, 42], [28, 29], [28, 51], [28, 124], [29, 43], [29, 52], [30, 44], [30, 45], [31, 45], [31, 53], [31, 123], [32, 46], [32, 47], [33, 47], [33, 54], [34, 37], [34, 48], [34, 122], [35, 38], [35, 62], [35, 126], [36, 39], [36, 50], [36, 119], [37, 42], [37, 63], [38, 55], [38, 64], [39, 46], [39, 65], [40, 44], [40, 66], [40, 125], [41, 55], [41, 56], [42, 43], [42, 67], [43, 57], [43, 68], [44, 58], [44, 69], [45, 59], [45, 60], [46, 60], [46, 70], [47, 58], [47, 61], [48, 51], [48, 62], [49, 52], [49, 77], [49, 128], [50, 53], [50, 66], [51, 56], [51, 78], [52, 71], [52, 79], [53, 61], [53, 80], [54, 59], [54, 81], [54, 127], [55, 71], [55, 72], [56, 57], [56, 82], [57, 83], [58, 73], [58, 74], [59, 74], [59, 84], [60, 75], [60, 76], [61, 76], [61, 85], [62, 67], [62, 77], [63, 64], [63, 78], [63, 128], [64, 68], [64, 91], [65, 69], [65, 80], [65, 127], [66, 70], [66, 81], [67, 72], [67, 92], [68, 86], [68, 93], [69, 75], [69, 94], [70, 73], [70, 95], [71, 86], [71, 87], [72, 96], [73, 97], [74, 88], [74, 89], [75, 89], [75, 98], [76, 90], [77, 82], [77, 91], [78, 79], [78, 92], [79, 83], [79, 103], [80, 84], [80, 95], [81, 85], [81, 94], [82, 87], [82, 104], [83, 99], [83, 105], [84, 90], [84, 106], [85, 88], [85, 107], [86, 99], [86, 100], [87, 108], [88, 109], [89, 101], [89, 102], [90, 102], [90, 110], [91, 96], [91, 103], [92, 93], [92, 104], [93, 113], [94, 97], [94, 106], [95, 98], [95, 107], [96, 100], [96, 114], [97, 101], [97, 115], [98, 116], [99, 111], [100, 117], [101, 118], [102, 112], [103, 108], [103, 113], [104, 105], [104, 114], [105, 119], [106, 109], [106, 116], [107, 110], [107, 115], [108, 111], [108, 120], [109, 112], [109, 121], [110, 122], [111, 123], [112, 124], [113, 117], [113, 119], [114, 120], [115, 121], [116, 118], [116, 122], [117, 125], [118, 126], [119, 123], [120, 125], [121, 126], [122, 124], [123, 127], [124, 128], [125, 127], [126, 128]]);;
R:=P177Census(D);;Need(Size(R.F)=1024);;
PrintTo("current_c4_descent/128_031.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_031 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
