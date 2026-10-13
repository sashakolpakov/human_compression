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
D:=P177Graph("VT3_224_51",224,[1, 5, 11, 12, 13, 14, 15, 17, 18, 19, 23, 26, 31, 32, 33, 35, 36, 37, 38, 40, 42, 45, 46, 47, 48, 49, 51, 53, 54, 57, 58, 59, 62, 64, 65, 67, 70, 71, 72, 73, 75, 76, 79, 82, 83, 86, 88, 89, 91, 95, 96, 97, 98, 100, 101, 103, 105, 110, 112, 113, 116, 118, 120, 122, 123, 124, 125, 126, 128, 129, 131, 132, 133, 136, 139, 141, 142, 143, 145, 148, 149, 155, 156, 159, 163, 164, 165, 166, 167, 168, 171, 173, 177, 179, 182, 184, 186, 187, 188, 192, 194, 195, 196, 198, 202, 204, 205, 217, 220, 221, 222, 224],[[1, 50], [1, 63], [1, 203], [2, 33], [2, 73], [2, 168], [3, 40], [3, 82], [3, 221], [4, 17], [4, 88], [4, 89], [5, 52], [5, 185], [5, 191], [6, 15], [6, 148], [6, 217], [7, 47], [7, 83], [7, 120], [8, 18], [8, 129], [8, 220], [9, 103], [9, 128], [9, 196], [10, 12], [10, 46], [10, 156], [11, 107], [11, 138], [11, 162], [12, 81], [12, 210], [13, 25], [13, 34], [13, 74], [14, 29], [14, 69], [14, 152], [15, 87], [15, 162], [16, 46], [16, 101], [16, 194], [17, 109], [17, 189], [18, 56], [18, 161], [19, 66], [19, 175], [19, 219], [20, 51], [20, 103], [20, 148], [21, 105], [21, 118], [21, 182], [22, 97], [22, 100], [22, 192], [23, 90], [23, 106], [23, 127], [24, 47], [24, 105], [24, 110], [25, 82], [25, 133], [26, 152], [26, 203], [26, 207], [27, 45], [27, 48], [27, 179], [28, 36], [28, 145], [28, 173], [29, 101], [29, 165], [30, 46], [30, 59], [30, 168], [31, 66], [31, 130], [31, 151], [32, 43], [32, 107], [32, 154], [33, 50], [33, 172], [34, 58], [34, 198], [35, 138], [35, 211], [35, 213], [36, 210], [36, 218], [37, 55], [37, 199], [37, 216], [38, 55], [38, 137], [38, 144], [39, 86], [39, 128], [39, 171], [40, 74], [40, 170], [41, 141], [41, 179], [41, 221], [42, 158], [42, 176], [42, 216], [43, 73], [43, 139], [44, 67], [44, 143], [44, 198], [45, 94], [45, 115], [47, 147], [48, 99], [48, 208], [49, 80], [49, 134], [49, 152], [50, 59], [51, 106], [51, 119], [52, 58], [52, 100], [53, 56], [53, 185], [53, 193], [54, 84], [54, 108], [54, 206], [55, 182], [56, 177], [57, 92], [57, 181], [57, 185], [58, 92], [59, 207], [60, 88], [60, 95], [60, 222], [61, 76], [61, 142], [61, 188], [62, 69], [62, 80], [62, 161], [63, 186], [63, 195], [64, 77], [64, 117], [64, 127], [65, 78], [65, 140], [65, 215], [66, 125], [67, 84], [67, 92], [68, 89], [68, 113], [68, 118], [69, 220], [70, 114], [70, 180], [70, 189], [71, 115], [71, 130], [71, 219], [72, 109], [72, 180], [72, 211], [73, 162], [74, 100], [75, 146], [75, 147], [75, 178], [76, 78], [76, 150], [77, 110], [77, 118], [78, 128], [79, 111], [79, 183], [79, 214], [80, 83], [81, 142], [81, 202], [82, 223], [83, 157], [84, 167], [85, 166], [85, 179], [85, 188], [86, 140], [86, 212], [87, 156], [87, 168], [88, 153], [89, 117], [90, 96], [90, 159], [91, 160], [91, 199], [91, 209], [93, 112], [93, 133], [93, 164], [94, 145], [94, 166], [95, 151], [95, 189], [96, 109], [96, 117], [97, 191], [97, 212], [98, 107], [98, 206], [98, 213], [99, 163], [99, 221], [101, 207], [102, 122], [102, 133], [102, 198], [103, 150], [104, 116], [104, 204], [104, 205], [105, 144], [106, 196], [108, 126], [108, 132], [110, 178], [111, 132], [111, 167], [112, 158], [112, 174], [113, 153], [113, 160], [114, 132], [114, 224], [115, 149], [116, 146], [116, 212], [119, 159], [119, 217], [120, 134], [120, 144], [121, 131], [121, 171], [121, 196], [122, 154], [122, 174], [123, 134], [123, 137], [123, 203], [124, 153], [124, 169], [124, 209], [125, 183], [125, 190], [126, 180], [126, 213], [127, 131], [129, 190], [129, 214], [130, 222], [131, 178], [135, 136], [135, 163], [135, 187], [136, 176], [136, 199], [137, 195], [138, 217], [139, 172], [139, 174], [140, 192], [141, 170], [141, 215], [142, 218], [143, 154], [143, 206], [145, 219], [146, 171], [147, 205], [148, 200], [149, 169], [149, 208], [150, 202], [151, 224], [155, 157], [155, 161], [155, 193], [156, 200], [157, 205], [158, 186], [159, 211], [160, 182], [163, 223], [164, 176], [164, 223], [165, 197], [165, 201], [166, 218], [167, 181], [169, 222], [170, 192], [172, 186], [173, 175], [173, 197], [175, 184], [177, 181], [177, 214], [183, 224], [184, 190], [184, 201], [187, 208], [187, 209], [188, 215], [191, 204], [193, 204], [194, 197], [194, 210], [195, 216], [200, 202], [201, 220]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_224_51.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_224_51 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
