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
D:=P177Graph("VT3_256_134",256,[1, 2, 4, 7, 13, 14, 15, 16, 17, 18, 20, 21, 24, 27, 29, 30, 31, 32, 33, 35, 36, 39, 40, 42, 47, 49, 50, 51, 52, 55, 57, 59, 60, 61, 63, 64, 66, 67, 68, 69, 71, 73, 74, 76, 77, 80, 81, 82, 83, 87, 88, 90, 91, 92, 93, 94, 95, 99, 102, 103, 105, 110, 115, 117, 120, 122, 124, 132, 134, 135, 136, 141, 146, 148, 149, 150, 151, 153, 155, 157, 159, 160, 161, 163, 164, 169, 172, 173, 175, 181, 183, 186, 189, 190, 191, 194, 198, 199, 201, 204, 205, 207, 210, 211, 212, 220, 221, 222, 223, 224, 226, 227, 229, 232, 234, 235, 240, 241, 242, 244, 245, 247, 249, 250, 251, 253, 254, 255],[[1, 46], [1, 56], [1, 238], [2, 118], [2, 128], [2, 170], [3, 71], [3, 76], [3, 244], [4, 48], [4, 62], [4, 139], [5, 16], [5, 59], [5, 201], [6, 169], [6, 199], [6, 211], [7, 108], [7, 129], [7, 228], [8, 115], [8, 149], [8, 199], [9, 29], [9, 31], [9, 49], [10, 55], [10, 153], [10, 253], [11, 16], [11, 161], [11, 163], [12, 40], [12, 71], [12, 95], [13, 142], [13, 176], [13, 182], [14, 100], [14, 203], [14, 236], [15, 58], [15, 192], [15, 193], [16, 233], [17, 139], [17, 185], [17, 246], [18, 133], [18, 166], [18, 246], [19, 146], [19, 148], [19, 172], [20, 45], [20, 75], [20, 206], [21, 111], [21, 195], [21, 228], [22, 91], [22, 102], [22, 249], [23, 47], [23, 73], [23, 254], [24, 133], [24, 218], [24, 231], [25, 33], [25, 102], [25, 115], [26, 67], [26, 103], [26, 141], [27, 79], [27, 158], [27, 177], [28, 69], [28, 93], [28, 212], [29, 179], [29, 252], [30, 65], [30, 137], [30, 256], [31, 152], [31, 215], [32, 46], [32, 106], [32, 113], [33, 41], [33, 123], [34, 60], [34, 82], [34, 226], [35, 123], [35, 193], [35, 219], [36, 43], [36, 114], [36, 209], [37, 164], [37, 169], [37, 186], [38, 83], [38, 93], [38, 232], [39, 142], [39, 215], [39, 256], [40, 127], [40, 144], [41, 90], [41, 117], [42, 46], [42, 104], [42, 236], [43, 224], [43, 251], [44, 110], [44, 120], [44, 160], [45, 105], [45, 189], [47, 96], [47, 170], [48, 124], [48, 198], [49, 86], [49, 217], [50, 126], [50, 145], [50, 166], [51, 106], [51, 230], [51, 237], [52, 152], [52, 167], [52, 225], [53, 94], [53, 175], [53, 240], [54, 161], [54, 210], [54, 244], [55, 97], [55, 182], [56, 175], [56, 221], [57, 70], [57, 106], [57, 185], [58, 73], [58, 99], [59, 197], [59, 238], [60, 84], [60, 168], [61, 119], [61, 165], [61, 228], [62, 210], [62, 235], [63, 158], [63, 180], [63, 196], [64, 128], [64, 154], [64, 197], [65, 136], [65, 226], [66, 128], [66, 130], [66, 177], [67, 121], [67, 208], [68, 126], [68, 154], [68, 192], [69, 70], [69, 123], [70, 242], [71, 230], [72, 135], [72, 222], [72, 227], [73, 75], [74, 143], [74, 213], [74, 230], [75, 155], [76, 174], [76, 193], [77, 78], [77, 107], [77, 237], [78, 222], [78, 250], [79, 88], [79, 150], [80, 104], [80, 125], [80, 142], [81, 165], [81, 196], [81, 219], [82, 113], [82, 180], [83, 116], [83, 239], [84, 135], [84, 194], [85, 169], [85, 183], [85, 194], [86, 141], [86, 160], [87, 119], [87, 125], [87, 127], [88, 104], [88, 206], [89, 148], [89, 159], [89, 186], [90, 109], [90, 177], [91, 108], [91, 113], [92, 98], [92, 101], [92, 114], [93, 200], [94, 143], [94, 184], [95, 178], [95, 187], [96, 190], [96, 226], [97, 110], [97, 247], [98, 163], [98, 241], [99, 179], [99, 216], [100, 122], [100, 234], [101, 105], [101, 212], [102, 156], [103, 156], [103, 233], [105, 188], [107, 149], [107, 224], [108, 134], [109, 151], [109, 245], [110, 162], [111, 161], [111, 255], [112, 134], [112, 227], [112, 232], [114, 207], [115, 203], [116, 120], [116, 198], [117, 137], [117, 171], [118, 220], [118, 253], [119, 146], [120, 131], [121, 132], [121, 232], [122, 174], [122, 217], [124, 187], [124, 188], [125, 205], [126, 146], [127, 141], [129, 151], [129, 181], [130, 132], [130, 234], [131, 190], [131, 201], [132, 143], [133, 194], [134, 182], [135, 187], [136, 145], [136, 214], [137, 189], [138, 191], [138, 211], [138, 221], [139, 151], [140, 204], [140, 244], [140, 249], [144, 229], [144, 245], [145, 157], [147, 212], [147, 223], [147, 253], [148, 213], [149, 243], [150, 166], [150, 200], [152, 222], [153, 174], [153, 214], [154, 235], [155, 162], [155, 231], [156, 157], [157, 248], [158, 247], [159, 179], [159, 180], [160, 171], [162, 240], [163, 168], [164, 197], [164, 202], [165, 191], [167, 172], [167, 223], [168, 234], [170, 205], [171, 183], [172, 203], [173, 178], [173, 202], [173, 248], [175, 252], [176, 199], [176, 241], [178, 247], [181, 184], [181, 225], [183, 195], [184, 207], [185, 254], [186, 239], [188, 191], [189, 213], [190, 225], [192, 227], [195, 220], [196, 224], [198, 236], [200, 255], [201, 219], [202, 242], [204, 209], [204, 239], [205, 209], [206, 250], [207, 248], [208, 211], [208, 254], [210, 256], [214, 221], [215, 242], [216, 241], [216, 245], [217, 251], [218, 223], [218, 229], [220, 237], [229, 238], [231, 249], [233, 250], [235, 243], [240, 243], [246, 251], [252, 255]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_256_134.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_256_134 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
