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
D:=P177Graph("150_005",150,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135],[[1, 17], [1, 30], [1, 140], [1, 147], [2, 16], [2, 18], [2, 141], [2, 148], [3, 17], [3, 19], [3, 142], [3, 149], [4, 18], [4, 20], [4, 143], [4, 150], [5, 19], [5, 21], [5, 136], [5, 144], [6, 20], [6, 22], [6, 137], [6, 145], [7, 21], [7, 23], [7, 138], [7, 146], [8, 22], [8, 24], [8, 139], [8, 147], [9, 23], [9, 25], [9, 140], [9, 148], [10, 24], [10, 26], [10, 141], [10, 149], [11, 25], [11, 27], [11, 142], [11, 150], [12, 26], [12, 28], [12, 136], [12, 143], [13, 27], [13, 29], [13, 137], [13, 144], [14, 28], [14, 30], [14, 138], [14, 145], [15, 16], [15, 29], [15, 139], [15, 146], [16, 35], [16, 42], [17, 36], [17, 43], [18, 37], [18, 44], [19, 38], [19, 45], [20, 31], [20, 39], [21, 32], [21, 40], [22, 33], [22, 41], [23, 34], [23, 42], [24, 35], [24, 43], [25, 36], [25, 44], [26, 37], [26, 45], [27, 31], [27, 38], [28, 32], [28, 39], [29, 33], [29, 40], [30, 34], [30, 41], [31, 47], [31, 60], [32, 46], [32, 48], [33, 47], [33, 49], [34, 48], [34, 50], [35, 49], [35, 51], [36, 50], [36, 52], [37, 51], [37, 53], [38, 52], [38, 54], [39, 53], [39, 55], [40, 54], [40, 56], [41, 55], [41, 57], [42, 56], [42, 58], [43, 57], [43, 59], [44, 58], [44, 60], [45, 46], [45, 59], [46, 65], [46, 72], [47, 66], [47, 73], [48, 67], [48, 74], [49, 68], [49, 75], [50, 61], [50, 69], [51, 62], [51, 70], [52, 63], [52, 71], [53, 64], [53, 72], [54, 65], [54, 73], [55, 66], [55, 74], [56, 67], [56, 75], [57, 61], [57, 68], [58, 62], [58, 69], [59, 63], [59, 70], [60, 64], [60, 71], [61, 77], [61, 90], [62, 76], [62, 78], [63, 77], [63, 79], [64, 78], [64, 80], [65, 79], [65, 81], [66, 80], [66, 82], [67, 81], [67, 83], [68, 82], [68, 84], [69, 83], [69, 85], [70, 84], [70, 86], [71, 85], [71, 87], [72, 86], [72, 88], [73, 87], [73, 89], [74, 88], [74, 90], [75, 76], [75, 89], [76, 95], [76, 102], [77, 96], [77, 103], [78, 97], [78, 104], [79, 98], [79, 105], [80, 91], [80, 99], [81, 92], [81, 100], [82, 93], [82, 101], [83, 94], [83, 102], [84, 95], [84, 103], [85, 96], [85, 104], [86, 97], [86, 105], [87, 91], [87, 98], [88, 92], [88, 99], [89, 93], [89, 100], [90, 94], [90, 101], [91, 107], [91, 120], [92, 106], [92, 108], [93, 107], [93, 109], [94, 108], [94, 110], [95, 109], [95, 111], [96, 110], [96, 112], [97, 111], [97, 113], [98, 112], [98, 114], [99, 113], [99, 115], [100, 114], [100, 116], [101, 115], [101, 117], [102, 116], [102, 118], [103, 117], [103, 119], [104, 118], [104, 120], [105, 106], [105, 119], [106, 125], [106, 132], [107, 126], [107, 133], [108, 127], [108, 134], [109, 128], [109, 135], [110, 121], [110, 129], [111, 122], [111, 130], [112, 123], [112, 131], [113, 124], [113, 132], [114, 125], [114, 133], [115, 126], [115, 134], [116, 127], [116, 135], [117, 121], [117, 128], [118, 122], [118, 129], [119, 123], [119, 130], [120, 124], [120, 131], [121, 137], [121, 150], [122, 136], [122, 138], [123, 137], [123, 139], [124, 138], [124, 140], [125, 139], [125, 141], [126, 140], [126, 142], [127, 141], [127, 143], [128, 142], [128, 144], [129, 143], [129, 145], [130, 144], [130, 146], [131, 145], [131, 147], [132, 146], [132, 148], [133, 147], [133, 149], [134, 148], [134, 150], [135, 136], [135, 149]]);;
R:=P177Census(D);;Need(Size(R.F)=1200);;
PrintTo("current_c4_descent/150_005.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 150_005 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
