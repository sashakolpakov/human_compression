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
D:=P177Graph("144_042",144,[1, 6, 7, 8, 10, 12, 13, 14, 15, 16, 17, 20, 22, 25, 26, 29, 30, 31, 32, 34, 35, 40, 48, 51, 56, 60, 68, 69, 70, 72, 73, 74, 75, 80, 81, 82, 84, 85, 86, 87, 88, 89, 90, 92, 93, 94, 95, 96, 97, 98, 101, 102, 104, 106, 108, 109, 110, 111, 112, 113, 115, 116, 117, 118, 119, 120, 121, 122, 127, 135, 137, 144],[[1, 2], [1, 5], [1, 24], [1, 39], [2, 6], [2, 14], [2, 16], [3, 7], [3, 15], [3, 35], [3, 74], [4, 7], [4, 8], [4, 16], [4, 75], [5, 17], [5, 35], [5, 40], [6, 18], [6, 36], [6, 41], [7, 36], [7, 37], [8, 19], [8, 38], [8, 42], [9, 10], [9, 14], [9, 20], [9, 48], [10, 21], [10, 39], [10, 50], [11, 20], [11, 22], [11, 40], [11, 116], [12, 21], [12, 23], [12, 41], [12, 114], [13, 18], [13, 24], [13, 42], [13, 99], [14, 43], [14, 47], [15, 24], [15, 44], [15, 76], [16, 45], [16, 65], [17, 46], [17, 67], [17, 77], [18, 68], [18, 69], [19, 35], [19, 56], [19, 69], [20, 33], [20, 67], [21, 68], [21, 70], [22, 47], [22, 71], [22, 78], [23, 48], [23, 72], [23, 73], [24, 73], [25, 27], [25, 33], [25, 37], [25, 49], [26, 27], [26, 28], [26, 38], [26, 50], [27, 70], [27, 74], [28, 51], [28, 72], [28, 75], [29, 37], [29, 47], [29, 52], [29, 143], [30, 49], [30, 53], [30, 71], [30, 76], [31, 50], [31, 54], [31, 65], [31, 142], [32, 44], [32, 55], [32, 77], [32, 141], [33, 51], [33, 56], [34, 39], [34, 46], [34, 59], [34, 78], [35, 79], [36, 80], [36, 88], [37, 89], [38, 81], [38, 90], [39, 82], [40, 83], [40, 107], [41, 84], [41, 98], [42, 85], [42, 108], [43, 86], [43, 89], [43, 119], [44, 111], [44, 112], [45, 87], [45, 97], [45, 120], [46, 112], [46, 113], [47, 113], [48, 49], [48, 99], [49, 111], [50, 97], [51, 79], [51, 114], [52, 88], [52, 115], [52, 121], [53, 89], [53, 116], [53, 118], [54, 90], [54, 116], [54, 117], [55, 74], [55, 82], [55, 118], [56, 91], [56, 136], [57, 70], [57, 88], [57, 92], [57, 117], [58, 68], [58, 90], [58, 93], [58, 122], [59, 74], [59, 94], [59, 115], [60, 61], [60, 76], [60, 107], [60, 124], [61, 75], [61, 95], [61, 98], [62, 72], [62, 96], [62, 108], [62, 118], [63, 82], [63, 97], [63, 119], [63, 137], [64, 80], [64, 98], [64, 112], [64, 120], [65, 86], [65, 121], [66, 75], [66, 84], [66, 87], [66, 116], [67, 122], [67, 127], [68, 128], [69, 123], [69, 129], [70, 130], [71, 92], [71, 98], [72, 131], [73, 105], [73, 132], [76, 135], [77, 87], [77, 90], [78, 96], [78, 101], [79, 102], [79, 144], [80, 130], [80, 140], [81, 100], [81, 124], [81, 128], [82, 139], [83, 84], [83, 93], [83, 135], [84, 125], [85, 126], [85, 131], [85, 141], [86, 103], [86, 139], [87, 140], [88, 103], [89, 141], [91, 110], [91, 121], [91, 127], [92, 128], [92, 142], [93, 129], [93, 139], [94, 130], [94, 138], [94, 143], [95, 100], [95, 131], [95, 143], [96, 132], [96, 142], [97, 138], [99, 104], [99, 110], [100, 111], [100, 127], [101, 114], [101, 129], [101, 133], [102, 107], [102, 132], [102, 138], [103, 104], [103, 135], [104, 134], [104, 136], [105, 135], [105, 137], [105, 144], [106, 123], [106, 136], [106, 140], [106, 141], [107, 121], [108, 124], [108, 139], [109, 114], [109, 123], [109, 125], [109, 143], [110, 126], [110, 142], [111, 134], [112, 128], [113, 123], [113, 126], [115, 124], [115, 129], [117, 133], [117, 136], [118, 133], [119, 125], [119, 131], [120, 126], [120, 132], [122, 125], [122, 134], [127, 138], [130, 137], [133, 144], [134, 137], [140, 144]]);;
R:=P177Census(D);;Need(Size(R.F)=576);;
PrintTo("current_c4_descent/144_042.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_042 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
