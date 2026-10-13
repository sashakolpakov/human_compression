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
D:=P177Graph("VT3_182_25",182,[1, 5, 6, 7, 8, 9, 10, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 176, 177, 178, 179, 180, 181],[[1, 2], [1, 3], [1, 4], [2, 5], [2, 6], [3, 7], [3, 9], [4, 8], [4, 10], [5, 11], [5, 13], [6, 12], [6, 14], [7, 15], [7, 19], [8, 16], [8, 20], [9, 17], [9, 21], [10, 18], [10, 22], [11, 23], [11, 27], [12, 24], [12, 28], [13, 25], [13, 29], [14, 26], [14, 30], [15, 31], [15, 39], [16, 32], [16, 40], [17, 33], [17, 41], [18, 34], [18, 42], [19, 35], [19, 43], [20, 36], [20, 44], [21, 37], [21, 45], [22, 38], [22, 46], [23, 47], [23, 55], [24, 48], [24, 56], [25, 49], [25, 57], [26, 50], [26, 58], [27, 51], [27, 59], [28, 52], [28, 60], [29, 53], [29, 61], [30, 54], [30, 62], [31, 63], [31, 79], [32, 64], [32, 80], [33, 65], [33, 81], [34, 66], [34, 82], [35, 67], [35, 83], [36, 68], [36, 84], [37, 69], [37, 85], [38, 70], [38, 86], [39, 71], [39, 87], [40, 72], [40, 88], [41, 73], [41, 89], [42, 74], [42, 90], [43, 75], [43, 91], [44, 76], [44, 92], [45, 77], [45, 93], [46, 78], [46, 94], [47, 95], [47, 111], [48, 96], [48, 112], [49, 97], [49, 113], [50, 98], [50, 114], [51, 99], [51, 115], [52, 100], [52, 116], [53, 101], [53, 117], [54, 102], [54, 118], [55, 103], [55, 119], [56, 104], [56, 120], [57, 105], [57, 121], [58, 106], [58, 122], [59, 107], [59, 123], [60, 108], [60, 124], [61, 109], [61, 125], [62, 110], [62, 126], [63, 121], [63, 127], [64, 124], [64, 142], [65, 125], [65, 141], [66, 109], [66, 128], [67, 117], [67, 129], [68, 126], [68, 143], [69, 130], [69, 144], [70, 102], [70, 145], [71, 106], [71, 131], [72, 122], [72, 138], [73, 110], [73, 135], [74, 103], [74, 132], [75, 133], [75, 143], [76, 113], [76, 134], [77, 98], [77, 137], [78, 105], [78, 130], [79, 116], [79, 146], [80, 123], [80, 135], [81, 108], [81, 147], [82, 136], [82, 148], [83, 118], [83, 142], [84, 111], [84, 137], [85, 99], [85, 138], [86, 115], [86, 131], [87, 119], [87, 139], [88, 140], [88, 146], [89, 95], [89, 136], [90, 104], [90, 127], [91, 112], [91, 128], [92, 96], [92, 141], [93, 97], [93, 132], [94, 100], [94, 129], [95, 149], [96, 164], [97, 163], [98, 150], [99, 151], [100, 165], [101, 152], [101, 166], [102, 167], [103, 153], [104, 160], [105, 157], [106, 154], [107, 155], [107, 165], [108, 156], [109, 159], [110, 152], [111, 168], [112, 157], [113, 169], [114, 158], [114, 170], [115, 164], [116, 159], [117, 160], [118, 153], [119, 161], [120, 162], [120, 168], [121, 158], [122, 149], [123, 150], [124, 163], [125, 154], [126, 151], [127, 151], [128, 172], [129, 149], [130, 161], [131, 163], [132, 171], [133, 155], [133, 171], [134, 165], [134, 173], [135, 157], [136, 169], [137, 159], [138, 172], [139, 152], [139, 173], [140, 166], [140, 171], [141, 153], [142, 174], [143, 156], [144, 162], [144, 174], [145, 168], [145, 175], [146, 167], [147, 158], [147, 175], [148, 170], [148, 174], [150, 177], [154, 176], [155, 176], [156, 178], [160, 177], [161, 178], [162, 176], [164, 179], [166, 179], [167, 180], [169, 180], [170, 179], [172, 181], [173, 181], [175, 181], [177, 182], [178, 182], [180, 182]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_182_25.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_182_25 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
