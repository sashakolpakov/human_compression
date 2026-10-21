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
D:=P177Graph("128_034",128,[1, 2, 9, 10, 13, 14, 15, 16, 17, 18, 21, 22, 23, 24, 27, 28, 31, 32, 37, 38, 39, 40, 43, 44, 49, 50, 57, 58, 63, 64, 65, 66, 67, 68, 81, 82, 85, 86, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 121, 122, 123, 124],[[1, 3], [1, 5], [1, 7], [1, 11], [2, 33], [2, 41], [2, 61], [2, 75], [3, 9], [3, 15], [3, 21], [4, 17], [4, 67], [4, 85], [4, 91], [5, 13], [5, 17], [5, 23], [6, 21], [6, 63], [6, 91], [6, 93], [7, 10], [7, 27], [7, 39], [8, 31], [8, 86], [8, 91], [8, 97], [9, 19], [9, 29], [9, 41], [10, 35], [10, 55], [10, 75], [11, 14], [11, 31], [11, 43], [12, 39], [12, 90], [12, 91], [12, 94], [13, 25], [13, 33], [13, 45], [14, 47], [14, 61], [14, 70], [15, 20], [15, 51], [15, 71], [16, 54], [16, 56], [16, 75], [16, 120], [17, 53], [17, 73], [18, 59], [18, 61], [18, 72], [18, 76], [19, 37], [19, 57], [19, 67], [20, 50], [20, 65], [20, 85], [21, 54], [21, 74], [22, 60], [22, 62], [22, 71], [22, 75], [23, 26], [23, 59], [23, 77], [24, 61], [24, 69], [24, 73], [24, 118], [25, 49], [25, 58], [25, 63], [26, 38], [26, 66], [26, 93], [27, 36], [27, 79], [27, 99], [28, 30], [28, 41], [28, 84], [28, 127], [29, 38], [29, 81], [29, 98], [30, 49], [30, 85], [30, 96], [31, 83], [31, 101], [32, 33], [32, 42], [32, 87], [32, 100], [33, 44], [34, 40], [34, 89], [34, 92], [34, 93], [35, 37], [35, 82], [35, 97], [36, 50], [36, 86], [36, 95], [37, 46], [37, 69], [38, 48], [38, 55], [39, 84], [39, 102], [40, 41], [40, 88], [40, 99], [42, 85], [42, 92], [42, 98], [43, 48], [43, 87], [43, 103], [44, 46], [44, 101], [44, 126], [45, 50], [45, 82], [45, 89], [46, 93], [46, 95], [47, 49], [47, 81], [47, 90], [48, 94], [48, 96], [49, 56], [50, 70], [51, 66], [51, 105], [51, 108], [52, 58], [52, 67], [52, 110], [52, 124], [53, 68], [53, 107], [53, 113], [54, 109], [54, 112], [55, 58], [55, 68], [56, 66], [56, 86], [57, 70], [57, 78], [57, 119], [58, 117], [59, 111], [59, 121], [60, 63], [60, 114], [60, 115], [62, 64], [62, 92], [62, 94], [63, 78], [64, 70], [64, 74], [64, 117], [65, 69], [65, 77], [65, 120], [66, 118], [67, 72], [68, 76], [68, 119], [69, 94], [71, 110], [71, 111], [72, 108], [72, 114], [73, 112], [73, 122], [74, 113], [74, 116], [76, 86], [76, 92], [77, 115], [77, 123], [78, 106], [78, 121], [79, 96], [79, 105], [79, 107], [80, 81], [80, 97], [80, 109], [80, 124], [81, 125], [82, 104], [82, 128], [83, 98], [83, 108], [83, 113], [84, 110], [84, 112], [87, 111], [87, 122], [88, 90], [88, 114], [88, 116], [89, 102], [89, 125], [90, 104], [95, 103], [95, 127], [96, 126], [97, 100], [98, 128], [99, 109], [99, 111], [100, 107], [100, 114], [101, 112], [101, 121], [102, 113], [102, 115], [103, 116], [103, 123], [104, 106], [104, 122], [105, 117], [105, 125], [106, 120], [106, 127], [107, 120], [108, 127], [109, 119], [110, 128], [115, 126], [116, 118], [117, 122], [118, 124], [119, 123], [121, 125], [123, 128], [124, 126]]);;
R:=P177Census(D);;Need(Size(R.F)=1024);;
PrintTo("current_c4_descent/128_034.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_034 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
