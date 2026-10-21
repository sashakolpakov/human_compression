Need:=function(ok) if not ok then Error("L059 cubic census invalid"); fi; end;;
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
D:=P177Graph("CSS_182_1",182,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129, 131, 133, 135, 137, 139, 141, 143, 145, 147, 149, 151, 153, 155, 157, 159, 161, 163, 165, 167, 169, 171, 173, 175, 177, 179, 181],[[1, 2], [1, 132], [1, 182], [2, 3], [2, 27], [3, 4], [3, 112], [4, 5], [4, 93], [5, 6], [5, 68], [6, 7], [6, 57], [7, 8], [7, 178], [8, 9], [8, 137], [9, 10], [9, 102], [10, 11], [10, 21], [11, 12], [11, 64], [12, 13], [12, 131], [13, 14], [13, 170], [14, 15], [14, 87], [15, 16], [15, 146], [16, 17], [16, 41], [17, 18], [17, 126], [18, 19], [18, 107], [19, 20], [19, 82], [20, 21], [20, 71], [21, 22], [22, 23], [22, 151], [23, 24], [23, 116], [24, 25], [24, 35], [25, 26], [25, 78], [26, 27], [26, 145], [27, 28], [28, 29], [28, 101], [29, 30], [29, 160], [30, 31], [30, 55], [31, 32], [31, 140], [32, 33], [32, 121], [33, 34], [33, 96], [34, 35], [34, 85], [35, 36], [36, 37], [36, 165], [37, 38], [37, 130], [38, 39], [38, 49], [39, 40], [39, 92], [40, 41], [40, 159], [41, 42], [42, 43], [42, 115], [43, 44], [43, 174], [44, 45], [44, 69], [45, 46], [45, 154], [46, 47], [46, 135], [47, 48], [47, 110], [48, 49], [48, 99], [49, 50], [50, 51], [50, 179], [51, 52], [51, 144], [52, 53], [52, 63], [53, 54], [53, 106], [54, 55], [54, 173], [55, 56], [56, 57], [56, 129], [57, 58], [58, 59], [58, 83], [59, 60], [59, 168], [60, 61], [60, 149], [61, 62], [61, 124], [62, 63], [62, 113], [63, 64], [64, 65], [65, 66], [65, 158], [66, 67], [66, 77], [67, 68], [67, 120], [68, 69], [69, 70], [70, 71], [70, 143], [71, 72], [72, 73], [72, 97], [73, 74], [73, 182], [74, 75], [74, 163], [75, 76], [75, 138], [76, 77], [76, 127], [77, 78], [78, 79], [79, 80], [79, 172], [80, 81], [80, 91], [81, 82], [81, 134], [82, 83], [83, 84], [84, 85], [84, 157], [85, 86], [86, 87], [86, 111], [87, 88], [88, 89], [88, 177], [89, 90], [89, 152], [90, 91], [90, 141], [91, 92], [92, 93], [93, 94], [94, 95], [94, 105], [95, 96], [95, 148], [96, 97], [97, 98], [98, 99], [98, 171], [99, 100], [100, 101], [100, 125], [101, 102], [102, 103], [103, 104], [103, 166], [104, 105], [104, 155], [105, 106], [106, 107], [107, 108], [108, 109], [108, 119], [109, 110], [109, 162], [110, 111], [111, 112], [112, 113], [113, 114], [114, 115], [114, 139], [115, 116], [116, 117], [117, 118], [117, 180], [118, 119], [118, 169], [119, 120], [120, 121], [121, 122], [122, 123], [122, 133], [123, 124], [123, 176], [124, 125], [125, 126], [126, 127], [127, 128], [128, 129], [128, 153], [129, 130], [130, 131], [131, 132], [132, 133], [133, 134], [134, 135], [135, 136], [136, 137], [136, 147], [137, 138], [138, 139], [139, 140], [140, 141], [141, 142], [142, 143], [142, 167], [143, 144], [144, 145], [145, 146], [146, 147], [147, 148], [148, 149], [149, 150], [150, 151], [150, 161], [151, 152], [152, 153], [153, 154], [154, 155], [155, 156], [156, 157], [156, 181], [157, 158], [158, 159], [159, 160], [160, 161], [161, 162], [162, 163], [163, 164], [164, 165], [164, 175], [165, 166], [166, 167], [167, 168], [168, 169], [169, 170], [170, 171], [171, 172], [172, 173], [173, 174], [174, 175], [175, 176], [176, 177], [177, 178], [178, 179], [179, 180], [180, 181], [181, 182]]);;
R:=P177Census(D);;
Need(Size(R.F)=Size(R.A));;
PrintTo("cubic_markings/CSS_182_1.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE CSS_182_1 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
