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
D:=P177Graph("110_002",110,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109],[[1, 2], [1, 22], [1, 90], [1, 110], [2, 3], [2, 23], [2, 91], [3, 4], [3, 24], [3, 92], [4, 5], [4, 25], [4, 93], [5, 6], [5, 26], [5, 94], [6, 7], [6, 27], [6, 95], [7, 8], [7, 28], [7, 96], [8, 9], [8, 29], [8, 97], [9, 10], [9, 30], [9, 98], [10, 11], [10, 31], [10, 99], [11, 12], [11, 32], [11, 100], [12, 13], [12, 33], [12, 101], [13, 14], [13, 34], [13, 102], [14, 15], [14, 35], [14, 103], [15, 16], [15, 36], [15, 104], [16, 17], [16, 37], [16, 105], [17, 18], [17, 38], [17, 106], [18, 19], [18, 39], [18, 107], [19, 20], [19, 40], [19, 108], [20, 21], [20, 41], [20, 109], [21, 22], [21, 42], [21, 110], [22, 23], [22, 43], [23, 24], [23, 44], [24, 25], [24, 45], [25, 26], [25, 46], [26, 27], [26, 47], [27, 28], [27, 48], [28, 29], [28, 49], [29, 30], [29, 50], [30, 31], [30, 51], [31, 32], [31, 52], [32, 33], [32, 53], [33, 34], [33, 54], [34, 35], [34, 55], [35, 36], [35, 56], [36, 37], [36, 57], [37, 38], [37, 58], [38, 39], [38, 59], [39, 40], [39, 60], [40, 41], [40, 61], [41, 42], [41, 62], [42, 43], [42, 63], [43, 44], [43, 64], [44, 45], [44, 65], [45, 46], [45, 66], [46, 47], [46, 67], [47, 48], [47, 68], [48, 49], [48, 69], [49, 50], [49, 70], [50, 51], [50, 71], [51, 52], [51, 72], [52, 53], [52, 73], [53, 54], [53, 74], [54, 55], [54, 75], [55, 56], [55, 76], [56, 57], [56, 77], [57, 58], [57, 78], [58, 59], [58, 79], [59, 60], [59, 80], [60, 61], [60, 81], [61, 62], [61, 82], [62, 63], [62, 83], [63, 64], [63, 84], [64, 65], [64, 85], [65, 66], [65, 86], [66, 67], [66, 87], [67, 68], [67, 88], [68, 69], [68, 89], [69, 70], [69, 90], [70, 71], [70, 91], [71, 72], [71, 92], [72, 73], [72, 93], [73, 74], [73, 94], [74, 75], [74, 95], [75, 76], [75, 96], [76, 77], [76, 97], [77, 78], [77, 98], [78, 79], [78, 99], [79, 80], [79, 100], [80, 81], [80, 101], [81, 82], [81, 102], [82, 83], [82, 103], [83, 84], [83, 104], [84, 85], [84, 105], [85, 86], [85, 106], [86, 87], [86, 107], [87, 88], [87, 108], [88, 89], [88, 109], [89, 90], [89, 110], [90, 91], [91, 92], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108], [108, 109], [109, 110]]);;
R:=P177Census(D);;Need(Size(R.F)=440);;
PrintTo("current_c4_descent/110_002.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 110_002 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
