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
D:=P177Graph("VT3_182_20",182,[1, 2, 3, 4, 7, 10, 17, 18, 20, 21, 25, 26, 27, 28, 29, 31, 32, 34, 35, 36, 38, 39, 41, 43, 45, 46, 47, 48, 51, 55, 56, 57, 60, 63, 67, 69, 70, 74, 76, 77, 78, 80, 81, 82, 85, 86, 87, 89, 90, 92, 100, 101, 102, 103, 104, 105, 106, 109, 115, 119, 120, 121, 123, 124, 125, 126, 132, 133, 136, 137, 138, 140, 142, 143, 144, 149, 150, 153, 154, 159, 161, 164, 166, 168, 169, 170, 171, 173, 174, 175, 182],[[1, 15], [1, 49], [1, 64], [2, 11], [2, 61], [2, 112], [3, 42], [3, 44], [3, 53], [4, 53], [4, 79], [4, 98], [5, 101], [5, 137], [5, 140], [6, 85], [6, 92], [6, 106], [7, 14], [7, 71], [7, 117], [8, 29], [8, 48], [8, 119], [9, 21], [9, 85], [9, 104], [10, 40], [10, 42], [10, 50], [11, 18], [11, 29], [12, 17], [12, 55], [12, 56], [13, 32], [13, 36], [13, 51], [14, 120], [14, 143], [15, 57], [15, 69], [16, 25], [16, 41], [16, 77], [17, 62], [17, 116], [18, 75], [18, 94], [19, 123], [19, 124], [19, 168], [20, 73], [20, 88], [20, 165], [21, 24], [21, 151], [22, 51], [22, 69], [22, 109], [23, 74], [23, 115], [23, 121], [24, 27], [24, 153], [25, 114], [25, 131], [26, 71], [26, 96], [26, 135], [27, 96], [27, 129], [28, 68], [28, 84], [28, 117], [29, 139], [30, 85], [30, 132], [30, 153], [31, 95], [31, 108], [31, 162], [32, 145], [32, 155], [33, 82], [33, 86], [33, 153], [34, 88], [34, 147], [34, 177], [35, 42], [35, 93], [35, 114], [36, 99], [36, 147], [37, 55], [37, 161], [37, 173], [38, 66], [38, 112], [38, 139], [39, 66], [39, 163], [39, 180], [40, 103], [40, 133], [41, 127], [41, 180], [43, 54], [43, 59], [43, 94], [44, 102], [44, 126], [45, 58], [45, 64], [45, 72], [46, 73], [46, 91], [46, 177], [47, 97], [47, 141], [47, 152], [48, 94], [48, 111], [49, 76], [49, 150], [50, 142], [50, 161], [51, 177], [52, 119], [52, 124], [52, 136], [53, 142], [54, 60], [54, 143], [55, 146], [56, 107], [56, 156], [57, 62], [57, 156], [58, 76], [58, 182], [59, 154], [59, 166], [60, 75], [60, 134], [61, 115], [61, 138], [62, 140], [63, 130], [63, 158], [63, 180], [64, 109], [65, 81], [65, 125], [65, 174], [66, 169], [67, 131], [67, 147], [67, 167], [68, 100], [68, 102], [69, 91], [70, 72], [70, 151], [70, 181], [71, 105], [72, 149], [73, 137], [74, 110], [74, 162], [75, 138], [76, 83], [77, 93], [77, 158], [78, 127], [78, 163], [78, 165], [79, 123], [79, 166], [80, 96], [80, 151], [80, 176], [81, 95], [81, 122], [82, 95], [82, 129], [83, 136], [83, 171], [84, 143], [84, 154], [86, 122], [86, 178], [87, 99], [87, 117], [87, 145], [88, 90], [89, 122], [89, 146], [89, 179], [90, 127], [90, 131], [91, 140], [92, 158], [92, 172], [93, 103], [97, 171], [97, 182], [98, 102], [98, 154], [99, 100], [100, 167], [101, 116], [101, 128], [103, 172], [104, 141], [104, 181], [105, 145], [105, 176], [106, 130], [106, 141], [107, 168], [107, 173], [108, 144], [108, 170], [109, 155], [110, 138], [110, 144], [111, 124], [111, 166], [112, 175], [113, 115], [113, 159], [113, 175], [114, 126], [116, 125], [118, 119], [118, 164], [118, 171], [120, 134], [120, 135], [121, 128], [121, 148], [123, 160], [125, 146], [126, 167], [128, 174], [129, 170], [130, 169], [132, 172], [132, 178], [133, 178], [133, 179], [134, 144], [135, 170], [136, 157], [137, 148], [139, 164], [142, 160], [148, 159], [149, 155], [149, 176], [150, 156], [150, 157], [152, 164], [152, 169], [157, 168], [159, 165], [160, 173], [161, 179], [162, 174], [163, 175], [181, 182]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_182_20.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_182_20 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
