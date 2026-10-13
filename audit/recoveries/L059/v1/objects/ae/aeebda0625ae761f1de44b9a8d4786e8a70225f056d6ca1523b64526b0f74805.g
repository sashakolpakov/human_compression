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
D:=P177Graph("VT3_192_45",192,[1, 3, 4, 5, 6, 9, 10, 11, 12, 13, 14, 15, 17, 19, 22, 24, 28, 31, 37, 41, 42, 48, 50, 52, 54, 58, 60, 61, 65, 66, 67, 68, 69, 70, 73, 74, 76, 77, 78, 82, 87, 89, 91, 95, 96, 97, 98, 99, 104, 106, 109, 115, 116, 122, 123, 126, 127, 129, 130, 132, 133, 134, 137, 138, 139, 140, 141, 142, 144, 145, 147, 149, 150, 151, 153, 154, 155, 161, 164, 165, 166, 167, 168, 170, 171, 175, 176, 177, 178, 179, 180, 182, 183, 185, 190, 192],[[1, 102], [1, 112], [1, 159], [2, 15], [2, 28], [2, 126], [3, 38], [3, 120], [3, 156], [4, 46], [4, 64], [4, 92], [5, 45], [5, 110], [5, 187], [6, 7], [6, 18], [6, 163], [7, 28], [7, 142], [8, 50], [8, 58], [8, 87], [9, 43], [9, 100], [9, 143], [10, 26], [10, 44], [10, 186], [11, 35], [11, 57], [11, 117], [12, 27], [12, 32], [12, 117], [13, 59], [13, 72], [13, 92], [14, 110], [14, 181], [14, 189], [15, 33], [15, 131], [16, 17], [16, 61], [16, 151], [17, 59], [17, 184], [18, 24], [18, 168], [19, 64], [19, 124], [19, 135], [20, 66], [20, 67], [20, 153], [21, 137], [21, 167], [21, 168], [22, 40], [22, 86], [22, 114], [23, 68], [23, 98], [23, 134], [24, 100], [24, 152], [25, 77], [25, 150], [25, 192], [26, 89], [26, 161], [27, 145], [27, 178], [28, 110], [29, 69], [29, 109], [29, 154], [30, 144], [30, 154], [30, 176], [31, 81], [31, 83], [31, 158], [32, 66], [32, 154], [33, 130], [33, 145], [34, 67], [34, 130], [34, 171], [35, 97], [35, 190], [36, 54], [36, 134], [36, 166], [37, 93], [37, 121], [37, 136], [38, 61], [38, 177], [39, 65], [39, 87], [39, 153], [40, 96], [40, 180], [41, 124], [41, 156], [41, 173], [42, 121], [42, 157], [42, 174], [43, 77], [43, 97], [44, 147], [44, 149], [45, 69], [45, 171], [46, 177], [46, 180], [47, 48], [47, 104], [47, 145], [48, 111], [48, 119], [49, 61], [49, 87], [49, 167], [50, 102], [50, 152], [51, 52], [51, 126], [51, 137], [52, 71], [52, 120], [53, 60], [53, 147], [53, 175], [54, 80], [54, 85], [55, 91], [55, 122], [55, 182], [56, 74], [56, 127], [56, 165], [57, 129], [57, 134], [58, 148], [58, 157], [59, 139], [60, 118], [60, 187], [62, 70], [62, 151], [62, 176], [63, 138], [63, 147], [63, 180], [64, 140], [65, 93], [65, 108], [66, 184], [67, 112], [68, 100], [68, 189], [69, 111], [70, 94], [70, 188], [71, 96], [71, 104], [72, 73], [72, 182], [73, 117], [73, 188], [74, 75], [74, 131], [75, 140], [75, 149], [76, 84], [76, 88], [76, 101], [77, 121], [78, 84], [78, 107], [78, 135], [79, 95], [79, 115], [79, 133], [80, 82], [80, 177], [81, 150], [81, 185], [82, 90], [82, 188], [83, 95], [83, 138], [84, 138], [85, 122], [85, 175], [86, 99], [86, 139], [88, 89], [88, 141], [89, 93], [90, 99], [90, 153], [91, 163], [91, 174], [92, 98], [94, 130], [94, 132], [95, 156], [96, 128], [97, 101], [98, 118], [99, 160], [101, 106], [102, 192], [103, 123], [103, 127], [103, 137], [104, 158], [105, 106], [105, 115], [105, 178], [106, 128], [107, 170], [107, 192], [108, 170], [108, 176], [109, 146], [109, 191], [111, 127], [112, 161], [113, 144], [113, 161], [113, 179], [114, 133], [114, 167], [115, 191], [116, 125], [116, 143], [116, 172], [118, 165], [119, 133], [119, 142], [120, 164], [122, 181], [123, 157], [123, 189], [124, 155], [125, 132], [125, 166], [126, 191], [128, 155], [129, 162], [129, 174], [131, 144], [132, 146], [135, 179], [136, 168], [136, 183], [139, 173], [140, 181], [141, 152], [141, 162], [142, 148], [143, 182], [146, 190], [148, 164], [149, 169], [150, 186], [151, 159], [155, 186], [158, 190], [159, 183], [160, 164], [160, 183], [162, 185], [163, 165], [166, 184], [169, 170], [169, 171], [172, 178], [172, 185], [173, 175], [179, 187]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_192_45.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_192_45 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
