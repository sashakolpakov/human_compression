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
D:=P177Graph("108_012",108,[1, 2, 3, 4, 5, 6, 7, 8, 9, 19, 20, 21, 22, 23, 24, 25, 26, 27, 37, 38, 39, 40, 41, 42, 43, 44, 45, 55, 56, 57, 58, 59, 60, 61, 62, 63, 73, 74, 75, 76, 77, 78, 79, 80, 81, 91, 92, 93, 94, 95, 96, 97, 98, 99],[[1, 13], [1, 16], [1, 104], [1, 108], [2, 14], [2, 17], [2, 105], [2, 106], [3, 15], [3, 18], [3, 103], [3, 107], [4, 10], [4, 16], [4, 102], [4, 107], [5, 11], [5, 17], [5, 100], [5, 108], [6, 12], [6, 18], [6, 101], [6, 106], [7, 10], [7, 13], [7, 101], [7, 105], [8, 11], [8, 14], [8, 102], [8, 103], [9, 12], [9, 15], [9, 100], [9, 104], [10, 20], [10, 21], [11, 19], [11, 21], [12, 19], [12, 20], [13, 23], [13, 24], [14, 22], [14, 24], [15, 22], [15, 23], [16, 26], [16, 27], [17, 25], [17, 27], [18, 25], [18, 26], [19, 33], [19, 35], [20, 31], [20, 36], [21, 32], [21, 34], [22, 29], [22, 36], [23, 30], [23, 34], [24, 28], [24, 35], [25, 30], [25, 32], [26, 28], [26, 33], [27, 29], [27, 31], [28, 41], [28, 45], [29, 42], [29, 43], [30, 40], [30, 44], [31, 39], [31, 44], [32, 37], [32, 45], [33, 38], [33, 43], [34, 38], [34, 42], [35, 39], [35, 40], [36, 37], [36, 41], [37, 49], [37, 52], [38, 50], [38, 53], [39, 51], [39, 54], [40, 46], [40, 52], [41, 47], [41, 53], [42, 48], [42, 54], [43, 46], [43, 49], [44, 47], [44, 50], [45, 48], [45, 51], [46, 56], [46, 57], [47, 55], [47, 57], [48, 55], [48, 56], [49, 59], [49, 60], [50, 58], [50, 60], [51, 58], [51, 59], [52, 62], [52, 63], [53, 61], [53, 63], [54, 61], [54, 62], [55, 69], [55, 71], [56, 67], [56, 72], [57, 68], [57, 70], [58, 65], [58, 72], [59, 66], [59, 70], [60, 64], [60, 71], [61, 66], [61, 68], [62, 64], [62, 69], [63, 65], [63, 67], [64, 77], [64, 81], [65, 78], [65, 79], [66, 76], [66, 80], [67, 75], [67, 80], [68, 73], [68, 81], [69, 74], [69, 79], [70, 74], [70, 78], [71, 75], [71, 76], [72, 73], [72, 77], [73, 85], [73, 88], [74, 86], [74, 89], [75, 87], [75, 90], [76, 82], [76, 88], [77, 83], [77, 89], [78, 84], [78, 90], [79, 82], [79, 85], [80, 83], [80, 86], [81, 84], [81, 87], [82, 92], [82, 93], [83, 91], [83, 93], [84, 91], [84, 92], [85, 95], [85, 96], [86, 94], [86, 96], [87, 94], [87, 95], [88, 98], [88, 99], [89, 97], [89, 99], [90, 97], [90, 98], [91, 105], [91, 107], [92, 103], [92, 108], [93, 104], [93, 106], [94, 101], [94, 108], [95, 102], [95, 106], [96, 100], [96, 107], [97, 102], [97, 104], [98, 100], [98, 105], [99, 101], [99, 103]]);;
R:=P177Census(D);;Need(Size(R.F)=432);;
PrintTo("current_c4_descent/108_012.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 108_012 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
