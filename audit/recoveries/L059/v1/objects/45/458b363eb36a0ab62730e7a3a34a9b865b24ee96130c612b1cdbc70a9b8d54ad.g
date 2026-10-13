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
D:=P177Graph("CSS_216_1",216,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129, 131, 133, 135, 137, 139, 141, 143, 145, 147, 149, 151, 153, 155, 157, 159, 161, 163, 165, 167, 169, 171, 173, 175, 177, 179, 181, 183, 185, 187, 189, 191, 193, 195, 197, 199, 201, 203, 205, 207, 209, 211, 213, 215],[[1, 2], [1, 14], [1, 216], [2, 3], [2, 205], [3, 4], [3, 160], [4, 5], [4, 63], [5, 6], [5, 90], [6, 7], [6, 137], [7, 8], [7, 20], [8, 9], [8, 211], [9, 10], [9, 70], [10, 11], [10, 165], [11, 12], [11, 96], [12, 13], [12, 143], [13, 14], [13, 26], [14, 15], [15, 16], [15, 172], [16, 17], [16, 75], [17, 18], [17, 102], [18, 19], [18, 149], [19, 20], [19, 32], [20, 21], [21, 22], [21, 82], [22, 23], [22, 177], [23, 24], [23, 108], [24, 25], [24, 155], [25, 26], [25, 38], [26, 27], [27, 28], [27, 184], [28, 29], [28, 87], [29, 30], [29, 114], [30, 31], [30, 161], [31, 32], [31, 44], [32, 33], [33, 34], [33, 94], [34, 35], [34, 189], [35, 36], [35, 120], [36, 37], [36, 167], [37, 38], [37, 50], [38, 39], [39, 40], [39, 196], [40, 41], [40, 99], [41, 42], [41, 126], [42, 43], [42, 173], [43, 44], [43, 56], [44, 45], [45, 46], [45, 106], [46, 47], [46, 201], [47, 48], [47, 132], [48, 49], [48, 179], [49, 50], [49, 62], [50, 51], [51, 52], [51, 208], [52, 53], [52, 111], [53, 54], [53, 138], [54, 55], [54, 185], [55, 56], [55, 68], [56, 57], [57, 58], [57, 118], [58, 59], [58, 213], [59, 60], [59, 144], [60, 61], [60, 191], [61, 62], [61, 74], [62, 63], [63, 64], [64, 65], [64, 123], [65, 66], [65, 150], [66, 67], [66, 197], [67, 68], [67, 80], [68, 69], [69, 70], [69, 130], [70, 71], [71, 72], [71, 156], [72, 73], [72, 203], [73, 74], [73, 86], [74, 75], [75, 76], [76, 77], [76, 135], [77, 78], [77, 162], [78, 79], [78, 209], [79, 80], [79, 92], [80, 81], [81, 82], [81, 142], [82, 83], [83, 84], [83, 168], [84, 85], [84, 215], [85, 86], [85, 98], [86, 87], [87, 88], [88, 89], [88, 147], [89, 90], [89, 174], [90, 91], [91, 92], [91, 104], [92, 93], [93, 94], [93, 154], [94, 95], [95, 96], [95, 180], [96, 97], [97, 98], [97, 110], [98, 99], [99, 100], [100, 101], [100, 159], [101, 102], [101, 186], [102, 103], [103, 104], [103, 116], [104, 105], [105, 106], [105, 166], [106, 107], [107, 108], [107, 192], [108, 109], [109, 110], [109, 122], [110, 111], [111, 112], [112, 113], [112, 171], [113, 114], [113, 198], [114, 115], [115, 116], [115, 128], [116, 117], [117, 118], [117, 178], [118, 119], [119, 120], [119, 204], [120, 121], [121, 122], [121, 134], [122, 123], [123, 124], [124, 125], [124, 183], [125, 126], [125, 210], [126, 127], [127, 128], [127, 140], [128, 129], [129, 130], [129, 190], [130, 131], [131, 132], [131, 216], [132, 133], [133, 134], [133, 146], [134, 135], [135, 136], [136, 137], [136, 195], [137, 138], [138, 139], [139, 140], [139, 152], [140, 141], [141, 142], [141, 202], [142, 143], [143, 144], [144, 145], [145, 146], [145, 158], [146, 147], [147, 148], [148, 149], [148, 207], [149, 150], [150, 151], [151, 152], [151, 164], [152, 153], [153, 154], [153, 214], [154, 155], [155, 156], [156, 157], [157, 158], [157, 170], [158, 159], [159, 160], [160, 161], [161, 162], [162, 163], [163, 164], [163, 176], [164, 165], [165, 166], [166, 167], [167, 168], [168, 169], [169, 170], [169, 182], [170, 171], [171, 172], [172, 173], [173, 174], [174, 175], [175, 176], [175, 188], [176, 177], [177, 178], [178, 179], [179, 180], [180, 181], [181, 182], [181, 194], [182, 183], [183, 184], [184, 185], [185, 186], [186, 187], [187, 188], [187, 200], [188, 189], [189, 190], [190, 191], [191, 192], [192, 193], [193, 194], [193, 206], [194, 195], [195, 196], [196, 197], [197, 198], [198, 199], [199, 200], [199, 212], [200, 201], [201, 202], [202, 203], [203, 204], [204, 205], [205, 206], [206, 207], [207, 208], [208, 209], [209, 210], [210, 211], [211, 212], [212, 213], [213, 214], [214, 215], [215, 216]]);;
R:=P177Census(D);;
Need(Size(R.F)=Size(R.A));;
PrintTo("cubic_markings/CSS_216_1.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE CSS_216_1 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
