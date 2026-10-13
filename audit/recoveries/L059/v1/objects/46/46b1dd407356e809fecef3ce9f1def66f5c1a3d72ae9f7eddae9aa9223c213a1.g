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
D:=P177Graph("126_005",126,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105],[[1, 23], [1, 42], [1, 116], [1, 117], [2, 22], [2, 24], [2, 117], [2, 118], [3, 23], [3, 25], [3, 118], [3, 119], [4, 24], [4, 26], [4, 119], [4, 120], [5, 25], [5, 27], [5, 120], [5, 121], [6, 26], [6, 28], [6, 121], [6, 122], [7, 27], [7, 29], [7, 122], [7, 123], [8, 28], [8, 30], [8, 123], [8, 124], [9, 29], [9, 31], [9, 124], [9, 125], [10, 30], [10, 32], [10, 125], [10, 126], [11, 31], [11, 33], [11, 106], [11, 126], [12, 32], [12, 34], [12, 106], [12, 107], [13, 33], [13, 35], [13, 107], [13, 108], [14, 34], [14, 36], [14, 108], [14, 109], [15, 35], [15, 37], [15, 109], [15, 110], [16, 36], [16, 38], [16, 110], [16, 111], [17, 37], [17, 39], [17, 111], [17, 112], [18, 38], [18, 40], [18, 112], [18, 113], [19, 39], [19, 41], [19, 113], [19, 114], [20, 40], [20, 42], [20, 114], [20, 115], [21, 22], [21, 41], [21, 115], [21, 116], [22, 45], [22, 62], [23, 46], [23, 63], [24, 43], [24, 47], [25, 44], [25, 48], [26, 45], [26, 49], [27, 46], [27, 50], [28, 47], [28, 51], [29, 48], [29, 52], [30, 49], [30, 53], [31, 50], [31, 54], [32, 51], [32, 55], [33, 52], [33, 56], [34, 53], [34, 57], [35, 54], [35, 58], [36, 55], [36, 59], [37, 56], [37, 60], [38, 57], [38, 61], [39, 58], [39, 62], [40, 59], [40, 63], [41, 43], [41, 60], [42, 44], [42, 61], [43, 68], [43, 81], [44, 69], [44, 82], [45, 70], [45, 83], [46, 71], [46, 84], [47, 64], [47, 72], [48, 65], [48, 73], [49, 66], [49, 74], [50, 67], [50, 75], [51, 68], [51, 76], [52, 69], [52, 77], [53, 70], [53, 78], [54, 71], [54, 79], [55, 72], [55, 80], [56, 73], [56, 81], [57, 74], [57, 82], [58, 75], [58, 83], [59, 76], [59, 84], [60, 64], [60, 77], [61, 65], [61, 78], [62, 66], [62, 79], [63, 67], [63, 80], [64, 93], [64, 98], [65, 94], [65, 99], [66, 95], [66, 100], [67, 96], [67, 101], [68, 97], [68, 102], [69, 98], [69, 103], [70, 99], [70, 104], [71, 100], [71, 105], [72, 85], [72, 101], [73, 86], [73, 102], [74, 87], [74, 103], [75, 88], [75, 104], [76, 89], [76, 105], [77, 85], [77, 90], [78, 86], [78, 91], [79, 87], [79, 92], [80, 88], [80, 93], [81, 89], [81, 94], [82, 90], [82, 95], [83, 91], [83, 96], [84, 92], [84, 97], [85, 111], [85, 122], [86, 112], [86, 123], [87, 113], [87, 124], [88, 114], [88, 125], [89, 115], [89, 126], [90, 106], [90, 116], [91, 107], [91, 117], [92, 108], [92, 118], [93, 109], [93, 119], [94, 110], [94, 120], [95, 111], [95, 121], [96, 112], [96, 122], [97, 113], [97, 123], [98, 114], [98, 124], [99, 115], [99, 125], [100, 116], [100, 126], [101, 106], [101, 117], [102, 107], [102, 118], [103, 108], [103, 119], [104, 109], [104, 120], [105, 110], [105, 121]]);;
R:=P177Census(D);;Need(Size(R.F)=2016);;
PrintTo("current_c4_descent/126_005.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 126_005 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
