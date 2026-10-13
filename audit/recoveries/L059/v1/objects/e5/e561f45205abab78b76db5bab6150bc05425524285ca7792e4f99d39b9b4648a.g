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
D:=P177Graph("108_011",108,[1, 2, 3, 4, 5, 6, 7, 8, 9, 19, 20, 21, 22, 23, 24, 25, 26, 27, 37, 38, 39, 40, 41, 42, 43, 44, 45, 55, 56, 57, 58, 59, 60, 61, 62, 63, 73, 74, 75, 76, 77, 78, 79, 80, 81, 91, 92, 93, 94, 95, 96, 97, 98, 99],[[1, 13], [1, 16], [1, 104], [1, 108], [2, 14], [2, 17], [2, 105], [2, 106], [3, 15], [3, 18], [3, 103], [3, 107], [4, 10], [4, 16], [4, 102], [4, 107], [5, 11], [5, 17], [5, 100], [5, 108], [6, 12], [6, 18], [6, 101], [6, 106], [7, 10], [7, 13], [7, 101], [7, 105], [8, 11], [8, 14], [8, 102], [8, 103], [9, 12], [9, 15], [9, 100], [9, 104], [10, 20], [10, 21], [11, 19], [11, 21], [12, 19], [12, 20], [13, 23], [13, 24], [14, 22], [14, 24], [15, 22], [15, 23], [16, 26], [16, 27], [17, 25], [17, 27], [18, 25], [18, 26], [19, 32], [19, 36], [20, 33], [20, 34], [21, 31], [21, 35], [22, 30], [22, 35], [23, 28], [23, 36], [24, 29], [24, 34], [25, 29], [25, 33], [26, 30], [26, 31], [27, 28], [27, 32], [28, 40], [28, 43], [29, 41], [29, 44], [30, 42], [30, 45], [31, 37], [31, 43], [32, 38], [32, 44], [33, 39], [33, 45], [34, 37], [34, 40], [35, 38], [35, 41], [36, 39], [36, 42], [37, 47], [37, 48], [38, 46], [38, 48], [39, 46], [39, 47], [40, 50], [40, 51], [41, 49], [41, 51], [42, 49], [42, 50], [43, 53], [43, 54], [44, 52], [44, 54], [45, 52], [45, 53], [46, 59], [46, 63], [47, 60], [47, 61], [48, 58], [48, 62], [49, 57], [49, 62], [50, 55], [50, 63], [51, 56], [51, 61], [52, 56], [52, 60], [53, 57], [53, 58], [54, 55], [54, 59], [55, 67], [55, 70], [56, 68], [56, 71], [57, 69], [57, 72], [58, 64], [58, 70], [59, 65], [59, 71], [60, 66], [60, 72], [61, 64], [61, 67], [62, 65], [62, 68], [63, 66], [63, 69], [64, 74], [64, 75], [65, 73], [65, 75], [66, 73], [66, 74], [67, 77], [67, 78], [68, 76], [68, 78], [69, 76], [69, 77], [70, 80], [70, 81], [71, 79], [71, 81], [72, 79], [72, 80], [73, 86], [73, 90], [74, 87], [74, 88], [75, 85], [75, 89], [76, 84], [76, 89], [77, 82], [77, 90], [78, 83], [78, 88], [79, 83], [79, 87], [80, 84], [80, 85], [81, 82], [81, 86], [82, 94], [82, 97], [83, 95], [83, 98], [84, 96], [84, 99], [85, 91], [85, 97], [86, 92], [86, 98], [87, 93], [87, 99], [88, 91], [88, 94], [89, 92], [89, 95], [90, 93], [90, 96], [91, 101], [91, 102], [92, 100], [92, 102], [93, 100], [93, 101], [94, 104], [94, 105], [95, 103], [95, 105], [96, 103], [96, 104], [97, 107], [97, 108], [98, 106], [98, 108], [99, 106], [99, 107]]);;
R:=P177Census(D);;Need(Size(R.F)=432);;
PrintTo("current_c4_descent/108_011.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 108_011 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
