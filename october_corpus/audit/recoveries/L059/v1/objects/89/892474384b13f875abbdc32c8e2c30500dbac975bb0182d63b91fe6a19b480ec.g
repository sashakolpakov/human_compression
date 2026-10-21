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
D:=P177Graph("080_028",80,[1, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80],[[1, 2], [1, 3], [1, 4], [1, 5], [2, 69], [2, 71], [2, 77], [3, 70], [3, 76], [3, 78], [4, 72], [4, 75], [4, 80], [5, 73], [5, 74], [5, 79], [6, 18], [6, 36], [6, 39], [6, 41], [7, 18], [7, 37], [7, 38], [7, 40], [8, 19], [8, 33], [8, 35], [8, 41], [9, 19], [9, 32], [9, 34], [9, 40], [10, 20], [10, 27], [10, 29], [10, 30], [11, 20], [11, 26], [11, 28], [11, 31], [12, 26], [12, 27], [12, 36], [12, 37], [13, 23], [13, 28], [13, 34], [13, 38], [14, 24], [14, 29], [14, 35], [14, 39], [15, 21], [15, 22], [15, 32], [15, 33], [16, 22], [16, 24], [16, 25], [16, 30], [17, 21], [17, 23], [17, 25], [17, 31], [18, 45], [18, 57], [19, 46], [19, 57], [20, 46], [20, 58], [21, 54], [21, 66], [22, 53], [22, 65], [23, 55], [23, 68], [24, 56], [24, 67], [25, 45], [25, 58], [26, 47], [26, 60], [27, 48], [27, 59], [28, 49], [28, 63], [29, 50], [29, 62], [30, 52], [30, 64], [31, 51], [31, 64], [32, 48], [32, 68], [33, 47], [33, 67], [34, 50], [34, 66], [35, 49], [35, 65], [36, 54], [36, 62], [37, 53], [37, 63], [38, 56], [38, 60], [39, 55], [39, 59], [40, 52], [40, 61], [41, 51], [41, 61], [42, 45], [42, 46], [42, 51], [42, 52], [43, 48], [43, 50], [43, 54], [43, 55], [44, 47], [44, 49], [44, 53], [44, 56], [45, 78], [46, 77], [47, 77], [48, 77], [49, 80], [50, 79], [51, 80], [52, 79], [53, 78], [54, 78], [55, 80], [56, 79], [57, 69], [57, 70], [58, 71], [58, 76], [59, 71], [59, 75], [60, 71], [60, 74], [61, 74], [61, 75], [62, 70], [62, 73], [63, 70], [63, 72], [64, 72], [64, 73], [65, 75], [65, 76], [66, 74], [66, 76], [67, 69], [67, 73], [68, 69], [68, 72]]);;
R:=P177Census(D);;Need(Size(R.F)=1920);;
PrintTo("current_c4_descent/080_028.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 080_028 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
