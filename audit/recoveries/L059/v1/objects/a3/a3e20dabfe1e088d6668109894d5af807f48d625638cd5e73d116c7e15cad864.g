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
D:=P177Graph("090_004",90,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89],[[1, 2], [1, 30], [1, 31], [1, 70], [2, 3], [2, 32], [2, 71], [3, 4], [3, 33], [3, 72], [4, 5], [4, 34], [4, 73], [5, 6], [5, 35], [5, 74], [6, 7], [6, 36], [6, 75], [7, 8], [7, 37], [7, 76], [8, 9], [8, 38], [8, 77], [9, 10], [9, 39], [9, 78], [10, 11], [10, 40], [10, 79], [11, 12], [11, 41], [11, 80], [12, 13], [12, 42], [12, 81], [13, 14], [13, 43], [13, 82], [14, 15], [14, 44], [14, 83], [15, 16], [15, 45], [15, 84], [16, 17], [16, 46], [16, 85], [17, 18], [17, 47], [17, 86], [18, 19], [18, 48], [18, 87], [19, 20], [19, 49], [19, 88], [20, 21], [20, 50], [20, 89], [21, 22], [21, 51], [21, 90], [22, 23], [22, 52], [22, 61], [23, 24], [23, 53], [23, 62], [24, 25], [24, 54], [24, 63], [25, 26], [25, 55], [25, 64], [26, 27], [26, 56], [26, 65], [27, 28], [27, 57], [27, 66], [28, 29], [28, 58], [28, 67], [29, 30], [29, 59], [29, 68], [30, 60], [30, 69], [31, 32], [31, 60], [31, 61], [32, 33], [32, 62], [33, 34], [33, 63], [34, 35], [34, 64], [35, 36], [35, 65], [36, 37], [36, 66], [37, 38], [37, 67], [38, 39], [38, 68], [39, 40], [39, 69], [40, 41], [40, 70], [41, 42], [41, 71], [42, 43], [42, 72], [43, 44], [43, 73], [44, 45], [44, 74], [45, 46], [45, 75], [46, 47], [46, 76], [47, 48], [47, 77], [48, 49], [48, 78], [49, 50], [49, 79], [50, 51], [50, 80], [51, 52], [51, 81], [52, 53], [52, 82], [53, 54], [53, 83], [54, 55], [54, 84], [55, 56], [55, 85], [56, 57], [56, 86], [57, 58], [57, 87], [58, 59], [58, 88], [59, 60], [59, 89], [60, 90], [61, 62], [61, 90], [62, 63], [63, 64], [64, 65], [65, 66], [66, 67], [67, 68], [68, 69], [69, 70], [70, 71], [71, 72], [72, 73], [73, 74], [74, 75], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80], [80, 81], [81, 82], [82, 83], [83, 84], [84, 85], [85, 86], [86, 87], [87, 88], [88, 89], [89, 90]]);;
R:=P177Census(D);;Need(Size(R.F)=360);;
PrintTo("current_c4_descent/090_004.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 090_004 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
