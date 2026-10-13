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
D:=P177Graph("128_017",128,[1, 3, 5, 7, 10, 12, 14, 16, 17, 19, 21, 23, 26, 28, 30, 32, 33, 35, 37, 39, 42, 44, 46, 48, 49, 51, 53, 55, 58, 60, 62, 64, 65, 67, 69, 71, 74, 76, 78, 80, 81, 83, 85, 87, 90, 92, 94, 96, 97, 99, 101, 103, 106, 108, 110, 112, 113, 115, 117, 119, 122, 124, 126, 128],[[1, 2], [1, 57], [1, 72], [1, 73], [2, 3], [2, 10], [2, 122], [3, 4], [3, 59], [3, 75], [4, 5], [4, 12], [4, 124], [5, 6], [5, 61], [5, 77], [6, 7], [6, 14], [6, 126], [7, 8], [7, 63], [7, 79], [8, 16], [8, 65], [8, 128], [9, 10], [9, 65], [9, 80], [9, 81], [10, 11], [10, 18], [11, 12], [11, 67], [11, 83], [12, 13], [12, 20], [13, 14], [13, 69], [13, 85], [14, 15], [14, 22], [15, 16], [15, 71], [15, 87], [16, 24], [16, 73], [17, 18], [17, 73], [17, 88], [17, 89], [18, 19], [18, 26], [19, 20], [19, 75], [19, 91], [20, 21], [20, 28], [21, 22], [21, 77], [21, 93], [22, 23], [22, 30], [23, 24], [23, 79], [23, 95], [24, 32], [24, 81], [25, 26], [25, 81], [25, 96], [25, 97], [26, 27], [26, 34], [27, 28], [27, 83], [27, 99], [28, 29], [28, 36], [29, 30], [29, 85], [29, 101], [30, 31], [30, 38], [31, 32], [31, 87], [31, 103], [32, 40], [32, 89], [33, 34], [33, 89], [33, 104], [33, 105], [34, 35], [34, 42], [35, 36], [35, 91], [35, 107], [36, 37], [36, 44], [37, 38], [37, 93], [37, 109], [38, 39], [38, 46], [39, 40], [39, 95], [39, 111], [40, 48], [40, 97], [41, 42], [41, 97], [41, 112], [41, 113], [42, 43], [42, 50], [43, 44], [43, 99], [43, 115], [44, 45], [44, 52], [45, 46], [45, 101], [45, 117], [46, 47], [46, 54], [47, 48], [47, 103], [47, 119], [48, 56], [48, 105], [49, 50], [49, 105], [49, 120], [49, 121], [50, 51], [50, 58], [51, 52], [51, 107], [51, 123], [52, 53], [52, 60], [53, 54], [53, 109], [53, 125], [54, 55], [54, 62], [55, 56], [55, 111], [55, 127], [56, 64], [56, 113], [57, 58], [57, 113], [57, 128], [58, 59], [58, 66], [59, 60], [59, 115], [60, 61], [60, 68], [61, 62], [61, 117], [62, 63], [62, 70], [63, 64], [63, 119], [64, 72], [64, 121], [65, 66], [65, 121], [66, 67], [66, 74], [67, 68], [67, 123], [68, 69], [68, 76], [69, 70], [69, 125], [70, 71], [70, 78], [71, 72], [71, 127], [72, 80], [73, 74], [74, 75], [74, 82], [75, 76], [76, 77], [76, 84], [77, 78], [78, 79], [78, 86], [79, 80], [80, 88], [81, 82], [82, 83], [82, 90], [83, 84], [84, 85], [84, 92], [85, 86], [86, 87], [86, 94], [87, 88], [88, 96], [89, 90], [90, 91], [90, 98], [91, 92], [92, 93], [92, 100], [93, 94], [94, 95], [94, 102], [95, 96], [96, 104], [97, 98], [98, 99], [98, 106], [99, 100], [100, 101], [100, 108], [101, 102], [102, 103], [102, 110], [103, 104], [104, 112], [105, 106], [106, 107], [106, 114], [107, 108], [108, 109], [108, 116], [109, 110], [110, 111], [110, 118], [111, 112], [112, 120], [113, 114], [114, 115], [114, 122], [115, 116], [116, 117], [116, 124], [117, 118], [118, 119], [118, 126], [119, 120], [120, 128], [121, 122], [122, 123], [123, 124], [124, 125], [125, 126], [126, 127], [127, 128]]);;
R:=P177Census(D);;Need(Size(R.F)=1024);;
PrintTo("current_c4_descent/128_017.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_017 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
