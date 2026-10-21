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
D:=P177Graph("090_003",90,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89],[[1, 32], [1, 60], [1, 62], [1, 90], [2, 31], [2, 33], [2, 61], [2, 63], [3, 32], [3, 34], [3, 62], [3, 64], [4, 33], [4, 35], [4, 63], [4, 65], [5, 34], [5, 36], [5, 64], [5, 66], [6, 35], [6, 37], [6, 65], [6, 67], [7, 36], [7, 38], [7, 66], [7, 68], [8, 37], [8, 39], [8, 67], [8, 69], [9, 38], [9, 40], [9, 68], [9, 70], [10, 39], [10, 41], [10, 69], [10, 71], [11, 40], [11, 42], [11, 70], [11, 72], [12, 41], [12, 43], [12, 71], [12, 73], [13, 42], [13, 44], [13, 72], [13, 74], [14, 43], [14, 45], [14, 73], [14, 75], [15, 44], [15, 46], [15, 74], [15, 76], [16, 45], [16, 47], [16, 75], [16, 77], [17, 46], [17, 48], [17, 76], [17, 78], [18, 47], [18, 49], [18, 77], [18, 79], [19, 48], [19, 50], [19, 78], [19, 80], [20, 49], [20, 51], [20, 79], [20, 81], [21, 50], [21, 52], [21, 80], [21, 82], [22, 51], [22, 53], [22, 81], [22, 83], [23, 52], [23, 54], [23, 82], [23, 84], [24, 53], [24, 55], [24, 83], [24, 85], [25, 54], [25, 56], [25, 84], [25, 86], [26, 55], [26, 57], [26, 85], [26, 87], [27, 56], [27, 58], [27, 86], [27, 88], [28, 57], [28, 59], [28, 87], [28, 89], [29, 58], [29, 60], [29, 88], [29, 90], [30, 31], [30, 59], [30, 61], [30, 89], [31, 62], [31, 90], [32, 61], [32, 63], [33, 62], [33, 64], [34, 63], [34, 65], [35, 64], [35, 66], [36, 65], [36, 67], [37, 66], [37, 68], [38, 67], [38, 69], [39, 68], [39, 70], [40, 69], [40, 71], [41, 70], [41, 72], [42, 71], [42, 73], [43, 72], [43, 74], [44, 73], [44, 75], [45, 74], [45, 76], [46, 75], [46, 77], [47, 76], [47, 78], [48, 77], [48, 79], [49, 78], [49, 80], [50, 79], [50, 81], [51, 80], [51, 82], [52, 81], [52, 83], [53, 82], [53, 84], [54, 83], [54, 85], [55, 84], [55, 86], [56, 85], [56, 87], [57, 86], [57, 88], [58, 87], [58, 89], [59, 88], [59, 90], [60, 61], [60, 89]]);;
R:=P177Census(D);;Need(Size(R.F)=360);;
PrintTo("current_c4_descent/090_003.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 090_003 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
