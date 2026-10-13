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
D:=P177Graph("CSS_210_1",210,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129, 131, 133, 135, 137, 139, 141, 143, 145, 147, 149, 151, 153, 155, 157, 159, 161, 163, 165, 167, 169, 171, 173, 175, 177, 179, 181, 183, 185, 187, 189, 191, 193, 195, 197, 199, 201, 203, 205, 207, 209],[[1, 2], [1, 170], [1, 210], [2, 3], [2, 125], [3, 4], [3, 86], [4, 5], [4, 141], [5, 6], [5, 92], [6, 7], [6, 67], [7, 8], [7, 156], [8, 9], [8, 179], [9, 10], [9, 202], [10, 11], [10, 27], [11, 12], [11, 208], [12, 13], [12, 103], [13, 14], [13, 132], [14, 15], [14, 23], [15, 16], [15, 90], [16, 17], [16, 115], [17, 18], [17, 174], [18, 19], [18, 199], [19, 20], [19, 48], [20, 21], [20, 61], [21, 22], [21, 94], [22, 23], [22, 39], [23, 24], [24, 25], [24, 77], [25, 26], [25, 136], [26, 27], [26, 153], [27, 28], [28, 29], [28, 41], [29, 30], [29, 68], [30, 31], [30, 165], [31, 32], [31, 200], [32, 33], [32, 155], [33, 34], [33, 116], [34, 35], [34, 171], [35, 36], [35, 122], [36, 37], [36, 97], [37, 38], [37, 186], [38, 39], [38, 209], [39, 40], [40, 41], [40, 57], [41, 42], [42, 43], [42, 133], [43, 44], [43, 162], [44, 45], [44, 53], [45, 46], [45, 120], [46, 47], [46, 145], [47, 48], [47, 204], [48, 49], [49, 50], [49, 78], [50, 51], [50, 91], [51, 52], [51, 124], [52, 53], [52, 69], [53, 54], [54, 55], [54, 107], [55, 56], [55, 166], [56, 57], [56, 183], [57, 58], [58, 59], [58, 71], [59, 60], [59, 98], [60, 61], [60, 195], [61, 62], [62, 63], [62, 185], [63, 64], [63, 146], [64, 65], [64, 201], [65, 66], [65, 152], [66, 67], [66, 127], [67, 68], [68, 69], [69, 70], [70, 71], [70, 87], [71, 72], [72, 73], [72, 163], [73, 74], [73, 192], [74, 75], [74, 83], [75, 76], [75, 150], [76, 77], [76, 175], [77, 78], [78, 79], [79, 80], [79, 108], [80, 81], [80, 121], [81, 82], [81, 154], [82, 83], [82, 99], [83, 84], [84, 85], [84, 137], [85, 86], [85, 196], [86, 87], [87, 88], [88, 89], [88, 101], [89, 90], [89, 128], [90, 91], [91, 92], [92, 93], [93, 94], [93, 176], [94, 95], [95, 96], [95, 182], [96, 97], [96, 157], [97, 98], [98, 99], [99, 100], [100, 101], [100, 117], [101, 102], [102, 103], [102, 193], [103, 104], [104, 105], [104, 113], [105, 106], [105, 180], [106, 107], [106, 205], [107, 108], [108, 109], [109, 110], [109, 138], [110, 111], [110, 151], [111, 112], [111, 184], [112, 113], [112, 129], [113, 114], [114, 115], [114, 167], [115, 116], [116, 117], [117, 118], [118, 119], [118, 131], [119, 120], [119, 158], [120, 121], [121, 122], [122, 123], [123, 124], [123, 206], [124, 125], [125, 126], [126, 127], [126, 187], [127, 128], [128, 129], [129, 130], [130, 131], [130, 147], [131, 132], [132, 133], [133, 134], [134, 135], [134, 143], [135, 136], [135, 210], [136, 137], [137, 138], [138, 139], [139, 140], [139, 168], [140, 141], [140, 181], [141, 142], [142, 143], [142, 159], [143, 144], [144, 145], [144, 197], [145, 146], [146, 147], [147, 148], [148, 149], [148, 161], [149, 150], [149, 188], [150, 151], [151, 152], [152, 153], [153, 154], [154, 155], [155, 156], [156, 157], [157, 158], [158, 159], [159, 160], [160, 161], [160, 177], [161, 162], [162, 163], [163, 164], [164, 165], [164, 173], [165, 166], [166, 167], [167, 168], [168, 169], [169, 170], [169, 198], [170, 171], [171, 172], [172, 173], [172, 189], [173, 174], [174, 175], [175, 176], [176, 177], [177, 178], [178, 179], [178, 191], [179, 180], [180, 181], [181, 182], [182, 183], [183, 184], [184, 185], [185, 186], [186, 187], [187, 188], [188, 189], [189, 190], [190, 191], [190, 207], [191, 192], [192, 193], [193, 194], [194, 195], [194, 203], [195, 196], [196, 197], [197, 198], [198, 199], [199, 200], [200, 201], [201, 202], [202, 203], [203, 204], [204, 205], [205, 206], [206, 207], [207, 208], [208, 209], [209, 210]]);;
R:=P177Census(D);;
Need(Size(R.F)=Size(R.A));;
PrintTo("cubic_markings/CSS_210_1.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE CSS_210_1 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
