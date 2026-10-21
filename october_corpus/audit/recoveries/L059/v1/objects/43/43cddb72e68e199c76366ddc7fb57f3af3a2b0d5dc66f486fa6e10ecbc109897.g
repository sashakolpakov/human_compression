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
D:=P177Graph("144_039",144,[1, 3, 4, 6, 9, 11, 13, 14, 17, 19, 20, 22, 25, 30, 35, 39, 40, 41, 42, 43, 45, 46, 48, 51, 53, 54, 55, 57, 58, 59, 60, 62, 65, 67, 69, 75, 76, 77, 79, 80, 81, 83, 84, 86, 87, 88, 90, 91, 94, 95, 100, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 124, 130, 131, 137, 141],[[1, 2], [1, 5], [1, 73], [1, 101], [2, 6], [2, 14], [2, 58], [3, 7], [3, 15], [3, 33], [3, 56], [4, 8], [4, 16], [4, 28], [4, 89], [5, 17], [5, 39], [5, 104], [6, 18], [6, 29], [6, 70], [7, 19], [7, 40], [7, 88], [8, 20], [8, 41], [8, 76], [9, 21], [9, 23], [9, 72], [9, 74], [10, 17], [10, 22], [10, 42], [10, 100], [11, 24], [11, 27], [11, 61], [11, 63], [12, 25], [12, 43], [12, 53], [12, 114], [13, 26], [13, 38], [13, 64], [13, 96], [14, 44], [14, 78], [14, 134], [15, 45], [15, 69], [15, 79], [16, 46], [16, 55], [16, 80], [17, 37], [17, 47], [18, 41], [18, 48], [18, 65], [19, 37], [19, 49], [19, 52], [20, 34], [20, 36], [20, 50], [21, 43], [21, 51], [21, 81], [22, 27], [22, 82], [22, 129], [23, 42], [23, 57], [23, 83], [24, 25], [24, 84], [24, 90], [25, 52], [25, 85], [26, 53], [26, 86], [26, 103], [27, 54], [27, 87], [28, 59], [28, 115], [28, 116], [29, 45], [29, 55], [29, 130], [30, 44], [30, 56], [30, 74], [30, 92], [31, 45], [31, 54], [31, 57], [31, 112], [32, 46], [32, 53], [32, 58], [32, 131], [33, 60], [33, 95], [33, 111], [34, 77], [34, 88], [34, 141], [35, 49], [35, 61], [35, 89], [35, 97], [36, 51], [36, 90], [36, 117], [37, 91], [37, 94], [38, 62], [38, 77], [38, 91], [39, 92], [39, 120], [39, 133], [40, 93], [40, 99], [40, 120], [41, 121], [41, 132], [42, 68], [42, 93], [43, 99], [43, 122], [44, 54], [44, 94], [45, 66], [46, 68], [46, 92], [47, 84], [47, 95], [47, 112], [48, 72], [48, 85], [48, 96], [49, 86], [49, 113], [50, 87], [50, 95], [50, 114], [51, 70], [51, 97], [52, 75], [52, 76], [53, 98], [54, 71], [55, 123], [55, 140], [56, 105], [56, 124], [57, 122], [57, 128], [58, 125], [58, 142], [59, 74], [59, 102], [59, 126], [60, 61], [60, 123], [60, 127], [61, 107], [62, 97], [62, 121], [62, 128], [63, 67], [63, 105], [63, 106], [64, 95], [64, 106], [64, 137], [65, 68], [65, 99], [65, 143], [66, 81], [66, 100], [66, 115], [67, 93], [67, 101], [67, 119], [68, 69], [69, 102], [69, 139], [70, 103], [70, 118], [71, 77], [71, 104], [71, 113], [72, 108], [72, 109], [73, 109], [73, 115], [73, 124], [74, 110], [75, 119], [75, 129], [75, 144], [76, 120], [76, 123], [77, 119], [78, 81], [78, 90], [78, 113], [79, 119], [79, 134], [79, 140], [80, 85], [80, 129], [80, 139], [81, 132], [82, 90], [82, 108], [82, 110], [83, 98], [83, 129], [83, 133], [84, 99], [84, 142], [85, 141], [86, 139], [86, 142], [87, 128], [87, 140], [88, 102], [88, 132], [89, 108], [89, 137], [91, 133], [91, 136], [92, 118], [93, 130], [94, 127], [94, 139], [96, 107], [96, 116], [97, 131], [98, 115], [98, 117], [100, 135], [100, 142], [101, 110], [101, 111], [102, 137], [103, 134], [103, 136], [104, 121], [104, 125], [105, 122], [105, 126], [106, 125], [106, 143], [107, 122], [107, 144], [108, 127], [109, 136], [109, 144], [110, 143], [111, 135], [111, 136], [112, 132], [112, 138], [113, 126], [114, 133], [114, 138], [116, 125], [116, 138], [117, 135], [117, 140], [118, 127], [118, 128], [120, 131], [121, 130], [123, 124], [124, 138], [126, 131], [130, 144], [134, 141], [135, 137], [141, 143]]);;
R:=P177Census(D);;Need(Size(R.F)=576);;
PrintTo("current_c4_descent/144_039.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_039 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
