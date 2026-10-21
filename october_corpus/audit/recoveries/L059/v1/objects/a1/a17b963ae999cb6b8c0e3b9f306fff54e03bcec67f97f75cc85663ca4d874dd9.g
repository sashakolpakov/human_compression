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
D:=P177Graph("120_002",120,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119],[[1, 2], [1, 12], [1, 110], [1, 120], [2, 3], [2, 13], [2, 111], [3, 4], [3, 14], [3, 112], [4, 5], [4, 15], [4, 113], [5, 6], [5, 16], [5, 114], [6, 7], [6, 17], [6, 115], [7, 8], [7, 18], [7, 116], [8, 9], [8, 19], [8, 117], [9, 10], [9, 20], [9, 118], [10, 11], [10, 21], [10, 119], [11, 12], [11, 22], [11, 120], [12, 13], [12, 23], [13, 14], [13, 24], [14, 15], [14, 25], [15, 16], [15, 26], [16, 17], [16, 27], [17, 18], [17, 28], [18, 19], [18, 29], [19, 20], [19, 30], [20, 21], [20, 31], [21, 22], [21, 32], [22, 23], [22, 33], [23, 24], [23, 34], [24, 25], [24, 35], [25, 26], [25, 36], [26, 27], [26, 37], [27, 28], [27, 38], [28, 29], [28, 39], [29, 30], [29, 40], [30, 31], [30, 41], [31, 32], [31, 42], [32, 33], [32, 43], [33, 34], [33, 44], [34, 35], [34, 45], [35, 36], [35, 46], [36, 37], [36, 47], [37, 38], [37, 48], [38, 39], [38, 49], [39, 40], [39, 50], [40, 41], [40, 51], [41, 42], [41, 52], [42, 43], [42, 53], [43, 44], [43, 54], [44, 45], [44, 55], [45, 46], [45, 56], [46, 47], [46, 57], [47, 48], [47, 58], [48, 49], [48, 59], [49, 50], [49, 60], [50, 51], [50, 61], [51, 52], [51, 62], [52, 53], [52, 63], [53, 54], [53, 64], [54, 55], [54, 65], [55, 56], [55, 66], [56, 57], [56, 67], [57, 58], [57, 68], [58, 59], [58, 69], [59, 60], [59, 70], [60, 61], [60, 71], [61, 62], [61, 72], [62, 63], [62, 73], [63, 64], [63, 74], [64, 65], [64, 75], [65, 66], [65, 76], [66, 67], [66, 77], [67, 68], [67, 78], [68, 69], [68, 79], [69, 70], [69, 80], [70, 71], [70, 81], [71, 72], [71, 82], [72, 73], [72, 83], [73, 74], [73, 84], [74, 75], [74, 85], [75, 76], [75, 86], [76, 77], [76, 87], [77, 78], [77, 88], [78, 79], [78, 89], [79, 80], [79, 90], [80, 81], [80, 91], [81, 82], [81, 92], [82, 83], [82, 93], [83, 84], [83, 94], [84, 85], [84, 95], [85, 86], [85, 96], [86, 87], [86, 97], [87, 88], [87, 98], [88, 89], [88, 99], [89, 90], [89, 100], [90, 91], [90, 101], [91, 92], [91, 102], [92, 93], [92, 103], [93, 94], [93, 104], [94, 95], [94, 105], [95, 96], [95, 106], [96, 97], [96, 107], [97, 98], [97, 108], [98, 99], [98, 109], [99, 100], [99, 110], [100, 101], [100, 111], [101, 102], [101, 112], [102, 103], [102, 113], [103, 104], [103, 114], [104, 105], [104, 115], [105, 106], [105, 116], [106, 107], [106, 117], [107, 108], [107, 118], [108, 109], [108, 119], [109, 110], [109, 120], [110, 111], [111, 112], [112, 113], [113, 114], [114, 115], [115, 116], [116, 117], [117, 118], [118, 119], [119, 120]]);;
R:=P177Census(D);;Need(Size(R.F)=480);;
PrintTo("current_c4_descent/120_002.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_002 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
