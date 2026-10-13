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
D:=P177Graph("096_039",96,[1, 3, 4, 6, 9, 11, 13, 14, 16, 18, 19, 21, 23, 27, 31, 34, 36, 37, 39, 42, 44, 46, 47, 49, 50, 52, 53, 55, 56, 57, 60, 62, 64, 65, 66, 68, 72, 73, 75, 80, 85, 86, 87, 89, 90, 91, 95, 96],[[1, 2], [1, 5], [1, 63], [1, 83], [2, 6], [2, 14], [2, 50], [3, 7], [3, 15], [3, 30], [3, 51], [4, 8], [4, 12], [4, 58], [4, 88], [5, 16], [5, 21], [5, 34], [6, 17], [6, 35], [6, 78], [7, 18], [7, 36], [7, 53], [8, 19], [8, 37], [8, 65], [9, 20], [9, 38], [9, 48], [9, 76], [10, 21], [10, 39], [10, 62], [10, 64], [11, 22], [11, 40], [11, 41], [11, 81], [12, 23], [12, 31], [12, 53], [13, 24], [13, 25], [13, 32], [13, 92], [14, 41], [14, 51], [14, 67], [15, 42], [15, 52], [15, 68], [16, 43], [16, 59], [16, 69], [17, 44], [17, 46], [17, 86], [18, 33], [18, 43], [18, 54], [19, 45], [19, 61], [19, 70], [20, 27], [20, 46], [20, 65], [21, 22], [21, 79], [22, 47], [22, 66], [23, 48], [23, 71], [23, 92], [24, 44], [24, 49], [24, 72], [25, 34], [25, 73], [25, 80], [26, 42], [26, 47], [26, 50], [26, 87], [27, 51], [27, 63], [27, 74], [28, 31], [28, 47], [28, 52], [28, 91], [29, 46], [29, 49], [29, 53], [29, 85], [30, 37], [30, 60], [30, 75], [31, 54], [31, 79], [32, 50], [32, 55], [32, 64], [33, 56], [33, 57], [33, 65], [34, 67], [34, 76], [35, 64], [35, 75], [35, 85], [36, 76], [36, 83], [36, 93], [37, 71], [37, 81], [38, 39], [38, 52], [38, 73], [39, 59], [39, 77], [40, 44], [40, 56], [40, 60], [41, 68], [41, 89], [42, 77], [42, 78], [43, 44], [43, 95], [45, 52], [45, 64], [45, 96], [46, 70], [47, 69], [48, 72], [48, 90], [49, 79], [49, 82], [50, 61], [51, 91], [53, 59], [54, 80], [54, 87], [55, 81], [55, 88], [55, 94], [56, 61], [56, 82], [57, 67], [57, 69], [57, 88], [58, 66], [58, 68], [58, 85], [59, 75], [60, 83], [60, 84], [61, 80], [62, 70], [62, 71], [62, 83], [63, 72], [63, 87], [65, 78], [66, 84], [66, 92], [67, 85], [68, 93], [69, 90], [70, 89], [71, 87], [72, 94], [73, 74], [73, 88], [74, 89], [74, 95], [75, 94], [76, 96], [77, 86], [77, 95], [78, 90], [79, 89], [80, 93], [81, 95], [82, 91], [82, 96], [84, 90], [84, 96], [86, 92], [86, 93], [91, 94]]);;
R:=P177Census(D);;Need(Size(R.F)=384);;
PrintTo("current_c4_descent/096_039.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_039 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
