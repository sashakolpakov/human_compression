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
D:=P177Graph("128_032",128,[1, 2, 3, 4, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 37, 38, 39, 40, 49, 50, 51, 52, 61, 62, 63, 64, 73, 74, 75, 76, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 105, 106, 107, 108, 109, 110, 111, 112, 121, 122, 123, 124],[[1, 5], [1, 9], [1, 10], [1, 13], [2, 5], [2, 65], [2, 66], [2, 77], [3, 13], [3, 53], [3, 55], [3, 101], [4, 77], [4, 101], [4, 125], [4, 127], [5, 17], [5, 25], [6, 17], [6, 49], [6, 50], [6, 105], [7, 25], [7, 29], [7, 31], [7, 91], [8, 91], [8, 105], [8, 121], [8, 123], [9, 21], [9, 22], [9, 29], [10, 37], [10, 38], [10, 49], [11, 29], [11, 81], [11, 83], [11, 121], [12, 49], [12, 109], [12, 111], [12, 121], [13, 19], [13, 26], [14, 26], [14, 29], [14, 30], [14, 89], [15, 19], [15, 49], [15, 51], [15, 107], [16, 89], [16, 107], [16, 121], [16, 122], [17, 33], [17, 45], [18, 33], [18, 77], [18, 78], [18, 118], [19, 45], [19, 59], [20, 59], [20, 101], [20, 103], [20, 118], [21, 41], [21, 42], [21, 53], [22, 66], [22, 69], [22, 70], [23, 53], [23, 97], [23, 99], [23, 127], [24, 66], [24, 115], [24, 116], [24, 127], [25, 35], [25, 46], [26, 46], [26, 57], [27, 35], [27, 77], [27, 79], [27, 120], [28, 57], [28, 101], [28, 102], [28, 120], [30, 53], [30, 54], [30, 102], [31, 66], [31, 68], [31, 79], [32, 79], [32, 102], [32, 127], [32, 128], [33, 61], [33, 73], [34, 61], [34, 94], [34, 105], [34, 106], [35, 73], [35, 87], [36, 87], [36, 91], [36, 92], [36, 94], [37, 65], [37, 69], [37, 71], [38, 42], [38, 44], [38, 55], [39, 65], [39, 114], [39, 116], [39, 125], [40, 55], [40, 99], [40, 100], [40, 125], [41, 61], [41, 62], [41, 81], [42, 93], [42, 94], [43, 73], [43, 75], [43, 81], [43, 111], [44, 87], [44, 88], [44, 111], [45, 63], [45, 74], [46, 74], [46, 85], [47, 63], [47, 96], [47, 105], [47, 107], [48, 85], [48, 89], [48, 91], [48, 96], [50, 65], [50, 67], [50, 78], [51, 55], [51, 56], [51, 103], [52, 78], [52, 103], [52, 125], [52, 126], [54, 81], [54, 82], [54, 122], [56, 111], [56, 112], [56, 122], [57, 76], [57, 86], [58, 86], [58, 89], [58, 90], [58, 95], [59, 64], [59, 76], [60, 64], [60, 95], [60, 107], [60, 108], [61, 97], [62, 70], [62, 117], [62, 118], [63, 97], [63, 115], [64, 70], [64, 115], [67, 109], [67, 110], [67, 123], [68, 83], [68, 84], [68, 123], [69, 93], [69, 95], [70, 83], [71, 86], [71, 88], [71, 109], [72, 75], [72, 76], [72, 83], [72, 109], [73, 98], [74, 98], [74, 113], [75, 118], [75, 120], [76, 113], [78, 106], [79, 92], [80, 92], [80, 106], [80, 123], [80, 124], [82, 97], [82, 98], [82, 128], [84, 113], [84, 115], [84, 128], [85, 100], [85, 114], [86, 114], [87, 100], [88, 119], [88, 120], [90, 102], [90, 104], [90, 119], [92, 119], [93, 117], [93, 119], [94, 99], [95, 116], [96, 99], [96, 116], [98, 112], [100, 112], [103, 108], [104, 108], [104, 122], [104, 124], [106, 117], [108, 117], [110, 113], [110, 114], [110, 126], [112, 126], [124, 126], [124, 128]]);;
R:=P177Census(D);;Need(Size(R.F)=3072);;
PrintTo("current_c4_descent/128_032.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_032 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
