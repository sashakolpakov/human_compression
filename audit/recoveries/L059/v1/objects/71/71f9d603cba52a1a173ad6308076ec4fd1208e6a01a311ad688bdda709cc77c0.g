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
D:=P177Graph("120_004",120,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119],[[1, 2], [1, 30], [1, 92], [1, 120], [2, 3], [2, 31], [2, 93], [3, 4], [3, 32], [3, 94], [4, 5], [4, 33], [4, 95], [5, 6], [5, 34], [5, 96], [6, 7], [6, 35], [6, 97], [7, 8], [7, 36], [7, 98], [8, 9], [8, 37], [8, 99], [9, 10], [9, 38], [9, 100], [10, 11], [10, 39], [10, 101], [11, 12], [11, 40], [11, 102], [12, 13], [12, 41], [12, 103], [13, 14], [13, 42], [13, 104], [14, 15], [14, 43], [14, 105], [15, 16], [15, 44], [15, 106], [16, 17], [16, 45], [16, 107], [17, 18], [17, 46], [17, 108], [18, 19], [18, 47], [18, 109], [19, 20], [19, 48], [19, 110], [20, 21], [20, 49], [20, 111], [21, 22], [21, 50], [21, 112], [22, 23], [22, 51], [22, 113], [23, 24], [23, 52], [23, 114], [24, 25], [24, 53], [24, 115], [25, 26], [25, 54], [25, 116], [26, 27], [26, 55], [26, 117], [27, 28], [27, 56], [27, 118], [28, 29], [28, 57], [28, 119], [29, 30], [29, 58], [29, 120], [30, 31], [30, 59], [31, 32], [31, 60], [32, 33], [32, 61], [33, 34], [33, 62], [34, 35], [34, 63], [35, 36], [35, 64], [36, 37], [36, 65], [37, 38], [37, 66], [38, 39], [38, 67], [39, 40], [39, 68], [40, 41], [40, 69], [41, 42], [41, 70], [42, 43], [42, 71], [43, 44], [43, 72], [44, 45], [44, 73], [45, 46], [45, 74], [46, 47], [46, 75], [47, 48], [47, 76], [48, 49], [48, 77], [49, 50], [49, 78], [50, 51], [50, 79], [51, 52], [51, 80], [52, 53], [52, 81], [53, 54], [53, 82], [54, 55], [54, 83], [55, 56], [55, 84], [56, 57], [56, 85], [57, 58], [57, 86], [58, 59], [58, 87], [59, 60], [59, 88], [60, 61], [60, 89], [61, 62], [61, 90], [62, 63], [62, 91], [63, 64], [63, 92], [64, 65], [64, 93], [65, 66], [65, 94], [66, 67], [66, 95], [67, 68], [67, 96], [68, 69], [68, 97], [69, 70], [69, 98], [70, 71], [70, 99], [71, 72], [71, 100], [72, 73], [72, 101], [73, 74], [73, 102], [74, 75], [74, 103], [75, 76], [75, 104], [76, 77], [76, 105], [77, 78], [77, 106], [78, 79], [78, 107], [79, 80], [79, 108], [80, 81], [80, 109], [81, 82], [81, 110], [82, 83], [82, 111], [83, 84], [83, 112], [84, 85], [84, 113], [85, 86], [85, 114], [86, 87], [86, 115], [87, 88], [87, 116], [88, 89], [88, 117], [89, 90], [89, 118], [90, 91], [90, 119], [91, 92], [91, 120], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108], [108, 109], [109, 110], [110, 111], [111, 112], [112, 113], [113, 114], [114, 115], [115, 116], [116, 117], [117, 118], [118, 119], [119, 120]]);;
R:=P177Census(D);;Need(Size(R.F)=480);;
PrintTo("current_c4_descent/120_004.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_004 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
