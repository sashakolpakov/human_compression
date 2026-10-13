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
D:=P177Graph("096_032",96,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80],[[1, 17], [1, 29], [1, 86], [1, 95], [2, 18], [2, 30], [2, 87], [2, 96], [3, 19], [3, 31], [3, 88], [3, 93], [4, 20], [4, 32], [4, 85], [4, 94], [5, 17], [5, 21], [5, 83], [5, 90], [6, 18], [6, 22], [6, 84], [6, 91], [7, 19], [7, 23], [7, 81], [7, 92], [8, 20], [8, 24], [8, 82], [8, 89], [9, 21], [9, 25], [9, 87], [9, 94], [10, 22], [10, 26], [10, 88], [10, 95], [11, 23], [11, 27], [11, 85], [11, 96], [12, 24], [12, 28], [12, 86], [12, 93], [13, 25], [13, 29], [13, 82], [13, 91], [14, 26], [14, 30], [14, 83], [14, 92], [15, 27], [15, 31], [15, 84], [15, 89], [16, 28], [16, 32], [16, 81], [16, 90], [17, 42], [17, 47], [18, 43], [18, 48], [19, 44], [19, 45], [20, 41], [20, 46], [21, 35], [21, 46], [22, 36], [22, 47], [23, 33], [23, 48], [24, 34], [24, 45], [25, 34], [25, 39], [26, 35], [26, 40], [27, 36], [27, 37], [28, 33], [28, 38], [29, 38], [29, 43], [30, 39], [30, 44], [31, 40], [31, 41], [32, 37], [32, 42], [33, 55], [33, 64], [34, 56], [34, 61], [35, 53], [35, 62], [36, 54], [36, 63], [37, 52], [37, 59], [38, 49], [38, 60], [39, 50], [39, 57], [40, 51], [40, 58], [41, 56], [41, 63], [42, 53], [42, 64], [43, 54], [43, 61], [44, 55], [44, 62], [45, 51], [45, 60], [46, 52], [46, 57], [47, 49], [47, 58], [48, 50], [48, 59], [49, 65], [49, 77], [50, 66], [50, 78], [51, 67], [51, 79], [52, 68], [52, 80], [53, 65], [53, 69], [54, 66], [54, 70], [55, 67], [55, 71], [56, 68], [56, 72], [57, 69], [57, 73], [58, 70], [58, 74], [59, 71], [59, 75], [60, 72], [60, 76], [61, 73], [61, 77], [62, 74], [62, 78], [63, 75], [63, 79], [64, 76], [64, 80], [65, 90], [65, 95], [66, 91], [66, 96], [67, 92], [67, 93], [68, 89], [68, 94], [69, 83], [69, 94], [70, 84], [70, 95], [71, 81], [71, 96], [72, 82], [72, 93], [73, 82], [73, 87], [74, 83], [74, 88], [75, 84], [75, 85], [76, 81], [76, 86], [77, 86], [77, 91], [78, 87], [78, 92], [79, 88], [79, 89], [80, 85], [80, 90]]);;
R:=P177Census(D);;Need(Size(R.F)=384);;
PrintTo("current_c4_descent/096_032.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_032 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
