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
D:=P177Graph("150_012",150,[1, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150],[[1, 2], [1, 3], [1, 4], [1, 5], [2, 141], [2, 145], [2, 147], [3, 140], [3, 143], [3, 148], [4, 142], [4, 144], [4, 150], [5, 139], [5, 146], [5, 149], [6, 44], [6, 45], [6, 64], [6, 65], [7, 46], [7, 47], [7, 66], [7, 67], [8, 48], [8, 52], [8, 56], [8, 60], [9, 51], [9, 54], [9, 59], [9, 61], [10, 50], [10, 55], [10, 57], [10, 63], [11, 49], [11, 53], [11, 58], [11, 62], [12, 32], [12, 38], [12, 50], [12, 68], [13, 33], [13, 37], [13, 51], [13, 69], [14, 35], [14, 36], [14, 49], [14, 71], [15, 34], [15, 39], [15, 48], [15, 70], [16, 28], [16, 43], [16, 60], [16, 67], [17, 30], [17, 42], [17, 61], [17, 66], [18, 31], [18, 41], [18, 63], [18, 65], [19, 29], [19, 40], [19, 62], [19, 64], [20, 28], [20, 37], [20, 40], [20, 46], [21, 30], [21, 39], [21, 41], [21, 47], [22, 31], [22, 36], [22, 43], [22, 44], [23, 29], [23, 38], [23, 42], [23, 45], [24, 31], [24, 33], [24, 35], [24, 129], [25, 28], [25, 32], [25, 33], [25, 132], [26, 29], [26, 32], [26, 34], [26, 131], [27, 30], [27, 34], [27, 35], [27, 130], [28, 77], [29, 80], [30, 79], [31, 78], [32, 87], [33, 88], [34, 85], [35, 86], [36, 82], [36, 109], [37, 84], [37, 110], [38, 83], [38, 111], [39, 81], [39, 112], [40, 87], [40, 108], [41, 86], [41, 107], [42, 85], [42, 105], [43, 88], [43, 106], [44, 92], [44, 93], [45, 89], [45, 96], [46, 91], [46, 95], [47, 90], [47, 94], [48, 90], [48, 102], [49, 92], [49, 104], [50, 89], [50, 103], [51, 91], [51, 101], [52, 81], [52, 97], [52, 106], [53, 82], [53, 98], [53, 108], [54, 84], [54, 99], [54, 105], [55, 83], [55, 100], [55, 107], [56, 77], [56, 99], [56, 110], [57, 78], [57, 98], [57, 109], [58, 80], [58, 100], [58, 111], [59, 79], [59, 97], [59, 112], [60, 73], [60, 93], [61, 74], [61, 96], [62, 76], [62, 95], [63, 75], [63, 94], [64, 73], [64, 104], [65, 74], [65, 103], [66, 76], [66, 101], [67, 75], [67, 102], [68, 77], [68, 85], [68, 102], [69, 78], [69, 87], [69, 103], [70, 80], [70, 86], [70, 104], [71, 79], [71, 88], [71, 101], [72, 73], [72, 74], [72, 75], [72, 76], [73, 126], [74, 125], [75, 128], [76, 127], [77, 117], [78, 120], [79, 119], [80, 118], [81, 120], [81, 133], [82, 117], [82, 134], [83, 119], [83, 136], [84, 118], [84, 135], [85, 121], [86, 122], [87, 124], [88, 123], [89, 121], [89, 131], [90, 122], [90, 130], [91, 124], [91, 132], [92, 123], [92, 129], [93, 125], [93, 137], [94, 127], [94, 138], [95, 128], [95, 138], [96, 126], [96, 137], [97, 126], [97, 136], [98, 127], [98, 133], [99, 125], [99, 134], [100, 128], [100, 135], [101, 114], [102, 116], [103, 115], [104, 113], [105, 114], [105, 119], [106, 116], [106, 117], [107, 115], [107, 120], [108, 113], [108, 118], [109, 114], [109, 121], [110, 115], [110, 122], [111, 116], [111, 123], [112, 113], [112, 124], [113, 147], [114, 148], [115, 150], [116, 149], [117, 143], [118, 144], [119, 146], [120, 145], [121, 143], [122, 144], [123, 146], [124, 145], [125, 150], [126, 147], [127, 148], [128, 149], [129, 139], [129, 141], [130, 139], [130, 142], [131, 140], [131, 142], [132, 140], [132, 141], [133, 143], [133, 147], [134, 144], [134, 148], [135, 146], [135, 150], [136, 145], [136, 149], [137, 141], [137, 142], [138, 139], [138, 140]]);;
R:=P177Census(D);;Need(Size(R.F)=300);;
PrintTo("current_c4_descent/150_012.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 150_012 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
