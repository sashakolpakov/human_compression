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
D:=P177Graph("VT3_200_39",200,[1, 8, 9, 10, 13, 16, 17, 18, 20, 22, 24, 25, 26, 28, 30, 31, 33, 36, 42, 44, 45, 46, 47, 48, 49, 50, 51, 53, 55, 62, 63, 64, 65, 66, 67, 70, 71, 72, 73, 74, 76, 78, 79, 81, 82, 88, 93, 95, 96, 97, 100, 101, 103, 104, 107, 110, 114, 115, 116, 117, 118, 120, 121, 123, 124, 131, 132, 134, 135, 136, 137, 141, 143, 144, 146, 148, 149, 156, 158, 160, 168, 169, 170, 172, 173, 175, 176, 178, 180, 181, 182, 184, 185, 186, 187, 188, 191, 193, 194, 196],[[1, 6], [1, 19], [1, 37], [2, 31], [2, 44], [2, 173], [3, 50], [3, 72], [3, 144], [4, 156], [4, 184], [4, 191], [5, 36], [5, 101], [5, 114], [6, 33], [6, 79], [7, 82], [7, 97], [7, 176], [8, 92], [8, 106], [8, 145], [9, 35], [9, 80], [9, 157], [10, 108], [10, 128], [10, 189], [11, 49], [11, 114], [11, 144], [12, 100], [12, 121], [12, 181], [13, 41], [13, 127], [13, 171], [14, 46], [14, 96], [14, 181], [15, 46], [15, 121], [15, 172], [16, 61], [16, 84], [16, 122], [17, 59], [17, 77], [17, 111], [18, 40], [18, 119], [18, 145], [19, 24], [19, 180], [20, 89], [20, 90], [20, 126], [21, 42], [21, 116], [21, 175], [22, 34], [22, 139], [22, 166], [23, 47], [23, 73], [23, 78], [24, 162], [24, 165], [25, 87], [25, 109], [25, 162], [26, 130], [26, 140], [26, 199], [27, 82], [27, 93], [27, 186], [28, 102], [28, 157], [28, 166], [29, 96], [29, 188], [29, 193], [30, 109], [30, 125], [30, 152], [31, 140], [31, 142], [32, 62], [32, 110], [32, 185], [33, 58], [33, 159], [34, 73], [34, 172], [35, 36], [35, 71], [36, 159], [37, 97], [37, 186], [38, 62], [38, 120], [38, 148], [39, 67], [39, 79], [39, 186], [40, 141], [40, 160], [41, 53], [41, 95], [42, 94], [42, 155], [43, 63], [43, 65], [43, 168], [44, 153], [44, 200], [45, 130], [45, 133], [45, 154], [46, 92], [47, 68], [47, 98], [48, 75], [48, 94], [48, 190], [49, 89], [49, 133], [50, 133], [50, 140], [51, 52], [51, 129], [51, 161], [52, 64], [52, 146], [53, 84], [53, 198], [54, 103], [54, 180], [54, 182], [55, 83], [55, 85], [55, 197], [56, 95], [56, 124], [56, 196], [57, 67], [57, 132], [57, 184], [58, 101], [58, 180], [59, 110], [59, 191], [60, 64], [60, 76], [60, 184], [61, 63], [61, 137], [62, 199], [63, 190], [64, 197], [65, 152], [65, 177], [66, 87], [66, 125], [66, 164], [67, 105], [68, 70], [68, 118], [69, 149], [69, 168], [69, 178], [70, 91], [70, 164], [71, 90], [71, 192], [72, 142], [72, 183], [73, 86], [74, 75], [74, 119], [74, 195], [75, 175], [76, 147], [76, 161], [77, 93], [77, 158], [78, 129], [78, 139], [79, 179], [80, 115], [80, 187], [81, 109], [81, 165], [81, 174], [82, 198], [83, 117], [83, 120], [84, 176], [85, 104], [85, 146], [86, 118], [86, 121], [87, 143], [88, 150], [88, 154], [88, 155], [89, 116], [90, 114], [91, 143], [91, 194], [92, 124], [93, 105], [94, 168], [95, 122], [96, 171], [97, 165], [98, 131], [98, 135], [99, 173], [99, 185], [99, 188], [100, 163], [100, 200], [101, 151], [102, 134], [102, 187], [103, 151], [103, 183], [104, 128], [104, 167], [105, 191], [106, 141], [106, 172], [107, 119], [107, 126], [107, 192], [108, 131], [108, 170], [110, 113], [111, 185], [111, 193], [112, 136], [112, 143], [112, 182], [113, 120], [113, 156], [115, 159], [115, 179], [116, 154], [117, 150], [117, 167], [118, 163], [122, 169], [123, 138], [123, 142], [123, 200], [124, 171], [125, 170], [126, 175], [127, 158], [127, 193], [128, 178], [129, 135], [130, 148], [131, 164], [132, 147], [132, 179], [134, 139], [134, 161], [135, 189], [136, 138], [136, 183], [137, 152], [137, 174], [138, 194], [141, 166], [144, 151], [145, 196], [146, 189], [147, 187], [148, 150], [149, 155], [149, 167], [153, 181], [153, 188], [156, 197], [157, 160], [158, 198], [160, 192], [162, 182], [163, 194], [169, 190], [169, 195], [170, 177], [173, 199], [174, 176], [177, 178], [195, 196]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_200_39.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_200_39 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
