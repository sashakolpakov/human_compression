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
D:=P177Graph("VT3_186_1",186,[1, 5, 6, 7, 10, 15, 16, 17, 18, 23, 30, 34, 35, 36, 37, 39, 40, 44, 46, 49, 50, 51, 52, 55, 56, 57, 59, 61, 62, 64, 66, 67, 68, 69, 70, 76, 78, 82, 83, 87, 88, 92, 93, 94, 95, 97, 98, 99, 100, 102, 104, 105, 107, 109, 116, 118, 119, 120, 121, 127, 129, 130, 131, 132, 133, 134, 136, 137, 138, 139, 140, 144, 148, 149, 150, 152, 155, 156, 157, 158, 159, 162, 164, 166, 167, 169, 171, 172, 174, 176, 177, 179, 186],[[1, 21], [1, 122], [1, 153], [2, 116], [2, 139], [2, 152], [3, 16], [3, 18], [3, 56], [4, 102], [4, 107], [4, 133], [5, 22], [5, 75], [5, 77], [6, 106], [6, 128], [6, 183], [7, 9], [7, 26], [7, 183], [8, 23], [8, 107], [8, 186], [9, 164], [9, 171], [10, 19], [10, 147], [10, 182], [11, 36], [11, 50], [11, 104], [12, 56], [12, 162], [12, 166], [13, 15], [13, 39], [13, 150], [14, 39], [14, 83], [14, 148], [15, 103], [15, 153], [16, 53], [16, 126], [17, 84], [17, 135], [17, 168], [18, 73], [18, 173], [19, 66], [19, 99], [20, 51], [20, 88], [20, 121], [21, 130], [21, 150], [22, 69], [22, 166], [23, 60], [23, 101], [24, 44], [24, 107], [24, 152], [25, 88], [25, 119], [25, 186], [26, 46], [26, 109], [27, 62], [27, 76], [27, 92], [28, 70], [28, 132], [28, 144], [29, 50], [29, 120], [29, 121], [30, 111], [30, 115], [30, 141], [31, 36], [31, 92], [31, 120], [32, 119], [32, 121], [32, 176], [33, 34], [33, 82], [33, 149], [34, 143], [34, 161], [35, 90], [35, 115], [35, 184], [36, 128], [37, 42], [37, 45], [37, 165], [38, 138], [38, 155], [38, 169], [39, 154], [40, 86], [40, 111], [40, 184], [41, 78], [41, 102], [41, 152], [42, 55], [42, 136], [43, 105], [43, 144], [43, 179], [44, 101], [44, 125], [45, 132], [45, 179], [46, 96], [46, 185], [47, 59], [47, 64], [47, 66], [48, 67], [48, 70], [48, 98], [49, 63], [49, 146], [49, 170], [50, 80], [51, 80], [51, 90], [52, 74], [52, 181], [52, 183], [53, 64], [53, 159], [54, 57], [54, 68], [54, 134], [55, 77], [55, 89], [56, 161], [57, 74], [57, 123], [58, 70], [58, 127], [58, 156], [59, 126], [59, 182], [60, 119], [60, 127], [61, 72], [61, 154], [61, 175], [62, 91], [62, 147], [63, 68], [63, 87], [64, 124], [65, 131], [65, 150], [65, 159], [66, 180], [67, 75], [67, 89], [68, 181], [69, 91], [69, 182], [71, 78], [71, 100], [71, 139], [72, 137], [72, 139], [73, 167], [73, 172], [74, 164], [75, 129], [76, 108], [76, 112], [77, 162], [78, 84], [79, 82], [79, 95], [79, 169], [80, 177], [81, 95], [81, 138], [81, 164], [82, 113], [83, 103], [83, 146], [84, 118], [85, 93], [85, 149], [85, 169], [86, 149], [86, 172], [87, 103], [87, 142], [88, 115], [89, 132], [90, 157], [91, 129], [92, 163], [93, 111], [93, 117], [94, 113], [94, 123], [94, 165], [95, 123], [96, 99], [96, 174], [97, 114], [97, 142], [97, 153], [98, 108], [98, 160], [99, 110], [100, 110], [100, 180], [101, 156], [102, 168], [104, 106], [104, 114], [105, 146], [105, 151], [106, 140], [108, 129], [109, 128], [109, 163], [110, 118], [112, 120], [112, 176], [113, 136], [114, 177], [116, 125], [116, 175], [117, 133], [117, 155], [118, 185], [122, 157], [122, 177], [124, 131], [124, 137], [125, 158], [126, 166], [127, 160], [130, 173], [130, 178], [131, 154], [133, 141], [134, 165], [134, 170], [135, 138], [135, 171], [136, 143], [137, 180], [140, 142], [140, 181], [141, 186], [143, 162], [144, 145], [145, 156], [145, 158], [147, 174], [148, 151], [148, 175], [151, 158], [155, 168], [157, 178], [159, 173], [160, 176], [161, 172], [163, 174], [167, 178], [167, 184], [170, 179], [171, 185]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_186_1.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_186_1 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
