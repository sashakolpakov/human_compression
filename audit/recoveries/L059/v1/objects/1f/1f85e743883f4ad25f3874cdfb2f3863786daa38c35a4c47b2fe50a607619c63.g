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
D:=P177Graph("120_006",120,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119],[[1, 2], [1, 42], [1, 80], [1, 120], [2, 3], [2, 43], [2, 81], [3, 4], [3, 44], [3, 82], [4, 5], [4, 45], [4, 83], [5, 6], [5, 46], [5, 84], [6, 7], [6, 47], [6, 85], [7, 8], [7, 48], [7, 86], [8, 9], [8, 49], [8, 87], [9, 10], [9, 50], [9, 88], [10, 11], [10, 51], [10, 89], [11, 12], [11, 52], [11, 90], [12, 13], [12, 53], [12, 91], [13, 14], [13, 54], [13, 92], [14, 15], [14, 55], [14, 93], [15, 16], [15, 56], [15, 94], [16, 17], [16, 57], [16, 95], [17, 18], [17, 58], [17, 96], [18, 19], [18, 59], [18, 97], [19, 20], [19, 60], [19, 98], [20, 21], [20, 61], [20, 99], [21, 22], [21, 62], [21, 100], [22, 23], [22, 63], [22, 101], [23, 24], [23, 64], [23, 102], [24, 25], [24, 65], [24, 103], [25, 26], [25, 66], [25, 104], [26, 27], [26, 67], [26, 105], [27, 28], [27, 68], [27, 106], [28, 29], [28, 69], [28, 107], [29, 30], [29, 70], [29, 108], [30, 31], [30, 71], [30, 109], [31, 32], [31, 72], [31, 110], [32, 33], [32, 73], [32, 111], [33, 34], [33, 74], [33, 112], [34, 35], [34, 75], [34, 113], [35, 36], [35, 76], [35, 114], [36, 37], [36, 77], [36, 115], [37, 38], [37, 78], [37, 116], [38, 39], [38, 79], [38, 117], [39, 40], [39, 80], [39, 118], [40, 41], [40, 81], [40, 119], [41, 42], [41, 82], [41, 120], [42, 43], [42, 83], [43, 44], [43, 84], [44, 45], [44, 85], [45, 46], [45, 86], [46, 47], [46, 87], [47, 48], [47, 88], [48, 49], [48, 89], [49, 50], [49, 90], [50, 51], [50, 91], [51, 52], [51, 92], [52, 53], [52, 93], [53, 54], [53, 94], [54, 55], [54, 95], [55, 56], [55, 96], [56, 57], [56, 97], [57, 58], [57, 98], [58, 59], [58, 99], [59, 60], [59, 100], [60, 61], [60, 101], [61, 62], [61, 102], [62, 63], [62, 103], [63, 64], [63, 104], [64, 65], [64, 105], [65, 66], [65, 106], [66, 67], [66, 107], [67, 68], [67, 108], [68, 69], [68, 109], [69, 70], [69, 110], [70, 71], [70, 111], [71, 72], [71, 112], [72, 73], [72, 113], [73, 74], [73, 114], [74, 75], [74, 115], [75, 76], [75, 116], [76, 77], [76, 117], [77, 78], [77, 118], [78, 79], [78, 119], [79, 80], [79, 120], [80, 81], [81, 82], [82, 83], [83, 84], [84, 85], [85, 86], [86, 87], [87, 88], [88, 89], [89, 90], [90, 91], [91, 92], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108], [108, 109], [109, 110], [110, 111], [111, 112], [112, 113], [113, 114], [114, 115], [115, 116], [116, 117], [117, 118], [118, 119], [119, 120]]);;
R:=P177Census(D);;Need(Size(R.F)=480);;
PrintTo("current_c4_descent/120_006.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_006 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
