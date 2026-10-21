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
D:=P177Graph("128_041",128,[1, 2, 3, 4, 5, 6, 7, 8, 33, 34, 35, 36, 37, 38, 39, 40, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128],[[1, 9], [1, 17], [1, 25], [1, 41], [2, 48], [2, 69], [2, 97], [2, 109], [3, 24], [3, 93], [3, 104], [3, 108], [4, 16], [4, 32], [4, 68], [4, 92], [5, 14], [5, 30], [5, 65], [5, 89], [6, 21], [6, 96], [6, 102], [6, 106], [7, 45], [7, 72], [7, 99], [7, 111], [8, 11], [8, 20], [8, 27], [8, 44], [9, 33], [9, 53], [9, 73], [10, 57], [10, 80], [10, 85], [10, 121], [11, 84], [11, 117], [11, 128], [12, 40], [12, 52], [12, 64], [12, 116], [13, 38], [13, 50], [13, 61], [13, 113], [14, 82], [14, 120], [14, 126], [15, 60], [15, 77], [15, 87], [15, 123], [16, 35], [16, 55], [16, 76], [17, 49], [17, 57], [17, 81], [18, 37], [18, 73], [18, 88], [18, 117], [19, 56], [19, 80], [19, 116], [19, 125], [20, 36], [20, 64], [20, 124], [21, 33], [21, 62], [21, 121], [22, 53], [22, 78], [22, 114], [22, 128], [23, 40], [23, 75], [23, 85], [23, 119], [24, 52], [24, 59], [24, 84], [25, 34], [25, 54], [25, 73], [26, 57], [26, 80], [26, 86], [26, 122], [27, 83], [27, 117], [27, 127], [28, 39], [28, 51], [28, 64], [28, 116], [29, 37], [29, 49], [29, 61], [29, 113], [30, 81], [30, 120], [30, 125], [31, 60], [31, 77], [31, 88], [31, 124], [32, 36], [32, 56], [32, 76], [33, 65], [33, 97], [34, 45], [34, 89], [34, 104], [35, 44], [35, 96], [35, 109], [36, 72], [36, 108], [37, 70], [37, 105], [38, 42], [38, 94], [38, 112], [39, 47], [39, 91], [39, 101], [40, 67], [40, 100], [41, 50], [41, 57], [41, 82], [42, 73], [42, 87], [42, 117], [43, 55], [43, 80], [43, 116], [43, 126], [44, 64], [44, 123], [45, 63], [45, 122], [46, 54], [46, 79], [46, 115], [46, 127], [47, 74], [47, 86], [47, 118], [48, 51], [48, 58], [48, 83], [49, 69], [49, 105], [50, 93], [50, 112], [51, 92], [51, 101], [52, 68], [52, 100], [53, 66], [53, 97], [54, 90], [54, 104], [55, 95], [55, 109], [56, 71], [56, 108], [58, 69], [58, 98], [58, 110], [59, 93], [59, 103], [59, 107], [60, 68], [60, 92], [61, 65], [61, 89], [62, 96], [62, 101], [62, 105], [63, 72], [63, 100], [63, 112], [65, 121], [66, 77], [66, 113], [66, 128], [67, 76], [67, 85], [67, 120], [68, 84], [69, 81], [70, 74], [70, 88], [70, 118], [71, 79], [71, 115], [71, 125], [72, 124], [74, 97], [74, 109], [75, 94], [75, 104], [75, 108], [76, 91], [77, 90], [78, 95], [78, 103], [78, 107], [79, 98], [79, 110], [81, 106], [82, 93], [82, 111], [83, 92], [83, 102], [84, 99], [85, 98], [86, 91], [86, 103], [87, 94], [87, 110], [88, 107], [89, 122], [90, 113], [90, 127], [91, 120], [94, 119], [95, 114], [95, 126], [96, 123], [98, 121], [99, 118], [99, 128], [100, 115], [101, 114], [102, 119], [102, 127], [103, 122], [105, 114], [106, 119], [106, 125], [107, 124], [110, 123], [111, 118], [111, 126], [112, 115]]);;
R:=P177Census(D);;Need(Size(R.F)=512);;
PrintTo("current_c4_descent/128_041.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_041 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
