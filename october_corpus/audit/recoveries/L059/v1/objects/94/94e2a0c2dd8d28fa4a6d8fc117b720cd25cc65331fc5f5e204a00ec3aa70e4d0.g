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
D:=P177Graph("144_043",144,[1, 3, 5, 7, 8, 9, 11, 13, 17, 18, 19, 24, 26, 28, 29, 33, 35, 36, 38, 40, 42, 43, 47, 48, 49, 52, 55, 56, 59, 61, 63, 66, 67, 69, 71, 73, 74, 75, 79, 82, 84, 87, 88, 90, 92, 93, 96, 97, 101, 102, 104, 106, 108, 110, 112, 113, 114, 116, 118, 119, 121, 122, 124, 125, 127, 129, 133, 134, 137, 139, 143, 144],[[1, 2], [1, 4], [1, 30], [1, 34], [2, 5], [2, 9], [2, 63], [3, 6], [3, 10], [3, 57], [3, 64], [4, 11], [4, 19], [4, 102], [5, 12], [5, 20], [5, 103], [6, 13], [6, 18], [6, 104], [7, 14], [7, 21], [7, 70], [7, 105], [8, 14], [8, 15], [8, 16], [8, 22], [9, 23], [9, 39], [9, 100], [10, 24], [10, 40], [10, 134], [11, 25], [11, 41], [11, 120], [12, 26], [12, 42], [12, 134], [13, 27], [13, 37], [13, 135], [14, 28], [14, 97], [15, 29], [15, 33], [15, 38], [16, 43], [16, 106], [16, 112], [17, 20], [17, 30], [17, 44], [17, 136], [18, 31], [18, 32], [18, 45], [19, 46], [19, 72], [19, 83], [20, 73], [20, 108], [21, 47], [21, 59], [21, 129], [22, 48], [22, 74], [22, 114], [23, 49], [23, 75], [23, 133], [24, 50], [24, 76], [24, 140], [25, 43], [25, 49], [25, 129], [26, 32], [26, 51], [26, 77], [27, 52], [27, 69], [27, 114], [28, 53], [28, 68], [28, 135], [29, 54], [29, 62], [29, 70], [30, 49], [30, 55], [31, 56], [31, 61], [31, 71], [32, 113], [32, 139], [33, 78], [33, 132], [33, 138], [34, 35], [34, 42], [34, 79], [35, 41], [35, 80], [35, 132], [36, 37], [36, 57], [36, 80], [36, 81], [37, 59], [37, 82], [38, 58], [38, 60], [38, 83], [39, 40], [39, 84], [39, 121], [40, 68], [40, 85], [41, 114], [41, 127], [42, 46], [42, 115], [43, 85], [43, 86], [44, 67], [44, 87], [44, 143], [45, 73], [45, 74], [45, 88], [46, 116], [46, 118], [47, 62], [47, 65], [47, 141], [48, 89], [48, 115], [48, 117], [49, 78], [50, 56], [50, 79], [50, 143], [51, 59], [51, 90], [51, 110], [52, 60], [52, 91], [52, 111], [53, 73], [53, 92], [53, 110], [54, 93], [54, 102], [54, 112], [55, 62], [55, 94], [55, 109], [56, 57], [56, 95], [57, 96], [58, 97], [58, 101], [58, 113], [59, 72], [60, 75], [60, 122], [61, 115], [61, 136], [61, 138], [62, 144], [63, 65], [63, 77], [63, 95], [64, 66], [64, 69], [64, 118], [65, 66], [65, 75], [66, 76], [66, 105], [67, 68], [67, 70], [67, 91], [68, 119], [69, 85], [69, 120], [70, 121], [71, 98], [71, 99], [71, 100], [72, 96], [72, 122], [73, 140], [74, 107], [74, 109], [75, 142], [76, 102], [76, 116], [77, 84], [77, 101], [78, 88], [78, 119], [79, 107], [79, 123], [80, 101], [80, 144], [81, 92], [81, 108], [81, 124], [82, 83], [82, 94], [82, 115], [83, 125], [84, 99], [84, 131], [85, 90], [86, 87], [86, 102], [86, 122], [87, 98], [87, 103], [88, 111], [88, 126], [89, 92], [89, 97], [89, 118], [90, 117], [90, 126], [91, 127], [91, 137], [92, 99], [93, 100], [93, 128], [93, 138], [94, 129], [94, 137], [95, 125], [95, 139], [96, 103], [96, 130], [97, 131], [98, 104], [98, 106], [99, 116], [100, 119], [101, 120], [103, 110], [104, 111], [104, 131], [105, 110], [105, 133], [106, 117], [106, 136], [107, 112], [107, 127], [108, 109], [108, 128], [109, 139], [111, 133], [112, 140], [113, 126], [113, 132], [114, 141], [116, 128], [117, 134], [118, 141], [119, 123], [120, 121], [121, 130], [122, 131], [123, 124], [123, 134], [124, 132], [124, 135], [125, 138], [125, 142], [126, 129], [127, 142], [128, 144], [130, 143], [130, 144], [133, 140], [135, 137], [136, 137], [139, 141], [142, 143]]);;
R:=P177Census(D);;Need(Size(R.F)=576);;
PrintTo("current_c4_descent/144_043.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_043 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
