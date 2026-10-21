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
D:=P177Graph("120_036",120,[1, 4, 5, 6, 8, 12, 15, 17, 18, 21, 22, 23, 25, 27, 30, 31, 33, 35, 36, 39, 41, 42, 46, 48, 49, 52, 53, 56, 57, 59, 61, 63, 65, 68, 69, 73, 74, 77, 78, 80, 81, 84, 86, 87, 89, 90, 93, 94, 95, 97, 98, 102, 105, 107, 112, 113, 116, 117, 118, 119],[[1, 2], [1, 3], [1, 13], [1, 20], [2, 4], [2, 5], [2, 21], [3, 6], [3, 8], [3, 31], [4, 7], [4, 9], [4, 32], [5, 10], [5, 13], [5, 44], [6, 11], [6, 14], [6, 45], [7, 12], [7, 15], [7, 46], [8, 16], [8, 20], [8, 62], [9, 17], [9, 21], [9, 49], [10, 18], [10, 22], [10, 63], [11, 17], [11, 23], [11, 48], [12, 14], [12, 19], [12, 24], [13, 25], [13, 80], [14, 31], [14, 35], [15, 26], [15, 32], [15, 67], [16, 27], [16, 33], [16, 53], [17, 28], [17, 29], [18, 26], [18, 34], [18, 66], [19, 22], [19, 30], [19, 35], [20, 36], [20, 98], [21, 37], [21, 99], [22, 44], [22, 50], [23, 38], [23, 45], [23, 85], [24, 39], [24, 46], [24, 86], [25, 40], [25, 47], [25, 71], [26, 41], [26, 42], [27, 34], [27, 38], [27, 83], [28, 39], [28, 48], [28, 84], [29, 30], [29, 33], [29, 49], [30, 43], [30, 50], [31, 51], [31, 91], [32, 52], [32, 112], [33, 43], [33, 62], [34, 53], [34, 63], [35, 54], [35, 104], [36, 55], [36, 64], [36, 70], [37, 56], [37, 65], [37, 89], [38, 57], [38, 59], [39, 58], [39, 60], [40, 48], [40, 53], [40, 102], [41, 54], [41, 66], [41, 103], [42, 43], [42, 47], [42, 67], [43, 61], [44, 68], [44, 95], [45, 69], [45, 112], [46, 55], [46, 70], [47, 61], [47, 80], [48, 71], [49, 72], [49, 110], [50, 59], [50, 73], [51, 74], [51, 81], [51, 105], [52, 75], [52, 82], [52, 106], [53, 76], [54, 77], [54, 78], [55, 63], [55, 113], [56, 66], [56, 71], [56, 114], [57, 72], [57, 83], [57, 114], [58, 73], [58, 81], [58, 84], [59, 64], [59, 85], [60, 61], [60, 65], [60, 86], [61, 79], [62, 77], [62, 87], [63, 88], [64, 73], [64, 98], [65, 79], [65, 99], [66, 89], [67, 90], [67, 118], [68, 91], [68, 100], [68, 115], [69, 92], [69, 101], [69, 108], [70, 74], [70, 93], [71, 94], [72, 95], [72, 97], [73, 96], [74, 83], [74, 103], [75, 84], [75, 89], [75, 119], [76, 90], [76, 102], [76, 119], [77, 100], [77, 103], [78, 79], [78, 82], [78, 104], [79, 98], [80, 96], [80, 101], [81, 91], [81, 96], [82, 98], [82, 112], [83, 105], [84, 106], [85, 107], [85, 117], [86, 92], [86, 108], [87, 99], [87, 100], [87, 111], [88, 107], [88, 113], [88, 116], [89, 109], [90, 110], [90, 111], [91, 102], [92, 105], [92, 116], [93, 103], [93, 106], [93, 120], [94, 108], [94, 114], [94, 120], [95, 100], [95, 114], [96, 97], [97, 101], [97, 110], [99, 113], [101, 112], [102, 115], [104, 107], [104, 116], [105, 109], [106, 117], [107, 115], [108, 118], [109, 116], [109, 119], [110, 119], [111, 113], [111, 118], [115, 117], [117, 120], [118, 120]]);;
R:=P177Census(D);;Need(Size(R.F)=480);;
PrintTo("current_c4_descent/120_036.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_036 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
