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
D:=P177Graph("VT3_256_21",256,[1, 3, 5, 8, 13, 14, 17, 20, 21, 24, 25, 26, 27, 28, 29, 32, 33, 35, 37, 38, 40, 41, 42, 46, 49, 51, 53, 55, 56, 57, 62, 64, 68, 70, 71, 73, 74, 75, 76, 78, 81, 83, 85, 86, 88, 89, 90, 92, 93, 94, 95, 99, 100, 101, 104, 106, 109, 110, 112, 113, 114, 115, 117, 118, 119, 120, 126, 128, 130, 137, 139, 140, 142, 145, 149, 150, 152, 154, 157, 158, 160, 162, 163, 165, 166, 168, 169, 170, 173, 177, 179, 186, 187, 189, 190, 191, 192, 202, 205, 209, 210, 211, 212, 213, 214, 217, 218, 219, 220, 222, 223, 224, 226, 227, 231, 232, 235, 236, 237, 241, 243, 245, 246, 248, 250, 252, 253, 255],[[1, 50], [1, 182], [1, 183], [2, 42], [2, 81], [2, 202], [3, 45], [3, 67], [3, 127], [4, 74], [4, 117], [4, 232], [5, 18], [5, 141], [5, 171], [6, 85], [6, 99], [6, 227], [7, 190], [7, 212], [7, 253], [8, 43], [8, 47], [8, 251], [9, 35], [9, 85], [9, 237], [10, 13], [10, 114], [10, 179], [11, 28], [11, 113], [11, 119], [12, 21], [12, 101], [12, 223], [13, 48], [13, 121], [14, 182], [14, 215], [14, 242], [15, 41], [15, 126], [15, 168], [16, 21], [16, 154], [16, 168], [17, 102], [17, 204], [17, 207], [18, 128], [18, 211], [19, 109], [19, 128], [19, 190], [20, 58], [20, 136], [20, 199], [21, 52], [22, 115], [22, 158], [22, 191], [23, 75], [23, 149], [23, 150], [24, 197], [24, 206], [24, 221], [25, 59], [25, 84], [25, 148], [26, 44], [26, 111], [26, 122], [27, 131], [27, 167], [27, 194], [28, 161], [28, 182], [29, 79], [29, 156], [29, 200], [30, 35], [30, 113], [30, 187], [31, 56], [31, 113], [31, 160], [32, 144], [32, 229], [32, 240], [33, 69], [33, 176], [33, 234], [34, 56], [34, 64], [34, 130], [35, 61], [36, 104], [36, 118], [36, 162], [37, 121], [37, 147], [37, 194], [38, 97], [38, 133], [38, 180], [39, 49], [39, 189], [39, 202], [40, 45], [40, 66], [40, 183], [41, 196], [41, 233], [42, 69], [42, 155], [43, 119], [43, 163], [44, 55], [44, 166], [45, 152], [46, 96], [46, 103], [46, 151], [47, 110], [47, 189], [48, 78], [48, 241], [49, 121], [49, 188], [50, 86], [50, 126], [51, 183], [51, 201], [51, 221], [52, 142], [52, 255], [53, 72], [53, 77], [53, 141], [54, 62], [54, 71], [54, 165], [55, 105], [55, 225], [56, 201], [57, 103], [57, 188], [57, 254], [58, 95], [58, 186], [59, 120], [59, 217], [60, 70], [60, 222], [60, 253], [61, 71], [61, 139], [62, 153], [62, 174], [63, 177], [63, 231], [63, 253], [64, 176], [64, 185], [65, 179], [65, 192], [65, 226], [66, 73], [66, 154], [67, 130], [67, 202], [68, 97], [68, 132], [68, 195], [69, 149], [70, 105], [70, 132], [71, 207], [72, 88], [72, 250], [73, 151], [73, 159], [74, 77], [74, 124], [75, 127], [75, 184], [76, 129], [76, 178], [76, 208], [77, 226], [78, 124], [78, 203], [79, 86], [79, 170], [80, 92], [80, 95], [80, 137], [81, 123], [81, 131], [82, 94], [82, 187], [82, 232], [83, 98], [83, 171], [83, 239], [84, 93], [84, 236], [85, 172], [86, 251], [87, 93], [87, 142], [87, 250], [88, 134], [88, 238], [89, 181], [89, 193], [89, 228], [90, 148], [90, 176], [90, 228], [91, 232], [91, 243], [91, 245], [92, 143], [92, 203], [93, 129], [94, 134], [94, 164], [95, 249], [96, 173], [96, 255], [97, 248], [98, 170], [98, 205], [99, 144], [99, 164], [100, 122], [100, 136], [100, 206], [101, 251], [101, 254], [102, 212], [102, 246], [103, 235], [104, 133], [104, 159], [105, 157], [106, 108], [106, 180], [106, 207], [107, 114], [107, 118], [107, 152], [108, 214], [108, 222], [109, 181], [109, 247], [110, 175], [110, 201], [111, 213], [111, 231], [112, 194], [112, 199], [112, 225], [114, 175], [115, 146], [115, 238], [116, 150], [116, 160], [116, 209], [117, 178], [117, 240], [118, 123], [119, 127], [120, 141], [120, 155], [122, 126], [123, 210], [124, 158], [125, 165], [125, 169], [125, 255], [128, 234], [129, 192], [130, 216], [131, 226], [132, 137], [133, 223], [134, 165], [135, 214], [135, 220], [135, 252], [136, 243], [137, 147], [138, 145], [138, 154], [138, 163], [139, 146], [139, 240], [140, 146], [140, 161], [140, 256], [142, 156], [143, 166], [143, 245], [144, 173], [145, 200], [145, 242], [147, 162], [148, 177], [149, 175], [150, 244], [151, 170], [152, 254], [153, 205], [153, 223], [155, 241], [156, 211], [157, 181], [157, 233], [158, 199], [159, 189], [160, 204], [161, 243], [162, 230], [163, 206], [164, 218], [166, 215], [167, 219], [167, 245], [168, 239], [169, 171], [169, 178], [172, 209], [172, 222], [173, 180], [174, 227], [174, 235], [177, 196], [179, 216], [184, 224], [184, 237], [185, 212], [185, 237], [186, 233], [186, 242], [187, 197], [188, 248], [190, 244], [191, 197], [191, 215], [192, 234], [193, 220], [193, 246], [195, 227], [195, 246], [196, 211], [198, 210], [198, 248], [198, 252], [200, 213], [203, 210], [204, 218], [205, 229], [208, 219], [208, 241], [209, 228], [213, 247], [214, 230], [216, 217], [217, 244], [218, 256], [219, 238], [220, 249], [221, 224], [224, 256], [225, 252], [229, 250], [230, 235], [231, 249], [236, 239], [236, 247]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_256_21.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_256_21 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
