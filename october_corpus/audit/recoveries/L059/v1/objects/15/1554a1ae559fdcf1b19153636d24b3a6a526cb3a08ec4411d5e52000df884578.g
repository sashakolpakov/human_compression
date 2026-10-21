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
D:=P177Graph("120_035",120,[1, 4, 5, 6, 8, 14, 16, 17, 19, 20, 21, 22, 23, 25, 27, 28, 30, 33, 39, 40, 46, 47, 50, 52, 53, 55, 56, 57, 60, 61, 62, 63, 64, 65, 68, 69, 70, 71, 72, 73, 75, 77, 78, 79, 82, 87, 90, 99, 102, 104, 106, 107, 108, 109, 110, 111, 112, 114, 115, 117],[[1, 2], [1, 3], [1, 7], [1, 11], [2, 4], [2, 5], [2, 17], [3, 6], [3, 8], [3, 25], [4, 7], [4, 9], [4, 26], [5, 10], [5, 12], [5, 37], [6, 11], [6, 13], [6, 38], [7, 14], [7, 39], [8, 15], [8, 18], [8, 54], [9, 16], [9, 19], [9, 55], [10, 17], [10, 20], [10, 56], [11, 21], [11, 57], [12, 22], [12, 27], [12, 72], [13, 23], [13, 28], [13, 73], [14, 24], [14, 29], [14, 74], [15, 25], [15, 30], [15, 75], [16, 26], [16, 31], [16, 51], [17, 32], [17, 76], [18, 33], [18, 40], [18, 90], [19, 34], [19, 41], [19, 91], [20, 35], [20, 42], [20, 92], [21, 36], [21, 43], [21, 74], [22, 37], [22, 44], [22, 93], [23, 35], [23, 38], [23, 45], [24, 39], [24, 46], [24, 71], [25, 32], [25, 89], [26, 47], [26, 82], [27, 48], [27, 58], [27, 105], [28, 49], [28, 59], [28, 83], [29, 50], [29, 60], [29, 106], [30, 42], [30, 51], [30, 88], [31, 52], [31, 61], [31, 64], [32, 53], [32, 62], [33, 44], [33, 54], [33, 95], [34, 55], [34, 63], [34, 65], [35, 52], [35, 56], [36, 57], [36, 61], [36, 64], [37, 47], [37, 104], [38, 63], [38, 65], [39, 66], [39, 100], [40, 58], [40, 67], [40, 94], [41, 68], [41, 77], [41, 114], [42, 69], [42, 78], [43, 70], [43, 79], [43, 102], [44, 61], [44, 71], [45, 46], [45, 52], [45, 71], [46, 80], [46, 84], [47, 49], [47, 81], [48, 63], [48, 72], [48, 107], [49, 73], [49, 82], [50, 74], [50, 83], [50, 85], [51, 52], [51, 75], [53, 76], [53, 80], [53, 84], [54, 65], [54, 104], [55, 66], [55, 113], [56, 83], [56, 85], [57, 86], [57, 103], [58, 77], [58, 87], [59, 68], [59, 87], [59, 109], [60, 88], [60, 94], [60, 118], [61, 95], [62, 89], [62, 96], [62, 97], [63, 80], [64, 96], [64, 97], [65, 98], [66, 69], [66, 99], [67, 82], [67, 90], [67, 107], [68, 83], [68, 91], [69, 92], [69, 100], [70, 74], [70, 91], [70, 101], [71, 93], [72, 85], [72, 113], [73, 86], [73, 116], [75, 91], [75, 101], [76, 102], [76, 112], [77, 94], [77, 103], [78, 86], [78, 88], [78, 103], [79, 92], [79, 105], [79, 120], [80, 107], [81, 104], [81, 108], [81, 109], [82, 97], [84, 108], [84, 109], [85, 110], [86, 99], [87, 100], [87, 105], [88, 106], [89, 106], [89, 111], [90, 101], [90, 116], [92, 102], [93, 106], [93, 111], [94, 112], [95, 102], [95, 112], [96, 114], [96, 115], [97, 107], [98, 104], [98, 114], [98, 115], [99, 113], [99, 116], [100, 109], [101, 117], [103, 114], [105, 111], [108, 118], [108, 119], [110, 113], [110, 118], [110, 119], [111, 120], [112, 118], [115, 119], [115, 120], [116, 117], [117, 119], [117, 120]]);;
R:=P177Census(D);;Need(Size(R.F)=480);;
PrintTo("current_c4_descent/120_035.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_035 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
