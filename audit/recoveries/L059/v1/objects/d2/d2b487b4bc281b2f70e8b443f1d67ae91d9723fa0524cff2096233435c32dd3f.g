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
D:=P177Graph("150_008",150,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125],[[1, 31], [1, 46], [1, 138], [1, 144], [2, 32], [2, 47], [2, 139], [2, 145], [3, 33], [3, 48], [3, 140], [3, 141], [4, 34], [4, 49], [4, 136], [4, 142], [5, 35], [5, 50], [5, 137], [5, 143], [6, 26], [6, 36], [6, 143], [6, 149], [7, 27], [7, 37], [7, 144], [7, 150], [8, 28], [8, 38], [8, 145], [8, 146], [9, 29], [9, 39], [9, 141], [9, 147], [10, 30], [10, 40], [10, 142], [10, 148], [11, 31], [11, 41], [11, 129], [11, 148], [12, 32], [12, 42], [12, 130], [12, 149], [13, 33], [13, 43], [13, 126], [13, 150], [14, 34], [14, 44], [14, 127], [14, 146], [15, 35], [15, 45], [15, 128], [15, 147], [16, 36], [16, 46], [16, 128], [16, 134], [17, 37], [17, 47], [17, 129], [17, 135], [18, 38], [18, 48], [18, 130], [18, 131], [19, 39], [19, 49], [19, 126], [19, 132], [20, 40], [20, 50], [20, 127], [20, 133], [21, 26], [21, 41], [21, 133], [21, 139], [22, 27], [22, 42], [22, 134], [22, 140], [23, 28], [23, 43], [23, 135], [23, 136], [24, 29], [24, 44], [24, 131], [24, 137], [25, 30], [25, 45], [25, 132], [25, 138], [26, 53], [26, 54], [27, 54], [27, 55], [28, 51], [28, 55], [29, 51], [29, 52], [30, 52], [30, 53], [31, 58], [31, 59], [32, 59], [32, 60], [33, 56], [33, 60], [34, 56], [34, 57], [35, 57], [35, 58], [36, 63], [36, 64], [37, 64], [37, 65], [38, 61], [38, 65], [39, 61], [39, 62], [40, 62], [40, 63], [41, 68], [41, 69], [42, 69], [42, 70], [43, 66], [43, 70], [44, 66], [44, 67], [45, 67], [45, 68], [46, 73], [46, 74], [47, 74], [47, 75], [48, 71], [48, 75], [49, 71], [49, 72], [50, 72], [50, 73], [51, 82], [51, 100], [52, 83], [52, 96], [53, 84], [53, 97], [54, 85], [54, 98], [55, 81], [55, 99], [56, 80], [56, 87], [57, 76], [57, 88], [58, 77], [58, 89], [59, 78], [59, 90], [60, 79], [60, 86], [61, 85], [61, 92], [62, 81], [62, 93], [63, 82], [63, 94], [64, 83], [64, 95], [65, 84], [65, 91], [66, 90], [66, 97], [67, 86], [67, 98], [68, 87], [68, 99], [69, 88], [69, 100], [70, 89], [70, 96], [71, 77], [71, 95], [72, 78], [72, 91], [73, 79], [73, 92], [74, 80], [74, 93], [75, 76], [75, 94], [76, 111], [76, 116], [77, 112], [77, 117], [78, 113], [78, 118], [79, 114], [79, 119], [80, 115], [80, 120], [81, 116], [81, 121], [82, 117], [82, 122], [83, 118], [83, 123], [84, 119], [84, 124], [85, 120], [85, 125], [86, 101], [86, 121], [87, 102], [87, 122], [88, 103], [88, 123], [89, 104], [89, 124], [90, 105], [90, 125], [91, 101], [91, 106], [92, 102], [92, 107], [93, 103], [93, 108], [94, 104], [94, 109], [95, 105], [95, 110], [96, 106], [96, 111], [97, 107], [97, 112], [98, 108], [98, 113], [99, 109], [99, 114], [100, 110], [100, 115], [101, 127], [101, 130], [102, 126], [102, 128], [103, 127], [103, 129], [104, 128], [104, 130], [105, 126], [105, 129], [106, 132], [106, 135], [107, 131], [107, 133], [108, 132], [108, 134], [109, 133], [109, 135], [110, 131], [110, 134], [111, 137], [111, 140], [112, 136], [112, 138], [113, 137], [113, 139], [114, 138], [114, 140], [115, 136], [115, 139], [116, 142], [116, 145], [117, 141], [117, 143], [118, 142], [118, 144], [119, 143], [119, 145], [120, 141], [120, 144], [121, 147], [121, 150], [122, 146], [122, 148], [123, 147], [123, 149], [124, 148], [124, 150], [125, 146], [125, 149]]);;
R:=P177Census(D);;Need(Size(R.F)=600);;
PrintTo("current_c4_descent/150_008.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 150_008 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
