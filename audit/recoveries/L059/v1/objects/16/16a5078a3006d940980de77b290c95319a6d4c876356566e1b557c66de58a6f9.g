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
D:=P177Graph("096_026",96,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95],[[1, 2], [1, 24], [1, 48], [1, 49], [2, 3], [2, 25], [2, 50], [3, 4], [3, 26], [3, 51], [4, 5], [4, 27], [4, 52], [5, 6], [5, 28], [5, 53], [6, 7], [6, 29], [6, 54], [7, 8], [7, 30], [7, 55], [8, 9], [8, 31], [8, 56], [9, 10], [9, 32], [9, 57], [10, 11], [10, 33], [10, 58], [11, 12], [11, 34], [11, 59], [12, 13], [12, 35], [12, 60], [13, 14], [13, 36], [13, 61], [14, 15], [14, 37], [14, 62], [15, 16], [15, 38], [15, 63], [16, 17], [16, 39], [16, 64], [17, 18], [17, 40], [17, 65], [18, 19], [18, 41], [18, 66], [19, 20], [19, 42], [19, 67], [20, 21], [20, 43], [20, 68], [21, 22], [21, 44], [21, 69], [22, 23], [22, 45], [22, 70], [23, 24], [23, 46], [23, 71], [24, 47], [24, 72], [25, 49], [25, 53], [25, 94], [26, 50], [26, 54], [26, 95], [27, 51], [27, 55], [27, 96], [28, 52], [28, 56], [28, 73], [29, 53], [29, 57], [29, 74], [30, 54], [30, 58], [30, 75], [31, 55], [31, 59], [31, 76], [32, 56], [32, 60], [32, 77], [33, 57], [33, 61], [33, 78], [34, 58], [34, 62], [34, 79], [35, 59], [35, 63], [35, 80], [36, 60], [36, 64], [36, 81], [37, 61], [37, 65], [37, 82], [38, 62], [38, 66], [38, 83], [39, 63], [39, 67], [39, 84], [40, 64], [40, 68], [40, 85], [41, 65], [41, 69], [41, 86], [42, 66], [42, 70], [42, 87], [43, 67], [43, 71], [43, 88], [44, 68], [44, 72], [44, 89], [45, 49], [45, 69], [45, 90], [46, 50], [46, 70], [46, 91], [47, 51], [47, 71], [47, 92], [48, 52], [48, 72], [48, 93], [49, 73], [50, 74], [51, 75], [52, 76], [53, 77], [54, 78], [55, 79], [56, 80], [57, 81], [58, 82], [59, 83], [60, 84], [61, 85], [62, 86], [63, 87], [64, 88], [65, 89], [66, 90], [67, 91], [68, 92], [69, 93], [70, 94], [71, 95], [72, 96], [73, 80], [73, 90], [74, 81], [74, 91], [75, 82], [75, 92], [76, 83], [76, 93], [77, 84], [77, 94], [78, 85], [78, 95], [79, 86], [79, 96], [80, 87], [81, 88], [82, 89], [83, 90], [84, 91], [85, 92], [86, 93], [87, 94], [88, 95], [89, 96]]);;
R:=P177Census(D);;Need(Size(R.F)=384);;
PrintTo("current_c4_descent/096_026.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_026 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
