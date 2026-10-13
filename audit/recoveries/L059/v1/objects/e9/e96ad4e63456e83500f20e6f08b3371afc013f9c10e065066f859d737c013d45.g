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
D:=P177Graph("CSS_220_1",220,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129, 131, 133, 135, 137, 139, 141, 143, 145, 147, 149, 151, 153, 155, 157, 159, 161, 163, 165, 167, 169, 171, 173, 175, 177, 179, 181, 183, 185, 187, 189, 191, 193, 195, 197, 199, 201, 203, 205, 207, 209, 211, 213, 215, 217, 219],[[1, 2], [1, 76], [1, 220], [2, 3], [2, 47], [3, 4], [3, 190], [4, 5], [4, 95], [5, 6], [5, 80], [6, 7], [6, 131], [7, 8], [7, 182], [8, 9], [8, 173], [9, 10], [9, 98], [10, 11], [10, 43], [11, 12], [11, 106], [12, 13], [12, 77], [13, 14], [13, 68], [14, 15], [14, 39], [15, 16], [15, 144], [16, 17], [16, 161], [17, 18], [17, 172], [18, 19], [18, 149], [19, 20], [19, 214], [20, 21], [20, 165], [21, 22], [21, 96], [22, 23], [22, 67], [23, 24], [23, 210], [24, 25], [24, 115], [25, 26], [25, 100], [26, 27], [26, 151], [27, 28], [27, 202], [28, 29], [28, 193], [29, 30], [29, 118], [30, 31], [30, 63], [31, 32], [31, 126], [32, 33], [32, 97], [33, 34], [33, 88], [34, 35], [34, 59], [35, 36], [35, 164], [36, 37], [36, 181], [37, 38], [37, 192], [38, 39], [38, 169], [39, 40], [40, 41], [40, 185], [41, 42], [41, 116], [42, 43], [42, 87], [43, 44], [44, 45], [44, 135], [45, 46], [45, 120], [46, 47], [46, 171], [47, 48], [48, 49], [48, 213], [49, 50], [49, 138], [50, 51], [50, 83], [51, 52], [51, 146], [52, 53], [52, 117], [53, 54], [53, 108], [54, 55], [54, 79], [55, 56], [55, 184], [56, 57], [56, 201], [57, 58], [57, 212], [58, 59], [58, 189], [59, 60], [60, 61], [60, 205], [61, 62], [61, 136], [62, 63], [62, 107], [63, 64], [64, 65], [64, 155], [65, 66], [65, 140], [66, 67], [66, 191], [67, 68], [68, 69], [69, 70], [69, 158], [70, 71], [70, 103], [71, 72], [71, 166], [72, 73], [72, 137], [73, 74], [73, 128], [74, 75], [74, 99], [75, 76], [75, 204], [76, 77], [77, 78], [78, 79], [78, 209], [79, 80], [80, 81], [81, 82], [81, 156], [82, 83], [82, 127], [83, 84], [84, 85], [84, 175], [85, 86], [85, 160], [86, 87], [86, 211], [87, 88], [88, 89], [89, 90], [89, 178], [90, 91], [90, 123], [91, 92], [91, 186], [92, 93], [92, 157], [93, 94], [93, 148], [94, 95], [94, 119], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100], [100, 101], [101, 102], [101, 176], [102, 103], [102, 147], [103, 104], [104, 105], [104, 195], [105, 106], [105, 180], [106, 107], [107, 108], [108, 109], [109, 110], [109, 198], [110, 111], [110, 143], [111, 112], [111, 206], [112, 113], [112, 177], [113, 114], [113, 168], [114, 115], [114, 139], [115, 116], [116, 117], [117, 118], [118, 119], [119, 120], [120, 121], [121, 122], [121, 196], [122, 123], [122, 167], [123, 124], [124, 125], [124, 215], [125, 126], [125, 200], [126, 127], [127, 128], [128, 129], [129, 130], [129, 218], [130, 131], [130, 163], [131, 132], [132, 133], [132, 197], [133, 134], [133, 188], [134, 135], [134, 159], [135, 136], [136, 137], [137, 138], [138, 139], [139, 140], [140, 141], [141, 142], [141, 216], [142, 143], [142, 187], [143, 144], [144, 145], [145, 146], [145, 220], [146, 147], [147, 148], [148, 149], [149, 150], [150, 151], [150, 183], [151, 152], [152, 153], [152, 217], [153, 154], [153, 208], [154, 155], [154, 179], [155, 156], [156, 157], [157, 158], [158, 159], [159, 160], [160, 161], [161, 162], [162, 163], [162, 207], [163, 164], [164, 165], [165, 166], [166, 167], [167, 168], [168, 169], [169, 170], [170, 171], [170, 203], [171, 172], [172, 173], [173, 174], [174, 175], [174, 199], [175, 176], [176, 177], [177, 178], [178, 179], [179, 180], [180, 181], [181, 182], [182, 183], [183, 184], [184, 185], [185, 186], [186, 187], [187, 188], [188, 189], [189, 190], [190, 191], [191, 192], [192, 193], [193, 194], [194, 195], [194, 219], [195, 196], [196, 197], [197, 198], [198, 199], [199, 200], [200, 201], [201, 202], [202, 203], [203, 204], [204, 205], [205, 206], [206, 207], [207, 208], [208, 209], [209, 210], [210, 211], [211, 212], [212, 213], [213, 214], [214, 215], [215, 216], [216, 217], [217, 218], [218, 219], [219, 220]]);;
R:=P177Census(D);;
Need(Size(R.F)=Size(R.A));;
PrintTo("cubic_markings/CSS_220_1.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE CSS_220_1 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
