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
D:=P177Graph("VT3_168_7",168,[1, 2, 10, 13, 14, 16, 17, 20, 22, 23, 24, 25, 26, 27, 28, 34, 36, 37, 38, 40, 41, 42, 45, 46, 47, 49, 50, 51, 53, 54, 58, 59, 60, 61, 64, 65, 66, 70, 72, 73, 74, 75, 76, 78, 83, 84, 85, 87, 89, 90, 91, 92, 96, 97, 98, 99, 105, 107, 110, 111, 115, 118, 120, 127, 128, 129, 133, 135, 136, 140, 141, 142, 143, 144, 147, 151, 153, 154, 156, 158, 161, 163, 166, 167],[[1, 69], [1, 121], [1, 134], [2, 5], [2, 80], [2, 102], [3, 36], [3, 147], [3, 156], [4, 17], [4, 45], [4, 76], [5, 49], [5, 141], [6, 14], [6, 58], [6, 144], [7, 58], [7, 60], [7, 147], [8, 36], [8, 40], [8, 99], [9, 72], [9, 143], [9, 163], [10, 62], [10, 79], [10, 150], [11, 14], [11, 128], [11, 167], [12, 65], [12, 72], [12, 142], [13, 63], [13, 81], [13, 124], [14, 101], [15, 89], [15, 97], [15, 151], [16, 33], [16, 100], [16, 106], [17, 29], [17, 113], [18, 24], [18, 107], [18, 163], [19, 78], [19, 85], [19, 127], [20, 68], [20, 106], [20, 126], [21, 27], [21, 50], [21, 135], [22, 112], [22, 124], [22, 152], [23, 104], [23, 125], [23, 145], [24, 137], [24, 159], [25, 86], [25, 108], [25, 126], [26, 57], [26, 116], [26, 149], [27, 52], [27, 125], [28, 31], [28, 33], [28, 109], [29, 66], [29, 136], [30, 64], [30, 85], [30, 133], [31, 105], [31, 167], [32, 42], [32, 59], [32, 154], [33, 34], [34, 94], [34, 102], [35, 58], [35, 118], [35, 127], [36, 160], [37, 71], [37, 164], [37, 168], [38, 44], [38, 106], [38, 160], [39, 84], [39, 156], [39, 158], [40, 55], [40, 104], [41, 67], [41, 137], [41, 138], [42, 93], [42, 121], [43, 59], [43, 107], [43, 167], [44, 83], [44, 110], [45, 126], [45, 155], [46, 77], [46, 145], [46, 146], [47, 48], [47, 82], [47, 117], [48, 128], [48, 136], [49, 63], [49, 122], [50, 68], [50, 82], [51, 56], [51, 119], [51, 155], [52, 118], [52, 141], [53, 67], [53, 88], [53, 94], [54, 62], [54, 139], [54, 155], [55, 120], [55, 143], [56, 87], [56, 161], [57, 141], [57, 158], [59, 86], [60, 77], [60, 114], [61, 101], [61, 119], [61, 149], [62, 118], [63, 128], [64, 116], [64, 130], [65, 123], [65, 157], [66, 134], [66, 159], [67, 84], [68, 140], [69, 147], [69, 161], [70, 112], [70, 132], [70, 150], [71, 75], [71, 83], [72, 152], [73, 79], [73, 123], [73, 148], [74, 88], [74, 113], [74, 162], [75, 80], [75, 93], [76, 77], [76, 80], [78, 81], [78, 137], [79, 153], [81, 91], [82, 133], [83, 112], [84, 132], [85, 93], [86, 158], [87, 94], [87, 165], [88, 144], [89, 109], [89, 164], [90, 109], [90, 125], [90, 134], [91, 104], [91, 108], [92, 146], [92, 148], [92, 165], [95, 97], [95, 111], [95, 154], [96, 100], [96, 103], [96, 157], [97, 122], [98, 117], [98, 139], [98, 164], [99, 113], [99, 130], [100, 127], [101, 120], [102, 143], [103, 111], [103, 115], [105, 130], [105, 150], [107, 146], [108, 166], [110, 149], [110, 159], [111, 119], [114, 142], [114, 151], [115, 132], [115, 145], [116, 142], [117, 156], [120, 131], [121, 153], [122, 129], [123, 166], [124, 161], [129, 148], [129, 160], [131, 140], [131, 153], [133, 165], [135, 152], [135, 162], [136, 157], [138, 140], [138, 151], [139, 163], [144, 168], [154, 162], [166, 168]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_168_7.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_168_7 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
