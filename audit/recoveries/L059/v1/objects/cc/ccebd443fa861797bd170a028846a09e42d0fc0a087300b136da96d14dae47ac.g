Need:=function(ok) if not ok then Error("L059 cutoff probe invalid"); fi; end;;
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


D:=P177Graph("144_046",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72],[[1, 104], [1, 108], [1, 117], [1, 121], [2, 108], [2, 117], [2, 142], [2, 143], [3, 78], [3, 81], [3, 85], [3, 109], [4, 81], [4, 82], [4, 94], [4, 126], [5, 81], [5, 85], [5, 98], [5, 130], [6, 75], [6, 82], [6, 87], [6, 94], [7, 75], [7, 84], [7, 95], [7, 99], [8, 84], [8, 99], [8, 128], [8, 132], [9, 114], [9, 119], [9, 133], [9, 136], [10, 85], [10, 106], [10, 118], [10, 124], [11, 77], [11, 89], [11, 127], [11, 128], [12, 111], [12, 113], [12, 115], [12, 117], [13, 100], [13, 114], [13, 134], [13, 139], [14, 75], [14, 88], [14, 95], [14, 135], [15, 79], [15, 128], [15, 129], [15, 132], [16, 88], [16, 114], [16, 119], [16, 138], [17, 90], [17, 95], [17, 106], [17, 118], [18, 76], [18, 77], [18, 100], [18, 127], [19, 99], [19, 111], [19, 113], [19, 122], [20, 74], [20, 111], [20, 134], [20, 139], [21, 87], [21, 90], [21, 112], [21, 122], [22, 78], [22, 100], [22, 109], [22, 114], [23, 89], [23, 112], [23, 122], [23, 144], [24, 87], [24, 90], [24, 125], [24, 138], [25, 80], [25, 92], [25, 115], [25, 117], [26, 132], [26, 133], [26, 136], [26, 144], [27, 73], [27, 74], [27, 102], [27, 108], [28, 76], [28, 93], [28, 107], [28, 119], [29, 76], [29, 100], [29, 125], [29, 135], [30, 80], [30, 96], [30, 105], [30, 137], [31, 94], [31, 118], [31, 142], [31, 143], [32, 77], [32, 131], [32, 136], [32, 141], [33, 130], [33, 132], [33, 140], [33, 144], [34, 89], [34, 105], [34, 137], [34, 144], [35, 80], [35, 96], [35, 125], [35, 138], [36, 78], [36, 80], [36, 92], [36, 120], [37, 90], [37, 93], [37, 95], [37, 139], [38, 73], [38, 74], [38, 84], [38, 112], [39, 73], [39, 93], [39, 107], [39, 113], [40, 79], [40, 86], [40, 92], [40, 129], [41, 86], [41, 88], [41, 92], [41, 135], [42, 94], [42, 118], [42, 131], [42, 141], [43, 116], [43, 130], [43, 140], [43, 143], [44, 101], [44, 120], [44, 124], [44, 126], [45, 76], [45, 101], [45, 119], [45, 120], [46, 77], [46, 104], [46, 121], [46, 136], [47, 86], [47, 96], [47, 102], [47, 108], [48, 103], [48, 124], [48, 126], [48, 140], [49, 85], [49, 124], [49, 129], [49, 137], [50, 82], [50, 106], [50, 116], [50, 123], [51, 91], [51, 110], [51, 127], [51, 133], [52, 89], [52, 98], [52, 103], [52, 128], [53, 75], [53, 87], [53, 107], [53, 134], [54, 73], [54, 103], [54, 113], [54, 140], [55, 101], [55, 109], [55, 110], [55, 141], [56, 74], [56, 98], [56, 111], [56, 130], [57, 79], [57, 97], [57, 104], [57, 105], [58, 88], [58, 116], [58, 138], [58, 143], [59, 86], [59, 96], [59, 101], [59, 109], [60, 84], [60, 110], [60, 112], [60, 141], [61, 83], [61, 121], [61, 129], [61, 137], [62, 102], [62, 115], [62, 116], [62, 123], [63, 82], [63, 91], [63, 106], [63, 110], [64, 98], [64, 103], [64, 123], [64, 142], [65, 78], [65, 91], [65, 120], [65, 131], [66, 91], [66, 99], [66, 122], [66, 131], [67, 97], [67, 104], [67, 107], [67, 134], [68, 83], [68, 97], [68, 102], [68, 115], [69, 83], [69, 97], [69, 127], [69, 133], [70, 79], [70, 81], [70, 105], [70, 126], [71, 123], [71, 125], [71, 135], [71, 142], [72, 83], [72, 93], [72, 121], [72, 139]]);;
R:=P177Census(D);;
Need(Size(R.F)=9216);;
PrintTo("quartic_cutoff_probe/144_046.g","L059Result := ",R,";\n");
Print("L059_CUTOFF_COMPLETE 144_046 ",Length(R.witnesses),"\n");
QUIT;
