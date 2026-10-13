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
D:=P177Graph("144_012",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120],[[1, 25], [1, 48], [1, 124], [1, 141], [2, 25], [2, 26], [2, 125], [2, 142], [3, 26], [3, 27], [3, 126], [3, 143], [4, 27], [4, 28], [4, 127], [4, 144], [5, 28], [5, 29], [5, 121], [5, 128], [6, 29], [6, 30], [6, 122], [6, 129], [7, 30], [7, 31], [7, 123], [7, 130], [8, 31], [8, 32], [8, 124], [8, 131], [9, 32], [9, 33], [9, 125], [9, 132], [10, 33], [10, 34], [10, 126], [10, 133], [11, 34], [11, 35], [11, 127], [11, 134], [12, 35], [12, 36], [12, 128], [12, 135], [13, 36], [13, 37], [13, 129], [13, 136], [14, 37], [14, 38], [14, 130], [14, 137], [15, 38], [15, 39], [15, 131], [15, 138], [16, 39], [16, 40], [16, 132], [16, 139], [17, 40], [17, 41], [17, 133], [17, 140], [18, 41], [18, 42], [18, 134], [18, 141], [19, 42], [19, 43], [19, 135], [19, 142], [20, 43], [20, 44], [20, 136], [20, 143], [21, 44], [21, 45], [21, 137], [21, 144], [22, 45], [22, 46], [22, 121], [22, 138], [23, 46], [23, 47], [23, 122], [23, 139], [24, 47], [24, 48], [24, 123], [24, 140], [25, 53], [25, 70], [26, 54], [26, 71], [27, 55], [27, 72], [28, 49], [28, 56], [29, 50], [29, 57], [30, 51], [30, 58], [31, 52], [31, 59], [32, 53], [32, 60], [33, 54], [33, 61], [34, 55], [34, 62], [35, 56], [35, 63], [36, 57], [36, 64], [37, 58], [37, 65], [38, 59], [38, 66], [39, 60], [39, 67], [40, 61], [40, 68], [41, 62], [41, 69], [42, 63], [42, 70], [43, 64], [43, 71], [44, 65], [44, 72], [45, 49], [45, 66], [46, 50], [46, 67], [47, 51], [47, 68], [48, 52], [48, 69], [49, 73], [49, 96], [50, 73], [50, 74], [51, 74], [51, 75], [52, 75], [52, 76], [53, 76], [53, 77], [54, 77], [54, 78], [55, 78], [55, 79], [56, 79], [56, 80], [57, 80], [57, 81], [58, 81], [58, 82], [59, 82], [59, 83], [60, 83], [60, 84], [61, 84], [61, 85], [62, 85], [62, 86], [63, 86], [63, 87], [64, 87], [64, 88], [65, 88], [65, 89], [66, 89], [66, 90], [67, 90], [67, 91], [68, 91], [68, 92], [69, 92], [69, 93], [70, 93], [70, 94], [71, 94], [71, 95], [72, 95], [72, 96], [73, 101], [73, 118], [74, 102], [74, 119], [75, 103], [75, 120], [76, 97], [76, 104], [77, 98], [77, 105], [78, 99], [78, 106], [79, 100], [79, 107], [80, 101], [80, 108], [81, 102], [81, 109], [82, 103], [82, 110], [83, 104], [83, 111], [84, 105], [84, 112], [85, 106], [85, 113], [86, 107], [86, 114], [87, 108], [87, 115], [88, 109], [88, 116], [89, 110], [89, 117], [90, 111], [90, 118], [91, 112], [91, 119], [92, 113], [92, 120], [93, 97], [93, 114], [94, 98], [94, 115], [95, 99], [95, 116], [96, 100], [96, 117], [97, 121], [97, 144], [98, 121], [98, 122], [99, 122], [99, 123], [100, 123], [100, 124], [101, 124], [101, 125], [102, 125], [102, 126], [103, 126], [103, 127], [104, 127], [104, 128], [105, 128], [105, 129], [106, 129], [106, 130], [107, 130], [107, 131], [108, 131], [108, 132], [109, 132], [109, 133], [110, 133], [110, 134], [111, 134], [111, 135], [112, 135], [112, 136], [113, 136], [113, 137], [114, 137], [114, 138], [115, 138], [115, 139], [116, 139], [116, 140], [117, 140], [117, 141], [118, 141], [118, 142], [119, 142], [119, 143], [120, 143], [120, 144]]);;
R:=P177Census(D);;Need(Size(R.F)=1152);;
PrintTo("current_c4_descent/144_012.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_012 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
