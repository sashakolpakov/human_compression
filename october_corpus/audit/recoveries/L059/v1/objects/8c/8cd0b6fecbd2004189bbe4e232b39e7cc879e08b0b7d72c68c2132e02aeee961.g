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
D:=P177Graph("VT3_152_25",152,[1, 2, 3, 4, 5, 6, 7, 12, 18, 19, 21, 23, 26, 27, 33, 34, 35, 36, 37, 44, 45, 46, 47, 48, 52, 54, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 70, 74, 76, 79, 80, 81, 84, 86, 87, 88, 90, 94, 97, 98, 100, 105, 106, 108, 109, 112, 113, 114, 115, 117, 118, 119, 122, 123, 125, 126, 132, 135, 141, 143, 144, 146, 148, 149, 150, 152],[[1, 8], [1, 22], [1, 142], [2, 11], [2, 99], [2, 130], [3, 28], [3, 137], [3, 147], [4, 50], [4, 56], [4, 78], [5, 25], [5, 116], [5, 134], [6, 24], [6, 83], [6, 103], [7, 53], [7, 91], [7, 138], [8, 18], [8, 149], [9, 26], [9, 80], [9, 126], [10, 23], [10, 44], [10, 80], [11, 123], [11, 146], [12, 102], [12, 107], [12, 140], [13, 47], [13, 109], [13, 143], [14, 33], [14, 54], [14, 146], [15, 37], [15, 61], [15, 148], [16, 60], [16, 105], [16, 117], [17, 35], [17, 46], [17, 106], [18, 25], [18, 56], [19, 22], [19, 29], [19, 77], [20, 58], [20, 113], [20, 132], [21, 50], [21, 75], [21, 127], [22, 100], [23, 92], [23, 124], [24, 109], [24, 126], [25, 63], [26, 43], [26, 103], [27, 93], [27, 127], [27, 129], [28, 98], [28, 148], [29, 44], [29, 70], [30, 57], [30, 60], [30, 65], [31, 34], [31, 64], [31, 90], [32, 47], [32, 76], [32, 88], [33, 72], [33, 140], [34, 51], [34, 120], [35, 42], [35, 133], [36, 40], [36, 50], [36, 129], [37, 41], [37, 130], [38, 54], [38, 61], [38, 118], [39, 125], [39, 141], [39, 144], [40, 86], [40, 125], [41, 98], [41, 113], [42, 48], [42, 76], [43, 62], [43, 119], [44, 69], [45, 68], [45, 83], [45, 139], [46, 91], [46, 95], [47, 124], [48, 91], [48, 121], [49, 109], [49, 117], [49, 150], [51, 108], [51, 119], [52, 53], [52, 121], [52, 131], [53, 135], [54, 130], [55, 58], [55, 59], [55, 66], [56, 87], [57, 136], [57, 140], [58, 101], [59, 68], [59, 120], [60, 127], [61, 151], [62, 77], [62, 142], [63, 89], [63, 142], [64, 89], [64, 116], [65, 75], [65, 102], [66, 99], [66, 139], [67, 79], [67, 115], [67, 152], [68, 108], [69, 114], [69, 122], [70, 104], [70, 151], [71, 105], [71, 123], [71, 150], [72, 118], [72, 135], [73, 84], [73, 106], [73, 112], [74, 101], [74, 120], [74, 145], [75, 87], [76, 92], [77, 80], [78, 86], [78, 149], [79, 102], [79, 134], [81, 85], [81, 128], [81, 137], [82, 88], [82, 143], [82, 144], [83, 150], [84, 95], [84, 145], [85, 98], [85, 132], [86, 137], [87, 134], [88, 133], [89, 119], [90, 96], [90, 145], [92, 114], [93, 117], [93, 143], [94, 95], [94, 96], [94, 138], [96, 115], [97, 110], [97, 111], [97, 128], [99, 113], [100, 104], [100, 147], [101, 112], [103, 108], [104, 148], [105, 136], [106, 111], [107, 135], [107, 152], [110, 112], [110, 132], [111, 141], [114, 121], [115, 116], [118, 131], [122, 131], [122, 151], [123, 139], [124, 126], [125, 128], [129, 144], [133, 141], [136, 146], [138, 152], [147, 149]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_152_25.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_152_25 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
