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
D:=P177Graph("128_036",128,[1, 2, 9, 10, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 27, 28, 31, 32, 37, 38, 39, 40, 43, 44, 49, 50, 57, 58, 63, 64, 65, 66, 67, 68, 81, 82, 83, 84, 91, 92, 93, 94, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 115, 116, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128],[[1, 3], [1, 5], [1, 7], [1, 11], [2, 33], [2, 41], [2, 61], [2, 75], [3, 9], [3, 15], [3, 21], [4, 17], [4, 67], [4, 93], [4, 101], [5, 13], [5, 17], [5, 23], [6, 21], [6, 63], [6, 101], [6, 103], [7, 10], [7, 27], [7, 39], [8, 31], [8, 94], [8, 101], [8, 105], [9, 19], [9, 29], [9, 41], [10, 35], [10, 55], [10, 75], [11, 14], [11, 31], [11, 43], [12, 39], [12, 100], [12, 101], [12, 104], [13, 25], [13, 33], [13, 45], [14, 47], [14, 61], [14, 79], [15, 20], [15, 51], [15, 71], [16, 54], [16, 56], [16, 75], [16, 118], [17, 53], [17, 73], [18, 59], [18, 61], [18, 72], [18, 76], [19, 37], [19, 57], [19, 67], [20, 65], [20, 91], [20, 93], [21, 54], [21, 74], [22, 60], [22, 62], [22, 71], [22, 75], [23, 26], [23, 59], [23, 77], [24, 61], [24, 73], [24, 80], [24, 96], [25, 49], [25, 63], [25, 81], [26, 83], [26, 103], [26, 115], [27, 36], [27, 87], [27, 109], [28, 30], [28, 41], [28, 86], [28, 90], [29, 38], [29, 84], [29, 106], [30, 82], [30, 92], [30, 93], [31, 89], [31, 111], [32, 33], [32, 42], [32, 97], [32, 110], [33, 44], [34, 40], [34, 99], [34, 102], [34, 103], [35, 37], [35, 83], [35, 105], [36, 81], [36, 91], [36, 94], [37, 69], [37, 95], [38, 55], [38, 78], [38, 114], [39, 90], [39, 112], [40, 41], [40, 98], [40, 109], [42, 93], [42, 102], [42, 106], [43, 48], [43, 97], [43, 113], [44, 46], [44, 70], [44, 111], [45, 50], [45, 66], [45, 99], [46, 58], [46, 103], [46, 116], [47, 49], [47, 65], [47, 100], [48, 57], [48, 104], [48, 115], [49, 85], [49, 117], [50, 52], [50, 79], [50, 88], [51, 66], [51, 116], [51, 122], [52, 58], [52, 67], [52, 119], [53, 68], [53, 121], [53, 125], [54, 120], [54, 124], [55, 58], [55, 68], [56, 66], [56, 92], [56, 94], [57, 70], [57, 117], [58, 113], [59, 107], [59, 123], [60, 63], [60, 126], [60, 127], [62, 64], [62, 102], [62, 104], [63, 78], [64, 74], [64, 79], [64, 95], [65, 69], [65, 118], [66, 114], [67, 72], [68, 76], [68, 117], [69, 99], [69, 107], [70, 91], [70, 127], [71, 119], [71, 123], [72, 122], [72, 126], [73, 108], [73, 124], [74, 125], [74, 128], [76, 94], [76, 102], [77, 84], [77, 92], [77, 127], [78, 82], [78, 107], [79, 82], [80, 84], [80, 104], [80, 116], [81, 86], [81, 95], [82, 87], [83, 85], [83, 96], [84, 88], [85, 106], [85, 119], [86, 115], [86, 122], [87, 116], [87, 121], [88, 105], [88, 120], [89, 106], [89, 122], [89, 125], [90, 119], [90, 124], [91, 96], [92, 113], [95, 108], [96, 128], [97, 108], [97, 123], [98, 100], [98, 126], [98, 128], [99, 112], [100, 114], [105, 110], [107, 111], [108, 114], [109, 120], [109, 123], [110, 121], [110, 126], [111, 124], [112, 125], [112, 127], [113, 128], [115, 118], [117, 120], [118, 121]]);;
R:=P177Census(D);;Need(Size(R.F)=2048);;
PrintTo("current_c4_descent/128_036.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_036 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
