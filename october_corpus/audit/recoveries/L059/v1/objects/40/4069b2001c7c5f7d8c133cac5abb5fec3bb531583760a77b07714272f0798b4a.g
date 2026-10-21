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
D:=P177Graph("VT3_256_30",256,[1, 2, 3, 5, 8, 9, 10, 13, 14, 15, 20, 21, 22, 23, 29, 31, 33, 34, 37, 39, 40, 42, 43, 46, 49, 50, 54, 55, 56, 57, 58, 60, 64, 67, 71, 73, 74, 75, 77, 81, 82, 83, 85, 89, 91, 92, 93, 94, 97, 99, 104, 106, 110, 111, 112, 117, 118, 119, 120, 125, 126, 127, 128, 129, 130, 131, 134, 137, 138, 140, 141, 143, 144, 145, 146, 147, 150, 151, 152, 153, 155, 156, 157, 158, 159, 160, 162, 163, 166, 173, 177, 179, 180, 183, 184, 187, 192, 193, 194, 200, 201, 203, 205, 207, 213, 214, 215, 216, 221, 225, 227, 228, 229, 230, 233, 234, 235, 236, 239, 243, 244, 247, 248, 249, 251, 252, 254, 256],[[1, 41], [1, 189], [1, 209], [2, 26], [2, 186], [2, 226], [3, 164], [3, 185], [3, 212], [4, 39], [4, 67], [4, 227], [5, 32], [5, 66], [5, 178], [6, 21], [6, 97], [6, 249], [7, 134], [7, 137], [7, 157], [8, 52], [8, 149], [8, 185], [9, 84], [9, 132], [9, 217], [10, 105], [10, 178], [10, 240], [11, 21], [11, 126], [11, 177], [12, 31], [12, 55], [12, 140], [13, 70], [13, 176], [13, 224], [14, 18], [14, 116], [14, 148], [15, 103], [15, 197], [15, 198], [16, 29], [16, 49], [16, 159], [17, 91], [17, 216], [17, 249], [18, 33], [18, 67], [19, 150], [19, 193], [19, 228], [20, 90], [20, 102], [20, 237], [21, 132], [22, 26], [22, 95], [22, 241], [23, 44], [23, 86], [23, 107], [24, 56], [24, 112], [24, 137], [25, 184], [25, 216], [25, 225], [26, 252], [27, 49], [27, 131], [27, 200], [28, 159], [28, 205], [28, 251], [29, 114], [29, 189], [30, 146], [30, 227], [30, 244], [31, 98], [31, 250], [32, 60], [32, 119], [33, 65], [33, 113], [34, 182], [34, 198], [34, 241], [35, 156], [35, 183], [35, 247], [36, 89], [36, 194], [36, 244], [37, 41], [37, 122], [37, 237], [38, 73], [38, 85], [38, 254], [39, 101], [39, 123], [40, 66], [40, 116], [40, 212], [41, 129], [42, 105], [42, 123], [42, 208], [43, 109], [43, 139], [43, 142], [44, 94], [44, 179], [45, 73], [45, 92], [45, 138], [46, 101], [46, 202], [46, 253], [47, 110], [47, 125], [47, 153], [48, 93], [48, 179], [48, 180], [49, 59], [50, 172], [50, 188], [50, 237], [51, 56], [51, 77], [51, 233], [52, 71], [52, 244], [53, 128], [53, 137], [53, 166], [54, 76], [54, 167], [54, 191], [55, 170], [55, 181], [56, 220], [57, 148], [57, 165], [57, 204], [58, 80], [58, 175], [58, 245], [59, 110], [59, 184], [60, 72], [60, 199], [61, 118], [61, 158], [61, 216], [62, 126], [62, 180], [62, 215], [63, 99], [63, 130], [63, 166], [64, 188], [64, 199], [64, 232], [65, 91], [65, 207], [66, 221], [67, 222], [68, 83], [68, 141], [68, 205], [69, 104], [69, 111], [69, 144], [70, 83], [70, 203], [71, 84], [71, 186], [72, 125], [72, 215], [73, 168], [74, 121], [74, 186], [74, 191], [75, 115], [75, 196], [75, 253], [76, 120], [76, 183], [77, 107], [77, 108], [78, 140], [78, 163], [78, 201], [79, 83], [79, 118], [79, 145], [80, 213], [80, 256], [81, 87], [81, 96], [81, 206], [82, 139], [82, 168], [82, 189], [84, 130], [85, 202], [85, 255], [86, 146], [86, 248], [87, 127], [87, 228], [88, 119], [88, 143], [88, 163], [89, 121], [89, 136], [90, 147], [90, 163], [91, 191], [92, 172], [92, 217], [93, 231], [93, 246], [94, 102], [94, 238], [95, 160], [95, 214], [96, 125], [96, 131], [97, 113], [97, 172], [98, 143], [98, 200], [99, 161], [99, 245], [100, 229], [100, 239], [100, 243], [101, 236], [102, 233], [103, 110], [103, 158], [104, 202], [104, 211], [105, 229], [106, 139], [106, 198], [106, 219], [107, 144], [108, 157], [108, 200], [109, 129], [109, 145], [111, 195], [111, 209], [112, 133], [112, 165], [113, 147], [114, 143], [114, 221], [115, 127], [115, 249], [116, 247], [117, 142], [117, 190], [117, 241], [118, 133], [119, 218], [120, 169], [120, 231], [121, 173], [122, 160], [122, 225], [123, 207], [124, 140], [124, 152], [124, 214], [126, 175], [127, 133], [128, 170], [128, 190], [129, 154], [130, 238], [131, 196], [132, 155], [134, 161], [134, 197], [135, 155], [135, 201], [135, 251], [136, 157], [136, 254], [138, 199], [138, 219], [141, 142], [141, 149], [144, 250], [145, 148], [146, 246], [147, 204], [149, 166], [150, 154], [150, 188], [151, 181], [151, 212], [151, 240], [152, 226], [152, 240], [153, 169], [153, 178], [154, 247], [155, 171], [156, 185], [156, 246], [158, 174], [159, 176], [160, 195], [161, 234], [162, 174], [162, 182], [162, 208], [164, 187], [164, 205], [165, 230], [167, 225], [167, 233], [168, 194], [169, 173], [170, 230], [171, 187], [171, 215], [173, 197], [174, 203], [175, 203], [176, 248], [177, 224], [177, 253], [179, 245], [180, 232], [181, 192], [182, 239], [183, 220], [184, 210], [187, 206], [190, 235], [192, 206], [192, 242], [193, 211], [193, 242], [194, 222], [195, 239], [196, 254], [201, 238], [204, 256], [207, 226], [208, 213], [209, 248], [210, 214], [210, 251], [211, 243], [213, 223], [217, 252], [218, 234], [218, 256], [219, 234], [220, 228], [221, 222], [223, 230], [223, 236], [224, 227], [229, 231], [232, 243], [235, 242], [235, 255], [236, 250], [252, 255]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_256_30.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_256_30 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
