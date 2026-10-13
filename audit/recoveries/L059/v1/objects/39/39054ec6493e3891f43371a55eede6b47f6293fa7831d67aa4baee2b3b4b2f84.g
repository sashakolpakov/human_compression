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
D:=P177Graph("110_006",110,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109],[[1, 2], [1, 26], [1, 60], [1, 86], [2, 3], [2, 17], [2, 97], [3, 4], [3, 38], [3, 78], [4, 5], [4, 49], [4, 69], [5, 10], [5, 56], [5, 110], [6, 7], [6, 31], [6, 65], [6, 91], [7, 8], [7, 22], [7, 102], [8, 9], [8, 43], [8, 83], [9, 10], [9, 54], [9, 74], [10, 15], [10, 61], [11, 12], [11, 36], [11, 70], [11, 96], [12, 13], [12, 27], [12, 107], [13, 14], [13, 48], [13, 88], [14, 15], [14, 59], [14, 79], [15, 20], [15, 66], [16, 17], [16, 41], [16, 75], [16, 101], [17, 18], [17, 32], [18, 19], [18, 53], [18, 93], [19, 20], [19, 64], [19, 84], [20, 25], [20, 71], [21, 22], [21, 46], [21, 80], [21, 106], [22, 23], [22, 37], [23, 24], [23, 58], [23, 98], [24, 25], [24, 69], [24, 89], [25, 30], [25, 76], [26, 27], [26, 51], [26, 85], [27, 28], [27, 42], [28, 29], [28, 63], [28, 103], [29, 30], [29, 74], [29, 94], [30, 35], [30, 81], [31, 32], [31, 56], [31, 90], [32, 33], [32, 47], [33, 34], [33, 68], [33, 108], [34, 35], [34, 79], [34, 99], [35, 40], [35, 86], [36, 37], [36, 61], [36, 95], [37, 38], [37, 52], [38, 39], [38, 73], [39, 40], [39, 84], [39, 104], [40, 45], [40, 91], [41, 42], [41, 66], [41, 100], [42, 43], [42, 57], [43, 44], [43, 78], [44, 45], [44, 89], [44, 109], [45, 50], [45, 96], [46, 47], [46, 71], [46, 105], [47, 48], [47, 62], [48, 49], [48, 83], [49, 50], [49, 94], [50, 55], [50, 101], [51, 52], [51, 76], [51, 110], [52, 53], [52, 67], [53, 54], [53, 88], [54, 55], [54, 99], [55, 60], [55, 106], [56, 57], [56, 81], [57, 58], [57, 72], [58, 59], [58, 93], [59, 60], [59, 104], [60, 65], [61, 62], [61, 86], [62, 63], [62, 77], [63, 64], [63, 98], [64, 65], [64, 109], [65, 70], [66, 67], [66, 91], [67, 68], [67, 82], [68, 69], [68, 103], [69, 70], [70, 75], [71, 72], [71, 96], [72, 73], [72, 87], [73, 74], [73, 108], [74, 75], [75, 80], [76, 77], [76, 101], [77, 78], [77, 92], [78, 79], [79, 80], [80, 85], [81, 82], [81, 106], [82, 83], [82, 97], [83, 84], [84, 85], [85, 90], [86, 87], [87, 88], [87, 102], [88, 89], [89, 90], [90, 95], [91, 92], [92, 93], [92, 107], [93, 94], [94, 95], [95, 100], [96, 97], [97, 98], [98, 99], [99, 100], [100, 105], [101, 102], [102, 103], [103, 104], [104, 105], [105, 110], [106, 107], [107, 108], [108, 109], [109, 110]]);;
R:=P177Census(D);;Need(Size(R.F)=2640);;
PrintTo("current_c4_descent/110_006.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 110_006 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
