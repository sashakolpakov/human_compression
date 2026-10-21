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
D:=P177Graph("126_007",126,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105],[[1, 23], [1, 42], [1, 114], [1, 119], [2, 22], [2, 24], [2, 115], [2, 120], [3, 23], [3, 25], [3, 116], [3, 121], [4, 24], [4, 26], [4, 117], [4, 122], [5, 25], [5, 27], [5, 118], [5, 123], [6, 26], [6, 28], [6, 119], [6, 124], [7, 27], [7, 29], [7, 120], [7, 125], [8, 28], [8, 30], [8, 121], [8, 126], [9, 29], [9, 31], [9, 106], [9, 122], [10, 30], [10, 32], [10, 107], [10, 123], [11, 31], [11, 33], [11, 108], [11, 124], [12, 32], [12, 34], [12, 109], [12, 125], [13, 33], [13, 35], [13, 110], [13, 126], [14, 34], [14, 36], [14, 106], [14, 111], [15, 35], [15, 37], [15, 107], [15, 112], [16, 36], [16, 38], [16, 108], [16, 113], [17, 37], [17, 39], [17, 109], [17, 114], [18, 38], [18, 40], [18, 110], [18, 115], [19, 39], [19, 41], [19, 111], [19, 116], [20, 40], [20, 42], [20, 112], [20, 117], [21, 22], [21, 41], [21, 113], [21, 118], [22, 51], [22, 56], [23, 52], [23, 57], [24, 53], [24, 58], [25, 54], [25, 59], [26, 55], [26, 60], [27, 56], [27, 61], [28, 57], [28, 62], [29, 58], [29, 63], [30, 43], [30, 59], [31, 44], [31, 60], [32, 45], [32, 61], [33, 46], [33, 62], [34, 47], [34, 63], [35, 43], [35, 48], [36, 44], [36, 49], [37, 45], [37, 50], [38, 46], [38, 51], [39, 47], [39, 52], [40, 48], [40, 53], [41, 49], [41, 54], [42, 50], [42, 55], [43, 65], [43, 84], [44, 64], [44, 66], [45, 65], [45, 67], [46, 66], [46, 68], [47, 67], [47, 69], [48, 68], [48, 70], [49, 69], [49, 71], [50, 70], [50, 72], [51, 71], [51, 73], [52, 72], [52, 74], [53, 73], [53, 75], [54, 74], [54, 76], [55, 75], [55, 77], [56, 76], [56, 78], [57, 77], [57, 79], [58, 78], [58, 80], [59, 79], [59, 81], [60, 80], [60, 82], [61, 81], [61, 83], [62, 82], [62, 84], [63, 64], [63, 83], [64, 93], [64, 98], [65, 94], [65, 99], [66, 95], [66, 100], [67, 96], [67, 101], [68, 97], [68, 102], [69, 98], [69, 103], [70, 99], [70, 104], [71, 100], [71, 105], [72, 85], [72, 101], [73, 86], [73, 102], [74, 87], [74, 103], [75, 88], [75, 104], [76, 89], [76, 105], [77, 85], [77, 90], [78, 86], [78, 91], [79, 87], [79, 92], [80, 88], [80, 93], [81, 89], [81, 94], [82, 90], [82, 95], [83, 91], [83, 96], [84, 92], [84, 97], [85, 107], [85, 126], [86, 106], [86, 108], [87, 107], [87, 109], [88, 108], [88, 110], [89, 109], [89, 111], [90, 110], [90, 112], [91, 111], [91, 113], [92, 112], [92, 114], [93, 113], [93, 115], [94, 114], [94, 116], [95, 115], [95, 117], [96, 116], [96, 118], [97, 117], [97, 119], [98, 118], [98, 120], [99, 119], [99, 121], [100, 120], [100, 122], [101, 121], [101, 123], [102, 122], [102, 124], [103, 123], [103, 125], [104, 124], [104, 126], [105, 106], [105, 125]]);;
R:=P177Census(D);;Need(Size(R.F)=1008);;
PrintTo("current_c4_descent/126_007.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 126_007 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
