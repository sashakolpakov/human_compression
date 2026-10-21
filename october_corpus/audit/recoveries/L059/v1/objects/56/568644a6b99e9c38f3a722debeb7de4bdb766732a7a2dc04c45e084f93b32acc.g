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
D:=P177Graph("VT3_216_138",216,[1, 2, 3, 5, 6, 7, 8, 9, 10, 12, 13, 15, 16, 17, 19, 21, 23, 24, 26, 30, 35, 37, 38, 43, 44, 45, 49, 50, 52, 53, 54, 55, 57, 58, 66, 68, 72, 79, 81, 87, 88, 90, 91, 93, 94, 95, 96, 98, 100, 101, 103, 104, 106, 107, 108, 109, 111, 114, 116, 121, 122, 123, 125, 126, 132, 135, 136, 137, 138, 140, 141, 148, 149, 150, 151, 154, 158, 159, 160, 162, 166, 170, 171, 172, 173, 174, 176, 177, 179, 180, 181, 185, 188, 189, 190, 191, 192, 196, 197, 198, 200, 203, 204, 207, 211, 212, 213, 215],[[1, 60], [1, 129], [1, 152], [2, 146], [2, 157], [2, 194], [3, 161], [3, 194], [3, 214], [4, 26], [4, 81], [4, 171], [5, 42], [5, 56], [5, 92], [6, 65], [6, 178], [6, 205], [7, 118], [7, 120], [7, 175], [8, 32], [8, 75], [8, 80], [9, 84], [9, 115], [9, 127], [10, 63], [10, 85], [10, 208], [11, 24], [11, 30], [11, 52], [12, 105], [12, 161], [12, 195], [13, 97], [13, 115], [13, 118], [14, 16], [14, 66], [14, 122], [15, 39], [15, 102], [15, 201], [16, 71], [16, 164], [17, 20], [17, 63], [17, 187], [18, 140], [18, 159], [18, 162], [19, 83], [19, 110], [19, 156], [20, 55], [20, 58], [21, 74], [21, 77], [21, 145], [22, 26], [22, 43], [22, 189], [23, 59], [23, 165], [23, 209], [24, 113], [24, 186], [25, 35], [25, 54], [25, 198], [26, 28], [27, 72], [27, 107], [27, 172], [28, 88], [28, 179], [29, 45], [29, 53], [29, 150], [30, 36], [30, 131], [31, 148], [31, 150], [31, 215], [32, 114], [32, 181], [33, 96], [33, 103], [33, 104], [34, 50], [34, 123], [34, 198], [35, 209], [35, 216], [36, 100], [36, 196], [37, 64], [37, 67], [37, 84], [38, 134], [38, 142], [38, 165], [39, 122], [39, 149], [40, 96], [40, 126], [40, 138], [41, 149], [41, 203], [41, 211], [42, 114], [42, 189], [43, 105], [43, 210], [44, 46], [44, 78], [44, 110], [45, 105], [45, 165], [46, 154], [46, 192], [47, 55], [47, 94], [47, 190], [48, 136], [48, 177], [48, 196], [49, 86], [49, 117], [49, 187], [50, 64], [50, 70], [51, 135], [51, 150], [51, 198], [52, 133], [52, 147], [53, 76], [53, 205], [54, 186], [54, 210], [55, 199], [56, 166], [56, 197], [57, 74], [57, 119], [57, 214], [58, 62], [58, 147], [59, 79], [59, 192], [60, 68], [60, 100], [61, 79], [61, 96], [61, 135], [62, 173], [62, 180], [63, 160], [64, 174], [65, 68], [65, 132], [66, 77], [66, 169], [67, 106], [67, 148], [68, 142], [69, 88], [69, 109], [69, 200], [70, 95], [70, 121], [71, 87], [71, 212], [72, 127], [72, 157], [73, 91], [73, 160], [73, 188], [74, 171], [75, 135], [75, 162], [76, 93], [76, 160], [77, 90], [78, 104], [78, 176], [79, 178], [80, 121], [80, 212], [81, 117], [81, 209], [82, 174], [82, 176], [82, 207], [83, 94], [83, 111], [84, 132], [85, 107], [85, 170], [86, 125], [86, 204], [87, 119], [87, 167], [88, 169], [89, 116], [89, 177], [89, 188], [90, 131], [90, 144], [91, 167], [91, 195], [92, 95], [92, 136], [93, 155], [93, 214], [94, 130], [95, 97], [97, 185], [98, 139], [98, 146], [98, 208], [99, 173], [99, 196], [99, 204], [100, 202], [101, 145], [101, 184], [101, 206], [102, 123], [102, 158], [103, 120], [103, 183], [104, 112], [106, 202], [106, 210], [107, 133], [108, 130], [108, 164], [108, 182], [109, 119], [109, 187], [110, 172], [111, 115], [111, 193], [112, 173], [112, 200], [113, 171], [113, 203], [114, 168], [116, 139], [116, 199], [117, 213], [118, 207], [120, 177], [121, 153], [122, 163], [123, 168], [124, 136], [124, 158], [124, 176], [125, 129], [125, 133], [126, 182], [126, 216], [127, 151], [128, 140], [128, 211], [128, 215], [129, 192], [130, 200], [131, 189], [132, 208], [134, 179], [134, 204], [137, 145], [137, 146], [137, 147], [138, 168], [138, 169], [139, 166], [140, 164], [141, 152], [141, 186], [141, 201], [142, 188], [143, 154], [143, 170], [143, 213], [144, 158], [144, 180], [148, 194], [149, 216], [151, 153], [151, 163], [152, 174], [153, 215], [154, 182], [155, 211], [155, 213], [156, 180], [156, 191], [157, 203], [159, 193], [159, 205], [161, 197], [162, 175], [163, 191], [166, 202], [167, 190], [170, 193], [172, 201], [175, 190], [178, 207], [179, 183], [181, 183], [181, 195], [184, 185], [184, 191], [185, 199], [197, 206], [206, 212]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_216_138.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_216_138 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
