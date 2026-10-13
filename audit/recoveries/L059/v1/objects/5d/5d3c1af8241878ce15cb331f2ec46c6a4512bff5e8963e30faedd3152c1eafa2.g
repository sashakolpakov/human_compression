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
D:=P177Graph("VT3_224_99",224,[1, 5, 6, 7, 8, 9, 10, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 223, 224],[[1, 2], [1, 3], [1, 4], [2, 5], [2, 6], [3, 7], [3, 9], [4, 8], [4, 10], [5, 11], [5, 13], [6, 12], [6, 14], [7, 15], [7, 19], [8, 16], [8, 20], [9, 17], [9, 21], [10, 18], [10, 22], [11, 23], [11, 27], [12, 24], [12, 28], [13, 25], [13, 29], [14, 26], [14, 30], [15, 31], [15, 39], [16, 32], [16, 40], [17, 33], [17, 41], [18, 34], [18, 42], [19, 35], [19, 43], [20, 36], [20, 44], [21, 37], [21, 45], [22, 38], [22, 46], [23, 47], [23, 55], [24, 48], [24, 56], [25, 49], [25, 57], [26, 50], [26, 58], [27, 51], [27, 59], [28, 52], [28, 60], [29, 53], [29, 61], [30, 54], [30, 62], [31, 63], [31, 79], [32, 64], [32, 80], [33, 65], [33, 81], [34, 66], [34, 82], [35, 67], [35, 83], [36, 68], [36, 84], [37, 69], [37, 85], [38, 70], [38, 86], [39, 71], [39, 87], [40, 72], [40, 88], [41, 73], [41, 89], [42, 74], [42, 90], [43, 75], [43, 91], [44, 76], [44, 92], [45, 77], [45, 93], [46, 78], [46, 94], [47, 95], [47, 111], [48, 96], [48, 112], [49, 97], [49, 113], [50, 98], [50, 114], [51, 99], [51, 115], [52, 100], [52, 116], [53, 101], [53, 117], [54, 102], [54, 118], [55, 103], [55, 119], [56, 104], [56, 120], [57, 105], [57, 121], [58, 106], [58, 122], [59, 107], [59, 123], [60, 108], [60, 124], [61, 109], [61, 125], [62, 110], [62, 126], [63, 115], [63, 127], [64, 105], [64, 144], [65, 128], [65, 145], [66, 100], [66, 146], [67, 129], [67, 131], [68, 98], [68, 130], [69, 113], [69, 140], [70, 107], [70, 131], [71, 132], [71, 144], [72, 111], [72, 133], [73, 96], [73, 147], [74, 126], [74, 128], [75, 102], [75, 134], [76, 120], [76, 135], [77, 135], [77, 148], [78, 117], [78, 149], [79, 104], [79, 136], [80, 137], [80, 138], [81, 101], [81, 138], [82, 119], [82, 134], [83, 95], [83, 150], [84, 125], [84, 127], [85, 110], [85, 151], [86, 139], [86, 152], [87, 114], [87, 141], [88, 108], [88, 140], [89, 123], [89, 153], [90, 141], [90, 154], [91, 121], [91, 142], [92, 143], [92, 150], [93, 116], [93, 139], [94, 106], [94, 147], [95, 155], [96, 172], [97, 156], [97, 173], [98, 174], [99, 157], [99, 159], [100, 158], [101, 168], [102, 159], [103, 160], [103, 172], [104, 161], [105, 175], [106, 156], [107, 162], [108, 163], [109, 163], [109, 176], [110, 177], [111, 164], [112, 165], [112, 166], [113, 166], [114, 162], [115, 178], [116, 155], [117, 179], [118, 167], [118, 180], [119, 169], [120, 168], [121, 181], [122, 169], [122, 182], [123, 170], [124, 171], [124, 178], [125, 167], [126, 175], [127, 183], [128, 186], [129, 177], [129, 192], [130, 165], [130, 184], [131, 193], [132, 180], [132, 187], [133, 179], [133, 185], [134, 168], [135, 187], [136, 182], [136, 186], [137, 158], [137, 188], [138, 189], [139, 184], [140, 162], [141, 190], [142, 170], [142, 195], [143, 171], [143, 190], [144, 191], [145, 173], [145, 193], [146, 174], [146, 192], [147, 183], [148, 181], [148, 185], [149, 157], [149, 194], [150, 194], [151, 161], [151, 188], [152, 160], [152, 189], [153, 176], [153, 191], [154, 164], [154, 195], [155, 196], [156, 199], [157, 205], [158, 197], [159, 206], [160, 200], [161, 198], [163, 200], [164, 199], [165, 201], [166, 202], [167, 197], [169, 203], [170, 208], [171, 203], [172, 204], [173, 206], [174, 205], [175, 196], [176, 198], [177, 207], [178, 207], [179, 201], [180, 202], [181, 204], [182, 208], [183, 196], [184, 211], [185, 214], [186, 209], [187, 213], [188, 212], [189, 210], [190, 212], [191, 211], [192, 213], [193, 214], [194, 209], [195, 210], [197, 217], [198, 220], [199, 215], [200, 219], [201, 218], [202, 216], [203, 218], [204, 217], [205, 219], [206, 220], [207, 215], [208, 216], [209, 217], [210, 222], [211, 215], [212, 221], [213, 222], [214, 221], [216, 224], [218, 223], [219, 224], [220, 223], [221, 224], [222, 223]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_224_99.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_224_99 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
