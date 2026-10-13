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
D:=P177Graph("090_009",90,[1, 4, 5, 6, 8, 13, 17, 19, 20, 21, 22, 23, 25, 27, 28, 29, 30, 31, 34, 40, 41, 46, 50, 52, 55, 57, 58, 59, 60, 62, 64, 67, 68, 69, 71, 74, 75, 77, 78, 79, 81, 82, 83, 87, 88],[[1, 2], [1, 3], [1, 11], [1, 14], [2, 4], [2, 6], [2, 25], [3, 5], [3, 8], [3, 20], [4, 7], [4, 10], [4, 39], [5, 9], [5, 15], [5, 33], [6, 12], [6, 18], [6, 61], [7, 13], [7, 19], [7, 62], [8, 16], [8, 26], [8, 51], [9, 17], [9, 27], [9, 52], [10, 21], [10, 30], [10, 82], [11, 22], [11, 31], [11, 83], [12, 23], [12, 27], [12, 71], [13, 24], [13, 32], [13, 84], [14, 28], [14, 40], [14, 77], [15, 21], [15, 41], [15, 78], [16, 19], [16, 29], [16, 57], [17, 24], [17, 42], [17, 76], [18, 34], [18, 46], [18, 68], [19, 47], [19, 86], [20, 35], [20, 48], [20, 90], [21, 36], [21, 45], [22, 37], [22, 42], [22, 63], [23, 38], [23, 49], [23, 76], [24, 50], [24, 67], [25, 43], [25, 63], [25, 90], [26, 34], [26, 55], [26, 64], [27, 65], [27, 73], [28, 32], [28, 44], [28, 48], [29, 38], [29, 66], [29, 84], [30, 53], [30, 72], [30, 80], [31, 43], [31, 54], [31, 66], [32, 58], [32, 88], [33, 55], [33, 57], [33, 77], [34, 56], [34, 70], [35, 40], [35, 58], [35, 67], [36, 52], [36, 59], [36, 74], [37, 50], [37, 60], [37, 64], [38, 75], [38, 79], [39, 68], [39, 71], [39, 83], [40, 49], [40, 53], [41, 54], [41, 80], [41, 85], [42, 69], [42, 88], [43, 50], [43, 69], [44, 46], [44, 59], [44, 67], [45, 60], [45, 62], [45, 81], [46, 85], [46, 89], [47, 55], [47, 75], [47, 87], [48, 79], [48, 81], [49, 81], [49, 87], [50, 73], [51, 52], [51, 77], [51, 78], [52, 80], [53, 60], [53, 79], [54, 59], [54, 75], [55, 84], [56, 57], [56, 60], [56, 69], [57, 89], [58, 70], [58, 85], [59, 70], [61, 62], [61, 82], [61, 83], [62, 80], [63, 74], [63, 75], [64, 72], [64, 89], [65, 68], [65, 79], [65, 87], [66, 74], [66, 87], [67, 86], [68, 76], [69, 72], [70, 71], [71, 89], [72, 81], [73, 78], [73, 88], [74, 85], [76, 78], [77, 90], [82, 84], [82, 86], [83, 90], [86, 88]]);;
R:=P177Census(D);;Need(Size(R.F)=2880);;
PrintTo("current_c4_descent/090_009.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 090_009 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
