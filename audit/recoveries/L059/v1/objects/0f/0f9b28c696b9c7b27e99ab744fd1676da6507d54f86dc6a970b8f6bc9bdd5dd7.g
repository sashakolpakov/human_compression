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
D:=P177Graph("VT3_254_18",254,[1, 2, 3, 7, 8, 9, 10, 11, 12, 14, 16, 17, 18, 20, 21, 22, 28, 31, 32, 33, 34, 39, 46, 49, 50, 51, 54, 55, 59, 63, 65, 67, 69, 70, 71, 72, 73, 74, 78, 81, 83, 84, 86, 89, 90, 91, 92, 93, 101, 105, 106, 110, 112, 114, 115, 119, 125, 126, 131, 133, 134, 137, 138, 141, 145, 146, 147, 148, 150, 151, 154, 155, 156, 157, 160, 161, 163, 166, 169, 171, 173, 174, 181, 182, 183, 184, 185, 187, 189, 191, 194, 195, 196, 197, 199, 201, 202, 204, 206, 209, 211, 212, 213, 214, 215, 218, 219, 220, 222, 223, 226, 229, 230, 231, 232, 233, 234, 237, 239, 242, 243, 246, 247, 250, 251, 253, 254],[[1, 45], [1, 162], [1, 207], [2, 36], [2, 136], [2, 190], [3, 25], [3, 198], [3, 217], [4, 10], [4, 114], [4, 218], [5, 67], [5, 160], [5, 246], [6, 194], [6, 204], [6, 219], [7, 23], [7, 58], [7, 164], [8, 62], [8, 102], [8, 224], [9, 88], [9, 127], [9, 179], [10, 117], [10, 159], [11, 37], [11, 217], [11, 238], [12, 127], [12, 139], [12, 178], [13, 151], [13, 231], [13, 233], [14, 142], [14, 144], [14, 149], [15, 84], [15, 213], [15, 219], [16, 111], [16, 130], [16, 224], [17, 41], [17, 103], [17, 224], [18, 162], [18, 179], [18, 236], [19, 138], [19, 161], [19, 194], [20, 66], [20, 117], [20, 118], [21, 38], [21, 99], [21, 120], [22, 44], [22, 175], [22, 203], [23, 84], [23, 187], [24, 46], [24, 112], [24, 163], [25, 131], [25, 214], [26, 31], [26, 206], [26, 246], [27, 156], [27, 163], [27, 166], [28, 152], [28, 180], [28, 228], [29, 59], [29, 157], [29, 184], [30, 31], [30, 55], [30, 254], [31, 152], [32, 38], [32, 47], [32, 186], [33, 38], [33, 87], [33, 103], [34, 36], [34, 75], [34, 98], [35, 173], [35, 187], [35, 223], [36, 215], [37, 72], [37, 151], [39, 111], [39, 121], [39, 135], [40, 63], [40, 101], [40, 182], [41, 90], [41, 232], [42, 115], [42, 157], [42, 166], [43, 63], [43, 73], [43, 147], [44, 46], [44, 209], [45, 86], [45, 154], [46, 205], [47, 71], [47, 91], [48, 89], [48, 147], [48, 233], [49, 113], [49, 192], [49, 245], [50, 94], [50, 190], [50, 208], [51, 76], [51, 139], [51, 158], [52, 69], [52, 181], [52, 191], [53, 212], [53, 220], [53, 230], [54, 103], [54, 130], [54, 186], [55, 85], [55, 245], [56, 119], [56, 154], [56, 220], [57, 83], [57, 125], [57, 131], [58, 133], [58, 219], [59, 68], [59, 221], [60, 126], [60, 196], [60, 243], [61, 106], [61, 174], [61, 191], [62, 126], [62, 239], [63, 128], [64, 67], [64, 183], [64, 218], [65, 75], [65, 82], [65, 165], [66, 71], [66, 212], [67, 80], [68, 115], [68, 171], [69, 95], [69, 120], [70, 108], [70, 123], [70, 188], [71, 225], [72, 79], [72, 98], [73, 107], [73, 142], [74, 94], [74, 116], [74, 136], [75, 105], [76, 78], [76, 174], [77, 83], [77, 197], [77, 247], [78, 167], [78, 248], [79, 215], [79, 231], [80, 145], [80, 223], [81, 164], [81, 168], [81, 198], [82, 92], [82, 125], [83, 244], [84, 235], [85, 112], [85, 206], [86, 121], [86, 236], [87, 90], [87, 150], [88, 134], [88, 169], [89, 128], [89, 240], [90, 252], [91, 99], [91, 241], [92, 102], [92, 132], [93, 104], [93, 170], [93, 188], [94, 184], [95, 106], [95, 141], [96, 148], [96, 242], [96, 254], [97, 161], [97, 233], [97, 253], [98, 155], [99, 141], [100, 187], [100, 199], [100, 237], [101, 107], [101, 203], [102, 232], [104, 201], [104, 229], [105, 132], [105, 190], [106, 167], [107, 209], [108, 201], [108, 254], [109, 145], [109, 173], [109, 222], [110, 142], [110, 200], [110, 249], [111, 126], [112, 192], [113, 115], [113, 229], [114, 118], [114, 203], [116, 156], [116, 157], [117, 220], [118, 182], [119, 159], [119, 207], [120, 150], [121, 243], [122, 137], [122, 150], [122, 181], [123, 148], [123, 181], [124, 134], [124, 195], [124, 243], [125, 172], [127, 250], [128, 211], [129, 183], [129, 199], [129, 223], [130, 230], [131, 165], [132, 239], [133, 198], [133, 238], [134, 236], [135, 154], [135, 230], [136, 185], [137, 216], [137, 252], [138, 140], [138, 248], [139, 251], [140, 202], [140, 253], [141, 153], [143, 169], [143, 171], [143, 250], [144, 185], [144, 215], [145, 228], [146, 153], [146, 240], [146, 241], [147, 149], [148, 216], [149, 231], [151, 177], [152, 242], [153, 202], [155, 165], [155, 217], [156, 249], [158, 226], [158, 250], [159, 183], [160, 175], [160, 205], [161, 177], [162, 237], [163, 200], [164, 173], [166, 192], [167, 202], [168, 214], [168, 222], [169, 221], [170, 174], [170, 226], [171, 227], [172, 197], [172, 232], [175, 218], [176, 194], [176, 213], [176, 251], [177, 204], [178, 213], [178, 234], [179, 234], [180, 189], [180, 222], [182, 225], [184, 210], [185, 249], [186, 212], [188, 191], [189, 193], [189, 244], [193, 242], [193, 247], [195, 210], [195, 221], [196, 208], [196, 210], [197, 252], [199, 207], [200, 209], [201, 245], [204, 238], [205, 206], [208, 239], [211, 225], [211, 241], [214, 244], [216, 247], [226, 227], [227, 229], [228, 246], [234, 235], [235, 237], [240, 253], [248, 251]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_254_18.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_254_18 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
