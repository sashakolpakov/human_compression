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
D:=P177Graph("VT3_256_45",256,[1, 3, 5, 6, 7, 8, 9, 11, 12, 13, 15, 17, 18, 19, 20, 22, 23, 28, 29, 31, 37, 39, 40, 44, 45, 47, 49, 53, 54, 58, 62, 63, 65, 67, 68, 69, 70, 72, 76, 77, 78, 81, 83, 84, 85, 87, 92, 96, 97, 101, 103, 104, 105, 106, 107, 108, 109, 112, 113, 116, 119, 120, 122, 123, 125, 127, 128, 129, 130, 138, 140, 142, 143, 144, 145, 146, 149, 153, 158, 159, 160, 161, 164, 165, 169, 172, 173, 175, 178, 181, 183, 185, 186, 187, 188, 189, 190, 192, 194, 195, 196, 199, 204, 205, 209, 210, 211, 213, 214, 220, 221, 223, 228, 229, 232, 235, 236, 239, 240, 242, 244, 245, 247, 249, 251, 252, 254, 255],[[1, 24], [1, 89], [1, 133], [2, 85], [2, 164], [2, 173], [3, 171], [3, 202], [3, 203], [4, 47], [4, 140], [4, 195], [5, 98], [5, 215], [5, 216], [6, 95], [6, 202], [6, 206], [7, 79], [7, 180], [7, 226], [8, 137], [8, 248], [8, 256], [9, 82], [9, 171], [9, 212], [10, 53], [10, 54], [10, 116], [11, 42], [11, 132], [11, 203], [12, 34], [12, 118], [12, 215], [13, 48], [13, 50], [13, 59], [14, 96], [14, 142], [14, 235], [15, 99], [15, 168], [15, 225], [16, 62], [16, 104], [16, 178], [17, 136], [17, 200], [17, 225], [18, 41], [18, 46], [18, 225], [19, 27], [19, 124], [19, 134], [20, 41], [20, 114], [20, 132], [21, 23], [21, 70], [21, 127], [22, 42], [22, 91], [22, 230], [23, 154], [23, 156], [24, 138], [24, 173], [25, 76], [25, 78], [25, 109], [26, 125], [26, 173], [26, 244], [27, 140], [27, 161], [28, 147], [28, 184], [28, 216], [29, 36], [29, 74], [29, 167], [30, 31], [30, 195], [30, 255], [31, 114], [31, 208], [32, 67], [32, 186], [32, 214], [33, 159], [33, 228], [33, 245], [34, 175], [34, 211], [35, 76], [35, 83], [35, 123], [36, 49], [36, 113], [37, 89], [37, 207], [37, 256], [38, 107], [38, 159], [38, 229], [39, 90], [39, 135], [39, 148], [40, 133], [40, 162], [40, 250], [41, 49], [42, 123], [43, 53], [43, 125], [43, 158], [44, 75], [44, 163], [44, 243], [45, 51], [45, 177], [45, 184], [46, 83], [46, 204], [47, 156], [47, 180], [48, 107], [48, 188], [49, 241], [50, 158], [50, 178], [51, 104], [51, 247], [52, 65], [52, 140], [52, 143], [53, 163], [54, 111], [54, 200], [55, 84], [55, 252], [55, 255], [56, 63], [56, 158], [56, 242], [57, 58], [57, 119], [57, 143], [58, 61], [58, 73], [59, 96], [59, 194], [60, 87], [60, 97], [60, 149], [61, 87], [61, 138], [62, 98], [62, 131], [63, 64], [63, 136], [64, 65], [64, 145], [65, 98], [66, 68], [66, 120], [66, 228], [67, 151], [67, 206], [68, 141], [68, 198], [69, 91], [69, 124], [69, 246], [70, 89], [70, 115], [71, 106], [71, 112], [71, 213], [72, 93], [72, 208], [72, 234], [73, 235], [73, 242], [74, 112], [74, 165], [75, 128], [75, 199], [76, 139], [77, 110], [77, 136], [77, 150], [78, 95], [78, 226], [79, 159], [79, 232], [80, 112], [80, 190], [80, 249], [81, 86], [81, 182], [81, 218], [82, 236], [82, 247], [83, 179], [84, 100], [84, 226], [85, 95], [85, 237], [86, 232], [86, 251], [87, 206], [88, 109], [88, 142], [88, 165], [90, 165], [90, 204], [91, 188], [92, 157], [92, 248], [92, 253], [93, 130], [93, 175], [94, 101], [94, 175], [94, 239], [96, 174], [97, 126], [97, 201], [99, 169], [99, 192], [100, 183], [100, 204], [101, 224], [101, 256], [102, 130], [102, 194], [102, 228], [103, 111], [103, 126], [103, 191], [104, 246], [105, 118], [105, 219], [105, 231], [106, 174], [106, 246], [107, 139], [108, 207], [108, 234], [108, 241], [109, 157], [110, 119], [110, 210], [111, 129], [113, 233], [113, 238], [114, 145], [115, 143], [115, 240], [116, 177], [116, 193], [117, 153], [117, 196], [117, 254], [118, 247], [119, 162], [120, 182], [120, 222], [121, 129], [121, 190], [121, 254], [122, 177], [122, 197], [122, 227], [123, 167], [124, 223], [125, 168], [126, 210], [127, 134], [127, 152], [128, 227], [128, 238], [129, 238], [130, 176], [131, 235], [131, 249], [132, 161], [133, 192], [134, 160], [135, 205], [135, 220], [137, 221], [137, 244], [138, 157], [139, 244], [141, 172], [141, 188], [142, 151], [144, 155], [144, 218], [144, 224], [145, 166], [146, 148], [146, 152], [146, 241], [147, 183], [147, 251], [148, 192], [149, 212], [149, 250], [150, 161], [150, 172], [151, 252], [152, 213], [153, 167], [153, 248], [154, 199], [154, 245], [155, 209], [155, 240], [156, 189], [160, 162], [160, 198], [163, 229], [164, 193], [164, 212], [166, 185], [166, 211], [168, 185], [169, 193], [169, 231], [170, 196], [170, 236], [170, 239], [171, 223], [172, 179], [174, 220], [176, 205], [176, 252], [178, 217], [179, 232], [180, 209], [181, 201], [181, 203], [181, 233], [182, 210], [183, 231], [184, 190], [185, 207], [186, 208], [186, 233], [187, 219], [187, 222], [187, 250], [189, 197], [189, 237], [191, 214], [191, 242], [194, 243], [195, 202], [196, 201], [197, 223], [198, 220], [199, 234], [200, 251], [205, 219], [209, 216], [211, 217], [213, 227], [214, 243], [215, 255], [217, 221], [218, 254], [221, 230], [222, 239], [224, 245], [229, 237], [230, 236], [240, 253], [249, 253]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_256_45.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_256_45 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
