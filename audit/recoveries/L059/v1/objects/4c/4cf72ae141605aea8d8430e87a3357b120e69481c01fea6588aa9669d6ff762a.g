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
D:=P177Graph("128_026",128,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112],[[1, 17], [1, 29], [1, 116], [1, 125], [2, 18], [2, 30], [2, 113], [2, 126], [3, 19], [3, 31], [3, 114], [3, 127], [4, 20], [4, 32], [4, 115], [4, 128], [5, 17], [5, 21], [5, 113], [5, 120], [6, 18], [6, 22], [6, 114], [6, 117], [7, 19], [7, 23], [7, 115], [7, 118], [8, 20], [8, 24], [8, 116], [8, 119], [9, 21], [9, 25], [9, 117], [9, 124], [10, 22], [10, 26], [10, 118], [10, 121], [11, 23], [11, 27], [11, 119], [11, 122], [12, 24], [12, 28], [12, 120], [12, 123], [13, 25], [13, 29], [13, 121], [13, 128], [14, 26], [14, 30], [14, 122], [14, 125], [15, 27], [15, 31], [15, 123], [15, 126], [16, 28], [16, 32], [16, 124], [16, 127], [17, 36], [17, 37], [18, 33], [18, 38], [19, 34], [19, 39], [20, 35], [20, 40], [21, 40], [21, 41], [22, 37], [22, 42], [23, 38], [23, 43], [24, 39], [24, 44], [25, 44], [25, 45], [26, 41], [26, 46], [27, 42], [27, 47], [28, 43], [28, 48], [29, 33], [29, 48], [30, 34], [30, 45], [31, 35], [31, 46], [32, 36], [32, 47], [33, 50], [33, 64], [34, 51], [34, 61], [35, 52], [35, 62], [36, 49], [36, 63], [37, 52], [37, 54], [38, 49], [38, 55], [39, 50], [39, 56], [40, 51], [40, 53], [41, 56], [41, 58], [42, 53], [42, 59], [43, 54], [43, 60], [44, 55], [44, 57], [45, 60], [45, 62], [46, 57], [46, 63], [47, 58], [47, 64], [48, 59], [48, 61], [49, 68], [49, 71], [50, 65], [50, 72], [51, 66], [51, 69], [52, 67], [52, 70], [53, 72], [53, 75], [54, 69], [54, 76], [55, 70], [55, 73], [56, 71], [56, 74], [57, 76], [57, 79], [58, 73], [58, 80], [59, 74], [59, 77], [60, 75], [60, 78], [61, 67], [61, 80], [62, 68], [62, 77], [63, 65], [63, 78], [64, 66], [64, 79], [65, 83], [65, 95], [66, 84], [66, 96], [67, 81], [67, 93], [68, 82], [68, 94], [69, 83], [69, 87], [70, 84], [70, 88], [71, 81], [71, 85], [72, 82], [72, 86], [73, 87], [73, 91], [74, 88], [74, 92], [75, 85], [75, 89], [76, 86], [76, 90], [77, 91], [77, 95], [78, 92], [78, 96], [79, 89], [79, 93], [80, 90], [80, 94], [81, 98], [81, 103], [82, 99], [82, 104], [83, 100], [83, 101], [84, 97], [84, 102], [85, 102], [85, 107], [86, 103], [86, 108], [87, 104], [87, 105], [88, 101], [88, 106], [89, 106], [89, 111], [90, 107], [90, 112], [91, 108], [91, 109], [92, 105], [92, 110], [93, 99], [93, 110], [94, 100], [94, 111], [95, 97], [95, 112], [96, 98], [96, 109], [97, 116], [97, 126], [98, 113], [98, 127], [99, 114], [99, 128], [100, 115], [100, 125], [101, 114], [101, 120], [102, 115], [102, 117], [103, 116], [103, 118], [104, 113], [104, 119], [105, 118], [105, 124], [106, 119], [106, 121], [107, 120], [107, 122], [108, 117], [108, 123], [109, 122], [109, 128], [110, 123], [110, 125], [111, 124], [111, 126], [112, 121], [112, 127]]);;
R:=P177Census(D);;Need(Size(R.F)=1024);;
PrintTo("current_c4_descent/128_026.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_026 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
