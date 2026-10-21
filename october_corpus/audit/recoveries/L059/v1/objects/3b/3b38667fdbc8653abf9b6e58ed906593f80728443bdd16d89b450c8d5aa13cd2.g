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
D:=P177Graph("090_005",90,[1, 2, 3, 4, 5, 11, 12, 13, 14, 15, 21, 22, 23, 24, 25, 31, 32, 33, 34, 35, 41, 42, 43, 44, 45, 51, 52, 53, 54, 55, 61, 62, 63, 64, 65, 71, 72, 73, 74, 75, 81, 82, 83, 84, 85],[[1, 7], [1, 10], [1, 88], [1, 89], [2, 6], [2, 8], [2, 89], [2, 90], [3, 7], [3, 9], [3, 86], [3, 90], [4, 8], [4, 10], [4, 86], [4, 87], [5, 6], [5, 9], [5, 87], [5, 88], [6, 13], [6, 14], [7, 14], [7, 15], [8, 11], [8, 15], [9, 11], [9, 12], [10, 12], [10, 13], [11, 17], [11, 20], [12, 16], [12, 18], [13, 17], [13, 19], [14, 18], [14, 20], [15, 16], [15, 19], [16, 23], [16, 24], [17, 24], [17, 25], [18, 21], [18, 25], [19, 21], [19, 22], [20, 22], [20, 23], [21, 27], [21, 30], [22, 26], [22, 28], [23, 27], [23, 29], [24, 28], [24, 30], [25, 26], [25, 29], [26, 33], [26, 34], [27, 34], [27, 35], [28, 31], [28, 35], [29, 31], [29, 32], [30, 32], [30, 33], [31, 37], [31, 40], [32, 36], [32, 38], [33, 37], [33, 39], [34, 38], [34, 40], [35, 36], [35, 39], [36, 43], [36, 44], [37, 44], [37, 45], [38, 41], [38, 45], [39, 41], [39, 42], [40, 42], [40, 43], [41, 47], [41, 50], [42, 46], [42, 48], [43, 47], [43, 49], [44, 48], [44, 50], [45, 46], [45, 49], [46, 53], [46, 54], [47, 54], [47, 55], [48, 51], [48, 55], [49, 51], [49, 52], [50, 52], [50, 53], [51, 57], [51, 60], [52, 56], [52, 58], [53, 57], [53, 59], [54, 58], [54, 60], [55, 56], [55, 59], [56, 63], [56, 64], [57, 64], [57, 65], [58, 61], [58, 65], [59, 61], [59, 62], [60, 62], [60, 63], [61, 67], [61, 70], [62, 66], [62, 68], [63, 67], [63, 69], [64, 68], [64, 70], [65, 66], [65, 69], [66, 73], [66, 74], [67, 74], [67, 75], [68, 71], [68, 75], [69, 71], [69, 72], [70, 72], [70, 73], [71, 77], [71, 80], [72, 76], [72, 78], [73, 77], [73, 79], [74, 78], [74, 80], [75, 76], [75, 79], [76, 83], [76, 84], [77, 84], [77, 85], [78, 81], [78, 85], [79, 81], [79, 82], [80, 82], [80, 83], [81, 87], [81, 90], [82, 86], [82, 88], [83, 87], [83, 89], [84, 88], [84, 90], [85, 86], [85, 89]]);;
R:=P177Census(D);;Need(Size(R.F)=360);;
PrintTo("current_c4_descent/090_005.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 090_005 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
