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
D:=P177Graph("108_003",108,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107],[[1, 2], [1, 36], [1, 37], [1, 94], [2, 3], [2, 38], [2, 95], [3, 4], [3, 39], [3, 96], [4, 5], [4, 40], [4, 97], [5, 6], [5, 41], [5, 98], [6, 7], [6, 42], [6, 99], [7, 8], [7, 43], [7, 100], [8, 9], [8, 44], [8, 101], [9, 10], [9, 45], [9, 102], [10, 11], [10, 46], [10, 103], [11, 12], [11, 47], [11, 104], [12, 13], [12, 48], [12, 105], [13, 14], [13, 49], [13, 106], [14, 15], [14, 50], [14, 107], [15, 16], [15, 51], [15, 108], [16, 17], [16, 52], [16, 73], [17, 18], [17, 53], [17, 74], [18, 19], [18, 54], [18, 75], [19, 20], [19, 55], [19, 76], [20, 21], [20, 56], [20, 77], [21, 22], [21, 57], [21, 78], [22, 23], [22, 58], [22, 79], [23, 24], [23, 59], [23, 80], [24, 25], [24, 60], [24, 81], [25, 26], [25, 61], [25, 82], [26, 27], [26, 62], [26, 83], [27, 28], [27, 63], [27, 84], [28, 29], [28, 64], [28, 85], [29, 30], [29, 65], [29, 86], [30, 31], [30, 66], [30, 87], [31, 32], [31, 67], [31, 88], [32, 33], [32, 68], [32, 89], [33, 34], [33, 69], [33, 90], [34, 35], [34, 70], [34, 91], [35, 36], [35, 71], [35, 92], [36, 72], [36, 93], [37, 38], [37, 72], [37, 73], [38, 39], [38, 74], [39, 40], [39, 75], [40, 41], [40, 76], [41, 42], [41, 77], [42, 43], [42, 78], [43, 44], [43, 79], [44, 45], [44, 80], [45, 46], [45, 81], [46, 47], [46, 82], [47, 48], [47, 83], [48, 49], [48, 84], [49, 50], [49, 85], [50, 51], [50, 86], [51, 52], [51, 87], [52, 53], [52, 88], [53, 54], [53, 89], [54, 55], [54, 90], [55, 56], [55, 91], [56, 57], [56, 92], [57, 58], [57, 93], [58, 59], [58, 94], [59, 60], [59, 95], [60, 61], [60, 96], [61, 62], [61, 97], [62, 63], [62, 98], [63, 64], [63, 99], [64, 65], [64, 100], [65, 66], [65, 101], [66, 67], [66, 102], [67, 68], [67, 103], [68, 69], [68, 104], [69, 70], [69, 105], [70, 71], [70, 106], [71, 72], [71, 107], [72, 108], [73, 74], [73, 108], [74, 75], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80], [80, 81], [81, 82], [82, 83], [83, 84], [84, 85], [85, 86], [86, 87], [87, 88], [88, 89], [89, 90], [90, 91], [91, 92], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108]]);;
R:=P177Census(D);;Need(Size(R.F)=432);;
PrintTo("current_c4_descent/108_003.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 108_003 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
