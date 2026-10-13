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
D:=P177Graph("144_073",144,[1, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144],[[1, 2], [1, 3], [1, 4], [1, 5], [2, 135], [2, 136], [2, 143], [3, 139], [3, 142], [3, 144], [4, 140], [4, 141], [4, 144], [5, 137], [5, 138], [5, 143], [6, 20], [6, 21], [6, 28], [6, 29], [7, 22], [7, 23], [7, 28], [7, 29], [8, 15], [8, 17], [8, 18], [8, 30], [9, 15], [9, 16], [9, 19], [9, 30], [10, 14], [10, 17], [10, 18], [10, 31], [11, 14], [11, 16], [11, 19], [11, 31], [12, 20], [12, 21], [12, 143], [12, 144], [13, 22], [13, 23], [13, 143], [13, 144], [14, 131], [14, 134], [15, 132], [15, 133], [16, 80], [16, 85], [17, 81], [17, 82], [18, 79], [18, 83], [19, 84], [19, 86], [20, 73], [20, 78], [21, 71], [21, 75], [22, 72], [22, 76], [23, 74], [23, 77], [24, 71], [24, 73], [24, 75], [24, 78], [25, 72], [25, 74], [25, 76], [25, 77], [26, 80], [26, 84], [26, 85], [26, 86], [27, 79], [27, 81], [27, 82], [27, 83], [28, 35], [28, 38], [29, 36], [29, 37], [30, 41], [30, 42], [31, 39], [31, 40], [32, 39], [32, 40], [32, 131], [32, 134], [33, 41], [33, 42], [33, 132], [33, 133], [34, 35], [34, 36], [34, 37], [34, 38], [35, 43], [35, 48], [36, 44], [36, 47], [37, 45], [37, 46], [38, 49], [38, 50], [39, 44], [39, 47], [40, 45], [40, 46], [41, 43], [41, 48], [42, 49], [42, 50], [43, 55], [43, 57], [44, 56], [44, 59], [45, 58], [45, 67], [46, 65], [46, 66], [47, 61], [47, 62], [48, 63], [48, 64], [49, 60], [49, 68], [50, 69], [50, 70], [51, 55], [51, 57], [51, 63], [51, 64], [52, 56], [52, 59], [52, 61], [52, 62], [53, 58], [53, 65], [53, 66], [53, 67], [54, 60], [54, 68], [54, 69], [54, 70], [55, 87], [55, 103], [56, 88], [56, 103], [57, 89], [57, 104], [58, 90], [58, 104], [59, 91], [59, 105], [60, 92], [60, 105], [61, 100], [61, 107], [62, 95], [62, 110], [63, 97], [63, 108], [64, 99], [64, 107], [65, 98], [65, 108], [66, 94], [66, 109], [67, 93], [67, 106], [68, 96], [68, 106], [69, 102], [69, 110], [70, 101], [70, 109], [71, 87], [71, 88], [72, 91], [72, 92], [73, 95], [73, 102], [74, 94], [74, 101], [75, 93], [75, 96], [76, 89], [76, 90], [77, 99], [77, 100], [78, 97], [78, 98], [79, 87], [79, 88], [80, 91], [80, 92], [81, 94], [81, 101], [82, 99], [82, 100], [83, 93], [83, 96], [84, 95], [84, 102], [85, 89], [85, 90], [86, 97], [86, 98], [87, 116], [88, 115], [89, 117], [90, 120], [91, 124], [92, 127], [93, 121], [94, 126], [95, 123], [96, 128], [97, 129], [98, 125], [99, 130], [100, 122], [101, 119], [102, 118], [103, 115], [103, 116], [104, 117], [104, 120], [105, 124], [105, 127], [106, 121], [106, 128], [107, 122], [107, 130], [108, 125], [108, 129], [109, 119], [109, 126], [110, 118], [110, 123], [111, 116], [111, 117], [111, 118], [111, 119], [112, 120], [112, 121], [112, 122], [112, 123], [113, 115], [113, 124], [113, 125], [113, 126], [114, 127], [114, 128], [114, 129], [114, 130], [115, 140], [116, 135], [117, 135], [118, 136], [119, 136], [120, 139], [121, 139], [122, 142], [123, 142], [124, 140], [125, 141], [126, 141], [127, 138], [128, 138], [129, 137], [130, 137], [131, 135], [131, 136], [132, 139], [132, 142], [133, 140], [133, 141], [134, 137], [134, 138]]);;
R:=P177Census(D);;Need(Size(R.F)=1152);;
PrintTo("current_c4_descent/144_073.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_073 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
