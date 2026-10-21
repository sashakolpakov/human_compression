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
D:=P177Graph("096_007",96,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96],[[1, 2], [1, 48], [1, 49], [1, 75], [2, 3], [2, 50], [2, 76], [3, 4], [3, 51], [3, 77], [4, 5], [4, 52], [4, 78], [5, 6], [5, 53], [5, 79], [6, 7], [6, 54], [6, 80], [7, 8], [7, 55], [7, 81], [8, 9], [8, 56], [8, 82], [9, 10], [9, 57], [9, 83], [10, 11], [10, 58], [10, 84], [11, 12], [11, 59], [11, 85], [12, 13], [12, 60], [12, 86], [13, 14], [13, 61], [13, 87], [14, 15], [14, 62], [14, 88], [15, 16], [15, 63], [15, 89], [16, 17], [16, 64], [16, 90], [17, 18], [17, 65], [17, 91], [18, 19], [18, 66], [18, 92], [19, 20], [19, 67], [19, 93], [20, 21], [20, 68], [20, 94], [21, 22], [21, 69], [21, 95], [22, 23], [22, 70], [22, 96], [23, 24], [23, 49], [23, 71], [24, 25], [24, 50], [24, 72], [25, 26], [25, 51], [25, 73], [26, 27], [26, 52], [26, 74], [27, 28], [27, 53], [27, 75], [28, 29], [28, 54], [28, 76], [29, 30], [29, 55], [29, 77], [30, 31], [30, 56], [30, 78], [31, 32], [31, 57], [31, 79], [32, 33], [32, 58], [32, 80], [33, 34], [33, 59], [33, 81], [34, 35], [34, 60], [34, 82], [35, 36], [35, 61], [35, 83], [36, 37], [36, 62], [36, 84], [37, 38], [37, 63], [37, 85], [38, 39], [38, 64], [38, 86], [39, 40], [39, 65], [39, 87], [40, 41], [40, 66], [40, 88], [41, 42], [41, 67], [41, 89], [42, 43], [42, 68], [42, 90], [43, 44], [43, 69], [43, 91], [44, 45], [44, 70], [44, 92], [45, 46], [45, 71], [45, 93], [46, 47], [46, 72], [46, 94], [47, 48], [47, 73], [47, 95], [48, 74], [48, 96], [49, 50], [49, 96], [50, 51], [51, 52], [52, 53], [53, 54], [54, 55], [55, 56], [56, 57], [57, 58], [58, 59], [59, 60], [60, 61], [61, 62], [62, 63], [63, 64], [64, 65], [65, 66], [66, 67], [67, 68], [68, 69], [69, 70], [70, 71], [71, 72], [72, 73], [73, 74], [74, 75], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80], [80, 81], [81, 82], [82, 83], [83, 84], [84, 85], [85, 86], [86, 87], [87, 88], [88, 89], [89, 90], [90, 91], [91, 92], [92, 93], [93, 94], [94, 95], [95, 96]]);;
R:=P177Census(D);;Need(Size(R.F)=384);;
PrintTo("current_c4_descent/096_007.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_007 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
