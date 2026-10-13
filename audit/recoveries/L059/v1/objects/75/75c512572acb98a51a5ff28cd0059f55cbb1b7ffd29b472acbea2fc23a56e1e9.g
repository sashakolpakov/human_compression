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
D:=P177Graph("104_003",104,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103],[[1, 2], [1, 28], [1, 78], [1, 104], [2, 3], [2, 29], [2, 79], [3, 4], [3, 30], [3, 80], [4, 5], [4, 31], [4, 81], [5, 6], [5, 32], [5, 82], [6, 7], [6, 33], [6, 83], [7, 8], [7, 34], [7, 84], [8, 9], [8, 35], [8, 85], [9, 10], [9, 36], [9, 86], [10, 11], [10, 37], [10, 87], [11, 12], [11, 38], [11, 88], [12, 13], [12, 39], [12, 89], [13, 14], [13, 40], [13, 90], [14, 15], [14, 41], [14, 91], [15, 16], [15, 42], [15, 92], [16, 17], [16, 43], [16, 93], [17, 18], [17, 44], [17, 94], [18, 19], [18, 45], [18, 95], [19, 20], [19, 46], [19, 96], [20, 21], [20, 47], [20, 97], [21, 22], [21, 48], [21, 98], [22, 23], [22, 49], [22, 99], [23, 24], [23, 50], [23, 100], [24, 25], [24, 51], [24, 101], [25, 26], [25, 52], [25, 102], [26, 27], [26, 53], [26, 103], [27, 28], [27, 54], [27, 104], [28, 29], [28, 55], [29, 30], [29, 56], [30, 31], [30, 57], [31, 32], [31, 58], [32, 33], [32, 59], [33, 34], [33, 60], [34, 35], [34, 61], [35, 36], [35, 62], [36, 37], [36, 63], [37, 38], [37, 64], [38, 39], [38, 65], [39, 40], [39, 66], [40, 41], [40, 67], [41, 42], [41, 68], [42, 43], [42, 69], [43, 44], [43, 70], [44, 45], [44, 71], [45, 46], [45, 72], [46, 47], [46, 73], [47, 48], [47, 74], [48, 49], [48, 75], [49, 50], [49, 76], [50, 51], [50, 77], [51, 52], [51, 78], [52, 53], [52, 79], [53, 54], [53, 80], [54, 55], [54, 81], [55, 56], [55, 82], [56, 57], [56, 83], [57, 58], [57, 84], [58, 59], [58, 85], [59, 60], [59, 86], [60, 61], [60, 87], [61, 62], [61, 88], [62, 63], [62, 89], [63, 64], [63, 90], [64, 65], [64, 91], [65, 66], [65, 92], [66, 67], [66, 93], [67, 68], [67, 94], [68, 69], [68, 95], [69, 70], [69, 96], [70, 71], [70, 97], [71, 72], [71, 98], [72, 73], [72, 99], [73, 74], [73, 100], [74, 75], [74, 101], [75, 76], [75, 102], [76, 77], [76, 103], [77, 78], [77, 104], [78, 79], [79, 80], [80, 81], [81, 82], [82, 83], [83, 84], [84, 85], [85, 86], [86, 87], [87, 88], [88, 89], [89, 90], [90, 91], [91, 92], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104]]);;
R:=P177Census(D);;Need(Size(R.F)=416);;
PrintTo("current_c4_descent/104_003.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 104_003 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
