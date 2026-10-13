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
D:=P177Graph("080_004",80,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80],[[1, 2], [1, 20], [1, 21], [1, 69], [2, 3], [2, 22], [2, 70], [3, 4], [3, 23], [3, 71], [4, 5], [4, 24], [4, 72], [5, 6], [5, 25], [5, 73], [6, 7], [6, 26], [6, 74], [7, 8], [7, 27], [7, 75], [8, 9], [8, 28], [8, 76], [9, 10], [9, 29], [9, 77], [10, 11], [10, 30], [10, 78], [11, 12], [11, 31], [11, 79], [12, 13], [12, 32], [12, 80], [13, 14], [13, 33], [13, 61], [14, 15], [14, 34], [14, 62], [15, 16], [15, 35], [15, 63], [16, 17], [16, 36], [16, 64], [17, 18], [17, 37], [17, 65], [18, 19], [18, 38], [18, 66], [19, 20], [19, 39], [19, 67], [20, 40], [20, 68], [21, 22], [21, 40], [21, 41], [22, 23], [22, 42], [23, 24], [23, 43], [24, 25], [24, 44], [25, 26], [25, 45], [26, 27], [26, 46], [27, 28], [27, 47], [28, 29], [28, 48], [29, 30], [29, 49], [30, 31], [30, 50], [31, 32], [31, 51], [32, 33], [32, 52], [33, 34], [33, 53], [34, 35], [34, 54], [35, 36], [35, 55], [36, 37], [36, 56], [37, 38], [37, 57], [38, 39], [38, 58], [39, 40], [39, 59], [40, 60], [41, 42], [41, 60], [41, 61], [42, 43], [42, 62], [43, 44], [43, 63], [44, 45], [44, 64], [45, 46], [45, 65], [46, 47], [46, 66], [47, 48], [47, 67], [48, 49], [48, 68], [49, 50], [49, 69], [50, 51], [50, 70], [51, 52], [51, 71], [52, 53], [52, 72], [53, 54], [53, 73], [54, 55], [54, 74], [55, 56], [55, 75], [56, 57], [56, 76], [57, 58], [57, 77], [58, 59], [58, 78], [59, 60], [59, 79], [60, 80], [61, 62], [61, 80], [62, 63], [63, 64], [64, 65], [65, 66], [66, 67], [67, 68], [68, 69], [69, 70], [70, 71], [71, 72], [72, 73], [73, 74], [74, 75], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80]]);;
R:=P177Census(D);;Need(Size(R.F)=320);;
PrintTo("current_c4_descent/080_004.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 080_004 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
