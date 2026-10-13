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
D:=P177Graph("VT3_242_25",242,[1, 2, 3, 6, 7, 10, 11, 12, 15, 16, 20, 23, 28, 29, 30, 31, 33, 34, 37, 38, 40, 41, 44, 50, 53, 54, 57, 58, 61, 62, 64, 66, 67, 69, 70, 76, 77, 78, 80, 81, 82, 84, 85, 87, 88, 89, 90, 91, 92, 93, 95, 97, 101, 103, 104, 105, 108, 109, 112, 114, 117, 118, 119, 124, 125, 127, 129, 131, 132, 133, 134, 135, 137, 139, 142, 143, 144, 145, 151, 155, 159, 162, 163, 165, 166, 172, 174, 175, 177, 180, 182, 183, 184, 185, 186, 187, 188, 191, 192, 194, 197, 201, 203, 205, 206, 207, 213, 214, 217, 218, 219, 221, 222, 228, 229, 231, 232, 234, 236, 239, 240],[[1, 36], [1, 45], [1, 190], [2, 102], [2, 141], [2, 220], [3, 39], [3, 43], [3, 68], [4, 82], [4, 108], [4, 163], [5, 40], [5, 85], [5, 91], [6, 65], [6, 160], [6, 210], [7, 120], [7, 161], [7, 167], [8, 67], [8, 180], [8, 236], [9, 104], [9, 151], [9, 213], [10, 32], [10, 140], [10, 170], [11, 106], [11, 195], [11, 227], [12, 83], [12, 208], [12, 237], [13, 50], [13, 88], [13, 221], [14, 84], [14, 101], [14, 129], [15, 73], [15, 160], [15, 164], [16, 36], [16, 110], [16, 148], [17, 34], [17, 143], [17, 192], [18, 34], [18, 57], [18, 142], [19, 144], [19, 228], [19, 236], [20, 39], [20, 42], [20, 168], [21, 174], [21, 207], [21, 240], [22, 23], [22, 66], [22, 145], [23, 94], [23, 224], [24, 80], [24, 81], [24, 231], [25, 38], [25, 103], [25, 177], [26, 44], [26, 97], [26, 101], [27, 81], [27, 180], [27, 205], [28, 43], [28, 130], [28, 176], [29, 72], [29, 223], [29, 225], [30, 46], [30, 99], [30, 178], [31, 83], [31, 199], [31, 238], [32, 163], [32, 174], [33, 86], [33, 136], [33, 198], [34, 107], [35, 137], [35, 201], [35, 217], [36, 37], [37, 152], [37, 169], [38, 171], [38, 233], [39, 41], [40, 68], [40, 130], [41, 179], [41, 204], [42, 105], [42, 221], [43, 203], [44, 72], [44, 116], [45, 78], [45, 127], [46, 64], [46, 137], [47, 67], [47, 144], [47, 207], [48, 70], [48, 77], [48, 183], [49, 119], [49, 188], [49, 239], [50, 164], [50, 227], [51, 188], [51, 194], [51, 201], [52, 101], [52, 218], [52, 231], [53, 60], [53, 141], [53, 241], [54, 150], [54, 208], [54, 238], [55, 78], [55, 108], [55, 182], [56, 62], [56, 109], [56, 183], [57, 128], [57, 136], [58, 96], [58, 98], [58, 123], [59, 92], [59, 114], [59, 186], [60, 175], [60, 219], [61, 158], [61, 202], [61, 235], [62, 181], [62, 199], [63, 67], [63, 105], [63, 205], [64, 121], [64, 153], [65, 76], [65, 165], [66, 113], [66, 148], [68, 87], [69, 128], [69, 130], [69, 157], [70, 170], [70, 181], [71, 76], [71, 87], [71, 91], [72, 218], [73, 76], [73, 88], [74, 145], [74, 162], [74, 177], [75, 125], [75, 151], [75, 159], [77, 140], [77, 212], [78, 212], [79, 90], [79, 95], [79, 129], [80, 115], [80, 227], [81, 200], [82, 102], [82, 241], [83, 109], [84, 96], [84, 193], [85, 107], [85, 128], [86, 114], [86, 222], [87, 168], [88, 168], [89, 156], [89, 171], [89, 224], [90, 195], [90, 233], [91, 100], [92, 150], [92, 198], [93, 99], [93, 121], [93, 238], [94, 127], [94, 132], [95, 96], [95, 215], [97, 161], [97, 193], [98, 114], [98, 232], [99, 206], [100, 165], [100, 166], [102, 182], [103, 164], [103, 195], [104, 158], [104, 210], [105, 204], [106, 129], [106, 231], [107, 166], [108, 140], [109, 209], [110, 159], [110, 213], [111, 119], [111, 139], [111, 194], [112, 220], [112, 226], [112, 230], [113, 162], [113, 213], [115, 205], [115, 221], [116, 191], [116, 234], [117, 189], [117, 209], [117, 224], [118, 149], [118, 152], [118, 216], [119, 225], [120, 184], [120, 219], [121, 185], [122, 124], [122, 185], [122, 228], [123, 134], [123, 186], [124, 146], [124, 181], [125, 196], [125, 216], [126, 180], [126, 214], [126, 239], [127, 148], [131, 136], [131, 157], [131, 173], [132, 189], [132, 212], [133, 156], [133, 215], [133, 233], [134, 215], [134, 237], [135, 147], [135, 196], [135, 202], [137, 242], [138, 142], [138, 192], [138, 206], [139, 149], [139, 223], [141, 184], [142, 198], [143, 147], [143, 235], [144, 146], [145, 171], [146, 240], [147, 217], [149, 197], [150, 206], [151, 202], [152, 159], [153, 228], [153, 229], [154, 155], [154, 163], [154, 203], [155, 176], [155, 241], [156, 172], [157, 175], [158, 165], [160, 177], [161, 191], [162, 210], [166, 235], [167, 222], [167, 232], [169, 187], [169, 197], [170, 240], [172, 209], [172, 237], [173, 219], [173, 222], [174, 179], [175, 176], [178, 192], [178, 217], [179, 203], [182, 190], [183, 189], [184, 226], [185, 199], [186, 208], [187, 190], [187, 220], [188, 242], [191, 226], [193, 232], [194, 216], [196, 201], [197, 230], [200, 214], [200, 218], [204, 207], [211, 229], [211, 236], [211, 239], [214, 225], [223, 234], [229, 242], [230, 234]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_242_25.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_242_25 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
