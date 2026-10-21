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
D:=P177Graph("VT3_216_55",216,[1, 5, 6, 8, 9, 13, 15, 16, 17, 18, 22, 23, 24, 25, 26, 27, 28, 30, 31, 32, 43, 45, 50, 51, 52, 53, 57, 58, 64, 65, 67, 69, 73, 74, 75, 76, 78, 79, 84, 87, 88, 90, 92, 95, 96, 98, 99, 101, 104, 105, 108, 111, 112, 115, 116, 117, 120, 122, 124, 125, 126, 128, 129, 130, 134, 136, 137, 138, 139, 140, 142, 143, 146, 147, 149, 151, 153, 154, 155, 156, 157, 165, 166, 169, 170, 172, 174, 175, 178, 179, 181, 182, 183, 185, 186, 187, 188, 189, 190, 191, 193, 195, 196, 197, 198, 202, 213, 214],[[1, 68], [1, 145], [1, 212], [2, 67], [2, 134], [2, 151], [3, 122], [3, 130], [3, 202], [4, 32], [4, 126], [4, 188], [5, 21], [5, 47], [5, 85], [6, 12], [6, 205], [6, 208], [7, 69], [7, 183], [7, 189], [8, 34], [8, 93], [8, 207], [9, 10], [9, 160], [9, 194], [10, 125], [10, 128], [11, 16], [11, 17], [11, 96], [12, 88], [12, 96], [13, 72], [13, 118], [13, 208], [14, 74], [14, 99], [14, 193], [15, 135], [15, 145], [15, 215], [16, 113], [16, 205], [17, 121], [17, 131], [18, 82], [18, 141], [18, 194], [19, 186], [19, 197], [19, 214], [20, 26], [20, 57], [20, 181], [21, 73], [21, 191], [22, 93], [22, 152], [22, 204], [23, 70], [23, 106], [23, 176], [24, 36], [24, 37], [24, 83], [25, 80], [25, 173], [25, 205], [26, 35], [26, 164], [27, 114], [27, 150], [27, 216], [28, 41], [28, 46], [28, 48], [29, 108], [29, 174], [29, 190], [30, 54], [30, 158], [30, 184], [31, 81], [31, 85], [31, 200], [32, 63], [32, 161], [33, 45], [33, 129], [33, 155], [34, 84], [34, 188], [35, 65], [35, 112], [36, 74], [36, 183], [37, 120], [37, 193], [38, 64], [38, 101], [38, 182], [39, 108], [39, 136], [39, 198], [40, 43], [40, 69], [40, 140], [41, 137], [41, 142], [42, 96], [42, 195], [42, 213], [43, 110], [43, 159], [44, 74], [44, 105], [44, 189], [45, 168], [45, 176], [46, 146], [46, 151], [47, 172], [47, 175], [48, 65], [48, 75], [49, 147], [49, 155], [49, 190], [50, 60], [50, 159], [50, 209], [51, 135], [51, 199], [51, 212], [52, 56], [52, 110], [52, 171], [53, 133], [53, 141], [53, 211], [54, 136], [54, 189], [55, 142], [55, 185], [55, 193], [56, 92], [56, 140], [57, 152], [57, 207], [58, 59], [58, 85], [58, 150], [59, 67], [59, 146], [60, 69], [60, 136], [61, 139], [61, 143], [61, 165], [62, 112], [62, 124], [62, 187], [63, 84], [63, 125], [64, 68], [64, 80], [65, 162], [66, 99], [66, 105], [66, 178], [67, 216], [68, 130], [70, 125], [70, 169], [71, 120], [71, 170], [71, 196], [72, 78], [72, 122], [73, 150], [73, 167], [75, 103], [75, 164], [76, 91], [76, 113], [76, 131], [77, 134], [77, 154], [77, 213], [78, 94], [78, 180], [79, 109], [79, 148], [79, 199], [80, 202], [81, 175], [81, 179], [82, 116], [82, 191], [83, 166], [83, 196], [84, 106], [86, 134], [86, 187], [86, 195], [87, 89], [87, 94], [87, 102], [88, 118], [88, 163], [89, 122], [89, 126], [90, 118], [90, 144], [90, 180], [91, 143], [91, 190], [92, 132], [92, 206], [93, 214], [94, 197], [95, 144], [95, 171], [95, 192], [97, 126], [97, 130], [97, 153], [98, 106], [98, 168], [98, 207], [99, 109], [100, 112], [100, 129], [100, 181], [101, 148], [101, 212], [102, 188], [102, 214], [103, 120], [103, 142], [104, 114], [104, 192], [104, 210], [105, 184], [107, 111], [107, 138], [107, 156], [108, 158], [109, 185], [110, 111], [111, 192], [113, 139], [114, 138], [115, 132], [115, 171], [115, 180], [116, 119], [116, 167], [117, 127], [117, 176], [117, 211], [119, 149], [119, 156], [121, 124], [121, 195], [123, 124], [123, 129], [123, 147], [127, 155], [127, 174], [128, 161], [128, 215], [131, 147], [132, 197], [133, 174], [133, 198], [135, 175], [137, 200], [137, 203], [138, 167], [139, 173], [140, 201], [141, 149], [143, 158], [144, 157], [145, 153], [146, 200], [148, 178], [149, 209], [151, 162], [152, 170], [153, 161], [154, 210], [154, 216], [156, 159], [157, 163], [157, 210], [160, 172], [160, 191], [162, 187], [163, 213], [164, 170], [165, 177], [165, 184], [166, 201], [166, 206], [168, 181], [169, 194], [169, 211], [172, 215], [173, 182], [177, 178], [177, 182], [179, 199], [179, 203], [183, 201], [185, 203], [186, 204], [186, 206], [196, 204], [198, 209], [202, 208]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_216_55.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_216_55 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
