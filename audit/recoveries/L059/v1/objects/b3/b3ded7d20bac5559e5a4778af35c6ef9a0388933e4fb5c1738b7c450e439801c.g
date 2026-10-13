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
D:=P177Graph("080_002",80,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79],[[1, 2], [1, 10], [1, 72], [1, 80], [2, 3], [2, 11], [2, 73], [3, 4], [3, 12], [3, 74], [4, 5], [4, 13], [4, 75], [5, 6], [5, 14], [5, 76], [6, 7], [6, 15], [6, 77], [7, 8], [7, 16], [7, 78], [8, 9], [8, 17], [8, 79], [9, 10], [9, 18], [9, 80], [10, 11], [10, 19], [11, 12], [11, 20], [12, 13], [12, 21], [13, 14], [13, 22], [14, 15], [14, 23], [15, 16], [15, 24], [16, 17], [16, 25], [17, 18], [17, 26], [18, 19], [18, 27], [19, 20], [19, 28], [20, 21], [20, 29], [21, 22], [21, 30], [22, 23], [22, 31], [23, 24], [23, 32], [24, 25], [24, 33], [25, 26], [25, 34], [26, 27], [26, 35], [27, 28], [27, 36], [28, 29], [28, 37], [29, 30], [29, 38], [30, 31], [30, 39], [31, 32], [31, 40], [32, 33], [32, 41], [33, 34], [33, 42], [34, 35], [34, 43], [35, 36], [35, 44], [36, 37], [36, 45], [37, 38], [37, 46], [38, 39], [38, 47], [39, 40], [39, 48], [40, 41], [40, 49], [41, 42], [41, 50], [42, 43], [42, 51], [43, 44], [43, 52], [44, 45], [44, 53], [45, 46], [45, 54], [46, 47], [46, 55], [47, 48], [47, 56], [48, 49], [48, 57], [49, 50], [49, 58], [50, 51], [50, 59], [51, 52], [51, 60], [52, 53], [52, 61], [53, 54], [53, 62], [54, 55], [54, 63], [55, 56], [55, 64], [56, 57], [56, 65], [57, 58], [57, 66], [58, 59], [58, 67], [59, 60], [59, 68], [60, 61], [60, 69], [61, 62], [61, 70], [62, 63], [62, 71], [63, 64], [63, 72], [64, 65], [64, 73], [65, 66], [65, 74], [66, 67], [66, 75], [67, 68], [67, 76], [68, 69], [68, 77], [69, 70], [69, 78], [70, 71], [70, 79], [71, 72], [71, 80], [72, 73], [73, 74], [74, 75], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80]]);;
R:=P177Census(D);;Need(Size(R.F)=320);;
PrintTo("current_c4_descent/080_002.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 080_002 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
