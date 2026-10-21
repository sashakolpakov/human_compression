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
D:=P177Graph("120_007",120,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119],[[1, 2], [1, 50], [1, 72], [1, 120], [2, 3], [2, 51], [2, 73], [3, 4], [3, 52], [3, 74], [4, 5], [4, 53], [4, 75], [5, 6], [5, 54], [5, 76], [6, 7], [6, 55], [6, 77], [7, 8], [7, 56], [7, 78], [8, 9], [8, 57], [8, 79], [9, 10], [9, 58], [9, 80], [10, 11], [10, 59], [10, 81], [11, 12], [11, 60], [11, 82], [12, 13], [12, 61], [12, 83], [13, 14], [13, 62], [13, 84], [14, 15], [14, 63], [14, 85], [15, 16], [15, 64], [15, 86], [16, 17], [16, 65], [16, 87], [17, 18], [17, 66], [17, 88], [18, 19], [18, 67], [18, 89], [19, 20], [19, 68], [19, 90], [20, 21], [20, 69], [20, 91], [21, 22], [21, 70], [21, 92], [22, 23], [22, 71], [22, 93], [23, 24], [23, 72], [23, 94], [24, 25], [24, 73], [24, 95], [25, 26], [25, 74], [25, 96], [26, 27], [26, 75], [26, 97], [27, 28], [27, 76], [27, 98], [28, 29], [28, 77], [28, 99], [29, 30], [29, 78], [29, 100], [30, 31], [30, 79], [30, 101], [31, 32], [31, 80], [31, 102], [32, 33], [32, 81], [32, 103], [33, 34], [33, 82], [33, 104], [34, 35], [34, 83], [34, 105], [35, 36], [35, 84], [35, 106], [36, 37], [36, 85], [36, 107], [37, 38], [37, 86], [37, 108], [38, 39], [38, 87], [38, 109], [39, 40], [39, 88], [39, 110], [40, 41], [40, 89], [40, 111], [41, 42], [41, 90], [41, 112], [42, 43], [42, 91], [42, 113], [43, 44], [43, 92], [43, 114], [44, 45], [44, 93], [44, 115], [45, 46], [45, 94], [45, 116], [46, 47], [46, 95], [46, 117], [47, 48], [47, 96], [47, 118], [48, 49], [48, 97], [48, 119], [49, 50], [49, 98], [49, 120], [50, 51], [50, 99], [51, 52], [51, 100], [52, 53], [52, 101], [53, 54], [53, 102], [54, 55], [54, 103], [55, 56], [55, 104], [56, 57], [56, 105], [57, 58], [57, 106], [58, 59], [58, 107], [59, 60], [59, 108], [60, 61], [60, 109], [61, 62], [61, 110], [62, 63], [62, 111], [63, 64], [63, 112], [64, 65], [64, 113], [65, 66], [65, 114], [66, 67], [66, 115], [67, 68], [67, 116], [68, 69], [68, 117], [69, 70], [69, 118], [70, 71], [70, 119], [71, 72], [71, 120], [72, 73], [73, 74], [74, 75], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80], [80, 81], [81, 82], [82, 83], [83, 84], [84, 85], [85, 86], [86, 87], [87, 88], [88, 89], [89, 90], [90, 91], [91, 92], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108], [108, 109], [109, 110], [110, 111], [111, 112], [112, 113], [113, 114], [114, 115], [115, 116], [116, 117], [117, 118], [118, 119], [119, 120]]);;
R:=P177Census(D);;Need(Size(R.F)=480);;
PrintTo("current_c4_descent/120_007.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_007 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
