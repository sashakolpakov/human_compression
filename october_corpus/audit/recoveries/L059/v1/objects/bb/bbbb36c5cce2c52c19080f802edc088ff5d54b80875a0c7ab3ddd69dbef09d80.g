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
D:=P177Graph("096_025",96,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95],[[1, 2], [1, 24], [1, 40], [1, 49], [2, 3], [2, 41], [2, 50], [3, 4], [3, 42], [3, 51], [4, 5], [4, 43], [4, 52], [5, 6], [5, 44], [5, 53], [6, 7], [6, 45], [6, 54], [7, 8], [7, 46], [7, 55], [8, 9], [8, 47], [8, 56], [9, 10], [9, 48], [9, 57], [10, 11], [10, 25], [10, 58], [11, 12], [11, 26], [11, 59], [12, 13], [12, 27], [12, 60], [13, 14], [13, 28], [13, 61], [14, 15], [14, 29], [14, 62], [15, 16], [15, 30], [15, 63], [16, 17], [16, 31], [16, 64], [17, 18], [17, 32], [17, 65], [18, 19], [18, 33], [18, 66], [19, 20], [19, 34], [19, 67], [20, 21], [20, 35], [20, 68], [21, 22], [21, 36], [21, 69], [22, 23], [22, 37], [22, 70], [23, 24], [23, 38], [23, 71], [24, 39], [24, 72], [25, 49], [25, 57], [25, 78], [26, 50], [26, 58], [26, 79], [27, 51], [27, 59], [27, 80], [28, 52], [28, 60], [28, 81], [29, 53], [29, 61], [29, 82], [30, 54], [30, 62], [30, 83], [31, 55], [31, 63], [31, 84], [32, 56], [32, 64], [32, 85], [33, 57], [33, 65], [33, 86], [34, 58], [34, 66], [34, 87], [35, 59], [35, 67], [35, 88], [36, 60], [36, 68], [36, 89], [37, 61], [37, 69], [37, 90], [38, 62], [38, 70], [38, 91], [39, 63], [39, 71], [39, 92], [40, 64], [40, 72], [40, 93], [41, 49], [41, 65], [41, 94], [42, 50], [42, 66], [42, 95], [43, 51], [43, 67], [43, 96], [44, 52], [44, 68], [44, 73], [45, 53], [45, 69], [45, 74], [46, 54], [46, 70], [46, 75], [47, 55], [47, 71], [47, 76], [48, 56], [48, 72], [48, 77], [49, 73], [50, 74], [51, 75], [52, 76], [53, 77], [54, 78], [55, 79], [56, 80], [57, 81], [58, 82], [59, 83], [60, 84], [61, 85], [62, 86], [63, 87], [64, 88], [65, 89], [66, 90], [67, 91], [68, 92], [69, 93], [70, 94], [71, 95], [72, 96], [73, 78], [73, 92], [74, 79], [74, 93], [75, 80], [75, 94], [76, 81], [76, 95], [77, 82], [77, 96], [78, 83], [79, 84], [80, 85], [81, 86], [82, 87], [83, 88], [84, 89], [85, 90], [86, 91], [87, 92], [88, 93], [89, 94], [90, 95], [91, 96]]);;
R:=P177Census(D);;Need(Size(R.F)=384);;
PrintTo("current_c4_descent/096_025.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_025 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
