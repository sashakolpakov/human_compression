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
D:=P177Graph("VT3_192_220",192,[1, 2, 3, 4, 6, 7, 9, 10, 13, 17, 20, 26, 28, 33, 37, 38, 40, 42, 43, 45, 46, 50, 51, 52, 53, 54, 55, 56, 57, 58, 60, 68, 69, 71, 76, 79, 80, 82, 83, 84, 86, 87, 88, 90, 94, 99, 101, 106, 107, 108, 111, 113, 115, 119, 122, 123, 124, 125, 126, 127, 129, 130, 131, 132, 134, 135, 136, 137, 138, 140, 141, 144, 146, 148, 150, 151, 154, 155, 156, 157, 159, 160, 161, 163, 165, 167, 170, 173, 174, 179, 181, 183, 184, 186, 188, 191],[[1, 21], [1, 142], [1, 176], [2, 77], [2, 97], [2, 109], [3, 29], [3, 92], [3, 171], [4, 81], [4, 102], [4, 142], [5, 82], [5, 130], [5, 155], [6, 102], [6, 117], [6, 168], [7, 23], [7, 93], [7, 95], [8, 52], [8, 87], [8, 90], [9, 22], [9, 32], [9, 97], [10, 75], [10, 147], [10, 172], [11, 130], [11, 141], [11, 159], [12, 17], [12, 26], [12, 183], [13, 67], [13, 77], [13, 114], [14, 56], [14, 101], [14, 108], [15, 45], [15, 80], [15, 167], [16, 84], [16, 125], [16, 150], [17, 61], [17, 153], [18, 79], [18, 87], [18, 140], [19, 20], [19, 40], [19, 69], [20, 24], [20, 92], [21, 38], [21, 111], [22, 126], [22, 181], [23, 45], [23, 127], [24, 80], [24, 184], [25, 108], [25, 156], [25, 191], [26, 59], [26, 66], [27, 50], [27, 51], [27, 136], [28, 35], [28, 44], [28, 91], [29, 37], [29, 129], [30, 107], [30, 113], [30, 179], [31, 33], [31, 46], [31, 163], [32, 42], [32, 150], [33, 47], [33, 59], [34, 53], [34, 58], [34, 148], [35, 42], [35, 123], [36, 38], [36, 123], [36, 130], [37, 149], [37, 158], [38, 105], [39, 94], [39, 106], [39, 191], [40, 70], [40, 128], [41, 83], [41, 137], [41, 174], [42, 175], [43, 59], [43, 164], [43, 168], [44, 68], [44, 88], [45, 100], [46, 103], [46, 152], [47, 137], [47, 165], [48, 55], [48, 148], [48, 151], [49, 56], [49, 94], [49, 129], [50, 73], [50, 185], [51, 110], [51, 178], [52, 128], [52, 133], [53, 112], [53, 153], [54, 61], [54, 164], [54, 182], [55, 114], [55, 169], [56, 120], [57, 72], [57, 143], [57, 176], [58, 66], [58, 139], [60, 110], [60, 162], [60, 166], [61, 71], [62, 113], [62, 135], [62, 151], [63, 136], [63, 140], [63, 146], [64, 84], [64, 181], [64, 188], [65, 94], [65, 107], [65, 111], [66, 174], [67, 88], [67, 132], [68, 78], [68, 171], [69, 77], [69, 78], [70, 79], [70, 84], [71, 116], [71, 187], [72, 76], [72, 173], [73, 127], [73, 163], [74, 101], [74, 131], [74, 146], [75, 144], [75, 170], [76, 91], [76, 120], [78, 150], [79, 98], [80, 133], [81, 83], [81, 122], [82, 139], [82, 168], [83, 85], [85, 106], [85, 113], [86, 97], [86, 112], [86, 121], [87, 185], [88, 149], [89, 140], [89, 186], [89, 188], [90, 145], [90, 187], [91, 111], [92, 99], [93, 151], [93, 174], [95, 115], [95, 183], [96, 124], [96, 144], [96, 160], [98, 99], [98, 131], [99, 118], [100, 135], [100, 138], [101, 178], [102, 165], [103, 170], [103, 186], [104, 125], [104, 131], [104, 154], [105, 122], [105, 179], [106, 166], [107, 149], [108, 143], [109, 119], [109, 161], [110, 156], [112, 155], [114, 184], [115, 133], [115, 169], [116, 161], [116, 181], [117, 144], [117, 159], [118, 157], [118, 167], [119, 153], [119, 169], [120, 154], [121, 123], [121, 132], [122, 139], [124, 152], [124, 190], [125, 180], [126, 172], [126, 182], [127, 162], [128, 161], [129, 192], [132, 177], [134, 147], [134, 180], [134, 189], [135, 158], [136, 152], [137, 162], [138, 166], [138, 192], [141, 172], [141, 175], [142, 191], [143, 160], [145, 163], [145, 183], [146, 189], [147, 188], [148, 177], [154, 171], [155, 182], [156, 190], [157, 178], [157, 192], [158, 184], [159, 176], [160, 189], [164, 170], [165, 190], [167, 185], [173, 175], [173, 180], [177, 179], [186, 187]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_192_220.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_192_220 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
