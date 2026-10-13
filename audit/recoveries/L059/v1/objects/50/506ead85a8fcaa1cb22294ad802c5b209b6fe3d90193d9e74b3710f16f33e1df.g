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
D:=P177Graph("130_006",130,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117],[[1, 15], [1, 26], [1, 123], [1, 126], [2, 14], [2, 16], [2, 124], [2, 127], [3, 15], [3, 17], [3, 125], [3, 128], [4, 16], [4, 18], [4, 126], [4, 129], [5, 17], [5, 19], [5, 127], [5, 130], [6, 18], [6, 20], [6, 118], [6, 128], [7, 19], [7, 21], [7, 119], [7, 129], [8, 20], [8, 22], [8, 120], [8, 130], [9, 21], [9, 23], [9, 118], [9, 121], [10, 22], [10, 24], [10, 119], [10, 122], [11, 23], [11, 25], [11, 120], [11, 123], [12, 24], [12, 26], [12, 121], [12, 124], [13, 14], [13, 25], [13, 122], [13, 125], [14, 32], [14, 35], [15, 33], [15, 36], [16, 34], [16, 37], [17, 35], [17, 38], [18, 36], [18, 39], [19, 27], [19, 37], [20, 28], [20, 38], [21, 29], [21, 39], [22, 27], [22, 30], [23, 28], [23, 31], [24, 29], [24, 32], [25, 30], [25, 33], [26, 31], [26, 34], [27, 41], [27, 52], [28, 40], [28, 42], [29, 41], [29, 43], [30, 42], [30, 44], [31, 43], [31, 45], [32, 44], [32, 46], [33, 45], [33, 47], [34, 46], [34, 48], [35, 47], [35, 49], [36, 48], [36, 50], [37, 49], [37, 51], [38, 50], [38, 52], [39, 40], [39, 51], [40, 58], [40, 61], [41, 59], [41, 62], [42, 60], [42, 63], [43, 61], [43, 64], [44, 62], [44, 65], [45, 53], [45, 63], [46, 54], [46, 64], [47, 55], [47, 65], [48, 53], [48, 56], [49, 54], [49, 57], [50, 55], [50, 58], [51, 56], [51, 59], [52, 57], [52, 60], [53, 67], [53, 78], [54, 66], [54, 68], [55, 67], [55, 69], [56, 68], [56, 70], [57, 69], [57, 71], [58, 70], [58, 72], [59, 71], [59, 73], [60, 72], [60, 74], [61, 73], [61, 75], [62, 74], [62, 76], [63, 75], [63, 77], [64, 76], [64, 78], [65, 66], [65, 77], [66, 84], [66, 87], [67, 85], [67, 88], [68, 86], [68, 89], [69, 87], [69, 90], [70, 88], [70, 91], [71, 79], [71, 89], [72, 80], [72, 90], [73, 81], [73, 91], [74, 79], [74, 82], [75, 80], [75, 83], [76, 81], [76, 84], [77, 82], [77, 85], [78, 83], [78, 86], [79, 93], [79, 104], [80, 92], [80, 94], [81, 93], [81, 95], [82, 94], [82, 96], [83, 95], [83, 97], [84, 96], [84, 98], [85, 97], [85, 99], [86, 98], [86, 100], [87, 99], [87, 101], [88, 100], [88, 102], [89, 101], [89, 103], [90, 102], [90, 104], [91, 92], [91, 103], [92, 110], [92, 113], [93, 111], [93, 114], [94, 112], [94, 115], [95, 113], [95, 116], [96, 114], [96, 117], [97, 105], [97, 115], [98, 106], [98, 116], [99, 107], [99, 117], [100, 105], [100, 108], [101, 106], [101, 109], [102, 107], [102, 110], [103, 108], [103, 111], [104, 109], [104, 112], [105, 119], [105, 130], [106, 118], [106, 120], [107, 119], [107, 121], [108, 120], [108, 122], [109, 121], [109, 123], [110, 122], [110, 124], [111, 123], [111, 125], [112, 124], [112, 126], [113, 125], [113, 127], [114, 126], [114, 128], [115, 127], [115, 129], [116, 128], [116, 130], [117, 118], [117, 129]]);;
R:=P177Census(D);;Need(Size(R.F)=520);;
PrintTo("current_c4_descent/130_006.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 130_006 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
