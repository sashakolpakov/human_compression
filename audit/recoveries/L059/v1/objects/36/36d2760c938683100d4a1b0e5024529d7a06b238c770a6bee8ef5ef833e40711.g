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
D:=P177Graph("144_015",144,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132, 134, 136, 138, 140, 142, 144],[[1, 2], [1, 72], [1, 73], [1, 89], [2, 3], [2, 74], [2, 90], [3, 4], [3, 75], [3, 91], [4, 5], [4, 76], [4, 92], [5, 6], [5, 77], [5, 93], [6, 7], [6, 78], [6, 94], [7, 8], [7, 79], [7, 95], [8, 9], [8, 80], [8, 96], [9, 10], [9, 81], [9, 97], [10, 11], [10, 82], [10, 98], [11, 12], [11, 83], [11, 99], [12, 13], [12, 84], [12, 100], [13, 14], [13, 85], [13, 101], [14, 15], [14, 86], [14, 102], [15, 16], [15, 87], [15, 103], [16, 17], [16, 88], [16, 104], [17, 18], [17, 89], [17, 105], [18, 19], [18, 90], [18, 106], [19, 20], [19, 91], [19, 107], [20, 21], [20, 92], [20, 108], [21, 22], [21, 93], [21, 109], [22, 23], [22, 94], [22, 110], [23, 24], [23, 95], [23, 111], [24, 25], [24, 96], [24, 112], [25, 26], [25, 97], [25, 113], [26, 27], [26, 98], [26, 114], [27, 28], [27, 99], [27, 115], [28, 29], [28, 100], [28, 116], [29, 30], [29, 101], [29, 117], [30, 31], [30, 102], [30, 118], [31, 32], [31, 103], [31, 119], [32, 33], [32, 104], [32, 120], [33, 34], [33, 105], [33, 121], [34, 35], [34, 106], [34, 122], [35, 36], [35, 107], [35, 123], [36, 37], [36, 108], [36, 124], [37, 38], [37, 109], [37, 125], [38, 39], [38, 110], [38, 126], [39, 40], [39, 111], [39, 127], [40, 41], [40, 112], [40, 128], [41, 42], [41, 113], [41, 129], [42, 43], [42, 114], [42, 130], [43, 44], [43, 115], [43, 131], [44, 45], [44, 116], [44, 132], [45, 46], [45, 117], [45, 133], [46, 47], [46, 118], [46, 134], [47, 48], [47, 119], [47, 135], [48, 49], [48, 120], [48, 136], [49, 50], [49, 121], [49, 137], [50, 51], [50, 122], [50, 138], [51, 52], [51, 123], [51, 139], [52, 53], [52, 124], [52, 140], [53, 54], [53, 125], [53, 141], [54, 55], [54, 126], [54, 142], [55, 56], [55, 127], [55, 143], [56, 57], [56, 128], [56, 144], [57, 58], [57, 73], [57, 129], [58, 59], [58, 74], [58, 130], [59, 60], [59, 75], [59, 131], [60, 61], [60, 76], [60, 132], [61, 62], [61, 77], [61, 133], [62, 63], [62, 78], [62, 134], [63, 64], [63, 79], [63, 135], [64, 65], [64, 80], [64, 136], [65, 66], [65, 81], [65, 137], [66, 67], [66, 82], [66, 138], [67, 68], [67, 83], [67, 139], [68, 69], [68, 84], [68, 140], [69, 70], [69, 85], [69, 141], [70, 71], [70, 86], [70, 142], [71, 72], [71, 87], [71, 143], [72, 88], [72, 144], [73, 92], [73, 126], [74, 93], [74, 127], [75, 94], [75, 128], [76, 95], [76, 129], [77, 96], [77, 130], [78, 97], [78, 131], [79, 98], [79, 132], [80, 99], [80, 133], [81, 100], [81, 134], [82, 101], [82, 135], [83, 102], [83, 136], [84, 103], [84, 137], [85, 104], [85, 138], [86, 105], [86, 139], [87, 106], [87, 140], [88, 107], [88, 141], [89, 108], [89, 142], [90, 109], [90, 143], [91, 110], [91, 144], [92, 111], [93, 112], [94, 113], [95, 114], [96, 115], [97, 116], [98, 117], [99, 118], [100, 119], [101, 120], [102, 121], [103, 122], [104, 123], [105, 124], [106, 125], [107, 126], [108, 127], [109, 128], [110, 129], [111, 130], [112, 131], [113, 132], [114, 133], [115, 134], [116, 135], [117, 136], [118, 137], [119, 138], [120, 139], [121, 140], [122, 141], [123, 142], [124, 143], [125, 144]]);;
R:=P177Census(D);;Need(Size(R.F)=1152);;
PrintTo("current_c4_descent/144_015.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_015 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
