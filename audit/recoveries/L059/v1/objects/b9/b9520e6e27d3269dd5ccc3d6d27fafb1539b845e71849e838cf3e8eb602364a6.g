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
D:=P177Graph("VT3_168_78",168,[1, 3, 6, 8, 11, 13, 14, 15, 16, 17, 18, 20, 21, 22, 24, 25, 29, 30, 34, 35, 37, 39, 43, 44, 45, 46, 49, 50, 52, 53, 54, 55, 57, 60, 62, 65, 67, 71, 72, 78, 79, 83, 84, 85, 88, 89, 90, 91, 92, 95, 97, 98, 99, 110, 112, 113, 114, 115, 116, 117, 118, 119, 120, 122, 124, 125, 126, 127, 128, 129, 130, 131, 133, 134, 138, 139, 145, 147, 148, 152, 153, 154, 163, 164],[[1, 66], [1, 74], [1, 136], [2, 72], [2, 120], [2, 147], [3, 66], [3, 111], [3, 121], [4, 52], [4, 60], [4, 83], [5, 54], [5, 95], [5, 127], [6, 12], [6, 58], [6, 165], [7, 54], [7, 116], [7, 130], [8, 51], [8, 146], [8, 162], [9, 34], [9, 52], [9, 84], [10, 35], [10, 85], [10, 88], [11, 40], [11, 132], [11, 144], [12, 83], [12, 84], [13, 64], [13, 73], [13, 159], [14, 74], [14, 123], [14, 165], [15, 93], [15, 106], [15, 168], [16, 23], [16, 36], [16, 96], [17, 80], [17, 158], [17, 166], [18, 26], [18, 109], [18, 132], [19, 43], [19, 126], [19, 152], [20, 61], [20, 63], [20, 166], [21, 59], [21, 100], [21, 135], [22, 36], [22, 101], [22, 157], [23, 72], [23, 116], [24, 105], [24, 151], [24, 160], [25, 64], [25, 76], [25, 103], [26, 46], [26, 112], [27, 99], [27, 110], [27, 117], [28, 138], [28, 148], [28, 164], [29, 64], [29, 75], [29, 156], [30, 108], [30, 140], [30, 141], [31, 99], [31, 138], [31, 153], [32, 65], [32, 78], [32, 115], [33, 37], [33, 98], [33, 122], [34, 59], [34, 81], [35, 41], [35, 51], [36, 54], [37, 73], [37, 156], [38, 125], [38, 133], [38, 164], [39, 123], [39, 136], [39, 149], [40, 49], [40, 110], [41, 43], [41, 45], [42, 67], [42, 115], [42, 163], [43, 167], [44, 103], [44, 157], [44, 159], [45, 70], [45, 82], [46, 144], [46, 156], [47, 49], [47, 99], [47, 154], [48, 91], [48, 114], [48, 133], [49, 142], [50, 68], [50, 87], [50, 167], [51, 119], [52, 109], [53, 96], [53, 107], [53, 140], [55, 56], [55, 80], [55, 143], [56, 89], [56, 128], [57, 61], [57, 81], [57, 160], [58, 127], [58, 130], [59, 97], [60, 132], [60, 149], [61, 131], [62, 94], [62, 151], [62, 162], [63, 112], [63, 145], [65, 77], [65, 86], [66, 134], [67, 69], [67, 93], [68, 126], [68, 127], [69, 113], [69, 122], [70, 119], [70, 128], [71, 75], [71, 76], [71, 166], [72, 140], [73, 129], [74, 152], [75, 112], [76, 139], [77, 79], [77, 120], [78, 104], [78, 141], [79, 105], [79, 150], [80, 139], [81, 145], [82, 134], [82, 152], [83, 123], [84, 135], [85, 167], [85, 168], [86, 124], [86, 163], [87, 90], [87, 95], [88, 93], [88, 146], [89, 94], [89, 158], [90, 137], [90, 168], [91, 103], [91, 155], [92, 111], [92, 143], [92, 161], [94, 119], [95, 101], [96, 114], [97, 150], [97, 160], [98, 142], [98, 144], [100, 116], [100, 147], [101, 118], [102, 113], [102, 115], [102, 154], [104, 153], [104, 154], [105, 124], [106, 122], [106, 129], [107, 133], [107, 148], [108, 148], [108, 153], [109, 145], [110, 149], [111, 164], [113, 142], [114, 157], [117, 121], [117, 136], [118, 137], [118, 159], [120, 141], [121, 138], [124, 162], [125, 143], [125, 155], [126, 165], [128, 161], [129, 137], [130, 135], [131, 151], [131, 158], [134, 161], [139, 155], [146, 163], [147, 150]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_168_78.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_168_78 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
