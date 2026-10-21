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
D:=P177Graph("VT3_224_98",224,[1, 5, 6, 7, 8, 9, 10, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223],[[1, 2], [1, 3], [1, 4], [2, 5], [2, 6], [3, 7], [3, 9], [4, 8], [4, 10], [5, 11], [5, 13], [6, 12], [6, 14], [7, 15], [7, 19], [8, 16], [8, 20], [9, 17], [9, 21], [10, 18], [10, 22], [11, 23], [11, 27], [12, 24], [12, 28], [13, 25], [13, 29], [14, 26], [14, 30], [15, 31], [15, 39], [16, 32], [16, 40], [17, 33], [17, 41], [18, 34], [18, 42], [19, 35], [19, 43], [20, 36], [20, 44], [21, 37], [21, 45], [22, 38], [22, 46], [23, 47], [23, 55], [24, 48], [24, 56], [25, 49], [25, 57], [26, 50], [26, 58], [27, 51], [27, 59], [28, 52], [28, 60], [29, 53], [29, 61], [30, 54], [30, 62], [31, 63], [31, 79], [32, 64], [32, 80], [33, 65], [33, 81], [34, 66], [34, 82], [35, 67], [35, 83], [36, 68], [36, 84], [37, 69], [37, 85], [38, 70], [38, 86], [39, 71], [39, 87], [40, 72], [40, 88], [41, 73], [41, 89], [42, 74], [42, 90], [43, 75], [43, 91], [44, 76], [44, 92], [45, 77], [45, 93], [46, 78], [46, 94], [47, 95], [47, 111], [48, 96], [48, 112], [49, 97], [49, 113], [50, 98], [50, 114], [51, 99], [51, 115], [52, 100], [52, 116], [53, 101], [53, 117], [54, 102], [54, 118], [55, 103], [55, 119], [56, 104], [56, 120], [57, 105], [57, 121], [58, 106], [58, 122], [59, 107], [59, 123], [60, 108], [60, 124], [61, 109], [61, 125], [62, 110], [62, 126], [63, 127], [63, 144], [64, 128], [64, 145], [65, 114], [65, 129], [66, 120], [66, 130], [67, 103], [67, 104], [68, 131], [68, 136], [69, 120], [69, 123], [70, 112], [70, 132], [71, 99], [71, 146], [72, 99], [72, 147], [73, 133], [73, 148], [74, 134], [74, 149], [75, 107], [75, 124], [76, 109], [76, 150], [77, 108], [77, 119], [78, 135], [78, 141], [79, 135], [79, 136], [80, 102], [80, 113], [81, 112], [81, 131], [82, 97], [82, 114], [83, 137], [83, 151], [84, 138], [84, 152], [85, 122], [85, 139], [86, 122], [86, 140], [87, 109], [87, 132], [88, 98], [88, 101], [89, 141], [89, 150], [90, 117], [90, 118], [91, 101], [91, 153], [92, 107], [92, 154], [93, 142], [93, 155], [94, 143], [94, 156], [95, 157], [95, 174], [96, 158], [96, 175], [97, 159], [98, 160], [100, 161], [100, 166], [102, 162], [103, 176], [104, 177], [105, 163], [105, 178], [106, 164], [106, 179], [108, 180], [110, 165], [110, 171], [111, 165], [111, 166], [113, 161], [115, 167], [115, 181], [116, 168], [116, 182], [117, 169], [118, 170], [119, 162], [121, 171], [121, 180], [123, 183], [124, 184], [125, 172], [125, 185], [126, 173], [126, 186], [127, 157], [127, 158], [128, 157], [128, 187], [129, 187], [129, 200], [130, 172], [130, 174], [131, 188], [132, 165], [133, 176], [133, 193], [134, 189], [134, 194], [135, 162], [136, 189], [137, 168], [137, 190], [138, 167], [138, 195], [139, 191], [139, 202], [140, 182], [140, 192], [141, 197], [142, 160], [142, 198], [143, 183], [143, 199], [144, 160], [144, 193], [145, 183], [145, 194], [146, 163], [146, 203], [147, 190], [147, 204], [148, 179], [148, 195], [149, 178], [149, 202], [150, 196], [151, 197], [151, 198], [152, 170], [152, 199], [153, 173], [153, 175], [154, 200], [154, 201], [155, 186], [155, 201], [156, 185], [156, 186], [158, 205], [159, 205], [159, 218], [161, 206], [163, 211], [164, 207], [164, 212], [166, 207], [167, 208], [168, 213], [169, 209], [169, 220], [170, 210], [171, 215], [172, 216], [173, 217], [174, 211], [175, 212], [176, 221], [177, 208], [177, 222], [178, 213], [179, 220], [180, 214], [181, 215], [181, 216], [182, 217], [184, 218], [184, 219], [185, 219], [187, 208], [188, 209], [188, 211], [189, 207], [190, 205], [191, 206], [191, 223], [192, 216], [192, 221], [193, 206], [194, 221], [195, 213], [196, 217], [196, 222], [197, 215], [198, 210], [199, 214], [200, 223], [201, 220], [202, 219], [203, 210], [203, 212], [204, 214], [204, 223], [209, 224], [218, 224], [222, 224]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_224_98.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_224_98 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
