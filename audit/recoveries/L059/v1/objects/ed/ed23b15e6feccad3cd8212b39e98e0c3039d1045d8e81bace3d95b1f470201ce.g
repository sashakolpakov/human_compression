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
D:=P177Graph("VT3_240_294",240,[1, 5, 6, 7, 8, 9, 10, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 240],[[1, 2], [1, 3], [1, 4], [2, 5], [2, 6], [3, 7], [3, 9], [4, 8], [4, 10], [5, 11], [5, 13], [6, 12], [6, 14], [7, 15], [7, 19], [8, 16], [8, 20], [9, 17], [9, 21], [10, 18], [10, 22], [11, 23], [11, 27], [12, 24], [12, 28], [13, 25], [13, 29], [14, 26], [14, 30], [15, 30], [15, 38], [16, 31], [16, 39], [17, 32], [17, 40], [18, 33], [18, 41], [19, 34], [19, 42], [20, 35], [20, 43], [21, 31], [21, 36], [22, 23], [22, 37], [23, 51], [24, 44], [24, 52], [25, 45], [25, 53], [26, 46], [26, 54], [27, 47], [27, 55], [28, 48], [28, 56], [29, 44], [29, 49], [30, 50], [31, 68], [32, 57], [32, 69], [33, 58], [33, 70], [34, 59], [34, 65], [35, 48], [35, 60], [36, 61], [36, 71], [37, 62], [37, 72], [38, 63], [38, 73], [39, 64], [39, 74], [40, 53], [40, 75], [41, 65], [41, 76], [42, 57], [42, 66], [43, 58], [43, 67], [44, 88], [45, 77], [45, 89], [46, 78], [46, 90], [47, 79], [47, 85], [48, 80], [49, 81], [49, 91], [50, 82], [50, 92], [51, 83], [51, 93], [52, 84], [52, 94], [53, 95], [54, 85], [54, 96], [55, 77], [55, 86], [56, 78], [56, 87], [57, 115], [58, 116], [59, 97], [59, 117], [60, 98], [60, 118], [61, 99], [61, 119], [62, 100], [62, 120], [63, 101], [63, 109], [64, 102], [64, 110], [65, 103], [66, 104], [66, 121], [67, 105], [67, 122], [68, 106], [68, 123], [69, 107], [69, 124], [70, 108], [70, 125], [71, 109], [71, 126], [72, 110], [72, 127], [73, 97], [73, 111], [74, 98], [74, 112], [75, 99], [75, 113], [76, 100], [76, 114], [77, 146], [78, 147], [79, 128], [79, 148], [80, 129], [80, 149], [81, 130], [81, 150], [82, 131], [82, 151], [83, 132], [83, 140], [84, 133], [84, 141], [85, 134], [86, 135], [86, 152], [87, 136], [87, 153], [88, 137], [88, 154], [89, 138], [89, 155], [90, 139], [90, 156], [91, 140], [91, 157], [92, 141], [92, 158], [93, 128], [93, 142], [94, 129], [94, 143], [95, 130], [95, 144], [96, 131], [96, 145], [97, 181], [98, 182], [99, 183], [100, 184], [101, 158], [101, 185], [102, 159], [102, 186], [103, 160], [103, 161], [104, 161], [104, 187], [105, 149], [105, 188], [106, 162], [106, 175], [107, 163], [107, 176], [108, 142], [108, 164], [109, 165], [110, 166], [111, 139], [111, 167], [112, 168], [112, 174], [113, 155], [113, 189], [114, 169], [114, 190], [115, 170], [115, 191], [116, 171], [116, 192], [117, 169], [117, 172], [118, 136], [118, 173], [119, 174], [119, 193], [120, 152], [120, 194], [121, 151], [121, 195], [122, 175], [122, 196], [123, 159], [123, 176], [124, 144], [124, 177], [125, 160], [125, 178], [126, 162], [126, 179], [127, 132], [127, 180], [128, 219], [129, 220], [130, 221], [131, 222], [132, 223], [133, 197], [133, 224], [134, 198], [134, 199], [135, 199], [135, 225], [136, 226], [137, 200], [137, 213], [138, 201], [138, 214], [139, 202], [140, 203], [141, 204], [142, 205], [143, 206], [143, 212], [144, 227], [145, 207], [145, 228], [146, 208], [146, 229], [147, 209], [147, 230], [148, 207], [148, 210], [149, 211], [150, 212], [150, 231], [151, 232], [152, 233], [153, 213], [153, 234], [154, 197], [154, 214], [155, 215], [156, 198], [156, 216], [157, 200], [157, 217], [158, 218], [159, 197], [160, 214], [161, 213], [162, 200], [163, 219], [163, 224], [164, 218], [164, 224], [165, 203], [165, 205], [166, 204], [166, 232], [167, 203], [167, 231], [168, 232], [168, 236], [169, 212], [170, 211], [170, 223], [171, 221], [171, 222], [172, 210], [172, 220], [173, 208], [173, 227], [174, 207], [175, 199], [176, 198], [177, 216], [177, 226], [178, 215], [178, 235], [179, 233], [179, 234], [180, 202], [180, 230], [181, 201], [181, 229], [182, 210], [182, 229], [183, 209], [183, 228], [184, 209], [184, 234], [185, 208], [185, 233], [186, 201], [186, 202], [187, 226], [187, 236], [188, 215], [188, 225], [189, 211], [189, 230], [190, 221], [190, 228], [191, 219], [191, 220], [192, 218], [192, 227], [193, 205], [193, 235], [194, 204], [194, 206], [195, 217], [195, 223], [196, 217], [196, 222], [206, 238], [216, 237], [225, 238], [231, 237], [235, 239], [236, 239], [237, 240], [238, 240], [239, 240]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_240_294.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_240_294 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
