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
D:=P177Graph("VT3_204_52",204,[1, 5, 6, 7, 8, 9, 10, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203],[[1, 2], [1, 3], [1, 4], [2, 5], [2, 6], [3, 7], [3, 9], [4, 8], [4, 10], [5, 11], [5, 13], [6, 12], [6, 14], [7, 15], [7, 19], [8, 16], [8, 20], [9, 17], [9, 21], [10, 18], [10, 22], [11, 23], [11, 27], [12, 24], [12, 28], [13, 25], [13, 29], [14, 26], [14, 30], [15, 31], [15, 39], [16, 32], [16, 40], [17, 33], [17, 41], [18, 34], [18, 42], [19, 35], [19, 43], [20, 36], [20, 44], [21, 37], [21, 45], [22, 38], [22, 46], [23, 47], [23, 55], [24, 48], [24, 56], [25, 49], [25, 57], [26, 50], [26, 58], [27, 51], [27, 59], [28, 52], [28, 60], [29, 53], [29, 61], [30, 54], [30, 62], [31, 63], [31, 79], [32, 64], [32, 80], [33, 65], [33, 81], [34, 66], [34, 82], [35, 67], [35, 83], [36, 68], [36, 84], [37, 69], [37, 85], [38, 70], [38, 86], [39, 71], [39, 87], [40, 72], [40, 88], [41, 73], [41, 89], [42, 74], [42, 90], [43, 75], [43, 91], [44, 76], [44, 92], [45, 77], [45, 93], [46, 78], [46, 94], [47, 95], [47, 111], [48, 96], [48, 112], [49, 97], [49, 113], [50, 98], [50, 114], [51, 99], [51, 115], [52, 100], [52, 116], [53, 101], [53, 117], [54, 102], [54, 118], [55, 103], [55, 119], [56, 104], [56, 120], [57, 105], [57, 121], [58, 106], [58, 122], [59, 107], [59, 123], [60, 108], [60, 124], [61, 109], [61, 125], [62, 110], [62, 126], [63, 127], [63, 135], [64, 102], [64, 128], [65, 98], [65, 130], [66, 97], [66, 129], [67, 112], [67, 145], [68, 120], [68, 130], [69, 129], [69, 146], [70, 96], [70, 147], [71, 103], [71, 148], [72, 131], [72, 149], [73, 123], [73, 144], [74, 110], [74, 132], [75, 122], [75, 133], [76, 134], [76, 150], [77, 111], [77, 139], [78, 106], [78, 135], [79, 109], [79, 131], [80, 99], [80, 143], [81, 113], [81, 136], [82, 137], [82, 145], [83, 138], [83, 151], [84, 125], [84, 152], [85, 118], [85, 150], [86, 117], [86, 139], [87, 124], [87, 132], [88, 100], [88, 140], [89, 140], [89, 141], [90, 107], [90, 142], [91, 105], [91, 143], [92, 119], [92, 138], [93, 116], [93, 153], [94, 144], [94, 154], [95, 155], [95, 163], [96, 156], [97, 158], [98, 157], [99, 173], [100, 158], [101, 157], [101, 174], [102, 175], [103, 176], [104, 159], [104, 177], [105, 172], [106, 160], [107, 161], [108, 162], [108, 178], [109, 167], [110, 163], [111, 159], [112, 171], [113, 164], [114, 165], [114, 173], [115, 166], [115, 179], [116, 180], [117, 178], [118, 167], [119, 160], [120, 168], [121, 168], [121, 169], [122, 170], [123, 171], [124, 166], [125, 181], [126, 172], [126, 182], [127, 169], [127, 180], [128, 162], [128, 188], [129, 183], [130, 184], [131, 192], [132, 184], [133, 177], [133, 183], [134, 156], [134, 179], [135, 185], [136, 179], [136, 185], [137, 174], [137, 175], [138, 191], [139, 186], [140, 187], [141, 155], [141, 170], [142, 169], [142, 190], [143, 186], [144, 188], [145, 189], [146, 165], [146, 176], [147, 165], [147, 192], [148, 174], [148, 187], [149, 161], [149, 177], [150, 190], [151, 162], [151, 164], [152, 155], [152, 189], [153, 182], [153, 191], [154, 181], [154, 182], [156, 198], [157, 193], [158, 194], [159, 202], [160, 194], [161, 193], [163, 195], [164, 195], [166, 201], [167, 196], [168, 197], [170, 200], [171, 196], [172, 198], [173, 199], [175, 202], [176, 197], [178, 200], [180, 199], [181, 201], [183, 201], [184, 203], [185, 202], [186, 203], [187, 198], [188, 197], [189, 199], [190, 200], [191, 193], [192, 195], [194, 204], [196, 204], [203, 204]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_204_52.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_204_52 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
