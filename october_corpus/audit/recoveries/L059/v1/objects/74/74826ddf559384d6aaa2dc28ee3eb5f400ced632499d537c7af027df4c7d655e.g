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
D:=P177Graph("144_060",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120],[[1, 25], [1, 28], [1, 131], [1, 132], [2, 29], [2, 32], [2, 129], [2, 130], [3, 26], [3, 27], [3, 135], [3, 136], [4, 30], [4, 31], [4, 133], [4, 134], [5, 25], [5, 26], [5, 138], [5, 139], [6, 27], [6, 28], [6, 142], [6, 143], [7, 29], [7, 30], [7, 137], [7, 140], [8, 31], [8, 32], [8, 141], [8, 144], [9, 33], [9, 36], [9, 139], [9, 140], [10, 37], [10, 40], [10, 137], [10, 138], [11, 34], [11, 35], [11, 143], [11, 144], [12, 38], [12, 39], [12, 141], [12, 142], [13, 33], [13, 34], [13, 122], [13, 123], [14, 35], [14, 36], [14, 126], [14, 127], [15, 37], [15, 38], [15, 121], [15, 124], [16, 39], [16, 40], [16, 125], [16, 128], [17, 41], [17, 44], [17, 123], [17, 124], [18, 45], [18, 48], [18, 121], [18, 122], [19, 42], [19, 43], [19, 127], [19, 128], [20, 46], [20, 47], [20, 125], [20, 126], [21, 41], [21, 42], [21, 130], [21, 131], [22, 43], [22, 44], [22, 134], [22, 135], [23, 45], [23, 46], [23, 129], [23, 132], [24, 47], [24, 48], [24, 133], [24, 136], [25, 63], [25, 66], [26, 61], [26, 66], [27, 61], [27, 65], [28, 63], [28, 65], [29, 64], [29, 68], [30, 62], [30, 68], [31, 62], [31, 67], [32, 64], [32, 67], [33, 50], [33, 71], [34, 50], [34, 69], [35, 49], [35, 69], [36, 49], [36, 71], [37, 52], [37, 72], [38, 52], [38, 70], [39, 51], [39, 70], [40, 51], [40, 72], [41, 55], [41, 58], [42, 53], [42, 58], [43, 53], [43, 57], [44, 55], [44, 57], [45, 56], [45, 60], [46, 54], [46, 60], [47, 54], [47, 59], [48, 56], [48, 59], [49, 73], [49, 76], [50, 77], [50, 80], [51, 74], [51, 75], [52, 78], [52, 79], [53, 73], [53, 74], [54, 75], [54, 76], [55, 77], [55, 78], [56, 79], [56, 80], [57, 81], [57, 84], [58, 85], [58, 88], [59, 82], [59, 83], [60, 86], [60, 87], [61, 81], [61, 82], [62, 83], [62, 84], [63, 85], [63, 86], [64, 87], [64, 88], [65, 89], [65, 92], [66, 93], [66, 96], [67, 90], [67, 91], [68, 94], [68, 95], [69, 89], [69, 90], [70, 91], [70, 92], [71, 93], [71, 94], [72, 95], [72, 96], [73, 111], [73, 114], [74, 109], [74, 114], [75, 109], [75, 113], [76, 111], [76, 113], [77, 112], [77, 116], [78, 110], [78, 116], [79, 110], [79, 115], [80, 112], [80, 115], [81, 98], [81, 119], [82, 98], [82, 117], [83, 97], [83, 117], [84, 97], [84, 119], [85, 100], [85, 120], [86, 100], [86, 118], [87, 99], [87, 118], [88, 99], [88, 120], [89, 103], [89, 106], [90, 101], [90, 106], [91, 101], [91, 105], [92, 103], [92, 105], [93, 104], [93, 108], [94, 102], [94, 108], [95, 102], [95, 107], [96, 104], [96, 107], [97, 121], [97, 124], [98, 125], [98, 128], [99, 122], [99, 123], [100, 126], [100, 127], [101, 121], [101, 122], [102, 123], [102, 124], [103, 125], [103, 126], [104, 127], [104, 128], [105, 129], [105, 132], [106, 133], [106, 136], [107, 130], [107, 131], [108, 134], [108, 135], [109, 129], [109, 130], [110, 131], [110, 132], [111, 133], [111, 134], [112, 135], [112, 136], [113, 137], [113, 140], [114, 141], [114, 144], [115, 138], [115, 139], [116, 142], [116, 143], [117, 137], [117, 138], [118, 139], [118, 140], [119, 141], [119, 142], [120, 143], [120, 144]]);;
R:=P177Census(D);;Need(Size(R.F)=288);;
PrintTo("current_c4_descent/144_060.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_060 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
