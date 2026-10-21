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
D:=P177Graph("144_034",144,[1, 2, 3, 13, 14, 15, 19, 20, 21, 22, 23, 24, 25, 26, 27, 31, 32, 33, 34, 35, 36, 37, 38, 39, 43, 44, 45, 49, 50, 51, 58, 59, 60, 64, 65, 66, 79, 80, 81, 88, 89, 90, 94, 95, 96, 97, 98, 99, 100, 101, 102, 106, 107, 108, 115, 116, 117, 118, 119, 120, 127, 128, 129, 136, 137, 138, 139, 140, 141, 142, 143, 144],[[1, 4], [1, 7], [1, 10], [1, 16], [2, 52], [2, 84], [2, 105], [2, 131], [3, 63], [3, 72], [3, 92], [3, 126], [4, 13], [4, 22], [4, 31], [5, 25], [5, 45], [5, 127], [5, 136], [6, 50], [6, 108], [6, 117], [6, 144], [7, 19], [7, 25], [7, 34], [8, 49], [8, 94], [8, 138], [8, 140], [9, 33], [9, 39], [9, 66], [9, 116], [10, 14], [10, 32], [10, 43], [11, 24], [11, 49], [11, 117], [11, 143], [12, 26], [12, 107], [12, 128], [12, 136], [13, 28], [13, 46], [13, 61], [14, 55], [14, 85], [14, 103], [15, 82], [15, 121], [15, 124], [15, 135], [16, 37], [16, 49], [16, 64], [17, 25], [17, 96], [17, 116], [17, 139], [18, 21], [18, 33], [18, 36], [18, 138], [19, 40], [19, 52], [19, 67], [20, 78], [20, 91], [20, 113], [20, 132], [21, 71], [21, 75], [21, 111], [22, 29], [22, 57], [22, 62], [23, 48], [23, 84], [23, 124], [23, 134], [24, 86], [24, 103], [24, 122], [25, 82], [26, 72], [26, 91], [26, 125], [27, 53], [27, 62], [27, 103], [27, 131], [28, 58], [28, 88], [28, 106], [29, 97], [29, 120], [29, 128], [30, 43], [30, 79], [30, 102], [30, 142], [31, 70], [31, 84], [31, 93], [32, 54], [32, 126], [32, 132], [33, 63], [33, 105], [34, 73], [34, 91], [34, 109], [35, 52], [35, 71], [35, 77], [35, 112], [36, 42], [36, 69], [36, 132], [37, 72], [37, 76], [37, 112], [38, 42], [38, 68], [38, 93], [38, 130], [39, 53], [39, 73], [39, 110], [40, 60], [40, 79], [40, 94], [41, 65], [41, 90], [41, 120], [41, 139], [42, 98], [42, 101], [43, 56], [43, 104], [44, 82], [44, 87], [44, 123], [44, 126], [45, 47], [45, 61], [45, 133], [46, 59], [46, 99], [46, 107], [47, 90], [47, 101], [47, 142], [48, 80], [48, 119], [48, 128], [49, 124], [50, 52], [50, 83], [50, 130], [51, 61], [51, 71], [51, 92], [51, 104], [53, 65], [53, 115], [54, 95], [54, 136], [54, 140], [55, 89], [55, 100], [55, 106], [56, 81], [56, 118], [56, 144], [57, 60], [57, 98], [57, 129], [58, 69], [58, 112], [58, 123], [59, 74], [59, 78], [59, 86], [60, 110], [60, 133], [61, 115], [62, 138], [62, 144], [63, 108], [63, 127], [64, 74], [64, 111], [64, 130], [65, 67], [65, 72], [66, 78], [66, 93], [66, 114], [67, 99], [67, 100], [68, 88], [68, 94], [68, 119], [69, 81], [69, 139], [70, 95], [70, 117], [70, 139], [71, 137], [73, 88], [73, 118], [74, 81], [74, 141], [75, 95], [75, 99], [75, 102], [76, 96], [76, 98], [76, 102], [77, 90], [77, 118], [77, 140], [78, 79], [79, 121], [80, 85], [80, 110], [80, 112], [81, 134], [82, 137], [83, 106], [83, 116], [83, 129], [84, 142], [85, 101], [85, 108], [86, 90], [86, 129], [87, 99], [87, 119], [87, 144], [88, 122], [89, 111], [89, 113], [89, 133], [91, 117], [92, 94], [92, 141], [93, 137], [95, 110], [96, 113], [96, 131], [97, 109], [97, 114], [97, 123], [98, 135], [100, 114], [100, 134], [101, 109], [102, 122], [103, 137], [104, 116], [104, 128], [105, 107], [105, 143], [106, 125], [107, 135], [108, 121], [109, 141], [111, 120], [113, 119], [114, 140], [115, 124], [115, 132], [118, 135], [120, 121], [122, 127], [123, 143], [125, 138], [125, 142], [126, 129], [127, 134], [130, 136], [131, 141], [133, 143]]);;
R:=P177Census(D);;Need(Size(R.F)=576);;
PrintTo("current_c4_descent/144_034.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_034 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
