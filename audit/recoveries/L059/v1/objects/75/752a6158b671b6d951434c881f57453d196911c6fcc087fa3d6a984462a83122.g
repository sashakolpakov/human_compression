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
D:=P177Graph("096_053",96,[1, 6, 7, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96],[[1, 2], [1, 3], [1, 4], [1, 5], [2, 85], [2, 92], [2, 93], [3, 87], [3, 90], [3, 94], [4, 88], [4, 89], [4, 95], [5, 86], [5, 91], [5, 96], [6, 8], [6, 12], [6, 14], [6, 15], [7, 9], [7, 10], [7, 11], [7, 13], [8, 20], [8, 28], [8, 36], [9, 23], [9, 28], [9, 37], [10, 24], [10, 31], [10, 41], [11, 27], [11, 30], [11, 39], [12, 26], [12, 30], [12, 38], [13, 21], [13, 29], [13, 42], [14, 25], [14, 31], [14, 43], [15, 22], [15, 29], [15, 40], [16, 23], [16, 27], [16, 32], [16, 33], [17, 21], [17, 24], [17, 34], [17, 35], [18, 20], [18, 25], [18, 32], [18, 35], [19, 22], [19, 26], [19, 33], [19, 34], [20, 78], [20, 82], [21, 73], [21, 84], [22, 74], [22, 83], [23, 75], [23, 81], [24, 76], [24, 81], [25, 77], [25, 83], [26, 80], [26, 82], [27, 79], [27, 84], [28, 65], [28, 71], [29, 68], [29, 69], [30, 67], [30, 70], [31, 66], [31, 72], [32, 61], [32, 69], [33, 62], [33, 72], [34, 64], [34, 71], [35, 63], [35, 70], [36, 53], [36, 54], [36, 73], [37, 55], [37, 56], [37, 74], [38, 55], [38, 59], [38, 76], [39, 53], [39, 57], [39, 77], [40, 57], [40, 60], [40, 75], [41, 54], [41, 60], [41, 80], [42, 58], [42, 59], [42, 78], [43, 56], [43, 58], [43, 79], [44, 73], [44, 75], [44, 76], [44, 79], [45, 74], [45, 77], [45, 78], [45, 80], [46, 69], [46, 70], [46, 71], [46, 72], [47, 65], [47, 66], [47, 67], [47, 68], [48, 55], [48, 57], [48, 62], [48, 67], [49, 59], [49, 60], [49, 64], [49, 68], [50, 53], [50, 56], [50, 61], [50, 65], [51, 54], [51, 58], [51, 63], [51, 66], [52, 61], [52, 62], [52, 63], [52, 64], [53, 90], [54, 92], [55, 92], [56, 91], [57, 89], [58, 89], [59, 90], [60, 91], [61, 93], [62, 94], [63, 96], [64, 95], [65, 88], [66, 87], [67, 86], [68, 85], [69, 89], [70, 90], [71, 92], [72, 91], [73, 93], [74, 93], [75, 95], [76, 94], [77, 94], [78, 95], [79, 96], [80, 96], [81, 85], [81, 86], [82, 85], [82, 87], [83, 86], [83, 88], [84, 87], [84, 88]]);;
R:=P177Census(D);;Need(Size(R.F)=384);;
PrintTo("current_c4_descent/096_053.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_053 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
