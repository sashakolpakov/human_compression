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
D:=P177Graph("096_040",96,[1, 3, 4, 6, 9, 11, 13, 14, 16, 18, 19, 21, 24, 28, 30, 32, 34, 36, 39, 41, 42, 45, 47, 48, 50, 51, 53, 55, 56, 59, 63, 65, 68, 70, 73, 75, 76, 78, 79, 80, 81, 83, 89, 90, 92, 94, 95, 96],[[1, 2], [1, 5], [1, 26], [1, 46], [2, 4], [2, 6], [2, 14], [3, 7], [3, 15], [3, 27], [3, 52], [4, 8], [4, 23], [4, 44], [5, 11], [5, 16], [5, 30], [6, 12], [6, 17], [6, 31], [7, 13], [7, 18], [7, 21], [8, 11], [8, 19], [8, 32], [9, 12], [9, 15], [9, 20], [9, 25], [10, 11], [10, 21], [10, 50], [10, 78], [11, 22], [12, 47], [12, 76], [13, 20], [13, 29], [13, 54], [14, 25], [14, 33], [14, 57], [15, 34], [15, 41], [16, 27], [16, 35], [16, 58], [17, 28], [17, 36], [17, 59], [18, 22], [18, 37], [18, 60], [19, 29], [19, 38], [19, 61], [20, 39], [20, 42], [21, 40], [21, 43], [22, 28], [22, 53], [23, 42], [23, 70], [23, 96], [24, 25], [24, 43], [24, 61], [24, 84], [25, 45], [26, 34], [26, 81], [26, 90], [27, 63], [27, 94], [28, 74], [28, 87], [29, 80], [29, 95], [30, 52], [30, 62], [30, 84], [31, 51], [31, 53], [31, 63], [32, 54], [32, 64], [32, 85], [33, 50], [33, 65], [33, 79], [34, 66], [34, 74], [35, 36], [35, 45], [35, 55], [36, 67], [36, 86], [37, 47], [37, 68], [37, 83], [38, 56], [38, 65], [38, 76], [39, 44], [39, 69], [39, 87], [40, 45], [40, 56], [40, 70], [41, 46], [41, 71], [41, 88], [42, 49], [42, 72], [43, 73], [43, 75], [44, 55], [44, 73], [45, 82], [46, 56], [46, 83], [47, 58], [47, 85], [48, 49], [48, 52], [48, 57], [48, 85], [49, 53], [49, 75], [50, 72], [50, 88], [51, 54], [51, 66], [51, 84], [52, 59], [53, 77], [54, 79], [55, 60], [55, 88], [56, 87], [57, 78], [57, 80], [58, 73], [58, 80], [59, 72], [59, 82], [60, 76], [60, 81], [61, 63], [61, 83], [62, 70], [62, 89], [62, 95], [63, 69], [64, 81], [64, 89], [64, 94], [65, 67], [65, 77], [66, 68], [66, 78], [67, 90], [67, 96], [68, 82], [68, 91], [69, 90], [69, 92], [70, 74], [71, 80], [71, 92], [71, 96], [72, 81], [73, 77], [74, 79], [75, 91], [75, 93], [76, 93], [77, 89], [78, 86], [79, 93], [82, 92], [83, 86], [84, 96], [85, 90], [86, 89], [87, 94], [88, 95], [91, 94], [91, 95], [92, 93]]);;
R:=P177Census(D);;Need(Size(R.F)=384);;
PrintTo("current_c4_descent/096_040.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_040 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
