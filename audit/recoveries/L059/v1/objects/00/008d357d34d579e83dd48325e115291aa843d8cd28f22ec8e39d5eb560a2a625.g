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
D:=P177Graph("128_005",128,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128],[[1, 2], [1, 64], [1, 65], [1, 99], [2, 3], [2, 66], [2, 100], [3, 4], [3, 67], [3, 101], [4, 5], [4, 68], [4, 102], [5, 6], [5, 69], [5, 103], [6, 7], [6, 70], [6, 104], [7, 8], [7, 71], [7, 105], [8, 9], [8, 72], [8, 106], [9, 10], [9, 73], [9, 107], [10, 11], [10, 74], [10, 108], [11, 12], [11, 75], [11, 109], [12, 13], [12, 76], [12, 110], [13, 14], [13, 77], [13, 111], [14, 15], [14, 78], [14, 112], [15, 16], [15, 79], [15, 113], [16, 17], [16, 80], [16, 114], [17, 18], [17, 81], [17, 115], [18, 19], [18, 82], [18, 116], [19, 20], [19, 83], [19, 117], [20, 21], [20, 84], [20, 118], [21, 22], [21, 85], [21, 119], [22, 23], [22, 86], [22, 120], [23, 24], [23, 87], [23, 121], [24, 25], [24, 88], [24, 122], [25, 26], [25, 89], [25, 123], [26, 27], [26, 90], [26, 124], [27, 28], [27, 91], [27, 125], [28, 29], [28, 92], [28, 126], [29, 30], [29, 93], [29, 127], [30, 31], [30, 94], [30, 128], [31, 32], [31, 65], [31, 95], [32, 33], [32, 66], [32, 96], [33, 34], [33, 67], [33, 97], [34, 35], [34, 68], [34, 98], [35, 36], [35, 69], [35, 99], [36, 37], [36, 70], [36, 100], [37, 38], [37, 71], [37, 101], [38, 39], [38, 72], [38, 102], [39, 40], [39, 73], [39, 103], [40, 41], [40, 74], [40, 104], [41, 42], [41, 75], [41, 105], [42, 43], [42, 76], [42, 106], [43, 44], [43, 77], [43, 107], [44, 45], [44, 78], [44, 108], [45, 46], [45, 79], [45, 109], [46, 47], [46, 80], [46, 110], [47, 48], [47, 81], [47, 111], [48, 49], [48, 82], [48, 112], [49, 50], [49, 83], [49, 113], [50, 51], [50, 84], [50, 114], [51, 52], [51, 85], [51, 115], [52, 53], [52, 86], [52, 116], [53, 54], [53, 87], [53, 117], [54, 55], [54, 88], [54, 118], [55, 56], [55, 89], [55, 119], [56, 57], [56, 90], [56, 120], [57, 58], [57, 91], [57, 121], [58, 59], [58, 92], [58, 122], [59, 60], [59, 93], [59, 123], [60, 61], [60, 94], [60, 124], [61, 62], [61, 95], [61, 125], [62, 63], [62, 96], [62, 126], [63, 64], [63, 97], [63, 127], [64, 98], [64, 128], [65, 66], [65, 128], [66, 67], [67, 68], [68, 69], [69, 70], [70, 71], [71, 72], [72, 73], [73, 74], [74, 75], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80], [80, 81], [81, 82], [82, 83], [83, 84], [84, 85], [85, 86], [86, 87], [87, 88], [88, 89], [89, 90], [90, 91], [91, 92], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108], [108, 109], [109, 110], [110, 111], [111, 112], [112, 113], [113, 114], [114, 115], [115, 116], [116, 117], [117, 118], [118, 119], [119, 120], [120, 121], [121, 122], [122, 123], [123, 124], [124, 125], [125, 126], [126, 127], [127, 128]]);;
R:=P177Census(D);;Need(Size(R.F)=512);;
PrintTo("current_c4_descent/128_005.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_005 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
