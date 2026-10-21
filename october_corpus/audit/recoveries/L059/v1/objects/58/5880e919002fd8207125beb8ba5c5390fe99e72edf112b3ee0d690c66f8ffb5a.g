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
D:=P177Graph("144_041",144,[1, 3, 5, 7, 8, 9, 11, 13, 17, 18, 20, 24, 25, 27, 28, 29, 32, 35, 37, 39, 40, 43, 45, 46, 48, 52, 53, 56, 58, 59, 61, 62, 65, 67, 69, 70, 72, 76, 77, 78, 80, 83, 85, 86, 88, 89, 91, 94, 96, 98, 99, 100, 103, 106, 107, 108, 109, 112, 114, 115, 117, 120, 121, 122, 125, 127, 129, 131, 134, 136, 138, 142],[[1, 2], [1, 4], [1, 47], [1, 73], [2, 5], [2, 9], [2, 107], [3, 6], [3, 10], [3, 30], [3, 33], [4, 11], [4, 18], [4, 127], [5, 12], [5, 19], [5, 132], [6, 13], [6, 20], [6, 58], [7, 14], [7, 15], [7, 21], [7, 57], [8, 15], [8, 22], [8, 51], [8, 54], [9, 23], [9, 34], [9, 84], [10, 24], [10, 35], [10, 86], [11, 12], [11, 36], [11, 143], [12, 25], [12, 37], [13, 26], [13, 38], [13, 79], [14, 27], [14, 39], [14, 85], [15, 28], [15, 77], [16, 28], [16, 29], [16, 40], [16, 80], [17, 30], [17, 38], [17, 41], [17, 81], [18, 42], [18, 55], [18, 60], [19, 43], [19, 59], [19, 112], [20, 44], [20, 60], [20, 116], [21, 35], [21, 45], [21, 59], [22, 46], [22, 61], [22, 109], [23, 25], [23, 62], [23, 117], [24, 26], [24, 63], [24, 110], [25, 47], [25, 64], [26, 48], [26, 65], [27, 49], [27, 50], [27, 51], [28, 50], [28, 111], [29, 51], [29, 66], [29, 113], [30, 48], [30, 52], [31, 52], [31, 53], [31, 61], [31, 67], [32, 50], [32, 54], [32, 68], [32, 104], [33, 65], [33, 69], [33, 106], [34, 61], [34, 70], [34, 88], [35, 71], [35, 82], [36, 72], [36, 86], [36, 120], [37, 42], [37, 73], [37, 87], [38, 53], [38, 88], [39, 74], [39, 84], [39, 119], [40, 60], [40, 75], [40, 87], [41, 76], [41, 80], [41, 122], [42, 89], [42, 98], [43, 47], [43, 90], [43, 135], [44, 48], [44, 91], [44, 134], [45, 49], [45, 92], [45, 101], [46, 50], [46, 93], [46, 133], [47, 94], [48, 95], [49, 77], [49, 96], [51, 78], [52, 79], [52, 128], [53, 90], [53, 97], [54, 98], [54, 131], [55, 78], [55, 80], [55, 99], [56, 75], [56, 79], [56, 81], [56, 124], [57, 91], [57, 96], [57, 100], [58, 95], [58, 101], [58, 130], [59, 102], [59, 118], [60, 103], [61, 104], [62, 105], [62, 116], [62, 137], [63, 106], [63, 109], [63, 138], [64, 67], [64, 70], [64, 107], [65, 71], [65, 118], [66, 108], [66, 112], [66, 136], [67, 68], [67, 84], [68, 88], [68, 109], [69, 104], [69, 110], [69, 140], [70, 119], [70, 123], [71, 120], [71, 121], [72, 73], [72, 113], [72, 130], [73, 121], [74, 77], [74, 106], [74, 129], [75, 78], [75, 122], [76, 79], [76, 105], [76, 133], [77, 123], [78, 111], [80, 124], [81, 117], [81, 131], [82, 94], [82, 96], [82, 112], [83, 102], [83, 111], [83, 113], [83, 141], [84, 125], [85, 110], [85, 123], [85, 135], [86, 118], [86, 126], [87, 99], [87, 127], [88, 128], [89, 93], [89, 119], [89, 141], [90, 114], [90, 129], [91, 92], [91, 130], [92, 122], [92, 138], [93, 127], [93, 131], [94, 102], [94, 132], [95, 99], [95, 103], [96, 118], [97, 115], [97, 120], [97, 142], [98, 133], [98, 144], [99, 116], [100, 101], [100, 124], [100, 140], [101, 134], [102, 136], [103, 137], [103, 139], [104, 138], [105, 107], [105, 131], [106, 135], [107, 139], [108, 111], [108, 130], [108, 143], [109, 140], [110, 129], [112, 141], [113, 134], [114, 126], [114, 128], [114, 137], [115, 128], [115, 132], [115, 135], [116, 142], [117, 133], [117, 139], [119, 136], [120, 137], [121, 126], [121, 143], [122, 140], [123, 125], [124, 138], [125, 141], [125, 144], [126, 142], [127, 144], [129, 132], [134, 143], [136, 144], [139, 142]]);;
R:=P177Census(D);;Need(Size(R.F)=576);;
PrintTo("current_c4_descent/144_041.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_041 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
