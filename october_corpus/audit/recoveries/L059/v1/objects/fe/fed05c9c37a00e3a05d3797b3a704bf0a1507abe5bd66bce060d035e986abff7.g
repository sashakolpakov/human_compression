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
D:=P177Graph("VT3_162_21",162,[1, 5, 8, 9, 11, 12, 14, 15, 16, 18, 20, 21, 23, 25, 27, 28, 31, 32, 34, 35, 41, 43, 45, 46, 48, 49, 50, 51, 55, 57, 58, 59, 60, 61, 62, 69, 70, 71, 74, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 87, 88, 90, 91, 93, 95, 102, 103, 104, 107, 108, 109, 113, 117, 118, 120, 121, 124, 125, 126, 127, 130, 135, 139, 142, 144, 145, 146, 150, 155, 161, 162],[[1, 75], [1, 106], [1, 147], [2, 8], [2, 31], [2, 78], [3, 32], [3, 78], [3, 107], [4, 5], [4, 48], [4, 51], [5, 86], [5, 158], [6, 15], [6, 85], [6, 126], [7, 34], [7, 127], [7, 150], [8, 40], [8, 63], [9, 10], [9, 105], [9, 136], [10, 58], [10, 118], [11, 24], [11, 119], [11, 154], [12, 36], [12, 38], [12, 111], [13, 81], [13, 109], [13, 142], [14, 68], [14, 123], [14, 132], [15, 72], [15, 89], [16, 30], [16, 54], [16, 148], [17, 28], [17, 77], [17, 82], [18, 42], [18, 52], [18, 132], [19, 61], [19, 139], [19, 144], [20, 66], [20, 72], [20, 137], [21, 22], [21, 94], [21, 97], [22, 25], [22, 125], [23, 54], [23, 66], [23, 98], [24, 81], [24, 155], [25, 65], [25, 151], [26, 49], [26, 71], [26, 146], [27, 53], [27, 65], [27, 119], [28, 29], [28, 101], [29, 126], [29, 161], [30, 91], [30, 155], [31, 56], [31, 105], [32, 40], [32, 147], [33, 43], [33, 48], [33, 84], [34, 129], [34, 138], [35, 98], [35, 134], [35, 141], [36, 69], [36, 90], [37, 46], [37, 79], [37, 104], [38, 45], [38, 130], [39, 62], [39, 95], [39, 139], [40, 77], [41, 134], [41, 157], [41, 159], [42, 50], [42, 80], [43, 128], [43, 138], [44, 51], [44, 84], [44, 103], [45, 53], [45, 140], [46, 54], [46, 137], [47, 109], [47, 135], [47, 146], [48, 133], [49, 73], [49, 106], [50, 92], [50, 123], [51, 99], [52, 58], [52, 145], [53, 81], [55, 110], [55, 115], [55, 148], [56, 58], [56, 80], [57, 101], [57, 111], [57, 153], [59, 64], [59, 141], [59, 157], [60, 66], [60, 122], [60, 141], [61, 89], [61, 153], [62, 128], [62, 143], [63, 80], [63, 82], [64, 121], [64, 150], [65, 130], [67, 77], [67, 90], [67, 93], [68, 79], [68, 88], [69, 116], [69, 140], [70, 105], [70, 149], [70, 159], [71, 133], [71, 158], [72, 108], [73, 74], [73, 76], [74, 75], [74, 129], [75, 107], [76, 133], [76, 138], [78, 149], [79, 148], [82, 92], [83, 94], [83, 136], [83, 151], [84, 143], [85, 131], [85, 137], [86, 88], [86, 120], [87, 97], [87, 143], [87, 156], [88, 115], [89, 95], [90, 101], [91, 98], [91, 154], [92, 161], [93, 116], [93, 147], [94, 118], [95, 112], [96, 102], [96, 107], [96, 121], [97, 103], [99, 120], [99, 145], [100, 125], [100, 130], [100, 144], [102, 149], [102, 157], [103, 160], [104, 123], [104, 131], [106, 117], [108, 112], [108, 122], [109, 110], [110, 155], [111, 144], [112, 127], [113, 134], [113, 152], [113, 154], [114, 117], [114, 142], [114, 146], [115, 135], [116, 117], [118, 160], [119, 124], [120, 132], [121, 129], [122, 150], [124, 151], [124, 152], [125, 156], [126, 153], [127, 128], [131, 161], [135, 158], [136, 162], [139, 156], [140, 142], [145, 160], [152, 162], [159, 162]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_162_21.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_162_21 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
