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
D:=P177Graph("120_013",120,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108],[[1, 13], [1, 24], [1, 112], [1, 117], [2, 13], [2, 14], [2, 113], [2, 118], [3, 14], [3, 15], [3, 114], [3, 119], [4, 15], [4, 16], [4, 115], [4, 120], [5, 16], [5, 17], [5, 109], [5, 116], [6, 17], [6, 18], [6, 110], [6, 117], [7, 18], [7, 19], [7, 111], [7, 118], [8, 19], [8, 20], [8, 112], [8, 119], [9, 20], [9, 21], [9, 113], [9, 120], [10, 21], [10, 22], [10, 109], [10, 114], [11, 22], [11, 23], [11, 110], [11, 115], [12, 23], [12, 24], [12, 111], [12, 116], [13, 29], [13, 34], [14, 30], [14, 35], [15, 31], [15, 36], [16, 25], [16, 32], [17, 26], [17, 33], [18, 27], [18, 34], [19, 28], [19, 35], [20, 29], [20, 36], [21, 25], [21, 30], [22, 26], [22, 31], [23, 27], [23, 32], [24, 28], [24, 33], [25, 37], [25, 48], [26, 37], [26, 38], [27, 38], [27, 39], [28, 39], [28, 40], [29, 40], [29, 41], [30, 41], [30, 42], [31, 42], [31, 43], [32, 43], [32, 44], [33, 44], [33, 45], [34, 45], [34, 46], [35, 46], [35, 47], [36, 47], [36, 48], [37, 53], [37, 58], [38, 54], [38, 59], [39, 55], [39, 60], [40, 49], [40, 56], [41, 50], [41, 57], [42, 51], [42, 58], [43, 52], [43, 59], [44, 53], [44, 60], [45, 49], [45, 54], [46, 50], [46, 55], [47, 51], [47, 56], [48, 52], [48, 57], [49, 61], [49, 72], [50, 61], [50, 62], [51, 62], [51, 63], [52, 63], [52, 64], [53, 64], [53, 65], [54, 65], [54, 66], [55, 66], [55, 67], [56, 67], [56, 68], [57, 68], [57, 69], [58, 69], [58, 70], [59, 70], [59, 71], [60, 71], [60, 72], [61, 77], [61, 82], [62, 78], [62, 83], [63, 79], [63, 84], [64, 73], [64, 80], [65, 74], [65, 81], [66, 75], [66, 82], [67, 76], [67, 83], [68, 77], [68, 84], [69, 73], [69, 78], [70, 74], [70, 79], [71, 75], [71, 80], [72, 76], [72, 81], [73, 85], [73, 96], [74, 85], [74, 86], [75, 86], [75, 87], [76, 87], [76, 88], [77, 88], [77, 89], [78, 89], [78, 90], [79, 90], [79, 91], [80, 91], [80, 92], [81, 92], [81, 93], [82, 93], [82, 94], [83, 94], [83, 95], [84, 95], [84, 96], [85, 101], [85, 106], [86, 102], [86, 107], [87, 103], [87, 108], [88, 97], [88, 104], [89, 98], [89, 105], [90, 99], [90, 106], [91, 100], [91, 107], [92, 101], [92, 108], [93, 97], [93, 102], [94, 98], [94, 103], [95, 99], [95, 104], [96, 100], [96, 105], [97, 109], [97, 120], [98, 109], [98, 110], [99, 110], [99, 111], [100, 111], [100, 112], [101, 112], [101, 113], [102, 113], [102, 114], [103, 114], [103, 115], [104, 115], [104, 116], [105, 116], [105, 117], [106, 117], [106, 118], [107, 118], [107, 119], [108, 119], [108, 120]]);;
R:=P177Census(D);;Need(Size(R.F)=480);;
PrintTo("current_c4_descent/120_013.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_013 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
