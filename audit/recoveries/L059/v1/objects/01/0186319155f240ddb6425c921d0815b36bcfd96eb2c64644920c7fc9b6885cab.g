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
D:=P177Graph("096_034",96,[1, 2, 3, 4, 8, 9, 12, 14, 15, 16, 17, 19, 20, 21, 25, 29, 30, 34, 36, 37, 40, 41, 45, 48, 49, 50, 51, 52, 59, 62, 64, 65, 67, 73, 74, 75, 76, 78, 79, 82, 83, 84, 86, 87, 90, 91, 93, 95],[[1, 27], [1, 42], [1, 47], [1, 71], [2, 43], [2, 57], [2, 58], [2, 60], [3, 11], [3, 24], [3, 88], [3, 89], [4, 6], [4, 47], [4, 58], [4, 61], [5, 16], [5, 45], [5, 76], [5, 87], [6, 73], [6, 82], [6, 90], [7, 14], [7, 25], [7, 50], [7, 90], [8, 31], [8, 68], [8, 88], [8, 89], [9, 56], [9, 63], [9, 68], [9, 85], [10, 37], [10, 59], [10, 67], [10, 84], [11, 20], [11, 45], [11, 91], [12, 33], [12, 38], [12, 94], [12, 96], [13, 21], [13, 48], [13, 65], [13, 93], [14, 44], [14, 60], [14, 81], [15, 43], [15, 53], [15, 60], [15, 94], [16, 44], [16, 80], [16, 85], [17, 53], [17, 57], [17, 58], [17, 94], [18, 30], [18, 37], [18, 49], [18, 64], [19, 23], [19, 28], [19, 72], [19, 77], [20, 70], [20, 80], [20, 85], [21, 24], [21, 26], [21, 54], [22, 37], [22, 67], [22, 74], [22, 76], [23, 74], [23, 76], [23, 86], [24, 40], [24, 91], [25, 32], [25, 46], [25, 53], [26, 36], [26, 65], [26, 84], [27, 49], [27, 67], [27, 78], [28, 59], [28, 84], [28, 86], [29, 47], [29, 58], [29, 66], [29, 92], [30, 31], [30, 38], [30, 96], [31, 64], [31, 91], [32, 36], [32, 50], [32, 59], [33, 40], [33, 64], [33, 65], [34, 39], [34, 69], [34, 72], [34, 92], [35, 36], [35, 59], [35, 79], [35, 83], [36, 42], [37, 63], [38, 52], [38, 93], [39, 51], [39, 74], [39, 87], [40, 46], [40, 54], [41, 54], [41, 70], [41, 72], [41, 77], [42, 75], [42, 84], [43, 76], [43, 87], [44, 45], [44, 82], [45, 70], [46, 65], [46, 95], [47, 78], [48, 61], [48, 71], [48, 88], [49, 57], [49, 63], [50, 66], [50, 77], [51, 55], [51, 69], [51, 80], [52, 61], [52, 69], [52, 88], [53, 95], [54, 86], [55, 62], [55, 75], [55, 78], [56, 75], [56, 78], [56, 79], [57, 67], [60, 82], [61, 73], [62, 72], [62, 80], [62, 92], [63, 83], [64, 94], [66, 73], [66, 95], [68, 83], [68, 91], [69, 93], [70, 86], [71, 75], [71, 93], [73, 92], [74, 96], [77, 95], [79, 81], [79, 85], [81, 83], [81, 90], [82, 89], [87, 96], [89, 90]]);;
R:=P177Census(D);;Need(Size(R.F)=192);;
PrintTo("current_c4_descent/096_034.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_034 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
