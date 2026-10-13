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
D:=P177Graph("144_040",144,[1, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 19, 23, 24, 25, 26, 28, 32, 39, 40, 44, 50, 52, 53, 59, 60, 61, 63, 64, 65, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 84, 87, 88, 89, 90, 94, 98, 102, 118, 119, 120, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138],[[1, 2], [1, 5], [1, 21], [1, 42], [2, 6], [2, 13], [2, 61], [3, 7], [3, 14], [3, 39], [3, 65], [4, 7], [4, 8], [4, 15], [4, 19], [5, 16], [5, 28], [5, 81], [6, 17], [6, 29], [6, 86], [7, 30], [7, 85], [8, 18], [8, 31], [8, 36], [9, 19], [9, 32], [9, 40], [9, 90], [10, 20], [10, 27], [10, 33], [10, 83], [11, 17], [11, 21], [11, 34], [11, 41], [12, 20], [12, 22], [12, 35], [12, 37], [13, 36], [13, 46], [13, 108], [14, 37], [14, 47], [14, 107], [15, 38], [15, 48], [15, 58], [16, 20], [16, 49], [16, 114], [17, 25], [17, 26], [18, 39], [18, 50], [18, 63], [19, 51], [19, 113], [20, 24], [21, 52], [21, 60], [22, 40], [22, 53], [22, 59], [23, 27], [23, 41], [23, 54], [23, 105], [24, 42], [24, 55], [24, 66], [25, 45], [25, 56], [25, 111], [26, 43], [26, 57], [26, 62], [27, 40], [27, 64], [28, 46], [28, 58], [28, 92], [29, 59], [29, 67], [29, 124], [30, 60], [30, 68], [30, 126], [31, 61], [31, 69], [31, 87], [32, 54], [32, 62], [32, 93], [33, 63], [33, 70], [33, 125], [34, 64], [34, 71], [34, 80], [35, 65], [35, 72], [35, 79], [36, 73], [36, 131], [37, 74], [37, 129], [38, 40], [38, 75], [38, 89], [39, 43], [39, 45], [41, 76], [41, 132], [42, 77], [42, 84], [43, 78], [43, 82], [44, 45], [44, 47], [44, 66], [44, 91], [45, 88], [46, 67], [46, 79], [47, 68], [47, 80], [48, 68], [48, 69], [48, 81], [49, 79], [49, 82], [49, 135], [50, 83], [50, 91], [50, 103], [51, 84], [51, 87], [51, 137], [52, 85], [52, 92], [52, 106], [53, 86], [53, 93], [53, 104], [54, 70], [54, 87], [55, 70], [55, 72], [55, 88], [56, 80], [56, 89], [56, 138], [57, 67], [57, 71], [57, 90], [58, 94], [58, 119], [59, 95], [59, 140], [60, 96], [60, 139], [61, 97], [61, 110], [62, 98], [62, 120], [63, 99], [63, 141], [64, 100], [64, 109], [65, 101], [65, 112], [66, 102], [66, 118], [67, 103], [68, 104], [69, 91], [69, 105], [70, 106], [71, 92], [71, 107], [72, 93], [72, 108], [73, 103], [73, 109], [73, 144], [74, 104], [74, 110], [74, 143], [75, 105], [75, 111], [75, 115], [76, 106], [76, 112], [76, 142], [77, 108], [77, 113], [77, 116], [78, 107], [78, 114], [78, 121], [79, 115], [80, 116], [81, 96], [81, 117], [82, 112], [82, 141], [83, 118], [83, 128], [84, 110], [84, 139], [85, 119], [85, 127], [86, 120], [86, 130], [87, 121], [88, 99], [88, 122], [89, 109], [89, 140], [90, 95], [90, 123], [91, 124], [92, 125], [93, 126], [94, 99], [94, 115], [94, 143], [95, 102], [95, 127], [96, 98], [96, 128], [97, 124], [97, 129], [97, 136], [98, 121], [98, 144], [99, 130], [100, 125], [100, 131], [100, 134], [101, 126], [101, 132], [101, 133], [102, 116], [102, 142], [103, 133], [104, 134], [105, 135], [106, 136], [107, 137], [108, 138], [109, 128], [110, 130], [111, 130], [111, 132], [112, 127], [113, 127], [113, 131], [114, 128], [114, 129], [115, 133], [116, 134], [117, 120], [117, 134], [117, 135], [118, 123], [118, 139], [119, 122], [119, 140], [120, 141], [121, 136], [122, 136], [122, 138], [123, 133], [123, 137], [124, 142], [125, 143], [126, 144], [129, 140], [131, 141], [132, 139], [135, 142], [137, 143], [138, 144]]);;
R:=P177Census(D);;Need(Size(R.F)=576);;
PrintTo("current_c4_descent/144_040.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_040 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
