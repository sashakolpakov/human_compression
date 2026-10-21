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
D:=P177Graph("VT3_182_16",182,[1, 2, 3, 4, 7, 10, 17, 18, 20, 21, 25, 26, 27, 28, 29, 31, 32, 34, 35, 36, 38, 39, 41, 43, 45, 46, 47, 48, 51, 55, 56, 57, 60, 63, 67, 69, 70, 74, 76, 77, 78, 80, 81, 82, 85, 86, 87, 89, 90, 92, 100, 101, 102, 103, 104, 105, 106, 109, 115, 119, 120, 121, 123, 124, 125, 126, 132, 133, 136, 137, 138, 140, 142, 143, 144, 149, 150, 153, 154, 159, 161, 164, 166, 168, 169, 170, 171, 173, 174, 175, 182],[[1, 8], [1, 49], [1, 64], [2, 61], [2, 65], [2, 112], [3, 44], [3, 53], [3, 145], [4, 71], [4, 79], [4, 98], [5, 39], [5, 101], [5, 137], [6, 26], [6, 85], [6, 106], [7, 9], [7, 14], [7, 71], [8, 48], [8, 119], [9, 21], [9, 104], [10, 42], [10, 50], [10, 99], [11, 18], [11, 29], [11, 76], [12, 17], [12, 55], [12, 159], [13, 35], [13, 36], [13, 51], [14, 123], [14, 143], [15, 57], [15, 69], [15, 90], [16, 41], [16, 77], [16, 153], [17, 62], [17, 79], [18, 75], [18, 95], [19, 123], [19, 140], [19, 168], [20, 73], [20, 88], [20, 156], [21, 24], [21, 180], [22, 25], [22, 51], [22, 69], [23, 74], [23, 115], [23, 164], [24, 27], [24, 143], [25, 114], [25, 131], [26, 96], [26, 135], [27, 129], [27, 158], [28, 84], [28, 117], [28, 151], [29, 139], [29, 162], [30, 85], [30, 120], [30, 153], [31, 40], [31, 95], [31, 162], [32, 97], [32, 145], [32, 155], [33, 60], [33, 82], [33, 153], [34, 49], [34, 147], [34, 177], [35, 42], [35, 114], [36, 58], [36, 99], [37, 55], [37, 121], [37, 161], [38, 66], [38, 112], [38, 128], [39, 163], [39, 180], [40, 103], [40, 133], [41, 91], [41, 127], [42, 81], [43, 54], [43, 94], [43, 129], [44, 89], [44, 126], [45, 58], [45, 72], [45, 139], [46, 91], [46, 157], [46, 177], [47, 113], [47, 141], [47, 152], [48, 94], [48, 108], [49, 150], [50, 161], [50, 174], [51, 83], [52, 69], [52, 124], [52, 136], [53, 125], [53, 142], [54, 143], [54, 168], [55, 98], [56, 59], [56, 107], [56, 156], [57, 111], [57, 156], [58, 76], [59, 154], [59, 166], [60, 75], [60, 134], [61, 138], [61, 171], [62, 78], [62, 140], [63, 73], [63, 158], [63, 180], [64, 67], [64, 109], [65, 81], [65, 174], [66, 70], [66, 169], [67, 147], [67, 167], [68, 100], [68, 102], [68, 161], [70, 151], [70, 181], [71, 105], [72, 100], [72, 149], [73, 137], [74, 162], [74, 179], [75, 136], [76, 83], [77, 93], [77, 177], [78, 127], [78, 165], [79, 123], [80, 96], [80, 130], [80, 151], [81, 122], [82, 93], [82, 95], [83, 136], [84, 154], [84, 173], [85, 127], [86, 114], [86, 122], [86, 178], [87, 117], [87, 145], [87, 181], [88, 90], [88, 92], [89, 146], [89, 179], [90, 131], [91, 140], [92, 158], [92, 172], [93, 103], [94, 150], [96, 154], [97, 171], [97, 182], [98, 102], [99, 100], [101, 116], [101, 160], [102, 176], [103, 147], [104, 141], [104, 163], [105, 141], [105, 176], [106, 130], [106, 165], [107, 137], [107, 173], [108, 144], [108, 170], [109, 118], [109, 155], [110, 119], [110, 138], [110, 144], [111, 124], [111, 166], [112, 182], [113, 115], [113, 175], [115, 146], [116, 125], [116, 175], [117, 142], [118, 119], [118, 171], [120, 134], [120, 135], [121, 128], [121, 148], [122, 138], [124, 134], [125, 146], [126, 155], [126, 167], [128, 174], [129, 170], [130, 169], [131, 132], [132, 172], [132, 178], [133, 167], [133, 179], [135, 166], [139, 164], [142, 160], [144, 178], [148, 159], [148, 169], [149, 152], [149, 176], [150, 157], [152, 164], [157, 168], [159, 165], [160, 173], [163, 175], [170, 172], [181, 182]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_182_16.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_182_16 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
