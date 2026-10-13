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
D:=P177Graph("112_002",112,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111],[[1, 2], [1, 16], [1, 98], [1, 112], [2, 3], [2, 17], [2, 99], [3, 4], [3, 18], [3, 100], [4, 5], [4, 19], [4, 101], [5, 6], [5, 20], [5, 102], [6, 7], [6, 21], [6, 103], [7, 8], [7, 22], [7, 104], [8, 9], [8, 23], [8, 105], [9, 10], [9, 24], [9, 106], [10, 11], [10, 25], [10, 107], [11, 12], [11, 26], [11, 108], [12, 13], [12, 27], [12, 109], [13, 14], [13, 28], [13, 110], [14, 15], [14, 29], [14, 111], [15, 16], [15, 30], [15, 112], [16, 17], [16, 31], [17, 18], [17, 32], [18, 19], [18, 33], [19, 20], [19, 34], [20, 21], [20, 35], [21, 22], [21, 36], [22, 23], [22, 37], [23, 24], [23, 38], [24, 25], [24, 39], [25, 26], [25, 40], [26, 27], [26, 41], [27, 28], [27, 42], [28, 29], [28, 43], [29, 30], [29, 44], [30, 31], [30, 45], [31, 32], [31, 46], [32, 33], [32, 47], [33, 34], [33, 48], [34, 35], [34, 49], [35, 36], [35, 50], [36, 37], [36, 51], [37, 38], [37, 52], [38, 39], [38, 53], [39, 40], [39, 54], [40, 41], [40, 55], [41, 42], [41, 56], [42, 43], [42, 57], [43, 44], [43, 58], [44, 45], [44, 59], [45, 46], [45, 60], [46, 47], [46, 61], [47, 48], [47, 62], [48, 49], [48, 63], [49, 50], [49, 64], [50, 51], [50, 65], [51, 52], [51, 66], [52, 53], [52, 67], [53, 54], [53, 68], [54, 55], [54, 69], [55, 56], [55, 70], [56, 57], [56, 71], [57, 58], [57, 72], [58, 59], [58, 73], [59, 60], [59, 74], [60, 61], [60, 75], [61, 62], [61, 76], [62, 63], [62, 77], [63, 64], [63, 78], [64, 65], [64, 79], [65, 66], [65, 80], [66, 67], [66, 81], [67, 68], [67, 82], [68, 69], [68, 83], [69, 70], [69, 84], [70, 71], [70, 85], [71, 72], [71, 86], [72, 73], [72, 87], [73, 74], [73, 88], [74, 75], [74, 89], [75, 76], [75, 90], [76, 77], [76, 91], [77, 78], [77, 92], [78, 79], [78, 93], [79, 80], [79, 94], [80, 81], [80, 95], [81, 82], [81, 96], [82, 83], [82, 97], [83, 84], [83, 98], [84, 85], [84, 99], [85, 86], [85, 100], [86, 87], [86, 101], [87, 88], [87, 102], [88, 89], [88, 103], [89, 90], [89, 104], [90, 91], [90, 105], [91, 92], [91, 106], [92, 93], [92, 107], [93, 94], [93, 108], [94, 95], [94, 109], [95, 96], [95, 110], [96, 97], [96, 111], [97, 98], [97, 112], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108], [108, 109], [109, 110], [110, 111], [111, 112]]);;
R:=P177Census(D);;Need(Size(R.F)=448);;
PrintTo("current_c4_descent/112_002.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 112_002 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
