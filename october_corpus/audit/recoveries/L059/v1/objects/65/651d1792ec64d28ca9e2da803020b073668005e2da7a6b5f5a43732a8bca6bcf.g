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
D:=P177Graph("144_071",144,[1, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144],[[1, 2], [1, 3], [1, 4], [1, 5], [2, 133], [2, 137], [2, 138], [3, 134], [3, 139], [3, 140], [4, 136], [4, 142], [4, 144], [5, 135], [5, 141], [5, 143], [6, 10], [6, 14], [6, 74], [6, 77], [7, 11], [7, 15], [7, 74], [7, 76], [8, 12], [8, 17], [8, 75], [8, 77], [9, 13], [9, 16], [9, 75], [9, 76], [10, 46], [10, 48], [10, 129], [11, 47], [11, 49], [11, 130], [12, 55], [12, 57], [12, 130], [13, 54], [13, 56], [13, 129], [14, 43], [14, 52], [14, 132], [15, 42], [15, 53], [15, 131], [16, 45], [16, 51], [16, 132], [17, 44], [17, 50], [17, 131], [18, 44], [18, 49], [18, 53], [18, 57], [19, 45], [19, 48], [19, 52], [19, 56], [20, 43], [20, 46], [20, 51], [20, 54], [21, 42], [21, 47], [21, 50], [21, 55], [22, 26], [22, 30], [22, 31], [22, 32], [23, 27], [23, 35], [23, 36], [23, 37], [24, 28], [24, 33], [24, 40], [24, 41], [25, 29], [25, 34], [25, 38], [25, 39], [26, 58], [26, 78], [26, 86], [27, 59], [27, 79], [27, 86], [28, 62], [28, 79], [28, 87], [29, 65], [29, 78], [29, 87], [30, 64], [30, 80], [30, 91], [31, 67], [31, 84], [31, 93], [32, 66], [32, 85], [32, 92], [33, 63], [33, 81], [33, 88], [34, 61], [34, 80], [34, 88], [35, 60], [35, 81], [35, 91], [36, 71], [36, 82], [36, 93], [37, 70], [37, 83], [37, 92], [38, 69], [38, 84], [38, 90], [39, 68], [39, 85], [39, 89], [40, 72], [40, 83], [40, 89], [41, 73], [41, 82], [41, 90], [42, 63], [42, 73], [43, 63], [43, 72], [44, 64], [44, 67], [45, 64], [45, 66], [46, 58], [46, 67], [47, 58], [47, 66], [48, 59], [48, 71], [49, 59], [49, 70], [50, 60], [50, 71], [51, 60], [51, 70], [52, 61], [52, 68], [53, 61], [53, 69], [54, 65], [54, 69], [55, 65], [55, 68], [56, 62], [56, 73], [57, 62], [57, 72], [58, 124], [59, 117], [60, 116], [61, 113], [62, 121], [63, 114], [64, 115], [65, 120], [66, 126], [67, 125], [68, 123], [69, 122], [70, 119], [71, 118], [72, 128], [73, 127], [74, 105], [74, 107], [75, 106], [75, 110], [76, 109], [76, 111], [77, 108], [77, 112], [78, 114], [78, 116], [79, 113], [79, 115], [80, 117], [80, 121], [81, 120], [81, 124], [82, 123], [82, 126], [83, 122], [83, 125], [84, 119], [84, 128], [85, 118], [85, 127], [86, 101], [86, 105], [87, 101], [87, 106], [88, 102], [88, 107], [89, 104], [89, 108], [90, 103], [90, 109], [91, 102], [91, 110], [92, 104], [92, 111], [93, 103], [93, 112], [94, 116], [94, 117], [94, 118], [94, 119], [95, 113], [95, 120], [95, 122], [95, 123], [96, 114], [96, 121], [96, 127], [96, 128], [97, 115], [97, 124], [97, 125], [97, 126], [98, 105], [98, 110], [98, 111], [98, 112], [99, 106], [99, 107], [99, 108], [99, 109], [100, 101], [100, 102], [100, 103], [100, 104], [101, 134], [102, 133], [103, 136], [104, 135], [105, 137], [106, 138], [107, 139], [108, 142], [109, 141], [110, 140], [111, 144], [112, 143], [113, 137], [114, 137], [115, 138], [116, 138], [117, 139], [118, 142], [119, 141], [120, 140], [121, 140], [122, 144], [123, 143], [124, 139], [125, 142], [126, 141], [127, 144], [128, 143], [129, 134], [129, 136], [130, 134], [130, 135], [131, 133], [131, 136], [132, 133], [132, 135]]);;
R:=P177Census(D);;Need(Size(R.F)=2304);;
PrintTo("current_c4_descent/144_071.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_071 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
