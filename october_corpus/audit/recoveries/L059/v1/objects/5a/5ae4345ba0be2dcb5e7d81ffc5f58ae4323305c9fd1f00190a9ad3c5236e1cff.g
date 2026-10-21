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
D:=P177Graph("096_055",96,[1, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96],[[1, 2], [1, 3], [1, 4], [1, 5], [2, 85], [2, 90], [2, 93], [3, 87], [3, 89], [3, 95], [4, 86], [4, 92], [4, 94], [5, 88], [5, 91], [5, 96], [6, 25], [6, 30], [6, 36], [6, 37], [7, 22], [7, 31], [7, 34], [7, 37], [8, 23], [8, 32], [8, 34], [8, 35], [9, 24], [9, 33], [9, 35], [9, 36], [10, 19], [10, 20], [10, 30], [10, 38], [11, 18], [11, 20], [11, 31], [11, 39], [12, 18], [12, 21], [12, 32], [12, 41], [13, 19], [13, 21], [13, 33], [13, 40], [14, 18], [14, 22], [14, 26], [14, 42], [15, 19], [15, 24], [15, 28], [15, 44], [16, 21], [16, 23], [16, 27], [16, 45], [17, 20], [17, 25], [17, 29], [17, 43], [18, 75], [19, 73], [20, 74], [21, 76], [22, 77], [22, 84], [23, 78], [23, 81], [24, 79], [24, 82], [25, 80], [25, 83], [26, 68], [26, 70], [26, 81], [27, 67], [27, 71], [27, 82], [28, 65], [28, 72], [28, 83], [29, 66], [29, 69], [29, 84], [30, 67], [30, 70], [31, 65], [31, 71], [32, 66], [32, 72], [33, 68], [33, 69], [34, 60], [34, 64], [35, 57], [35, 61], [36, 58], [36, 62], [37, 59], [37, 63], [38, 53], [38, 54], [38, 77], [39, 54], [39, 56], [39, 78], [40, 53], [40, 55], [40, 80], [41, 55], [41, 56], [41, 79], [42, 61], [42, 62], [42, 73], [43, 61], [43, 64], [43, 76], [44, 63], [44, 64], [44, 75], [45, 62], [45, 63], [45, 74], [46, 57], [46, 59], [46, 78], [46, 80], [47, 58], [47, 60], [47, 77], [47, 79], [48, 69], [48, 70], [48, 71], [48, 72], [49, 56], [49, 60], [49, 67], [49, 73], [50, 55], [50, 57], [50, 65], [50, 74], [51, 54], [51, 59], [51, 68], [51, 76], [52, 53], [52, 58], [52, 66], [52, 75], [53, 89], [54, 90], [55, 91], [56, 92], [57, 93], [58, 94], [59, 96], [60, 95], [61, 92], [62, 91], [63, 89], [64, 90], [65, 85], [66, 86], [67, 87], [68, 88], [69, 93], [70, 94], [71, 96], [72, 95], [73, 85], [74, 86], [75, 88], [76, 87], [77, 93], [78, 94], [79, 96], [80, 95], [81, 85], [81, 89], [82, 86], [82, 90], [83, 88], [83, 92], [84, 87], [84, 91]]);;
R:=P177Census(D);;Need(Size(R.F)=192);;
PrintTo("current_c4_descent/096_055.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_055 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
