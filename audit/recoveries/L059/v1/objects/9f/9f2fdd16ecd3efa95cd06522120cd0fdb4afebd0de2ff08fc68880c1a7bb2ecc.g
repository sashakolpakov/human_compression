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
D:=P177Graph("120_008",120,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120],[[1, 2], [1, 60], [1, 61], [1, 83], [2, 3], [2, 62], [2, 84], [3, 4], [3, 63], [3, 85], [4, 5], [4, 64], [4, 86], [5, 6], [5, 65], [5, 87], [6, 7], [6, 66], [6, 88], [7, 8], [7, 67], [7, 89], [8, 9], [8, 68], [8, 90], [9, 10], [9, 69], [9, 91], [10, 11], [10, 70], [10, 92], [11, 12], [11, 71], [11, 93], [12, 13], [12, 72], [12, 94], [13, 14], [13, 73], [13, 95], [14, 15], [14, 74], [14, 96], [15, 16], [15, 75], [15, 97], [16, 17], [16, 76], [16, 98], [17, 18], [17, 77], [17, 99], [18, 19], [18, 78], [18, 100], [19, 20], [19, 79], [19, 101], [20, 21], [20, 80], [20, 102], [21, 22], [21, 81], [21, 103], [22, 23], [22, 82], [22, 104], [23, 24], [23, 83], [23, 105], [24, 25], [24, 84], [24, 106], [25, 26], [25, 85], [25, 107], [26, 27], [26, 86], [26, 108], [27, 28], [27, 87], [27, 109], [28, 29], [28, 88], [28, 110], [29, 30], [29, 89], [29, 111], [30, 31], [30, 90], [30, 112], [31, 32], [31, 91], [31, 113], [32, 33], [32, 92], [32, 114], [33, 34], [33, 93], [33, 115], [34, 35], [34, 94], [34, 116], [35, 36], [35, 95], [35, 117], [36, 37], [36, 96], [36, 118], [37, 38], [37, 97], [37, 119], [38, 39], [38, 98], [38, 120], [39, 40], [39, 61], [39, 99], [40, 41], [40, 62], [40, 100], [41, 42], [41, 63], [41, 101], [42, 43], [42, 64], [42, 102], [43, 44], [43, 65], [43, 103], [44, 45], [44, 66], [44, 104], [45, 46], [45, 67], [45, 105], [46, 47], [46, 68], [46, 106], [47, 48], [47, 69], [47, 107], [48, 49], [48, 70], [48, 108], [49, 50], [49, 71], [49, 109], [50, 51], [50, 72], [50, 110], [51, 52], [51, 73], [51, 111], [52, 53], [52, 74], [52, 112], [53, 54], [53, 75], [53, 113], [54, 55], [54, 76], [54, 114], [55, 56], [55, 77], [55, 115], [56, 57], [56, 78], [56, 116], [57, 58], [57, 79], [57, 117], [58, 59], [58, 80], [58, 118], [59, 60], [59, 81], [59, 119], [60, 82], [60, 120], [61, 62], [61, 120], [62, 63], [63, 64], [64, 65], [65, 66], [66, 67], [67, 68], [68, 69], [69, 70], [70, 71], [71, 72], [72, 73], [73, 74], [74, 75], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80], [80, 81], [81, 82], [82, 83], [83, 84], [84, 85], [85, 86], [86, 87], [87, 88], [88, 89], [89, 90], [90, 91], [91, 92], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108], [108, 109], [109, 110], [110, 111], [111, 112], [112, 113], [113, 114], [114, 115], [115, 116], [116, 117], [117, 118], [118, 119], [119, 120]]);;
R:=P177Census(D);;Need(Size(R.F)=480);;
PrintTo("current_c4_descent/120_008.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_008 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
