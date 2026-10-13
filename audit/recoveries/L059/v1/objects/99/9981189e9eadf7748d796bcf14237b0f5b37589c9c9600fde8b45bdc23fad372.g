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
D:=P177Graph("130_003",130,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129],[[1, 2], [1, 52], [1, 80], [1, 130], [2, 3], [2, 53], [2, 81], [3, 4], [3, 54], [3, 82], [4, 5], [4, 55], [4, 83], [5, 6], [5, 56], [5, 84], [6, 7], [6, 57], [6, 85], [7, 8], [7, 58], [7, 86], [8, 9], [8, 59], [8, 87], [9, 10], [9, 60], [9, 88], [10, 11], [10, 61], [10, 89], [11, 12], [11, 62], [11, 90], [12, 13], [12, 63], [12, 91], [13, 14], [13, 64], [13, 92], [14, 15], [14, 65], [14, 93], [15, 16], [15, 66], [15, 94], [16, 17], [16, 67], [16, 95], [17, 18], [17, 68], [17, 96], [18, 19], [18, 69], [18, 97], [19, 20], [19, 70], [19, 98], [20, 21], [20, 71], [20, 99], [21, 22], [21, 72], [21, 100], [22, 23], [22, 73], [22, 101], [23, 24], [23, 74], [23, 102], [24, 25], [24, 75], [24, 103], [25, 26], [25, 76], [25, 104], [26, 27], [26, 77], [26, 105], [27, 28], [27, 78], [27, 106], [28, 29], [28, 79], [28, 107], [29, 30], [29, 80], [29, 108], [30, 31], [30, 81], [30, 109], [31, 32], [31, 82], [31, 110], [32, 33], [32, 83], [32, 111], [33, 34], [33, 84], [33, 112], [34, 35], [34, 85], [34, 113], [35, 36], [35, 86], [35, 114], [36, 37], [36, 87], [36, 115], [37, 38], [37, 88], [37, 116], [38, 39], [38, 89], [38, 117], [39, 40], [39, 90], [39, 118], [40, 41], [40, 91], [40, 119], [41, 42], [41, 92], [41, 120], [42, 43], [42, 93], [42, 121], [43, 44], [43, 94], [43, 122], [44, 45], [44, 95], [44, 123], [45, 46], [45, 96], [45, 124], [46, 47], [46, 97], [46, 125], [47, 48], [47, 98], [47, 126], [48, 49], [48, 99], [48, 127], [49, 50], [49, 100], [49, 128], [50, 51], [50, 101], [50, 129], [51, 52], [51, 102], [51, 130], [52, 53], [52, 103], [53, 54], [53, 104], [54, 55], [54, 105], [55, 56], [55, 106], [56, 57], [56, 107], [57, 58], [57, 108], [58, 59], [58, 109], [59, 60], [59, 110], [60, 61], [60, 111], [61, 62], [61, 112], [62, 63], [62, 113], [63, 64], [63, 114], [64, 65], [64, 115], [65, 66], [65, 116], [66, 67], [66, 117], [67, 68], [67, 118], [68, 69], [68, 119], [69, 70], [69, 120], [70, 71], [70, 121], [71, 72], [71, 122], [72, 73], [72, 123], [73, 74], [73, 124], [74, 75], [74, 125], [75, 76], [75, 126], [76, 77], [76, 127], [77, 78], [77, 128], [78, 79], [78, 129], [79, 80], [79, 130], [80, 81], [81, 82], [82, 83], [83, 84], [84, 85], [85, 86], [86, 87], [87, 88], [88, 89], [89, 90], [90, 91], [91, 92], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108], [108, 109], [109, 110], [110, 111], [111, 112], [112, 113], [113, 114], [114, 115], [115, 116], [116, 117], [117, 118], [118, 119], [119, 120], [120, 121], [121, 122], [122, 123], [123, 124], [124, 125], [125, 126], [126, 127], [127, 128], [128, 129], [129, 130]]);;
R:=P177Census(D);;Need(Size(R.F)=520);;
PrintTo("current_c4_descent/130_003.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 130_003 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
