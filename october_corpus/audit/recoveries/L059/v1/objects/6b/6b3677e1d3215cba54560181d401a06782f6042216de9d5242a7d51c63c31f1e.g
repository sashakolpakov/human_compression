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
D:=P177Graph("VT3_234_34",234,[1, 3, 5, 7, 10, 12, 15, 16, 17, 18, 19, 20, 22, 27, 29, 30, 33, 35, 39, 40, 41, 46, 51, 52, 54, 57, 60, 61, 62, 63, 64, 66, 68, 69, 70, 71, 72, 73, 77, 78, 79, 80, 82, 83, 90, 91, 94, 96, 97, 101, 106, 108, 113, 117, 119, 122, 124, 125, 126, 128, 129, 130, 133, 138, 139, 141, 143, 148, 150, 151, 153, 154, 159, 160, 162, 165, 166, 168, 169, 170, 172, 173, 174, 175, 180, 183, 184, 185, 187, 191, 193, 197, 198, 199, 202, 203, 205, 206, 207, 208, 209, 210, 212, 213, 215, 216, 217, 218, 220, 222, 223, 226, 228, 230, 232, 233, 234],[[1, 26], [1, 85], [1, 145], [2, 18], [2, 80], [2, 143], [3, 76], [3, 100], [3, 171], [4, 33], [4, 97], [4, 159], [5, 14], [5, 145], [5, 231], [6, 22], [6, 52], [6, 187], [7, 114], [7, 118], [7, 227], [8, 30], [8, 77], [8, 215], [9, 68], [9, 139], [9, 183], [10, 107], [10, 176], [10, 201], [11, 96], [11, 101], [11, 129], [12, 31], [12, 121], [12, 189], [13, 19], [13, 83], [13, 183], [14, 150], [14, 170], [15, 34], [15, 81], [15, 114], [16, 37], [16, 167], [16, 211], [17, 161], [17, 190], [17, 224], [18, 56], [18, 200], [19, 45], [19, 93], [20, 45], [20, 147], [20, 182], [21, 68], [21, 153], [21, 166], [22, 181], [22, 194], [23, 185], [23, 218], [23, 220], [24, 91], [24, 170], [24, 234], [25, 83], [25, 210], [25, 217], [26, 46], [26, 119], [27, 49], [27, 89], [27, 201], [28, 72], [28, 128], [28, 184], [29, 85], [29, 115], [29, 163], [30, 55], [30, 136], [31, 193], [31, 206], [32, 91], [32, 187], [32, 198], [33, 145], [33, 188], [34, 70], [34, 72], [35, 44], [35, 112], [35, 167], [36, 69], [36, 141], [36, 197], [37, 51], [37, 128], [38, 94], [38, 175], [38, 233], [39, 164], [39, 177], [39, 204], [40, 114], [40, 171], [40, 186], [41, 58], [41, 100], [41, 102], [42, 54], [42, 57], [42, 217], [43, 124], [43, 141], [43, 143], [44, 169], [44, 180], [45, 68], [46, 67], [46, 163], [47, 66], [47, 96], [47, 193], [48, 54], [48, 172], [48, 223], [49, 185], [49, 228], [50, 71], [50, 220], [50, 234], [51, 135], [51, 144], [52, 92], [52, 111], [53, 101], [53, 108], [53, 151], [54, 225], [55, 113], [55, 174], [56, 205], [56, 226], [57, 178], [57, 227], [58, 63], [58, 173], [59, 60], [59, 78], [59, 233], [60, 137], [60, 176], [61, 121], [61, 134], [61, 182], [62, 67], [62, 196], [62, 219], [63, 76], [63, 149], [64, 111], [64, 127], [64, 181], [65, 185], [65, 191], [65, 208], [66, 144], [66, 146], [67, 203], [69, 140], [69, 204], [70, 123], [70, 186], [71, 155], [71, 156], [72, 192], [73, 99], [73, 110], [73, 229], [74, 90], [74, 139], [74, 226], [75, 83], [75, 122], [75, 230], [76, 207], [77, 84], [77, 110], [78, 84], [78, 136], [79, 120], [79, 134], [79, 189], [80, 86], [80, 104], [81, 180], [81, 184], [82, 86], [82, 140], [82, 179], [84, 175], [85, 150], [86, 154], [87, 187], [87, 218], [87, 234], [88, 169], [88, 202], [88, 228], [89, 216], [89, 220], [90, 161], [90, 200], [91, 116], [92, 153], [92, 198], [93, 222], [93, 230], [94, 105], [94, 156], [95, 172], [95, 202], [95, 213], [96, 135], [97, 158], [97, 231], [98, 133], [98, 168], [98, 208], [99, 175], [99, 232], [100, 230], [101, 164], [102, 138], [102, 222], [103, 126], [103, 151], [103, 203], [104, 205], [104, 223], [105, 130], [105, 232], [106, 110], [106, 120], [106, 132], [107, 216], [107, 233], [108, 135], [108, 195], [109, 117], [109, 124], [109, 125], [111, 166], [112, 191], [112, 228], [113, 179], [113, 204], [115, 117], [115, 160], [116, 150], [116, 160], [117, 161], [118, 122], [118, 217], [119, 188], [119, 214], [120, 215], [121, 212], [122, 171], [123, 148], [123, 165], [124, 200], [125, 163], [125, 196], [126, 192], [126, 195], [127, 206], [127, 212], [128, 195], [129, 152], [129, 177], [130, 155], [130, 231], [131, 183], [131, 210], [131, 226], [132, 138], [132, 173], [133, 146], [133, 181], [134, 138], [136, 199], [137, 154], [137, 199], [139, 224], [140, 143], [141, 196], [142, 162], [142, 174], [142, 215], [144, 168], [146, 206], [147, 166], [147, 212], [148, 157], [148, 188], [149, 159], [149, 209], [151, 219], [152, 162], [152, 193], [153, 224], [154, 221], [155, 170], [156, 216], [157, 159], [157, 207], [158, 209], [158, 232], [160, 190], [162, 189], [164, 197], [165, 192], [165, 214], [167, 184], [168, 211], [169, 178], [172, 178], [173, 229], [174, 177], [176, 213], [179, 199], [180, 227], [182, 222], [186, 207], [190, 198], [191, 211], [194, 208], [194, 218], [197, 219], [201, 202], [203, 214], [205, 225], [209, 229], [210, 225], [213, 221], [221, 223]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_234_34.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_234_34 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
