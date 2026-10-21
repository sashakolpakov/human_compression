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
D:=P177Graph("VT3_248_40",248,[1, 2, 3, 4, 6, 9, 11, 14, 17, 19, 22, 23, 24, 27, 28, 29, 32, 33, 36, 37, 39, 41, 44, 45, 46, 47, 48, 52, 54, 58, 59, 60, 64, 65, 67, 68, 72, 74, 75, 76, 79, 80, 81, 88, 90, 94, 95, 96, 97, 98, 100, 104, 105, 106, 107, 109, 112, 115, 116, 118, 119, 121, 123, 127, 128, 130, 132, 133, 135, 138, 139, 140, 141, 143, 147, 148, 149, 152, 154, 156, 157, 159, 161, 162, 164, 172, 173, 175, 176, 177, 179, 180, 183, 184, 185, 186, 187, 188, 189, 191, 194, 195, 196, 198, 199, 206, 210, 213, 215, 216, 218, 219, 223, 224, 225, 226, 228, 231, 232, 233, 235, 237, 238, 243],[[1, 55], [1, 124], [1, 207], [2, 21], [2, 126], [2, 209], [3, 25], [3, 155], [3, 182], [4, 25], [4, 169], [4, 200], [5, 74], [5, 97], [5, 105], [6, 63], [6, 150], [6, 163], [7, 54], [7, 172], [7, 228], [8, 157], [8, 162], [8, 184], [9, 111], [9, 129], [9, 192], [10, 48], [10, 88], [10, 198], [11, 155], [11, 166], [11, 202], [12, 64], [12, 128], [12, 233], [13, 90], [13, 105], [13, 132], [14, 71], [14, 125], [14, 136], [15, 175], [15, 189], [15, 198], [16, 100], [16, 139], [16, 140], [17, 34], [17, 49], [17, 222], [18, 76], [18, 94], [18, 172], [19, 49], [19, 125], [19, 208], [20, 104], [20, 128], [20, 176], [21, 187], [21, 232], [22, 66], [22, 125], [22, 209], [23, 38], [23, 86], [23, 222], [24, 101], [24, 113], [24, 167], [25, 243], [26, 106], [26, 130], [26, 133], [27, 77], [27, 171], [27, 201], [28, 30], [28, 146], [28, 230], [29, 35], [29, 61], [29, 240], [30, 156], [30, 179], [31, 48], [31, 154], [31, 213], [32, 61], [32, 158], [32, 229], [33, 86], [33, 236], [33, 241], [34, 52], [34, 231], [35, 161], [35, 177], [36, 144], [36, 200], [36, 229], [37, 57], [37, 91], [37, 166], [38, 47], [38, 149], [39, 62], [39, 102], [39, 122], [40, 68], [40, 100], [40, 162], [41, 78], [41, 166], [41, 182], [42, 88], [42, 213], [42, 235], [43, 132], [43, 179], [43, 195], [44, 87], [44, 178], [44, 220], [45, 167], [45, 204], [45, 220], [46, 57], [46, 170], [46, 193], [47, 110], [47, 174], [48, 241], [49, 149], [50, 81], [50, 109], [50, 223], [51, 123], [51, 157], [51, 206], [52, 207], [52, 208], [53, 127], [53, 138], [53, 185], [54, 70], [54, 150], [55, 141], [55, 186], [56, 75], [56, 95], [56, 238], [57, 206], [58, 114], [58, 222], [58, 241], [59, 77], [59, 92], [59, 214], [60, 69], [60, 103], [60, 142], [61, 176], [62, 159], [62, 213], [63, 138], [63, 215], [64, 234], [64, 239], [65, 84], [65, 165], [65, 230], [66, 79], [66, 232], [67, 108], [67, 170], [67, 192], [68, 93], [68, 190], [69, 184], [69, 223], [70, 76], [70, 215], [71, 127], [71, 219], [72, 84], [72, 146], [72, 207], [73, 159], [73, 216], [73, 235], [74, 117], [74, 203], [75, 103], [75, 214], [76, 110], [77, 95], [78, 206], [78, 226], [79, 84], [79, 208], [80, 82], [80, 85], [80, 111], [81, 85], [81, 120], [82, 121], [82, 147], [83, 115], [83, 135], [83, 164], [85, 194], [86, 96], [87, 97], [87, 180], [88, 245], [89, 112], [89, 127], [89, 152], [90, 117], [90, 153], [91, 183], [91, 188], [92, 107], [92, 216], [93, 199], [93, 216], [94, 220], [94, 248], [95, 244], [96, 110], [96, 248], [97, 167], [98, 120], [98, 160], [98, 165], [99, 119], [99, 173], [99, 180], [100, 151], [101, 147], [101, 210], [102, 154], [102, 173], [103, 109], [104, 145], [104, 240], [105, 113], [106, 122], [106, 242], [107, 201], [107, 242], [108, 210], [108, 228], [109, 197], [111, 223], [112, 131], [112, 234], [113, 121], [114, 198], [114, 231], [115, 134], [115, 202], [116, 126], [116, 131], [116, 244], [117, 177], [118, 182], [118, 211], [118, 221], [119, 122], [119, 205], [120, 187], [121, 168], [123, 129], [123, 170], [124, 175], [124, 231], [126, 238], [128, 181], [129, 184], [130, 205], [130, 240], [131, 219], [132, 168], [133, 145], [133, 201], [134, 224], [134, 225], [135, 137], [135, 163], [136, 149], [136, 185], [137, 138], [137, 152], [139, 221], [139, 246], [140, 190], [140, 245], [141, 146], [141, 247], [142, 162], [142, 199], [143, 169], [143, 217], [143, 229], [144, 156], [144, 196], [145, 233], [147, 192], [148, 178], [148, 236], [148, 248], [150, 188], [151, 157], [151, 226], [152, 239], [153, 179], [153, 196], [154, 236], [155, 225], [156, 247], [158, 177], [158, 196], [159, 242], [160, 194], [160, 195], [161, 203], [161, 205], [163, 183], [164, 181], [164, 239], [165, 232], [168, 194], [169, 225], [171, 191], [171, 233], [172, 204], [173, 178], [174, 185], [174, 215], [175, 212], [176, 217], [180, 203], [181, 224], [183, 202], [186, 212], [186, 227], [187, 197], [188, 193], [189, 245], [189, 246], [190, 235], [191, 234], [191, 244], [193, 228], [195, 230], [197, 238], [199, 214], [200, 218], [204, 210], [209, 219], [211, 237], [211, 243], [212, 237], [217, 224], [218, 227], [218, 247], [221, 226], [227, 243], [237, 246]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_248_40.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_248_40 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
