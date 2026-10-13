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
D:=P177Graph("120_048",120,[1, 2, 5, 9, 12, 13, 14, 18, 19, 21, 23, 25, 27, 28, 29, 30, 31, 32, 36, 37, 38, 42, 44, 50, 51, 54, 56, 65, 68, 70, 74, 75, 76, 78, 80, 81, 82, 86, 88, 89, 90, 91, 92, 95, 96, 101, 103, 105, 106, 107, 110, 112, 113, 114, 115, 116, 117, 118, 119, 120],[[1, 6], [1, 16], [1, 62], [1, 109], [2, 52], [2, 72], [2, 85], [2, 111], [3, 18], [3, 51], [3, 101], [3, 115], [4, 38], [4, 54], [4, 78], [4, 118], [5, 11], [5, 33], [5, 41], [5, 93], [6, 19], [6, 51], [6, 105], [7, 19], [7, 25], [7, 75], [7, 101], [8, 96], [8, 113], [8, 114], [8, 118], [9, 35], [9, 69], [9, 85], [9, 104], [10, 54], [10, 75], [10, 76], [10, 117], [11, 30], [11, 105], [11, 106], [12, 83], [12, 94], [12, 99], [12, 104], [13, 53], [13, 61], [13, 67], [13, 98], [14, 24], [14, 48], [14, 84], [14, 102], [15, 51], [15, 91], [15, 95], [15, 106], [16, 23], [16, 30], [16, 65], [17, 28], [17, 44], [17, 54], [17, 105], [18, 39], [18, 64], [18, 85], [19, 40], [19, 94], [20, 27], [20, 65], [20, 90], [20, 120], [21, 26], [21, 63], [21, 72], [21, 79], [22, 32], [22, 37], [22, 92], [22, 110], [23, 83], [23, 97], [23, 98], [24, 42], [24, 50], [24, 119], [25, 52], [25, 53], [25, 71], [26, 30], [26, 110], [26, 116], [27, 43], [27, 55], [27, 58], [28, 47], [28, 108], [28, 109], [29, 40], [29, 57], [29, 64], [29, 100], [30, 60], [31, 41], [31, 63], [31, 85], [31, 102], [32, 59], [32, 73], [32, 100], [33, 81], [33, 88], [33, 113], [34, 36], [34, 82], [34, 96], [34, 112], [35, 80], [35, 81], [35, 110], [36, 48], [36, 53], [36, 73], [37, 58], [37, 72], [37, 97], [38, 43], [38, 87], [38, 99], [39, 82], [39, 92], [39, 113], [40, 107], [40, 120], [41, 95], [41, 96], [42, 46], [42, 64], [42, 104], [43, 50], [43, 86], [44, 60], [44, 97], [44, 99], [45, 92], [45, 105], [45, 114], [45, 115], [46, 68], [46, 82], [46, 88], [47, 75], [47, 86], [47, 89], [48, 76], [48, 89], [49, 50], [49, 54], [49, 56], [49, 74], [50, 108], [51, 77], [52, 76], [52, 80], [53, 56], [55, 95], [55, 107], [55, 116], [56, 62], [56, 66], [57, 86], [57, 92], [57, 103], [58, 103], [58, 118], [59, 106], [59, 107], [59, 113], [60, 81], [60, 117], [61, 65], [61, 68], [61, 119], [62, 75], [62, 90], [63, 103], [63, 115], [64, 89], [65, 94], [66, 68], [66, 78], [66, 81], [67, 90], [67, 112], [67, 118], [68, 69], [69, 74], [69, 101], [70, 71], [70, 73], [70, 79], [70, 84], [71, 74], [71, 91], [72, 112], [73, 88], [74, 77], [76, 83], [77, 119], [77, 120], [78, 93], [78, 111], [79, 80], [79, 95], [80, 100], [82, 102], [83, 112], [84, 86], [84, 107], [87, 106], [87, 114], [87, 120], [88, 98], [89, 94], [90, 93], [91, 102], [91, 108], [93, 116], [96, 111], [97, 114], [98, 110], [99, 119], [100, 101], [103, 109], [104, 117], [108, 115], [109, 116], [111, 117]]);;
R:=P177Census(D);;Need(Size(R.F)=240);;
PrintTo("current_c4_descent/120_048.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_048 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
