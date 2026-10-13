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
D:=P177Graph("VT3_222_1",222,[1, 3, 8, 10, 12, 13, 14, 16, 17, 20, 24, 27, 28, 32, 33, 34, 36, 37, 38, 40, 41, 42, 47, 50, 51, 52, 53, 54, 56, 57, 58, 61, 63, 64, 65, 66, 74, 78, 82, 84, 86, 90, 92, 93, 95, 98, 99, 100, 101, 102, 105, 106, 107, 109, 110, 114, 117, 118, 119, 121, 122, 125, 127, 129, 130, 131, 133, 136, 137, 138, 140, 143, 144, 147, 148, 150, 153, 155, 156, 158, 159, 161, 163, 164, 165, 167, 168, 171, 176, 177, 180, 181, 182, 184, 188, 189, 190, 191, 192, 194, 195, 197, 205, 206, 207, 210, 211, 213, 214, 219, 220],[[1, 26], [1, 62], [1, 218], [2, 95], [2, 101], [2, 219], [3, 81], [3, 170], [3, 215], [4, 125], [4, 153], [4, 213], [5, 98], [5, 129], [5, 211], [6, 63], [6, 99], [6, 109], [7, 8], [7, 61], [7, 158], [8, 35], [8, 94], [9, 163], [9, 165], [9, 180], [10, 25], [10, 120], [10, 126], [11, 100], [11, 177], [11, 184], [12, 160], [12, 175], [12, 203], [13, 67], [13, 71], [13, 79], [14, 22], [14, 142], [14, 185], [15, 34], [15, 107], [15, 147], [16, 31], [16, 55], [16, 123], [17, 60], [17, 67], [17, 141], [18, 90], [18, 105], [18, 125], [19, 114], [19, 131], [19, 167], [20, 45], [20, 62], [20, 69], [21, 117], [21, 121], [21, 190], [22, 119], [22, 150], [23, 99], [23, 176], [23, 188], [24, 108], [24, 174], [24, 196], [25, 117], [25, 210], [26, 92], [26, 127], [27, 60], [27, 135], [27, 203], [28, 35], [28, 173], [28, 175], [29, 131], [29, 136], [29, 197], [30, 159], [30, 163], [30, 206], [31, 36], [31, 171], [32, 49], [32, 124], [32, 179], [33, 97], [33, 124], [33, 149], [34, 173], [34, 212], [35, 66], [36, 44], [36, 185], [37, 83], [37, 145], [37, 201], [38, 59], [38, 83], [38, 132], [39, 51], [39, 58], [39, 129], [40, 134], [40, 169], [40, 170], [41, 108], [41, 113], [41, 222], [42, 72], [42, 126], [42, 128], [43, 95], [43, 99], [43, 133], [44, 57], [44, 119], [45, 127], [45, 182], [46, 51], [46, 121], [46, 210], [47, 59], [47, 178], [47, 187], [48, 119], [48, 144], [48, 189], [49, 54], [49, 195], [50, 157], [50, 216], [50, 217], [51, 146], [52, 77], [52, 81], [52, 134], [53, 132], [53, 169], [53, 178], [54, 83], [54, 115], [55, 136], [55, 167], [56, 132], [56, 134], [56, 201], [57, 186], [57, 222], [58, 75], [58, 154], [59, 195], [60, 106], [61, 128], [61, 151], [62, 118], [63, 85], [63, 103], [64, 113], [64, 174], [64, 216], [65, 85], [65, 179], [65, 204], [66, 80], [66, 160], [67, 176], [68, 140], [68, 156], [68, 219], [69, 130], [69, 194], [70, 74], [70, 93], [70, 105], [71, 188], [71, 207], [72, 90], [72, 137], [73, 93], [73, 143], [73, 189], [74, 115], [74, 145], [75, 86], [75, 100], [76, 127], [76, 164], [76, 220], [77, 110], [77, 153], [78, 87], [78, 208], [78, 209], [79, 106], [79, 181], [80, 117], [80, 158], [81, 86], [82, 96], [82, 157], [82, 199], [84, 187], [84, 193], [84, 204], [85, 220], [86, 146], [87, 114], [87, 214], [88, 164], [88, 182], [88, 219], [89, 106], [89, 155], [89, 206], [90, 120], [91, 98], [91, 101], [91, 133], [92, 139], [92, 193], [93, 200], [94, 118], [94, 205], [95, 103], [96, 184], [96, 197], [97, 109], [97, 188], [98, 154], [100, 215], [101, 183], [102, 116], [102, 128], [102, 196], [103, 164], [104, 150], [104, 181], [104, 207], [105, 166], [107, 152], [107, 209], [108, 168], [109, 179], [110, 146], [110, 202], [111, 121], [111, 129], [111, 138], [112, 133], [112, 176], [112, 211], [113, 161], [114, 169], [115, 148], [116, 137], [116, 168], [118, 151], [120, 213], [122, 139], [122, 152], [122, 187], [123, 159], [123, 165], [124, 148], [125, 145], [126, 158], [130, 162], [130, 174], [131, 170], [135, 138], [135, 190], [136, 199], [137, 166], [138, 141], [139, 147], [140, 162], [140, 216], [141, 211], [142, 181], [142, 206], [143, 166], [143, 221], [144, 221], [144, 222], [147, 218], [148, 200], [149, 191], [149, 207], [150, 172], [151, 194], [152, 214], [153, 201], [154, 177], [155, 198], [155, 203], [156, 183], [156, 217], [157, 161], [159, 185], [160, 190], [161, 186], [162, 182], [163, 198], [165, 208], [167, 208], [168, 221], [171, 186], [171, 199], [172, 189], [172, 191], [173, 205], [175, 192], [177, 183], [178, 214], [180, 209], [180, 212], [184, 217], [191, 200], [192, 198], [192, 212], [193, 220], [194, 196], [195, 204], [197, 215], [202, 210], [202, 213], [205, 218]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_222_1.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_222_1 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
