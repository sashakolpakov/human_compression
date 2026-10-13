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
D:=P177Graph("112_004",112,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112],[[1, 2], [1, 56], [1, 57], [1, 87], [2, 3], [2, 58], [2, 88], [3, 4], [3, 59], [3, 89], [4, 5], [4, 60], [4, 90], [5, 6], [5, 61], [5, 91], [6, 7], [6, 62], [6, 92], [7, 8], [7, 63], [7, 93], [8, 9], [8, 64], [8, 94], [9, 10], [9, 65], [9, 95], [10, 11], [10, 66], [10, 96], [11, 12], [11, 67], [11, 97], [12, 13], [12, 68], [12, 98], [13, 14], [13, 69], [13, 99], [14, 15], [14, 70], [14, 100], [15, 16], [15, 71], [15, 101], [16, 17], [16, 72], [16, 102], [17, 18], [17, 73], [17, 103], [18, 19], [18, 74], [18, 104], [19, 20], [19, 75], [19, 105], [20, 21], [20, 76], [20, 106], [21, 22], [21, 77], [21, 107], [22, 23], [22, 78], [22, 108], [23, 24], [23, 79], [23, 109], [24, 25], [24, 80], [24, 110], [25, 26], [25, 81], [25, 111], [26, 27], [26, 82], [26, 112], [27, 28], [27, 57], [27, 83], [28, 29], [28, 58], [28, 84], [29, 30], [29, 59], [29, 85], [30, 31], [30, 60], [30, 86], [31, 32], [31, 61], [31, 87], [32, 33], [32, 62], [32, 88], [33, 34], [33, 63], [33, 89], [34, 35], [34, 64], [34, 90], [35, 36], [35, 65], [35, 91], [36, 37], [36, 66], [36, 92], [37, 38], [37, 67], [37, 93], [38, 39], [38, 68], [38, 94], [39, 40], [39, 69], [39, 95], [40, 41], [40, 70], [40, 96], [41, 42], [41, 71], [41, 97], [42, 43], [42, 72], [42, 98], [43, 44], [43, 73], [43, 99], [44, 45], [44, 74], [44, 100], [45, 46], [45, 75], [45, 101], [46, 47], [46, 76], [46, 102], [47, 48], [47, 77], [47, 103], [48, 49], [48, 78], [48, 104], [49, 50], [49, 79], [49, 105], [50, 51], [50, 80], [50, 106], [51, 52], [51, 81], [51, 107], [52, 53], [52, 82], [52, 108], [53, 54], [53, 83], [53, 109], [54, 55], [54, 84], [54, 110], [55, 56], [55, 85], [55, 111], [56, 86], [56, 112], [57, 58], [57, 112], [58, 59], [59, 60], [60, 61], [61, 62], [62, 63], [63, 64], [64, 65], [65, 66], [66, 67], [67, 68], [68, 69], [69, 70], [70, 71], [71, 72], [72, 73], [73, 74], [74, 75], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80], [80, 81], [81, 82], [82, 83], [83, 84], [84, 85], [85, 86], [86, 87], [87, 88], [88, 89], [89, 90], [90, 91], [91, 92], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108], [108, 109], [109, 110], [110, 111], [111, 112]]);;
R:=P177Census(D);;Need(Size(R.F)=448);;
PrintTo("current_c4_descent/112_004.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 112_004 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
