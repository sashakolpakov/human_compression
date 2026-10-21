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
D:=P177Graph("130_004",130,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129],[[1, 2], [1, 58], [1, 74], [1, 130], [2, 3], [2, 59], [2, 75], [3, 4], [3, 60], [3, 76], [4, 5], [4, 61], [4, 77], [5, 6], [5, 62], [5, 78], [6, 7], [6, 63], [6, 79], [7, 8], [7, 64], [7, 80], [8, 9], [8, 65], [8, 81], [9, 10], [9, 66], [9, 82], [10, 11], [10, 67], [10, 83], [11, 12], [11, 68], [11, 84], [12, 13], [12, 69], [12, 85], [13, 14], [13, 70], [13, 86], [14, 15], [14, 71], [14, 87], [15, 16], [15, 72], [15, 88], [16, 17], [16, 73], [16, 89], [17, 18], [17, 74], [17, 90], [18, 19], [18, 75], [18, 91], [19, 20], [19, 76], [19, 92], [20, 21], [20, 77], [20, 93], [21, 22], [21, 78], [21, 94], [22, 23], [22, 79], [22, 95], [23, 24], [23, 80], [23, 96], [24, 25], [24, 81], [24, 97], [25, 26], [25, 82], [25, 98], [26, 27], [26, 83], [26, 99], [27, 28], [27, 84], [27, 100], [28, 29], [28, 85], [28, 101], [29, 30], [29, 86], [29, 102], [30, 31], [30, 87], [30, 103], [31, 32], [31, 88], [31, 104], [32, 33], [32, 89], [32, 105], [33, 34], [33, 90], [33, 106], [34, 35], [34, 91], [34, 107], [35, 36], [35, 92], [35, 108], [36, 37], [36, 93], [36, 109], [37, 38], [37, 94], [37, 110], [38, 39], [38, 95], [38, 111], [39, 40], [39, 96], [39, 112], [40, 41], [40, 97], [40, 113], [41, 42], [41, 98], [41, 114], [42, 43], [42, 99], [42, 115], [43, 44], [43, 100], [43, 116], [44, 45], [44, 101], [44, 117], [45, 46], [45, 102], [45, 118], [46, 47], [46, 103], [46, 119], [47, 48], [47, 104], [47, 120], [48, 49], [48, 105], [48, 121], [49, 50], [49, 106], [49, 122], [50, 51], [50, 107], [50, 123], [51, 52], [51, 108], [51, 124], [52, 53], [52, 109], [52, 125], [53, 54], [53, 110], [53, 126], [54, 55], [54, 111], [54, 127], [55, 56], [55, 112], [55, 128], [56, 57], [56, 113], [56, 129], [57, 58], [57, 114], [57, 130], [58, 59], [58, 115], [59, 60], [59, 116], [60, 61], [60, 117], [61, 62], [61, 118], [62, 63], [62, 119], [63, 64], [63, 120], [64, 65], [64, 121], [65, 66], [65, 122], [66, 67], [66, 123], [67, 68], [67, 124], [68, 69], [68, 125], [69, 70], [69, 126], [70, 71], [70, 127], [71, 72], [71, 128], [72, 73], [72, 129], [73, 74], [73, 130], [74, 75], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80], [80, 81], [81, 82], [82, 83], [83, 84], [84, 85], [85, 86], [86, 87], [87, 88], [88, 89], [89, 90], [90, 91], [91, 92], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108], [108, 109], [109, 110], [110, 111], [111, 112], [112, 113], [113, 114], [114, 115], [115, 116], [116, 117], [117, 118], [118, 119], [119, 120], [120, 121], [121, 122], [122, 123], [123, 124], [124, 125], [125, 126], [126, 127], [127, 128], [128, 129], [129, 130]]);;
R:=P177Census(D);;Need(Size(R.F)=520);;
PrintTo("current_c4_descent/130_004.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 130_004 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
