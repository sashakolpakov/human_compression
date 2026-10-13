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
D:=P177Graph("150_006",150,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125],[[1, 27], [1, 50], [1, 133], [1, 144], [2, 26], [2, 28], [2, 134], [2, 145], [3, 27], [3, 29], [3, 135], [3, 146], [4, 28], [4, 30], [4, 136], [4, 147], [5, 29], [5, 31], [5, 137], [5, 148], [6, 30], [6, 32], [6, 138], [6, 149], [7, 31], [7, 33], [7, 139], [7, 150], [8, 32], [8, 34], [8, 126], [8, 140], [9, 33], [9, 35], [9, 127], [9, 141], [10, 34], [10, 36], [10, 128], [10, 142], [11, 35], [11, 37], [11, 129], [11, 143], [12, 36], [12, 38], [12, 130], [12, 144], [13, 37], [13, 39], [13, 131], [13, 145], [14, 38], [14, 40], [14, 132], [14, 146], [15, 39], [15, 41], [15, 133], [15, 147], [16, 40], [16, 42], [16, 134], [16, 148], [17, 41], [17, 43], [17, 135], [17, 149], [18, 42], [18, 44], [18, 136], [18, 150], [19, 43], [19, 45], [19, 126], [19, 137], [20, 44], [20, 46], [20, 127], [20, 138], [21, 45], [21, 47], [21, 128], [21, 139], [22, 46], [22, 48], [22, 129], [22, 140], [23, 47], [23, 49], [23, 130], [23, 141], [24, 48], [24, 50], [24, 131], [24, 142], [25, 26], [25, 49], [25, 132], [25, 143], [26, 58], [26, 69], [27, 59], [27, 70], [28, 60], [28, 71], [29, 61], [29, 72], [30, 62], [30, 73], [31, 63], [31, 74], [32, 64], [32, 75], [33, 51], [33, 65], [34, 52], [34, 66], [35, 53], [35, 67], [36, 54], [36, 68], [37, 55], [37, 69], [38, 56], [38, 70], [39, 57], [39, 71], [40, 58], [40, 72], [41, 59], [41, 73], [42, 60], [42, 74], [43, 61], [43, 75], [44, 51], [44, 62], [45, 52], [45, 63], [46, 53], [46, 64], [47, 54], [47, 65], [48, 55], [48, 66], [49, 56], [49, 67], [50, 57], [50, 68], [51, 77], [51, 100], [52, 76], [52, 78], [53, 77], [53, 79], [54, 78], [54, 80], [55, 79], [55, 81], [56, 80], [56, 82], [57, 81], [57, 83], [58, 82], [58, 84], [59, 83], [59, 85], [60, 84], [60, 86], [61, 85], [61, 87], [62, 86], [62, 88], [63, 87], [63, 89], [64, 88], [64, 90], [65, 89], [65, 91], [66, 90], [66, 92], [67, 91], [67, 93], [68, 92], [68, 94], [69, 93], [69, 95], [70, 94], [70, 96], [71, 95], [71, 97], [72, 96], [72, 98], [73, 97], [73, 99], [74, 98], [74, 100], [75, 76], [75, 99], [76, 108], [76, 119], [77, 109], [77, 120], [78, 110], [78, 121], [79, 111], [79, 122], [80, 112], [80, 123], [81, 113], [81, 124], [82, 114], [82, 125], [83, 101], [83, 115], [84, 102], [84, 116], [85, 103], [85, 117], [86, 104], [86, 118], [87, 105], [87, 119], [88, 106], [88, 120], [89, 107], [89, 121], [90, 108], [90, 122], [91, 109], [91, 123], [92, 110], [92, 124], [93, 111], [93, 125], [94, 101], [94, 112], [95, 102], [95, 113], [96, 103], [96, 114], [97, 104], [97, 115], [98, 105], [98, 116], [99, 106], [99, 117], [100, 107], [100, 118], [101, 127], [101, 150], [102, 126], [102, 128], [103, 127], [103, 129], [104, 128], [104, 130], [105, 129], [105, 131], [106, 130], [106, 132], [107, 131], [107, 133], [108, 132], [108, 134], [109, 133], [109, 135], [110, 134], [110, 136], [111, 135], [111, 137], [112, 136], [112, 138], [113, 137], [113, 139], [114, 138], [114, 140], [115, 139], [115, 141], [116, 140], [116, 142], [117, 141], [117, 143], [118, 142], [118, 144], [119, 143], [119, 145], [120, 144], [120, 146], [121, 145], [121, 147], [122, 146], [122, 148], [123, 147], [123, 149], [124, 148], [124, 150], [125, 126], [125, 149]]);;
R:=P177Census(D);;Need(Size(R.F)=600);;
PrintTo("current_c4_descent/150_006.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 150_006 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
