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
D:=P177Graph("090_010",90,[1, 3, 5, 6, 10, 13, 14, 17, 19, 20, 21, 24, 25, 27, 31, 33, 34, 38, 41, 42, 43, 44, 45, 48, 50, 52, 55, 56, 58, 59, 60, 61, 62, 63, 65, 67, 69, 70, 73, 74, 75, 78, 79, 83, 85],[[1, 36], [1, 37], [1, 46], [1, 54], [2, 61], [2, 63], [2, 69], [2, 73], [3, 28], [3, 36], [3, 47], [3, 57], [4, 56], [4, 58], [4, 69], [4, 73], [5, 15], [5, 47], [5, 57], [5, 90], [6, 39], [6, 40], [6, 84], [6, 87], [7, 42], [7, 48], [7, 69], [7, 70], [8, 56], [8, 58], [8, 61], [8, 63], [9, 33], [9, 48], [9, 78], [9, 79], [10, 68], [10, 76], [10, 84], [10, 87], [11, 17], [11, 20], [11, 69], [11, 70], [12, 33], [12, 48], [12, 62], [12, 65], [13, 15], [13, 72], [13, 80], [13, 86], [14, 15], [14, 28], [14, 36], [14, 90], [15, 24], [16, 33], [16, 42], [16, 50], [16, 55], [17, 36], [17, 37], [17, 89], [18, 19], [18, 24], [18, 33], [18, 42], [19, 72], [19, 80], [19, 88], [20, 46], [20, 54], [20, 89], [21, 39], [21, 40], [21, 68], [21, 76], [22, 62], [22, 65], [22, 78], [22, 79], [23, 27], [23, 34], [23, 43], [23, 45], [24, 86], [24, 88], [25, 32], [25, 35], [25, 46], [25, 49], [26, 34], [26, 43], [26, 62], [26, 67], [27, 30], [27, 32], [27, 49], [28, 41], [28, 44], [29, 74], [29, 75], [29, 78], [29, 85], [30, 45], [30, 62], [30, 67], [31, 76], [31, 77], [31, 86], [31, 90], [32, 50], [32, 52], [34, 76], [34, 77], [35, 45], [35, 83], [35, 85], [37, 41], [37, 44], [38, 64], [38, 71], [38, 81], [38, 84], [39, 74], [39, 85], [40, 75], [40, 78], [41, 64], [41, 71], [42, 89], [43, 86], [43, 90], [44, 81], [44, 84], [45, 46], [47, 75], [47, 79], [48, 89], [49, 58], [49, 59], [50, 51], [50, 88], [51, 52], [51, 58], [51, 59], [52, 81], [52, 87], [53, 56], [53, 59], [53, 75], [53, 79], [54, 83], [54, 85], [55, 81], [55, 87], [55, 88], [56, 57], [57, 59], [60, 66], [60, 71], [60, 80], [60, 82], [61, 80], [61, 82], [63, 66], [63, 71], [64, 65], [64, 67], [65, 66], [66, 67], [68, 70], [68, 73], [70, 77], [72, 74], [72, 83], [73, 77], [74, 82], [82, 83]]);;
R:=P177Census(D);;Need(Size(R.F)=1440);;
PrintTo("current_c4_descent/090_010.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 090_010 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
