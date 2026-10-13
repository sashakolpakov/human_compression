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
D:=P177Graph("144_032",144,[1, 2, 3, 4, 5, 6, 25, 26, 27, 28, 29, 30, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 103, 104, 105, 106, 107, 108, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144],[[1, 7], [1, 13], [1, 19], [1, 31], [2, 18], [2, 36], [2, 75], [2, 114], [3, 56], [3, 76], [3, 91], [3, 131], [4, 20], [4, 57], [4, 96], [4, 121], [5, 98], [5, 113], [5, 119], [5, 122], [6, 8], [6, 99], [6, 116], [6, 132], [7, 25], [7, 43], [7, 61], [8, 39], [8, 66], [8, 137], [9, 40], [9, 49], [9, 83], [9, 104], [10, 44], [10, 54], [10, 67], [10, 105], [11, 68], [11, 87], [11, 138], [11, 140], [12, 26], [12, 84], [12, 90], [12, 143], [13, 37], [13, 46], [13, 49], [14, 42], [14, 47], [14, 66], [14, 105], [15, 26], [15, 85], [15, 106], [15, 133], [16, 27], [16, 50], [16, 138], [16, 141], [17, 65], [17, 71], [17, 84], [17, 142], [18, 68], [18, 81], [18, 86], [19, 27], [19, 63], [19, 79], [20, 66], [20, 69], [20, 133], [21, 47], [21, 70], [21, 85], [21, 140], [22, 37], [22, 80], [22, 90], [22, 141], [23, 38], [23, 51], [23, 104], [23, 134], [24, 28], [24, 48], [24, 54], [24, 107], [25, 34], [25, 55], [25, 109], [26, 95], [26, 114], [27, 74], [27, 97], [28, 33], [28, 75], [28, 115], [29, 96], [29, 116], [29, 126], [29, 127], [30, 56], [30, 98], [30, 123], [30, 130], [31, 67], [31, 82], [31, 85], [32, 66], [32, 72], [32, 83], [32, 141], [33, 49], [33, 137], [33, 142], [34, 86], [34, 105], [34, 134], [35, 41], [35, 48], [35, 65], [35, 106], [36, 38], [36, 45], [36, 50], [37, 73], [37, 91], [38, 57], [38, 78], [39, 58], [39, 102], [39, 112], [40, 92], [40, 113], [40, 118], [41, 117], [41, 125], [41, 132], [42, 101], [42, 122], [42, 129], [43, 57], [43, 101], [43, 111], [44, 91], [44, 114], [44, 117], [45, 118], [45, 126], [45, 131], [46, 102], [46, 121], [46, 130], [47, 74], [47, 92], [48, 58], [48, 77], [49, 127], [50, 112], [50, 123], [51, 102], [51, 119], [51, 124], [52, 73], [52, 99], [52, 118], [52, 128], [53, 56], [53, 74], [53, 93], [53, 111], [54, 59], [54, 96], [55, 64], [55, 103], [55, 136], [56, 137], [57, 88], [58, 63], [58, 144], [59, 72], [59, 79], [59, 143], [60, 69], [60, 82], [60, 87], [60, 104], [61, 100], [61, 115], [61, 131], [62, 97], [62, 114], [62, 120], [62, 121], [63, 95], [63, 122], [64, 75], [64, 92], [64, 132], [65, 76], [65, 113], [67, 110], [67, 119], [68, 99], [68, 111], [69, 77], [69, 100], [70, 76], [70, 94], [70, 120], [71, 93], [71, 121], [71, 128], [72, 124], [72, 131], [73, 103], [73, 133], [74, 108], [75, 80], [76, 134], [77, 86], [77, 139], [78, 79], [78, 89], [78, 142], [79, 99], [80, 93], [80, 119], [81, 94], [81, 122], [81, 127], [82, 123], [82, 132], [83, 109], [83, 120], [84, 100], [84, 112], [85, 126], [86, 130], [87, 91], [87, 129], [88, 94], [88, 110], [88, 125], [89, 98], [89, 109], [89, 117], [90, 101], [90, 116], [92, 143], [93, 144], [94, 103], [95, 104], [95, 135], [96, 138], [97, 136], [97, 139], [98, 133], [100, 108], [101, 107], [102, 140], [103, 112], [105, 128], [106, 111], [106, 124], [107, 120], [107, 123], [108, 117], [108, 127], [109, 144], [110, 137], [110, 139], [113, 138], [115, 135], [115, 140], [116, 134], [118, 139], [124, 136], [125, 135], [125, 141], [126, 144], [128, 135], [129, 136], [129, 142], [130, 143]]);;
R:=P177Census(D);;Need(Size(R.F)=576);;
PrintTo("current_c4_descent/144_032.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_032 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
