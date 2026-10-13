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
D:=P177Graph("112_005",112,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112],[[1, 2], [1, 28], [1, 29], [1, 89], [2, 3], [2, 30], [2, 90], [3, 4], [3, 31], [3, 91], [4, 5], [4, 32], [4, 92], [5, 6], [5, 33], [5, 93], [6, 7], [6, 34], [6, 94], [7, 8], [7, 35], [7, 95], [8, 9], [8, 36], [8, 96], [9, 10], [9, 37], [9, 97], [10, 11], [10, 38], [10, 98], [11, 12], [11, 39], [11, 99], [12, 13], [12, 40], [12, 100], [13, 14], [13, 41], [13, 101], [14, 15], [14, 42], [14, 102], [15, 16], [15, 43], [15, 103], [16, 17], [16, 44], [16, 104], [17, 18], [17, 45], [17, 105], [18, 19], [18, 46], [18, 106], [19, 20], [19, 47], [19, 107], [20, 21], [20, 48], [20, 108], [21, 22], [21, 49], [21, 109], [22, 23], [22, 50], [22, 110], [23, 24], [23, 51], [23, 111], [24, 25], [24, 52], [24, 112], [25, 26], [25, 53], [25, 85], [26, 27], [26, 54], [26, 86], [27, 28], [27, 55], [27, 87], [28, 56], [28, 88], [29, 30], [29, 56], [29, 57], [30, 31], [30, 58], [31, 32], [31, 59], [32, 33], [32, 60], [33, 34], [33, 61], [34, 35], [34, 62], [35, 36], [35, 63], [36, 37], [36, 64], [37, 38], [37, 65], [38, 39], [38, 66], [39, 40], [39, 67], [40, 41], [40, 68], [41, 42], [41, 69], [42, 43], [42, 70], [43, 44], [43, 71], [44, 45], [44, 72], [45, 46], [45, 73], [46, 47], [46, 74], [47, 48], [47, 75], [48, 49], [48, 76], [49, 50], [49, 77], [50, 51], [50, 78], [51, 52], [51, 79], [52, 53], [52, 80], [53, 54], [53, 81], [54, 55], [54, 82], [55, 56], [55, 83], [56, 84], [57, 58], [57, 84], [57, 85], [58, 59], [58, 86], [59, 60], [59, 87], [60, 61], [60, 88], [61, 62], [61, 89], [62, 63], [62, 90], [63, 64], [63, 91], [64, 65], [64, 92], [65, 66], [65, 93], [66, 67], [66, 94], [67, 68], [67, 95], [68, 69], [68, 96], [69, 70], [69, 97], [70, 71], [70, 98], [71, 72], [71, 99], [72, 73], [72, 100], [73, 74], [73, 101], [74, 75], [74, 102], [75, 76], [75, 103], [76, 77], [76, 104], [77, 78], [77, 105], [78, 79], [78, 106], [79, 80], [79, 107], [80, 81], [80, 108], [81, 82], [81, 109], [82, 83], [82, 110], [83, 84], [83, 111], [84, 112], [85, 86], [85, 112], [86, 87], [87, 88], [88, 89], [89, 90], [90, 91], [91, 92], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108], [108, 109], [109, 110], [110, 111], [111, 112]]);;
R:=P177Census(D);;Need(Size(R.F)=448);;
PrintTo("current_c4_descent/112_005.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 112_005 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
