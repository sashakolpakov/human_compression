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
D:=P177Graph("120_027",120,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119],[[1, 2], [1, 30], [1, 58], [1, 61], [2, 3], [2, 59], [2, 62], [3, 4], [3, 60], [3, 63], [4, 5], [4, 31], [4, 64], [5, 6], [5, 32], [5, 65], [6, 7], [6, 33], [6, 66], [7, 8], [7, 34], [7, 67], [8, 9], [8, 35], [8, 68], [9, 10], [9, 36], [9, 69], [10, 11], [10, 37], [10, 70], [11, 12], [11, 38], [11, 71], [12, 13], [12, 39], [12, 72], [13, 14], [13, 40], [13, 73], [14, 15], [14, 41], [14, 74], [15, 16], [15, 42], [15, 75], [16, 17], [16, 43], [16, 76], [17, 18], [17, 44], [17, 77], [18, 19], [18, 45], [18, 78], [19, 20], [19, 46], [19, 79], [20, 21], [20, 47], [20, 80], [21, 22], [21, 48], [21, 81], [22, 23], [22, 49], [22, 82], [23, 24], [23, 50], [23, 83], [24, 25], [24, 51], [24, 84], [25, 26], [25, 52], [25, 85], [26, 27], [26, 53], [26, 86], [27, 28], [27, 54], [27, 87], [28, 29], [28, 55], [28, 88], [29, 30], [29, 56], [29, 89], [30, 57], [30, 90], [31, 61], [31, 71], [31, 104], [32, 62], [32, 72], [32, 105], [33, 63], [33, 73], [33, 106], [34, 64], [34, 74], [34, 107], [35, 65], [35, 75], [35, 108], [36, 66], [36, 76], [36, 109], [37, 67], [37, 77], [37, 110], [38, 68], [38, 78], [38, 111], [39, 69], [39, 79], [39, 112], [40, 70], [40, 80], [40, 113], [41, 71], [41, 81], [41, 114], [42, 72], [42, 82], [42, 115], [43, 73], [43, 83], [43, 116], [44, 74], [44, 84], [44, 117], [45, 75], [45, 85], [45, 118], [46, 76], [46, 86], [46, 119], [47, 77], [47, 87], [47, 120], [48, 78], [48, 88], [48, 91], [49, 79], [49, 89], [49, 92], [50, 80], [50, 90], [50, 93], [51, 61], [51, 81], [51, 94], [52, 62], [52, 82], [52, 95], [53, 63], [53, 83], [53, 96], [54, 64], [54, 84], [54, 97], [55, 65], [55, 85], [55, 98], [56, 66], [56, 86], [56, 99], [57, 67], [57, 87], [57, 100], [58, 68], [58, 88], [58, 101], [59, 69], [59, 89], [59, 102], [60, 70], [60, 90], [60, 103], [61, 91], [62, 92], [63, 93], [64, 94], [65, 95], [66, 96], [67, 97], [68, 98], [69, 99], [70, 100], [71, 101], [72, 102], [73, 103], [74, 104], [75, 105], [76, 106], [77, 107], [78, 108], [79, 109], [80, 110], [81, 111], [82, 112], [83, 113], [84, 114], [85, 115], [86, 116], [87, 117], [88, 118], [89, 119], [90, 120], [91, 102], [91, 110], [92, 103], [92, 111], [93, 104], [93, 112], [94, 105], [94, 113], [95, 106], [95, 114], [96, 107], [96, 115], [97, 108], [97, 116], [98, 109], [98, 117], [99, 110], [99, 118], [100, 111], [100, 119], [101, 112], [101, 120], [102, 113], [103, 114], [104, 115], [105, 116], [106, 117], [107, 118], [108, 119], [109, 120]]);;
R:=P177Census(D);;Need(Size(R.F)=480);;
PrintTo("current_c4_descent/120_027.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_027 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
