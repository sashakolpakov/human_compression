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
D:=P177Graph("VT3_192_193",192,[1, 2, 3, 6, 7, 8, 10, 13, 14, 16, 19, 25, 27, 28, 31, 33, 34, 35, 36, 37, 38, 39, 44, 47, 48, 49, 50, 54, 56, 58, 59, 61, 63, 67, 70, 72, 74, 76, 77, 79, 80, 82, 86, 93, 94, 95, 96, 99, 100, 105, 107, 109, 110, 118, 123, 127, 129, 130, 131, 132, 133, 135, 136, 137, 138, 139, 140, 143, 144, 147, 150, 151, 152, 155, 156, 157, 158, 159, 160, 161, 162, 166, 167, 168, 169, 170, 172, 173, 174, 175, 179, 183, 185, 187, 190, 191],[[1, 23], [1, 30], [1, 97], [2, 9], [2, 42], [2, 142], [3, 57], [3, 64], [3, 142], [4, 28], [4, 96], [4, 169], [5, 6], [5, 107], [5, 158], [6, 92], [6, 128], [7, 87], [7, 180], [7, 184], [8, 51], [8, 87], [8, 91], [9, 77], [9, 79], [10, 30], [10, 115], [10, 126], [11, 25], [11, 174], [11, 191], [12, 35], [12, 77], [12, 183], [13, 42], [13, 73], [13, 188], [14, 89], [14, 145], [14, 189], [15, 38], [15, 109], [15, 162], [16, 18], [16, 53], [16, 65], [17, 44], [17, 139], [17, 143], [18, 156], [18, 157], [19, 102], [19, 111], [19, 149], [20, 47], [20, 100], [20, 147], [21, 61], [21, 131], [21, 136], [22, 37], [22, 56], [22, 144], [23, 131], [23, 158], [24, 99], [24, 118], [24, 139], [25, 45], [25, 186], [26, 133], [26, 144], [26, 155], [27, 64], [27, 75], [27, 149], [28, 104], [28, 165], [29, 133], [29, 137], [29, 175], [30, 173], [31, 52], [31, 84], [31, 176], [32, 118], [32, 136], [32, 152], [33, 40], [33, 66], [33, 114], [34, 69], [34, 177], [34, 186], [35, 83], [35, 116], [36, 52], [36, 53], [36, 116], [37, 111], [37, 125], [38, 46], [38, 141], [39, 60], [39, 83], [39, 171], [40, 131], [40, 191], [41, 58], [41, 183], [41, 190], [42, 99], [43, 99], [43, 100], [43, 173], [44, 46], [44, 182], [45, 147], [45, 155], [46, 138], [47, 87], [47, 106], [48, 142], [48, 145], [48, 186], [49, 114], [49, 134], [49, 163], [50, 55], [50, 60], [50, 128], [51, 76], [51, 129], [52, 93], [53, 144], [54, 91], [54, 97], [54, 116], [55, 155], [55, 170], [56, 81], [56, 108], [57, 93], [57, 162], [58, 69], [58, 119], [59, 85], [59, 89], [59, 176], [60, 185], [61, 171], [61, 189], [62, 70], [62, 95], [62, 152], [63, 73], [63, 85], [63, 119], [64, 70], [65, 151], [65, 187], [66, 130], [66, 183], [67, 88], [67, 111], [67, 153], [68, 100], [68, 110], [68, 172], [69, 169], [70, 128], [71, 159], [71, 174], [71, 187], [72, 124], [72, 181], [72, 182], [73, 127], [74, 92], [74, 177], [74, 182], [75, 76], [75, 137], [76, 178], [77, 124], [78, 80], [78, 139], [78, 185], [79, 81], [79, 184], [80, 88], [80, 148], [81, 107], [82, 164], [82, 165], [82, 192], [83, 161], [84, 118], [84, 123], [85, 150], [86, 103], [86, 149], [86, 164], [88, 166], [89, 105], [90, 107], [90, 159], [90, 172], [91, 166], [92, 168], [93, 120], [94, 101], [94, 121], [94, 181], [95, 101], [95, 126], [96, 120], [96, 121], [97, 138], [98, 110], [98, 137], [98, 167], [101, 179], [102, 130], [102, 160], [103, 157], [103, 173], [104, 138], [104, 170], [105, 115], [105, 163], [106, 130], [106, 168], [108, 143], [108, 150], [109, 117], [109, 153], [110, 171], [112, 127], [112, 129], [112, 156], [113, 127], [113, 135], [113, 158], [114, 162], [115, 133], [117, 147], [117, 179], [119, 167], [120, 172], [121, 129], [122, 150], [122, 161], [122, 179], [123, 146], [123, 192], [124, 175], [125, 136], [125, 169], [126, 190], [132, 154], [132, 181], [132, 189], [134, 156], [134, 185], [135, 146], [135, 153], [140, 163], [140, 165], [140, 184], [141, 151], [141, 167], [143, 178], [145, 166], [146, 175], [148, 159], [148, 190], [151, 180], [152, 180], [154, 160], [154, 187], [157, 177], [160, 188], [161, 164], [168, 176], [170, 188], [174, 192], [178, 191]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_192_193.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_192_193 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
