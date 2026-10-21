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
D:=P177Graph("VT3_206_14",206,[1, 3, 6, 8, 11, 14, 17, 18, 21, 27, 28, 29, 31, 34, 36, 38, 39, 40, 43, 44, 45, 48, 50, 52, 53, 57, 59, 62, 64, 67, 69, 70, 71, 73, 76, 77, 78, 79, 82, 84, 85, 86, 87, 90, 91, 92, 93, 94, 97, 99, 100, 101, 102, 103, 105, 106, 108, 111, 112, 113, 114, 117, 118, 120, 121, 123, 125, 126, 127, 130, 131, 136, 137, 140, 142, 147, 148, 150, 151, 153, 154, 155, 157, 159, 160, 162, 164, 166, 168, 170, 175, 179, 181, 182, 183, 188, 192, 195, 197, 198, 199, 201, 202],[[1, 32], [1, 129], [1, 134], [2, 140], [2, 188], [2, 192], [3, 139], [3, 165], [3, 184], [4, 17], [4, 69], [4, 73], [5, 67], [5, 87], [5, 113], [6, 61], [6, 109], [6, 174], [7, 31], [7, 117], [7, 179], [8, 23], [8, 51], [8, 206], [9, 53], [9, 137], [9, 197], [10, 73], [10, 136], [10, 162], [11, 30], [11, 35], [11, 66], [12, 27], [12, 34], [12, 154], [13, 21], [13, 36], [13, 82], [14, 55], [14, 56], [14, 138], [15, 85], [15, 164], [15, 188], [16, 131], [16, 154], [16, 182], [17, 66], [17, 193], [18, 30], [18, 128], [18, 193], [19, 84], [19, 108], [19, 111], [20, 40], [20, 76], [20, 199], [21, 156], [21, 190], [22, 71], [22, 86], [22, 102], [23, 84], [23, 137], [24, 40], [24, 79], [24, 183], [25, 52], [25, 70], [25, 77], [26, 57], [26, 86], [26, 181], [27, 37], [27, 58], [28, 134], [28, 180], [28, 205], [29, 109], [29, 133], [29, 200], [30, 43], [31, 167], [31, 177], [32, 45], [32, 199], [33, 44], [33, 82], [33, 121], [34, 176], [34, 194], [35, 78], [35, 195], [36, 96], [36, 163], [37, 118], [37, 168], [38, 42], [38, 72], [38, 204], [39, 134], [39, 145], [39, 187], [40, 95], [41, 52], [41, 108], [41, 120], [42, 103], [42, 151], [43, 89], [43, 122], [44, 98], [44, 184], [45, 75], [45, 172], [46, 130], [46, 179], [46, 198], [47, 166], [47, 170], [47, 179], [48, 49], [48, 80], [48, 186], [49, 70], [49, 108], [50, 141], [50, 156], [50, 176], [51, 90], [51, 197], [52, 167], [53, 109], [53, 143], [54, 70], [54, 100], [54, 103], [55, 100], [55, 151], [56, 64], [56, 153], [57, 98], [57, 110], [58, 62], [58, 131], [59, 104], [59, 152], [59, 158], [60, 71], [60, 147], [60, 175], [61, 148], [61, 197], [62, 152], [62, 206], [63, 78], [63, 157], [63, 175], [64, 129], [64, 145], [65, 85], [65, 114], [65, 126], [66, 157], [67, 135], [67, 171], [68, 127], [68, 148], [68, 159], [69, 163], [69, 190], [71, 161], [72, 91], [72, 105], [73, 74], [74, 117], [74, 166], [75, 76], [75, 202], [76, 203], [77, 169], [77, 177], [78, 133], [79, 158], [79, 180], [80, 111], [80, 113], [81, 94], [81, 105], [81, 160], [82, 110], [83, 91], [83, 151], [83, 181], [84, 132], [85, 178], [86, 88], [87, 124], [87, 143], [88, 99], [88, 125], [89, 150], [89, 192], [90, 115], [90, 152], [91, 98], [92, 167], [92, 173], [92, 189], [93, 129], [93, 172], [93, 196], [94, 144], [94, 204], [95, 114], [95, 164], [96, 102], [96, 175], [97, 107], [97, 144], [97, 178], [99, 161], [99, 187], [100, 169], [101, 141], [101, 149], [101, 165], [102, 110], [103, 186], [104, 131], [104, 183], [105, 184], [106, 116], [106, 186], [106, 204], [107, 155], [107, 188], [111, 124], [112, 115], [112, 158], [112, 205], [113, 116], [114, 185], [115, 148], [116, 142], [117, 189], [118, 132], [118, 206], [119, 140], [119, 150], [119, 202], [120, 132], [120, 173], [121, 156], [121, 165], [122, 195], [122, 201], [123, 135], [123, 143], [123, 200], [124, 137], [125, 138], [125, 145], [126, 139], [126, 149], [127, 161], [127, 174], [128, 150], [128, 170], [130, 146], [130, 172], [133, 147], [135, 201], [136, 176], [136, 190], [138, 181], [139, 160], [140, 203], [141, 154], [142, 144], [142, 171], [146, 170], [146, 202], [147, 174], [149, 182], [153, 169], [153, 196], [155, 171], [155, 191], [157, 163], [159, 187], [159, 205], [160, 178], [162, 189], [162, 194], [164, 203], [166, 193], [168, 173], [168, 194], [177, 198], [180, 199], [182, 185], [183, 185], [191, 192], [191, 201], [195, 200], [196, 198]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_206_14.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_206_14 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
