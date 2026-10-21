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
D:=P177Graph("120_042",120,[1, 2, 3, 4, 5, 16, 17, 18, 19, 20, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 86, 87, 88, 89, 90, 106, 107, 108, 109, 110, 116, 117, 118, 119, 120],[[1, 6], [1, 8], [1, 11], [1, 21], [2, 21], [2, 83], [2, 85], [2, 92], [3, 11], [3, 57], [3, 61], [3, 63], [4, 92], [4, 99], [4, 100], [4, 114], [5, 57], [5, 102], [5, 104], [5, 114], [6, 16], [6, 18], [6, 41], [7, 41], [7, 48], [7, 50], [7, 109], [8, 31], [8, 33], [8, 71], [9, 89], [9, 109], [9, 119], [9, 120], [10, 71], [10, 78], [10, 80], [10, 89], [11, 26], [11, 46], [12, 46], [12, 80], [12, 108], [12, 110], [13, 26], [13, 32], [13, 41], [13, 43], [14, 69], [14, 70], [14, 80], [14, 119], [15, 32], [15, 72], [15, 74], [15, 119], [16, 36], [16, 38], [16, 61], [17, 23], [17, 25], [17, 61], [17, 84], [18, 56], [18, 58], [18, 101], [19, 54], [19, 84], [19, 114], [19, 115], [20, 54], [20, 92], [20, 94], [20, 101], [21, 28], [21, 76], [22, 50], [22, 76], [22, 88], [22, 90], [23, 28], [23, 71], [23, 73], [24, 50], [24, 67], [24, 69], [24, 120], [25, 42], [25, 44], [25, 120], [26, 51], [26, 81], [27, 81], [27, 94], [27, 95], [27, 102], [28, 51], [28, 62], [29, 39], [29, 40], [29, 99], [29, 102], [30, 59], [30, 60], [30, 62], [30, 99], [31, 36], [31, 37], [31, 83], [32, 65], [32, 83], [33, 91], [33, 93], [33, 97], [34, 55], [34, 65], [34, 112], [34, 114], [35, 55], [35, 57], [35, 59], [35, 97], [36, 66], [36, 68], [37, 43], [37, 45], [37, 49], [38, 73], [38, 75], [38, 79], [39, 49], [39, 89], [39, 90], [40, 79], [40, 109], [40, 110], [41, 95], [42, 53], [42, 55], [42, 95], [43, 101], [43, 103], [44, 97], [44, 99], [44, 115], [45, 62], [45, 64], [45, 115], [46, 53], [46, 105], [47, 85], [47, 105], [47, 113], [47, 115], [48, 53], [48, 56], [48, 57], [49, 85], [49, 100], [50, 100], [51, 86], [51, 106], [52, 72], [52, 76], [52, 78], [52, 106], [53, 86], [54, 69], [54, 72], [55, 69], [56, 66], [56, 67], [58, 106], [58, 107], [58, 117], [59, 87], [59, 89], [60, 71], [60, 72], [60, 117], [61, 108], [62, 108], [63, 67], [63, 77], [63, 79], [64, 90], [64, 117], [64, 119], [65, 67], [65, 90], [66, 96], [66, 98], [68, 91], [68, 103], [68, 105], [70, 84], [70, 85], [70, 91], [73, 96], [73, 97], [74, 101], [74, 102], [74, 112], [75, 81], [75, 82], [75, 112], [76, 98], [77, 98], [77, 111], [77, 112], [78, 91], [78, 92], [79, 104], [80, 104], [81, 88], [82, 110], [82, 118], [82, 120], [83, 88], [84, 110], [86, 93], [86, 111], [87, 93], [87, 104], [87, 105], [88, 111], [93, 118], [94, 107], [94, 109], [95, 118], [96, 116], [96, 118], [98, 107], [100, 107], [103, 116], [103, 117], [106, 113], [108, 113], [111, 116], [113, 116]]);;
R:=P177Census(D);;Need(Size(R.F)=480);;
PrintTo("current_c4_descent/120_042.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_042 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
