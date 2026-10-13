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
D:=P177Graph("090_002",90,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89],[[1, 2], [1, 20], [1, 72], [1, 90], [2, 3], [2, 21], [2, 73], [3, 4], [3, 22], [3, 74], [4, 5], [4, 23], [4, 75], [5, 6], [5, 24], [5, 76], [6, 7], [6, 25], [6, 77], [7, 8], [7, 26], [7, 78], [8, 9], [8, 27], [8, 79], [9, 10], [9, 28], [9, 80], [10, 11], [10, 29], [10, 81], [11, 12], [11, 30], [11, 82], [12, 13], [12, 31], [12, 83], [13, 14], [13, 32], [13, 84], [14, 15], [14, 33], [14, 85], [15, 16], [15, 34], [15, 86], [16, 17], [16, 35], [16, 87], [17, 18], [17, 36], [17, 88], [18, 19], [18, 37], [18, 89], [19, 20], [19, 38], [19, 90], [20, 21], [20, 39], [21, 22], [21, 40], [22, 23], [22, 41], [23, 24], [23, 42], [24, 25], [24, 43], [25, 26], [25, 44], [26, 27], [26, 45], [27, 28], [27, 46], [28, 29], [28, 47], [29, 30], [29, 48], [30, 31], [30, 49], [31, 32], [31, 50], [32, 33], [32, 51], [33, 34], [33, 52], [34, 35], [34, 53], [35, 36], [35, 54], [36, 37], [36, 55], [37, 38], [37, 56], [38, 39], [38, 57], [39, 40], [39, 58], [40, 41], [40, 59], [41, 42], [41, 60], [42, 43], [42, 61], [43, 44], [43, 62], [44, 45], [44, 63], [45, 46], [45, 64], [46, 47], [46, 65], [47, 48], [47, 66], [48, 49], [48, 67], [49, 50], [49, 68], [50, 51], [50, 69], [51, 52], [51, 70], [52, 53], [52, 71], [53, 54], [53, 72], [54, 55], [54, 73], [55, 56], [55, 74], [56, 57], [56, 75], [57, 58], [57, 76], [58, 59], [58, 77], [59, 60], [59, 78], [60, 61], [60, 79], [61, 62], [61, 80], [62, 63], [62, 81], [63, 64], [63, 82], [64, 65], [64, 83], [65, 66], [65, 84], [66, 67], [66, 85], [67, 68], [67, 86], [68, 69], [68, 87], [69, 70], [69, 88], [70, 71], [70, 89], [71, 72], [71, 90], [72, 73], [73, 74], [74, 75], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80], [80, 81], [81, 82], [82, 83], [83, 84], [84, 85], [85, 86], [86, 87], [87, 88], [88, 89], [89, 90]]);;
R:=P177Census(D);;Need(Size(R.F)=360);;
PrintTo("current_c4_descent/090_002.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 090_002 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
