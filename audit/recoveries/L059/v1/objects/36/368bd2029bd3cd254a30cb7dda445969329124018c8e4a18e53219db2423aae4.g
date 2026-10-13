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
D:=P177Graph("108_004",108,[1, 3, 5, 7, 9, 11, 13, 15, 17, 20, 22, 24, 26, 28, 30, 32, 34, 36, 37, 39, 41, 43, 45, 47, 49, 51, 53, 56, 58, 60, 62, 64, 66, 68, 70, 72, 73, 75, 77, 79, 81, 83, 85, 87, 89, 92, 94, 96, 98, 100, 102, 104, 106, 108],[[1, 2], [1, 18], [1, 19], [1, 97], [2, 3], [2, 20], [2, 98], [3, 4], [3, 21], [3, 99], [4, 5], [4, 22], [4, 100], [5, 6], [5, 23], [5, 101], [6, 7], [6, 24], [6, 102], [7, 8], [7, 25], [7, 103], [8, 9], [8, 26], [8, 104], [9, 10], [9, 27], [9, 105], [10, 11], [10, 28], [10, 106], [11, 12], [11, 29], [11, 107], [12, 13], [12, 30], [12, 108], [13, 14], [13, 31], [13, 91], [14, 15], [14, 32], [14, 92], [15, 16], [15, 33], [15, 93], [16, 17], [16, 34], [16, 94], [17, 18], [17, 35], [17, 95], [18, 36], [18, 96], [19, 20], [19, 36], [19, 37], [20, 21], [20, 38], [21, 22], [21, 39], [22, 23], [22, 40], [23, 24], [23, 41], [24, 25], [24, 42], [25, 26], [25, 43], [26, 27], [26, 44], [27, 28], [27, 45], [28, 29], [28, 46], [29, 30], [29, 47], [30, 31], [30, 48], [31, 32], [31, 49], [32, 33], [32, 50], [33, 34], [33, 51], [34, 35], [34, 52], [35, 36], [35, 53], [36, 54], [37, 38], [37, 54], [37, 55], [38, 39], [38, 56], [39, 40], [39, 57], [40, 41], [40, 58], [41, 42], [41, 59], [42, 43], [42, 60], [43, 44], [43, 61], [44, 45], [44, 62], [45, 46], [45, 63], [46, 47], [46, 64], [47, 48], [47, 65], [48, 49], [48, 66], [49, 50], [49, 67], [50, 51], [50, 68], [51, 52], [51, 69], [52, 53], [52, 70], [53, 54], [53, 71], [54, 72], [55, 56], [55, 72], [55, 73], [56, 57], [56, 74], [57, 58], [57, 75], [58, 59], [58, 76], [59, 60], [59, 77], [60, 61], [60, 78], [61, 62], [61, 79], [62, 63], [62, 80], [63, 64], [63, 81], [64, 65], [64, 82], [65, 66], [65, 83], [66, 67], [66, 84], [67, 68], [67, 85], [68, 69], [68, 86], [69, 70], [69, 87], [70, 71], [70, 88], [71, 72], [71, 89], [72, 90], [73, 74], [73, 90], [73, 91], [74, 75], [74, 92], [75, 76], [75, 93], [76, 77], [76, 94], [77, 78], [77, 95], [78, 79], [78, 96], [79, 80], [79, 97], [80, 81], [80, 98], [81, 82], [81, 99], [82, 83], [82, 100], [83, 84], [83, 101], [84, 85], [84, 102], [85, 86], [85, 103], [86, 87], [86, 104], [87, 88], [87, 105], [88, 89], [88, 106], [89, 90], [89, 107], [90, 108], [91, 92], [91, 108], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108]]);;
R:=P177Census(D);;Need(Size(R.F)=432);;
PrintTo("current_c4_descent/108_004.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 108_004 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
