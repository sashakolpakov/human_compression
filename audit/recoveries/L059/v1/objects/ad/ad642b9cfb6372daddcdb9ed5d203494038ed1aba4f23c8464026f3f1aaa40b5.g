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
D:=P177Graph("144_029",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108],[[1, 37], [1, 67], [1, 117], [1, 136], [2, 38], [2, 68], [2, 118], [2, 137], [3, 39], [3, 69], [3, 119], [3, 138], [4, 40], [4, 70], [4, 120], [4, 133], [5, 41], [5, 71], [5, 115], [5, 134], [6, 42], [6, 72], [6, 116], [6, 135], [7, 37], [7, 43], [7, 123], [7, 142], [8, 38], [8, 44], [8, 124], [8, 143], [9, 39], [9, 45], [9, 125], [9, 144], [10, 40], [10, 46], [10, 126], [10, 139], [11, 41], [11, 47], [11, 121], [11, 140], [12, 42], [12, 48], [12, 122], [12, 141], [13, 43], [13, 49], [13, 112], [13, 129], [14, 44], [14, 50], [14, 113], [14, 130], [15, 45], [15, 51], [15, 114], [15, 131], [16, 46], [16, 52], [16, 109], [16, 132], [17, 47], [17, 53], [17, 110], [17, 127], [18, 48], [18, 54], [18, 111], [18, 128], [19, 49], [19, 55], [19, 118], [19, 135], [20, 50], [20, 56], [20, 119], [20, 136], [21, 51], [21, 57], [21, 120], [21, 137], [22, 52], [22, 58], [22, 115], [22, 138], [23, 53], [23, 59], [23, 116], [23, 133], [24, 54], [24, 60], [24, 117], [24, 134], [25, 55], [25, 61], [25, 124], [25, 141], [26, 56], [26, 62], [26, 125], [26, 142], [27, 57], [27, 63], [27, 126], [27, 143], [28, 58], [28, 64], [28, 121], [28, 144], [29, 59], [29, 65], [29, 122], [29, 139], [30, 60], [30, 66], [30, 123], [30, 140], [31, 61], [31, 67], [31, 111], [31, 130], [32, 62], [32, 68], [32, 112], [32, 131], [33, 63], [33, 69], [33, 113], [33, 132], [34, 64], [34, 70], [34, 114], [34, 127], [35, 65], [35, 71], [35, 109], [35, 128], [36, 66], [36, 72], [36, 110], [36, 129], [37, 88], [37, 105], [38, 89], [38, 106], [39, 90], [39, 107], [40, 85], [40, 108], [41, 86], [41, 103], [42, 87], [42, 104], [43, 75], [43, 94], [44, 76], [44, 95], [45, 77], [45, 96], [46, 78], [46, 91], [47, 73], [47, 92], [48, 74], [48, 93], [49, 81], [49, 100], [50, 82], [50, 101], [51, 83], [51, 102], [52, 84], [52, 97], [53, 79], [53, 98], [54, 80], [54, 99], [55, 87], [55, 106], [56, 88], [56, 107], [57, 89], [57, 108], [58, 90], [58, 103], [59, 85], [59, 104], [60, 86], [60, 105], [61, 76], [61, 93], [62, 77], [62, 94], [63, 78], [63, 95], [64, 73], [64, 96], [65, 74], [65, 91], [66, 75], [66, 92], [67, 82], [67, 99], [68, 83], [68, 100], [69, 84], [69, 101], [70, 79], [70, 102], [71, 80], [71, 97], [72, 81], [72, 98], [73, 124], [73, 130], [74, 125], [74, 131], [75, 126], [75, 132], [76, 121], [76, 127], [77, 122], [77, 128], [78, 123], [78, 129], [79, 130], [79, 136], [80, 131], [80, 137], [81, 132], [81, 138], [82, 127], [82, 133], [83, 128], [83, 134], [84, 129], [84, 135], [85, 136], [85, 142], [86, 137], [86, 143], [87, 138], [87, 144], [88, 133], [88, 139], [89, 134], [89, 140], [90, 135], [90, 141], [91, 112], [91, 142], [92, 113], [92, 143], [93, 114], [93, 144], [94, 109], [94, 139], [95, 110], [95, 140], [96, 111], [96, 141], [97, 112], [97, 118], [98, 113], [98, 119], [99, 114], [99, 120], [100, 109], [100, 115], [101, 110], [101, 116], [102, 111], [102, 117], [103, 118], [103, 124], [104, 119], [104, 125], [105, 120], [105, 126], [106, 115], [106, 121], [107, 116], [107, 122], [108, 117], [108, 123]]);;
R:=P177Census(D);;Need(Size(R.F)=1152);;
PrintTo("current_c4_descent/144_029.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_029 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
