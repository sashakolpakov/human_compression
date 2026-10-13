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
D:=P177Graph("VT3_218_20",218,[1, 3, 8, 9, 10, 14, 15, 16, 17, 18, 20, 23, 27, 28, 30, 32, 33, 35, 36, 37, 39, 40, 41, 42, 46, 47, 50, 51, 53, 56, 58, 59, 61, 63, 64, 66, 67, 68, 69, 71, 73, 74, 76, 77, 80, 82, 85, 88, 91, 92, 96, 98, 99, 100, 102, 103, 104, 106, 107, 108, 110, 111, 113, 117, 118, 122, 123, 124, 125, 128, 129, 134, 135, 136, 138, 140, 143, 144, 148, 149, 150, 151, 153, 158, 161, 162, 163, 164, 165, 166, 168, 172, 175, 177, 179, 180, 182, 192, 195, 199, 200, 202, 205, 206, 210, 211, 215, 216, 217],[[1, 6], [1, 171], [1, 209], [2, 14], [2, 27], [2, 172], [3, 7], [3, 31], [3, 147], [4, 82], [4, 108], [4, 206], [5, 63], [5, 180], [5, 205], [6, 58], [6, 73], [7, 35], [7, 37], [8, 95], [8, 145], [8, 154], [9, 79], [9, 178], [9, 194], [10, 81], [10, 109], [10, 173], [11, 35], [11, 144], [11, 200], [12, 53], [12, 80], [12, 158], [13, 104], [13, 164], [13, 175], [14, 90], [14, 114], [15, 19], [15, 83], [15, 176], [16, 45], [16, 131], [16, 174], [17, 116], [17, 173], [17, 193], [18, 119], [18, 178], [18, 208], [19, 92], [19, 100], [20, 60], [20, 159], [20, 188], [21, 42], [21, 58], [21, 179], [22, 23], [22, 107], [22, 150], [23, 94], [23, 214], [24, 68], [24, 76], [24, 182], [25, 27], [25, 37], [25, 71], [26, 28], [26, 180], [26, 215], [27, 156], [28, 121], [28, 214], [29, 53], [29, 128], [29, 136], [30, 54], [30, 132], [30, 189], [31, 77], [31, 200], [32, 52], [32, 78], [32, 209], [33, 130], [33, 152], [33, 156], [34, 61], [34, 77], [34, 179], [35, 156], [36, 38], [36, 55], [36, 86], [37, 184], [38, 39], [38, 202], [39, 43], [39, 133], [40, 84], [40, 114], [40, 154], [41, 139], [41, 189], [41, 198], [42, 119], [42, 155], [43, 63], [43, 85], [44, 59], [44, 151], [44, 177], [45, 111], [45, 216], [46, 137], [46, 142], [46, 194], [47, 48], [47, 186], [47, 204], [48, 102], [48, 140], [49, 99], [49, 108], [49, 161], [50, 120], [50, 170], [50, 176], [51, 54], [51, 95], [51, 170], [52, 166], [52, 182], [53, 183], [54, 135], [55, 148], [55, 163], [56, 57], [56, 146], [56, 176], [57, 162], [57, 175], [58, 87], [59, 174], [59, 191], [60, 98], [60, 140], [61, 79], [61, 119], [62, 64], [62, 102], [62, 110], [63, 127], [64, 127], [64, 204], [65, 153], [65, 166], [65, 199], [66, 115], [66, 187], [66, 188], [67, 75], [67, 79], [67, 137], [68, 112], [68, 213], [69, 72], [69, 93], [69, 188], [70, 129], [70, 175], [70, 217], [71, 90], [71, 94], [72, 117], [72, 164], [73, 78], [73, 141], [74, 160], [74, 189], [74, 207], [75, 77], [75, 113], [76, 130], [76, 201], [78, 144], [80, 115], [80, 159], [81, 138], [81, 153], [82, 126], [82, 194], [83, 122], [83, 215], [84, 111], [84, 134], [85, 86], [85, 97], [86, 143], [87, 91], [87, 129], [88, 147], [88, 181], [88, 184], [89, 143], [89, 163], [89, 177], [90, 150], [91, 139], [91, 171], [92, 186], [92, 218], [93, 98], [93, 100], [94, 106], [95, 107], [96, 183], [96, 197], [96, 201], [97, 149], [97, 211], [98, 186], [99, 169], [99, 174], [100, 146], [101, 158], [101, 161], [101, 192], [102, 203], [103, 116], [103, 160], [103, 198], [104, 155], [104, 208], [105, 110], [105, 123], [105, 153], [106, 121], [106, 184], [107, 120], [108, 212], [109, 110], [109, 211], [111, 145], [112, 125], [112, 128], [113, 147], [113, 190], [114, 210], [115, 124], [116, 138], [117, 187], [117, 208], [118, 121], [118, 133], [118, 181], [120, 122], [122, 214], [123, 203], [123, 213], [124, 126], [124, 212], [125, 185], [125, 203], [126, 195], [127, 211], [128, 201], [129, 155], [130, 172], [131, 134], [131, 161], [132, 162], [132, 217], [133, 180], [134, 157], [135, 145], [135, 207], [136, 159], [136, 185], [137, 148], [138, 196], [139, 217], [140, 185], [141, 179], [141, 200], [142, 163], [142, 206], [143, 167], [144, 152], [146, 164], [148, 190], [149, 167], [149, 173], [150, 154], [151, 167], [151, 193], [152, 182], [157, 192], [157, 210], [158, 212], [160, 168], [162, 170], [165, 171], [165, 196], [165, 198], [166, 213], [168, 191], [168, 193], [169, 177], [169, 206], [172, 197], [178, 195], [181, 202], [183, 192], [187, 195], [190, 202], [191, 216], [196, 199], [197, 210], [199, 209], [204, 205], [205, 218], [207, 216], [215, 218]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_218_20.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_218_20 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
