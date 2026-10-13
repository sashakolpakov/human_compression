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
D:=P177Graph("096_054",96,[1, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96],[[1, 2], [1, 3], [1, 4], [1, 5], [2, 86], [2, 89], [2, 93], [3, 87], [3, 90], [3, 94], [4, 85], [4, 92], [4, 96], [5, 88], [5, 91], [5, 95], [6, 30], [6, 34], [6, 36], [6, 46], [7, 31], [7, 35], [7, 36], [7, 47], [8, 33], [8, 34], [8, 37], [8, 49], [9, 32], [9, 35], [9, 37], [9, 48], [10, 20], [10, 24], [10, 41], [10, 43], [11, 18], [11, 25], [11, 38], [11, 45], [12, 19], [12, 25], [12, 39], [12, 42], [13, 21], [13, 24], [13, 40], [13, 44], [14, 18], [14, 26], [14, 29], [14, 30], [15, 21], [15, 27], [15, 29], [15, 32], [16, 20], [16, 27], [16, 28], [16, 33], [17, 19], [17, 26], [17, 28], [17, 31], [18, 77], [18, 81], [19, 80], [19, 82], [20, 79], [20, 84], [21, 78], [21, 83], [22, 77], [22, 80], [22, 83], [22, 84], [23, 78], [23, 79], [23, 81], [23, 82], [24, 65], [24, 66], [25, 67], [25, 68], [26, 55], [26, 56], [27, 53], [27, 54], [28, 65], [28, 67], [29, 66], [29, 68], [30, 70], [30, 73], [31, 69], [31, 76], [32, 72], [32, 75], [33, 71], [33, 74], [34, 78], [34, 80], [35, 77], [35, 79], [36, 63], [36, 64], [37, 61], [37, 62], [38, 54], [38, 58], [38, 73], [39, 53], [39, 57], [39, 76], [40, 55], [40, 60], [40, 75], [41, 56], [41, 59], [41, 74], [42, 59], [42, 62], [42, 72], [43, 57], [43, 63], [43, 70], [44, 58], [44, 64], [44, 69], [45, 60], [45, 61], [45, 71], [46, 53], [46, 61], [46, 65], [47, 54], [47, 62], [47, 66], [48, 56], [48, 64], [48, 67], [49, 55], [49, 63], [49, 68], [50, 69], [50, 70], [50, 71], [50, 72], [51, 59], [51, 60], [51, 73], [51, 76], [52, 57], [52, 58], [52, 74], [52, 75], [53, 88], [54, 85], [55, 86], [56, 87], [57, 93], [58, 94], [59, 96], [60, 95], [61, 90], [62, 89], [63, 92], [64, 91], [65, 93], [66, 94], [67, 96], [68, 95], [69, 89], [70, 90], [71, 92], [72, 91], [73, 86], [74, 88], [75, 85], [76, 87], [77, 93], [78, 96], [79, 95], [80, 94], [81, 88], [81, 89], [82, 85], [82, 90], [83, 87], [83, 92], [84, 86], [84, 91]]);;
R:=P177Census(D);;Need(Size(R.F)=192);;
PrintTo("current_c4_descent/096_054.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_054 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
