Need:=function(ok) if not ok then Error("L059 cutoff probe invalid"); fi; end;;
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


D:=P177Graph("128_033",128,[1, 3, 4, 6, 10, 12, 14, 16, 17, 19, 20, 26, 28, 29, 30, 33, 38, 39, 40, 41, 43, 48, 49, 52, 54, 55, 56, 58, 61, 62, 63, 64, 66, 68, 70, 74, 75, 76, 77, 80, 81, 82, 83, 84, 85, 86, 87, 90, 92, 99, 104, 105, 110, 111, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128],[[1, 2], [1, 5], [1, 65], [1, 67], [2, 6], [2, 12], [2, 86], [3, 7], [3, 9], [3, 53], [3, 60], [4, 8], [4, 13], [4, 36], [4, 59], [5, 14], [5, 26], [5, 77], [6, 13], [6, 15], [6, 27], [7, 16], [7, 28], [7, 70], [8, 14], [8, 29], [8, 66], [9, 17], [9, 20], [9, 76], [10, 18], [10, 21], [10, 31], [10, 57], [11, 19], [11, 30], [11, 64], [11, 83], [12, 31], [12, 47], [12, 98], [13, 48], [13, 75], [14, 32], [14, 35], [15, 30], [15, 33], [15, 49], [16, 21], [16, 34], [16, 50], [17, 36], [17, 51], [17, 89], [18, 20], [18, 52], [18, 74], [19, 31], [19, 45], [19, 53], [20, 37], [20, 42], [21, 38], [21, 49], [22, 39], [22, 43], [22, 58], [22, 82], [23, 40], [23, 54], [23, 64], [23, 99], [24, 41], [24, 55], [24, 58], [24, 92], [25, 40], [25, 56], [25, 62], [25, 63], [26, 57], [26, 69], [26, 107], [27, 58], [27, 70], [27, 80], [28, 59], [28, 71], [28, 106], [29, 60], [29, 72], [29, 116], [30, 73], [30, 97], [31, 61], [32, 33], [32, 54], [32, 74], [33, 44], [33, 46], [34, 55], [34, 62], [34, 75], [35, 56], [35, 58], [35, 76], [36, 43], [36, 63], [37, 64], [37, 77], [37, 81], [38, 65], [38, 78], [38, 108], [39, 42], [39, 79], [39, 96], [40, 57], [40, 60], [41, 44], [41, 59], [41, 65], [42, 62], [42, 66], [43, 46], [43, 67], [44, 61], [44, 68], [45, 62], [45, 80], [45, 85], [46, 81], [46, 84], [47, 82], [47, 87], [47, 122], [48, 53], [48, 88], [48, 109], [49, 89], [49, 95], [50, 64], [50, 68], [50, 86], [51, 83], [51, 90], [51, 121], [52, 67], [52, 91], [52, 103], [53, 92], [54, 93], [54, 115], [55, 94], [55, 114], [56, 95], [56, 102], [57, 84], [59, 85], [60, 82], [61, 72], [61, 96], [63, 78], [63, 97], [65, 83], [66, 98], [66, 100], [67, 99], [68, 100], [68, 101], [69, 87], [69, 92], [69, 126], [70, 93], [70, 103], [71, 90], [71, 99], [71, 125], [72, 104], [72, 126], [73, 76], [73, 105], [73, 123], [74, 106], [74, 112], [75, 107], [75, 113], [76, 108], [77, 94], [77, 109], [78, 110], [78, 125], [79, 86], [79, 111], [79, 119], [80, 112], [80, 118], [81, 113], [81, 117], [82, 101], [83, 102], [84, 88], [84, 114], [85, 91], [85, 115], [86, 116], [87, 103], [87, 108], [88, 104], [88, 122], [89, 104], [89, 119], [90, 109], [90, 116], [91, 110], [91, 121], [92, 117], [93, 105], [93, 128], [94, 111], [94, 127], [95, 120], [95, 128], [96, 120], [96, 121], [97, 122], [97, 124], [98, 110], [98, 123], [99, 118], [100, 124], [100, 127], [101, 105], [101, 125], [102, 111], [102, 126], [103, 119], [104, 106], [105, 117], [106, 127], [107, 110], [107, 128], [108, 127], [109, 123], [111, 118], [112, 120], [112, 123], [113, 119], [113, 124], [114, 120], [114, 125], [115, 124], [115, 126], [116, 128], [117, 121], [118, 122]]);;
R:=P177Census(D);;
Need(Size(R.F)=18432);;
PrintTo("quartic_cutoff_probe/128_033.g","L059Result := ",R,";\n");
Print("L059_CUTOFF_COMPLETE 128_033 ",Length(R.witnesses),"\n");
QUIT;
