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
D:=P177Graph("CSS_240_1",240,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129, 131, 133, 135, 137, 139, 141, 143, 145, 147, 149, 151, 153, 155, 157, 159, 161, 163, 165, 167, 169, 171, 173, 175, 177, 179, 181, 183, 185, 187, 189, 191, 193, 195, 197, 199, 201, 203, 205, 207, 209, 211, 213, 215, 217, 219, 221, 223, 225, 227, 229, 231, 233, 235, 237, 239],[[1, 2], [1, 128], [1, 240], [2, 3], [2, 41], [3, 4], [3, 156], [4, 5], [4, 63], [5, 6], [5, 192], [6, 7], [6, 93], [7, 8], [7, 112], [8, 9], [8, 121], [9, 10], [9, 236], [10, 11], [10, 215], [11, 12], [11, 42], [12, 13], [12, 99], [13, 14], [13, 166], [14, 15], [14, 115], [15, 16], [15, 196], [16, 17], [16, 151], [17, 18], [17, 218], [18, 19], [18, 227], [19, 20], [19, 158], [20, 21], [20, 33], [21, 22], [21, 174], [22, 23], [22, 109], [23, 24], [23, 58], [24, 25], [24, 77], [25, 26], [25, 152], [26, 27], [26, 65], [27, 28], [27, 180], [28, 29], [28, 87], [29, 30], [29, 216], [30, 31], [30, 117], [31, 32], [31, 136], [32, 33], [32, 145], [33, 34], [34, 35], [34, 239], [35, 36], [35, 66], [36, 37], [36, 123], [37, 38], [37, 190], [38, 39], [38, 139], [39, 40], [39, 220], [40, 41], [40, 175], [41, 42], [42, 43], [43, 44], [43, 182], [44, 45], [44, 57], [45, 46], [45, 198], [46, 47], [46, 133], [47, 48], [47, 82], [48, 49], [48, 101], [49, 50], [49, 176], [50, 51], [50, 89], [51, 52], [51, 204], [52, 53], [52, 111], [53, 54], [53, 240], [54, 55], [54, 141], [55, 56], [55, 160], [56, 57], [56, 169], [57, 58], [58, 59], [59, 60], [59, 90], [60, 61], [60, 147], [61, 62], [61, 214], [62, 63], [62, 163], [63, 64], [64, 65], [64, 199], [65, 66], [66, 67], [67, 68], [67, 206], [68, 69], [68, 81], [69, 70], [69, 222], [70, 71], [70, 157], [71, 72], [71, 106], [72, 73], [72, 125], [73, 74], [73, 200], [74, 75], [74, 113], [75, 76], [75, 228], [76, 77], [76, 135], [77, 78], [78, 79], [78, 165], [79, 80], [79, 184], [80, 81], [80, 193], [81, 82], [82, 83], [83, 84], [83, 114], [84, 85], [84, 171], [85, 86], [85, 238], [86, 87], [86, 187], [87, 88], [88, 89], [88, 223], [89, 90], [90, 91], [91, 92], [91, 230], [92, 93], [92, 105], [93, 94], [94, 95], [94, 181], [95, 96], [95, 130], [96, 97], [96, 149], [97, 98], [97, 224], [98, 99], [98, 137], [99, 100], [100, 101], [100, 159], [101, 102], [102, 103], [102, 189], [103, 104], [103, 208], [104, 105], [104, 217], [105, 106], [106, 107], [107, 108], [107, 138], [108, 109], [108, 195], [109, 110], [110, 111], [110, 211], [111, 112], [112, 113], [113, 114], [114, 115], [115, 116], [116, 117], [116, 129], [117, 118], [118, 119], [118, 205], [119, 120], [119, 154], [120, 121], [120, 173], [121, 122], [122, 123], [122, 161], [123, 124], [124, 125], [124, 183], [125, 126], [126, 127], [126, 213], [127, 128], [127, 232], [128, 129], [129, 130], [130, 131], [131, 132], [131, 162], [132, 133], [132, 219], [133, 134], [134, 135], [134, 235], [135, 136], [136, 137], [137, 138], [138, 139], [139, 140], [140, 141], [140, 153], [141, 142], [142, 143], [142, 229], [143, 144], [143, 178], [144, 145], [144, 197], [145, 146], [146, 147], [146, 185], [147, 148], [148, 149], [148, 207], [149, 150], [150, 151], [150, 237], [151, 152], [152, 153], [153, 154], [154, 155], [155, 156], [155, 186], [156, 157], [157, 158], [158, 159], [159, 160], [160, 161], [161, 162], [162, 163], [163, 164], [164, 165], [164, 177], [165, 166], [166, 167], [167, 168], [167, 202], [168, 169], [168, 221], [169, 170], [170, 171], [170, 209], [171, 172], [172, 173], [172, 231], [173, 174], [174, 175], [175, 176], [176, 177], [177, 178], [178, 179], [179, 180], [179, 210], [180, 181], [181, 182], [182, 183], [183, 184], [184, 185], [185, 186], [186, 187], [187, 188], [188, 189], [188, 201], [189, 190], [190, 191], [191, 192], [191, 226], [192, 193], [193, 194], [194, 195], [194, 233], [195, 196], [196, 197], [197, 198], [198, 199], [199, 200], [200, 201], [201, 202], [202, 203], [203, 204], [203, 234], [204, 205], [205, 206], [206, 207], [207, 208], [208, 209], [209, 210], [210, 211], [211, 212], [212, 213], [212, 225], [213, 214], [214, 215], [215, 216], [216, 217], [217, 218], [218, 219], [219, 220], [220, 221], [221, 222], [222, 223], [223, 224], [224, 225], [225, 226], [226, 227], [227, 228], [228, 229], [229, 230], [230, 231], [231, 232], [232, 233], [233, 234], [234, 235], [235, 236], [236, 237], [237, 238], [238, 239], [239, 240]]);;
R:=P177Census(D);;
Need(Size(R.F)=Size(R.A));;
PrintTo("cubic_markings/CSS_240_1.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE CSS_240_1 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
