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
D:=P177Graph("VT3_240_110",240,[1, 3, 4, 5, 11, 12, 16, 17, 18, 19, 20, 26, 28, 31, 32, 33, 35, 36, 39, 42, 45, 46, 47, 49, 51, 53, 59, 61, 62, 63, 64, 67, 69, 71, 72, 74, 75, 76, 79, 80, 81, 82, 83, 84, 85, 88, 92, 93, 97, 100, 103, 104, 105, 107, 108, 109, 113, 122, 124, 127, 128, 129, 130, 132, 136, 139, 140, 142, 145, 148, 150, 151, 152, 153, 154, 155, 157, 160, 162, 163, 164, 166, 167, 170, 173, 174, 178, 179, 180, 182, 183, 184, 187, 189, 193, 195, 198, 202, 204, 208, 210, 211, 212, 214, 215, 216, 217, 219, 220, 221, 223, 225, 226, 227, 228, 230, 234, 236, 237, 240],[[1, 66], [1, 141], [1, 235], [2, 47], [2, 107], [2, 130], [3, 27], [3, 70], [3, 185], [4, 65], [4, 138], [4, 158], [5, 114], [5, 133], [5, 222], [6, 12], [6, 170], [6, 183], [7, 31], [7, 107], [7, 173], [8, 142], [8, 198], [8, 208], [9, 88], [9, 105], [9, 136], [10, 19], [10, 166], [10, 174], [11, 24], [11, 112], [11, 188], [12, 120], [12, 191], [13, 35], [13, 45], [13, 164], [14, 103], [14, 104], [14, 130], [15, 49], [15, 221], [15, 234], [16, 110], [16, 147], [16, 201], [17, 106], [17, 119], [17, 207], [18, 54], [18, 120], [18, 146], [19, 44], [19, 117], [20, 48], [20, 68], [20, 91], [21, 83], [21, 140], [21, 195], [22, 92], [22, 167], [22, 230], [23, 79], [23, 180], [23, 214], [24, 46], [24, 81], [25, 140], [25, 163], [25, 189], [26, 86], [26, 118], [26, 137], [27, 39], [27, 108], [28, 78], [28, 168], [28, 239], [29, 109], [29, 173], [29, 216], [30, 217], [30, 219], [30, 221], [31, 89], [31, 95], [32, 48], [32, 116], [32, 238], [33, 91], [33, 99], [33, 186], [34, 92], [34, 155], [34, 163], [35, 44], [35, 77], [36, 55], [36, 77], [36, 95], [37, 93], [37, 217], [37, 240], [38, 72], [38, 184], [38, 237], [39, 123], [39, 224], [40, 113], [40, 122], [40, 164], [41, 64], [41, 128], [41, 142], [42, 68], [42, 196], [42, 205], [43, 53], [43, 85], [43, 124], [44, 167], [45, 66], [45, 233], [46, 110], [46, 144], [47, 86], [47, 192], [48, 97], [49, 144], [49, 206], [50, 72], [50, 100], [50, 225], [51, 176], [51, 200], [51, 232], [52, 124], [52, 154], [52, 212], [53, 115], [53, 203], [54, 153], [54, 210], [55, 136], [55, 198], [56, 75], [56, 76], [56, 223], [57, 109], [57, 139], [57, 180], [58, 155], [58, 166], [58, 214], [59, 70], [59, 141], [59, 199], [60, 219], [60, 223], [60, 226], [61, 181], [61, 222], [61, 233], [62, 196], [62, 201], [62, 239], [63, 70], [63, 87], [63, 190], [64, 175], [64, 224], [65, 162], [65, 230], [66, 180], [67, 137], [67, 191], [67, 218], [68, 164], [69, 120], [69, 158], [69, 209], [71, 94], [71, 172], [71, 235], [72, 188], [73, 81], [73, 132], [73, 220], [74, 144], [74, 222], [74, 232], [75, 149], [75, 199], [76, 126], [76, 206], [77, 220], [78, 128], [78, 211], [79, 90], [79, 156], [80, 106], [80, 194], [80, 200], [81, 141], [82, 125], [82, 177], [82, 213], [83, 165], [83, 192], [84, 89], [84, 117], [84, 171], [85, 135], [85, 238], [86, 124], [87, 129], [87, 160], [88, 98], [88, 126], [89, 183], [90, 113], [90, 129], [91, 182], [92, 238], [93, 134], [93, 168], [94, 108], [94, 187], [95, 214], [96, 127], [96, 130], [96, 162], [97, 138], [97, 147], [98, 108], [98, 204], [99, 234], [99, 236], [100, 114], [100, 207], [101, 139], [101, 187], [101, 220], [102, 128], [102, 204], [102, 219], [103, 159], [103, 191], [104, 135], [104, 161], [105, 175], [105, 229], [106, 182], [107, 209], [109, 111], [110, 151], [111, 170], [111, 198], [112, 150], [112, 223], [113, 114], [115, 140], [115, 173], [116, 127], [116, 221], [117, 145], [118, 189], [118, 225], [119, 155], [119, 216], [121, 136], [121, 145], [121, 151], [122, 131], [122, 200], [123, 184], [123, 210], [125, 204], [125, 237], [126, 228], [127, 146], [129, 231], [131, 227], [131, 234], [132, 181], [132, 205], [133, 150], [133, 152], [134, 153], [134, 208], [135, 236], [137, 148], [138, 211], [139, 229], [142, 171], [143, 153], [143, 179], [143, 202], [145, 205], [146, 193], [147, 227], [148, 172], [148, 190], [149, 151], [149, 187], [150, 213], [152, 169], [152, 194], [154, 176], [154, 186], [156, 167], [156, 182], [157, 165], [157, 231], [157, 235], [158, 217], [159, 179], [159, 212], [160, 188], [160, 233], [161, 210], [161, 215], [162, 203], [163, 186], [165, 178], [166, 203], [168, 183], [169, 184], [169, 212], [170, 192], [171, 228], [172, 202], [174, 209], [174, 239], [175, 202], [176, 215], [177, 193], [177, 240], [178, 218], [178, 229], [179, 185], [181, 227], [185, 225], [189, 194], [190, 195], [193, 197], [195, 207], [196, 230], [197, 226], [197, 236], [199, 237], [201, 228], [206, 211], [208, 218], [213, 215], [216, 231], [224, 240], [226, 232]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_240_110.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_240_110 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
