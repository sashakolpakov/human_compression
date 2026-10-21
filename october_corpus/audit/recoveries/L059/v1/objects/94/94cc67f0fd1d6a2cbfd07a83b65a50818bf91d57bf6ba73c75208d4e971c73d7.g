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
D:=P177Graph("084_012",84,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70],[[1, 15], [1, 44], [1, 55], [1, 71], [2, 16], [2, 45], [2, 56], [2, 72], [3, 17], [3, 43], [3, 46], [3, 73], [4, 18], [4, 44], [4, 47], [4, 74], [5, 19], [5, 45], [5, 48], [5, 75], [6, 20], [6, 46], [6, 49], [6, 76], [7, 21], [7, 47], [7, 50], [7, 77], [8, 22], [8, 48], [8, 51], [8, 78], [9, 23], [9, 49], [9, 52], [9, 79], [10, 24], [10, 50], [10, 53], [10, 80], [11, 25], [11, 51], [11, 54], [11, 81], [12, 26], [12, 52], [12, 55], [12, 82], [13, 27], [13, 53], [13, 56], [13, 83], [14, 28], [14, 43], [14, 54], [14, 84], [15, 29], [15, 60], [15, 65], [16, 30], [16, 61], [16, 66], [17, 31], [17, 62], [17, 67], [18, 32], [18, 63], [18, 68], [19, 33], [19, 64], [19, 69], [20, 34], [20, 65], [20, 70], [21, 35], [21, 57], [21, 66], [22, 36], [22, 58], [22, 67], [23, 37], [23, 59], [23, 68], [24, 38], [24, 60], [24, 69], [25, 39], [25, 61], [25, 70], [26, 40], [26, 57], [26, 62], [27, 41], [27, 58], [27, 63], [28, 42], [28, 59], [28, 64], [29, 43], [29, 80], [29, 81], [30, 44], [30, 81], [30, 82], [31, 45], [31, 82], [31, 83], [32, 46], [32, 83], [32, 84], [33, 47], [33, 71], [33, 84], [34, 48], [34, 71], [34, 72], [35, 49], [35, 72], [35, 73], [36, 50], [36, 73], [36, 74], [37, 51], [37, 74], [37, 75], [38, 52], [38, 75], [38, 76], [39, 53], [39, 76], [39, 77], [40, 54], [40, 77], [40, 78], [41, 55], [41, 78], [41, 79], [42, 56], [42, 79], [42, 80], [43, 57], [44, 58], [45, 59], [46, 60], [47, 61], [48, 62], [49, 63], [50, 64], [51, 65], [52, 66], [53, 67], [54, 68], [55, 69], [56, 70], [57, 71], [58, 72], [59, 73], [60, 74], [61, 75], [62, 76], [63, 77], [64, 78], [65, 79], [66, 80], [67, 81], [68, 82], [69, 83], [70, 84]]);;
R:=P177Census(D);;Need(Size(R.F)=2016);;
PrintTo("current_c4_descent/084_012.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 084_012 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
