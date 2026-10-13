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
D:=P177Graph("VT3_194_17",194,[1, 2, 5, 7, 9, 10, 12, 13, 19, 21, 24, 27, 28, 32, 36, 37, 40, 44, 47, 48, 51, 52, 53, 55, 58, 59, 60, 61, 62, 65, 68, 69, 70, 73, 74, 75, 76, 77, 78, 79, 80, 81, 83, 85, 90, 92, 93, 95, 96, 97, 98, 100, 102, 103, 104, 105, 106, 107, 108, 111, 116, 118, 119, 122, 126, 128, 129, 132, 134, 138, 143, 146, 147, 148, 152, 157, 158, 159, 161, 163, 164, 165, 166, 167, 168, 170, 172, 175, 176, 177, 178, 181, 183, 185, 190, 191, 194],[[1, 115], [1, 117], [1, 187], [2, 64], [2, 86], [2, 160], [3, 90], [3, 126], [3, 178], [4, 92], [4, 128], [4, 194], [5, 34], [5, 133], [5, 155], [6, 12], [6, 111], [6, 158], [7, 127], [7, 130], [7, 131], [8, 21], [8, 28], [8, 102], [9, 45], [9, 112], [9, 189], [10, 26], [10, 89], [10, 173], [11, 28], [11, 55], [11, 85], [12, 87], [12, 154], [13, 14], [13, 49], [13, 137], [14, 175], [14, 185], [15, 21], [15, 80], [15, 96], [16, 60], [16, 104], [16, 168], [17, 53], [17, 100], [17, 159], [18, 108], [18, 148], [18, 181], [19, 22], [19, 39], [19, 130], [20, 59], [20, 69], [20, 159], [21, 153], [22, 116], [22, 146], [23, 81], [23, 166], [23, 185], [24, 72], [24, 171], [24, 180], [25, 40], [25, 59], [25, 172], [26, 104], [26, 138], [27, 84], [27, 156], [27, 180], [28, 120], [29, 44], [29, 75], [29, 181], [30, 61], [30, 79], [30, 129], [31, 95], [31, 170], [31, 191], [32, 117], [32, 125], [32, 174], [33, 76], [33, 157], [33, 170], [34, 76], [34, 146], [35, 70], [35, 107], [35, 129], [36, 50], [36, 125], [36, 187], [37, 115], [37, 145], [37, 151], [38, 65], [38, 83], [38, 175], [39, 47], [39, 164], [40, 101], [40, 141], [41, 53], [41, 126], [41, 152], [42, 65], [42, 97], [42, 98], [43, 44], [43, 176], [43, 183], [44, 123], [45, 95], [45, 177], [46, 69], [46, 100], [46, 185], [47, 127], [47, 144], [48, 109], [48, 144], [48, 153], [49, 100], [49, 126], [50, 60], [50, 118], [51, 124], [51, 136], [51, 154], [52, 101], [52, 114], [52, 136], [53, 82], [54, 62], [54, 118], [54, 176], [55, 182], [55, 187], [56, 95], [56, 111], [56, 122], [57, 61], [57, 119], [57, 146], [58, 71], [58, 82], [58, 94], [59, 114], [60, 182], [61, 130], [62, 123], [62, 154], [63, 75], [63, 78], [63, 108], [64, 92], [64, 172], [65, 149], [66, 105], [66, 152], [66, 178], [67, 76], [67, 119], [67, 191], [68, 140], [68, 149], [68, 162], [69, 186], [70, 72], [70, 156], [71, 159], [71, 165], [72, 97], [73, 99], [73, 140], [73, 174], [74, 110], [74, 127], [74, 188], [75, 162], [77, 99], [77, 117], [77, 151], [78, 91], [78, 149], [79, 131], [79, 142], [80, 86], [80, 88], [81, 160], [81, 186], [82, 157], [83, 137], [83, 140], [84, 106], [84, 177], [85, 115], [85, 193], [86, 128], [87, 118], [87, 168], [88, 161], [88, 163], [89, 96], [89, 161], [90, 99], [90, 137], [91, 97], [91, 107], [92, 141], [93, 139], [93, 141], [93, 188], [94, 122], [94, 170], [96, 120], [98, 171], [98, 192], [101, 103], [102, 109], [102, 193], [103, 124], [103, 139], [104, 112], [105, 133], [105, 145], [106, 112], [106, 173], [107, 142], [108, 142], [109, 164], [110, 143], [110, 148], [111, 189], [113, 134], [113, 143], [113, 181], [114, 165], [116, 133], [116, 184], [119, 169], [120, 138], [121, 177], [121, 190], [121, 191], [122, 150], [123, 134], [124, 134], [125, 176], [128, 153], [129, 169], [131, 148], [132, 145], [132, 184], [132, 193], [135, 147], [135, 161], [135, 167], [136, 158], [138, 182], [139, 143], [144, 194], [147, 173], [147, 180], [150, 158], [150, 165], [151, 178], [152, 155], [155, 157], [156, 190], [160, 163], [162, 183], [163, 179], [164, 184], [166, 179], [166, 192], [167, 171], [167, 179], [168, 189], [169, 190], [172, 186], [174, 183], [175, 192], [188, 194]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_194_17.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_194_17 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
