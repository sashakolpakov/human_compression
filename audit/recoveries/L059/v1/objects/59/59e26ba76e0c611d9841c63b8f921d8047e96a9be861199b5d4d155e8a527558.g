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
D:=P177Graph("150_007",150,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125],[[1, 31], [1, 46], [1, 132], [1, 150], [2, 32], [2, 47], [2, 133], [2, 146], [3, 33], [3, 48], [3, 134], [3, 147], [4, 34], [4, 49], [4, 135], [4, 148], [5, 35], [5, 50], [5, 131], [5, 149], [6, 26], [6, 36], [6, 130], [6, 137], [7, 27], [7, 37], [7, 126], [7, 138], [8, 28], [8, 38], [8, 127], [8, 139], [9, 29], [9, 39], [9, 128], [9, 140], [10, 30], [10, 40], [10, 129], [10, 136], [11, 31], [11, 41], [11, 135], [11, 142], [12, 32], [12, 42], [12, 131], [12, 143], [13, 33], [13, 43], [13, 132], [13, 144], [14, 34], [14, 44], [14, 133], [14, 145], [15, 35], [15, 45], [15, 134], [15, 141], [16, 36], [16, 46], [16, 140], [16, 147], [17, 37], [17, 47], [17, 136], [17, 148], [18, 38], [18, 48], [18, 137], [18, 149], [19, 39], [19, 49], [19, 138], [19, 150], [20, 40], [20, 50], [20, 139], [20, 146], [21, 26], [21, 41], [21, 127], [21, 145], [22, 27], [22, 42], [22, 128], [22, 141], [23, 28], [23, 43], [23, 129], [23, 142], [24, 29], [24, 44], [24, 130], [24, 143], [25, 30], [25, 45], [25, 126], [25, 144], [26, 52], [26, 55], [27, 51], [27, 53], [28, 52], [28, 54], [29, 53], [29, 55], [30, 51], [30, 54], [31, 57], [31, 60], [32, 56], [32, 58], [33, 57], [33, 59], [34, 58], [34, 60], [35, 56], [35, 59], [36, 62], [36, 65], [37, 61], [37, 63], [38, 62], [38, 64], [39, 63], [39, 65], [40, 61], [40, 64], [41, 67], [41, 70], [42, 66], [42, 68], [43, 67], [43, 69], [44, 68], [44, 70], [45, 66], [45, 69], [46, 72], [46, 75], [47, 71], [47, 73], [48, 72], [48, 74], [49, 73], [49, 75], [50, 71], [50, 74], [51, 82], [51, 100], [52, 83], [52, 96], [53, 84], [53, 97], [54, 85], [54, 98], [55, 81], [55, 99], [56, 80], [56, 87], [57, 76], [57, 88], [58, 77], [58, 89], [59, 78], [59, 90], [60, 79], [60, 86], [61, 85], [61, 92], [62, 81], [62, 93], [63, 82], [63, 94], [64, 83], [64, 95], [65, 84], [65, 91], [66, 90], [66, 97], [67, 86], [67, 98], [68, 87], [68, 99], [69, 88], [69, 100], [70, 89], [70, 96], [71, 77], [71, 95], [72, 78], [72, 91], [73, 79], [73, 92], [74, 80], [74, 93], [75, 76], [75, 94], [76, 106], [76, 121], [77, 107], [77, 122], [78, 108], [78, 123], [79, 109], [79, 124], [80, 110], [80, 125], [81, 101], [81, 111], [82, 102], [82, 112], [83, 103], [83, 113], [84, 104], [84, 114], [85, 105], [85, 115], [86, 106], [86, 116], [87, 107], [87, 117], [88, 108], [88, 118], [89, 109], [89, 119], [90, 110], [90, 120], [91, 111], [91, 121], [92, 112], [92, 122], [93, 113], [93, 123], [94, 114], [94, 124], [95, 115], [95, 125], [96, 101], [96, 116], [97, 102], [97, 117], [98, 103], [98, 118], [99, 104], [99, 119], [100, 105], [100, 120], [101, 127], [101, 130], [102, 126], [102, 128], [103, 127], [103, 129], [104, 128], [104, 130], [105, 126], [105, 129], [106, 132], [106, 135], [107, 131], [107, 133], [108, 132], [108, 134], [109, 133], [109, 135], [110, 131], [110, 134], [111, 137], [111, 140], [112, 136], [112, 138], [113, 137], [113, 139], [114, 138], [114, 140], [115, 136], [115, 139], [116, 142], [116, 145], [117, 141], [117, 143], [118, 142], [118, 144], [119, 143], [119, 145], [120, 141], [120, 144], [121, 147], [121, 150], [122, 146], [122, 148], [123, 147], [123, 149], [124, 148], [124, 150], [125, 146], [125, 149]]);;
R:=P177Census(D);;Need(Size(R.F)=600);;
PrintTo("current_c4_descent/150_007.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 150_007 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
