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
D:=P177Graph("VT3_250_30",250,[1, 5, 6, 11, 16, 18, 21, 23, 24, 26, 27, 28, 29, 32, 39, 40, 46, 49, 50, 52, 53, 54, 55, 57, 62, 63, 65, 66, 68, 69, 71, 73, 75, 76, 77, 78, 81, 82, 84, 86, 90, 92, 93, 94, 95, 96, 99, 101, 102, 105, 113, 114, 116, 118, 120, 121, 123, 124, 125, 126, 127, 128, 129, 130, 131, 133, 137, 139, 142, 146, 150, 151, 152, 153, 155, 158, 159, 160, 169, 170, 171, 172, 173, 174, 176, 178, 179, 180, 184, 186, 188, 189, 190, 192, 194, 196, 197, 198, 199, 200, 201, 203, 206, 209, 213, 214, 216, 217, 219, 220, 225, 226, 227, 229, 233, 234, 235, 236, 238, 240, 242, 245, 246, 247, 248],[[1, 132], [1, 223], [1, 237], [2, 94], [2, 198], [2, 245], [3, 86], [3, 139], [3, 169], [4, 49], [4, 84], [4, 120], [5, 45], [5, 79], [5, 111], [6, 37], [6, 122], [6, 136], [7, 105], [7, 186], [7, 225], [8, 68], [8, 179], [8, 219], [9, 16], [9, 86], [9, 171], [10, 63], [10, 127], [10, 171], [11, 12], [11, 72], [11, 147], [12, 203], [12, 227], [13, 73], [13, 197], [13, 217], [14, 77], [14, 114], [14, 169], [15, 92], [15, 124], [15, 226], [16, 47], [16, 111], [17, 29], [17, 152], [17, 160], [18, 48], [18, 103], [18, 191], [19, 23], [19, 96], [19, 171], [20, 118], [20, 137], [20, 213], [21, 138], [21, 141], [21, 223], [22, 29], [22, 75], [22, 170], [23, 35], [23, 119], [24, 72], [24, 230], [24, 232], [25, 84], [25, 121], [25, 180], [26, 115], [26, 185], [26, 215], [27, 83], [27, 215], [27, 230], [28, 47], [28, 108], [28, 182], [29, 115], [30, 90], [30, 94], [30, 216], [31, 196], [31, 229], [31, 240], [32, 168], [32, 177], [32, 218], [33, 46], [33, 75], [33, 206], [34, 94], [34, 101], [34, 242], [35, 219], [35, 245], [36, 150], [36, 151], [36, 246], [37, 199], [37, 247], [38, 54], [38, 78], [38, 159], [39, 89], [39, 141], [39, 157], [40, 207], [40, 230], [40, 241], [41, 82], [41, 199], [41, 209], [42, 66], [42, 155], [42, 190], [43, 81], [43, 93], [43, 214], [44, 62], [44, 200], [44, 217], [45, 73], [45, 114], [46, 119], [46, 161], [47, 179], [48, 77], [48, 153], [49, 61], [49, 88], [50, 167], [50, 211], [50, 224], [51, 155], [51, 160], [51, 209], [52, 135], [52, 156], [52, 208], [53, 106], [53, 112], [53, 181], [54, 166], [54, 222], [55, 58], [55, 59], [55, 61], [56, 99], [56, 130], [56, 197], [57, 140], [57, 231], [57, 250], [58, 128], [58, 188], [59, 65], [59, 123], [60, 124], [60, 139], [60, 220], [61, 245], [62, 88], [62, 148], [63, 64], [63, 212], [64, 78], [64, 186], [65, 140], [65, 232], [66, 205], [66, 212], [67, 126], [67, 133], [67, 248], [68, 103], [68, 202], [69, 109], [69, 111], [69, 204], [70, 146], [70, 188], [70, 206], [71, 161], [71, 187], [71, 250], [72, 197], [73, 185], [74, 125], [74, 201], [74, 225], [75, 168], [76, 104], [76, 117], [76, 167], [77, 135], [78, 191], [79, 101], [79, 113], [80, 102], [80, 178], [80, 235], [81, 89], [81, 134], [82, 163], [82, 221], [83, 120], [83, 133], [84, 89], [85, 131], [85, 139], [85, 213], [86, 98], [87, 131], [87, 159], [87, 246], [88, 152], [90, 191], [90, 224], [91, 99], [91, 153], [91, 234], [92, 108], [92, 156], [93, 145], [93, 147], [95, 98], [95, 110], [95, 154], [96, 104], [96, 181], [97, 137], [97, 227], [97, 235], [98, 236], [99, 249], [100, 123], [100, 174], [100, 178], [101, 165], [102, 132], [102, 161], [103, 146], [104, 192], [105, 221], [105, 241], [106, 137], [106, 180], [107, 120], [107, 184], [107, 225], [108, 184], [109, 128], [109, 176], [110, 118], [110, 200], [112, 123], [112, 201], [113, 144], [113, 221], [114, 187], [115, 194], [116, 162], [116, 205], [116, 210], [117, 128], [117, 130], [118, 177], [119, 172], [121, 168], [121, 222], [122, 142], [122, 198], [124, 166], [125, 145], [125, 249], [126, 175], [126, 222], [127, 239], [127, 243], [129, 147], [129, 163], [129, 208], [130, 154], [131, 193], [132, 217], [133, 228], [134, 194], [134, 236], [135, 238], [136, 186], [136, 236], [138, 170], [138, 203], [140, 216], [141, 219], [142, 162], [142, 195], [143, 189], [143, 238], [143, 246], [144, 174], [144, 234], [145, 242], [146, 215], [148, 173], [148, 199], [149, 159], [149, 201], [149, 229], [150, 202], [150, 231], [151, 239], [151, 244], [152, 204], [153, 195], [154, 233], [155, 187], [156, 194], [157, 229], [157, 233], [158, 165], [158, 202], [158, 228], [160, 243], [162, 172], [163, 213], [164, 189], [164, 206], [164, 233], [165, 226], [166, 172], [167, 247], [169, 211], [170, 211], [173, 181], [173, 183], [174, 205], [175, 209], [175, 216], [176, 241], [176, 244], [177, 190], [178, 228], [179, 249], [180, 239], [182, 189], [182, 235], [183, 220], [183, 242], [184, 210], [185, 198], [188, 212], [190, 207], [192, 193], [192, 250], [193, 234], [195, 240], [196, 218], [196, 232], [200, 210], [203, 231], [204, 227], [207, 238], [208, 248], [214, 224], [214, 244], [218, 247], [220, 223], [226, 243], [237, 240], [237, 248]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_250_30.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_250_30 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
