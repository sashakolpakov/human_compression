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
D:=P177Graph("130_002",130,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129],[[1, 2], [1, 48], [1, 84], [1, 130], [2, 3], [2, 49], [2, 85], [3, 4], [3, 50], [3, 86], [4, 5], [4, 51], [4, 87], [5, 6], [5, 52], [5, 88], [6, 7], [6, 53], [6, 89], [7, 8], [7, 54], [7, 90], [8, 9], [8, 55], [8, 91], [9, 10], [9, 56], [9, 92], [10, 11], [10, 57], [10, 93], [11, 12], [11, 58], [11, 94], [12, 13], [12, 59], [12, 95], [13, 14], [13, 60], [13, 96], [14, 15], [14, 61], [14, 97], [15, 16], [15, 62], [15, 98], [16, 17], [16, 63], [16, 99], [17, 18], [17, 64], [17, 100], [18, 19], [18, 65], [18, 101], [19, 20], [19, 66], [19, 102], [20, 21], [20, 67], [20, 103], [21, 22], [21, 68], [21, 104], [22, 23], [22, 69], [22, 105], [23, 24], [23, 70], [23, 106], [24, 25], [24, 71], [24, 107], [25, 26], [25, 72], [25, 108], [26, 27], [26, 73], [26, 109], [27, 28], [27, 74], [27, 110], [28, 29], [28, 75], [28, 111], [29, 30], [29, 76], [29, 112], [30, 31], [30, 77], [30, 113], [31, 32], [31, 78], [31, 114], [32, 33], [32, 79], [32, 115], [33, 34], [33, 80], [33, 116], [34, 35], [34, 81], [34, 117], [35, 36], [35, 82], [35, 118], [36, 37], [36, 83], [36, 119], [37, 38], [37, 84], [37, 120], [38, 39], [38, 85], [38, 121], [39, 40], [39, 86], [39, 122], [40, 41], [40, 87], [40, 123], [41, 42], [41, 88], [41, 124], [42, 43], [42, 89], [42, 125], [43, 44], [43, 90], [43, 126], [44, 45], [44, 91], [44, 127], [45, 46], [45, 92], [45, 128], [46, 47], [46, 93], [46, 129], [47, 48], [47, 94], [47, 130], [48, 49], [48, 95], [49, 50], [49, 96], [50, 51], [50, 97], [51, 52], [51, 98], [52, 53], [52, 99], [53, 54], [53, 100], [54, 55], [54, 101], [55, 56], [55, 102], [56, 57], [56, 103], [57, 58], [57, 104], [58, 59], [58, 105], [59, 60], [59, 106], [60, 61], [60, 107], [61, 62], [61, 108], [62, 63], [62, 109], [63, 64], [63, 110], [64, 65], [64, 111], [65, 66], [65, 112], [66, 67], [66, 113], [67, 68], [67, 114], [68, 69], [68, 115], [69, 70], [69, 116], [70, 71], [70, 117], [71, 72], [71, 118], [72, 73], [72, 119], [73, 74], [73, 120], [74, 75], [74, 121], [75, 76], [75, 122], [76, 77], [76, 123], [77, 78], [77, 124], [78, 79], [78, 125], [79, 80], [79, 126], [80, 81], [80, 127], [81, 82], [81, 128], [82, 83], [82, 129], [83, 84], [83, 130], [84, 85], [85, 86], [86, 87], [87, 88], [88, 89], [89, 90], [90, 91], [91, 92], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108], [108, 109], [109, 110], [110, 111], [111, 112], [112, 113], [113, 114], [114, 115], [115, 116], [116, 117], [117, 118], [118, 119], [119, 120], [120, 121], [121, 122], [122, 123], [123, 124], [124, 125], [125, 126], [126, 127], [127, 128], [128, 129], [129, 130]]);;
R:=P177Census(D);;Need(Size(R.F)=520);;
PrintTo("current_c4_descent/130_002.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 130_002 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
