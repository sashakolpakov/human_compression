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
D:=P177Graph("080_009",80,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70],[[1, 11], [1, 20], [1, 72], [1, 79], [2, 11], [2, 12], [2, 73], [2, 80], [3, 12], [3, 13], [3, 71], [3, 74], [4, 13], [4, 14], [4, 72], [4, 75], [5, 14], [5, 15], [5, 73], [5, 76], [6, 15], [6, 16], [6, 74], [6, 77], [7, 16], [7, 17], [7, 75], [7, 78], [8, 17], [8, 18], [8, 76], [8, 79], [9, 18], [9, 19], [9, 77], [9, 80], [10, 19], [10, 20], [10, 71], [10, 78], [11, 23], [11, 30], [12, 21], [12, 24], [13, 22], [13, 25], [14, 23], [14, 26], [15, 24], [15, 27], [16, 25], [16, 28], [17, 26], [17, 29], [18, 27], [18, 30], [19, 21], [19, 28], [20, 22], [20, 29], [21, 35], [21, 36], [22, 36], [22, 37], [23, 37], [23, 38], [24, 38], [24, 39], [25, 39], [25, 40], [26, 31], [26, 40], [27, 31], [27, 32], [28, 32], [28, 33], [29, 33], [29, 34], [30, 34], [30, 35], [31, 45], [31, 48], [32, 46], [32, 49], [33, 47], [33, 50], [34, 41], [34, 48], [35, 42], [35, 49], [36, 43], [36, 50], [37, 41], [37, 44], [38, 42], [38, 45], [39, 43], [39, 46], [40, 44], [40, 47], [41, 51], [41, 60], [42, 51], [42, 52], [43, 52], [43, 53], [44, 53], [44, 54], [45, 54], [45, 55], [46, 55], [46, 56], [47, 56], [47, 57], [48, 57], [48, 58], [49, 58], [49, 59], [50, 59], [50, 60], [51, 63], [51, 70], [52, 61], [52, 64], [53, 62], [53, 65], [54, 63], [54, 66], [55, 64], [55, 67], [56, 65], [56, 68], [57, 66], [57, 69], [58, 67], [58, 70], [59, 61], [59, 68], [60, 62], [60, 69], [61, 75], [61, 76], [62, 76], [62, 77], [63, 77], [63, 78], [64, 78], [64, 79], [65, 79], [65, 80], [66, 71], [66, 80], [67, 71], [67, 72], [68, 72], [68, 73], [69, 73], [69, 74], [70, 74], [70, 75]]);;
R:=P177Census(D);;Need(Size(R.F)=320);;
PrintTo("current_c4_descent/080_009.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 080_009 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
