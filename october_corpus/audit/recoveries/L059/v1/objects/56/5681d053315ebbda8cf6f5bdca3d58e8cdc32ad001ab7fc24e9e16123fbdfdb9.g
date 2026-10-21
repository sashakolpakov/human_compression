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
D:=P177Graph("128_020",128,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127],[[1, 2], [1, 32], [1, 50], [1, 65], [2, 3], [2, 51], [2, 66], [3, 4], [3, 52], [3, 67], [4, 5], [4, 53], [4, 68], [5, 6], [5, 54], [5, 69], [6, 7], [6, 55], [6, 70], [7, 8], [7, 56], [7, 71], [8, 9], [8, 57], [8, 72], [9, 10], [9, 58], [9, 73], [10, 11], [10, 59], [10, 74], [11, 12], [11, 60], [11, 75], [12, 13], [12, 61], [12, 76], [13, 14], [13, 62], [13, 77], [14, 15], [14, 63], [14, 78], [15, 16], [15, 64], [15, 79], [16, 17], [16, 33], [16, 80], [17, 18], [17, 34], [17, 81], [18, 19], [18, 35], [18, 82], [19, 20], [19, 36], [19, 83], [20, 21], [20, 37], [20, 84], [21, 22], [21, 38], [21, 85], [22, 23], [22, 39], [22, 86], [23, 24], [23, 40], [23, 87], [24, 25], [24, 41], [24, 88], [25, 26], [25, 42], [25, 89], [26, 27], [26, 43], [26, 90], [27, 28], [27, 44], [27, 91], [28, 29], [28, 45], [28, 92], [29, 30], [29, 46], [29, 93], [30, 31], [30, 47], [30, 94], [31, 32], [31, 48], [31, 95], [32, 49], [32, 96], [33, 65], [33, 67], [33, 116], [34, 66], [34, 68], [34, 117], [35, 67], [35, 69], [35, 118], [36, 68], [36, 70], [36, 119], [37, 69], [37, 71], [37, 120], [38, 70], [38, 72], [38, 121], [39, 71], [39, 73], [39, 122], [40, 72], [40, 74], [40, 123], [41, 73], [41, 75], [41, 124], [42, 74], [42, 76], [42, 125], [43, 75], [43, 77], [43, 126], [44, 76], [44, 78], [44, 127], [45, 77], [45, 79], [45, 128], [46, 78], [46, 80], [46, 97], [47, 79], [47, 81], [47, 98], [48, 80], [48, 82], [48, 99], [49, 81], [49, 83], [49, 100], [50, 82], [50, 84], [50, 101], [51, 83], [51, 85], [51, 102], [52, 84], [52, 86], [52, 103], [53, 85], [53, 87], [53, 104], [54, 86], [54, 88], [54, 105], [55, 87], [55, 89], [55, 106], [56, 88], [56, 90], [56, 107], [57, 89], [57, 91], [57, 108], [58, 90], [58, 92], [58, 109], [59, 91], [59, 93], [59, 110], [60, 92], [60, 94], [60, 111], [61, 93], [61, 95], [61, 112], [62, 94], [62, 96], [62, 113], [63, 65], [63, 95], [63, 114], [64, 66], [64, 96], [64, 115], [65, 97], [66, 98], [67, 99], [68, 100], [69, 101], [70, 102], [71, 103], [72, 104], [73, 105], [74, 106], [75, 107], [76, 108], [77, 109], [78, 110], [79, 111], [80, 112], [81, 113], [82, 114], [83, 115], [84, 116], [85, 117], [86, 118], [87, 119], [88, 120], [89, 121], [90, 122], [91, 123], [92, 124], [93, 125], [94, 126], [95, 127], [96, 128], [97, 98], [97, 128], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108], [108, 109], [109, 110], [110, 111], [111, 112], [112, 113], [113, 114], [114, 115], [115, 116], [116, 117], [117, 118], [118, 119], [119, 120], [120, 121], [121, 122], [122, 123], [123, 124], [124, 125], [125, 126], [126, 127], [127, 128]]);;
R:=P177Census(D);;Need(Size(R.F)=1024);;
PrintTo("current_c4_descent/128_020.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_020 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
