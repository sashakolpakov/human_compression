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
D:=P177Graph("144_013",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120],[[1, 25], [1, 48], [1, 129], [1, 136], [2, 25], [2, 26], [2, 130], [2, 137], [3, 26], [3, 27], [3, 131], [3, 138], [4, 27], [4, 28], [4, 132], [4, 139], [5, 28], [5, 29], [5, 133], [5, 140], [6, 29], [6, 30], [6, 134], [6, 141], [7, 30], [7, 31], [7, 135], [7, 142], [8, 31], [8, 32], [8, 136], [8, 143], [9, 32], [9, 33], [9, 137], [9, 144], [10, 33], [10, 34], [10, 121], [10, 138], [11, 34], [11, 35], [11, 122], [11, 139], [12, 35], [12, 36], [12, 123], [12, 140], [13, 36], [13, 37], [13, 124], [13, 141], [14, 37], [14, 38], [14, 125], [14, 142], [15, 38], [15, 39], [15, 126], [15, 143], [16, 39], [16, 40], [16, 127], [16, 144], [17, 40], [17, 41], [17, 121], [17, 128], [18, 41], [18, 42], [18, 122], [18, 129], [19, 42], [19, 43], [19, 123], [19, 130], [20, 43], [20, 44], [20, 124], [20, 131], [21, 44], [21, 45], [21, 125], [21, 132], [22, 45], [22, 46], [22, 126], [22, 133], [23, 46], [23, 47], [23, 127], [23, 134], [24, 47], [24, 48], [24, 128], [24, 135], [25, 58], [25, 65], [26, 59], [26, 66], [27, 60], [27, 67], [28, 61], [28, 68], [29, 62], [29, 69], [30, 63], [30, 70], [31, 64], [31, 71], [32, 65], [32, 72], [33, 49], [33, 66], [34, 50], [34, 67], [35, 51], [35, 68], [36, 52], [36, 69], [37, 53], [37, 70], [38, 54], [38, 71], [39, 55], [39, 72], [40, 49], [40, 56], [41, 50], [41, 57], [42, 51], [42, 58], [43, 52], [43, 59], [44, 53], [44, 60], [45, 54], [45, 61], [46, 55], [46, 62], [47, 56], [47, 63], [48, 57], [48, 64], [49, 73], [49, 96], [50, 73], [50, 74], [51, 74], [51, 75], [52, 75], [52, 76], [53, 76], [53, 77], [54, 77], [54, 78], [55, 78], [55, 79], [56, 79], [56, 80], [57, 80], [57, 81], [58, 81], [58, 82], [59, 82], [59, 83], [60, 83], [60, 84], [61, 84], [61, 85], [62, 85], [62, 86], [63, 86], [63, 87], [64, 87], [64, 88], [65, 88], [65, 89], [66, 89], [66, 90], [67, 90], [67, 91], [68, 91], [68, 92], [69, 92], [69, 93], [70, 93], [70, 94], [71, 94], [71, 95], [72, 95], [72, 96], [73, 106], [73, 113], [74, 107], [74, 114], [75, 108], [75, 115], [76, 109], [76, 116], [77, 110], [77, 117], [78, 111], [78, 118], [79, 112], [79, 119], [80, 113], [80, 120], [81, 97], [81, 114], [82, 98], [82, 115], [83, 99], [83, 116], [84, 100], [84, 117], [85, 101], [85, 118], [86, 102], [86, 119], [87, 103], [87, 120], [88, 97], [88, 104], [89, 98], [89, 105], [90, 99], [90, 106], [91, 100], [91, 107], [92, 101], [92, 108], [93, 102], [93, 109], [94, 103], [94, 110], [95, 104], [95, 111], [96, 105], [96, 112], [97, 121], [97, 144], [98, 121], [98, 122], [99, 122], [99, 123], [100, 123], [100, 124], [101, 124], [101, 125], [102, 125], [102, 126], [103, 126], [103, 127], [104, 127], [104, 128], [105, 128], [105, 129], [106, 129], [106, 130], [107, 130], [107, 131], [108, 131], [108, 132], [109, 132], [109, 133], [110, 133], [110, 134], [111, 134], [111, 135], [112, 135], [112, 136], [113, 136], [113, 137], [114, 137], [114, 138], [115, 138], [115, 139], [116, 139], [116, 140], [117, 140], [117, 141], [118, 141], [118, 142], [119, 142], [119, 143], [120, 143], [120, 144]]);;
R:=P177Census(D);;Need(Size(R.F)=1152);;
PrintTo("current_c4_descent/144_013.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_013 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
