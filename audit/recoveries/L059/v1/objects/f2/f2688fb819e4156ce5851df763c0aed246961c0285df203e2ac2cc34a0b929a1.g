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
D:=P177Graph("104_004",104,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104],[[1, 2], [1, 52], [1, 53], [1, 63], [2, 3], [2, 54], [2, 64], [3, 4], [3, 55], [3, 65], [4, 5], [4, 56], [4, 66], [5, 6], [5, 57], [5, 67], [6, 7], [6, 58], [6, 68], [7, 8], [7, 59], [7, 69], [8, 9], [8, 60], [8, 70], [9, 10], [9, 61], [9, 71], [10, 11], [10, 62], [10, 72], [11, 12], [11, 63], [11, 73], [12, 13], [12, 64], [12, 74], [13, 14], [13, 65], [13, 75], [14, 15], [14, 66], [14, 76], [15, 16], [15, 67], [15, 77], [16, 17], [16, 68], [16, 78], [17, 18], [17, 69], [17, 79], [18, 19], [18, 70], [18, 80], [19, 20], [19, 71], [19, 81], [20, 21], [20, 72], [20, 82], [21, 22], [21, 73], [21, 83], [22, 23], [22, 74], [22, 84], [23, 24], [23, 75], [23, 85], [24, 25], [24, 76], [24, 86], [25, 26], [25, 77], [25, 87], [26, 27], [26, 78], [26, 88], [27, 28], [27, 79], [27, 89], [28, 29], [28, 80], [28, 90], [29, 30], [29, 81], [29, 91], [30, 31], [30, 82], [30, 92], [31, 32], [31, 83], [31, 93], [32, 33], [32, 84], [32, 94], [33, 34], [33, 85], [33, 95], [34, 35], [34, 86], [34, 96], [35, 36], [35, 87], [35, 97], [36, 37], [36, 88], [36, 98], [37, 38], [37, 89], [37, 99], [38, 39], [38, 90], [38, 100], [39, 40], [39, 91], [39, 101], [40, 41], [40, 92], [40, 102], [41, 42], [41, 93], [41, 103], [42, 43], [42, 94], [42, 104], [43, 44], [43, 53], [43, 95], [44, 45], [44, 54], [44, 96], [45, 46], [45, 55], [45, 97], [46, 47], [46, 56], [46, 98], [47, 48], [47, 57], [47, 99], [48, 49], [48, 58], [48, 100], [49, 50], [49, 59], [49, 101], [50, 51], [50, 60], [50, 102], [51, 52], [51, 61], [51, 103], [52, 62], [52, 104], [53, 54], [53, 104], [54, 55], [55, 56], [56, 57], [57, 58], [58, 59], [59, 60], [60, 61], [61, 62], [62, 63], [63, 64], [64, 65], [65, 66], [66, 67], [67, 68], [68, 69], [69, 70], [70, 71], [71, 72], [72, 73], [73, 74], [74, 75], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80], [80, 81], [81, 82], [82, 83], [83, 84], [84, 85], [85, 86], [86, 87], [87, 88], [88, 89], [89, 90], [90, 91], [91, 92], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104]]);;
R:=P177Census(D);;Need(Size(R.F)=416);;
PrintTo("current_c4_descent/104_004.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 104_004 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
