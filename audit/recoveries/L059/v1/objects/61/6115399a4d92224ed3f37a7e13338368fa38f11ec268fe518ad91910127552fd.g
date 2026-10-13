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
D:=P177Graph("096_003",96,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95],[[1, 2], [1, 32], [1, 66], [1, 96], [2, 3], [2, 33], [2, 67], [3, 4], [3, 34], [3, 68], [4, 5], [4, 35], [4, 69], [5, 6], [5, 36], [5, 70], [6, 7], [6, 37], [6, 71], [7, 8], [7, 38], [7, 72], [8, 9], [8, 39], [8, 73], [9, 10], [9, 40], [9, 74], [10, 11], [10, 41], [10, 75], [11, 12], [11, 42], [11, 76], [12, 13], [12, 43], [12, 77], [13, 14], [13, 44], [13, 78], [14, 15], [14, 45], [14, 79], [15, 16], [15, 46], [15, 80], [16, 17], [16, 47], [16, 81], [17, 18], [17, 48], [17, 82], [18, 19], [18, 49], [18, 83], [19, 20], [19, 50], [19, 84], [20, 21], [20, 51], [20, 85], [21, 22], [21, 52], [21, 86], [22, 23], [22, 53], [22, 87], [23, 24], [23, 54], [23, 88], [24, 25], [24, 55], [24, 89], [25, 26], [25, 56], [25, 90], [26, 27], [26, 57], [26, 91], [27, 28], [27, 58], [27, 92], [28, 29], [28, 59], [28, 93], [29, 30], [29, 60], [29, 94], [30, 31], [30, 61], [30, 95], [31, 32], [31, 62], [31, 96], [32, 33], [32, 63], [33, 34], [33, 64], [34, 35], [34, 65], [35, 36], [35, 66], [36, 37], [36, 67], [37, 38], [37, 68], [38, 39], [38, 69], [39, 40], [39, 70], [40, 41], [40, 71], [41, 42], [41, 72], [42, 43], [42, 73], [43, 44], [43, 74], [44, 45], [44, 75], [45, 46], [45, 76], [46, 47], [46, 77], [47, 48], [47, 78], [48, 49], [48, 79], [49, 50], [49, 80], [50, 51], [50, 81], [51, 52], [51, 82], [52, 53], [52, 83], [53, 54], [53, 84], [54, 55], [54, 85], [55, 56], [55, 86], [56, 57], [56, 87], [57, 58], [57, 88], [58, 59], [58, 89], [59, 60], [59, 90], [60, 61], [60, 91], [61, 62], [61, 92], [62, 63], [62, 93], [63, 64], [63, 94], [64, 65], [64, 95], [65, 66], [65, 96], [66, 67], [67, 68], [68, 69], [69, 70], [70, 71], [71, 72], [72, 73], [73, 74], [74, 75], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80], [80, 81], [81, 82], [82, 83], [83, 84], [84, 85], [85, 86], [86, 87], [87, 88], [88, 89], [89, 90], [90, 91], [91, 92], [92, 93], [93, 94], [94, 95], [95, 96]]);;
R:=P177Census(D);;Need(Size(R.F)=384);;
PrintTo("current_c4_descent/096_003.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_003 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
