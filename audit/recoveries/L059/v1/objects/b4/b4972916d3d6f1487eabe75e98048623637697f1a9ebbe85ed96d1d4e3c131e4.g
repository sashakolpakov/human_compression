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
D:=P177Graph("080_005",80,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80],[[1, 2], [1, 40], [1, 41], [1, 63], [2, 3], [2, 42], [2, 64], [3, 4], [3, 43], [3, 65], [4, 5], [4, 44], [4, 66], [5, 6], [5, 45], [5, 67], [6, 7], [6, 46], [6, 68], [7, 8], [7, 47], [7, 69], [8, 9], [8, 48], [8, 70], [9, 10], [9, 49], [9, 71], [10, 11], [10, 50], [10, 72], [11, 12], [11, 51], [11, 73], [12, 13], [12, 52], [12, 74], [13, 14], [13, 53], [13, 75], [14, 15], [14, 54], [14, 76], [15, 16], [15, 55], [15, 77], [16, 17], [16, 56], [16, 78], [17, 18], [17, 57], [17, 79], [18, 19], [18, 58], [18, 80], [19, 20], [19, 41], [19, 59], [20, 21], [20, 42], [20, 60], [21, 22], [21, 43], [21, 61], [22, 23], [22, 44], [22, 62], [23, 24], [23, 45], [23, 63], [24, 25], [24, 46], [24, 64], [25, 26], [25, 47], [25, 65], [26, 27], [26, 48], [26, 66], [27, 28], [27, 49], [27, 67], [28, 29], [28, 50], [28, 68], [29, 30], [29, 51], [29, 69], [30, 31], [30, 52], [30, 70], [31, 32], [31, 53], [31, 71], [32, 33], [32, 54], [32, 72], [33, 34], [33, 55], [33, 73], [34, 35], [34, 56], [34, 74], [35, 36], [35, 57], [35, 75], [36, 37], [36, 58], [36, 76], [37, 38], [37, 59], [37, 77], [38, 39], [38, 60], [38, 78], [39, 40], [39, 61], [39, 79], [40, 62], [40, 80], [41, 42], [41, 80], [42, 43], [43, 44], [44, 45], [45, 46], [46, 47], [47, 48], [48, 49], [49, 50], [50, 51], [51, 52], [52, 53], [53, 54], [54, 55], [55, 56], [56, 57], [57, 58], [58, 59], [59, 60], [60, 61], [61, 62], [62, 63], [63, 64], [64, 65], [65, 66], [66, 67], [67, 68], [68, 69], [69, 70], [70, 71], [71, 72], [72, 73], [73, 74], [74, 75], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80]]);;
R:=P177Census(D);;Need(Size(R.F)=320);;
PrintTo("current_c4_descent/080_005.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 080_005 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
