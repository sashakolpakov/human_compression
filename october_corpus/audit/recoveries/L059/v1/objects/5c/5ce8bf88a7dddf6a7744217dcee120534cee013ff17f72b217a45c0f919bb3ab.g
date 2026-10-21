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
D:=P177Graph("VT3_208_54",208,[1, 6, 9, 12, 13, 14, 16, 18, 19, 20, 21, 22, 23, 25, 26, 30, 31, 32, 34, 35, 36, 37, 38, 39, 42, 45, 46, 49, 50, 52, 55, 56, 60, 61, 63, 65, 69, 70, 73, 76, 83, 96, 98, 99, 100, 101, 104, 105, 108, 110, 112, 115, 116, 117, 118, 120, 123, 124, 126, 128, 132, 133, 134, 135, 139, 140, 142, 143, 145, 147, 148, 150, 151, 152, 153, 154, 155, 158, 159, 160, 161, 165, 166, 167, 169, 171, 173, 174, 175, 176, 177, 179, 181, 184, 187, 188, 190, 194, 197, 198, 199, 200, 201, 202],[[1, 77], [1, 168], [1, 183], [2, 56], [2, 152], [2, 166], [3, 22], [3, 73], [3, 134], [4, 52], [4, 118], [4, 174], [5, 50], [5, 83], [5, 128], [6, 17], [6, 121], [6, 186], [7, 147], [7, 155], [7, 159], [8, 12], [8, 83], [8, 117], [9, 28], [9, 51], [9, 93], [10, 50], [10, 112], [10, 158], [11, 96], [11, 176], [11, 187], [12, 136], [12, 164], [13, 80], [13, 172], [13, 185], [14, 72], [14, 79], [14, 109], [15, 32], [15, 120], [15, 124], [16, 85], [16, 114], [16, 164], [17, 175], [17, 188], [18, 62], [18, 106], [18, 192], [19, 66], [19, 122], [19, 178], [20, 33], [20, 111], [20, 170], [21, 77], [21, 89], [21, 195], [22, 178], [22, 189], [23, 59], [23, 64], [23, 74], [24, 128], [24, 145], [24, 198], [25, 67], [25, 121], [25, 170], [26, 43], [26, 131], [26, 207], [27, 36], [27, 158], [27, 188], [28, 110], [28, 169], [29, 61], [29, 110], [29, 167], [30, 77], [30, 122], [30, 206], [31, 102], [31, 107], [31, 125], [32, 54], [32, 186], [33, 98], [33, 140], [34, 149], [34, 189], [34, 208], [35, 53], [35, 58], [35, 97], [36, 43], [36, 164], [37, 62], [37, 95], [37, 131], [38, 75], [38, 91], [38, 106], [39, 88], [39, 162], [39, 195], [40, 46], [40, 60], [40, 177], [41, 115], [41, 152], [41, 190], [42, 66], [42, 88], [42, 92], [43, 139], [44, 133], [44, 165], [44, 187], [45, 130], [45, 146], [45, 182], [46, 54], [46, 86], [47, 49], [47, 76], [47, 167], [48, 99], [48, 147], [48, 176], [49, 97], [49, 146], [50, 82], [51, 134], [51, 184], [52, 82], [52, 193], [53, 150], [53, 198], [54, 148], [55, 64], [55, 68], [55, 183], [56, 136], [56, 141], [57, 133], [57, 153], [57, 161], [58, 112], [58, 201], [59, 108], [59, 190], [60, 78], [60, 196], [61, 119], [61, 138], [62, 167], [63, 93], [63, 106], [63, 204], [64, 158], [65, 87], [65, 89], [65, 156], [66, 96], [67, 135], [67, 142], [68, 70], [68, 153], [69, 75], [69, 163], [69, 203], [70, 114], [70, 137], [71, 100], [71, 160], [71, 181], [72, 112], [72, 147], [73, 131], [73, 141], [74, 104], [74, 126], [75, 98], [76, 125], [76, 163], [78, 154], [78, 173], [79, 115], [79, 175], [80, 123], [80, 148], [81, 83], [81, 179], [81, 181], [82, 152], [84, 132], [84, 166], [84, 188], [85, 118], [85, 201], [86, 160], [86, 202], [87, 154], [87, 187], [88, 105], [89, 151], [90, 108], [90, 148], [90, 199], [91, 151], [91, 171], [92, 101], [92, 171], [93, 166], [94, 124], [94, 142], [94, 200], [95, 120], [95, 132], [96, 191], [97, 153], [98, 122], [99, 146], [99, 162], [100, 203], [100, 208], [101, 157], [101, 193], [102, 181], [102, 201], [103, 108], [103, 132], [103, 135], [104, 109], [104, 191], [105, 144], [105, 205], [107, 140], [107, 194], [109, 161], [110, 127], [111, 116], [111, 199], [113, 117], [113, 200], [113, 202], [114, 115], [116, 149], [116, 191], [117, 157], [118, 180], [119, 133], [119, 155], [120, 182], [121, 126], [123, 206], [123, 208], [124, 138], [125, 159], [126, 206], [127, 135], [127, 177], [128, 137], [129, 150], [129, 155], [129, 184], [130, 165], [130, 177], [134, 163], [136, 197], [137, 159], [138, 173], [139, 193], [139, 204], [140, 172], [141, 171], [142, 185], [143, 156], [143, 178], [143, 204], [144, 165], [144, 200], [145, 172], [145, 180], [149, 151], [150, 192], [154, 157], [156, 197], [160, 170], [161, 195], [162, 173], [168, 175], [168, 199], [169, 186], [169, 207], [174, 196], [174, 205], [176, 183], [179, 185], [179, 196], [180, 202], [182, 184], [189, 194], [190, 207], [192, 194], [197, 205], [198, 203]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_208_54.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_208_54 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
