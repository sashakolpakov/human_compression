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
D:=P177Graph("VT3_168_89",168,[1, 5, 6, 7, 8, 9, 10, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 164, 165, 166, 167, 168],[[1, 2], [1, 3], [1, 4], [2, 5], [2, 6], [3, 7], [3, 9], [4, 8], [4, 10], [5, 11], [5, 13], [6, 12], [6, 14], [7, 15], [7, 19], [8, 16], [8, 20], [9, 17], [9, 21], [10, 18], [10, 22], [11, 23], [11, 27], [12, 24], [12, 28], [13, 25], [13, 29], [14, 26], [14, 30], [15, 31], [15, 39], [16, 32], [16, 40], [17, 33], [17, 41], [18, 34], [18, 42], [19, 35], [19, 43], [20, 36], [20, 44], [21, 37], [21, 45], [22, 38], [22, 46], [23, 47], [23, 55], [24, 48], [24, 56], [25, 49], [25, 57], [26, 50], [26, 58], [27, 51], [27, 59], [28, 52], [28, 60], [29, 53], [29, 61], [30, 54], [30, 62], [31, 63], [31, 79], [32, 64], [32, 80], [33, 65], [33, 81], [34, 66], [34, 82], [35, 67], [35, 83], [36, 68], [36, 84], [37, 69], [37, 85], [38, 70], [38, 86], [39, 71], [39, 87], [40, 72], [40, 88], [41, 73], [41, 89], [42, 74], [42, 90], [43, 75], [43, 91], [44, 76], [44, 92], [45, 77], [45, 93], [46, 78], [46, 94], [47, 95], [47, 111], [48, 96], [48, 112], [49, 97], [49, 113], [50, 98], [50, 114], [51, 99], [51, 115], [52, 100], [52, 116], [53, 101], [53, 117], [54, 102], [54, 118], [55, 103], [55, 119], [56, 104], [56, 120], [57, 105], [57, 121], [58, 106], [58, 122], [59, 107], [59, 123], [60, 108], [60, 124], [61, 109], [61, 125], [62, 110], [62, 126], [63, 125], [63, 127], [64, 105], [64, 126], [65, 110], [65, 138], [66, 116], [66, 139], [67, 118], [67, 140], [68, 120], [68, 128], [69, 121], [69, 141], [70, 117], [70, 129], [71, 122], [71, 142], [72, 119], [72, 130], [73, 96], [73, 123], [74, 110], [74, 131], [75, 114], [75, 132], [76, 108], [76, 141], [77, 128], [77, 133], [78, 97], [78, 106], [79, 115], [79, 124], [80, 134], [80, 142], [81, 113], [81, 135], [82, 107], [82, 140], [83, 111], [83, 129], [84, 98], [84, 125], [85, 102], [85, 130], [86, 99], [86, 133], [87, 104], [87, 131], [88, 100], [88, 135], [89, 101], [89, 134], [90, 103], [90, 132], [91, 105], [91, 136], [92, 111], [92, 137], [93, 95], [93, 116], [94, 96], [94, 127], [95, 143], [97, 154], [98, 155], [99, 156], [100, 144], [101, 157], [102, 145], [103, 158], [104, 146], [106, 147], [107, 148], [108, 157], [109, 144], [109, 149], [112, 150], [112, 158], [113, 151], [114, 156], [115, 145], [117, 146], [118, 149], [119, 147], [120, 151], [121, 150], [122, 148], [123, 152], [124, 153], [126, 143], [127, 143], [128, 161], [129, 162], [130, 146], [131, 159], [132, 157], [133, 160], [134, 163], [135, 156], [136, 152], [136, 161], [137, 154], [137, 159], [138, 153], [138, 162], [139, 155], [139, 163], [140, 151], [141, 148], [142, 160], [144, 166], [145, 167], [147, 164], [149, 165], [150, 168], [152, 166], [153, 164], [154, 167], [155, 168], [158, 165], [159, 166], [160, 165], [161, 164], [162, 168], [163, 167]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_168_89.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_168_89 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
