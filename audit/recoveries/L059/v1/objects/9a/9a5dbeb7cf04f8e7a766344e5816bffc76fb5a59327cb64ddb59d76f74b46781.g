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
D:=P177Graph("VT3_220_53",220,[1, 5, 6, 7, 8, 9, 10, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218],[[1, 2], [1, 3], [1, 4], [2, 5], [2, 6], [3, 7], [3, 9], [4, 8], [4, 10], [5, 11], [5, 13], [6, 12], [6, 14], [7, 15], [7, 19], [8, 16], [8, 20], [9, 17], [9, 21], [10, 18], [10, 22], [11, 23], [11, 27], [12, 24], [12, 28], [13, 25], [13, 29], [14, 26], [14, 30], [15, 31], [15, 39], [16, 32], [16, 40], [17, 33], [17, 41], [18, 34], [18, 42], [19, 35], [19, 43], [20, 36], [20, 44], [21, 37], [21, 45], [22, 38], [22, 46], [23, 47], [23, 55], [24, 48], [24, 56], [25, 49], [25, 57], [26, 50], [26, 58], [27, 51], [27, 59], [28, 52], [28, 60], [29, 53], [29, 61], [30, 54], [30, 62], [31, 62], [31, 78], [32, 63], [32, 79], [33, 64], [33, 80], [34, 65], [34, 81], [35, 66], [35, 82], [36, 67], [36, 83], [37, 68], [37, 84], [38, 69], [38, 85], [39, 70], [39, 86], [40, 71], [40, 87], [41, 72], [41, 88], [42, 73], [42, 89], [43, 74], [43, 90], [44, 75], [44, 91], [45, 63], [45, 76], [46, 47], [46, 77], [47, 107], [48, 92], [48, 108], [49, 93], [49, 109], [50, 94], [50, 110], [51, 95], [51, 111], [52, 96], [52, 112], [53, 97], [53, 113], [54, 98], [54, 114], [55, 99], [55, 115], [56, 100], [56, 116], [57, 101], [57, 117], [58, 102], [58, 118], [59, 103], [59, 119], [60, 104], [60, 120], [61, 92], [61, 105], [62, 106], [63, 139], [64, 121], [64, 138], [65, 105], [65, 122], [66, 123], [66, 140], [67, 117], [67, 124], [68, 125], [68, 141], [69, 98], [69, 142], [70, 126], [70, 133], [71, 100], [71, 127], [72, 101], [72, 128], [73, 104], [73, 134], [74, 129], [74, 135], [75, 102], [75, 130], [76, 94], [76, 143], [77, 125], [77, 144], [78, 131], [78, 145], [79, 119], [79, 132], [80, 111], [80, 146], [81, 133], [81, 147], [82, 109], [82, 134], [83, 112], [83, 140], [84, 113], [84, 148], [85, 135], [85, 149], [86, 115], [86, 136], [87, 137], [87, 145], [88, 96], [88, 150], [89, 128], [89, 151], [90, 108], [90, 121], [91, 122], [91, 138], [92, 170], [93, 152], [93, 169], [94, 153], [95, 154], [95, 171], [96, 155], [97, 156], [97, 172], [98, 173], [99, 157], [99, 164], [100, 158], [101, 159], [102, 165], [103, 160], [103, 166], [104, 161], [105, 174], [106, 156], [106, 175], [107, 162], [107, 176], [108, 163], [109, 177], [110, 164], [110, 178], [111, 165], [112, 171], [113, 179], [114, 166], [114, 180], [115, 167], [116, 168], [116, 176], [117, 181], [118, 159], [118, 182], [119, 152], [120, 153], [120, 169], [121, 193], [122, 194], [123, 167], [123, 174], [124, 163], [124, 183], [125, 184], [126, 159], [126, 185], [127, 166], [127, 187], [128, 157], [129, 186], [129, 195], [130, 162], [130, 196], [131, 161], [131, 190], [132, 155], [132, 182], [133, 179], [134, 187], [135, 158], [136, 154], [136, 188], [137, 185], [137, 189], [138, 169], [139, 186], [139, 197], [140, 180], [141, 190], [141, 198], [142, 182], [142, 199], [143, 154], [143, 181], [144, 177], [144, 185], [145, 183], [146, 175], [146, 191], [147, 192], [147, 197], [148, 164], [148, 187], [149, 171], [149, 190], [150, 174], [150, 184], [151, 163], [151, 173], [152, 210], [153, 211], [155, 200], [156, 201], [157, 202], [158, 204], [160, 203], [160, 212], [161, 213], [162, 207], [165, 204], [167, 205], [168, 202], [168, 206], [170, 203], [170, 214], [172, 207], [172, 215], [173, 216], [175, 202], [176, 200], [177, 208], [178, 209], [178, 214], [179, 204], [180, 207], [181, 201], [183, 209], [184, 212], [186, 208], [188, 216], [188, 217], [189, 206], [189, 211], [191, 203], [191, 213], [192, 200], [192, 217], [193, 215], [193, 217], [194, 206], [194, 218], [195, 201], [195, 218], [196, 208], [196, 214], [197, 213], [198, 210], [198, 215], [199, 205], [199, 218], [205, 219], [209, 219], [210, 219], [211, 220], [212, 220], [216, 220]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_220_53.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_220_53 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
