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
D:=P177Graph("VT3_216_76",216,[1, 3, 8, 9, 14, 15, 16, 17, 22, 24, 25, 26, 27, 31, 33, 35, 36, 42, 43, 44, 46, 48, 50, 54, 55, 58, 62, 63, 64, 65, 66, 67, 68, 72, 73, 74, 77, 80, 81, 85, 88, 89, 91, 95, 96, 98, 100, 103, 105, 106, 108, 109, 110, 111, 116, 117, 118, 119, 120, 122, 124, 128, 132, 135, 136, 139, 142, 143, 147, 148, 151, 153, 154, 156, 157, 159, 160, 162, 163, 167, 169, 170, 171, 173, 177, 183, 184, 185, 186, 188, 189, 190, 193, 194, 195, 198, 199, 200, 202, 204, 205, 206, 208, 209, 210, 211, 213, 215],[[1, 29], [1, 93], [1, 152], [2, 89], [2, 170], [2, 183], [3, 125], [3, 130], [3, 158], [4, 122], [4, 151], [4, 202], [5, 31], [5, 73], [5, 163], [6, 44], [6, 46], [6, 215], [7, 68], [7, 96], [7, 194], [8, 39], [8, 52], [8, 155], [9, 20], [9, 94], [9, 175], [10, 48], [10, 159], [10, 195], [11, 26], [11, 120], [11, 169], [12, 62], [12, 91], [12, 118], [13, 14], [13, 95], [13, 198], [14, 104], [14, 155], [15, 32], [15, 197], [15, 201], [16, 76], [16, 141], [16, 181], [17, 51], [17, 145], [17, 201], [18, 42], [18, 128], [18, 205], [19, 119], [19, 147], [19, 210], [20, 95], [20, 205], [21, 98], [21, 151], [21, 200], [22, 78], [22, 121], [22, 192], [23, 67], [23, 173], [23, 185], [24, 79], [24, 144], [24, 180], [25, 37], [25, 47], [25, 86], [26, 97], [26, 149], [27, 40], [27, 112], [27, 121], [28, 50], [28, 177], [28, 184], [29, 136], [29, 190], [30, 77], [30, 96], [30, 186], [31, 168], [31, 203], [32, 43], [32, 190], [33, 51], [33, 155], [33, 172], [34, 116], [34, 159], [34, 211], [35, 39], [35, 101], [35, 187], [36, 57], [36, 84], [36, 115], [37, 111], [37, 213], [38, 128], [38, 167], [38, 169], [39, 183], [40, 42], [40, 142], [41, 42], [41, 117], [41, 211], [43, 196], [43, 214], [44, 133], [44, 175], [45, 124], [45, 147], [45, 170], [46, 52], [46, 87], [47, 170], [47, 195], [48, 61], [48, 79], [49, 68], [49, 85], [49, 110], [50, 129], [50, 180], [51, 73], [52, 202], [53, 81], [53, 154], [53, 209], [54, 82], [54, 92], [54, 102], [55, 75], [55, 113], [55, 207], [56, 148], [56, 204], [56, 206], [57, 74], [57, 139], [58, 114], [58, 123], [58, 203], [59, 108], [59, 119], [59, 139], [60, 66], [60, 143], [60, 198], [61, 65], [61, 167], [62, 130], [62, 179], [63, 137], [63, 141], [63, 150], [64, 78], [64, 97], [64, 146], [65, 192], [65, 214], [66, 99], [66, 121], [67, 107], [67, 131], [68, 69], [69, 160], [69, 208], [70, 135], [70, 156], [70, 185], [71, 88], [71, 153], [71, 173], [72, 141], [72, 152], [72, 161], [73, 125], [74, 129], [74, 134], [75, 118], [75, 162], [76, 77], [76, 89], [77, 129], [78, 189], [79, 153], [80, 145], [80, 164], [80, 216], [81, 168], [81, 178], [82, 116], [82, 186], [83, 136], [83, 171], [83, 183], [84, 167], [84, 171], [85, 176], [85, 216], [86, 189], [86, 204], [87, 109], [87, 116], [88, 127], [88, 166], [89, 166], [90, 124], [90, 163], [90, 199], [91, 99], [91, 133], [92, 136], [92, 143], [93, 157], [93, 199], [94, 98], [94, 189], [95, 180], [96, 192], [97, 177], [98, 140], [99, 210], [100, 126], [100, 149], [100, 172], [101, 103], [101, 110], [102, 120], [102, 200], [103, 138], [103, 197], [104, 132], [104, 135], [105, 158], [105, 165], [105, 182], [106, 138], [106, 149], [106, 178], [107, 160], [107, 215], [108, 161], [108, 187], [109, 115], [109, 191], [110, 114], [111, 113], [111, 131], [112, 157], [112, 202], [113, 122], [114, 204], [115, 148], [117, 166], [117, 182], [118, 127], [119, 140], [120, 216], [122, 196], [123, 184], [123, 210], [124, 191], [125, 160], [126, 147], [126, 194], [127, 148], [128, 203], [130, 200], [131, 143], [132, 182], [132, 214], [133, 154], [134, 142], [134, 156], [135, 176], [137, 151], [137, 209], [138, 188], [139, 165], [140, 173], [142, 201], [144, 157], [144, 188], [145, 153], [146, 162], [146, 163], [150, 193], [150, 198], [152, 206], [154, 164], [156, 179], [158, 188], [159, 161], [162, 187], [164, 213], [165, 213], [168, 186], [169, 181], [171, 174], [172, 206], [174, 208], [174, 209], [175, 190], [176, 199], [177, 212], [178, 185], [179, 195], [181, 215], [184, 196], [191, 193], [193, 197], [194, 207], [205, 207], [208, 212], [211, 212]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_216_76.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_216_76 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
