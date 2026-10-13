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
D:=P177Graph("VT3_258_1",258,[1, 4, 5, 6, 11, 14, 15, 17, 20, 21, 23, 28, 31, 32, 33, 34, 36, 37, 39, 42, 44, 46, 48, 49, 50, 52, 53, 56, 58, 59, 60, 63, 64, 67, 69, 71, 74, 78, 82, 83, 85, 86, 90, 92, 93, 94, 95, 96, 97, 99, 100, 101, 103, 106, 107, 108, 110, 113, 115, 117, 118, 120, 121, 123, 124, 126, 127, 131, 132, 133, 134, 135, 138, 140, 141, 144, 145, 148, 149, 150, 151, 152, 160, 162, 163, 165, 167, 168, 169, 176, 182, 184, 185, 186, 187, 192, 193, 194, 195, 196, 198, 201, 204, 205, 209, 210, 211, 214, 216, 218, 219, 223, 228, 229, 232, 233, 238, 239, 241, 242, 244, 247, 248, 249, 252, 253, 254, 257, 258],[[1, 19], [1, 68], [1, 200], [2, 151], [2, 163], [2, 219], [3, 31], [3, 93], [3, 123], [4, 16], [4, 22], [4, 88], [5, 12], [5, 199], [5, 235], [6, 41], [6, 146], [6, 161], [7, 28], [7, 168], [7, 252], [8, 15], [8, 46], [8, 123], [9, 150], [9, 165], [9, 201], [10, 64], [10, 78], [10, 126], [11, 27], [11, 159], [11, 231], [12, 28], [12, 44], [13, 46], [13, 49], [13, 121], [14, 73], [14, 158], [14, 190], [15, 72], [15, 129], [16, 64], [16, 133], [17, 136], [17, 156], [17, 173], [18, 193], [18, 209], [18, 253], [19, 82], [19, 253], [20, 171], [20, 203], [20, 217], [21, 84], [21, 112], [21, 122], [22, 96], [22, 126], [23, 45], [23, 180], [23, 225], [24, 184], [24, 214], [24, 239], [25, 33], [25, 96], [25, 198], [26, 50], [26, 185], [26, 186], [27, 53], [27, 218], [28, 159], [29, 134], [29, 145], [29, 168], [30, 74], [30, 95], [30, 160], [31, 72], [31, 128], [32, 54], [32, 111], [32, 190], [33, 146], [33, 177], [34, 76], [34, 155], [34, 190], [35, 107], [35, 167], [35, 185], [36, 57], [36, 61], [36, 153], [37, 70], [37, 183], [37, 246], [38, 100], [38, 167], [38, 238], [39, 40], [39, 142], [39, 237], [40, 165], [40, 211], [41, 198], [41, 247], [42, 105], [42, 157], [42, 255], [43, 67], [43, 132], [43, 216], [44, 98], [44, 220], [45, 103], [45, 187], [46, 175], [47, 150], [47, 229], [47, 253], [48, 114], [48, 147], [48, 166], [49, 80], [49, 156], [50, 65], [50, 221], [51, 135], [51, 145], [51, 252], [52, 70], [52, 224], [52, 234], [53, 170], [53, 256], [54, 78], [54, 144], [55, 94], [55, 209], [55, 229], [56, 175], [56, 200], [56, 240], [57, 182], [57, 258], [58, 91], [58, 155], [58, 251], [59, 104], [59, 139], [59, 147], [60, 73], [60, 111], [60, 217], [61, 110], [61, 196], [62, 117], [62, 135], [62, 152], [63, 125], [63, 156], [63, 175], [64, 91], [65, 107], [65, 196], [66, 132], [66, 209], [66, 241], [67, 139], [67, 166], [68, 115], [68, 150], [69, 174], [69, 227], [69, 237], [70, 83], [71, 146], [71, 188], [71, 230], [72, 113], [73, 228], [74, 89], [74, 164], [75, 113], [75, 134], [75, 249], [76, 99], [76, 176], [77, 90], [77, 223], [77, 233], [78, 155], [79, 85], [79, 133], [79, 167], [80, 124], [80, 232], [81, 85], [81, 141], [81, 185], [82, 224], [82, 226], [83, 116], [83, 226], [84, 94], [84, 241], [85, 91], [86, 153], [86, 183], [86, 234], [87, 95], [87, 118], [87, 242], [88, 140], [88, 192], [89, 118], [89, 239], [90, 173], [90, 245], [92, 122], [92, 203], [92, 255], [93, 208], [93, 236], [94, 255], [95, 112], [96, 137], [97, 98], [97, 181], [97, 221], [98, 252], [99, 174], [99, 251], [100, 119], [100, 246], [101, 136], [101, 153], [101, 245], [102, 113], [102, 148], [102, 194], [103, 164], [103, 171], [104, 108], [104, 238], [105, 165], [105, 229], [106, 142], [106, 227], [106, 236], [107, 119], [108, 116], [108, 246], [109, 131], [109, 148], [109, 247], [110, 119], [110, 183], [111, 204], [112, 162], [114, 151], [114, 192], [115, 208], [115, 240], [116, 244], [117, 174], [117, 212], [118, 199], [120, 130], [120, 189], [120, 256], [121, 129], [121, 191], [122, 160], [123, 240], [124, 161], [124, 191], [125, 210], [125, 257], [126, 177], [127, 159], [127, 172], [127, 199], [128, 134], [128, 149], [129, 148], [130, 169], [130, 218], [131, 154], [131, 213], [132, 206], [133, 207], [135, 181], [136, 257], [137, 192], [137, 219], [138, 143], [138, 166], [138, 189], [139, 244], [140, 147], [140, 207], [141, 212], [141, 251], [142, 201], [143, 169], [143, 216], [144, 177], [144, 188], [145, 222], [149, 222], [149, 236], [151, 189], [152, 222], [152, 227], [154, 163], [154, 194], [157, 211], [157, 228], [158, 176], [158, 211], [160, 171], [161, 205], [162, 179], [162, 197], [163, 256], [164, 214], [168, 231], [169, 179], [170, 194], [170, 249], [172, 218], [172, 242], [173, 232], [176, 237], [178, 187], [178, 204], [178, 254], [179, 242], [180, 233], [180, 254], [181, 186], [182, 243], [182, 250], [184, 202], [184, 250], [186, 212], [187, 217], [188, 204], [191, 247], [193, 206], [193, 226], [195, 220], [195, 221], [195, 243], [196, 243], [197, 216], [197, 241], [198, 213], [200, 210], [201, 208], [202, 223], [202, 258], [203, 228], [205, 215], [205, 230], [206, 244], [207, 238], [210, 224], [213, 219], [214, 225], [215, 232], [215, 233], [220, 248], [223, 225], [230, 254], [231, 249], [234, 257], [235, 239], [235, 248], [245, 258], [248, 250]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_258_1.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_258_1 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
