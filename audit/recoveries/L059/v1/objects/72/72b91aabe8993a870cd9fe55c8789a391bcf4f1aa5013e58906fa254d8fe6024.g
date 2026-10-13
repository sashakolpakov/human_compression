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
D:=P177Graph("108_021",108,[1, 2, 3, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 28, 29, 30, 34, 35, 36, 40, 41, 42, 49, 50, 51, 67, 68, 69, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 97, 98, 99, 100, 101, 102],[[1, 4], [1, 7], [1, 9], [1, 10], [2, 10], [2, 43], [2, 45], [2, 70], [3, 4], [3, 52], [3, 54], [3, 70], [4, 13], [4, 19], [5, 19], [5, 22], [5, 24], [5, 76], [6, 13], [6, 76], [6, 82], [6, 84], [7, 16], [7, 18], [7, 22], [8, 22], [8, 40], [8, 73], [8, 75], [9, 28], [9, 30], [9, 40], [10, 14], [10, 34], [11, 34], [11, 40], [11, 42], [11, 97], [12, 14], [12, 97], [12, 100], [12, 102], [13, 25], [13, 37], [14, 37], [14, 46], [15, 25], [15, 46], [15, 56], [15, 57], [16, 31], [16, 33], [16, 43], [17, 43], [17, 48], [17, 94], [17, 96], [18, 48], [18, 55], [18, 57], [19, 26], [19, 61], [20, 61], [20, 70], [20, 72], [20, 104], [21, 26], [21, 104], [21, 106], [21, 107], [22, 64], [23, 47], [23, 48], [23, 64], [23, 107], [24, 91], [24, 93], [24, 107], [25, 49], [25, 67], [26, 41], [26, 67], [27, 29], [27, 30], [27, 41], [27, 49], [28, 54], [28, 58], [28, 60], [29, 54], [29, 106], [29, 108], [30, 55], [30, 56], [31, 49], [31, 51], [31, 73], [32, 67], [32, 69], [32, 73], [32, 78], [33, 78], [33, 83], [33, 84], [34, 47], [34, 91], [35, 70], [35, 71], [35, 91], [35, 103], [36, 47], [36, 94], [36, 95], [36, 103], [37, 50], [37, 80], [38, 76], [38, 77], [38, 80], [38, 89], [39, 50], [39, 89], [39, 97], [39, 98], [40, 65], [41, 65], [41, 95], [42, 61], [42, 63], [42, 95], [43, 81], [44, 77], [44, 78], [44, 81], [44, 102], [45, 85], [45, 86], [45, 102], [46, 68], [46, 79], [47, 68], [48, 79], [49, 94], [50, 71], [50, 94], [51, 53], [51, 54], [51, 71], [52, 84], [52, 85], [52, 87], [53, 84], [53, 98], [53, 99], [55, 88], [55, 90], [56, 100], [56, 101], [57, 82], [57, 83], [58, 75], [58, 79], [58, 81], [59, 68], [59, 69], [59, 75], [59, 99], [60, 99], [60, 101], [60, 102], [61, 100], [62, 76], [62, 78], [62, 88], [62, 100], [63, 73], [63, 74], [63, 88], [64, 77], [64, 85], [65, 85], [65, 98], [66, 67], [66, 68], [66, 77], [66, 98], [69, 103], [69, 104], [71, 74], [72, 74], [72, 80], [72, 81], [74, 93], [75, 93], [79, 106], [80, 106], [82, 91], [82, 92], [83, 103], [83, 105], [86, 95], [86, 96], [86, 105], [87, 105], [87, 107], [87, 108], [88, 96], [89, 96], [89, 108], [90, 92], [90, 93], [90, 108], [92, 97], [92, 99], [101, 104], [101, 105]]);;
R:=P177Census(D);;Need(Size(R.F)=432);;
PrintTo("current_c4_descent/108_021.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 108_021 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
