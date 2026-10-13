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
D:=P177Graph("120_037",120,[1, 4, 5, 6, 8, 12, 15, 17, 18, 19, 22, 23, 24, 26, 28, 32, 33, 34, 39, 40, 43, 46, 48, 49, 51, 54, 55, 57, 58, 62, 63, 64, 67, 68, 70, 71, 73, 75, 77, 78, 81, 82, 85, 88, 90, 91, 96, 100, 102, 104, 105, 107, 108, 110, 111, 112, 113, 114, 118, 119],[[1, 2], [1, 3], [1, 92], [1, 103], [2, 4], [2, 5], [2, 110], [3, 6], [3, 8], [3, 105], [4, 7], [4, 9], [4, 76], [5, 10], [5, 13], [5, 47], [6, 11], [6, 14], [6, 52], [7, 12], [7, 15], [7, 82], [8, 16], [8, 21], [8, 30], [9, 17], [9, 22], [9, 70], [10, 18], [10, 23], [10, 77], [11, 19], [11, 24], [11, 57], [12, 20], [12, 25], [12, 101], [13, 26], [13, 33], [13, 48], [14, 23], [14, 34], [14, 91], [15, 27], [15, 35], [15, 89], [16, 17], [16, 28], [16, 54], [17, 29], [17, 36], [18, 30], [18, 37], [18, 83], [19, 31], [19, 38], [19, 80], [20, 32], [20, 39], [20, 51], [21, 40], [21, 51], [21, 71], [22, 41], [22, 52], [22, 72], [23, 36], [23, 45], [24, 42], [24, 53], [24, 65], [25, 43], [25, 54], [25, 108], [26, 27], [26, 44], [26, 79], [27, 46], [27, 55], [28, 47], [28, 56], [28, 72], [29, 48], [29, 57], [29, 104], [30, 49], [30, 102], [31, 32], [31, 33], [31, 58], [32, 50], [32, 59], [33, 60], [33, 95], [34, 61], [34, 76], [34, 83], [35, 62], [35, 77], [35, 96], [36, 55], [36, 68], [37, 63], [37, 78], [37, 90], [38, 64], [38, 77], [38, 114], [39, 65], [39, 79], [39, 117], [40, 42], [40, 66], [40, 99], [41, 43], [41, 67], [41, 100], [42, 46], [42, 68], [43, 69], [43, 80], [44, 70], [44, 81], [44, 96], [45, 71], [45, 82], [45, 104], [46, 72], [46, 83], [47, 73], [47, 113], [48, 74], [48, 115], [49, 50], [49, 52], [49, 84], [50, 75], [50, 85], [51, 86], [51, 93], [52, 111], [53, 54], [53, 67], [53, 112], [54, 87], [55, 80], [55, 93], [56, 75], [56, 81], [56, 88], [57, 98], [57, 109], [58, 89], [58, 99], [58, 117], [59, 73], [59, 90], [59, 100], [60, 63], [60, 91], [60, 114], [61, 62], [61, 64], [61, 85], [62, 65], [62, 92], [63, 69], [63, 93], [64, 94], [64, 101], [65, 102], [66, 78], [66, 91], [66, 112], [67, 89], [67, 103], [68, 95], [68, 101], [69, 96], [69, 104], [70, 86], [70, 97], [71, 87], [71, 106], [72, 119], [73, 76], [73, 84], [74, 75], [74, 77], [74, 105], [75, 106], [76, 107], [78, 79], [78, 92], [79, 107], [80, 102], [81, 99], [81, 103], [82, 97], [82, 116], [83, 118], [84, 108], [84, 114], [85, 97], [85, 109], [86, 88], [86, 108], [87, 90], [87, 110], [88, 94], [88, 95], [89, 113], [90, 115], [91, 98], [92, 108], [93, 111], [94, 104], [94, 112], [95, 107], [96, 120], [97, 105], [98, 100], [98, 110], [99, 111], [100, 116], [101, 113], [102, 115], [103, 114], [105, 117], [106, 113], [106, 118], [107, 109], [109, 119], [110, 117], [111, 116], [112, 120], [115, 119], [116, 118], [118, 120], [119, 120]]);;
R:=P177Census(D);;Need(Size(R.F)=960);;
PrintTo("current_c4_descent/120_037.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_037 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
