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
D:=P177Graph("096_012",96,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96],[[1, 2], [1, 48], [1, 49], [1, 59], [2, 3], [2, 50], [2, 60], [3, 4], [3, 51], [3, 61], [4, 5], [4, 52], [4, 62], [5, 6], [5, 53], [5, 63], [6, 7], [6, 54], [6, 64], [7, 8], [7, 55], [7, 65], [8, 9], [8, 56], [8, 66], [9, 10], [9, 57], [9, 67], [10, 11], [10, 58], [10, 68], [11, 12], [11, 59], [11, 69], [12, 13], [12, 60], [12, 70], [13, 14], [13, 61], [13, 71], [14, 15], [14, 62], [14, 72], [15, 16], [15, 63], [15, 73], [16, 17], [16, 64], [16, 74], [17, 18], [17, 65], [17, 75], [18, 19], [18, 66], [18, 76], [19, 20], [19, 67], [19, 77], [20, 21], [20, 68], [20, 78], [21, 22], [21, 69], [21, 79], [22, 23], [22, 70], [22, 80], [23, 24], [23, 71], [23, 81], [24, 25], [24, 72], [24, 82], [25, 26], [25, 73], [25, 83], [26, 27], [26, 74], [26, 84], [27, 28], [27, 75], [27, 85], [28, 29], [28, 76], [28, 86], [29, 30], [29, 77], [29, 87], [30, 31], [30, 78], [30, 88], [31, 32], [31, 79], [31, 89], [32, 33], [32, 80], [32, 90], [33, 34], [33, 81], [33, 91], [34, 35], [34, 82], [34, 92], [35, 36], [35, 83], [35, 93], [36, 37], [36, 84], [36, 94], [37, 38], [37, 85], [37, 95], [38, 39], [38, 86], [38, 96], [39, 40], [39, 49], [39, 87], [40, 41], [40, 50], [40, 88], [41, 42], [41, 51], [41, 89], [42, 43], [42, 52], [42, 90], [43, 44], [43, 53], [43, 91], [44, 45], [44, 54], [44, 92], [45, 46], [45, 55], [45, 93], [46, 47], [46, 56], [46, 94], [47, 48], [47, 57], [47, 95], [48, 58], [48, 96], [49, 62], [49, 84], [50, 63], [50, 85], [51, 64], [51, 86], [52, 65], [52, 87], [53, 66], [53, 88], [54, 67], [54, 89], [55, 68], [55, 90], [56, 69], [56, 91], [57, 70], [57, 92], [58, 71], [58, 93], [59, 72], [59, 94], [60, 73], [60, 95], [61, 74], [61, 96], [62, 75], [63, 76], [64, 77], [65, 78], [66, 79], [67, 80], [68, 81], [69, 82], [70, 83], [71, 84], [72, 85], [73, 86], [74, 87], [75, 88], [76, 89], [77, 90], [78, 91], [79, 92], [80, 93], [81, 94], [82, 95], [83, 96]]);;
R:=P177Census(D);;Need(Size(R.F)=384);;
PrintTo("current_c4_descent/096_012.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_012 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
