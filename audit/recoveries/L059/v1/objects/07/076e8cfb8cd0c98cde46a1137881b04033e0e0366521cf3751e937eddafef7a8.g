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
D:=P177Graph("128_009",128,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112],[[1, 17], [1, 32], [1, 117], [1, 124], [2, 17], [2, 18], [2, 118], [2, 125], [3, 18], [3, 19], [3, 119], [3, 126], [4, 19], [4, 20], [4, 120], [4, 127], [5, 20], [5, 21], [5, 121], [5, 128], [6, 21], [6, 22], [6, 113], [6, 122], [7, 22], [7, 23], [7, 114], [7, 123], [8, 23], [8, 24], [8, 115], [8, 124], [9, 24], [9, 25], [9, 116], [9, 125], [10, 25], [10, 26], [10, 117], [10, 126], [11, 26], [11, 27], [11, 118], [11, 127], [12, 27], [12, 28], [12, 119], [12, 128], [13, 28], [13, 29], [13, 113], [13, 120], [14, 29], [14, 30], [14, 114], [14, 121], [15, 30], [15, 31], [15, 115], [15, 122], [16, 31], [16, 32], [16, 116], [16, 123], [17, 37], [17, 46], [18, 38], [18, 47], [19, 39], [19, 48], [20, 33], [20, 40], [21, 34], [21, 41], [22, 35], [22, 42], [23, 36], [23, 43], [24, 37], [24, 44], [25, 38], [25, 45], [26, 39], [26, 46], [27, 40], [27, 47], [28, 41], [28, 48], [29, 33], [29, 42], [30, 34], [30, 43], [31, 35], [31, 44], [32, 36], [32, 45], [33, 56], [33, 57], [34, 57], [34, 58], [35, 58], [35, 59], [36, 59], [36, 60], [37, 60], [37, 61], [38, 61], [38, 62], [39, 62], [39, 63], [40, 63], [40, 64], [41, 49], [41, 64], [42, 49], [42, 50], [43, 50], [43, 51], [44, 51], [44, 52], [45, 52], [45, 53], [46, 53], [46, 54], [47, 54], [47, 55], [48, 55], [48, 56], [49, 70], [49, 77], [50, 71], [50, 78], [51, 72], [51, 79], [52, 73], [52, 80], [53, 65], [53, 74], [54, 66], [54, 75], [55, 67], [55, 76], [56, 68], [56, 77], [57, 69], [57, 78], [58, 70], [58, 79], [59, 71], [59, 80], [60, 65], [60, 72], [61, 66], [61, 73], [62, 67], [62, 74], [63, 68], [63, 75], [64, 69], [64, 76], [65, 81], [65, 96], [66, 81], [66, 82], [67, 82], [67, 83], [68, 83], [68, 84], [69, 84], [69, 85], [70, 85], [70, 86], [71, 86], [71, 87], [72, 87], [72, 88], [73, 88], [73, 89], [74, 89], [74, 90], [75, 90], [75, 91], [76, 91], [76, 92], [77, 92], [77, 93], [78, 93], [78, 94], [79, 94], [79, 95], [80, 95], [80, 96], [81, 101], [81, 110], [82, 102], [82, 111], [83, 103], [83, 112], [84, 97], [84, 104], [85, 98], [85, 105], [86, 99], [86, 106], [87, 100], [87, 107], [88, 101], [88, 108], [89, 102], [89, 109], [90, 103], [90, 110], [91, 104], [91, 111], [92, 105], [92, 112], [93, 97], [93, 106], [94, 98], [94, 107], [95, 99], [95, 108], [96, 100], [96, 109], [97, 120], [97, 121], [98, 121], [98, 122], [99, 122], [99, 123], [100, 123], [100, 124], [101, 124], [101, 125], [102, 125], [102, 126], [103, 126], [103, 127], [104, 127], [104, 128], [105, 113], [105, 128], [106, 113], [106, 114], [107, 114], [107, 115], [108, 115], [108, 116], [109, 116], [109, 117], [110, 117], [110, 118], [111, 118], [111, 119], [112, 119], [112, 120]]);;
R:=P177Census(D);;Need(Size(R.F)=512);;
PrintTo("current_c4_descent/128_009.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_009 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
