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
D:=P177Graph("128_035",128,[1, 2, 3, 4, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 41, 42, 43, 44, 49, 50, 51, 52, 57, 58, 59, 60, 77, 78, 79, 80, 93, 94, 95, 96, 101, 102, 103, 104, 105, 106, 107, 108, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124],[[1, 5], [1, 9], [1, 11], [1, 13], [2, 13], [2, 90], [2, 98], [2, 100], [3, 5], [3, 63], [3, 64], [3, 71], [4, 71], [4, 90], [4, 125], [4, 126], [5, 17], [5, 25], [6, 25], [6, 50], [6, 58], [6, 60], [7, 17], [7, 31], [7, 32], [7, 35], [8, 35], [8, 50], [8, 117], [8, 118], [9, 21], [9, 23], [9, 29], [10, 29], [10, 113], [10, 114], [10, 118], [11, 41], [11, 43], [11, 57], [12, 57], [12, 118], [12, 123], [12, 124], [13, 33], [13, 49], [14, 26], [14, 30], [14, 32], [14, 49], [15, 19], [15, 33], [15, 59], [15, 60], [16, 19], [16, 26], [16, 118], [16, 120], [17, 37], [17, 53], [18, 53], [18, 70], [18, 72], [18, 74], [19, 37], [19, 67], [20, 67], [20, 74], [20, 89], [20, 90], [21, 45], [21, 47], [21, 61], [22, 61], [22, 85], [22, 86], [22, 126], [23, 81], [23, 83], [23, 97], [24, 97], [24, 111], [24, 112], [24, 126], [25, 65], [25, 76], [26, 54], [26, 76], [27, 39], [27, 65], [27, 69], [27, 70], [28, 39], [28, 54], [28, 90], [28, 92], [29, 69], [29, 89], [30, 62], [30, 64], [30, 89], [31, 69], [31, 99], [31, 100], [32, 126], [32, 128], [33, 55], [33, 73], [34, 38], [34, 55], [34, 89], [34, 91], [35, 68], [35, 73], [36, 38], [36, 68], [36, 71], [36, 72], [37, 77], [37, 93], [38, 93], [38, 106], [39, 77], [39, 103], [40, 49], [40, 50], [40, 103], [40, 106], [41, 85], [41, 87], [41, 99], [42, 45], [42, 46], [42, 99], [42, 125], [43, 62], [43, 109], [43, 111], [44, 62], [44, 83], [44, 84], [44, 125], [45, 77], [45, 79], [46, 102], [46, 104], [46, 123], [47, 95], [47, 96], [47, 116], [48, 106], [48, 108], [48, 116], [48, 123], [49, 66], [50, 56], [51, 66], [51, 75], [51, 91], [51, 92], [52, 56], [52, 69], [52, 71], [52, 75], [53, 101], [53, 108], [54, 94], [54, 108], [55, 79], [55, 101], [56, 79], [56, 94], [57, 72], [57, 92], [58, 72], [58, 97], [58, 98], [59, 61], [59, 63], [59, 92], [60, 125], [60, 127], [61, 117], [62, 117], [63, 113], [63, 115], [64, 121], [64, 123], [65, 95], [65, 105], [66, 78], [66, 95], [67, 104], [67, 105], [68, 78], [68, 104], [70, 117], [70, 119], [73, 96], [73, 107], [74, 80], [74, 96], [75, 102], [75, 107], [76, 80], [76, 102], [77, 82], [78, 82], [78, 111], [79, 88], [80, 88], [80, 111], [81, 101], [81, 102], [81, 115], [82, 115], [82, 124], [83, 105], [83, 106], [84, 94], [84, 96], [84, 124], [85, 107], [85, 108], [86, 103], [86, 104], [86, 114], [87, 93], [87, 95], [87, 121], [88, 114], [88, 121], [91, 119], [91, 120], [93, 112], [94, 112], [97, 120], [98, 114], [98, 116], [99, 120], [100, 122], [100, 124], [101, 109], [103, 109], [105, 110], [107, 110], [109, 122], [110, 113], [110, 122], [112, 113], [115, 128], [116, 128], [119, 127], [119, 128], [121, 127], [122, 127]]);;
R:=P177Census(D);;Need(Size(R.F)=3072);;
PrintTo("current_c4_descent/128_035.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_035 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
