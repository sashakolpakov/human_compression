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
D:=P177Graph("096_056",96,[1, 6, 7, 12, 13, 14, 15, 16, 17, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96],[[1, 2], [1, 3], [1, 4], [1, 5], [2, 86], [2, 87], [2, 96], [3, 91], [3, 92], [3, 93], [4, 85], [4, 88], [4, 95], [5, 89], [5, 90], [5, 94], [6, 8], [6, 9], [6, 10], [6, 11], [7, 30], [7, 31], [7, 32], [7, 33], [8, 15], [8, 44], [8, 47], [9, 14], [9, 45], [9, 46], [10, 13], [10, 50], [10, 51], [11, 12], [11, 48], [11, 49], [12, 18], [12, 19], [12, 33], [13, 20], [13, 21], [13, 30], [14, 24], [14, 25], [14, 31], [15, 22], [15, 23], [15, 32], [16, 18], [16, 20], [16, 22], [16, 25], [17, 19], [17, 21], [17, 23], [17, 24], [18, 36], [18, 44], [19, 43], [19, 45], [20, 38], [20, 46], [21, 37], [21, 47], [22, 41], [22, 50], [23, 40], [23, 49], [24, 42], [24, 51], [25, 39], [25, 48], [26, 36], [26, 43], [26, 52], [26, 57], [27, 37], [27, 38], [27, 53], [27, 54], [28, 39], [28, 42], [28, 56], [28, 59], [29, 40], [29, 41], [29, 55], [29, 58], [30, 39], [30, 40], [31, 36], [31, 37], [32, 38], [32, 43], [33, 41], [33, 42], [34, 77], [34, 80], [34, 83], [34, 84], [35, 78], [35, 79], [35, 81], [35, 82], [36, 67], [37, 66], [38, 65], [39, 71], [40, 72], [41, 69], [42, 70], [43, 68], [44, 65], [44, 73], [45, 66], [45, 73], [46, 67], [46, 74], [47, 68], [47, 74], [48, 69], [48, 75], [49, 70], [49, 76], [50, 71], [50, 76], [51, 72], [51, 75], [52, 64], [52, 66], [52, 80], [53, 63], [53, 68], [53, 77], [54, 64], [54, 67], [54, 78], [55, 62], [55, 70], [55, 84], [56, 62], [56, 69], [56, 81], [57, 63], [57, 65], [57, 79], [58, 61], [58, 71], [58, 82], [59, 61], [59, 72], [59, 83], [60, 61], [60, 62], [60, 63], [60, 64], [61, 93], [62, 94], [63, 95], [64, 96], [65, 88], [66, 87], [67, 86], [68, 85], [69, 89], [70, 90], [71, 92], [72, 91], [73, 85], [73, 86], [74, 87], [74, 88], [75, 90], [75, 92], [76, 89], [76, 91], [77, 87], [77, 93], [78, 88], [78, 93], [79, 86], [79, 94], [80, 85], [80, 94], [81, 92], [81, 96], [82, 89], [82, 95], [83, 90], [83, 96], [84, 91], [84, 95]]);;
R:=P177Census(D);;Need(Size(R.F)=384);;
PrintTo("current_c4_descent/096_056.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_056 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
