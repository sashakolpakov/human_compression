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
D:=P177Graph("VT3_220_4",220,[1, 2, 3, 4, 5, 8, 12, 13, 14, 17, 18, 21, 22, 23, 28, 29, 32, 35, 37, 38, 41, 42, 43, 49, 50, 51, 52, 60, 62, 64, 65, 66, 67, 68, 73, 74, 75, 76, 77, 79, 80, 81, 82, 83, 85, 86, 88, 91, 92, 94, 95, 97, 98, 99, 102, 104, 105, 108, 110, 111, 116, 117, 119, 120, 122, 123, 125, 127, 130, 135, 137, 139, 141, 142, 143, 144, 146, 154, 155, 157, 158, 163, 164, 165, 166, 168, 173, 175, 177, 178, 184, 185, 186, 190, 197, 200, 202, 203, 204, 205, 207, 209, 210, 212, 213, 214, 215, 216, 218, 219],[[1, 30], [1, 176], [1, 192], [2, 103], [2, 132], [2, 159], [3, 71], [3, 153], [3, 206], [4, 33], [4, 53], [4, 118], [5, 84], [5, 133], [5, 201], [6, 119], [6, 141], [6, 165], [7, 13], [7, 123], [7, 178], [8, 47], [8, 54], [8, 179], [9, 17], [9, 79], [9, 205], [10, 68], [10, 135], [10, 212], [11, 22], [11, 157], [11, 185], [12, 20], [12, 44], [12, 180], [13, 20], [13, 30], [14, 27], [14, 54], [14, 195], [15, 17], [15, 66], [15, 97], [16, 127], [16, 155], [16, 205], [17, 191], [18, 103], [18, 161], [18, 217], [19, 68], [19, 91], [19, 190], [20, 79], [21, 26], [21, 59], [21, 188], [22, 58], [22, 100], [23, 39], [23, 45], [23, 136], [24, 28], [24, 98], [24, 215], [25, 127], [25, 164], [25, 165], [26, 67], [26, 95], [27, 66], [27, 178], [28, 107], [28, 160], [29, 55], [29, 112], [29, 115], [30, 184], [31, 64], [31, 197], [31, 200], [32, 90], [32, 106], [32, 217], [33, 143], [33, 207], [34, 43], [34, 123], [34, 139], [35, 133], [35, 156], [35, 169], [36, 49], [36, 94], [36, 186], [37, 101], [37, 109], [37, 181], [38, 63], [38, 93], [38, 129], [39, 120], [39, 142], [40, 62], [40, 80], [40, 185], [41, 134], [41, 174], [41, 198], [42, 96], [42, 189], [42, 196], [43, 121], [43, 220], [44, 94], [44, 111], [45, 62], [45, 79], [46, 83], [46, 127], [46, 209], [47, 122], [47, 125], [48, 64], [48, 77], [48, 81], [49, 63], [49, 87], [50, 56], [50, 70], [50, 147], [51, 84], [51, 149], [51, 191], [52, 161], [52, 172], [52, 208], [53, 82], [53, 219], [54, 135], [55, 88], [55, 104], [56, 75], [56, 98], [57, 60], [57, 125], [57, 166], [58, 74], [58, 175], [59, 80], [59, 154], [60, 167], [60, 183], [61, 95], [61, 105], [61, 125], [62, 152], [63, 210], [64, 113], [65, 121], [65, 126], [65, 195], [66, 93], [67, 69], [67, 193], [68, 192], [69, 155], [69, 203], [70, 146], [70, 163], [71, 92], [71, 139], [72, 81], [72, 214], [72, 216], [73, 126], [73, 182], [73, 196], [74, 153], [74, 211], [75, 179], [75, 182], [76, 114], [76, 148], [76, 199], [77, 134], [77, 167], [78, 110], [78, 120], [78, 135], [80, 126], [81, 112], [82, 93], [82, 188], [83, 129], [83, 189], [84, 102], [85, 134], [85, 162], [85, 170], [86, 115], [86, 152], [86, 156], [87, 157], [87, 202], [88, 118], [88, 192], [89, 91], [89, 116], [89, 186], [90, 99], [90, 146], [91, 172], [92, 109], [92, 162], [94, 114], [95, 150], [96, 142], [96, 146], [97, 113], [97, 171], [98, 198], [99, 100], [99, 114], [100, 143], [101, 117], [101, 209], [102, 170], [102, 188], [103, 108], [104, 147], [104, 171], [105, 147], [105, 199], [106, 173], [106, 213], [107, 197], [107, 218], [108, 115], [108, 150], [109, 122], [110, 129], [110, 174], [111, 140], [111, 174], [112, 120], [113, 157], [116, 179], [116, 206], [117, 145], [117, 208], [118, 215], [119, 160], [119, 201], [121, 214], [122, 136], [123, 169], [124, 190], [124, 200], [124, 209], [128, 130], [128, 137], [128, 144], [130, 176], [130, 194], [131, 166], [131, 175], [131, 213], [132, 184], [132, 202], [133, 177], [136, 173], [137, 149], [137, 151], [138, 173], [138, 184], [138, 200], [139, 140], [140, 204], [141, 145], [141, 195], [142, 149], [143, 156], [144, 169], [144, 181], [145, 158], [148, 177], [148, 190], [150, 210], [151, 186], [151, 216], [152, 165], [153, 155], [154, 180], [154, 187], [158, 171], [158, 194], [159, 164], [159, 168], [160, 213], [161, 214], [162, 185], [163, 170], [163, 208], [164, 198], [166, 187], [167, 177], [168, 183], [168, 211], [172, 219], [175, 194], [176, 203], [178, 183], [180, 215], [181, 210], [182, 202], [187, 216], [189, 207], [191, 218], [193, 204], [193, 212], [196, 203], [197, 220], [199, 205], [201, 212], [204, 217], [206, 218], [207, 220], [211, 219]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_220_4.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_220_4 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
