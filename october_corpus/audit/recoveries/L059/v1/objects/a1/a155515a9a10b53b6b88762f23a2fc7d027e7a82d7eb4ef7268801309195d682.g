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
D:=P177Graph("128_004",128,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128],[[1, 2], [1, 32], [1, 33], [1, 101], [2, 3], [2, 34], [2, 102], [3, 4], [3, 35], [3, 103], [4, 5], [4, 36], [4, 104], [5, 6], [5, 37], [5, 105], [6, 7], [6, 38], [6, 106], [7, 8], [7, 39], [7, 107], [8, 9], [8, 40], [8, 108], [9, 10], [9, 41], [9, 109], [10, 11], [10, 42], [10, 110], [11, 12], [11, 43], [11, 111], [12, 13], [12, 44], [12, 112], [13, 14], [13, 45], [13, 113], [14, 15], [14, 46], [14, 114], [15, 16], [15, 47], [15, 115], [16, 17], [16, 48], [16, 116], [17, 18], [17, 49], [17, 117], [18, 19], [18, 50], [18, 118], [19, 20], [19, 51], [19, 119], [20, 21], [20, 52], [20, 120], [21, 22], [21, 53], [21, 121], [22, 23], [22, 54], [22, 122], [23, 24], [23, 55], [23, 123], [24, 25], [24, 56], [24, 124], [25, 26], [25, 57], [25, 125], [26, 27], [26, 58], [26, 126], [27, 28], [27, 59], [27, 127], [28, 29], [28, 60], [28, 128], [29, 30], [29, 61], [29, 97], [30, 31], [30, 62], [30, 98], [31, 32], [31, 63], [31, 99], [32, 64], [32, 100], [33, 34], [33, 64], [33, 65], [34, 35], [34, 66], [35, 36], [35, 67], [36, 37], [36, 68], [37, 38], [37, 69], [38, 39], [38, 70], [39, 40], [39, 71], [40, 41], [40, 72], [41, 42], [41, 73], [42, 43], [42, 74], [43, 44], [43, 75], [44, 45], [44, 76], [45, 46], [45, 77], [46, 47], [46, 78], [47, 48], [47, 79], [48, 49], [48, 80], [49, 50], [49, 81], [50, 51], [50, 82], [51, 52], [51, 83], [52, 53], [52, 84], [53, 54], [53, 85], [54, 55], [54, 86], [55, 56], [55, 87], [56, 57], [56, 88], [57, 58], [57, 89], [58, 59], [58, 90], [59, 60], [59, 91], [60, 61], [60, 92], [61, 62], [61, 93], [62, 63], [62, 94], [63, 64], [63, 95], [64, 96], [65, 66], [65, 96], [65, 97], [66, 67], [66, 98], [67, 68], [67, 99], [68, 69], [68, 100], [69, 70], [69, 101], [70, 71], [70, 102], [71, 72], [71, 103], [72, 73], [72, 104], [73, 74], [73, 105], [74, 75], [74, 106], [75, 76], [75, 107], [76, 77], [76, 108], [77, 78], [77, 109], [78, 79], [78, 110], [79, 80], [79, 111], [80, 81], [80, 112], [81, 82], [81, 113], [82, 83], [82, 114], [83, 84], [83, 115], [84, 85], [84, 116], [85, 86], [85, 117], [86, 87], [86, 118], [87, 88], [87, 119], [88, 89], [88, 120], [89, 90], [89, 121], [90, 91], [90, 122], [91, 92], [91, 123], [92, 93], [92, 124], [93, 94], [93, 125], [94, 95], [94, 126], [95, 96], [95, 127], [96, 128], [97, 98], [97, 128], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108], [108, 109], [109, 110], [110, 111], [111, 112], [112, 113], [113, 114], [114, 115], [115, 116], [116, 117], [117, 118], [118, 119], [119, 120], [120, 121], [121, 122], [122, 123], [123, 124], [124, 125], [125, 126], [126, 127], [127, 128]]);;
R:=P177Census(D);;Need(Size(R.F)=512);;
PrintTo("current_c4_descent/128_004.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_004 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
