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
D:=P177Graph("096_033",96,[1, 3, 6, 8, 10, 11, 12, 14, 15, 16, 17, 19, 25, 26, 27, 28, 29, 32, 36, 37, 43, 44, 45, 46, 48, 55, 57, 58, 63, 64, 65, 66, 67, 70, 71, 72, 74, 78, 80, 82, 83, 86, 87, 89, 90, 91, 94, 96],[[1, 9], [1, 68], [1, 73], [1, 85], [2, 12], [2, 17], [2, 80], [2, 91], [3, 31], [3, 53], [3, 54], [3, 62], [4, 25], [4, 57], [4, 63], [4, 96], [5, 14], [5, 19], [5, 43], [5, 86], [6, 20], [6, 41], [6, 50], [6, 88], [7, 37], [7, 44], [7, 57], [7, 72], [8, 24], [8, 51], [8, 68], [8, 69], [9, 27], [9, 29], [9, 94], [10, 34], [10, 40], [10, 50], [10, 53], [11, 34], [11, 38], [11, 50], [11, 92], [12, 61], [12, 79], [12, 88], [13, 19], [13, 44], [13, 64], [13, 89], [14, 47], [14, 49], [14, 77], [15, 23], [15, 39], [15, 69], [15, 79], [16, 22], [16, 33], [16, 42], [16, 81], [17, 52], [17, 77], [17, 79], [18, 28], [18, 32], [18, 78], [18, 94], [19, 35], [19, 73], [20, 36], [20, 46], [20, 70], [21, 55], [21, 57], [21, 67], [21, 72], [22, 27], [22, 71], [22, 80], [23, 58], [23, 70], [23, 90], [24, 25], [24, 80], [24, 91], [25, 69], [25, 95], [26, 41], [26, 53], [26, 54], [26, 76], [27, 38], [27, 56], [28, 54], [28, 75], [28, 84], [29, 35], [29, 52], [29, 56], [30, 48], [30, 65], [30, 78], [30, 86], [31, 57], [31, 63], [31, 82], [32, 42], [32, 68], [32, 73], [33, 63], [33, 72], [33, 80], [34, 37], [34, 89], [35, 43], [35, 71], [36, 50], [36, 56], [36, 93], [37, 47], [37, 60], [38, 45], [38, 71], [39, 48], [39, 70], [39, 86], [40, 43], [40, 45], [40, 64], [41, 82], [41, 87], [42, 91], [42, 94], [43, 75], [44, 47], [44, 51], [45, 53], [45, 92], [46, 60], [46, 69], [46, 79], [47, 48], [48, 49], [49, 55], [49, 67], [51, 89], [51, 96], [52, 71], [52, 74], [54, 65], [55, 81], [55, 84], [56, 87], [58, 59], [58, 62], [58, 95], [59, 65], [59, 78], [59, 90], [60, 70], [60, 89], [61, 66], [61, 67], [61, 74], [62, 82], [62, 83], [63, 92], [64, 73], [64, 75], [65, 75], [66, 76], [66, 81], [66, 84], [67, 76], [68, 96], [72, 92], [74, 77], [74, 88], [76, 82], [77, 86], [78, 84], [81, 91], [83, 85], [83, 93], [83, 95], [85, 90], [85, 94], [87, 88], [87, 93], [90, 93], [95, 96]]);;
R:=P177Census(D);;Need(Size(R.F)=192);;
PrintTo("current_c4_descent/096_033.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_033 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
